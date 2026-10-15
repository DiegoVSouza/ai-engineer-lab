# P03 — Observabilidade e confiabilidade (Bloco 3)

## Objetivo
Enxergar o que um sistema de agentes faz em produção e localizar a causa de um incidente em minutos.

## Entregáveis
- `projects/p03-observability/` com pacote `supportops_obs`.
- `instrumentation/`: OpenTelemetry (traces, métricas, logs correlacionados) para chamadas LLM, agentes, tools, banco, HTTP. **Verificar convenções semânticas GenAI atuais do OTel na execução** (estão em evolução) e registrar em `sources.lock.json`; opt-in para captura de conteúdo (PII).
- `stack/`: `docker-compose.obs.yml` (OTel Collector + Jaeger ou Tempo + Prometheus + Grafana).
- `metrics/`: tokens, custo, latência (histogramas p50/p95), taxa de erro, retries, sucesso por tarefa, passos por execução.
- `dashboards/` (Grafana JSON provisionado) e `alerts/` (regras Prometheus: custo anômalo, erro, p95, **loop de agente**).
- `loopdetect/`: detector de loops (mesma tool+args repetida, ciclo de estados, passos > limite).
- `incident-lab/`: 3 incidentes simulados (tool lenta, loop de agente, explosão de custo) + runbook com como achar a causa pelo trace.
- App demo fina que usa o runner `core` do P01 **via interface mínima** (stub local até a integração).

## Public API
```python
def setup_telemetry(service_name: str, *, otlp_endpoint: str | None, capture_content: bool=False) -> None
@traced_agent(name=...) / @traced_tool(name=...)
def record_llm_call(resp: LLMResponse) -> None   # tokens, custo, latência
class LoopDetector: def observe(self, step: StepRecord) -> LoopSignal
```

## Fases
- **001 instrumentation** (setup + decorators + spans LLM/tool/agent).
- **002 stack+metrics** (compose, métricas, dashboards).
- **003 alerts+loops** (regras e detector).
- **004 incident-lab** (simulações + runbook + evidência).

## Verificação
- Teste com exporter em memória: uma requisição gera árvore de spans LLM→agente→tool→db com atributos esperados e `trace_id` nos logs.
- Alertas validados com `promtool check rules`; teste de unidade de cada regra com séries sintéticas, se disponível.
- Detector pega os 3 padrões de loop e **não** dispara em execução saudável (falso-positivo).
- Cada incidente: screenshot/trace exportado + runbook; sem trace real = `PENDING`.

## README exigido
Arquitetura (Mermaid), como subir a stack, como instrumentar um serviço, guia de dashboards, tabela de alertas, passo a passo de cada incidente.

## Documentação de conhecimento
`docs/knowledge/P03-observability.md`: traces vs métricas vs logs, convenções GenAI, cardinalidade, SLI/SLO para IA, custo como métrica de primeira classe, sampling, privacidade em traces.

## Fora de escopo
Fila/mensageria (P04), evals (P02), deploy na nuvem.
