# GSD-LITE-PLUS — SDD for independent AI projects

This is the Builder-layer workflow used by every project initialized from `harness-kit/`. It preserves the useful controls from the former monorepo harness without coupling unrelated products.

## 1. Principles

1. Spec before product code: `SPEC.md`, `PLAN.md`, and `VERIFY.md` exist before implementation.
2. State lives in files, never only in the conversation.
3. A plan has 2–4 tasks; split it when it grows larger.
4. `PLAN.md` is an imperative executor prompt with explicit path ownership.
5. `VERIFY.md` exists before execution and is run by a clean-context verifier.
6. Tests precede implementation where behavior can be tested.
7. Evidence is a command, exit code, and stored output; otherwise the result is incomplete.
8. Control logic is deterministic under `LLM_MODE=fake`.
9. External effects need user authorization.

## 2. Per-project layout

```text
<project>/
  harness.yaml                 # harness profile and module toggles
  .harness/                    # kit version and resolved module lock
  docs/harness/                # intake, progress, failures, agent card
  .planning/phases/NNN-name/   # SPEC.md, PLAN.md, VERIFY.md
  shared/                      # policies, skills, tool specifications, MCP allowlist
  agent/                       # product layer when selected
  evals/                       # product evaluations when selected
  artifacts/                   # commands, logs, metrics, and gate evidence
```

The root lab owns the kit. A product owns everything inside its own directory. Product plans must never write to `harness-kit/` unless the task is explicitly a kit evolution.

## 3. Phase loop

`INTAKE → SPEC → VERIFY draft → PLAN → PLAN CHECK → TESTS → EXECUTE → VERIFY → GATE → DOCS → KNOWLEDGE`

The project orchestrator is the only writer of its progress state. Plans declare `allowed_write_paths`, `forbidden_changes`, `llm_mode`, a validation command, and a stop condition.

## 4. Gates

| Gate | Minimum evidence |
|---|---|
| G-INTAKE | Valid `harness.yaml`, decisions recorded, profile modules resolved |
| G-SPEC | Complete SPEC/PLAN/VERIFY and disjoint paths |
| G-CODE | Project validation passes in fake mode and output is saved |
| G-EVAL | Relevant regression/capability evals pass; a missing eval is `incomplete` |
| G-SEC | No unresolved high-severity finding; complete lethal trifecta has a documented control |
| G-DOCS | README follows the standard; metrics are real runs or `PENDING` |
| G-KIT | A kit change is validated against two real projects before release |

## 5. Product learning loop

For an agent product, production or replay traces feed `docs/harness/failures.md`, then the failure taxonomy, an eval, and a code/prompt/tool change. Prompts are versioned and tools have a specification plus contract tests. Do not add multi-agent coordination, long-term memory, or governance modules until the profile and observed need justify them.

## 6. Legacy curriculum

`specs/P00–P05` document the original coupled SupportOps curriculum. They remain useful project briefs and learning material, but independent projects created after this migration do not share `shared/domain` or a mandatory integration wave.
