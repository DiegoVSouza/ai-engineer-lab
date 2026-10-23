# VERIFY — Fly.io portfolio deployment

Status: PASS_FLY_DEPLOYED. Public and private app acceptance, local stack, and checkpoint restore gates passed. Model quality remains PENDING.

The Fly Agent guide was fetched on 2026-10-23 and directs deployment to Machines, inspection of existing apps, secret storage, and verification through status/logs. `fly auth whoami` exited 0. Existing personal apps were inventoried and left untouched. Eight lab apps now run in `iad`, one machine per process group.

P04/P05 public endpoints, OIDC tenant checks, MCP tenant authorization, Redis queue completion and request-based cold autostart passed. DB, Redis, SNS and Jaeger are private-only. PostgreSQL, Redis and P05 graph volumes have manual 14-day snapshots; daily snapshots are configured. The local checkpoint and Docker stack remain available for rollback. See `docs/harness/lab-stack/fly-deployment.md` for machine layout, approximate cost and recovery limits. The deployed mode is fake; no model-quality claim is made.

The local unified Compose stack was rebuilt without removing its named volumes. P04 0.1.4 and P05 0.4.3 use Redis Streams for delivery. `python scripts/stack.py check` exits 0 with local OIDC API/MCP, tenant isolation, HITL, durable workers and telemetry acceptance. Evidence: `artifacts/evidence/fly/local-compose-gate.txt`.

The local-only checkpoint at `artifacts/checkpoints/pre-fly-final-20261023/` contains Git bundles, PostgreSQL dump, Redis RDB and archives of all 12 Compose volumes. Restore checks passed in disposable services; the checkpoint is excluded from Git and has restricted Windows ACLs. Evidence: `artifacts/evidence/fly/checkpoint-restore.txt`.

| Gate | Command | Exit | Evidence |
| --- | --- | ---: | --- |
| Local Compose Redis Streams stack | `python scripts/stack.py check` | 0 | `artifacts/evidence/fly/local-compose-gate.txt` |
| Checkpoint restore and volume archive integrity | Disposable PostgreSQL/Redis restores and tar checks | 0 | `artifacts/evidence/fly/checkpoint-restore.txt` |
| Fly config/build/deploy | `ops/fly/deploy.ps1`; `fly config validate --strict` | 0 | `artifacts/evidence/fly/preflight-configs-builds.txt`; `provision-build.txt`; `provision-deploy.txt` |
| OIDC, tenant separation, MCP authorization and queues | Public HTTP acceptance | 0 | `artifacts/evidence/fly/oidc-acceptance.txt`; `mcp-oidc-acceptance.txt`; `p04-redis-queue-acceptance.txt`; `p05-redis-queue-acceptance.txt` |
| Cold autostart and machine inventory | Public wake-up checks; `fly machine list` | 0 | `artifacts/evidence/fly/autostart-acceptance.txt`; `final-resource-inventory.txt` |
| Manual regional recovery points | `fly volumes snapshots create/list` for PostgreSQL, Redis and P05 | 0 | `artifacts/evidence/fly/manual-volume-snapshots.txt` |

The local stack and old volumes were preserved. No live model evaluation ran; keep model-quality metrics PENDING until an evaluation run is recorded.
