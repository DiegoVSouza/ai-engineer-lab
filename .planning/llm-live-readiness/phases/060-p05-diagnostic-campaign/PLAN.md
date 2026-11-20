# Plan

1. Tests first in `scripts/harness/test_live_free_account.py` for the diagnostic and holdout branches (admitted only by their own exact, committed authorization; the development authorization never opens them).
2. Add the two authorization constants and the merged `_p05_campaigns()` in `live_free_account.py`.
3. Commit `AUTHORIZATION.json`; rerun the root live tests.

allowed_write_paths: `.planning/llm-live-readiness/phases/060-p05-diagnostic-campaign/**`, `.planning/llm-live-readiness/phases/061-p05-holdout-campaign/**`, `scripts/harness/live_free_account.py`, `scripts/harness/test_live_free_account.py`, `artifacts/evidence/llm-live-readiness/p05-diag-holdout-guard/**`.
forbidden_changes: usage ledgers, `shared/policies/**`, other projects' guards, credentials.
Budget: zero provider calls in this phase.
