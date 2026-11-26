# Verification

Status: INCOMPLETE until fake gates and live smoke evidence are recorded.

| Check | Command | Exit | Evidence |
|---|---|---:|---|
| Root authorization guard regressions | `python -m pytest scripts/harness/test_live_free_account.py -q` | 0 | `artifacts/evidence/framework-smokes-root-tests.txt` |
| P01 project test suite | `uv run --group frameworks --with pytest pytest tests -q` | 0 | `projects/p01/artifacts/evidence/framework-smoke-tests.txt` |
| Frozen live smoke, max 20 requests | PENDING | PENDING | `artifacts/evidence/p01-framework-smoke-run.txt` |
