# Phase 012 plan

## Ownership

`allowed_write_paths`:

- `.planning/llm-live-readiness/phases/012-p01-tool-boundary-reconciliation/**`
- `.planning/llm-live-readiness/STATUS.md`

`forbidden_changes`: `projects/**`, root provider/account policy and ledgers, harness kit, unrelated root docs or files, external systems, secrets, approvals, provider calls, Docker, push or publication.

## Tasks

1. Verify the P01 phase-011 plan/verification, proposed-tool paths, development dry-run summary, preservation hashes and project candidate history. Draft the coordinator update with PASS/INCOMPLETE boundaries.
2. Run `python scripts/harness/check.py --root .`, inspect the staged root-only diff, and commit locally. Preserve all unrelated user changes.

## Validation

- Read-only source facts from `projects/p01/.planning/phases/011-real-tool-source-contract/VERIFY.md`, `projects/p01/artifacts/evidence/real-tool-source-contract-011/dry-run-summary.txt`, and proposed contracts under `projects/p01/shared/tools/`.
- `python scripts/harness/check.py --root .`.
- Confirm staged paths are limited to this phase and `.planning/llm-live-readiness/STATUS.md`.

## Budget and stop conditions

- USD 0; no provider, Docker, secrets, or project service access.
- Stop if project verification differs from its committed evidence or any project/user-owned root path enters staging.
- Implementer reconciliation only; no independent or human approval is inferred.
