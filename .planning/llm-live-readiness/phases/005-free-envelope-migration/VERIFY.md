# Verify — free envelope migration

All execution checks start PENDING. Plan review is by the implementing agent, not independent approval.

- [ ] Explicit user approval matches only ten free P00 calls / 20,480 input / 2,560 output / USD 0.002304 economic estimate; paid USD 0 and all quality reviews stay pending.
- [ ] All six remaining original evaluations and confirmations remain funded, with unchanged per-call/trial/free-rate/model/pricing constraints and no extras inferred.
- [ ] Baseline/current policy identities and tracked committed migration inputs verified; any other delta or dirty/untracked source is rejected.
- [ ] Dry-run reads no credential/provider and writes no registry, audit or usage state.
- [ ] Shared lease protects revalidation; reserved in-flight/uncertain attempts block, while completed unknown usage retains its full original reserve.
- [ ] Registry UUIDs and all provider/logical event fields/receipts/reservations unchanged; only approved policy SHA transitions.
- [ ] Append-only prepared/applied audit and atomic replacement recover idempotently from interrupted transitions without lost history or new UUIDs.
- [ ] Unauthorized/corrupt/linked paths, missing ledgers, tampered audit, rollback, duplicate apply and concurrency fail closed in regressions.
- [ ] Root guard/transport/migration tests and real P00/P01 locked gates pass; sanitized commands/exits/output saved; staged review and pre-apply source commit recorded.
- [ ] Actual apply and post-reconciliation complete with no provider call, no historical campaign rewrite, no root registry reset and no consumption change.
- [ ] Human/independent/dataset/rubric review, billing proof, holdout/generalization and promotion remain PENDING/INCOMPLETE.
