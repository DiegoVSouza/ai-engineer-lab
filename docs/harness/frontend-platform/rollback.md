# Rollback and cutover plan — frontend platform (F5)

Status: written, not rehearsed. Nothing here has been run against Cloudflare or Fly.

## Order of the cutover

1. **Owner go and access.** The owner authenticates Wrangler (`wrangler login`, or a `CLOUDFLARE_API_TOKEN` kept outside Git) and confirms the Pages project names in the inventory of `ops/pages/deploy.ps1` (`supportops-console`, `lab-portfolio`). On 2026-10-31 `wrangler whoami` reported an expired login, so this is the first blocker.
2. **Release P05 with CORS.** Bump P05 (additive, contract unchanged), rebuild the wheel, update `ops/stack/projects.lock.json`, set `CORS_ALLOWED_ORIGINS=https://<console-project>.pages.dev` in `fly/p05/fly.toml`, `fly deploy`. Check a preflight with `curl -i -X OPTIONS` from the Pages origin.
3. **Keycloak client.** Run `ops/stack/idp_clients.py` with `WEB_ORIGIN` listing the existing Fly web origin and the Pages origin, so both work during the cutover.
4. **Publish the fronts.** `ops/pages/deploy.ps1 -Site console -CreateProject` then `-Apply` (the first call without `-Apply` prints the plan). Same for `portfolio`.
5. **Public e2e.** Playwright with axe against the Pages URLs (sign-in through the real Keycloak, create a ticket, approve a refund). Record under `artifacts/evidence/pages/`.
6. **Retire the Fly web app only after step 5 passes.** Remove `supportops-lab-web` from `ops/fly/stack-apps.ps1` and from the up/down lifecycle, then destroy the app. Until then it is the fallback.

## Rollback

| Failure | Action | Evidence it worked |
| --- | --- | --- |
| A bad front release on Pages | Pages deployments are immutable. Redeploy the previous commit with `ops/pages/deploy.ps1`, or promote the previous deployment from the Cloudflare dashboard `[VERIFICAR in the Cloudflare docs before the first deploy]`. The per-deploy record in `artifacts/evidence/pages/` names the commit to return to. | The public e2e passes on the old commit. |
| P05 CORS release breaks the API | `fly releases` and `fly deploy --image <previous>` for `supportops-lab-p05`; unset `CORS_ALLOWED_ORIGINS`, which turns CORS off. The same-origin Fly web app still works because it proxies `/api`. | `/readyz` and the Fly web e2e pass. |
| Keycloak client change locks users out | Re-run `idp_clients.py` with only the previous origin. The client is applied idempotently. | PKCE sign-in from the Fly web origin. |
| The whole cutover | Keep `supportops-lab-web` running until the Pages e2e is green; reverting is then "do nothing". | n/a |

## Rehearsal required before calling F5 done

Deploy to a throwaway Pages branch, break it on purpose, roll back, and keep the logs. Until that exists, rollback is `PENDING`, not proven.
