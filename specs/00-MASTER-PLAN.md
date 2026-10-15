# MASTER PLAN — AI Engineer Lab

## Ondas e paralelismo
| Onda | Unidades | Paralelo? | Gate de saída |
|---|---|---|---|
| 0 | H00 ensaio do harness | não | G-HAR |
| 1 | [P00 Fundação](P00-foundation.md) | não (base de tudo) | G-CODE + G-CONTRACT (congela `shared/domain`) |
| 2 | [P01](P01-multi-agent-orchestration.md), [P02](P02-prod-ai-toolkit.md), [P03](P03-agent-observability.md), [P04](P04-async-ai-platform.md) | **sim, 4 worktrees** | G-CODE, G-SEC, G-DOCS por projeto |
| 3 | INT: integrador publica pacotes `supportops-*` | não | G-CONTRACT |
| 4 | [P05 SupportOps Platform](P05-supportops-platform.md) | parcial (infra ∥ API ∥ MCP) | todos os gates |
| ∥ | Knowledge (`docs/knowledge`) e LinkedIn (`sdd-publish`) | contínuo | G-KNOW, G-PUBLISH |

## Grafo de dependências
P00 → {P01, P02, P03, P04} → INT → P05.
P05 consome: `p01` (supervisor-worker LangGraph), `p02` (tools/evals/guardrails/cost), `p03` (OTel), `p04` (fila/worker/idempotência).

## Contratos que permitem o paralelismo
- `shared/domain`: modelos Pydantic congelados (ver P00).
- `shared/llm`: `LLMClient` com modos fake/replay/live.
- `shared/testkit`: fixtures, dataset sintético, `FakeLLM` programável.
- Cada projeto expõe **Public API** (seção da spec) e só a muda via ADR.

## Regras de ouro da onda 2
1. Cada projeto em seu worktree e branch `proj/<pid>`.
2. Nenhum projeto importa outro durante a onda 2; só `shared/*`.
3. Integração (onda 3) transforma cada projeto em pacote instalável (`uv` workspace member).

## Ordem de kickoff (cole no Codex)
- Onda 0: `Leia AGENTS.md e harness/GSD-LITE-PLUS.md. Execute sdd-bootstrap.`
- Onda 1: `Execute sdd-plan p00, sdd-plan-check, sdd-execute, sdd-verify, sdd-gate.`
- Onda 2: `bash scripts/harness/new-worktrees.sh p01 p02 p03 p04 && bash scripts/harness/run-parallel.sh p01 p02 p03 p04`
- Onda 3: `Acione o agent sdd-integrator para mergear as branches em ordem de dependência e publicar os pacotes.
- Onda 4: `Execute sdd-plan p05 ...`

## Orçamento
`LAB_MAX_USD` (padrão 5) vale só para runs `live`. Tudo em CI roda `fake`. Benchmarks reais: `replay` a partir de cassettes gravadas uma vez com autorização.
