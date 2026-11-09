# Plan

1. Tests first in `scripts/harness/test_live_free_account.py` for the new branch (admitted with a valid authorization, 24 cap, blocked without or with a modified authorization, other campaign names and p02 `local-operation-v1` unchanged, other projects unchanged). Run them red.
2. Add `_p02_campaigns()` and the branch in `live_free_account.py`; the P05 and P02 authorization checks share one helper without changing P05 behaviour.
3. Write and commit `AUTHORIZATION.json`; rerun the root tests (baseline 83 OK).

allowed_write_paths: `.planning/llm-live-readiness/phases/058-p02-live-campaign/**`, `scripts/harness/live_free_account.py`, `scripts/harness/test_live_free_account.py`, `artifacts/evidence/llm-live-readiness/p02-dev-campaign/**`.
forbidden_changes: usage ledgers, `shared/policies/**`, other projects' guards, credentials, holdout and confirmation reserves.
Budget: zero provider calls in this phase. max_tries: 3.
