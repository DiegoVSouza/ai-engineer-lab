# PLAN — Fly.io portfolio deployment

allowed_write_paths: `.planning/projects/lab-stack/**`; `docs/harness/lab-stack/**`; `docs/knowledge/**`; `fly/**`; `ops/fly/**`; `.gitignore`; `README.md`; project deployment files and product queue adapters explicitly owned by their own plans; `artifacts/evidence/fly/**`.

forbidden: credentials in Git; public database/Redis ports; setting a fake monthly-cost claim; live paid model calls; deleting Docker volumes before verified backups; changing unrelated lab stacks.

llm_mode: fake.

1. Add and verify a Redis Streams broker adapter in P04 while retaining its SQS adapter and existing recovery contract.
2. Consume that adapter from P05 durable dispatch and use Redis for both local Compose and Fly queue delivery.
3. Configure separate Fly apps in `iad` for P04/P05 runtime and identity/data/telemetry dependencies, with minimum viable machines, private services, persistent disks and autostop only where request-driven startup is safe.
4. Create a repeatable pre-deploy Git/data backup and documented restore path; deploy and run public acceptance after Fly authentication is available.

Validation: P04 fast/full gates with real Redis, visibility/reclaim/retry/DLQ/crash scenarios; P05 fast/full gates with PostgreSQL/Redis/Keycloak; rendered Fly configs and `fly deploy --build-only` before deploy; after deploy inspect each machine, check health and public endpoints, and verify persistence/backups. Save commands, exit codes and redacted outputs.

Stop conditions: no Fly authentication; failed backup/restore check; unsafe resource cost; any public data-service binding; or missing service acceptance. Keep old stacks and volumes until rollback data is verified.

Plan review: accepted for implementation. Fly CLI login and any usage cost are account-scoped; user asked for minimum machines and autostop, no monthly ceiling was set.
