# Handoff para implementar com o Luna

Esta pasta contém a spec completa para sair dos testes pequenos e avaliar os seis projetos antes de promover os fluxos aprovados para live local no Docker. Não houve chamadas novas ao Groq nesta tarefa de documentação.

Leia [SPEC.md](SPEC.md), [PLAN.md](PLAN.md) e [VERIFY.md](VERIFY.md). A meta é 390 casos distintos e três execuções por caso, com análise por domínio, idioma e tipo de erro. Isso exige execução em lotes e pode levar várias janelas da conta gratuita. O total é uma meta de avaliação, não autorização para aumentar orçamento.

O plano inclui conjuntos de desenvolvimento e holdout, revisão dos graders, falhas operacionais, segurança, RAG, recuperação de workers, traces, controle cumulativo de consumo, canário e rollback. Corrigir usando o holdout exige uma confirmação nova antes de afirmar que a qualidade generaliza. Se faltar quota, orçamento ou revisão humana, o resultado fica INCOMPLETE.

Live significa usar Groq de verdade no ambiente local. Deploy público, dados de clientes e reembolsos reais precisam de outra fase. Fake continua padrão nos testes e no CI.

## Prompt para colar na nova sessão

```text
Implemente a avaliação ampla e a adoção de live local descritas em
.planning/llm-live-readiness/SPEC.md.

Primeiro leia AGENTS.md, harness/GSD-LITE-PLUS.md, a skill lab-commits e os
arquivos PLAN.md e VERIFY.md desta pasta. Inspecione o estado atual dos seis
repositórios; não presuma que os commits e serviços continuam iguais.

Comece pela preparação: inventário, política de orçamento, datasets,
rubricas, splits e dry-run. Antes de código de produto, crie uma fase SDD
no projeto dono, com SPEC/PLAN/VERIFY, allowed_write_paths concretos e
revisão do plano. Trabalhe uma fase de um projeto por vez.

Use somente GROQ_API_KEY_1..4 do .env da raiz, sem imprimir, registrar,
hashear ou expor segredos. Prefira openai/gpt-oss-20b e confirme o catálogo
antes das chamadas. Não execute a campanha ampla com tetos PENDING,
não aumente orçamento nem trate quatro chaves como quatro cotas.

Preserve fake/replay offline. Faça regressões significativas, avaliações
reais em lotes, análise dos erros e correções de causa raiz. Não rerode
um erro semântico só para conseguir aprovação, não enfraqueça os graders
e não mude o holdout para melhorar a pontuação.

Salve comandos, exit codes, resultados sanitizados e consumo acumulado
nos artifacts do projeto. Se atingir quota/orçamento, salve checkpoint e
informe o comando de retomada; não faça fallback silencioso.

Promova apenas projetos com todos os gates aplicáveis aprovados. Suba
serviços locais isolados, execute canário e rollback sem tocar nos stacks
alheios. Não faça deploy público, push, envio de mensagens ou reembolso.

Atualize docs e conhecimento, revise o staged diff e faça commits locais
atômicos com escopos de componente, como feat(rag) ou fix(planner),
sem usar (p05) ou outros IDs de projeto como escopo. Informe o que passou,
o que falhou e o que ainda está INCOMPLETE com evidências e hashes reais.
```

## Como acompanhar

Peça o dry-run antes do primeiro lote: ele deve mostrar quantidade de casos, chamadas máximas, consumo reservado, limites aprovados e campos ainda pendentes, sem acessar o provedor. Depois acompanhe o report.md de cada campanha e o estado de promoção de cada projeto.

Um resultado bom inclui erros preservados e corrigidos, não apenas uma tabela verde. A adoção local de live só fica concluída quando os gates de qualidade, segurança, operação, consumo e rollback tiverem evidência.
