# Plan

1. Capture a read-only Docker baseline and prepare a fresh Git snapshot with unique namespace, image tag, ports, and pytest/Terraform paths.
2. Run one fake full gate after persisting its marker; clean only resources carrying the new namespace.
3. Record command/output/exit, baseline comparison, and whether the frozen operation may proceed.

allowed_write_paths: `.planning/llm-live-readiness/phases/048-p04-replacement-gate/**`, `artifacts/evidence/llm-live-readiness/p04-replacement-gate-048/**`, `projects/p04/artifacts/evidence/reentrant-reviewed-operation-042/**`, `projects/p04/.planning/phases/042-replacement-gate/**`.

forbidden_changes: candidate/source/manifest, policy, ledgers, credentials, provider/live calls, previous evidence, unowned Docker resources including `gossett_backend`, Terraform apply, fallback, capacity changes, release, push, and human-review claims. Stop on pre-gate drift or uncertain outcome. Plan-check is implementer self-assessment.
