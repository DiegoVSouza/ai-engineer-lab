# Plan

1. Preflight, then `python scripts/stack.py fly-up`.
2. Fix at the cause anything that stops the deploy, and repeat only what failed.
3. Run the e2e against the public URL and record the result.

allowed_write_paths: `ops/fly/*.ps1`, `fly/**`, `scripts/harness/test_fly_ops.py`, `README.md`, `docs/knowledge/self-hosted-stack.md`, `docs/harness/lab-stack/**`, `ops/stack/projects.lock.json`, `.planning/projects/lab-stack/**`, `artifacts/evidence/fly/console-deploy-006/**`, `projects/p06/**`.

forbidden_changes: apps outside the inventory, destroying volumes or data, plan upgrades, real customer data, live model calls, secrets in Git or evidence.

llm_mode: fake. budget: running Fly machines, stopped with `fly-down`. validation: `python scripts/e2e_fly.py` in `projects/p06`. stop conditions: three failed attempts on one failure.
