# Phase 015 plan

## Ownership

`allowed_write_paths`:

- `.planning/llm-live-readiness/phases/015-p03-privacy-and-service-reconciliation/**`
- `.planning/llm-live-readiness/STATUS.md`

`forbidden_changes`: project repositories, account/campaign policy and ledgers, harness kit, unrelated root files, secrets, provider calls, Docker, external systems, approvals, push or publication.

## Tasks

1. Verify P03 phases 017–020 candidate/reconciliation commits, their verification states, failure reports and exact gate evidence.
2. Update coordinator status with scoped PASS/INCOMPLETE boundaries, run `python scripts/harness/check.py --root .`, review root-only staged paths and commit.

## Validation

- Confirm P03 HEAD `5a10634b189e4385b04aefbe9bc44b8e6bd90596` is clean.
- Read P03 phase 017, 018, 019 and 020 verification and evidence summaries.
- Run `python scripts/harness/check.py --root .` and save command/exit/output.
- Confirm only this phase and `.planning/llm-live-readiness/STATUS.md` are staged.

## Budget and stop conditions

- USD 0; no provider, credentials, Docker or external effects.
- Stop if project status/evidence differs or any project/unrelated file appears in root staging.
- Implementer reconciliation only; human/independent review remains PENDING.
