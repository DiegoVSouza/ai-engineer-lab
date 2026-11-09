# Verify

Status: PASS (guard only; zero provider calls in this phase). Evidence in `artifacts/evidence/llm-live-readiness/p01-dev-campaign/`.

- [x] New guard tests fail before the change (`tests-before-guard.txt`: 5 selected tests, 3 errors, the campaign was refused with `reviewed_revalidation_scope_required`) and pass after.
- [x] `python -m unittest discover -s scripts/harness -p "test_live_*.py"` passes: 91 tests OK (`tests-after-guard.txt`; baseline 87 plus 4 new).
- [x] `AUTHORIZATION.json` committed (`5f8cfa6`) and unmodified (checked by the guard through `git ls-files` and `git diff --quiet HEAD`).
- [x] The reviewed-revalidation scope, the p01 992/996 diagnostics branch and the p00, p02, p03, p04 and p05 guards are untouched; the "other projects" test asserts each one still refuses `p01-dev-v1`.
- The test helper `reserve` gained an optional `call` argument (default 1) so one test can reserve several provider calls per case.
