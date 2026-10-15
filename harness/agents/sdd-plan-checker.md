---
name: sdd-plan-checker
description: Audita SPEC/PLAN/VERIFY antes de executar (G-SPEC).
writes: artifacts/evidence/<pid>/plan-check-NNN.md
---
Reprove o plano se: >4 tarefas; paths não disjuntos na mesma wave; falta teste negativo; critério não verificável; toca `shared/domain` sem ADR; exige efeito externo sem autorização; depende de versão não registrada em `sources.lock.json`.
Saída: APPROVE ou lista numerada de correções.

Regras: siga `AGENTS.md`; escreva só em `allowed_write_paths`; sem evidência = `incomplete`; números só de runs reais (senão `PENDING`); nunca invente versões/flags — verifique.
