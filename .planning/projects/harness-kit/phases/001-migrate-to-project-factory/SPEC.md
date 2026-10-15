# Phase 001 — Migrate the lab to a project factory

## Objective

Turn the lab from a single, coupled SupportOps curriculum into a versioned harness kit that initializes independent AI projects from an explicit profile.

## Requirements

- [ ] REQ-HK-001: The repository provides a versioned `harness-kit/` with a bootstrap command that resolves modules from `harness.yaml`.
- [ ] REQ-HK-002: Bootstrap refuses a complete lethal trifecta unless a security plan exists.
- [ ] REQ-HK-003: Every initialized project records the kit version and resolved modules without overwriting existing files.
- [ ] REQ-HK-004: The lab's planning model supports independent projects and retains the SDD evidence gates for each project.
- [ ] REQ-HK-005: The previous SupportOps P00–P05 specifications remain available as archived curriculum material.

## Out of scope

- Migrating or implementing any portfolio product.
- Installing dependencies, calling external services, or creating a remote repository.

## Acceptance criteria

- Given a valid agent-app profile, when the bootstrap runs, then the project receives the selected product and builder structure plus a module lock.
- Given a profile with all lethal-trifecta values set and no security plan, when the bootstrap runs, then it exits non-zero without initializing the project.
- Given an existing generated file, when the bootstrap runs again, then it exits non-zero and preserves that file.
