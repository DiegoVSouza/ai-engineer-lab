# Verify

- [x] New user authorization and finite free-only policy recorded; human approval remains pending.
- [x] Requests/tokens/estimated economic value are conserved across project/campaign switches and resume; billed cost stays unknown.
- [x] Unknown usage, malformed records, duplicates, concurrent caps, lease contention and process death fail safely. Registry references detect missing/replaced usage databases instead of resetting consumption.
- [x] Minute/day/cumulative limits and stricter provider feedback stop further reservations; quota stops all projects conservatively for a day.
- [x] Dry-run reads no credentials and performs no provider/Docker calls or production database initialization.
- [x] Authenticated catalog preflight confirms the model for all four deduplicated numbered credentials, exit 0; no credential identities/raw headers saved and zero generation calls.
- [x] Twenty standard-library offline tests pass; source format/lint/compilation checks pass. Commands/exits and sanitized evidence recorded; reviewed paths committed locally.
- [ ] Independent clean-context verification remains pending.

Initial test mistakes and incomplete metadata preflight were preserved. Catalog client now sends explicit application/Accept headers and emits only aggregate failure categories. No generation, product files, stacks or budgets were changed. The guard is not yet integrated into product dispatchers; later owning-project phases must use the single source of provider usage and require the common lease/guard contract.
