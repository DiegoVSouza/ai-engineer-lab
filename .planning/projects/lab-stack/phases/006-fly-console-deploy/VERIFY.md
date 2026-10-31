# Verification

PASS — 2026-10-31. Console published at https://supportops-lab-web.fly.dev and accepted from outside.

| Command | Exit | Evidence (`artifacts/evidence/fly/console-deploy-006/`) |
| --- | --- | --- |
| `python scripts/stack.py fly-up` (cwd: lab root) | 1, stopped at the P04 health wait after all apps deployed | `fly-up-attempt1.txt` |
| `python scripts/e2e_fly.py` (cwd: projects/p06), attempt 1 | 1, client not applied yet | `e2e-fly-attempt1.txt` |
| `pwsh -File ops/fly/deploy.ps1 -Action Reconcile` | 0, client applied, three public probes 200 | `reconcile-attempt1.txt` |
| `pwsh -File ops/fly/deploy.ps1 -Action Deploy -Only supportops-lab-sns,supportops-lab-web` | 0 | `deploy-sns-web.txt` |
| `python scripts/e2e_fly.py`, attempt 2 | 1, axe ran before the sign-in screen rendered | `e2e-fly-attempt2.txt` |
| `python scripts/e2e_fly.py`, attempt 3 | 0, 2 passed | `e2e-fly-attempt3.txt` |
| `python -m pytest -q scripts/harness/test_fly_ops.py scripts/harness/test_stack_cli.py` | 0 | `pytest.txt` |

The background task reported exit 0 because the command ended in `tee`; the recorded exit of `fly-up` is 1.

Defects found by the real deploy, each fixed at the cause:

1. `Wait-ForHealthyApp`, which phase 003 had extended to autostop apps, cannot succeed reliably because those machines stop at idle. `Up` now judges them by real HTTP probes, which also wake them.
2. LocalStack listened on IPv4 only and `.internal` resolves to IPv6, so the P04 worker failed every few seconds with `worker_failure`. `GATEWAY_LISTEN` now binds `[::]:4566`. No worker failure logged since 03:54:30Z.
3. Console `/readyz` timed out at 5 seconds while P05 woke from cold. Now 15 seconds.
4. `-Only a,b` through `pwsh -File` arrived as one string and the allowlist refused it. The list is now split before the check.

The e2e change only waits for the sign-in screen before running axe; no assertion was removed.
