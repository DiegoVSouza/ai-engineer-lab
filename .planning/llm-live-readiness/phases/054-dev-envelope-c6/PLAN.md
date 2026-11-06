# Plan

1. Freeze baseline (policy 9b195344...), authorization and plan-check; commit before applying.
2. Clone the c5 migration as `migrate_free_envelope_c6.py`; extend the account guard and the P00 allocation table to total 493 with campaign `free-dev-c6`; `free-dev-c5` becomes immutable; the final stage reads `phases/053-p00-final-run/AUTHORIZATION.json` (created only when the candidate is frozen).
3. Tests, dry-run, `--apply`, then P00 full fake gate, catalog preflight and the development pass in batches of at most ten trials.

allowed_write_paths: `.planning/llm-live-readiness/phases/054-dev-envelope-c6/**`, `.planning/llm-live-readiness/AUTHORIZATION.md`, `scripts/harness/migrate_free_envelope_c6.py`, `scripts/harness/test_migrate_free_envelope_c6.py`, `scripts/harness/live_free_account.py`, `scripts/harness/test_live_free_account.py`, `shared/policies/groq-free-campaign.json`, `artifacts/evidence/llm-live-readiness/envelope-c6/**`, `.runtime/llm-live-readiness/` migration files named by the script.
forbidden_changes: usage ledgers, historical campaigns, credentials, other projects, confirmation reserve, pricing/model/per-call caps.
Budget in this phase: zero provider calls. max_tries: 3.
