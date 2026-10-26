# Accounted provider session

Offline transport result: PASS. Real campaign/project integration: INCOMPLETE.

`python -S scripts/harness/test_live_provider_transport.py -v`: exit 0, 13 tests passed. `python -S scripts/harness/test_live_free_account.py -v`: exit 0, 20 guard regressions passed. Lint, format and compilation passed; initial import-order lint failure remains preserved.

A read-only preview operation validates the full rendered reservation against all project logs before a launcher reserves a logical trial. Preview never grants a consumable token or increments usage; actual reservation rechecks atomically. Capacity exhaustion can therefore stop a chunk before creating an unnecessary uncertain local trial.

Tests prove opt-in/live mode precede credentials/storage, a full durable input/output reservation exists before POST, rendered schemas/tools and Unicode bytes count toward input limits, original output caps and fixed model cannot be overridden, hidden reasoning is excluded, failed/unknown usage remains charged, and quota/credential/transport/model mismatch/usage overrun stop without retry. A truncated/semantically wrong observation returns once for the owning product grader rather than resampling.

The session uses numbered root credentials only, checks the authenticated catalog once over that same in-memory set, and sends a single bounded HTTP request per provider attempt with redirects refused. Unknown provider diagnostics and raw headers never enter logs or usage storage. Response content exists only in the transient subprocess protocol; no content is stored by this transport.

The full-request token reservation uses compact UTF-8 payload bytes plus explicit chat/function framing slack. It is a conservative upper bound awaiting actual model usage validation; any observed excess is retained and blocks further calls for reconciliation. `max_completion_tokens` retains existing project caps and includes reasoning; `include_reasoning=false` prevents emitting the separate reasoning field. Current parameters were checked against [official reasoning documentation](https://console.groq.com/docs/reasoning).

No production project manifest/database was created and no generation was performed in this phase. Next: implement the owning P00 launcher/report binding, commit its candidate, then run a bounded authorized free-only pilot. Human review and promotion remain pending.
