# Verification

PASS — 2026-10-30, local scope. `fly-up` was validated by dry run and by `fly config validate --strict`, never executed.

| Command (cwd: lab root) | Exit | Evidence (`artifacts/evidence/lab-stack/console-integration-004/`) |
| --- | --- | --- |
| `python scripts/stack.py up`, attempts 1, 2, 3 | 0, 0, 0 | `up-attempt*.txt` |
| `python scripts/stack.py check`, final | 0 | `check-attempt2.txt` |
| `python -m pytest -q scripts/harness/test_fly_ops.py scripts/harness/test_stack_cli.py` | 0 | `pytest.txt` |
| Inventory and data comparison | see | `inventory-diff.txt`, `p05-rows-*.txt` |

Browser e2e evidence lives in P06 `artifacts/evidence/console-001/`. Inventory shows only `supportops-lab` containers recreated or added; all named volumes kept and P05 rows only grew.
