# Specification handoff and implementation sequence

## Current task: documentation only

1. Inspect lab rules, current project profiles, live entrypoints and prior evidence. Define the broad campaign, budget boundaries and local promotion scope.
2. Write SPEC.md, this PLAN.md, VERIFY.md and the Portuguese Luna handoff. Review arithmetic, applicable gates, safety/accounting requirements and project independence.
3. Validate the documentation structure and references, save the executed command/exit/output as evidence, inspect the staged diff and commit only these task paths locally.

allowed_write_paths:
- .planning/llm-live-readiness/**
- artifacts/evidence/llm-live-readiness-spec/**

forbidden_changes: product code, project Git histories, prior live-testing draft, root .env, harness-kit/**, unrelated user files, existing Docker stacks.
llm_mode: no provider execution in this documentation task.
stop_condition: a documentation requirement needs secrets or product implementation; record it rather than performing that work.

## Luna execution: one project phase at a time

This intake is not an executable cross-project code ownership plan. First create project-local phases using the next available IDs, not guessed phase numbers. Recheck each repository's status and rules. Each local plan must contain 2–4 tasks, concrete files, tests, gates, budget source and a stop condition. Commit planning before a multi-task implementation.

For every project, split work into these phases:

1. **Campaign preparation:** inventory contracts/runtime; reconcile budget policy; build reviewed datasets/splits/rubrics, report schema and dry-run reservation manifest. Test graders using deliberate bad outputs. No live calls yet.
2. **Bounded runner and runtime:** implement or adapt local adapter/CLI and actual API/worker live configuration where applicable, global serialization lease, durable trial/ledger writes, resume, safe errors and offline contract/fault tests. Run fast/full/service regressions and package consumer checks. The runtime to be promoted must exist before quality evaluation. Reuse existing paths before adding abstractions.
3. **Evaluation and fixes:** authenticated preflight, pilot, development trials, at most two documented correction rounds, frozen holdout and fresh confirmation when consumed. Stop/checkpoint on quota/budget. Complete independent rubric review and all VERIFY gates before advancing.
4. **Local promotion:** promote the already evaluated normal live entrypoint, verify the exact candidate revision/configuration, run synthetic canary cohorts and rollback; update documentation/knowledge and commit reviewed evidence. Runtime/prompt/model changes invalidate affected evaluation gates and require reevaluation; do not add a new integration after holdout and carry its earlier approval forward.

Each phase itself needs 2–4 implementation tasks; split again if it becomes larger. Completing preparation in all projects before reserving the whole campaign is recommended. Order product implementation by actual dependency needs: foundation and observability contracts first when needed, then consumers. There is no mandatory shared release wave and no sibling-source import shortcut.

Luna may write a coordination checklist under this intake, but all execution state, metrics and product changes belong to the owning project's repository. A cross-project summary references those reports rather than copying metrics into competing sources of truth. Do not add a root runner that imports project source.

## Proposed per-project files to inspect before naming write paths

- p00: scripts/smoke_groq.py, supportops_foundation/, tests/, demo/, docs/harness/.
- p01: scripts/run_live_groq_eval.py, src/supportops_agents/, installed runner adapters, tests/, evals/.
- p02: scripts/run_live_groq_eval.py, supportops_toolkit/, evals/datasets/v1/, tests/.
- p03: scripts/run_live_groq_eval.py, scripts/check_services.py, supportops_obs/, stack/, tests/.
- p04: supportops_async/live_groq.py, API/worker configuration, scripts/run_live_service_eval.py, agent/prompts/live-workflow.md, Docker profiles, tests/.
- p05: supportops_platform/agents/, service_runtime.py, api/, scripts/check_live_services.py, docker-compose.live.yml, agent/prompts/, evals/, tests/.

These are discovery anchors, not blanket write permission. Resolve actual package directories and project-specific instructions before the local plan. Changes to profiles, dependencies, prompts, APIs and report schemas require explicit coverage in that plan and corresponding regressions.
