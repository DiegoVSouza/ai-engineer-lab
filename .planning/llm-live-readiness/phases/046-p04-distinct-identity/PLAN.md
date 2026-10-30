# Plan

1. Bind the exact new P04 identity to committed phase045 authorization, retaining exact prior-history and reservation checks.
2. Add offline tests for scope, authorization tampering, completed operation and no-replay; execute locked regressions and record evidence.
3. Commit the guard before P04 prepares its own controller and isolated gate.

allowed_write_paths: `scripts/harness/live_free_account.py`, `scripts/harness/test_p01_p04_revalidation.py`, `.planning/llm-live-readiness/phases/046-p04-distinct-identity/**`, `artifacts/evidence/llm-live-readiness/p04-distinct-identity-046/**`.

forbidden_changes: policy, ledgers, reservations, old authority, receipts, manifests, credentials, provider/live calls, Docker, paid usage, fallback, holdout or human evaluation. Fake/offline only; stop on identity/history mismatch. Plan-check is implementer self-assessment.
