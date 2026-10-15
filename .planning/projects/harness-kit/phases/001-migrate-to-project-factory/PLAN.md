# Plan — Phase 001

```yaml
project: harness-kit
requirement_ids: [REQ-HK-001, REQ-HK-002, REQ-HK-003, REQ-HK-004, REQ-HK-005]
allowed_write_paths:
  - AGENTS.md
  - README.md
  - harness/GSD-LITE-PLUS.md
  - harness-kit/**
  - scripts/harness/new-project.py
  - .planning/PROJECT-SPEC.md
  - .planning/ROADMAP.md
  - .planning/STATE.md
  - .planning/decisions.md
  - .planning/projects/harness-kit/**
forbidden_changes: [projects/**, specs/P00-*.md, specs/P01-*.md, specs/P02-*.md, specs/P03-*.md, specs/P04-*.md, specs/P05-*.md]
llm_mode: fake
validation_command: python scripts/harness/new-project.py --help
stop_condition: Acceptance criteria have recorded evidence.
```

## Wave 1

1. Create the kit's profile schema, defaults, resolver and safe bootstrap command.
2. Rewrite lab-level instructions and roadmap for independently initialized projects while retaining SDD phases and evidence.

## Wave 2

1. Exercise a positive bootstrap, a trifecta rejection, and an overwrite rejection in temporary directories.
2. Save command output under `artifacts/evidence/harness-kit/` and update planning state.
