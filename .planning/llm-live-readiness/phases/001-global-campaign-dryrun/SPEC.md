# Phase 001 — Account-wide campaign dry-run

## Goal

Provide one offline, sanitized inventory of the six project campaign pilots and their full/confirmation ceilings. Expose unresolved shared quota and cumulative-budget limits before any project campaign can be dispatched.

## Starting evidence

- Projects P00–P05 now each have a project-owned preparation CLI and durable local reservation/lease primitives.
- Those ledgers are intentionally independent. Groq quota is account-wide; independent project counters do not by themselves enforce one shared allowance.
- Existing project configs still contain `PENDING` account quota, cumulative ceilings, or human approvals. The 390-case campaign size is not authority to increase any budget.
- Local product repositories have separate Git histories. This root tool may orchestrate only their documented `--dry-run` CLI interfaces; no sibling source imports.

## Acceptance criteria

1. The root CLI invokes each project's documented offline pilot dry-run without importing project code, reading `.env`, constructing provider SDK clients, touching Docker/services, or modifying project files.
2. It validates each JSON result and reports per-project pilot calls, primary calls, confirmation calls, additive total where available, pending approvals/caps, and an account-wide sum. No unknown field is silently treated as zero.
3. Any missing/failed project dry-run or any unresolved shared quota/limit makes the aggregate result `INCOMPLETE`; it never authorizes generation.
4. The report records sanitized commands, exit codes, and `provider_accessed=false`, `credentials_read=false`, and `docker_mutated=false` for every project.
5. Evidence is written only to the root phase evidence directory; project historical reports and unrelated Git work remain unchanged.

## Out of scope

Global live ledger/lease enforcement, project dispatch, credentials, model catalog preflight, provider calls, Docker/service operations, changing project budgets/configuration, or changing human approvals.

## Status

`PLANNED`; the result is a safety inventory, not campaign authorization.
