# Plan

1. Code: guard opens `free-holdout-c1` only for this authorization (account layer); P00 scope gate opens only when the file is valid and the candidate hashes match.
2. Gates: P00 tests, full fake gate, catalog preflight, holdout dry-run.
3. Run `--stage holdout --campaign-id free-holdout-c1` in batches of at most ten trials, 70 s apart for the free per-minute token limit. A critical failure stops the run.
4. Record the result in `failures.md` and VERIFY without editing the candidate.

allowed_write_paths: `.planning/llm-live-readiness/phases/052-p00-holdout-run/**`, `scripts/harness/live_free_account.py`, `scripts/harness/test_live_free_account.py`, `.planning/llm-live-readiness/AUTHORIZATION.md`.
forbidden_changes: prompt, schema, dataset, rubric, policy, confirmation reserve, other projects.
Budget: at most 84 calls, USD 0 paid. max_tries: 3.
