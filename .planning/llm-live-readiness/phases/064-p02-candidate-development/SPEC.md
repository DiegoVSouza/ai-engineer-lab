# Phase 064: P02 candidate development guard

Prepare a separately authorized, bounded guard for `p02-dev-v2`, at most 24 free-plan attempts on development cases. Existing `p02-dev-v1` usage remains counted; the original development ceiling is 72 attempts in total. Preserve other project caps, all unresolved reservations, paid USD 0 and protected holdout/confirmation allocations. An uncertain or non-OK attempt closes the new campaign; do not replay it. A root authorization must be committed and unmodified before admission.

No provider call is part of guard implementation or testing. The owner previously requested continuing the free-only campaigns, with a USD 5 total-loss cap and no paid spend. A freeze and live dispatch require the independently implemented P02 campaign path, accounted preflight and reconciliation; none is implied by a green root unit test.
