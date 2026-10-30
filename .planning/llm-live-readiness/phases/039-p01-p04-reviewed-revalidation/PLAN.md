# Plan

1. Reconcile actual ledger, authority, source and Git; implement individually scoped exceptions and a preserving finite migration with offline crash, history, cap and no-replay tests.
2. Validate the migration, apply only once after all checks, implement and validate P01 current strict-schema operation in an isolated snapshot; freeze and invoke at most once.
3. Validate P04 service prerequisites and inventory, implement and validate a separate current-fingerprint operation; freeze and invoke at most once in an owned namespace. Reconcile and update P00 binding and the final handoff.

allowed_write_paths: .planning/llm-live-readiness/phases/039-p01-p04-reviewed-revalidation/**; scripts/harness/live_free_account.py; scripts/harness/migrate_p01_p04_revalidation.py; scripts/harness/test_p01_p04_revalidation.py; shared/policies/groq-free-campaign.json; artifacts/evidence/llm-live-readiness/p01-p04-revalidation/**; .runtime/llm-live-readiness/ledger-references.json and owned migration metadata; .planning/llm-live-readiness/{WORK,STATUS,AUTHORIZATION,CONTINUATION-PLAN,EXECUTOR-HANDOFF}.md. Product changes require separate project-local phases with concrete paths before implementation.
forbidden_changes: prior outcomes, manifests, IDs, reserves, unrelated files/resources, holdout/confirmation, paid use, model/provider fallback, customer data, public deploy, messages, push/PR/merge, refunds and Terraform apply. Fake by default. max_tries 3 per local failure; no live replay. Stop on unknown history, invalid authorization, uncertainty, quota or failure. Plan-check is implementer self-assessment.

Test-path amendment: allow scripts/harness/test_p01_p04_migration_regression.py for the inherited migration crash/history test suite; no product scope change.
