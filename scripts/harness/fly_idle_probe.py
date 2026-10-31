#!/usr/bin/env python3
"""Watch the Fly stack go idle, then time how long one request takes to wake it."""
import json
from pathlib import Path
import subprocess
import sys
import time
from urllib.error import URLError
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT/'artifacts/evidence/lab-stack/fly-autostop-009/idle-probe.json'
APPS = ('db', 'redis', 'idp', 'sns', 'jaeger', 'mcp', 'p04', 'p05', 'web')
TIMEOUT = 2700


def states():
    result = {}
    for app in APPS:
        output = subprocess.run(['fly', 'machine', 'list', '--app', f'supportops-lab-{app}', '--json'],
                                capture_output=True, text=True, timeout=60).stdout
        result[app] = sorted(machine['state'] for machine in json.loads(output))
    return result


def main():
    started = time.monotonic()
    samples = []
    while True:
        current = states()
        elapsed = round(time.monotonic() - started)
        samples.append({'seconds': elapsed, 'running': [app for app, value in current.items() if 'started' in value]})
        print(elapsed, samples[-1]['running'], flush=True)
        if not samples[-1]['running'] or elapsed > TIMEOUT:
            break
        time.sleep(60)
    all_stopped = not samples[-1]['running']
    wake = None
    if all_stopped:
        began = time.monotonic()
        while time.monotonic() - began < 300:
            try:
                with urlopen('https://supportops-lab-web.fly.dev/readyz', timeout=60) as response:
                    if response.status == 200:
                        wake = round(time.monotonic() - began, 1)
                        break
            except (URLError, OSError):
                pass
            time.sleep(2)
    report = {'all_stopped': all_stopped, 'seconds_until_all_stopped': samples[-1]['seconds'], 'wake_seconds': wake,
              'after_wake': states(), 'samples': samples}
    OUT.write_text(json.dumps(report, indent=2)+'\n', encoding='utf-8', newline='\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'samples'}))
    return 0 if all_stopped and wake is not None else 1


if __name__ == '__main__':
    sys.exit(main())
