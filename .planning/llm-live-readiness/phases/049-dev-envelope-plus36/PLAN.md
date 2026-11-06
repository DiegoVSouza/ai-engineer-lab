# Plan

1. Freeze baseline policy (`f8428a8d...`), authorization and plan-check; commit before applying.
2. Clone the plus13 migration as `migrate_free_envelope_plus36.py` (own append-only audit DB, committed-input checks, leases, pending marker, read-only ledger continuity) with the +36 delta and the new policy hash.
3. Run migration tests, committed-source dry-run, then `--apply`; verify UUIDs, ledger prefixes and unknown reserves are unchanged.
4. P00 follow-up (own phase): owner review state in dataset v2/config, candidate freeze, dry-run, then the 36-trial pass.

allowed_write_paths: `.planning/llm-live-readiness/phases/049-dev-envelope-plus36/**`, `.planning/llm-live-readiness/AUTHORIZATION.md`, `scripts/harness/migrate_free_envelope_plus36.py`, `scripts/harness/test_migrate_free_envelope_plus36.py`, `shared/policies/groq-free-campaign.json`, `artifacts/evidence/llm-live-readiness/envelope-plus36/**`, `.runtime/llm-live-readiness/ledger-references.json` (policy hash only), `.runtime/llm-live-readiness/policy-migrations-plus36.sqlite*`, `.runtime/llm-live-readiness/policy-migration.pending`, `.runtime/llm-live-readiness/ledger-references.policy-migration.tmp`, `.runtime/llm-live-readiness/account.lock`, `.runtime/llm-live-readiness/campaign.lock`.
forbidden_changes: usage ledgers, historical campaigns, credentials, other projects' allocations, holdout/confirmation, pricing/model/per-call caps, provider calls.
Budget: zero provider calls, USD 0 in this phase. max_tries: 3.
