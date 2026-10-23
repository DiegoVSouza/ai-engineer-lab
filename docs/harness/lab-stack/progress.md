# Deployment progress

## 2026-10-22 â€” Unified self-hosted local acceptance

The root Compose application now operates P00â€“P05 together. P00/P01/P02 are installed libraries with successful provenance and execution gates. P03 provides telemetry and dashboards; P04 and P05 run independent APIs and workers. Keycloak runs in production server mode with a separate PostgreSQL database and verified HTTPS introspection, and the deployed P05 API uses that issuer. All published ports are loopback-only.

Generated credentials and TLS material live in service-scoped Docker volumes. The initial strict-TLS extension failure and premature socket readiness check were corrected. Acceptance passed tenant denial, separate human approval, worker processing, token revocation at both API and MCP, metrics, dashboards and a correlated trace. Container recreation preserved credentials/CA, Keycloak identity and completed product records.

The six product source repositories were preserved. The root owns the deployment and its evidence. The selected self-hosted local IdP is configured and accepted for this topology; third-party/public issuer compatibility is not claimed. LLM mode remains fake and model evaluation stays PENDING per user choice. LocalStack broker messages and Jaeger traces remain ephemeral; drain jobs before broker maintenance. Public domain hosting and production queue/backup operations are outside this deployment.

Commands, exits and redacted output are indexed in VERIFY.md. The stack is intentionally left running for the user.
