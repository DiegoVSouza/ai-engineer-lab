# P01 — Multi-agentes e orquestração

## Resumo de 1 página
Implementei a mesma triagem de tickets em 5 frameworks para comparar controle de fluxo, estado, maturidade e observabilidade com o mesmo dataset. A base é um supervisor-worker em Python puro com critério de finalização explícito; LangGraph cobre paralelismo, retries, checkpoints e HITL.

## Padrões (saber desenhar e explicar)
| Padrão | Ideia | Use quando | Risco |
|---|---|---|---|
| Supervisor-worker | um agente roteia para especialistas | tarefas decomponíveis, controle central | supervisor vira gargalo/ponto único |
| Handoff | agente passa o controle a outro | conversas com especialização sequencial | perda de contexto |
| Planner-executor | planeja, depois executa | tarefas longas e previsíveis | plano desatualizado |
| Parallel agents | fan-out/fan-in | subtarefas independentes | conflito de estado, custo |
| Human-in-the-loop | pausa para aprovação | ações irreversíveis/sensíveis | latência, UX |

## Frameworks (resumo mental; **verifique o estado atual antes de afirmar maturidade**)
- **LangGraph**: grafo explícito de estado; forte em checkpoints, paralelismo, HITL; mais código.
- **CrewAI**: abstração de papéis/tarefas; rápido de prototipar; menos controle fino de fluxo.
- **AutoGen / Semantic Kernel**: conversação multi-agente e plugins; ambos em transição para o Microsoft Agent Framework — confirmar na execução (ver `sources.lock.json`).
- **LlamaIndex**: forte em RAG/dados; agentes e workflows orientados a eventos.

## Critério de finalização (pergunta clássica)
O supervisor para quando: (1) resposta aprovada; (2) escalonamento; (3) limite de passos; (4) orçamento esgotado. Sem isso, há loop infinito e custo ilimitado.

## Perguntas de entrevista
1. *When would you NOT use a multi-agent system?* — When a single prompt + tools solves it; agents add cost, latency, nondeterminism.
2. *How do you prevent agent loops?* — Step/token/time limits, repeated-call detection, explicit termination states.
3. *How do you manage shared state?* — Typed state object, reducers, checkpointing; avoid free-form chat history as state.
4. *Why compare frameworks on the same dataset?* — Removes confounders; shows trade-offs with data.
5. *How do you add human approval?* — Interrupt before the sensitive tool, persist state, resume on approval.
(Complete com ≥5 após o run.)

## Números para citar
`PENDING`: acurácia, passos médios, custo e latência por framework.
