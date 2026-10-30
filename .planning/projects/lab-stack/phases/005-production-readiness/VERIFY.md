# Verification

PASS for the checklist; overall verdict is **not ready for real customers**, see `docs/harness/lab-stack/production-readiness.md`.

| Command (cwd: lab root) | Exit | Evidence (`artifacts/evidence/lab-stack/production-readiness-005/`) |
| --- | --- | --- |
| `python scripts/harness/check_migrations.py` | 0 | `checklist.json` |
| `python scripts/harness/restart_cycle.py`, attempt 1 | 1, anonymous volumes leaked on every `down` | `restart-cycle-attempt1.json` |
| `python scripts/harness/restart_cycle.py`, attempt 2 after `tmpfs` | 0 | `restart-cycle.json` |
| `python scripts/stack.py check` after restart, and after the final compose change | 0, 0 | `check-after-restart.txt`, `check-final.txt` |
| `python scripts/e2e.py` in `projects/p06` after restart | 0 | `e2e-after-restart.txt` |
| `python scripts/harness/production_readiness.py` | 0 | `checklist.json`, `readiness-run.txt` |
| `python scripts/stack.py checkout` | 0 | `checkout.txt` |

Attempt 1 of the restart cycle found a real leak: LocalStack and Jaeger images declare `VOLUME`, and each `down` orphaned one anonymous volume per service. Their data is ephemeral by design, so `tmpfs` replaces them. Removing the three orphans created here was refused by the permission mode and is left to the owner.
