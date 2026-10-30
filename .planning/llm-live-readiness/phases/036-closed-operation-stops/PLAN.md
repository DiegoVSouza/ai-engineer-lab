# Plan

1. Add read-only logical terminal checks for original P01/P04 operational scopes and P01 diagnostic scope, refusing malformed/missing required history rather than granting replay.
2. Test new original IDs and completed diagnostic, maintain successful in-progress diagnostic calls and all account/transport/exception regressions; save evidence and commit.

allowed_write_paths: .planning/llm-live-readiness/phases/036-closed-operation-stops/**; scripts/harness/live_free_account.py; scripts/harness/test_p01_reviewed_diagnostic.py; scripts/harness/test_p04_reviewed_diagnostic.py; artifacts/evidence/llm-live-readiness/closed-operation-stops/**; .planning/llm-live-readiness/WORK.md.
forbidden_changes: budgets, authority, historical outcomes/ledgers/manifests, provider calls/credentials, Docker, sibling products, holdout/confirmation and human approvals. Fake zero calls/USD0. max_tries3. Stop on read uncertainty or failing regression. Plan-check: implementer self-assessment.
