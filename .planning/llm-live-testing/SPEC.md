# Live LLM Testing Across Lab Projects — Specification

## Status

Draft. The next implementation chat must first identify the target project(s) and confirm each project's existing SDD state before changing product code.

## Goal

Run bounded, reproducible evaluations against real LLM providers for the selected lab projects, using the root `.env` credentials without exposing secrets. Prefer Groq with `openai/gpt-oss-20b`, already confirmed reachable through the official Groq SDK; use another configured provider/model only when the selected project requires a capability Groq cannot provide or Groq is unavailable.

## User and problem

The developer needs evidence from real model executions rather than mocks alone. Free-tier accounts have shared rate and daily limits, so runs must be small, serialized where appropriate, and cost/token bounded. Failures must distinguish invalid credentials, model access, rate limits, transient transport errors, provider policy errors, and evaluator/product failures.

## Scope

- Inspect candidate projects and select only projects with a relevant existing evaluation workflow; do not infer that every project needs a live integration.
- For each selected project, inspect its `harness.yaml`, intake/decisions, phase specs, provider adapter, tests, and existing artifact conventions before implementation.
- Add or reuse a real-provider test/evaluation path that is opt-in (`LLM_MODE=live`) and leaves fake/replay behavior deterministic and offline.
- Load credentials from environment or the lab-root `.env` through the project's existing secret-loading convention; never log, persist, or commit secret values.
- Support bounded key rotation for `GROQ_API_KEY`, `GROQ_API_KEY_1` through `_4`: rotate after retryable throttling/transient failures, apply bounded exponential backoff with jitter, respect `Retry-After` when present, and stop after one bounded pass through configured keys. Do not rotate on authentication, permission, invalid-model, or request-validation errors.
- Use the model ID returned by the current provider catalog/docs when available; default to `openai/gpt-oss-20b` only after confirming it is listed for the key. Record the model actually returned by each run.
- Record command, exit code, sanitized provider/model metadata, timestamps, token usage, retry/rotation count, outcome, and redacted error class/status in project `artifacts/`.
- Estimate/record actual run usage from provider-reported token counts. Use `PENDING` for costs unless authoritative current pricing and actual usage support a calculation. Enforce a small per-run token/request cap and the project's configured budget.
- Add eval assertions tied to the selected project's behavior, not merely a successful HTTP response. Keep each live run small enough for free-tier limits.

## Out of scope

- Deploying, publishing, pushing, or contacting external parties.
- Broad benchmark claims, fabricated cost/quality metrics, or a large load test.
- Printing key prefixes, fingerprints, or secret-bearing request/response headers.
- Changing `harness-kit/` or shared kit behavior without a separate kit phase and validation against at least two real projects.
- Falling back silently from a failed live request to fake output.

## Acceptance criteria

1. Selected project(s) and their live-evaluation purpose are stated in the phase artifacts.
2. Fake-mode tests remain offline and deterministic; live mode is explicitly opt-in.
3. A tiny real-provider smoke/evaluation run succeeds or produces a precise, sanitized failure classification with no secret leakage.
4. Rotation covers configured keys at most once per request cycle, retries only retryable failures, honors provider backoff guidance, and has tests for exhaustion and non-retryable errors.
5. Model selection is validated against current provider information; successful artifacts record the actual model and usage.
6. Every real run stores command, exit code, and sanitized output in the selected project's `artifacts/`; metrics without a run are `PENDING`.
7. Budget/token limits and stop conditions are explicit before making provider calls.
8. Project-specific `SPEC.md`, `PLAN.md`, and `VERIFY.md` are complete before implementation; no product code changes occur in this specification phase.

## Security and operational constraints

- Secrets remain only in the existing local `.env`/environment and are ignored by Git.
- Never echo, hash, fingerprint, or log credentials.
- Avoid parallel fan-out against free-tier keys; default to sequential calls and low token limits.
- Use finite connect/read timeouts, bounded retries, jitter, and a hard retry ceiling.
- Stop on exhausted daily quota or budget; do not switch providers in a way that can incur unapproved charges.

## Open decisions for PLAN

- Which project(s) should receive the live evaluation, based on existing profiles and evaluation suites?
- Which existing provider interface and artifact conventions should be reused in each project?
- The exact per-project request/token ceiling and the smallest meaningful domain evaluation case.
- Whether project-root `.env` loading is already supported or a safe environment injection is needed.
