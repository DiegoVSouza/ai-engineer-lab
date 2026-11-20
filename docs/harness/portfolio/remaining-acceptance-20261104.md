# Remaining acceptance, 2026-11-04

This is a review packet, not authorization to execute external actions or spend. Existing reservations, consumed operation identities and stop conditions remain authoritative.

| Owner | Finite next acceptance scope | Required input and evidence |
| --- | --- | --- |
| P00 dataset/rubric reviewers | Resolve cases p00-live-025, 026 and 037 against their protected answers and original rubric; record disagreement and reviewer identity. | Phase 028 final-analysis.md records 27/36 development passes and the contract conflicts. Human annotations must be authored by reviewers. No holdout access is needed for this review. |
| P00 budget owner | After contract resolution, decide whether to fund a separately frozen development candidate. | Current primary remainder is 84 holdout calls, with 60 separate confirmation calls; neither can fund correction. Specify an additional finite call/token/time ceiling and paid/free policy before any new execution. No allocation amount is proposed without the revised contract. |
| P00 local service owner | Enable the pinned LocalStack 2026.08.3 image for the isolated phase 044 check. | Valid license/authentication stored outside Git, or an explicit scoped decision to use another supported image followed by fresh configuration verification. Existing exit 55 and runner exit 1 remain recorded. |
| P01 source/evaluation owners | Supply a versioned non-customer KB/billing corpus, tenant/record ACL contract and comparable six-runner evaluation scope. | Existing four-call synthetic Core acceptance is operational only. Review rubric/dataset and finite budget before live comparison; preserve previous operation counters. |
| P02 integration owner | Select a real external corpus and caller identity contract, then define model-refusal and citation-grounding acceptance cases. | Local retrieval/injection screening and synthetic refusal do not establish integrated model refusal or entailment. Use fake controls first; real-provider work requires finite authorization. |
| P03 privacy/operations owner | Inspect the flagged exception log and accept service failure telemetry using explicit forbidden content categories and backend/exporter reliability criteria. | Phase 026 corrected the scope: saved Jaeger summary confirms one real trace but also flags database.ticket.get / log:exception.message; values are absent. Inspect eligible raw telemetry without copying content to public artifacts. Production cost/latency/quality and failure-path privacy remain separate. |
| P04 operations owner | Review configured exporter delivery and API/worker failure-span privacy on the intended production backend. | Local OTLP and fake/service evidence is available; define authorized failure injection and reliability criteria. Terraform apply and load testing require separately stated scope and authorization. |
| P05 identity/product owners | Decide whether third-party IdP and revocation of queued jobs remain release requirements; if retained, identify issuer, test tenant and revocation semantics. | Keycloak-on-Fly acceptance already exists. Queue authorization snapshot/expiry does not establish immediate issuer revocation. Semantic quality and human review remain separately gated. |
| P06 | No new Fly or session-renewal execution is proposed. | Existing main-flow and silent-renewal acceptance remain the recorded evidence. |
| P07 owner/accessibility reviewer | Approve CV draft; run screen-reader and visual review; exercise Turnstile start flow; measure FPS on a named physical device. | Record browser/device, route, actions, expected/actual result and reviewer. Current local automated gate passed 60 browser tests; it supplies none of these human/device acceptances. No publication is authorized by this packet. |
| P08 accessibility/visual reviewer | Review screen-reader navigation and squint/readability screenshots in both themes. | Keep human outcomes pending until recorded. The Three.js scene belongs to P07 and is outside P08 scope. |
| Independent verifier | Review the historical contracts that explicitly reserve unchecked boxes for independent sign-off. | The per-file map is verify-triage-20261104.md. Implementer test output alone does not provide that sign-off. |

Before an authorized execution, prepare its own bounded phase and preserve the current source fingerprint, ledgers and immutable artifacts. No secrets should be supplied in this document or committed logs.

## Addendum, 2026-11-09: changes after the 2026-11-04 packet

