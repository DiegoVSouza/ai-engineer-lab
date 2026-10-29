# Plan

1. Prepare exact four-call policy delta and structured authority record under existing user free-capacity authorization.
2. Implement P03 migration/protected operating cap and current logical operation-history audit; test immutable prefixes, crashes, unknowns, finite caps and failure stops in isolated fake stores.
3. Commit validated inputs, run current-history dry-run, apply only after successful reconciliation and save evidence.

allowed_write_paths: .planning/llm-live-readiness/phases/032-p03-operation-envelope/**; scripts/harness/migrate_p03_operation.py; scripts/harness/test_migrate_p03_operation.py; scripts/harness/live_free_account.py; shared/policies/groq-free-campaign.json; artifacts/evidence/llm-live-readiness/p03-operation-envelope/**; .runtime/llm-live-readiness/ledger-references.json (policy transition only); .runtime/llm-live-readiness/policy-migrations-p03-operation.sqlite*; .runtime/llm-live-readiness/policy-migration.pending; .runtime/llm-live-readiness/ledger-references.policy-migration.tmp; .runtime/llm-live-readiness/account.lock; .runtime/llm-live-readiness/campaign.lock; .planning/llm-live-readiness/WORK.md; .planning/llm-live-readiness/STATUS.md; .planning/llm-live-readiness/CONTINUATION-PLAN.md.
forbidden_changes: historical data/receipts/ledgers, other allocations, rate/model/provider caps, credentials/live calls, Docker, human approvals, holdout/confirmation. Fake mode, zero calls/USD 0 paid. max_tries: 3 per stable failure. Stop on unknown/inflight work, mismatch, lock contention or failed tests. Plan-check: implementer self-assessment.
