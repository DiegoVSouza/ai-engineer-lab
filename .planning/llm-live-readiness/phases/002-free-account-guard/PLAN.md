# Plan

- allowed_write_paths: `.planning/llm-live-readiness/phases/002-free-account-guard/**`, `.planning/llm-live-readiness/AUTHORIZATION.md`, `.gitignore` (ignore only runtime coordination metadata), `scripts/harness/live_free_account.py`, `scripts/harness/test_live_free_account.py`, `shared/policies/groq-free-campaign.json`, `artifacts/evidence/llm-live-readiness/free-account-guard/**`. Runtime locks/registry at `.runtime/llm-live-readiness/**` are untracked references only, never authoritative usage; tests use temporary roots.
- llm_mode: fake for tests and inventory; live only for authenticated GET model-catalog metadata. No generation in this phase.
- forbidden_changes: `.env` writes, secret-bearing evidence, product sources/artifacts, existing service stacks, kit, datasets/rubrics/holdout, public/external effects and paid usage.
- Validation: standard-library tests with synthetic project trees/databases; CLI dry-run with no credentials/provider; metadata preflight against fixed HTTPS Groq endpoint. Capture commands/exits/sanitized output, preserving errors.
- Stop condition: model inaccessible, unexpected response, absent numbered keys or unsafe accounting input. No generation fallback and no inferred human approval.

1. Record the new free-only authorization, sourced ceiling/pricing policy and finite campaign/project maxima from existing reservation inventory.
2. Implement/test the machine lease, append-only per-project provider-attempt accounting and aggregate minute/day/cumulative checks; unknown usage remains charged.
3. Implement credential-free dry-run and sanitized authenticated catalog preflight, record evidence/limitations, inspect staged paths and commit locally.

Plan review: accepted. The helper is Builder orchestration and imports no project source. It cannot initialize production project databases in this phase; synthetic tests alone exercise writes. The current rate/pricing sources are official Groq documentation. Metadata preflight proves model access, not account billing tier or available daily tokens. Project integration remains explicit follow-up work.
