# Detailed implementation plan
## Ownership
Documentation allowed paths: this folder, parent STATUS.md, artifacts/evidence/llm-live-readiness-spec/luna-corrections/** and P00 phase 016 SPEC/PLAN/VERIFY. This delivery does not change runtime. Future phases need concrete owning-repository allowed_write_paths and plan review before code. Inspect actual HEAD/status/AGENTS/harness.yaml/decisions/services; preserve unrelated files/stacks.

## A. P00 existing phase 016
1. Read expanded phase 016 and immutable pilot evidence. Reuse root guard/transport; diagnostic fix is already implemented.
2. Clarify generic next-workflow semantics. Concrete issues may select read-only lookup without retrieved records; request_info means issue/subject is unclear. No expected labels or facts leak.
3. Add strict existing output schema, both objects additionalProperties false, required fields, global enums and nullable readonly tool. Share one pure payload builder between execution and bound checks. Include schema hash in frozen identity. Full messages/schema/framing must fit existing 2048 input/256 output limits; shorten prompt if necessary, do not increase limits.
4. Propagate root allowlisted error code/numeric HTTP status and request_schema/tool_selection without raw text. Protect confirmation in every new/resumed campaign and cumulative stage check.
5. Run focused regressions plus locked full gate, save commands/exits, review staged diff, commit candidate before calls. Prove private ACL and UTF-8 regressions remain passing.
6. Show no-provider dry-run: 12 cases/36 attempts, <=10 new trials/chunk, complete reservations, consumed usage, protected confirmation and pending reviews. Verify CLI help before using flags.
7. Execute only new free-dev-c1 development chunks. Existing interface: uv run --locked python scripts/run_live_campaign.py --stage development --campaign-id free-dev-c1 --execute-free --max-trials 10, with LLM_MODE=live. Resume interface: --resume free-dev-c1 --execute-free --max-trials 10. Validate interfaces first. Stop at 36 total attempts, on resource/provider uncertainty, or candidate mismatch. Never resume old pilot after changes. No holdout/promotion here.

## B. Shared allocation and container transport
Create root-owned SDD phases. First allocate remaining calls/tokens/economic capacity by project/stage including actual usage, protected confirmation, corrections, judges and canary. Unallocated work is INCOMPLETE. Migration must preserve registry identities and append-only events; no silent cap expansion or resets.
If Docker requires bridge, specify local request/auth/receipt/lifecycle contract, fixed upstream/model, no retries, bounded timeout and shared guard. Prove fresh isolated host/container connectivity and denied callers/log redaction/shutdown. No existing gateway flags may be assumed. Reusable changes require applicable multi-project validation; do not edit harness-kit incidentally.

## C. Five owning integrations, one at a time
For each P01–P05: inspect current source and existing phases; create SPEC/PLAN/VERIFY with exact adapter/prompt/tool/config/test/evidence paths. Freeze candidate/dataset/rubric, provider calls per trial and every live entry point. Implement account binding, bounded execution, resume and reporting. Test fake/replay without keys and operational faults before bounded real pilot/development.
P01: actual planning/tool limits and duplicate-effect prevention. P02: retrieval, attribution, refusal and injection isolation. P03: task-specific runtime and telemetry/export failures. P04/P05: actual API/RAG/workers, traces and kill-after-effect recovery, not detached prompt classifiers. Recheck original gates; these focus areas do not replace them.
Prove legacy SDK paths cannot bypass accounting. Record owned Docker identities before/after; touch only owned resources. Service skips remain INCOMPLETE.

## D. Review and frozen evaluations
Choose review interface owner, then create its SDD phase. Read private stores, safely render untrusted content, append immutable provenance-bound annotations, no answers in logs/exports and no provider call on view. Prepare original review samples and critical failures; user performs actual review later.
Regenerate aggregate offline dry-run after configuration changes. Reconcile every attempt with project receipts and shared usage. Run sealed holdout only under applicable original gates. Holdout-guided changes need new confirmation phase/cases/capacity. Do not invent independent approval.

## E. Promotion
After all applicable gates including human/independent review: owning local deployment phase, exact evaluated identity, funded original canary cohorts (5/25/50 where applicable), thresholds, isolated services and demonstrated rollback. No public deployment.

## Every phase
Save commands/exit codes/sanitized output and checkpoints in project artifacts. Update progress/failures/knowledge, stage explicit paths, review staged diff and commit locally with English component scope, never project IDs. Use locked environments. Report PASS/FAIL/INCOMPLETE with real hashes; never convert missing quota/review into PASS.
