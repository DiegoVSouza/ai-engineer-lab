# Plan

1. Add a red test proving an unallocated v3 identity is blocked, its own committed authorization admits it, a non-OK attempt halts it, and prior v1/v2/v3 reservations remain inside the 72-attempt cap.
2. Add the root guard branch and committed authorization from the owner's prior free-model iteration instruction. Run focused and full root guard tests; preserve USD 0 paid allocation and holdout/confirmation protection.
3. In P02, bind v3 to the candidate prompt, tests, runner and root authorization path. Run fixture/fake checks and source review, commit and freeze one manifest. Live work may start only after account reconciliation reports no uncertain attempts and all 48 prior P02 development attempts are accounted.
4. Run a six-case pilot; proceed with the remaining 18 only if all pilot attempts settle `ok`. Record reports and content-free observations. Keep model-quality and external RAG statuses open unless the actual acceptance gate passes.

allowed_write_paths: `.planning/llm-live-readiness/phases/065-p02-candidate-v3/**`, `scripts/harness/live_free_account.py`, `scripts/harness/test_live_free_account.py`, `artifacts/evidence/p02-candidate-v3-065/**`, `projects/p02/.planning/phases/021-candidate-v3-development/**`, `projects/p02/agent/prompts/**`, `projects/p02/scripts/campaign_execution.py`, `projects/p02/scripts/candidate_corpus.py`, `projects/p02/scripts/run_live_campaign.py`, `projects/p02/tests/test_campaign_candidate.py`, `projects/p02/evals/live-execution.json`, `projects/p02/artifacts/evidence/candidate-v3-development-021/**`, `projects/p02/artifacts/evals/live/p02-dev-v3/**`, `projects/p02/docs/harness/{progress,failures,feature_list}.md|json`.

forbidden_changes: prior campaign manifests, reports, trials, ledgers and authorizations; dataset, rubric and holdout; other projects; credentials; real tools; paid provider allowance; production deployment.
