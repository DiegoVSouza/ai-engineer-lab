# Spec: P05 diagnostic campaign `p05-diag-v1`

Why: `p05-dev-v1` scored 8 of 16 and four trials stopped on `worker_contract`, but the provider-side cause of a refused call is not recorded. The executor now keeps a content-free `provider_diagnostic` (p05 commit `124003c`). This campaign runs the two development cases `citation_correctness-02` and `prompt_injection-01` once to read that cause.

Scope: 2 trials, at most 8 provider calls, free Groq keys through the root account, USD 0.00 authorized, owner cap USD 5.00. No quality claim. The holdout is not opened.
