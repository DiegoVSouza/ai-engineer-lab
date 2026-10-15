# P03 — Observabilidade e confiabilidade

## Resumo de 1 página
Instrumentei agentes e APIs com OpenTelemetry para ter um trace de ponta a ponta (LLM → agente → tool → banco), métricas de custo/latência/erro, dashboards, alertas e um detector de loops. Validei com 3 incidentes simulados e um runbook.

## Conceitos
- **Três sinais**: traces (causalidade), métricas (tendência/alerta), logs (detalhe) — correlacionados por `trace_id`.
- **Convenções semânticas GenAI do OTel**: atributos padronizados para modelo, tokens, operação. Ainda em evolução → verificar versão atual.
- **Cardinalidade**: nunca use `user_id`/prompt como label de métrica.
- **SLI/SLO para IA**: latência p95, taxa de sucesso da tarefa, custo por requisição, taxa de escalonamento, qualidade amostrada.
- **Privacidade**: não capture prompts/respostas por padrão; opt-in, redija PII.
- **Sampling**: tail-based para guardar traces com erro/lentos.

## Como achar causa de incidente (roteiro)
1. Alerta dispara → dashboard: qual métrica? 2. Filtrar traces por intervalo e erro. 3. Maior span filho = suspeito. 4. Ver atributos (modelo, tokens, retries). 5. Confirmar no log correlacionado.

## Perguntas de entrevista
1. *How do you observe an LLM app differently from a normal service?* — Non-determinism, cost as a metric, token usage, quality signals, long multi-step traces.
2. *What alerts would you set?* — Cost anomaly, error rate, p95, agent loop, retry storms.
3. *How do you detect an agent loop?* — Repeated tool+args, state cycles, step count over limit.
4. *Tracing and PII?* — Redact, opt-in content capture, retention limits.
(≥6 adicionais após execução.)

## Números para citar
`PENDING`: overhead de instrumentação, tempo para diagnosticar cada incidente.
