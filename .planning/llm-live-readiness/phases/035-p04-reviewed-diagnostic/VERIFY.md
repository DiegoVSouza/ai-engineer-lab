# Verification

PENDING focused authority/history/cap/no-replay tests and account/transport regressions, command/cwd/exit/sanitized output. No provider access.

PASS: seven focused tests on attempt3/3; attempt1 copied decision string mismatch, attempt2 original authorization JSON used Windows cp1252 and was rejected by strict UTF-8. Corrected encoding to ASCII JSON escapes; exact user decision preserved. Historical failures in focused-attempt1/2.json. Account33, transport22 and P01 exception5 regressions PASS. No provider calls. Original receipt, three-call logical reserve and unresolved original step required; closed diagnostic, wrong identity, changed history/authority, uncertain and failed continuation denied. Evidence artifacts/evidence/llm-live-readiness/p04-reviewed-diagnostic/*.json.
