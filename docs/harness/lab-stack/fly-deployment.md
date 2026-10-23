# Fly.io portfolio deployment

The lab runs in Fly.io's `iad` region. P00–P03 are reusable libraries and are installed into the P04/P05 products; they do not need separate web machines. P04 and P05 each run an API and a Redis Streams worker. P05's MCP endpoint is deployed as its own app.

## Apps

| App | Purpose | Public access | Idle policy |
| --- | --- | --- | --- |
| `supportops-lab-p04` | P04 API and worker | API at `https://supportops-lab-p04.fly.dev` | API stops at idle; worker stays on for queue delivery |
| `supportops-lab-p05` | P05 API and worker | API at `https://supportops-lab-p05.fly.dev` | API stops at idle; worker stays on for queue delivery |
| `supportops-lab-mcp` | P05 MCP server | `https://supportops-lab-mcp.fly.dev/mcp` | Stops at idle and starts through Fly Proxy |
| `supportops-lab-idp` | Keycloak OIDC realm | `https://supportops-lab-idp.fly.dev/realms/supportops` | Always on because APIs introspect tokens against it |
| `supportops-lab-db` | PostgreSQL 16 + pgvector | Private 6PN only | Always on; 10 GB encrypted volume |
| `supportops-lab-redis` | Authenticated Redis Streams | Private 6PN only | Always on; 1 GB encrypted volume, AOF enabled |
| `supportops-lab-sns` | LocalStack SNS compatibility for P04 outbox events | Private 6PN only | Always on; topics are recreated by the ready hook |
| `supportops-lab-jaeger` | P05 OpenTelemetry receiver and trace UI | Private 6PN only; use `fly proxy` for the UI | Always on to receive spans; trace storage is in memory |

Database and Redis have no public service bindings. Fly secrets hold all runtime passwords and signing keys. A local copy of the generated demo credentials is kept outside Git in the ACL-restricted checkpoint directory. Rotate those demo passwords before sharing the identity realm broadly.

## Machine sizing and cost

The API and MCP process groups use shared 1x/256 MB machines and Fly Proxy autostop with zero minimum warm machines. Persistent dependencies and workers remain at one machine each. The workers poll Redis Streams and cannot use request-based autostop; stopping them would leave queued work unprocessed. Keycloak uses shared 1x/2 GB because its measured startup/runtime footprint exceeded 1 GB locally.

Using the Fly list prices checked on 2026-10-23, the always-running machines total about USD 27.13 per 30 days. The three volumes total 12 GB, about USD 1.80 per month. The rough idle baseline is therefore USD 28.93 per month before stopped root filesystems, stored snapshots above the included 10 GB, data transfer, or time when the three web process groups are active. Actual billing is account and usage dependent.

## Backups and restore

The local checkpoint at `artifacts/checkpoints/pre-fly-final-20261023/` contains a verified PostgreSQL cluster dump, Redis RDB, all 12 local Compose volume archives and Git bundles. It is excluded from Git and protected by a Windows ACL. Fly's Postgres, Redis and P05 graph volumes use daily snapshots with 14-day retention; manual acceptance snapshots are also created after deployment checks.

List and create Fly snapshots with:

```powershell
fly volumes list --app supportops-lab-db
fly volumes snapshots list <volume-id> --app supportops-lab-db
fly volumes snapshots create <volume-id> --app supportops-lab-db
```

Restore by creating a replacement volume from a selected snapshot with `fly volumes create <new-name> --app <app> --region iad --size <gb> --snapshot-id <snapshot-id> --yes`, then attach it to a replacement machine. Never replace a live volume as a routine check. Volume snapshots are regional recovery points, not an independent offsite backup. Jaeger uses in-memory storage and loses old traces when its machine restarts.

## Model quality options

The deployed runtime uses `LLM_MODE=fake`. This keeps authorization and queue behavior deterministic; it does not measure model quality. Model evaluation remains `PENDING`.

1. Replay evaluation compares prompt/configuration changes against recorded cassettes. It is repeatable and has no provider charge, but only tests the captured examples.
2. Live evaluation sends a fixed, redacted dataset to a provider and compares task quality, latency, failures and cost. This requires provider credentials and a separate spend decision; no live provider calls are enabled in this deployment.
3. Self-hosting an open model provides control over weights and requests, but is not suitable for these minimum CPU machines. It needs a GPU-capable host or a separate inference service and a larger cost envelope.

Start with replay, then run a small live comparison only after choosing a provider and dataset. Keep model score claims `PENDING` until those runs are recorded in project artifacts.
