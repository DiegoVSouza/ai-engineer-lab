# Phase 002 — Free-account guard

Implement a standard-library account guard used through a subprocess contract by independent project launchers. One machine-local exclusive lease serializes all calls. Authoritative provider-attempt reservations and outcomes live in each project's separate usage database; aggregate checks read those databases rather than maintaining duplicate root usage.

The user authorized the remaining implementation and free-tier campaign on 2026-10-26, with no paid usage, and will review results after technical preparation. Human review remains pending and promotion cannot pass until it is recorded. Public deployment, customer data, external messages and real refunds remain excluded.

Use the published free-plan ceilings for `openai/gpt-oss-20b` as upper bounds, clamped by smaller authenticated response limits. Enforce request/token rolling minute/day windows, finite cumulative campaign/project caps, retained unknown reservations, immutable attempts, process-crash recovery and stop-on-quota/cooldown. Four numbered keys never multiply quota. Provider headers cannot establish billing tier or remaining daily tokens; report that uncertainty and preserve provider-enforced exhaustion behavior. No paid upgrade/fallback.

Acceptance: meaningful offline cross-project/concurrency/crash/rate/accounting tests; sanitized no-generation CLI inventory and authenticated model-catalog preflight; credentials selected only from numbered root `.env` entries without logging/hashing them. Actual project writes/generation require a separately planned owning-project integration phase. Provider dispatch is not enabled by this foundation phase.
