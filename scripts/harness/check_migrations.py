#!/usr/bin/env python3
"""Prove P05 and P04 migrations run up, down and up in a disposable database."""
import json
from pathlib import Path
import subprocess
import sys
import time
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[2]
IMAGE = 'pgvector/pgvector:0.8.7-pg16'
P05 = ROOT/'projects/p05/migrations'
P04 = ROOT/'projects/p04'
SETS = {
    'p05': ([P05/'002_pgvector_knowledge.sql', P05/'003_product_state.sql', P05/'004_authorization_lease.sql'],
            [P05/'down/004_authorization_lease.sql', P05/'down/003_product_state.sql', P05/'down/002_pgvector_knowledge.sql']),
    'p04': ([P04/'supportops_async/store/migrations/001_tasks.sql'], [P04/'infra/postgres/001_tasks.down.sql']),
}
QUERY = "SELECT count(*) FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE'"


def psql(container, database, *arguments, stdin=None):
    return subprocess.run(['docker', 'exec', '-i', container, 'psql', '-U', 'postgres', '-d', database,
                           '-v', 'ON_ERROR_STOP=1', '-q', *arguments],
                          input=stdin, capture_output=True, text=True, timeout=60)


def apply(container, database, files):
    for path in files:
        result = psql(container, database, stdin=path.read_text(encoding='utf-8'))
        if result.returncode:
            raise RuntimeError(f'{path.name}: {result.stderr.strip()[:300]}')


def tables(container, database):
    return int(psql(container, database, '-tAc', QUERY).stdout.strip())


def main():
    container = f'lab-migration-check-{uuid4().hex[:8]}'
    subprocess.run(['docker', 'run', '-d', '--rm', '--name', container, '--label', 'lab.owner=migration-check',
                    '--pull=never', '--network', 'none', '-e', 'POSTGRES_HOST_AUTH_METHOD=trust', IMAGE],
                   check=True, capture_output=True)
    report = {}
    try:
        for _ in range(60):
            if psql(container, 'postgres', '-c', 'SELECT 1').returncode == 0:
                break
            time.sleep(1)
        psql(container, 'postgres', '-c', 'SELECT 1').check_returncode()
        time.sleep(2)
        for name, (up, down) in SETS.items():
            psql(container, 'postgres', '-c', f'CREATE DATABASE {name}').check_returncode()
            apply(container, name, up)
            first = tables(container, name)
            apply(container, name, down)
            after_down = tables(container, name)
            apply(container, name, up)
            report[name] = {'tables_up': first, 'tables_down': after_down, 'tables_up_again': tables(container, name)}
            if not first or after_down or report[name]['tables_up_again'] != first:
                raise RuntimeError(f'{name}: cycle did not return to the expected state: {report[name]}')
    finally:
        subprocess.run(['docker', 'rm', '-f', container], capture_output=True)
    print(json.dumps({'status': 'PASS', **report}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
