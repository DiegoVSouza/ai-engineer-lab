# SPEC — Run SupportOps with one self-hosted Compose stack

Start the lab's P00–P05 runtime from a root Compose file. P00–P02 are installed versioned libraries exercised by a successful package gate; P03 supplies telemetry; P04 and P05 run their own APIs and workers. Add a persistent Keycloak server with HTTPS and a real PostgreSQL database, generated local credentials, tenant-scoped users, API/MCP introspection, and revocation acceptance.

Expose only loopback ports. Preserve existing Compose projects and their volumes. Keep product repositories independent and read-only. Use approved pinned package/image versions. Store generated keys/passwords only in Docker volumes. LLM mode stays fake; SQS/SNS remain local emulation and model evaluation stays pending.

Acceptance: one `docker compose up -d --build --wait` starts required services without manual secret setup; package gate runs P00–P04 installed packages; local HTTPS identity issues tokens for API access; cross-tenant access and revoked tokens are denied; P04 and P05 durable worker jobs finish; dashboards/traces are reachable; credentials and completed database records survive container recreation. Save redacted commands, exit codes and outputs. Leave the stack running.
