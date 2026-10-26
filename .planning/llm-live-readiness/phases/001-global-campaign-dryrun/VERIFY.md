# Verify — Account-wide campaign dry-run

Save outputs and exits in `artifacts/evidence/llm-live-readiness/global-dry-run/`.

- [ ] Synthetic contract tests cover valid P00–P05 summaries, malformed output, nonzero exit, missing numeric ceilings, and safety flags.
- [ ] The real dry-run invokes all six documented pilot commands under `-S` and receives exit 0 from each.
- [ ] Per-project and aggregate calls/tokens/confirmation fields are reported with source values and no guessed zeros.
- [ ] Aggregate remains `INCOMPLETE` while any account quota, spend/token cap, reviewer approval, or project prerequisite is `PENDING`.
- [ ] No credentials, provider SDK/network, Docker, services, or project files were accessed/modified.
- [ ] Evidence is sanitized, staged paths are limited to this phase, staged diff is reviewed, and local commit succeeds.
- [ ] Independent clean-context review remains separately recorded.
