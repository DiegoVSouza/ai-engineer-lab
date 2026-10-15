# P05 — SupportOps Platform (projeto internacional, flagship) (Bloco 5)

## Objetivo
Aplicação end-to-end que integra P01–P04: multi-agentes supervisor-worker com RAG, tools e MCP, exposta por API autenticada, assíncrona, observável, avaliada e segura, com documentação pública em inglês.

## Entregáveis
- `projects/p05-supportops-platform/`: serviço `supportops_platform`.
- `agents/`: supervisor-worker LangGraph (reutiliza p01), workers: triage, kb-rag, billing, crm, responder; HITL para ações sensíveis.
- `rag/`: ingestão de KB, chunking, embeddings, **pgvector**, retrieval híbrido simples, citações, eval de retrieval (hit@k) em `fake`/`replay`.
- `mcp/`: servidor MCP (billing/CRM mock) + cliente usado pelos agentes. **Verificar SDK/spec atual do MCP na execução**.
- `api/`: FastAPI, auth (JWT com escopos; chaves por tenant), rate limiting (Redis), multi-tenant básico, endpoints de tickets, status, aprovação HITL, feedback.
- `async/`: usa p04 (fila, worker, DLQ, idempotência).
- `quality/`: usa p02 (evals no CI, guardrails, limites, relatório custo/latência).
- `obs/`: usa p03 (traces, métricas, dashboards, alertas).
- `infra/`: compose completo + Terraform plan + CI/CD.
- `benchmarks/`: comparação de ≥2 modelos/configurações (qualidade × custo × latência) com `replay`.
- `docs/`: arquitetura, ADRs, threat model, runbook, benchmark.

## Public API
`openapi.yaml` versionado: `POST /v1/tickets`, `GET /v1/tickets/{id}`, `POST /v1/tickets/{id}/approve`, `POST /v1/feedback`, `GET /healthz`, `GET /metrics`. Contrato congelado após a fase 003; mudança = ADR + versão.

## Fases
- **001 integration-skeleton** (importa pacotes p01–p04, compose completo, health).
- **002 rag+mcp** (Wave 1: RAG ∥ MCP server; Wave 2: ligação aos agentes).
- **003 api+auth+async** (API, JWT, rate limit, enfileiramento; congela OpenAPI).
- **004 quality-security** (evals no CI, guardrails ponta a ponta, threat model, teste adversarial pela API).
- **005 observability+benchmarks** (dashboards, alertas, benchmark, relatório de custo).
- **006 docs-release** (README EN, architecture, demo script, tag `v0.1.0` local).

## Verificação
- `make verify` verde em `fake` com stack completa em compose.
- E2E: ticket → fila → agentes (RAG+MCP) → resposta com citações → status `done`; ticket com reembolso alto → pausa HITL → `approve` → conclui.
- Usuário do tenant A não lê ticket do tenant B (teste negativo).
- Injeção via conteúdo de KB não aciona tool proibida (teste adversarial).
- Uma mudança de prompt que piora o dataset falha o CI.
- Crash de worker no meio → recuperação sem efeito duplicado.
- Um trace único cobre API → fila → worker → agente → LLM → tool → DB.
- README permite a um recrutador entender problema, arquitetura e resultados sem abrir o código; números com link para `artifacts/runs/` ou `PENDING`.

## README exigido
Segue `docs/standards/README-STANDARD.md` na íntegra: pitch, diagrama de arquitetura, quickstart de 5 min, demo, resultados (custo, latência, qualidade), decisões, limitações, roadmap, `README.pt-BR.md`.

## Documentação de conhecimento
`docs/knowledge/P05-supportops-platform.md` + `docs/knowledge/06-system-design-and-security.md`: walkthrough de arquitetura, decisões e alternativas, escala para 10 mil usuários simultâneos, segurança agentic, roteiro de apresentação de 5 minutos.

## Fora de escopo
Deploy real na AWS e publicação (exigem autorização), UI web completa (opcional: demo CLI/Swagger), fine-tuning.
