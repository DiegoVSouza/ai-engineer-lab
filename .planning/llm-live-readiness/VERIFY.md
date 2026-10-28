# Verification contract

Current execution reconciliation, 2026-10-28: root phases 026/027 validate transport and the explicitly authorized/applied +13 migration; 58 control and 28 migration tests passed. P00 phase 028 full fake gate passes 148 tests, P01 final dependent gate passes 71 tests and six runners, P04 phase 027 full local privacy/service gate passes 87 tests with Terraform plan-only. Existing scoped P02/P03/P05 acceptances were inspected; see current STATUS/WORK and owning phase evidence. Human/independent/dataset/rubric/holdout/generalization/promotion remain pending. Historical claims below are preserved and superseded where they conflict with those current records.

## Documentation delivery

- [x] Lab rules, workflow and commit skill read; current profiles and live entrypoints inspected.
- [x] SPEC, PLAN, VERIFY and Portuguese handoff exist; this task edits no product code.
- [x] Case totals, split totals, trial count and maximum normal call count agree.
- [x] Budgets are not silently expanded; the specified runner blocks generation on unknown approval/quota while permitting dry-run.
- [x] The specification preserves deterministic fake/replay and distinguishes real provider runs from offline tests and fixture metrics. Runtime implementation remains pending.
- [x] Per-project ownership, held-out protocol, failure correction, local canary and rollback are specified.
- [x] Documentation validation command, exit code 0 and output saved in artifacts/evidence/llm-live-readiness-spec/validation.json.

Staged review and local commit reference: supplied in the delivery handoff after Git confirms success.

Root specification and documentation validation: PASS. Project implementations and gates are recorded in the current project reconciliation below. Live campaigns, human/independent approvals, and promotion remain PENDING/INCOMPLETE.

## Current project reconciliation — 2026-10-27

- P04 OTLP service export: PASS on candidate `beff749202805b138d820daaddb80a4468afc7c9`; one synthetic local request produced API and worker spans in the same phase-owned Jaeger trace. Full local gate PASS (84 tests, service scenarios, Docker build, Terraform plan-only). See [phase verification](../../projects/p04/.planning/phases/020-existing-tracer-provider/VERIFY.md) and [evidence](../../projects/p04/artifacts/evidence/otel-provider-020/).
- Phase 019's provider-collision failure, task and trace remain immutable historical evidence; phase 020 used a new task/trace and did not replay it.
- P04 RAG/retrieval, live model quality, billing, human/independent review, and promotion remain INCOMPLETE/PENDING. No project is declared live approved.
- P00 generation remains blocked pending authoritative Free billing/quota proof; its funded call allocation and protected confirmation remain unchanged.

## Future project verifier

Start from project rules, SPEC, candidate revisions and artifacts without relying on implementation-chat claims. Use a separate reviewer session for clean-context verification; no agent spawning is required by this handoff. Missing evidence is INCOMPLETE.

### Offline checks before provider access

1. Validate dataset schema/uniqueness, semantic split isolation, family/language coverage and review provenance. Prove graders reject wrong decision/tool/schema, unsupported facts and invalid citations.
2. Run fake/replay without network and without live credentials. Test unknown/missing mode, unavailable model, missing keys, missing budget, shared-lease contention, timeout, quota, long Retry-After, all-key exhaustion, permanent errors and no semantic retry/fallback.
3. Test exact/upper-bound accounting for all messages/tools/reasoning/output, unknown failed usage, retries, judges, chunk boundaries and process restarts. Prove cumulative caps cannot reset on resume. Crash around dispatch/outcome/ledger writes; no silent replay of uncertain attempts.
4. Test service authorization/tenant isolation, cancellation, duplicate effects, queues/DLQ, worker crash/lease recovery and controlled unavailable behavior. Check no secret-bearing logs, layers, files or expanded Compose output.
5. Run the actual project fast/full/service/package checks and document all skips. Repeated checks are required only after changes or unresolved concerns justify them.

### Real campaign evidence

1. Verify catalog/model availability and environment version evidence. Preflight and reservation must precede generation. Cross-check trial provenance with provider usage and persisted service state/trace where applicable.
2. Verify exact planned unique cases/trials completed, all failures included, no duplicate success substitution and no fake result counted as real. Recompute per-slice scores, unique-case all-three-pass Wilson intervals, operational denominators and totals from trials.jsonl.
3. Check immutable baseline/candidate attempts, correction taxonomy/regressions, consumed holdout tracking and fresh confirmation where needed. Confirm manual review actually occurred; otherwise keep that gate pending.
4. Reconcile ledger reservations and known provider usage. Unknown usage and billing must remain unknown/PENDING. Confirm all observed and conservative reserved spend stays within authorized limits, including canary and judges.
5. Query actual Jaeger/Prometheus/service state without dumping response content or environment. Test export outage/recovery separately; never describe an offline simulated outage as a real provider failure.

### Promotion decision

All applicable SPEC thresholds must pass per project, including frozen latency/queue targets. Verify local cohorts of 5/25/50 tasks and exercised rollback. Confirm normal CLI/API/worker paths use live only with explicit opt-in and that refund/external-action restrictions remain enforced. Report exact supported runners and NOT_APPLICABLE service paths with rationale.

Result must state PASS, FAIL or INCOMPLETE per gate, source/dataset/prompt revisions, limitations, unresolved errors, rollout state, rollback reference and local commit hashes. No provider results are supplied by this documentation task.
