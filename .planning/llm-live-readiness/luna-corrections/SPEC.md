# Live readiness corrections
Status: planning handoff, 2026-10-26. Product readiness: INCOMPLETE.

## Authority
Read AGENTS.md, harness/GSD-LITE-PLUS.md, lab-commits, and parent SPEC/PLAN/VERIFY/AUTHORIZATION. Original thresholds remain authoritative. User authorizes free Groq only; paid allowance USD 0. Human review is deferred, not approved. No public deployment, push, messages, customer data or real refunds.

## Verified baseline
Shared account guard and single-attempt subprocess transport are implemented. Sanitized diagnostics fix: 8e5c82b2a8f2983a563b6bd1b920519090059783. P00 real adapter exists; privacy fix: 054701e9b5f486a39e96df4f8fc4cd6a0a9ecdcb. Phase 016 at cbcf881 is planning only. P01–P05 broad dispatch/account integration remains incomplete. P05 historical locked fake acceptance is not live quality evidence.

P00 artifacts/evals/live/free-pilot-v1 is immutable: four requests, three graded responses, zero passes, one operational error, two untouched planned trials. Known usage 844 input/248 output. Including unknown usage reservation: charged 2,319 input/504 output; economic estimate USD 0.000325125, billed cost PENDING. Historical error 017 lost HTTP status/code; never reconstruct it as fact. Three semantic failures chose request_info instead of expected lookup workflow; shipping also omitted a tool.

## Requirements
R1. Preserve 390 distinct cases, three trials each, sealed development/holdout splits and unchanged graders. No semantic retries or case-specific expected labels in prompts. Holdout-informed fixes need at least 20 fresh reviewed confirmation cases per affected project, three trials each.

R2. Implement existing P00 phase 016 first: generic lookup-versus-clarification semantics, strict existing JSON contract, pure shared payload builder, full serialized input bound, schema provenance, sanitized diagnostic propagation and protected confirmation. New free-dev-c1: 12 development cases × three trials, at most 36 attempts, chunks at most ten. No holdout in this phase.

R3. Root policy remains cumulative: 4,074 requests / 14,290,944 input / 1,786,368 output; economic cap USD 1.6077312 is not paid authorization. Published configured free upper limits RPM30/RPD1000/TPM8000/TPD200000 require current verification before calls; lower authenticated limits win. Headers do not prove billing tier or exact remaining daily tokens. Four numbered keys share one account. Read only root .env GROQ_API_KEY_1..4; never expose/hash secrets.

R4. P00 confirmation reserve: 60 calls / 122,880 input / 15,360 output / economic USD 0.013824. Primary pilot/development/holdout envelope: 126 calls / 258,048 input / 32,256 output / USD 0.0290304. Existing four attempts remain charged. After 36 development attempts, 86 nonconfirmation calls remain, of which 84 fund holdout. Extra corrections/judges/canary are not automatically funded. Allocate before dispatch. Any policy migration needs its own reviewed phase and preserves UUIDs, history and unknown reservations; never reset registry/ledgers to bypass policy SHA.

R5. Every normal live CLI/API/worker provider path must use the shared guard. P01–P03 need owning adapters; P04/P05 must exercise actual service/RAG/worker behavior. Docker-compatible bridge is unresolved: do not assume containers can run host subprocesses or reach host loopback. No gateway currently exists. Design/test local authenticated connectivity before adoption; no keys in images or public listener.

R6. Preserve receipts, source/prompt/schema/dataset/rubric provenance, outcome, latency, sanitized reason/status/code and cumulative usage. Raw answers belong only in private ACL-protected review stores, never public artifacts; no raw provider errors, headers or reasoning. Unknown usage stays fully charged. Source changes require a new candidate, not edited manifests.

R7. Prepare local review interface with escaped untrusted content, append-only annotations bound to case/trial/candidate/rubric, original critical-failure/stratified/double-review coverage, no provider calls on view. Actual user/independent review remains PENDING until performed.

R8. Reports retain operational/model denominators, all-three-pass case results, case-level uncertainty and domain/language/error slices. Quota/capacity/uncertainty means checkpoint and INCOMPLETE with validated resume command. All original quality/security/operation/consumption/human gates precede funded local canary and rollback. Fake/replay remains default.
