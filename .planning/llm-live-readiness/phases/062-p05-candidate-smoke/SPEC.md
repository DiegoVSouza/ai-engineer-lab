# Spec: P05 candidate smoke `p05-diag-v2`

Why: `p05-diag-v1` showed `worker_contract` at the second worker with no provider error, so the cause is the model output, not the transport. Candidate v2 asks for a native strict schema per worker (p05 `72c5c05`). This smoke runs the four development cases that stopped on `worker_contract` once each (at most 16 calls, free Groq keys, USD 0.00) to see that the provider accepts the schema and the failures drop. Not a quality number; the holdout stays closed.
