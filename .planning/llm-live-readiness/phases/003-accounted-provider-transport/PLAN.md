# Plan

- allowed_write_paths: `.planning/llm-live-readiness/phases/003-accounted-provider-transport/**`, `scripts/harness/live_provider_transport.py`, `scripts/harness/test_live_provider_transport.py`, `scripts/harness/live_free_account.py` (catalog over the same in-memory numbered key set, model-mismatch stop and read-only reservation preview), `artifacts/evidence/llm-live-readiness/provider-transport/**`.
- llm_mode: fake for simulated HTTP; the live protocol requires explicit live mode and a project-owned enabled/synthetic execution manifest. No production project writes/generation in this foundation phase.
- forbidden_changes: `.env`, product sources/artifacts/configs, account caps/policy, existing services, datasets/rubrics, public effects, paid usage and raw provider logs/cassettes.
- Validation: tests for reservation-before-request, exact full-payload bounds, model/usage/schema failures, transport/quota, no automatic retries, sanitized headers/errors, owner opt-in and metadata-only session startup; run prior guard regressions plus lint/format/compile.
- Stop condition: no owning-project opt-in or unreviewed transport contract. Generation remains inaccessible to existing project CLIs until separately integrated.

1. Define owner opt-in and a finite single-attempt protocol with provider preflight and byte-based conservative input reservation including framing overhead.
2. Implement/test the provider session and normalization/error boundary over the existing account guard; reserve before HTTP and complete before returning an observation.
3. Run regressions, capture evidence/limits and review/commit explicit paths. Human review stays pending; do not imply model quality from fixtures.

Plan review: accepted. A persistent stdin/stdout session avoids repeated catalog calls and keeps keys only in memory. Every generation attempt has its own ledger reservation; retries are disabled. Project integration must use a subprocess rather than importing sibling/root implementation into a product runtime.
