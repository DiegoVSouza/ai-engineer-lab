# Roadmap Remediation — Portfolio Specification

**Status:** Draft for implementation planning

**Baseline:** `roadmap-ai-engineer.md`, P00–P05 specs, and the read-only portfolio audit dated 2026-10-15
**Scope:** Close evidenced gaps in roadmap blocks 1–5 across the six independent project repositories. This portfolio document does not replace each repository's SDD phase artifacts.

## Objective

Bring the P00–P05 portfolio into demonstrable alignment with its original acceptance criteria and roadmap blocks 1–5. Preserve independent Git histories and package boundaries. Report verified local behavior separately from service-backed E2E, replay, and live-model evaluation.

“100% market best practices” is not an acceptance target: it is not objectively measurable. Acceptance is based on the concrete criteria below, the original project specs, and reproducible evidence. Do not claim production readiness from unit tests, doubles, fixtures, Compose parsing, or package installation alone.

## Baseline findings to address

- P01 compares five framework adapters using only three synthetic cases; framework-native behavior is uneven, and LangGraph checkpoint identity is the business ticket ID.
- P02's tool timeout does not terminate an already-running thread, execution limits are caller-driven, and its full feature checklist is empty. Cost and model-quality measurements are pending.
- P03 has an empty feature checklist; alert-rule validation was incomplete while its full check returned success. Its traces, dashboards, and simulations have not been demonstrated against the integrated service stack.
- P04 recovery evidence uses SQLite and an in-memory broker. The service tests were skipped. Lease renewal during a long-running step, PostgreSQL/SQS behavior, Docker runtime, and Terraform validation remain unproven.
- P05's package-consumer gate passes, but the product path does not yet prove durable P04 queue processing, authenticated network MCP, PostgreSQL/Redis, pgvector/hybrid retrieval, or an end-to-end trace. Its public routes must be reconciled with the frozen P05 API spec. Replay/live evaluation remains pending.
- Several project state artifacts are stale or empty, including feature lists and agent-card/progress records.
- Roadmap blocks 6 (interview/system-design learning) and 7 (LinkedIn/networking) are not software-project acceptance criteria and have no completion evidence in this portfolio.

## Acceptance criteria by project

### P00 — Shared foundation

- Preserve the versioned domain, fake/replay/live interfaces, cassette provenance, and deterministic testkit.
- Keep live budget limits fail-closed and document the limit of a generic adapter when provider pricing or quotas are unknown.
- Keep service, provider, cost, latency, and model-quality claims `INCOMPLETE` or `PENDING` until the corresponding run is authorized and recorded.
- Preserve wheel/source hashes and consumer provenance for each released contract version.

### P01 — Multi-agent orchestration (roadmap block 1)

- Separate business ticket identity from execution/checkpoint identity; repeated runs of one ticket must not inherit stale state unless an explicit resume key is supplied.
- Exercise all framework adapters against the same versioned golden cases (target: all 60 P00 cases where their contract permits) and report per-case behavior and unsupported semantics.
- The comparison must distinguish framework-native orchestration from a generic worker wrapper. Document fan-out, retries, checkpoints, HITL, state, and observability for each adapter.
- Keep accuracy, tokens, cost, and latency `PENDING` for fake-only runs; do not represent a three-case smoke as a representative benchmark.
- Correct stale documentation about P00 package availability and identify exactly which consumer paths use installed wheels versus local doubles.

### P02 — Production toolkit (roadmap block 2)

- Make timeout/retry behavior safe for side-effecting tools: either use cancellable process/service isolation or prohibit automatic retries after an indeterminate timeout unless idempotency is provided and tested.
- Enforce step, token, and wall-clock limits in the execution path rather than relying on callers to remember to consume counters.
- Define the supported input/output schema subset precisely and test boundary values, including booleans versus numbers and non-finite numbers; use a standard validator if the contract requires full JSON Schema/Pydantic behavior.
- Keep fake regression and adversarial tests in the local gate. Add replay/model-backed checks only when sanitized cassettes or explicit authorization exist.
- Keep before/after cost and latency `PENDING` until comparable recorded runs exist; populate `feature_list.json` and current progress state with evidence-backed statuses.

### P03 — Observability and reliability (roadmap block 3)

- Correct telemetry initialization so later setup calls cannot mutate active-provider configuration; expose a tested flush/shutdown path.
- Provide a deterministic, integrated trace through API, queue, worker, agent, fake/replay LLM boundary, tool, and database, with correlation IDs and privacy-safe attributes.
- Add and validate metrics for task success by task type, retries, errors, and cost per request/task. Ensure alert names match what their expressions measure.
- Validate Prometheus rules with `promtool` and test representative alert series. If the validator or required stack is unavailable, the full product gate must report `INCOMPLETE` with a nonzero exit code.
- Load the provisioned dashboard and exercise the incident scenarios against a local stack before claiming dashboard/alert E2E. Synthetic data must remain labeled synthetic; production metrics remain `PENDING`.
- Populate the feature checklist and record incomplete stack checks accurately.

