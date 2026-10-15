# P05 — SupportOps Platform (flagship)

## Pitch
**30s:** Construí uma plataforma que triagem tickets B2B com agentes: supervisor-worker, RAG com citações e ações em billing/CRM via MCP, tudo assíncrono, observável, avaliado e com guardrails.
**2min:** + arquitetura (API → fila → worker → LangGraph → RAG/MCP → DB), + segurança (JWT, tenants, HITL), + qualidade (evals no CI), + números (`PENDING`).
**5min:** + decisões, falhas encontradas, como escalaria.
*(Versão EN: escrever após a execução.)*

## Walkthrough de uma requisição
Cliente → `POST /v1/tickets` (JWT, rate limit) → grava + enfileira (idempotente) → worker pega → guardrails de entrada → supervisor roteia → RAG (pgvector) ∥ billing/CRM via MCP → responder valida com citações → ação sensível? pausa HITL → resultado persistido → eventos → `GET` mostra status. Um `trace_id` atravessa tudo.

## Conceitos-chave
- **RAG**: chunking, embeddings, recuperação híbrida, citações, avaliação (hit@k, groundedness); falhas: chunk ruim, contexto demais, doc desatualizado, injeção via documento.
- **MCP**: protocolo padrão para expor tools/recursos a agentes; segurança: escopo por tool, autenticação, confirmação, auditoria.
- **Multi-tenancy**: isolamento em dados, cache, vetores e filas.
- **HITL**: aprovação para ações irreversíveis, com estado persistido.

## Perguntas de entrevista
1. *Walk me through the architecture.* — (use o walkthrough acima, em 2 minutos.)
2. *What would you change for 10k concurrent users?* — ver `06-system-design-and-security.md`.
3. *What was the hardest bug?* — preencher com falha real do run.
4. *How do you know it works?* — evals no CI, testes adversariais, métricas reais.
5. *What would you do with 2 more weeks?* — limitações do README.
(≥5 adicionais.)

## Números para citar
`PENDING`: custo/ticket, p50/p95, acurácia no golden set, hit@k, taxa de escalonamento.
