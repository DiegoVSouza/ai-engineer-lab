# Plan

1. Tests first in `scripts/harness/test_live_free_account.py` for the new branch (admitted with a valid authorization, 64 cap, blocked without or with a modified authorization, other campaign names and p05 `local-operation-v1` unchanged, other projects unchanged).
2. Add `_p05_campaigns()` and the branch in `live_free_account.py`.
3. Write and commit `AUTHORIZATION.json`; rerun the root tests (baseline 79 OK).

allowed_write_paths: `.planning/llm-live-readiness/phases/057-p05-live-campaign/**`, `scripts/harness/live_free_account.py`, `scripts/harness/test_live_free_account.py`, `artifacts/evidence/llm-live-readiness/p05-dev-campaign/**`.
forbidden_changes: usage ledgers, `shared/policies/**`, other projects' guards, credentials, holdout and confirmation reserves.
Budget: zero provider calls in this phase. max_tries: 3.
