# Phase 004 — Provider error diagnostics

P00's first real pilot exposed an observability defect: a provider failure was reduced to `request_schema` and then `configuration`, with no retained HTTP status or categorical provider code. Its exact historical cause is unknown and must not be retroactively invented or rerun to obtain a passing sample.

Persist no raw provider body/message/failed generation. Extract only a fixed allowlist of provider error codes plus numeric HTTP status into the transient protocol; classify structured-generation failure separately from invalid request, authentication/model access, transport and quota. Unknown strings become OTHER. Keep every failed usage reservation conservative and retries disabled.

Acceptance: simulated API-error tests prove categorical diagnostics and no raw/private strings escape; prior accounting/transport regressions pass. No new provider generation or product file changes in this root phase. The owning P00 phase must separately preserve these fields and declare any development correction.
