# Migration evidence commands

## Planning

Command from lab root: `python -S artifacts/evidence/llm-live-readiness/envelope-migration/validate_plan.py`.

Exit code: 0. Complete output: `plan-validation.json`. It verifies the exact old policy snapshot/canonical SHA, explicit user-authorized delta, all unchanged project allocations and complete remaining funding. It changes no policy, registry, ledger or audit state and accesses no credential/provider. Plan review is by the implementing agent; independent review and all quality approvals remain PENDING.

Implementation/gate/dry-run/apply command evidence will be appended only after actual execution. The policy and registry remain unmigrated at this planning checkpoint.
