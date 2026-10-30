#!/usr/bin/env python3
"""Prove `stack.py down` then `up` keeps data and leaves other Compose projects alone."""
import json
from pathlib import Path
import subprocess
import sys
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'artifacts/evidence/lab-stack/production-readiness-005'
QUERY = 'select kind,count(*) from platform_objects group by kind order by kind'


def text(*command):
    return subprocess.run(command, cwd=ROOT, capture_output=True, text=True, encoding='utf-8', errors='replace').stdout


def inventory():
    rows = text('docker', 'ps', '-a', '--no-trunc', '--format', '{{.ID}}|{{.Names}}|{{.Label "com.docker.compose.project"}}').splitlines()
    return {'foreign_containers': sorted(row for row in rows if not row.endswith('|supportops-lab')),
            'volumes': sorted(text('docker', 'volume', 'ls', '--format', '{{.Name}}').splitlines())}


def rows():
    return text('docker', 'exec', 'supportops-lab-postgres-1', 'psql', '-U', 'lab_admin', '-d', 'p05', '-tAc', QUERY).split()


def stack(action):
    result = subprocess.run([sys.executable, 'scripts/stack.py', action], cwd=ROOT, capture_output=True, text=True,
                            encoding='utf-8', errors='replace')
    (OUT/f'restart-{action}.txt').write_text(result.stdout+result.stderr, encoding='utf-8', newline='\n')
    return result.returncode


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    before, data_before = inventory(), rows()
    down = stack('down')
    gone = not text('docker', 'ps', '-a', '--filter', 'label=com.docker.compose.project=supportops-lab', '-q').strip()
    during = inventory()
    up = stack('up') if down == 0 else None
    data_after, after = rows(), inventory()
    persistence = stack('persistence') if up == 0 else None
    ready = urlopen('http://localhost:48080/readyz', timeout=10).status if up == 0 else None
    report = {'down_exit': down, 'containers_removed': gone, 'up_exit': up, 'persistence_exit': persistence,
              'console_ready_status': ready, 'p05_rows_before': data_before, 'p05_rows_after': data_after,
              'volumes_unchanged': before['volumes'] == during['volumes'] == after['volumes'],
              'foreign_containers_unchanged': before['foreign_containers'] == during['foreign_containers'] == after['foreign_containers'],
              'foreign_container_count': len(before['foreign_containers'])}
    report['status'] = 'PASS' if (down == 0 and gone and up == 0 and persistence == 0 and ready == 200
                                  and data_before == data_after and report['volumes_unchanged']
                                  and report['foreign_containers_unchanged']) else 'FAIL'
    (OUT/'restart-cycle.json').write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps(report))
    return 0 if report['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
