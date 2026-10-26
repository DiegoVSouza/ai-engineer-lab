# Provider diagnostics correction

Offline result: PASS. No provider generation, production usage changes or product edits in this phase.

`python -S scripts/harness/test_live_provider_transport.py -v`: exit 0, 15 tests passed. `python -S scripts/harness/test_live_free_account.py -v`: exit 0, 20 tests passed. Lint/format/compilation passed.

The transport now emits numeric HTTP status and only a fixed provider error-code allowlist. JSON validation/tool-generation failure, authentication/model access, request schema, quota and transient HTTP statuses are distinguished. Unrecognized code strings become OTHER. Raw messages, failed generations and headers are discarded; unknown failed usage stays fully reserved and errors never trigger retry.

This change does not identify the historical P00 pilot error, whose status/code were lost by the old boundary. Its baseline remains INCOMPLETE and unchanged. The owning project must retain the new categorical fields and preserve `request_schema` rather than collapsing it into configuration before a declared development correction candidate. No holdout was executed or changed.

Official behavior references checked: [error status definitions](https://console.groq.com/docs/errors) and [structured output mode/error guarantees](https://console.groq.com/docs/structured-outputs). These references support handling possible validation errors; they do not establish the missing historical cause.
