# Plan — authenticated rate-limit preflight

## Tasks

1. Inspect the official header contract and existing catalog/account guard APIs; plan-check and commit this SDD before code.
2. Parse only allowlisted numeric response headers, aggregate the shared-account minima, feed the result to the in-memory shared guard before registration/dispatch, and add offline tests for lower request/token limits, remaining capacity, reset windows, absent/malformed headers, multiple shared keys and no credential disclosure. Preserve existing durable POST feedback behavior.
3. Run the locked root account/transport tests and P00 full gate because P00 fingerprints root account/transport sources. Save exact commands/outputs; review staged diff/secrets; commit root guard separately, then re-run and recommit the P00 candidate with its changed root fingerprint before any authenticated preflight.

allowed_write_paths:
- `.planning/llm-live-readiness/phases/006-authenticated-rate-limit-preflight/**`
- `artifacts/evidence/llm-live-readiness/authenticated-rate-limit-preflight/**`
- `scripts/harness/live_free_account.py`
- `scripts/harness/live_provider_transport.py`
- `scripts/harness/test_live_free_account.py`
- `scripts/harness/test_live_provider_transport.py`
- `.planning/llm-live-readiness/STATUS.md`

forbidden_changes: policy, authorization, budgets, ledger/registry/audit/runtime data, provider completions, P00 candidate source until this root commit exists, sibling projects, project data/rubrics/graders/prompts, dependency locks, secrets, paid use, fallback, key rotation, retries, public actions.

Validation:
- `python -S -m unittest discover -s scripts/harness -p test_live_free_account.py -v`
- `python -S -m unittest discover -s scripts/harness -p test_live_provider_transport.py -v`
- `projects/p00/.venv/Scripts/python.exe scripts/check_full.py` from P00 with its phase-owned `P00_PYTEST_BASETEMP` override.
- Fake response tests must prove lower authenticated limits stop reservation before HTTP completion; no credential or network use in tests.

Budget: zero provider completions during implementation; later P00 C2 maximum remains 36, shared primary/confirmation budgets unchanged, paid USD 0. Stop on unexpected provider access, any durable-ledger/registry mutation, or inability to preserve existing limits.
