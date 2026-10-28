# Plan

1. Add unnumbered credential selection with stable slot zero, secret-value deduplication and offline regressions.
2. Run locked account/transport suites and record evidence. No actual credentials or provider are accessed; free-tier eligibility of the new credential remains unverified before live use.

allowed_write_paths: `.planning/llm-live-readiness/phases/024-unnumbered-credential/**`, `scripts/harness/live_free_account.py`, `scripts/harness/test_live_free_account.py`, `artifacts/evidence/llm-live-readiness/unnumbered-credential-024/**`. forbidden_changes: live ledger, policy, budgets, historical candidates, secrets, model requests and completion retries. USD 0; fake fixtures only. Fingerprint changes invalidate historical C2 resume. Self-assessed plan-check; independent review pending. Research: https://console.groq.com/docs/rate-limits specifies organization limits and Retry-After; https://github.com/groq/groq-python#retries documents default SDK retries. This custom transport retains no automatic completion replay because uncertain attempts have no spare funding.
