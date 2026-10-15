# P01 — Multi-agentes e orquestração (Bloco 1)

## Objetivo
Implementar o **mesmo caso de uso** (triagem de ticket do SupportOps: classificar → buscar KB → decidir ação → responder/escalar) em 5 frameworks e comparar com evidência.

## Entregáveis
- `projects/p01-multi-agent/` com pacote `supportops_agents`.
- `core/`: supervisor-worker em Python puro (agentes: `classifier`, `kb_researcher`, `billing_agent`, `responder`; estado compartilhado; **critério de finalização explícito**: máx. passos, resposta aprovada, ou escalonamento).
- `frameworks/langgraph/`: paralelismo (kb ∥ billing), retries por nó, checkpointer (SQLite), interrupt/HITL para reembolso acima do limite.
- `frameworks/crewai/`, `frameworks/autogen/`, `frameworks/semantic_kernel/`, `frameworks/llamaindex/`: mesmo contrato `TriageRunner`.
- `comparison/`: harness que roda os 5 no golden set e gera `results.json` + `COMPARISON.md` (facilidade, controle de fluxo, estado, maturidade, observabilidade, nº de linhas, acurácia, passos, tokens, custo, latência).
- Nota de maturidade: **verificar na execução** o estado de AutoGen e Semantic Kernel (ambos migrando para o Microsoft Agent Framework); registrar em `sources.lock.json` e decidir via ADR se implementa AutoGen/SK clássicos ou Agent Framework.

## Public API
```python
class TriageRunner(Protocol):
    name: str
    def run(self, ticket: Ticket, *, llm: LLMClient, max_steps: int = 12) -> TriageResult: ...
# TriageResult: decision: TriageDecision, trace: list[StepRecord], usage, stop_reason
def get_runner(name: Literal["core","langgraph","crewai","autogen","semantic_kernel","llamaindex"]) -> TriageRunner
```

## Fases
- **001 core supervisor-worker** (Wave 1: estado+agentes ∥ testes de finalização; Wave 2: loop).
- **002 langgraph** (paralelismo, retries, checkpoint+retomada, HITL).
- **003 crewai**.
- **004 autogen + semantic_kernel + llamaindex** (3 executores em paralelo, 1 por framework, paths disjuntos).
- **005 comparison** (harness, tabela, análise de "quando usar cada um").

## Verificação
- Os 6 runners passam os mesmos testes de contrato em `fake`.
- Supervisor **para** em: limite de passos, aprovação, escalonamento (3 testes) e nunca entra em loop infinito (teste com LLM fake que sempre pede mais um passo).
- LangGraph: retomada após kill no meio (teste); HITL pausa e retoma.
- `COMPARISON.md` com números de `artifacts/runs/` ou `PENDING`; "quando escolher cada framework" com ≥1 cenário por framework.

## README exigido
Problema, diagrama Mermaid de cada arquitetura, tabela comparativa, como rodar cada framework, resultados, limitações, decisões (ADRs).

## Documentação de conhecimento
`docs/knowledge/P01-multi-agent.md`: padrões (supervisor-worker, handoff, planner-executor, parallel, HITL), estado, quando usar cada framework, falhas típicas (loops, estado inconsistente).

## Fora de escopo
Observabilidade avançada (P03), fila (P04), API HTTP e auth (P05), avaliação formal (P02).