### P04 — Durable asynchronous processing (roadmap block 4)

- Renew database leases and broker visibility while a step is executing, not only between steps; test a step longer than the lease/visibility interval.
- Prove crash recovery, bounded retry, DLQ behavior, and effect idempotency against PostgreSQL and LocalStack SQS/SNS as well as the existing SQLite/fake path.
- Run Compose services, image build, Terraform validation/plan, and the integration suite when local tools are available. Record missing daemon/CLI/services as `INCOMPLETE` rather than passing the full gate.
- CI must run the required local checks and integration/configuration gates. Do not deploy, push images, apply Terraform, or publish to AWS without separate authorization.
- State the guarantee precisely: deduplication of the local effect ledger is not universal exactly-once delivery for arbitrary external side effects.

### P05 — International SupportOps platform (roadmap block 5)

- Reconcile the versioned OpenAPI contract with the original spec (`/healthz`, ticket approval, and feedback routes). Preserve compatibility or record an ADR and version change for every deliberate contract deviation.
- Exercise an end-to-end fake-mode path using installed P00–P04 wheels: authenticated ticket request → durable P04 queue/worker → P01 triage → tenant-scoped RAG and authorized MCP tools → approval where required → persisted status and response citations.
- Use PostgreSQL for durable product state and Redis for the specified rate-limit behavior in the service-backed path. In-memory storage/queues remain useful for unit tests but do not satisfy the integration gate.
- Implement the specified embedding/pgvector and hybrid retrieval path; retain lexical fixtures for deterministic unit tests. Verify tenant filtering, citations, and prompt-injection behavior through the API/agent path.
- Carry trusted authenticated identity from the MCP transport into authorization; a principal injected only into an in-memory test server does not satisfy authenticated network transport.
- Export one correlated trace across API, queue, worker, agent, LLM boundary, MCP/tool, and database. Provision and exercise dashboards/alerts locally.
- Put P02 regression/adversarial checks in the project CI gate. A deliberate degraded fixture must fail the gate.
- Run the specified replay benchmark for at least two model/configuration variants only when valid cassettes are available. Keep live evaluation, quality, cost, and latency `PENDING` until explicitly authorized real runs are recorded.
- Complete and maintain `agent-card.md`, feature statuses, progress, architecture, threat model, runbook, and bilingual knowledge material. Do not mark pending service/model gates as passed.

## Portfolio-level completion criteria

- Each project has a dedicated local SDD phase with `SPEC.md`, `PLAN.md`, and `VERIFY.md` before its product-code changes. Every plan has 2–4 observable tasks, explicit `allowed_write_paths`, forbidden changes, dependencies, checks, and a stop condition.
- Cross-project work uses only versioned local packages, installed from artifacts with version, source commit, SHA-256, and consumer contract tests. No relative sibling-source imports.
- Each required check records command, exit code, and output under that project's `artifacts/evidence/`; unit, package integration, service integration, E2E, and agent evaluation are labeled separately.
- Full gates return nonzero/`INCOMPLETE` when required acceptance gates have not run or failed. Optional diagnostics may pass independently but cannot turn product acceptance green.
- Contract changes have an ADR, package/API version change where applicable, and consumer update. No silent public-contract changes or weakened tests.
- All six project repos remain independent, use `main`, have clean committed state at handoff, and no external publication/deployment occurs without separate authorization.
- A portfolio matrix maps roadmap blocks 1–5 to project evidence and explicitly lists blocks 6–7 as separate learning/visibility work, not completed by software commits.

## Execution order and ownership

1. **Upstream corrections:** P01, P02, P03, and P04 may proceed independently, with no more than three simultaneous executors. Each executor writes only within its project repository. Public package changes require a new versioned artifact and consumer update.
2. **P05 integration:** after upstream artifact reviews, install and pin the exact approved wheels, then run the service-backed end-to-end gates. Do not substitute doubles for required integrations.
3. **Portfolio reconciliation:** update the roadmap matrix and stale state documents from saved evidence; keep non-executed and externally authorized work pending.

Shared harness/kit changes are excluded. Any later need for a kit change requires a separate phase and validation against two real projects.

## Out of scope and authorization boundaries

- No paid/live LLM calls, provider credentials, external messages, AWS deploy/apply, package publication, Git push, public repository publication, PR, or merge are authorized by this specification.
- Blocks 6 and 7 require separate human learning/visibility work. Do not claim interview readiness, LinkedIn activity, networking, or public portfolio visibility from repository changes alone.
- Do not weaken tests or reinterpret fake/replay results as real model quality.
