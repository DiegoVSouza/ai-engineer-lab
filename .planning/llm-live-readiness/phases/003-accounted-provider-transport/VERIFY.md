# Verify

- [x] Explicit project opt-in, synthetic-only scope, fixed model and numbered-key preflight required; keys remain in memory for the session.
- [x] Full input byte bound plus bounded chat/tool framing slack and unchanged output caps checked before HTTP; durable reservation precedes dispatch.
- [x] Known usage reconciles, unknown usage stays charged, observed bound overrun and model mismatch prevent later attempts across projects.
- [x] Quota/transport/permanent errors never retry or expose content/credentials/raw headers; generation redirects are refused.
- [x] JSON-lines protocol carries only transient synthetic output; artifacts contain sanitized evidence. No production project opt-in exists in this phase and no generation was performed.
- [x] Twelve transport tests and twenty prior guard tests pass, exit 0. Lint, format and compilation pass; initial import-order lint failure was retained.
- [x] Staged implementation paths and evidence reviewed for local commit.
- [ ] Independent clean-context verification remains pending.
