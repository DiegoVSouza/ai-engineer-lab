# Verify — Account-wide campaign dry-run

Save outputs and exits in `artifacts/evidence/llm-live-readiness/global-dry-run/`.

- [x] Five synthetic contract tests cover P00–P05 reservation shapes, malformed output, nonzero exit, missing call ceilings, and unsafe flags.
- [x] The real dry-run invokes all 18 documented pilot/development/holdout commands under `-S`; each exits 0.
- [x] Cases/calls/totals are reported for all six projects. Token fields absent from P00/P05 dry-run contracts are explicitly `PENDING` with named gaps, never treated as zero.
- [x] Aggregate status remains `INCOMPLETE` with shared quota, cumulative caps, cross-project ledger, human review, and model preflight blockers.
- [x] No credentials, provider SDK/network, Docker, services, or project files were accessed/modified.
- [x] Evidence is sanitized and staged paths are limited to this phase; staged diff is reviewed and locally committed.
- [ ] Independent clean-context review remains separately recorded.
