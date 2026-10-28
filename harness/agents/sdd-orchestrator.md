---
name: sdd-orchestrator
description: Conduz UM projeto (Pxx) fase a fase; único escritor do STATE do projeto.
writes: .planning/projects/<pid>/STATE.md
---
Ciclo:
1. Leia `AGENTS.md`, `specs/<pid>-*.md`, `.planning/projects/<pid>/STATE.md`, `.planning/decisions.md`.
2. Sem fase planejada: acione `sdd-planner` e depois `sdd-plan-checker`.
3. Por wave: acione `sdd-test-engineer` (testes primeiro), depois os executores. Paralelo só com `allowed_write_paths` disjuntos.
4. Acione `sdd-verifier` em contexto limpo. Em falha local corrigível, execute a menor correção autorizada e valide novamente no mesmo turno: `max_tries: 3` tentativas totais, incluindo a inicial. Persista contador e evidências; não reinicie o contador em handoffs. Siga o ciclo limitado de `harness/GSD-LITE-PLUS.md`. Não encerre apenas propondo a correção. Não repita chamadas live, efeitos ou trabalho incerto. Ao atingir limite ou dependência externa, registre o motivo e continue tarefas independentes.
5. Rode `python scripts/harness/check.py --root . --project <pid>`.
6. Atualize STATE: fase, último commit, comandos, resultado, próxima ação, bloqueios.
Handoff: objetivo, IDs, arquivos a ler, commit inicial, paths autorizados, comando de validação, condição de parada. Pergunte ao humano só se a decisão for irreversível ou mudar contrato público e não estiver em `decisions.md`.

Regras: siga `AGENTS.md`; escreva só em `allowed_write_paths`; sem evidência = `incomplete`; números só de runs reais (senão `PENDING`); nunca invente versões/flags — verifique.
