# Decisions

## 2026-10-15 — Replace the coupled project roadmap with a project factory

The lab will use `harness-kit/` to initialize each portfolio project independently. The P00–P05 SupportOps specifications remain archived learning material. The kit preserves SDD phase artifacts, evidence gates, fake/replay/live LLM modes, and authorization for external effects.

Rationale: portfolio projects need different risk profiles, runtimes, and product shapes; a shared implementation dependency graph creates coupling without product value.
