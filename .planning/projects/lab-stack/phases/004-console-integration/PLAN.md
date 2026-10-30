# Plan

1. Add `ops/stack/idp_clients.py`, the Compose services, the port, and extend `ops/stack/tools.py`.
2. Add `fly/web/fly.toml`, the inventory entry, start/stop order, and the client step in `deploy.ps1`.
3. Save the Docker inventory, run `python scripts/stack.py up`, then `check`, then the browser e2e against the real stack. Named volumes and unrelated resources stay untouched.
4. Document in README and the Portuguese guide.

allowed_write_paths: `docker-compose.yml`, `.env.example`, `ops/stack/idp_clients.py`, `ops/stack/tools.py`, `ops/stack/projects.lock.json`, `fly/web/**`, `ops/fly/*.ps1`, `scripts/stack.py`, `scripts/harness/test_fly_ops.py`, `scripts/harness/test_stack_cli.py`, `README.md`, `docs/knowledge/self-hosted-stack.md`, `docs/harness/**`, `.planning/projects/lab-stack/**`, `artifacts/evidence/lab-stack/console-integration-004/**`.

forbidden_changes: `stack.py down --volumes`, stopping or removing anything outside Compose project `supportops-lab`, real Fly mutations, secrets in Git or evidence, `harness-kit/`.

llm_mode: fake. budget: USD 0. validation: `python scripts/stack.py up`, `python scripts/stack.py check`, `npm run e2e` in `projects/p06`.

stop conditions: three failed attempts on one failure, or any change that would put existing stack data at risk.
