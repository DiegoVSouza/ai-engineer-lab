# Phase 013 plan

## Ownership

`allowed_write_paths`:

- `.planning/llm-live-readiness/phases/013-p02-retrieval-reconciliation/**`
- `.planning/llm-live-readiness/STATUS.md`

`forbidden_changes`: `projects/**`, campaign/account policies and ledgers, harness kit, unrelated root files, secrets, provider calls, Docker, external systems, approvals, push or publication.

## Tasks

1. Verify P02 phase 011 verification, commit, gate evidence and scope; draft a coordinator entry that separates local contracts from live/integrated gates.
2. Run `python scripts/harness/check.py --root .`, inspect the root-only staged diff, and commit locally.

## Validation

- Read `projects/p02/.planning/phases/011-retrieval-misses-and-interrupts/VERIFY.md` and its committed evidence.
- Confirm P02 HEAD is `68218650a4932e11441517cdb3d658f51fb391b9` and clean.
- Run `python scripts/harness/check.py --root .`.
- Confirm staged paths are limited to this phase and `.planning/llm-live-readiness/STATUS.md`.

## Budget and stop conditions

- USD 0; no provider, credentials, Docker or external effects.
- Stop if P02 verification differs from its committed evidence or project/user-owned files enter the root staging area.
- Implementer reconciliation only; no independent or human approval is inferred.
