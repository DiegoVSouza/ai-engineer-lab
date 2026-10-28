# Phase 016 — Reconcile P04 span privacy

## Goal

Record P04 phase 021's API/worker exception status-description fix and its scoped offline evidence in the lab coordinator.

## Acceptance criteria

1. Link P04 candidate commit `379cb09c646cd77bfd8cb51f91f6b5d6939adfea` and evidence cleanup commit `073449ef57ad543c3d68d99edaf42ee5707b1419`.
2. Record true baseline red evidence against the original clean source, both API/worker paths fixed, focused/fast checks passing, and full gate INCOMPLETE only on omitted services/tooling.
3. Preserve trace export deployment, RAG, model quality, billing, human/independent approval and promotion as pending.
4. Run the root harness check; stage only this phase and root coordinator status; commit locally.

## Constraints

Documentation-only root coordinator update. Do not touch project Gits, ledgers, live budgets, external systems, secrets or unrelated root paths.
