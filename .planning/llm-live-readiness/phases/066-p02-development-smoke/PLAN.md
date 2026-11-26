# Plan

## Allowed write paths

- `scripts/harness/live_free_account.py`
- `.planning/llm-live-readiness/phases/066-p02-development-smoke/**`
- `projects/p02/scripts/campaign_execution.py`
- `projects/p02/scripts/run_live_campaign.py`
- `projects/p02/evals/live-execution.json`
- `projects/p02/.planning/phases/066-development-smoke/**`
- New campaign outputs under `projects/p02/artifacts/evals/live/p02-dev-v4-smoke/`
- Root execution evidence under `artifacts/evidence/`

## Steps

1. Add exact authorization to the root account guard and a regression proving only four incremental P02 development reservations fit the 76-attempt ceiling.
2. Add the sealed P02 campaign ID and candidate freeze; preserve the existing runner and transport boundary.
3. Run relevant unit and fixture checks, save command/exit/output evidence, review the diff, then commit root and P02 changes separately.
4. Freeze the committed P02 candidate and run at most four trials through the root transport. Stop on any non-OK or uncertain result.

## Non-goals

No holdout, confirmation, paid provider, old-campaign resume, or unrelated project changes.
