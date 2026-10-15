---
name: sdd-execute
description: Executa o PLAN por waves com testes primeiro.
---

Argumento: `<pid> [fase]`. Acione `sdd-orchestrator`. Por wave: test-engineer → executores (paths disjuntos em paralelo) → commits atômicos → `make -C projects/<pid> verify` em `LLM_MODE=fake`.

Regras: `AGENTS.md` vale sempre; evidência antes de dizer 'pronto'.
