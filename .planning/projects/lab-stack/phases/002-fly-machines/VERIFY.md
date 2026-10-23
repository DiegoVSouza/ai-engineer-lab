# VERIFY — Fly.io portfolio deployment

Status: IN_PROGRESS; local Redis Streams acceptance and checkpoint restoration passed. Fly authentication is available; public apps have not been created or deployed yet.

The Fly Agent guide was fetched successfully on 2026-10-23 and directs deployment/public URLs to Machines, says to inspect existing apps first, keep credentials in Fly secrets, and verify deployment via status/logs. `fly auth whoami` exits 0. `fly apps list` showed nine existing personal apps; none are part of this lab and none were changed. No lab Fly app, machine, or volume has been created yet.

The local unified Compose stack was rebuilt without removing its named volumes. P04 0.1.4 and P05 0.4.3 now use Redis Streams for delivery. `python scripts/stack.py check` exits 0 with OIDC API/MCP, tenant isolation, HITL, P04 Redis Streams worker, Keycloak revocation and P03 telemetry acceptance. Evidence: `artifacts/evidence/fly/local-compose-gate.txt`.

The local-only checkpoint is `artifacts/checkpoints/pre-fly-final-20261023/`. It includes Git bundles, a full PostgreSQL cluster dump, Redis RDB and read-only archives of all 12 Compose volumes. The PostgreSQL dump restored successfully into a disposable pgvector/PostgreSQL 16 instance; Redis RDB loaded in a disposable Redis instance; all volume archives passed tar integrity checks. SHA-256 manifest and restricted Windows ACLs are present. Restore evidence: `artifacts/evidence/fly/checkpoint-restore.txt`. This checkpoint is excluded from Git.

No public data services, Fly machines, volumes or billable Fly resources have been created. Remaining gates: render/validate deployment configs, deploy only the new lab apps in `iad`, inspect health and public endpoints, and check Fly volume snapshots and persistence before considering cleanup of any lab Docker stack.

| Gate | Command | Exit | Evidence |
| --- | --- | ---: | --- |
| Fly CLI identity | `fly auth whoami` | 0 | Interactive login approved; existing account apps inventoried |
| Local Compose Redis Streams stack | `python scripts/stack.py check` | 0 | `artifacts/evidence/fly/local-compose-gate.txt` |
| Checkpoint restore and volume archive integrity | Disposable PostgreSQL/Redis restores and tar checks | 0 | `artifacts/evidence/fly/checkpoint-restore.txt` |
