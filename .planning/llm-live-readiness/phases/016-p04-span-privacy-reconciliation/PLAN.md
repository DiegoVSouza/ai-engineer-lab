# Phase 016 plan

## Ownership

`allowed_write_paths`:

- `.planning/llm-live-readiness/phases/016-p04-span-privacy-reconciliation/**`
- `.planning/llm-live-readiness/STATUS.md`

`forbidden_changes`: projects, harness kit, account/campaign policy and ledgers, unrelated root files, secrets, provider calls, Docker, external systems, approvals, push or publication.

## Tasks

1. Verify P04 phase 021 commits, baseline/fixed tests, full-gate evidence and current status.
2. Update coordinator status, run `python scripts/harness/check.py --root .`, inspect root-only staged changes and commit.

## Validation

- Confirm P04 HEAD `073449ef57ad543c3d68d99edaf42ee5707b1419` and clean worktree.
- Read P04 phase 021 verification and project evidence summary.
- Run root harness check and save command, exit and output.
- Confirm only this phase and root `STATUS.md` are staged.

## Budget and stop conditions

- USD 0; no provider, credentials, Docker or external effects.
- Stop if project evidence differs or project/unrelated root files enter staging.
- Implementer reconciliation only; no independent/human approval is inferred.
