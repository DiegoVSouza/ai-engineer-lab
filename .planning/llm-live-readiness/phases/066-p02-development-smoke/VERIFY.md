# Verification

Status: INCOMPLETE until the live campaign evidence is recorded.

| Check | Command | Exit | Evidence |
|---|---|---:|---|
| Root account guard regressions | `python -m pytest scripts/harness/test_live_free_account.py -q` | 0 | `artifacts/evidence/framework-smokes-root-tests.txt` |
| P02 project test suite | `python -m pytest tests -q` | 0 | `projects/p02/artifacts/evals/live/p02-dev-v4-smoke/fake-checks.txt` |
| Candidate freeze and live run | PENDING | PENDING | `artifacts/evidence/p02-dev-v4-smoke-run.txt` |
