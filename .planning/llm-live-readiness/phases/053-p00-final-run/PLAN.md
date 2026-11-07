# Plan

1. Fake gate and catalog preflight with the frozen candidate; development replay shows c6 + director at 182/192 (in-sample).
2. Run `--stage holdout --campaign-id free-final-c1` in batches of at most ten trials, 70 s apart for the free per-minute token limit. A critical failure stops the run.
3. Record the result in `projects/p00/docs/harness/failures.md` and VERIFY, then update the README and portfolio status from it.

allowed_write_paths: `.planning/llm-live-readiness/phases/053-p00-final-run/**`.
forbidden_changes: prompt, schema, dataset, rubric, director, policy, other projects.
Budget: at most 60 calls, USD 0 paid. max_tries: 3.
