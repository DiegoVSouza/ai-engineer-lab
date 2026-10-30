# Verification

The migration regression suite passed 9 tests, exit0. It proves a changed P00 source blob is denied without a complete audit, denied after only `prepared`, and accepted only after the validated `prepared` plus `applied` audit sequence. Existing tests were reconciled so the already-consumed P01 workflow is correctly closed while only P04 can model an open revalidation reservation.

After commits `414ab7f` (root guard) and P00 `2335de8` (allocation source), the read-only migration returned `ALREADY_APPLIED`, exit0, on the changed committed P00 source. It preserved all registry identities and reported provider accounting90 / 31991 / 8380 with one historical unknown-usage attempt. Evidence: `artifacts/evidence/llm-live-readiness/post-apply-source-binding-044/migration-regression.json` and `applied-migration-readonly.json`. No provider, credentials, ledger mutation, gate or live operation occurred. This phase cannot replace any consumed P00/P04 full gate.
