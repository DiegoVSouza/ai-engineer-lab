# Plan

## Allowed write paths

- `scripts/harness/live_free_account.py`
- `.planning/llm-live-readiness/phases/067-p01-framework-smoke/**`
- `projects/p01/src/supportops_agents/registry.py`
- `projects/p01/src/supportops_agents/accounted_frameworks.py`
- `projects/p01/src/supportops_agents/accounted_live.py`
- `projects/p01/scripts/framework_smoke.py`
- `projects/p01/evals/live-execution.json`
- `projects/p01/tests/**` (focused runner contracts only)
- `projects/p01/.planning/phases/067-framework-smoke/**`
- New campaign outputs under `projects/p01/artifacts/evals/live/p01-framework-smoke-v1/`
- Root evidence under `artifacts/evidence/`

## Steps

1. Add exact committed root authorization and regression tests for the 20-request P01 campaign.
2. Permit explicit live runner construction only from the accounted framework adapter; preserve telemetry shutdown and ordered-worker boundary.
3. Add one sealed campaign executor with a manifest tied to committed project and root source hashes.
4. Run framework fake tests and gates, commit root and P01 changes separately, freeze, then execute at most five workflows through the root transport.

No kit changes, holdout, retries, direct provider clients, or other project changes.
