# Plan

1. Record the finite superseding authority and retain the consumed `-038-` attempt as an immutable INCOMPLETE predecessor.
2. Bind the exact new P04 identity in the shared guard, with committed-authority, exact historical provider/logical prefix, duplicate, reservation, and no-replay checks retained.
3. Add regressions for rejection of both prior P04 identities and authority tampering; run the locked root guard test and save sanitized evidence.

allowed_write_paths: `scripts/harness/live_free_account.py`, `scripts/harness/test_p01_p04_revalidation.py`, `.planning/llm-live-readiness/phases/047-p04-reentrant-operation/**`, `artifacts/evidence/llm-live-readiness/p04-reentrant-operation-047/**`, `.planning/llm-live-readiness/{AUTHORIZATION,STATUS,WORK,EXECUTOR-HANDOFF,CONTINUATION-PLAN}.md`.

forbidden_changes: policy, migration state, capacity, ledgers, historical operation/manifests, credentials, provider/live calls, Docker, `gossett_backend`, fallback, reservation release, counter reset, holdout84, confirmation60, Terraform apply, deployment, push, PR, and human-review claims.

Validation/budget: fake/offline Python unittest only; provider access 0 and paid USD 0. Stop if the committed authority, historical prefixes, or an existing reservation differs. Plan-check is implementer self-assessment.
