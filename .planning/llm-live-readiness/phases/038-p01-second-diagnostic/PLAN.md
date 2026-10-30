# Plan

1. Implement exact second-operation authority/history exception and finite preserving policy migration, including retained P04 unknown step and completed diagnostic/P05 operation receipts.
2. Test scope/history/closed/uncertain/no-replay and migration atomicity/interruption/unknown reserves/UUID/prefix protections; account and transport regressions.
3. Commit proposed policy/inputs, dry-run/apply validated metadata migration once, save command/cwd/exit/output and continue owning P01 workflow.

allowed_write_paths: .planning/llm-live-readiness/phases/038-p01-second-diagnostic/**; scripts/harness/live_free_account.py; scripts/harness/test_p01_second_diagnostic.py; scripts/harness/migrate_p01_second_diagnostic.py; scripts/harness/test_migrate_p01_second_diagnostic.py; shared/policies/groq-free-campaign.json; .planning/llm-live-readiness/AUTHORIZATION.md; .planning/llm-live-readiness/WORK.md; artifacts/evidence/llm-live-readiness/p01-second-diagnostic/**; .runtime/llm-live-readiness/policy-migrations-p01-second-diagnostic.sqlite; .runtime/llm-live-readiness/ledger-references.json and policy-migration.pending (migration only).
forbidden_changes: provider calls/credentials, original outcomes/IDs/manifests/rows/reservations, other project caps/holdout/confirmation, Docker, paid use/fallback, human approvals. Zero calls/USD0; max_tries3 per failure. Stop on mismatch/inflight/history/failed regression. Plan-check implementer self-assessment.
