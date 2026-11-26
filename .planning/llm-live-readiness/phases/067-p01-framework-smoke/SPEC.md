# P01 Framework Live Smoke

## Goal

Run one synthetic development workflow through each existing non-Core framework runner, using only the accounted root Groq transport.

## Bounds

- New campaign `p01-framework-smoke-v1`; five distinct cases, one per runner.
- Four provider requests maximum per workflow, 20 total maximum; the call ledger stops on the first uncertain or non-OK outcome.
- Paid spend USD 0.00; no holdout, confirmation, side effects, retry, or old campaign replay.
- The five framework adapters receive only the project-owned accounted client; they do not receive credentials or direct network clients.

## Acceptance

Each runner is covered by fake contract tests and one frozen-candidate live smoke attempt, with call counts reconciled against both project and root ledgers. Any blocked or failed workflow is reported incomplete without replay.
