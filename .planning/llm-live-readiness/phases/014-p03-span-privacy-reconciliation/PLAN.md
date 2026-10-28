# Phase 014 plan

## Ownership

`allowed_write_paths`:

- `.planning/llm-live-readiness/phases/014-p03-span-privacy-reconciliation/**`
- `.planning/llm-live-readiness/STATUS.md`

`forbidden_changes`: project repositories, account/campaign policy and ledgers, harness kit, unrelated user paths, secrets, provider calls, Docker, external systems, approvals, push or publication.

## Tasks

1. Verify the P03 phase-017 commits, verification, test/gate outputs and before/after infrastructure reconciliation; draft scoped coordinator status.
2. Run `python scripts/harness/check.py --root .`, review the root-only staged diff and commit locally.

## Validation

- Read P03 `.planning/phases/017-span-status-privacy/VERIFY.md`, candidate/evidence commits, and `artifacts/evidence/span-status-privacy-017/`.
- Confirm P03 HEAD `b2a00143ba6d98a4e383876e699c8290db73ffb4` is clean.
- Run `python scripts/harness/check.py --root .`.
- Confirm staged paths are limited to this phase and coordinator `STATUS.md`.

## Budget and stop conditions

- USD 0; no provider, credentials, Docker or external effects.
- Stop if P03 evidence differs from committed claims or any project/unrelated root path enters staging.
- Implementer reconciliation only; human/independent review remains PENDING.
