---
name: sdd-parallel
description: Roda vários projetos em paralelo via git worktrees.
---

Argumento: `<pid> <pid> ...`. 1) `bash scripts/harness/new-worktrees.sh <pids>`. 2) Em cada worktree, uma sessão Codex executa `sdd-plan` → `sdd-execute` → `sdd-verify`. 3) Ao fim, `sdd-integrator` integra em ordem de dependência. Só paralelize projetos da mesma onda do MASTER-PLAN.

Regras: `AGENTS.md` vale sempre; evidência antes de dizer 'pronto'.
