# Transport regression and boundary audit

Audit the custom catalog and completion transport after 03b711a. Bound metadata response size and close HTTP error responses even when reading their bodies fails. Preserve single-attempt completions and all historical campaign identities. Socket timeouts are not evidence of a total wall-clock deadline; report that limitation explicitly.

Budget: fake/offline only, zero provider calls and USD 0. No credential reads.
