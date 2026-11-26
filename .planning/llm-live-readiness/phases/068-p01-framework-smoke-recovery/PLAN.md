# Plan

Allowed paths: `scripts/harness/live_free_account.py`, `scripts/harness/test_live_free_account.py`, this phase, `projects/p01/scripts/framework_smoke.py`, `projects/p01/evals/live-execution.json`, `projects/p01/src/supportops_agents/accounted_live.py`, `projects/p01/.planning/phases/068-framework-smoke-recovery/**`, and new campaign v2 outputs.

1. Add a new exact root authorization with a root regression enforcing 20 calls cumulatively across campaign IDs.
2. Fix manifest keys to use `projects/p01/`; include only the matching v2 authorization in the frozen root source set.
3. Commit root and P01 changes, freeze v2, validate manifest and capacity, then execute the remaining authorized scope.

Campaign v1 remains closed with zero provider calls. No counter reset or campaign resume.
