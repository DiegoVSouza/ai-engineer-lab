# Plan

1. Freeze baseline (policy 3d40c818...), authorization and plan-check; commit before applying.
2. Clone the plus36 migration as `migrate_free_envelope_c4.py` with the +10 delta and the new hash; make the account guard and P00 allocation table cover total 265 with campaign `free-dev-c4`; `free-dev-c3` becomes immutable.
3. Run migration and guard tests, committed-source dry-run, then `--apply`; verify UUIDs, prefixes and unknown reserves.
4. P00: full fake gate, catalog preflight, then one funded pass of `free-dev-c4` in batches of at most ten.

allowed_write_paths: `.planning/llm-live-readiness/phases/050-dev-envelope-c4/**`, `.planning/llm-live-readiness/AUTHORIZATION.md`, `scripts/harness/migrate_free_envelope_c4.py`, `scripts/harness/test_migrate_free_envelope_c4.py`, `scripts/harness/live_free_account.py`, `scripts/harness/test_live_free_account.py`, `shared/policies/groq-free-campaign.json`, `artifacts/evidence/llm-live-readiness/envelope-c4/**`, `.runtime/llm-live-readiness/` migration files named by the script.
forbidden_changes: usage ledgers, historical campaigns, credentials, other projects' allocations, holdout/confirmation, pricing/model/per-call caps.
Budget in this phase: zero provider calls. max_tries: 3.
