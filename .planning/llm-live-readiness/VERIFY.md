# Verification contract

## Documentation delivery

- [x] Lab rules, workflow and commit skill read; current profiles and live entrypoints inspected.
- [x] SPEC, PLAN, VERIFY and Portuguese handoff exist; this task edits no product code.
- [x] Case totals, split totals, trial count and maximum normal call count agree.
- [x] Budgets are not silently expanded; the specified runner blocks generation on unknown approval/quota while permitting dry-run.
- [x] The specification preserves deterministic fake/replay and distinguishes real provider runs from offline tests and fixture metrics. Runtime implementation remains pending.
- [x] Per-project ownership, held-out protocol, failure correction, local canary and rollback are specified.
- [x] Documentation validation command, exit code 0 and output saved in artifacts/evidence/llm-live-readiness-spec/validation.json.

Staged review and local commit reference: supplied in the delivery handoff after Git confirms success.

Delivery status: documentation validation PASS. Campaign and promotion status: PENDING implementation.

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
