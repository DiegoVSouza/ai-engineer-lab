# Production readiness

**Verdict: code complete, not ready for real customers.** The stack runs end to end locally and on Fly with `LLM_MODE=fake`, is observable, restarts without data loss and rolls back. What remains needs owner decisions, listed below. `python scripts/harness/production_readiness.py` re-checks the running stack and writes `artifacts/evidence/lab-stack/production-readiness-005/checklist.json`.

## Checklist

| Item | Result | What was proven | Evidence |
| --- | --- | --- | --- |
| Health checks | PASS | Every service with a health check is healthy; `otel` and `web-metrics` have no shell or HTTP client and `p04-worker` has no port | `checklist.json` |
| Readiness | PASS | Console `/readyz` passes through P05 `/readyz`, which pings PostgreSQL and Redis | `checklist.json`, P05 phase 032 |
| Reversible migrations | PASS | P05 and P04 up, down, up in a disposable database. Down files for 002 and 003 destroy data by nature | `scripts/harness/check_migrations.py` |
| Structured logs | PASS | JSON locally on `api`, `mcp`, `p04-api`, `web`; on Fly for P05, P04 and MCP. Worker stderr lines are not JSON | `checklist.json`, `fly-json-logs.txt` |
| Metrics | PASS local | Console, P05 API and P05 worker targets up. P04 is not scraped, and Fly has no Prometheus | `checklist.json` |
| Tracing | PASS local | P05 spans in Jaeger, and a browser `traceparent` reaches P05 | `check.txt` |
| Resource limits | PASS local | Memory and CPU limits on all 15 services. Values are estimates, not load-tested | `checklist.json` |
| Restart policy | PASS | `unless-stopped` on all 15 services | `checklist.json` |
| Secrets out of code | PASS | No key pattern in tracked files of the lab, P05, P06; `.env` ignored; no provider key in container environments | `checklist.json` |
| Restore | PASS local | `p04`, `p05` and `keycloak` dumps restored into a disposable database with identical row counts per table. Fly snapshots were not restored | `scripts/harness/restore_rehearsal.py` |
| Rollback | PASS | Local restart keeps data. On Fly the console went to the previous image and forward again, ready both ways | `restart-cycle.json`, `fly-rollback.txt` |

Evidence is in `artifacts/evidence/lab-stack/production-readiness-005/` and `remaining-readiness-008/`.

## Rollback

- **Local:** `git checkout` the previous commit in the affected project, then `python scripts/stack.py up`. Images are tagged `:local` and overwritten, so a rollback rebuilds. Data stays in named volumes.
- **Fly:** read the image with `fly machine list --app <app> --json`, then `fly deploy --app <app> --config fly/<dir>/fly.toml --image <previous image> --ha=false --yes`. Rehearsed on `supportops-lab-web`. Keep the previous image reference before each deploy.
- **Schema:** stop API and worker, deploy the previous image, take a dump, then apply the down file. See `projects/p05/docs/runbook.md`.

## Open items, all owner decisions

Blockers for real customers:

1. **Model quality is unknown.** `LLM_MODE=fake` everywhere. Deferred by the owner until code is complete.
2. **Queue and broker are emulated.** LocalStack provides SNS, with ephemeral state.
3. **Demo identity.** Bootstrap Keycloak admin, synthetic users on a public URL, `fly.dev` hostnames and a local CA in Compose. Needs a permanent admin, real users and a chosen domain.
4. **No automated backup.** Fly snapshots exist, and local dumps are manual. Needs a schedule, retention and an off-site copy.
5. **No load test.** Rate limits, CPU and memory limits are unmeasured under load, and Fly machines are the smallest size.

Should decide:

6. Push: `projects.lock.json` pins local commits and P06 has no remote, so `checkout` cannot clone on a fresh machine.
7. Five orphan anonymous volumes from phase 005 need the owner. `tmpfs` stopped new ones. The list is in `production-readiness-005/orphan-volumes.json`.
8. Screen reader run by a person. axe cannot replace it.
9. Fly has no Prometheus or dashboards. Choose a metrics destination if the public deployment stays.

## Known limits of the fixes

The pre-authentication IP limit is ten times the subject limit, so a burst across many users can still reach 600 requests per minute per proxy IP. The API trims token scopes by role, but the token itself still lists every scope. A manual refund must be approved within the 15-minute authorization lease; later the API answers 409 and the agent requests again.
