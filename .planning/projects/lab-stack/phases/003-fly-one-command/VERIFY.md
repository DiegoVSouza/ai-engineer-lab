# Verification

PASS for the code and documentation scope, 2026-10-30. A real deploy stays INCOMPLETE: not authorized and not run. No mutating Fly command ran; `-Action Status` and `-DryRun` issued only read calls against the real account.

| Command (cwd: lab root) | Exit | Evidence |
| --- | --- | --- |
| `python -m pytest -q scripts/harness/test_stack_cli.py scripts/harness/test_fly_ops.py` before the code | 1 (13 failed, 4 passed, expected red) | `artifacts/evidence/lab-stack/fly-one-command-003/red-first.txt` |
| same, attempt 1 | 1 (2 failed) | `pytest-attempt1.txt` |
| same, attempt 2 | 0 (17 passed) | `pytest-attempt2.txt` |
| `pwsh -File ops/fly/deploy.ps1 -Action Up -DryRun` | 0 | `dry-run-up.txt` |
| `pwsh -File ops/fly/deploy.ps1 -Action Down -DryRun` | 0 | `dry-run-down.txt` |
| `pwsh -File ops/fly/deploy.ps1 -Action Status` | 0 | `status-real-readonly.txt` |
| `Get-Help` and `stack.py --help` | 0 | `help.txt` |

Attempt 1 found two real defects, both fixed at the cause. `Wait-ForHealthyApp` piped a single wrapped array, so `Up` could never see a healthy machine. Flags were forwarded out of order. The red run also confirmed that `stack.py down --volumes`, as documented earlier, was rejected by argparse.
