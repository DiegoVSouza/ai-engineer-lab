# P02 — AI Engineering em produção

## Resumo de 1 página
Toolkit com tools de schema validado, pipeline de evals com detecção de regressão, guardrails com suíte adversarial e otimização de custo/latência. O ponto: mudar prompt ou modelo roda evals e acusa regressão sozinho.

## Conceitos
- **Structured outputs**: schema (Pydantic/JSON Schema) → validação → retry com feedback do erro. Falhar alto quando inválido.
- **Retries**: só em erros retriáveis; backoff exponencial + jitter; idempotência para tools com efeito colateral; timeouts em toda chamada.
- **Evals**: dataset versionado; métricas de decisão e de tool call; offline (CI) vs online (produção, feedback). **LLM-as-judge**: útil mas enviesado (posição, verbosidade, auto-preferência) → calibrar com humano.
- **Prompt injection**: direta (usuário) e **indireta** (via documento, KB, resultado de tool). Defesa em camadas: separar instruções de dados, least-privilege nas tools, allowlist por papel, confirmação para ações sensíveis, saída validada, limites de execução. Nenhuma defesa única basta.
- **Custo/latência**: streaming (latência percebida), cache (exato/semântico — cuidado com vazamento entre tenants), roteamento de modelo (barato primeiro, escala por confiança), controle de tokens (contexto curto, resumo).

## Trade-offs
| Decisão | Ganho | Custo |
|---|---|---|
| Cache semântico | menos custo | respostas obsoletas/vazamento |
| Roteador de modelos | custo menor | complexidade e erro de roteamento |
| Guardrail por LLM | cobre variações | latência, falsos positivos |

## Perguntas de entrevista
1. *How would you detect a regression after a prompt change?* — Versioned eval set in CI with thresholds and per-slice metrics.
2. *Direct vs indirect prompt injection?* — Indirect arrives via data the agent reads; mitigate with privilege separation and tool allowlists.
3. *How do you make tool calls safe?* — Schema validation, authorization, limits, confirmation, audit log.
4. *How to cut cost 50% without hurting quality?* — Measure first; routing, caching, shorter context; verify with evals.
(≥6 adicionais após execução.)

## Números para citar
`PENDING`: taxa de bloqueio adversarial, custo/latência antes×depois.
