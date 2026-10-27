# Phase 009 plan

## Ownership

Allowed write paths:

- `.planning/llm-live-readiness/phases/009-project-gate-reconciliation/**`
- `.planning/llm-live-readiness/STATUS.md`
- `.planning/llm-live-readiness/VERIFY.md`

Forbidden changes:

- Any project source, evidence, ledgers, manifests, datasets, rubrics, budgets, approvals, other lab paths, and existing untracked root work.

## Tasks

1. Confirm P03/P04 commits and phase reports match the new local gate claims; preserve all P00/P01 and other pending states.
2. Update the aggregate status/verification text, run the read-only lab harness check, review staged paths, and commit locally.

## Validation

- `python scripts/harness/check.py --root .`
- `git diff --check` and staged-path review.

## Budget and stop conditions

- Budget: USD 0; no provider calls or external effects.
- Stop if a project commit/report does not support a status claim or if root/project work is dirty outside the allowed paths; leave the corresponding gate INCOMPLETE.
