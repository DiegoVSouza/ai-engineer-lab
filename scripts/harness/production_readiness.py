#!/usr/bin/env python3
"""Check the running root stack item by item and save the result as evidence."""
import json
from pathlib import Path
import re
import subprocess
import sys
from urllib.error import URLError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'artifacts/evidence/lab-stack/production-readiness-005'
PROJECT = 'supportops-lab'
RUNNING = ('api', 'worker', 'mcp', 'p04-api', 'p04-worker', 'web', 'web-metrics', 'postgres', 'keycloak', 'redis',
           'localstack', 'otel', 'jaeger', 'prometheus', 'grafana')
NO_HEALTHCHECK = {'otel': 'image has no shell or HTTP client',
                  'web-metrics': 'image has no shell or HTTP client; Prometheus scrapes it',
                  'p04-worker': 'no port; liveness shown by the stack check processing a task'}
JSON_LOGS = ('api', 'mcp', 'p04-api', 'web')
SECRET = re.compile(r'gsk_[A-Za-z0-9]{20,}|hf_[A-Za-z0-9]{20,}|sk-or-[A-Za-z0-9-]{20,}|-----BEGIN [A-Z ]*PRIVATE KEY')
REPOSITORIES = ('.', 'projects/p05', 'projects/p06')


def run(*command):
    result = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace')
    return result.returncode, result.stdout, result.stderr


def inspect(service):
    code, out, _ = run('docker', 'inspect', f'{PROJECT}-{service}-1')
    if code:
        raise RuntimeError(f'{service} is not running')
    return json.loads(out)[0]


def http(url):
    try:
        with urlopen(url, timeout=5) as response:
            return response.status, response.read().decode()
    except URLError as error:
        return getattr(error, 'code', 0), str(error)


def health():
    details = {}
    for service in RUNNING:
        state = inspect(service)['State']
        details[service] = state.get('Health', {}).get('Status') or NO_HEALTHCHECK.get(service, 'MISSING')
    bad = [name for name, value in details.items() if value not in ('healthy', *NO_HEALTHCHECK.values())]
    return not bad, details


def readiness():
    web = http('http://localhost:48080/readyz')
    return web[0] == 200 and 'ready' in web[1], {'web_readyz': web}


def migrations():
    code, out, err = run(sys.executable, 'scripts/harness/check_migrations.py')
    return code == 0, {'exit_code': code, 'output': (out + err).strip()[:500]}


def logs():
    details = {}
    for service in JSON_LOGS:
        lines = run('docker', 'logs', '--tail', '20', f'{PROJECT}-{service}-1')
        rows = [line for line in (lines[1] + lines[2]).splitlines() if line.strip().startswith('{')]
        total = [line for line in (lines[1] + lines[2]).splitlines() if line.strip()]
        valid = 0
        for row in rows:
            try:
                json.loads(row)
                valid += 1
            except ValueError:
                pass
        details[service] = {'json_lines': valid, 'lines': len(total)}
    return all(item['lines'] and item['json_lines'] / item['lines'] >= 0.9 for item in details.values()), details


def metrics():
    status, body = http('http://localhost:49090/api/v1/targets?state=active')
    targets = json.loads(body)['data']['activeTargets'] if status == 200 else []
    details = {item['labels']['job']: item['health'] for item in targets}
    return bool(details) and all(value == 'up' for value in details.values()), details


def tracing():
    status, body = http('http://localhost:46686/api/services')
    services = json.loads(body).get('data') or [] if status == 200 else []
    return {'p05-api', 'p05-worker'} <= set(services) or any('p05' in name for name in services), {'services': services}


def limits():
    details = {service: {key: inspect(service)['HostConfig'][key] for key in ('Memory', 'NanoCpus')} for service in RUNNING}
    return all(all(item.values()) for item in details.values()), details


def restart():
    details = {service: inspect(service)['HostConfig']['RestartPolicy']['Name'] for service in RUNNING}
    return all(value == 'unless-stopped' for value in details.values()), details


def secrets():
    details = {}
    clean = True
    for repository in REPOSITORIES:
        base = ROOT/repository
        code, out, _ = run('git', '-C', str(base), 'ls-files')
        hits = []
        for name in out.splitlines():
            path = base/name
            if path.suffix in ('.sqlite', '.tar', '.woff2', '.png', '.whl') or not path.is_file():
                continue
            if SECRET.search(path.read_text(encoding='utf-8', errors='ignore')):
                hits.append(name)
        details[repository] = {'tracked_files': len(out.splitlines()), 'secret_hits': hits}
        clean = clean and code == 0 and not hits
    ignored = run('git', 'check-ignore', '.env')[0] == 0
    details['env_ignored'] = ignored
    environment = {service: [item.split('=')[0] for item in inspect(service)['Config']['Env'] if item.startswith('GROQ')]
                   for service in ('api', 'worker', 'web')}
    details['provider_keys_in_containers'] = environment
    return clean and ignored and not any(environment.values()), details


def restore():
    code, out, err = run(sys.executable, 'scripts/harness/restore_rehearsal.py')
    return code == 0, {'exit_code': code, 'output': (out + err).strip()[:600]}


def rollback():
    document = ROOT/'docs/harness/lab-stack/production-readiness.md'
    text = document.read_text(encoding='utf-8') if document.exists() else ''
    restart_log = OUT/'restart-cycle.json'
    cycle = json.loads(restart_log.read_text()) if restart_log.exists() else {}
    return '## Rollback' in text and cycle.get('status') == 'PASS', {'plan': document.name, 'restart_cycle': cycle}


CHECKS = {'health': health, 'readiness': readiness, 'migrations': migrations, 'structured_logs': logs,
          'metrics': metrics, 'tracing': tracing, 'resource_limits': limits, 'restart_policy': restart,
          'secrets': secrets, 'restore': restore, 'rollback': rollback}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    report = {}
    for name, check in CHECKS.items():
        try:
            passed, details = check()
        except Exception as error:
            passed, details = False, {'error': str(error)[:300]}
        report[name] = {'status': 'PASS' if passed else 'FAIL', 'details': details}
        print(f"{report[name]['status']} {name}")
    (OUT/'checklist.json').write_text(json.dumps(report, indent=2, ensure_ascii=False)+'\n', encoding='utf-8', newline='\n')
    return 0 if all(item['status'] == 'PASS' for item in report.values()) else 1


if __name__ == '__main__':
    sys.exit(main())
