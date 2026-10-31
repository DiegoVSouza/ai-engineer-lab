# Verification

PASS — 2026-10-31. Code and rehearsal items closed. Verdict stays not ready for real customers; the remainder needs owner decisions.

| Command | Exit | Evidence (`artifacts/evidence/lab-stack/remaining-readiness-008/` unless noted) |
| --- | --- | --- |
| `python scripts/stack.py up`, `check` (lab root) | 0, 0 | `up.txt`, `check.txt` |
| `python scripts/stack.py fly-up` (lab root), complete in one run | 0 | `fly-up.txt` |
| `fly deploy --image <previous>`, then `--image <new>` on `supportops-lab-web` | 0, 0, `/readyz` 200 both ways | `fly-rollback.txt` |
| `python scripts/e2e_fly.py` (projects/p06), on the final state | 0, 3 passed, renewal skipped there | `e2e-fly.txt` |
| `E2E_RENEWAL=1 python scripts/e2e.py` (projects/p06), local | 0, 4 passed | P06 `artifacts/evidence/blockers-002/e2e-renewal.txt` |
| `python scripts/harness/restore_rehearsal.py` (lab root) | 0 | `checklist.json` under production-readiness-005 |
| `python scripts/harness/production_readiness.py` (lab root) | 0, 11 items | `readiness-run.txt` |
| `scripts/check_services.py` in `p05-gate-033` | 0 | P05 `artifacts/evidence/console-blockers-033/` |

Fly JSON logs were read from `fly logs` for P05, P04 and MCP (`fly-json-logs.txt`). Token renewal was proven against the local stack, not Fly. No P04 worker failure after the deploy finished.
