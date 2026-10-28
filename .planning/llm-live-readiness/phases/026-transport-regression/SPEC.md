# Transport regression and boundary audit

Audit the custom catalog and completion transport after 03b711a. Bound metadata response size and close HTTP error responses even when reading their bodies fails. Preserve single-attempt completions and all historical campaign identities. Socket timeouts are not evidence of a total wall-clock deadline; report that limitation explicitly.

Budget: fake/offline only, zero provider calls and USD 0. No credential reads.

Audit follow-up: standalone catalog requests must reject redirects, and a 429 must stop traversal instead of trying another credential. Slot 0 remains discoverable for metadata but must not initialize a generation session while its Free eligibility is unverified; numbered-slot attestation must not be inherited by slot 0. No policy or authorization is changed by these controls.
