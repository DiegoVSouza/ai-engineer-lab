# Verification

Status: PRE-APPLY PASS; apply pending. No provider call, no credential access.

Pre-apply evidence:
- Exact delta: `artifacts/evidence/llm-live-readiness/envelope-plus36/plan-validation.txt` (PASS_EXACT_DELTA, old f8428a8d..., new 3d40c818...).
- Account guard rewritten for the 255 total in `scripts/harness/live_free_account.py`: only `local-live-operation-v1` (10 calls) and `free-dev-c3` (36 calls) can spend; any other campaign, including holdout and confirmation, raises `protected_p00_allocation`; a non-ok completed attempt stops further calls (`prior_operational_failure_requires_review`). Three new tests in `test_live_free_account.py`; the file passes (36 tests).
- P00 side (`projects/p00`, commit b7f1395 then 0b401cd): allocation table keyed by policy total (219 and 255), scope gate per envelope, binding check, dry-run reserve and revalidation-audit handling for the new hash; 12 new tests in `tests/llm/test_allocation_plus36.py`. P00 `tests/llm`: 136 passed; fast gate OK.
- Migration clone `migrate_free_envelope_plus36.py`: 14 tests pass; pinned P00 campaign source blob 0b401cd.
- Whole harness suite: 319 tests, 2 failures in `test_fly_ops` (`idp_clients.py` expected in Fly script output), unrelated to policy or budget.
- 12 tests in `projects/p00/tests/test_live_campaign_preparation.py` need the applied state (policy and registry hash must match) and are re-run after apply.

Budget interpretation: `authorized_paid_spend_usd` stays 0.00 (free-plan keys); USD 5.00 is an owner total-loss ceiling recorded in AUTHORIZATION.json. Independent review is WAIVED_BY_OWNER, not independently verified.
