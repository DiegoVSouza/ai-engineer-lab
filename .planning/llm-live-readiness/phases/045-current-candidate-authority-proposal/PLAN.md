# Plan

1. On explicit approval only, prepare fresh isolated snapshots and consume at most one P00 full fake gate and one P04 full fake gate, each with a durable marker and baseline checks.
2. Define P04's distinct identity as `local-reviewed-operation-038-v1` / `fixture-reviewed-operation-038`, trial1/max_workflows1; retain its existing three-call logical envelope (12,288 input, 1,536 output), fixed `openai/gpt-oss-20b`, timeout at most30s, no fallback and paidUSD0. No capacity expansion, release or counter reset.
3. Only if the P04 gate passes and source/manifest/reservation/provider preflight all pass, freeze and invoke that distinct workflow once; reconcile without replay. P00 has no live dispatch in this proposal.

allowed_write_paths after explicit approval: new phase-owned evidence/snapshots and the minimally necessary P00/P04 current-candidate manifest/controller/test paths, declared concretely before each implementation phase. This planning phase writes only `.planning/llm-live-readiness/phases/045-current-candidate-authority-proposal/**`.

forbidden_changes: historical reports, receipts, audit rows, policy caps, ledger prefixes, unknown reservations, `gossett_backend`, other Docker resources, customer data, paid use, fallback, deployment, push/PR/merge, Terraform apply, holdout84, confirmation60, or human-review/promotion claims. Stop on any failed/uncertain gate or reservation/preflight mismatch; never replay a prior identity.
