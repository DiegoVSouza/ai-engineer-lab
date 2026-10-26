# Live readiness implementation status

Overall status: **INCOMPLETE**. This coordination checklist references project-owned evidence; it does not authorize generation or replace project ledgers/reports. Small historical provider smoke tests do not constitute the broad campaign.

## Implemented preparation

- All six projects expose offline campaign inventories, frozen synthetic dataset/split/rubric contracts and local durable ledger/resume-inspection foundations. See the [aggregate dry-run](../../artifacts/evidence/llm-live-readiness/global-dry-run/report.md) for planning maxima and unresolved account requirements.
- P00 now has an offline-tested bounded single-attempt controller: reservation/checkpoint before execution, at most ten new trials, immutable semantic failures, conservative uncertain-attempt handling, pacing/deadline boundaries and process-crash recovery. Implementation commit: `eacec0086ad9ee484393085553cad0cef0822c14`. Evidence: [P00 batch controller report](../../projects/p00/artifacts/evidence/live-campaign-batches/report.md).
- P05's previously reported dependency failure was caused by invoking global Python instead of its locked environment. The corrected complete fake gate passed, including service security, RAG/MCP, correlated traces and worker recovery in a fresh Docker namespace. Existing container identities/states were preserved and temporary resources removed. Evidence commit: `6c75a7977892f886f1db698c5135eb2bee681caa`; whitespace-only follow-up: `7d9c10d`. See [full acceptance](../../projects/p05/artifacts/evidence/locked-acceptance/check-full.txt), [service summary](../../projects/p05/artifacts/evidence/locked-acceptance/phase-021-service-summary.json), [isolation proof](../../projects/p05/artifacts/evidence/locked-acceptance/isolation.txt) and [verification](../../projects/p05/.planning/phases/021-locked-local-acceptance/VERIFY.md).

## Remaining implementation

1. **Whole-account enforcement:** configure one machine-local lease identity used by every campaign launcher and reconcile authoritative usage/reservations across all six project ledgers. Local ledger tests and a callback accepting a synthetic reservation do not implement this guard. Account limits must survive project switches, new campaign IDs and resume; include retries, judges, confirmation and canary traffic.
2. **Real batch dispatch integration:** bind reviewed project adapters/graders to the bounded controller and normal CLI/API/worker paths where applicable. All current broad-campaign CLIs still deny generation; `--resume --dry-run` only inspects saved state. The P00 controller is not connected to Groq, and equivalent project-specific execution still needs implementation in P01–P05. Require frozen dataset/candidate/model/prompt provenance and finite provider timeouts before dispatch. The synchronous controller's wall clock prevents subsequent calls; its injected adapter must bound an in-flight request.
3. **Campaign reporting and operational acceptance:** complete and validate trial-to-report aggregation, per-domain/language/error slices, case-level all-three-pass intervals, operational denominators and cumulative reservation/known-usage reconciliation. Complete remaining applicable service/export fault gates against the evaluated candidate. Fake regression acceptance establishes control behavior only.

## Required evidence and approvals

1. Verified account/model free-tier capacity, finite approved cumulative request/input/output/estimated-spend/time/pacing limits and funded confirmation capacity. These fields remain `PENDING`; paid authorization stays zero. Four keys share account limits.
2. Independent dataset/rubric review, sealed holdout provenance, reviewer capacity and recorded human review. Holdout-guided fixes consume that holdout and require newly reviewed fresh confirmation cases before claiming generalization.
3. Authenticated current model catalog verification before generation; then authorized pilot, development and holdout batches with preserved failures, at most the specified correction rounds, and no semantic resampling.
4. Independent clean-context verification, all applicable quality/security/operation/consumption gates, then local synthetic canary cohorts and exercised rollback on the exact evaluated candidate. No project is broadly promoted by this checklist.

## Next implementation boundary

Implement the shared account guard and launcher contract before connecting a provider callback. Keep every generation command denied while approvals/limits are unresolved. Continue one owning-project SDD phase at a time; do not import sibling source or introduce a second authoritative usage ledger. Use `uv run --locked` for project gates, retain operational failures, and record commands/exits in the owning project's artifacts.
