# Plan

1. Isolate the post-apply source-binding decision in the phase039 migrator, retaining the exact historical blob requirement until a valid applied audit exists.
2. Add unit tests for unchanged source, changed source before apply, and changed source after the append-only applied audit; run the migration regression suite offline.
3. Re-run the applied migration read-only and record the result. Preserve all current project changes and stop before any full gate, manifest write, reservation, credential read, provider action, or live dispatch.

allowed_write_paths: `scripts/harness/migrate_p01_p04_revalidation.py`, `scripts/harness/test_p01_p04_revalidation.py`, `.planning/llm-live-readiness/phases/044-post-apply-source-binding/**`, `artifacts/evidence/llm-live-readiness/post-apply-source-binding-044/**`, `.planning/llm-live-readiness/{CONTINUATION-PLAN,STATUS,WORK,EXECUTOR-HANDOFF,AUTHORIZATION}.md`.

forbidden_changes: policy, migration audit rows, ledgers, reservations, project sources, manifests, historical receipts/reports, gate markers, credentials, provider/live calls, paid usage, fallback, Docker, Terraform apply, holdout or human review. Fake/offline only; provider calls0, paidUSD0. Stop if audit is not exact applied state or current source is uncommitted.
