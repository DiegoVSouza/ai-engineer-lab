# Plan

1. CPU limits in Compose. `infra/logging` in the P04 and P05 images, with `--log-config` in `fly/*.toml`.
2. nginx `stub_status`, exporter service, Prometheus job. `traceparent` from the console, checked by `stack.py check`.
3. Renewal e2e, `scripts/harness/restore_rehearsal.py`, then `fly-up`, Fly e2e, and a rollback of the web app and forward again.
4. Update the readiness document and knowledge notes.

allowed_write_paths: `docker-compose.yml`, `ops/stack/**`, `fly/**`, `ops/fly/**`, `scripts/harness/**`, `README.md`, `docs/**`, `.planning/**`, `artifacts/evidence/lab-stack/remaining-readiness-008/**`, `artifacts/evidence/fly/**`, P04 `infra/logging/**` and `Dockerfile`, P05 `infra/logging/**` and `Dockerfile`, `projects/p06/**`.

forbidden_changes: P04 fingerprinted paths, `stack.py down --volumes`, deleting volumes, push, database dumps in Git or evidence, resources outside `supportops-lab`, `lab-restore-check` and the stack's Fly inventory.

llm_mode: fake. budget: running Fly machines. validation: `python scripts/harness/production_readiness.py`, `python scripts/e2e_fly.py`. stop conditions: three failed attempts on one failure.
