---
name: sdd-verify
description: Verificação goal-backward da fase.
---

Argumento: `<pid> [fase]`. Acione `sdd-verifier` em contexto limpo. Reporte X/Y e evidência. FAIL local corrigível → execute correção pequena dentro dos paths/spec autorizados e valide no mesmo turno, até `max_tries: 3` tentativas totais (inicial + duas correções). Persista contador, diagnóstico e saída sanitizada. Siga o ciclo limitado de `harness/GSD-LITE-PLUS.md`; aprovação, orçamento, live e trabalho incerto são condições de parada, nunca de replay automático. Ao parar uma tarefa, continue trabalho independente permitido.

Regras: `AGENTS.md` vale sempre; evidência antes de dizer 'pronto'.