The table above is kept as written on 2026-11-04. These items changed afterwards; sources are the P00 `docs/harness/decisions.md` and `failures.md`, and the P07 `docs/harness/decisions.md`.

| Row above | Status on 2026-11-09 |
| --- | --- |
| P00 dataset/rubric reviewers (cases 025, 026, 037) | Owner decided on 2026-11-06: 025 and 026 keep their expected outcomes; 037 became `request_info` with no tool (dataset `live-v2`). Rule: no identifier means no lookup. |
| P00 budget owner | Free Groq keys up to provider limits with a hard owner cap of USD 5.00 in total. `authorized_paid_spend_usd` stays 0.00. The protected holdout was consumed on 2026-11-06 (29/84 = 34.5%, older dataset). The 60 confirmation calls were consumed on 2026-11-07 as a single-use final run: 54/60 = 90.0% (Wilson 95% 0.799 to 0.953), campaign `free-final-c1`. No further tuning on that split; a changed candidate needs fresh cases. |
| P00 reviewers (independence) | Independent reviewer requirement waived by the owner (`WAIVED_BY_OWNER`). This is owner approval, not independent verification. The owner recorded the human review as done on 2026-11-09 (owner attestation, `OWNER_REVIEWED`). |
| P00 local service owner (LocalStack) | LocalStack replaced by `motoserver/moto:5.2.5` (no token). The isolated moto check passed (`artifacts/evidence/moto-services-046/result.json`). The feature `local-services-and-hosted-ci` still reads `LOCAL_SERVICE_E2E_PENDING` until a full local service e2e is recorded. |
| P07 screen-reader review | No human screen-reader tester is available. `projects/p07/scripts/a11y-reader.mjs` runs an automated pass (Playwright + Edge: accessibility tree, headings, landmarks, tab order, axe). It is the technical evidence; the owner recorded the human review as done on 2026-11-09 (owner attestation). |
| P07 CV approval | CV text approved by the owner. The site-versus-CV claim diff is not done yet (deferred by the owner). |

Still open and unchanged: P01 corpus and six-runner comparison, P02 external RAG and refusal, P03 and P04 privacy and production acceptance, P05 third-party IdP, Turnstile start flow, device FPS, and independent sign-off on historical contracts.

## Addendum 2, 2026-11-09: owner decisions of the day

Owner reply (verbatim, PT): "pode usar os modelos da groq tem as env ai documentada, o idp terceiro deixa on hold, pode subir no docker e no fly, o fps no celular deixa on hold".

| Subject | Decision | Limits that stay in force |
| --- | --- | --- |
| Groq models | Authorized for the remaining model-quality evaluations (P01, P02, P05) using the keys already documented in the lab `.env` (`GROQ_API_KEY*`, `GROQ_MODEL`; names only, never values). | Free keys up to provider limits, hard owner total-loss cap USD 5.00 (decision of 2026-11-06), `authorized_paid_spend_usd` 0.00, root free-account ledger and the shared daily token window. Each campaign still needs its own bounded phase, a frozen candidate and an envelope migration. The consumed P00 final split is not reusable. |
| Third-party IdP (P05) | ON HOLD. Features `auth-tenant-scope`, `mcp-trusted-principal`, `network-mcp-auth`, `product-end-to-end-orchestration`, `durable-authorization-snapshot`, `mcp-external-token-introspection` keep `THIRD_PARTY_IDP_PENDING` or `INCOMPLETE_EXTERNAL_IDENTITY`. | Keycloak on Fly is not a third-party IdP. |
| Docker and Fly | Authorized to start the local Docker stack and wake the Fly stack for acceptance runs (P03, P04, P05, P00 local services). | Wake, use and power down again; record commands, exit codes and saved output. No new paid resources, no DNS or public-facing changes beyond the existing apps. |
| Device FPS (P07) | ON HOLD. `portfolio-3d-scene` keeps `DEVICE_FPS_PENDING`. | No FPS number without a named physical device. |
