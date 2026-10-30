# Plan

1. Verify current root guard history/identity checks, phase039 applied policy and the new phase041 user authority; identify every caller and regression expectation.
2. Add the exact P01 identity and refuse the consumed P01 identity; retain P04's old identity, exact immutable history, one-workflow limit, open-reservation checks and fail-closed behavior. Add offline tests for wrong identity, replay, altered history, reservation and duplicate dispatch.
3. Run bounded fake regressions, record command/cwd/exit/sanitized output and review staged diff before an atomic local commit. P01 owns its controller and full fake gate separately.

allowed_write_paths: `scripts/harness/live_free_account.py`, `scripts/harness/test_p01_p04_revalidation.py`, `.planning/llm-live-readiness/phases/042-p01-distinct-operation-guard/**`, `artifacts/evidence/llm-live-readiness/p01-distinct-guard-042/**`.

forbidden_changes: policy, migration, ledgers or historical reservations, P04 identity or historical evidence, project source, credentials, live/provider calls, paid use, fallback, external effects, holdout, confirmation or human review. Fake only, provider calls0, paidUSD0; preserve persistent regression counters. Stop on unknown history, incompatible policy or unclear authority. Plan-check is implementer self-assessment.
