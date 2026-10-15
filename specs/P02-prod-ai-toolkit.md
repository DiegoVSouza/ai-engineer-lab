# P02 — Toolkit de AI em produção (Bloco 2)

## Objetivo
Pacote reutilizável que transforma protótipos de agentes em sistemas confiáveis, avaliáveis, seguros e econômicos.

## Entregáveis
- `projects/p02-prod-toolkit/` com pacote `supportops_toolkit`.
- `tools/`: registro de tools com schemas Pydantic, validação de entrada/saída, retries com backoff+jitter, timeouts, classificação de erros (retriável vs fatal), tools de exemplo (`lookup_invoice`, `issue_refund`, `search_kb`).
- `evals/`: dataset versionado (`datasets/v1/*.jsonl`), runner, métricas (acurácia de decisão, acerto de tool call, groundedness simples por regra, taxa de escalonamento correto), comparação com baseline e **detecção de regressão** (falha o CI se cair além do limiar).
- `guardrails/`: detector de prompt injection (heurística + classificador via LLM em `fake`), allowlist de tools por papel, limites de execução (passos/tokens/tempo), redação de PII, **suíte adversarial** (≥30 casos: injeção direta, indireta via KB, exfiltração, tool abuse, reembolso fora do limite).
- `cost/`: streaming, cache semântico/exato, roteamento de modelo (barato→caro com critério), orçamento de tokens; `report.py` gera relatório antes/depois.
- Workflow de CI que roda evals em `fake`/`replay`.

## Public API
```python
@tool(schema_in=..., schema_out=..., timeout_s=..., retries=...)
class ExecutionLimits(BaseModel): max_steps:int; max_tokens:int; max_seconds:float
def guard(input_text: str, *, role: str) -> GuardVerdict   # allow|block|redact + reasons
def run_evals(runner: Callable, dataset: Path) -> EvalReport
class ModelRouter: def pick(self, task: TaskProfile) -> str
```

## Fases
- **001 tools** (schemas, retries, timeouts, testes de falha).
- **002 evals** (dataset v1, runner, regressão, integração CI).
- **003 guardrails** (Wave 1: injection ∥ limites; Wave 2: suíte adversarial).
- **004 cost-latency** (cache, roteamento, streaming, relatório).

## Verificação
- Mudar prompt/modelo no FakeLLM para pior resposta → `run_evals` falha com regressão (teste).
- Limites: agente que tenta 100 passos é interrompido no limite (teste).
- Suíte adversarial: taxa de bloqueio reportada; casos não bloqueados listados (não esconder).
- Relatório antes/depois com números de runs reais ou `PENDING`.

## README exigido
Como definir uma tool, rodar evals, ler o relatório de regressão, estender guardrails, interpretar o relatório de custo.

## Documentação de conhecimento
`docs/knowledge/P02-prod-ai.md`: structured outputs, desenho de evals (offline/online, LLM-as-judge e vieses), prompt injection (direta/indireta), custo/latência (caching, routing, streaming), trade-offs.

## Fora de escopo
Tracing/dashboards (P03), filas (P04), orquestração multi-agente (P01).
