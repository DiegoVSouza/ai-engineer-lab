# Handoff para o Luna
Leia [SPEC.md](SPEC.md), [PLAN.md](PLAN.md) e [VERIFY.md](VERIFY.md). A primeira implementação é a fase 016 existente do P00. O piloto anterior permanece reprovado; este pacote não declara live aprovado.

## Prompt para colar
```text
Implemente .planning/llm-live-readiness/luna-corrections/SPEC.md seguindo PLAN.md
e VERIFY.md, além dos requisitos originais de llm-live-readiness.
Leia AGENTS.md, harness/GSD-LITE-PLUS.md, a skill lab-commits, AUTHORIZATION.md
e SPEC/PLAN/VERIFY da fase 016 de projects/p00. Inspecione HEAD/status/serviços.

Comece só pela fase 016 do P00: semântica genérica de lookup, schema estrito,
payload completo/provenance, diagnósticos sanitizados e confirmação protegida.
Preserve dataset, graders, holdout e free-pilot-v1. Não rerode falha semântica,
não invente HTTP/code histórico. Teste fake/replay, execute gate locked,
salve evidências e comite candidato antes de chamar provedor.

Mostre dry-run offline antes de free-dev-c1: 12 casos, 36 tentativas máximas,
lotes de até 10, consumo acumulado, reservas e pendências. Depois execute
lotes reais autorizados com checkpoint seguro. Sem holdout/promoção na fase 016.

Só GROQ_API_KEY_1..4 do .env raiz; sem expor/hashear segredos. Quatro chaves
compartilham quota. Confirme catálogo/limites atuais; pago USD 0.
Não aumente teto nem apague ledgers/registry para contornar limites.
Correções extras, judges e canário exigem alocação explícita em fase própria.

Continue próximas fases um projeto por vez com SDD e caminhos concretos.
Integre CLI/API/workers reais ao guard; gateway Docker ainda não existe.
Prepare revisão privada para eu fazer depois; não marque revisão aprovada.
Holdout usado para corrigir exige confirmação nova antes de generalização.

Preserve stacks alheios. Sem deploy público, push, mensagens ou reembolsos.
Registre comandos/exits/consumo/erros e hashes reais. Commits locais atômicos
com escopos de componente. Informe PASS/FAIL/INCOMPLETE com evidências.
```
