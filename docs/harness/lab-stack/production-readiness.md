# Production readiness

**Verdict: not ready for real customers.** The stack runs end to end, is observable, and restarts without data loss, locally with `LLM_MODE=fake`. The blockers below stay open. `python scripts/harness/production_readiness.py` re-checks the running stack and writes `artifacts/evidence/lab-stack/production-readiness-005/checklist.json`.

## Checklist

| Item | Result | What was proven | Evidence |
| --- | --- | --- | --- |
| Health checks | PASS | 12 of 14 long-running services report healthy; `otel` has no shell or HTTP client and `p04-worker` has no port. Neither has a health check | `checklist.json` |
| Readiness | PASS | Console `/readyz` passes through P05 `/readyz`, which pings PostgreSQL and Redis. Failure path covered by P05 tests | `checklist.json`, P05 phase 032 |
| Reversible migrations | PASS | P05 and P04 up, down, up in a disposable database. Down files for 002 and 003 destroy data by nature | `scripts/harness/check_migrations.py` |
| Structured logs | PASS local | JSON on `api`, `mcp`, `p04-api`, `web` | `checklist.json` |
| Metrics | PASS local | Every Prometheus target up | `checklist.json` |
| Tracing | PASS local | P05 spans in Jaeger; `stack.py check` verifies one correlated trace | `check-after-restart.txt` |
| Resource limits | PASS local | Memory limit on all 14 services. CPU limits not set | `checklist.json` |
| Restart policy | PASS | `unless-stopped` on all 14 services | `checklist.json` |
| Secrets out of code | PASS | No key pattern in tracked files of the lab, P05, P06; `.env` ignored; no provider key in container environments | `checklist.json` |
| Rollback | PASS for restart, INCOMPLETE for release | Real `down` and `up`: 86 foreign containers, volumes and P05 rows unchanged, `persistence` and `check` exit 0. A release rollback has never been rehearsed | `restart-cycle.json` |

## Rollback

- **Local:** `git checkout` the previous commit in the affected project, then `python scripts/stack.py up`. Images are tagged `:local` and overwritten, so a rollback rebuilds. Data stays in named volumes.
- **Fly:** `fly releases --app <app>`, then `fly deploy --app <app> --image <previous image>`. Keycloak, PostgreSQL and Redis data live in volumes with 14-day snapshots.
- **Schema:** stop API and worker, deploy the previous image, take a dump, then apply the down file. See `projects/p05/docs/runbook.md`.

## Open items

Blockers for real customers:

1. **Model quality is unknown.** `LLM_MODE=fake` everywhere. Deferred by the user until code is complete.
2. **Fly console never deployed.** `fly-up` is tested by dry run and a fake `flyctl` only. Needs the user's authorization, and the first run will exercise the real deploy path, including P05 0.4.4.
3. **Rate limit is shared behind the console.** P05 cannot decode OIDC tokens in its middleware, so it buckets by client IP, and every console user arrives from the `web` container: 60 requests per minute for all of them. Fix: bucket by verified subject after introspection, or trust `X-Forwarded-For` from the proxy only.
4. **Queue and broker are emulated.** LocalStack provides SNS, with ephemeral state. A production broker must replace it.
5. **Demo identity.** Bootstrap Keycloak admin, synthetic users, and a local CA. Needs a permanent admin, real users and public certificates.
6. **No automated backup.** Fly snapshots exist; the local stack has only manual dumps. No restore rehearsal since 2026-10-23.
7. **Manual refund requests have no effect path.** `POST /v1/tickets/{id}/refund-approvals` creates an approval that no worker executes when approved; only the triage task does. The console says so. Fix: enqueue the effect, or remove the route from the console.
8. **Console tokens carry every scope.** Keycloak scopes are not role-bound here, so an approver's token also has agent scopes. Separation of duties holds because P05 checks role and refuses self-approval, but least privilege does not.

Should fix:

9. Unpushed commits: `projects.lock.json` pins local commits and P06 has no remote, so `checkout` cannot clone on a fresh machine. Push needs authorization.
10. Fly logs are not JSON: `--log-config` is applied by Compose only, and `/ops` does not exist in Fly images.
11. Prometheus does not scrape the console, and the browser sends no `traceparent`, so traces start at P05.
12. No CPU limits; memory limits are estimates from one idle measurement, not load tests.
13. `scripts/check_services.py` (P05's own full service gate) has not run on 0.4.4; the root `stack.py check` and browser e2e have.
14. 5 orphan anonymous volumes remain from this phase: LocalStack and Jaeger `down` cycles, and two early runs of `check_migrations.py`. Both causes are fixed and later runs add none. Deleting them was refused by the session's permission mode, so they need the owner. The list is in `artifacts/evidence/lab-stack/production-readiness-005/orphan-volumes.json`.
