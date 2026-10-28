# Verification

PENDING exact-delta authorization validation, injected Git/SQLite crash/idempotency/history/lease/path tests, root/consumer gates, committed-source dry-run, apply and post-apply UUID/prefix/unknown-reserve reconciliation. Paid remains zero; no model calls in this phase.

Pre-apply PASS: exact-delta validator; 28 migration regressions (14 historical, 14 +13) and final +13 owning-source recheck (14), covering dry-run/no-write, idempotency, unknown reserve/UUID/prefix preservation, malformed delta/auth/source, lease/link refusal, crash before/after replace and append-only audit. Root account/transport/dry-run suite passed 58 tests with recorded slot-0 attestation guard. P00 committed candidate 77f1289 passed 75 focused execution/batch/ledger controls and fast/format checks; full real-allocation-dependent gate follows apply. Source pin a0b681362098e2bd2a8e7d5f1d3e850fcbe22244. Independent verification remains pending. No runtime policy metadata has been changed yet.
