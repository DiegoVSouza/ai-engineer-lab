# W1b — verification before building

Run 2026-10-31. Sources are linked. Items I could not verify against a primary source are `PENDING`, not assumed. No machine was started and no model was called to produce this file.

## 1. Fly Machines API: can the cost guard work?

| Question | Finding | Status |
| --- | --- | --- |
| List machines without waking them | `GET https://api.machines.dev/v1/apps/{app}/machines` is the call the CLI uses ([Fly docs](https://fly.io/docs/machines/guides-examples/managing-machines-with-the-api/), [forum](https://community.fly.io/t/best-way-to-list-app-instances-at-runtime/19933)) | Docs confirmed through search; **PENDING** a direct HTTP call from a Function |
| State and timing without waking | Local check: `fly machine list --app supportops-lab-p05 --json` returned `state`, `created_at`, `updated_at`, `config.guest` (cpu kind, cpus, memory) and `events[]` with `start`/`exit`/`stop` types and epoch-ms timestamps. The machine stayed `stopped` | **Verified locally** (read only) |
| Compute cost from that | Runtime is the sum of `start` to `exit` intervals in `events[]`, priced by `guest` size. The cost guard is feasible as an estimate | Feasible. **PENDING**: how many events Fly retains per machine. If the window is short, the guard must poll often and keep its own ledger of intervals |
| Read-only token | `fly tokens create readonly` mints an org-scoped read-only token; deploy tokens are app-scoped ([forum](https://community.fly.io/t/best-way-to-list-app-instances-at-runtime/19933)) | **PENDING**: confirm in the first W8 step that a read-only token can list machines. The guard and `/api/status` must use it, never a deploy token |
| Reading state wakes nothing | Listing is a control-plane call, not a request through the Fly Proxy. A request to `*.fly.dev` is what wakes a machine (autostart) | Consistent with `fly-deployment.md`; the local list above confirms it |
| Stop autostart at the ceiling | Needs a write token. Kept in the Cron Worker only, as a separate secret | Design decision. Not built yet |

Conclusion: the guard is viable as an estimate from the machine events, not from the bill. The Fly dashboard stays the source of truth for the real invoice.

## 2. Fly prepaid credits

Fly's own billing page was not returned by search. What exists is forum material only, so treat it as indicative:

- Credits are applied first; the rest is charged to the card on file ([How do billing credits work?](https://community.fly.io/t/how-do-billing-credits-work/20724)).
- Staff said the account is suspended when credits run out and no card is on file ([same thread](https://community.fly.io/t/how-do-billing-credits-work/20724)).
- Early staff replies said there are no spending limits ([Can I set a billing limit per month?](https://community.fly.io/t/can-i-set-a-billing-limit-per-month/714)).
- One user reports prepaid credit rolling into an invoice anyway ([thread](https://community.fly.io/t/prepaid-budget-used-up-rolled-directly-into-billing/28103)).

Status: **PENDING** a primary source. Decision stands from the spec: Fly has no hard cap that I can rely on, so the USD 5 ceiling is enforced by our own guard and checked against the dashboard. Whether Postgres volumes survive a suspension is unknown, which is one more reason to keep a verified backup.

## 3. Groq limits

- Official page: [console.groq.com/docs/rate-limits](https://console.groq.com/docs/rate-limits.md). `retry-after` is set only on a 429. The other `x-ratelimit-*` headers are always present. Cached tokens do not count.
- Reset headers are durations (`2m59.56s`, `7.66s`), per the official example. A third-party guide claims timestamps; I did not trust it.
- Limits are per organization, and the real numbers depend on the model and plan.
- **PENDING**: the real limits for the four keys. Reading them needs one tiny completion per key. That is a live call, so it is folded into the W4 live smoke, inside the USD 10 ceiling, and recorded there. The failover code must parse durations and must not hard-code any number from this page.

## 4. Minimum wake order for the demo

From `docs/harness/lab-stack/fly-deployment.md` and `ops/fly/power.ps1`:

| Order | App | Why | Can stay asleep |
| --- | --- | --- | --- |
| 1 | `supportops-lab-db` | Ledger, tickets, pgvector | no |
| 2 | `supportops-lab-redis` | Queue for the worker | no |
| 3 | `supportops-lab-idp` | Sign-in (about 22 s cold) | no |
| 4 | `supportops-lab-p05` API and worker | Triage, refund flow. The worker polls Redis, so request-based autostop does not wake it | no |
| 5 | `supportops-lab-mcp` | MCP boundary in the tour | no, if the tour shows it |
| — | `supportops-lab-p04` | Async case demo | **yes**, until a P04 step is in the tour (**PENDING** decision with W8) |
| — | `supportops-lab-sns` | P04 outbox events only | **yes** |
| — | `supportops-lab-jaeger` | Starts itself on a Flycast connection | **yes** unless the trace step is wanted |
| — | `supportops-lab-web` | Retired after Pages works | yes |

Measured: web wake 16 s, Keycloak cold start 22 s (`artifacts/evidence/fly/idle-acceptance/idle-probe.json`). The real wake time of the reduced set is **PENDING** a measurement in W8.

## 5. Turnstile and the CSP

[Cloudflare reference](https://developers.cloudflare.com/turnstile/reference/content-security-policy): `challenges.cloudflare.com` in `script-src` and `frame-src`. `connect-src 'self'` only for pre-clearance, which this site does not use. Cloudflare also documents a nonce-based setup.

Decision: add exactly `https://challenges.cloudflare.com` to `script-src` and `frame-src`, in a `_headers` block for `/demo/*` only. Every other route keeps the strict policy. **PENDING**: a real-Chrome check on the deployed `/demo/` that reports zero violations, because the widget loads resources in sequence and a second directive can show up.
