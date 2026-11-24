# Plan

1. Add red tests for a missing or tampered authorization, the new 24-attempt cap, cumulative 72-attempt development ceiling across IDs, uncertain/failing attempts, and unchanged protection of holdout, confirmation and other projects.
2. Add the committed authorization and the smallest root guard branch that preserves cumulative usage; no policy cap or prior reservation changes. Run the root guard tests and save command, exit code and output.
3. Reconcile actual P02 usage read-only. Keep any live execution blocked until the P02 executor explicitly binds the new authorization and prompt and all gates pass.

allowed_write_paths: `.planning/llm-live-readiness/phases/064-p02-candidate-development/**`, `scripts/harness/live_free_account.py`, `scripts/harness/test_live_free_account.py`, `artifacts/evidence/p02-candidate-guard-064/**`.

forbidden_changes: `harness-kit/**`, project files, existing authorizations, policies and ledgers; no provider access. Three total attempts per reproducible failure; no resetting consumed live or gate limits.
