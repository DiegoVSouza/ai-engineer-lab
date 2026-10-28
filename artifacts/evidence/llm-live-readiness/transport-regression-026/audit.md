# Custom transport audit

Source inspected: `live_free_account.catalog_request/catalog_preflight`, `live_provider_transport.ProviderSession.complete`, P00 `scripts/campaign_execution.ProviderClient` and `campaign_batch.run_chunk`.

- Catalog: at most three connection attempts per credential, identical Request object; 4-second socket timeout; two jitter waits capped at 0.25/0.5 seconds. Five unique authorized slots imply at most 15 GET opens and 3.75 seconds jitter. HTTP errors, including 429, are never retried. Reading a response body is outside the retry loop, so read failures do not repeat a request.
- The apparent 12.75 seconds per credential is NOT a total deadline. Python documents timeout for blocking operations; a slow body or DNS resolution is not proven bounded by this arithmetic. P00's actual parent uses an 80-second initialization receive bound, then kills/waits up to five seconds. Other consumers need their own parent-bound audit. No SDK retry semantics were used as transport proof.
- Confirmed and fixed: catalog used unbounded `read()`; now reads at most 1,000,001 bytes and rejects over 1,000,000. Context-managed success/malformed responses close on exit.
- Confirmed and fixed: completion HTTPError body-read timeout escaped before close. A try/finally now closes it; unreadable body yields status-only sanitized classification and preserves unknown usage at the full reservation. No POST retry or key switch occurs in that attempt.
- Completion success reads at most 2,000,001 bytes, rejects oversized bodies and closes the response. POST uses a no-redirect opener. Metadata's default standalone opener still follows redirects; this requires a separate scope correction before claiming equivalent credential redirect protection.
- P00's actual request receive timer is min(20, requested timeout + 2), normally 17 seconds, followed by process kill/wait on timeout. If killed after send, the durable reserved provider event remains unresolved; no replay is justified. Whole-campaign deadline is checked around dispatch; initialization/cleanup overhead is outside an exact wall-clock SLA.
- Reservation: account machine lease covers cumulative approval, slot selection, FULL-synchronous insertion and commit before HTTP. Completion is appended separately. A slot is a variable number at dispatch, not authenticated organization/key identity. Historical attribution cannot be reconstructed by modulo arithmetic.
- Sanitization: only allowlisted codes/numeric rate metadata are returned; raw provider body and credential are not in protocol diagnostics. Transport test fixtures use synthetic PRIVATE sentinels only.

Official references checked 2026-10-28: https://docs.python.org/3.13/library/urllib.request.html (blocking-operation timeout), https://console.groq.com/docs/rate-limits (429 and organization-wide limits). Published limits do not prove billing tier or usable account capacity. No provider access occurred in this audit.

Evidence: attempt1.json and *attempt1.txt preserve the two reproduced failures; attempt2.json and *attempt2.txt record correction PASS (28 account, 20 transport). Commands use P00's locked environment; all credentials/provider responses are injected fixtures.

Remaining: cross-project regression, metadata redirect protection, effective total-bound verification per consumer, credential billing eligibility, P00 complete receipt/crash/authorization audit. These are executable pending work, not demonstrated external blockers.
