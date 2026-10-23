# Decisions

## 2026-10-15 — Replace the coupled project roadmap with a project factory

The lab will use `harness-kit/` to initialize each portfolio project independently. The P00–P05 SupportOps specifications remain archived learning material. The kit preserves SDD phase artifacts, evidence gates, fake/replay/live LLM modes, and authorization for external effects.

Rationale: portfolio projects need different risk profiles, runtimes, and product shapes; a shared implementation dependency graph creates coupling without product value.

## 2026-10-22 — Operate existing SupportOps products through a root Compose stack

The user authorized local self-hosted identity and one Compose application for all existing projects. The lab root owns orchestration, generated credential/TLS bootstrap, operator commands and integration evidence. Product repositories remain read-only and independently versioned. P00–P02 run as installed libraries; P03 supplies telemetry and P04/P05 keep separate runtime services and database users. This adds an optional local operations path without changing the project factory or kit.

Keycloak runs in production server mode with PostgreSQL persistence and locally generated HTTPS certificates. Only loopback application ports are published. No public DNS/cloud deployment or live model run is authorized by this local setup; model evaluation remains pending. LocalStack queues and Jaeger traces are ephemeral in this configuration, so jobs must drain before broker maintenance.
