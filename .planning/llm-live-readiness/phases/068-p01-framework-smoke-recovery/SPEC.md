# P01 Framework Smoke Recovery

## Goal

Correct the source path prefix in the frozen candidate manifest after campaign v1 was rejected by the local guard before transport dispatch.

## Preserved authorization

Campaign v1 recorded zero provider usage. Campaign v2 may use only the original five-runner development scope. The root guard counts all P01 `p01-framework-smoke-*` provider reservations together and enforces a cumulative ceiling of 20, so the recovery cannot reset the budget.

## Acceptance

The new candidate manifest matches the root guard path convention, fake tests pass, and live execution uses only `SubprocessGuard` and `AccountedCoreClient`. No holdout, confirmation, paid spend, or replay of campaign v1.
