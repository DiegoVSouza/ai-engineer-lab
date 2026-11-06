# Plan

1. Freeze baseline (policy ed9fb42c...), authorization and plan-check; commit before applying.
2. Clone the c6 migration as `migrate_free_envelope_c7.py`; extend the account guard and the P00 allocation table to total 685 with campaign `free-dev-c7`; `free-dev-c6` becomes immutable.
3. Tests, dry-run, `--apply`, P00 full fake gate, catalog preflight, then the development pass in batches of at most ten trials.

allowed_write_paths: `.planning/llm-live-readiness/phases/055-dev-envelope-c7/**`, `.planning/llm-live-readiness/AUTHORIZATION.md`, `scripts/harness/migrate_free_envelope_c7.py`, `scripts/harness/test_migrate_free_envelope_c7.py`, `scripts/harness/live_free_account.py`, `scripts/harness/test_live_free_account.py`, `shared/policies/groq-free-campaign.json`, `artifacts/evidence/llm-live-readiness/envelope-c7/**`, `.runtime/llm-live-readiness/` migration files named by the script.
forbidden_changes: usage ledgers, historical campaigns, credentials, other projects, confirmation reserve, pricing/model/per-call caps.
Budget in this phase: zero provider calls. max_tries: 3.
