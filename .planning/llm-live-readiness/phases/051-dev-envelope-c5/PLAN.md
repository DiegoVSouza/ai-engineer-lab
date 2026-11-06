# Plan

1. Freeze baseline (policy 7184ffe3...), authorization and plan-check; commit before applying.
2. Clone the c4 migration as `migrate_free_envelope_c5.py`; extend the account guard and the P00 allocation table to total 301 with campaign `free-dev-c5`; `free-dev-c4` becomes immutable.
3. Tests, committed-source dry-run, `--apply`, then P00 full fake gate, catalog preflight and one funded pass in batches of at most ten.

allowed_write_paths: `.planning/llm-live-readiness/phases/051-dev-envelope-c5/**`, `.planning/llm-live-readiness/AUTHORIZATION.md`, `scripts/harness/migrate_free_envelope_c5.py`, `scripts/harness/test_migrate_free_envelope_c5.py`, `scripts/harness/live_free_account.py`, `scripts/harness/test_live_free_account.py`, `shared/policies/groq-free-campaign.json`, `artifacts/evidence/llm-live-readiness/envelope-c5/**`, `.runtime/llm-live-readiness/` migration files named by the script.
forbidden_changes: usage ledgers, historical campaigns, credentials, other projects, holdout/confirmation, pricing/model/per-call caps.
Budget in this phase: zero provider calls. max_tries: 3.
