# Phase 005 — User-authorized free envelope migration

Status: PLANNED. Provider access in this phase: zero. Human/independent/dataset/rubric review and promotion remain PENDING.

## Explicit authority

On 2026-10-27 the user explicitly approved the proposed additional P00 envelope, free only, subject to a validated migration phase. Authorization ID: `p00-free-envelope-plus10-v1`. This supersedes the prior no-cap-increase boundary only for the exact amendment below. It is not a review or promotion approval.

| Dimension | P00 before → after | Global before → after |
| --- | --- | --- |
| Calls | 186 → 196 | 4,074 → 4,084 |
| Input tokens | 380,928 → 401,408 | 14,290,944 → 14,311,424 |
| Output tokens | 47,616 → 50,176 | 1,786,368 → 1,788,928 |
| Economic estimate USD | 0.0428544 → 0.0451584 | 1.6077312 → 1.6100352 |

Delta: ten calls / 20,480 input / 2,560 output / USD 0.002304 economic estimate. Paid allowance stays USD 0. Model, prices, free rate ceilings, per-call maxima, per-trial counts, P01–P05 allocations and protected confirmations are unchanged. No corrections, judges or canary acquire funding implicitly.

## Accounting continuity

The old canonical policy SHA-256 is `ec7ccca5e2bece8cb677cab24dfd9822255bf9fbb791807f956837e62db5ce8d`. The inspected registry contains P00 UUID `384f921b0e8a4e7db7c5ae0491df3635`; sixteen attempts remain charged. Known usage is 5,236/1,650. The unknown pilot attempt retains 1,475/256 at the transport and 2,048/256 logically. Charged totals are 6,711/1,906 in the authoritative campaign provider ledger and 7,284/1,906 logically; they are not additive. Actual billing and current daily provider quota remain unknown.

P00 primary becomes 136 calls, leaving 120 after its existing sixteen attempts. This funds a completely fresh 36-trial development candidate and the unchanged 84-trial holdout. Confirmation remains 60 calls / 122,880 input / 15,360 output / USD 0.013824. The old candidate's twelve results and 24 pending trials remain historical and cannot transfer. All other project commitments remain funded: remaining primary calls are P00 120, P01 744, P02 246, P03 96, P04 558 and P05 1,464 (3,228 total); protected confirmations total 840. Thus 4,068 future calls exactly equal the amended global 4,084 minus sixteen consumed. No spare calls exist for extras.

## Migration requirements

1. Preserve the old policy snapshot and explicit structured authorization before code. Accept only the exact approved delta; reject any other field, project, paid/model/rate/per-call change.
2. Provide a credential-free, provider-free, read-only dry-run. Apply only from tracked committed migration/policy/authorization inputs after offline gates and staged review. Acquire P00's campaign execution lease first, then the shared account lease (matching P00 lock order), and revalidate under both so provider and logical journals cannot change during inspection.
   The P00 campaign source must be tracked, clean in its separate Git, and match the reviewed lock-bearing source blob pinned by the migration helper.
3. Change only the registry's policy SHA, preserving its complete project UUID mapping and other metadata. Never delete/reset a ledger, reference, counter, receipt, event, reservation or unknown use. Validate all registered ledger identities and complete event histories before and after; compare the separate logical ledger histories read-only as well.
4. Refuse active/uncertain reserved attempts, unknown registry states, unregistered usage, tampering, wrong source, path links/reparse points or concurrent lease contention. Completed historical attempts with missing usage remain fully reserved and do not block solely because usage is unknown.
5. Keep an append-only audit store for migration decisions/outcomes, distinct from authoritative provider consumption. A durable prepared event precedes the atomic registry replacement; an applied event follows verified continuity. Idempotent recovery recognizes only the approved old/new policy states, preserves newer appended events/UUIDs and never rolls back history or silently repeats a migration.
   A durable pending marker must block every ordinary shared-account reservation between registry replacement and the verified applied audit. Only the migration verifier may inspect that marked state; recovery removes the marker after audit reconciliation.
6. Preserve the old frozen campaigns and all quality/review gates. P00 owning phase 019 must separately bind its primary ceiling/candidate. No generation is part of this root migration phase. Validate the shared guard/transport regressions and both real P00/P01 locked product gates before apply.
