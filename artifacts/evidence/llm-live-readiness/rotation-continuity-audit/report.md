# Campaign continuity audit

## Executed evidence

The locked P00 environment ran the root injected-transport suite: 18 tests PASS, exit 0; see transport-command.json and transport-tests.txt. The offline C2 dry-run exited 0 without credentials or provider access; see p00-dry-run-command.json and p00-dry-run.json. These tests do not establish live quality or human approval.

The dry-run reproduces fingerprint 56bef263770d396fe69d915bc8aea1bdc9a9109e83584d08e28377adbb01af6b and 29 accounted calls. Provider usage is 11470/3255 input/output; logical usage is 12043/3255. Do not add these views. Historical unknown transport reservation is 1475/256; logical reservation is 2048/256. Primary remaining is 107 calls; confirmation 60 protected. Billing UNKNOWN. Dry-run candidate_commit reports current evidence HEAD bb729e3fcca4574d1f1cf140fb558f1da5bacf12, while historical evaluated candidate remains 7099cc5d0f4d576d14f28f7dab4648b074b59740; identical source fingerprint does not rewrite historical provenance.

## Findings

- PASS: the actual campaign ProviderSession performs one completion HTTP request and returns errors without retry. The generic GroqKeyRotationTransport is a separate adapter and its retries do not prove campaign retry behavior.
- PASS: reservation commits with synchronous=FULL before HTTP. Existing transport tests cover restart rotation, no retry after error, conservative unknown usage and smaller authenticated limits.
- INCOMPLETE: credential selection is computed after reservation from a fresh aggregate snapshot. Reservation rows contain no credential slot or organization identity. Persistent count alone cannot prove immutable attribution to a selected credential. Historical attribution must remain unknown.
- INCOMPLETE: aggregate guards are conservative; independently verified per-organization topology and remaining daily balances are absent. User attests keys 1..4 are distinct Free accounts. This does not multiply funding or authenticate billing.
- INCOMPLETE: current dry-run reports dataset_review and rubric_review blockers and generation_authorized=false. The previously documented provisional development exception must be reconciled with the resume execution path before generation. Do not silently remove gates.

## Finite next tasks and dependencies

1. Finish account-guard and resume-path audit, including window expiry and receipt reconciliation. No provider budget consumed. Live continuity remains INCOMPLETE until this evidence exists.
2. If selection persistence needs correction, create a separate root transport phase and owning P00 provenance phase. Changing fingerprint invalidates C2 resume; 23 remaining C2 plus 84 holdout use all 107 primary calls, with zero spare for a replacement 36-trial candidate. Demonstrate any deficit before generation. Preserve UUIDs/events/receipts and historical unknown attribution.
3. P01: inspect latest local phases and implement durable bounded tool dispatch and duplicate-effect controls. Offline work requires no provider calls; primary allocation 744, confirmation 240 protected. Gates INCOMPLETE until owning service evidence exists.
4. P02: inspect and implement executable retrieval, attribution/refusal, context isolation and injection controls. Primary 246, confirmation 60 protected; service/live gates INCOMPLETE.
5. P03: inspect existing runtime/export/service evidence and resolve remaining operational gates. Primary 96, confirmation 60 protected; live gates INCOMPLETE.
6. P04: inspect API/RAG/worker recovery and trace evidence; implement missing paths in owning phases. Primary 558, confirmation 180 protected; live gates INCOMPLETE.
7. P05: inspect real API/RAG/worker paths, identity/security/recovery and finish owning gates. Primary 1464, confirmation 240 protected; live gates INCOMPLETE.
8. Validate private review security, append-only corrections, provenance and review coverage against current records. Existing 29-record navigation evidence is historical. Human/independent/dataset/rubric reviews remain PENDING until actually performed.

All project work requires existing-ID inspection, project-local plans, locked checks, recorded command/exit/output and local commits. No project source, ledger, secret, service or campaign was changed by this audit.
