# Verify — authenticated rate-limit preflight

Implementation has not started. No credentials have been read and no provider request has been made for this phase.

- [ ] Exact official header semantics and source/date are recorded.
- [ ] Allowlisted authenticated response limits are sanitized and combined conservatively across shared keys.
- [ ] Lower authenticated RPD/TPM and remaining-capacity/reset values constrain the shared guard before any reservation.
- [ ] Missing/malformed values remain explicit and never raise static ceilings; billing tier and daily token remainder remain unverified.
- [ ] Fake tests cover preflight/model denial, lower limits, resets, shared keys, absent headers and secret-free reports.
- [ ] Root tests and P00 locked full gate pass; no ledger, registry, policy or campaign history was changed.
- [ ] Root guard commit exists and the dependent P00 candidate is re-fingerprinted, validated and recommitted before authenticated preflight.
- [ ] Human, independent, dataset/rubric and promotion reviews remain PENDING.
