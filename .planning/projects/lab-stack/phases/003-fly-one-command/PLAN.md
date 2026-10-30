# Plan

1. Tests first: `scripts/harness/test_fly_ops.py` drives the scripts against a fake `fly` executable (`FLY_BIN`) and pins allowlist, ordering, exit codes and destroy confirmation; `scripts/harness/test_stack_cli.py` pins argument forwarding.
2. Add `ops/fly/stack-apps.ps1` (inventory, allowlist, `Invoke-Fly`), and rebuild `deploy.ps1` and `power.ps1` on it. Make `stack.py` forward Compose flags and add `fly-up`, `fly-down`, `fly-status`.
3. Document side by side in `README.md` and `docs/knowledge/self-hosted-stack.md`.

allowed_write_paths: `ops/fly/*.ps1`, `scripts/stack.py`, `scripts/harness/test_fly_ops.py`, `scripts/harness/test_stack_cli.py`, `README.md`, `docs/knowledge/self-hosted-stack.md`, `.planning/projects/lab-stack/**`, `artifacts/evidence/lab-stack/fly-one-command-003/**`.

forbidden_changes: real `fly deploy|apps create|volumes create|machine *|scale|secrets|apps destroy`; any app outside the allowlist; committing secrets; `harness-kit/`.

llm_mode: fake (no model involved). budget: USD 0, no Fly mutation. validation: `python -m pytest -q scripts/harness/test_fly_ops.py scripts/harness/test_stack_cli.py`.

stop conditions: three failed attempts on one failure, or any need to reach the real Fly API with a mutating call.
