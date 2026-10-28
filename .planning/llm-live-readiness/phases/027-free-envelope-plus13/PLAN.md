# Plan

1. Record explicit authorization, exact immutable baseline/proposal and plan-check self-assessment; commit planning before code.
2. Build a narrow +13 migration from the existing same-repository migration contract with its own append-only audit DB, committed-input/owner checks, shared leases, pending marker, crash recovery/idempotency and read-only ledger continuity. Update slot-0 eligibility guard to require the recorded attestation, with injected tests. Preserve historical +10 behavior and audit.
3. Coordinate P00 phase 028's exact primary/candidate binding and run locked root migration/account/transport plus P00 focused controls. Commit validated inputs before actual metadata application. The actual policy/registry-dependent P00 full gate follows application immediately; pre-apply mismatch intentionally denies read-only allocation. P01 remains disabled and its locked full consumer regression follows the final committed root transport.
4. Dry-run and apply the explicitly authorized migration, verify prefixes/UUIDs/unknown reserves and protected allocations, reconcile coordination docs and commit evidence. Generation requires separate owning candidate freeze/preflight and all current execution gates.

allowed_write_paths:
- .planning/llm-live-readiness/phases/027-free-envelope-plus13/**
- .planning/llm-live-readiness/AUTHORIZATION.md
- .planning/llm-live-readiness/STATUS.md
- .planning/llm-live-readiness/WORK.md
- .planning/llm-live-readiness/EXECUTOR-HANDOFF.md
- .planning/llm-live-readiness/SPEC.md
- .planning/llm-live-readiness/VERIFY.md
- scripts/harness/migrate_free_envelope_plus13.py
- scripts/harness/test_migrate_free_envelope_plus13.py
- scripts/harness/test_migrate_free_envelope.py (pin historical fixture source, preserve historical migration semantics)
- scripts/harness/live_provider_transport.py
- scripts/harness/test_live_provider_transport.py
- shared/policies/groq-free-campaign.json
- artifacts/evidence/llm-live-readiness/envelope-plus13/**
- .runtime/llm-live-readiness/ledger-references.json (atomic policy hash only)
- .runtime/llm-live-readiness/policy-migrations-plus13.sqlite*
- .runtime/llm-live-readiness/policy-migration.pending
- .runtime/llm-live-readiness/ledger-references.policy-migration.tmp
- .runtime/llm-live-readiness/account.lock
- .runtime/llm-live-readiness/campaign.lock

forbidden_changes: provider/logical usage ledgers, historical campaigns/results/manifests/private answers, original +10 audit/helper semantics, credentials, other project allocations, paid/model/pricing/per-call/free-rate caps, holdout, kit, Docker/stacks, provider calls in this migration phase and fabricated review.

Budget: zero provider calls, USD 0. max_tries: 3 per failure persisted. Plan-check: implementer self-assessment; independent review pending. Stop application on dirty/mismatched inputs, pending uncertain work, UUID/history divergence or lease contention; never reset a ledger. Continue independent authorized tasks on a blocked action.
