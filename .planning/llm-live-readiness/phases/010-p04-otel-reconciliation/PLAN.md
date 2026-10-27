# Phase 010 plan

## Ownership

Allowed write paths:

- `.planning/llm-live-readiness/phases/010-p04-otel-reconciliation/**`
- `.planning/llm-live-readiness/STATUS.md`
- `.planning/llm-live-readiness/VERIFY.md`

Forbidden changes:

- Any `projects/**` path, account/provider/ledger/registry/campaign state, project artifact, budget or approval, root `.planning/llm-live-testing/**`, other untracked root content, harness-kit, external service, Docker resource, or live provider.

## Tasks

1. Verify project P04 HEAD is `dbd9389` and phase 020 VERIFY/evidence report a committed candidate, service trace result, full-gate exit, and cleanup reconciliation.
2. Update only the aggregate status/checklist, run the read-only lab harness check and `git diff --check`, review staged paths, and commit locally.

## Validation

- Read-only evidence check: `git -C projects/p04 rev-parse HEAD`; inspect `.planning/phases/020-existing-tracer-provider/VERIFY.md` and phase evidence.
- `python scripts/harness/check.py --root .`
- `git diff --check` and staged path review.

## Budget and stop conditions

- Budget USD 0; no model/provider calls or external effects.
- Stop if P04 HEAD/evidence do not match the scoped PASS or project status includes unstaged/uncommitted changes; retain the corresponding aggregate gate as INCOMPLETE.
- Preserve unrelated root untracked content byte-for-byte; no independent or human approval is inferred.
