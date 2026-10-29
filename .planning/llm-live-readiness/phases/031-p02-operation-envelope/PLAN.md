# Plan

1. Prepare an exact four-call P02 policy proposal and authorization derived from the existing user free-capacity authorization.
2. Implement migration and scoped shared-account protection; verify immutable history, unknown reserves, locks, crash recovery and repeated apply with fake stores.
3. Commit validated inputs, inspect dry-run and apply only if all histories reconcile; save evidence and checkpoint.

allowed_write_paths: .planning/llm-live-readiness/phases/031-p02-operation-envelope/**; scripts/harness/migrate_p02_operation.py; scripts/harness/test_migrate_p02_operation.py; scripts/harness/live_free_account.py; scripts/harness/test_live_free_account.py; shared/policies/groq-free-campaign.json; artifacts/evidence/llm-live-readiness/p02-operation-envelope/**; .runtime/llm-live-readiness/ledger-references.json (policy transition only); .runtime/llm-live-readiness/policy-migrations-p02-operation.sqlite*; .runtime/llm-live-readiness/policy-migration.pending; .runtime/llm-live-readiness/ledger-references.policy-migration.tmp; .runtime/llm-live-readiness/account.lock; .runtime/llm-live-readiness/campaign.lock.

forbidden_changes: historical ledgers, manifests, receipts, other allocations, holdout/confirmation, model/rates, credentials, live calls, Docker, human approvals. Fake/default mode; zero calls/USD 0 paid. max_tries: 3 per failure, persisted; no replay. Stop on history mismatch, unknown active work or failed validation. Plan-check: implementer self-assessment.

Coordination amendment: allowed writes also include `.planning/llm-live-readiness/CONTINUATION-PLAN.md`, `STATUS.md` and `WORK.md` to record actual P02 migration/consumer acceptance and the next independent task. These references do not authorize other product writes.
