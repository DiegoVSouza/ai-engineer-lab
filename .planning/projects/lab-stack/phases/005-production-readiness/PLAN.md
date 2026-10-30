# Plan

1. Compose: memory limits on every long-running service, health checks for Grafana and Prometheus, JSON logs on the uvicorn services.
2. P05 `/readyz`, P05 and P04 down migrations, `scripts/harness/check_migrations.py` against a disposable database.
3. `scripts/harness/production_readiness.py`, a real `down` and `up` restart, `persistence`, `check` and e2e.
4. `docs/harness/lab-stack/production-readiness.md`, with rollback and the open items.

allowed_write_paths: `docker-compose.yml`, `ops/stack/**`, `scripts/stack.py`, `scripts/harness/check_migrations.py`, `scripts/harness/production_readiness.py`, `scripts/harness/test_stack_cli.py`, `README.md`, `docs/knowledge/**`, `docs/harness/lab-stack/**`, `.planning/**`, `artifacts/evidence/lab-stack/production-readiness-005/**`, P05 and P04 paths listed in their own plans.

forbidden_changes: `stack.py down --volumes`, resources outside `supportops-lab` and the disposable namespace `lab-migration-check`, real Fly mutations, weakening a check to pass.

llm_mode: fake. budget: USD 0. validation: `python scripts/harness/production_readiness.py`. stop conditions: three failed attempts on one failure.
