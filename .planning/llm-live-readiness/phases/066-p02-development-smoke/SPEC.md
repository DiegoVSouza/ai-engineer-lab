# P02 Development Smoke

## Goal

Run at most four new live development trials on the frozen P02 candidate through the existing accounted Groq transport.

## Constraints

- Campaign ID: `p02-dev-v4-smoke`; one trial and one provider request per case.
- The four attempts join the already consumed 72 P02 development attempts; the cumulative ceiling is 76.
- Select the first four cases from the development-only ordering. Never load or execute holdout rows.
- Free-only: paid spend is USD 0.00. Stop on the first non-OK or uncertain provider result.
- Do not resume or replay p02-dev-v1, v2, or v3.

## Acceptance

The exact root authorization and candidate manifest are committed and source-bound; fake plumbing passes; live output records status, exit code, and provider usage for each attempt; total new attempts never exceeds four.
