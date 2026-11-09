# Plan

1. Tests first in `scripts/harness/test_live_free_account.py` for the new branch (admitted with a valid authorization, 76 cap, blocked without or with a modified authorization, other campaign names and the reviewed revalidation scope unchanged, other projects unchanged). Run them red and save the output.
2. Add `_p01_campaigns()` and the branch in `live_free_account.py`, reusing `_authorized_campaign`.
3. Write and commit `AUTHORIZATION.json`; rerun the root tests (baseline 87 OK).

allowed_write_paths: `.planning/llm-live-readiness/phases/059-p01-live-campaign/**`, `scripts/harness/live_free_account.py`, `scripts/harness/test_live_free_account.py`, `artifacts/evidence/llm-live-readiness/p01-dev-campaign/**`.
forbidden_changes: usage ledgers, `shared/policies/**`, other projects' guards, credentials, holdout and confirmation reserves.
Budget: zero provider calls in this phase. max_tries: 3.
