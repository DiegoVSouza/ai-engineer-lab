# Plan

1. Freeze baseline (policy 7ffc4192...), authorization and plan-check; commit before applying.
2. Clone the c7 migration as `migrate_free_envelope_c8.py`; extend the account guard and the P00 allocation table to total 755 with campaign `free-dev-c8`; `free-dev-c7` becomes immutable.
3. Tests, dry-run and `--apply` today with zero provider calls. The Groq pass and the final run happen after the free daily window reopens (about 14:10 UTC on 2026-11-07), following `projects/p00/docs/harness/runbook-2026-11-07.md`.

allowed_write_paths: `.planning/llm-live-readiness/phases/056-dev-envelope-c8/**`, `.planning/llm-live-readiness/AUTHORIZATION.md`, `scripts/harness/migrate_free_envelope_c8.py`, `scripts/harness/test_migrate_free_envelope_c8.py`, `scripts/harness/live_free_account.py`, `scripts/harness/test_live_free_account.py`, `shared/policies/groq-free-campaign.json`, `artifacts/evidence/llm-live-readiness/envelope-c8/**`, `.runtime/llm-live-readiness/` migration files named by the script.
forbidden_changes: usage ledgers, historical campaigns, credentials, other projects, confirmation reserve, pricing/model/per-call caps.
Budget in this phase: zero provider calls. max_tries: 3.
