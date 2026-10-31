#!/usr/bin/env python3
"""Restore live local dumps into a disposable database and compare row counts.

Dumps stay in memory and only counts are printed, because they hold private data.
"""
import json
from pathlib import Path
import subprocess
import sys
import time
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[2]
SOURCE = 'supportops-lab-postgres-1'
IMAGE = 'pgvector/pgvector:0.8.7-pg16'
DATABASES = ('p04', 'p05', 'keycloak')
TABLES = "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE' ORDER BY 1"


def exec_psql(container, user, database, sql):
    result = subprocess.run(['docker', 'exec', container, 'psql', '-U', user, '-d', database, '-tAc', sql],
                            capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise RuntimeError(result.stderr.strip()[:300])
    return result.stdout.strip()


def counts(container, user, database):
    tables = exec_psql(container, user, database, TABLES).split()
    return {table: int(exec_psql(container, user, database, f'SELECT count(*) FROM "{table}"')) for table in tables}


def main():
    container = f'lab-restore-check-{uuid4().hex[:8]}'
    subprocess.run(['docker', 'run', '-d', '--rm', '--name', container, '--label', 'lab.owner=restore-check',
                    '--pull=never', '--network', 'none', '--tmpfs', '/var/lib/postgresql/data',
                    '-e', 'POSTGRES_HOST_AUTH_METHOD=trust', IMAGE], check=True, capture_output=True)
    report = {}
    try:
        for _ in range(60):
            if subprocess.run(['docker', 'exec', container, 'psql', '-U', 'postgres', '-c', 'SELECT 1'], capture_output=True).returncode == 0:
                break
            time.sleep(1)
        time.sleep(2)
        for database in DATABASES:
            before = counts(SOURCE, 'lab_admin', database)
            dump = subprocess.run(['docker', 'exec', SOURCE, 'pg_dump', '-U', 'lab_admin', '-Fc', database],
                                  capture_output=True, timeout=300, check=True).stdout
            exec_psql(container, 'postgres', 'postgres', f'CREATE DATABASE {database}')
            restored = subprocess.run(['docker', 'exec', '-i', container, 'pg_restore', '-U', 'postgres', '-d', database,
                                       '--no-owner', '--no-privileges', '--exit-on-error'], input=dump, capture_output=True, timeout=300)
            if restored.returncode:
                raise RuntimeError(f'{database}: {restored.stderr.decode(errors="replace")[:300]}')
            after = counts(container, 'postgres', database)
            report[database] = {'tables': len(after), 'rows': sum(after.values()), 'dump_bytes': len(dump)}
            if not after or before != after:
                raise RuntimeError(f'{database}: restored counts differ')
    finally:
        subprocess.run(['docker', 'rm', '-f', '-v', container], capture_output=True)
    print(json.dumps({'status': 'PASS', **report}))
    return 0


if __name__ == '__main__':
    sys.exit(main())
