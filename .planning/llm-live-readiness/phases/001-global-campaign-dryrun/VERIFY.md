# Verify — Account-wide campaign dry-run

Save outputs and exits in `artifacts/evidence/llm-live-readiness/global-dry-run/`.

- [x] Five synthetic contract tests cover P00–P05 reservation shapes, malformed output, nonzero exit, missing call ceilings, and unsafe flags.
- [x] The real dry-run invokes all 18 documented pilot/development/holdout commands under `-S`; each exits 0.
- [x] Cases/calls/totals and primary/confirmation token maxima are reported for all six projects; additive token ceiling is derived without treating missing values as zero. Current `reservation_gaps=[]`.
- [x] Aggregate status remains `INCOMPLETE` with shared quota, cumulative caps, cross-project ledger, human review, and model preflight blockers.
- [x] The coordinator made no project writes; dry-runs did read project configuration. No credentials/provider/network/Docker/services were accessed or modified.
- [x] Refreshed evidence after P00/P05 CLI token-contract fixes: all 18 dry-runs exit 0; 5 aggregate contract tests pass; 390 cases, 3,150 primary, 840 confirmation, 4,074 additive calls; summed token maxima 11,182,080 / 1,397,760 primary, 2,826,240 / 353,280 confirmation, 14,008,320 / 1,751,040 additive.
- [x] Evidence is sanitized and staged paths are limited to this phase; staged diff is reviewed and locally committed.
- [ ] Independent clean-context review remains separately recorded.

Test invocation note: the first `unittest` module-name form failed because the test imports its sibling script as a top-level module. The direct script invocation passed all five tests; both command outcomes are retained in the evidence folder.
