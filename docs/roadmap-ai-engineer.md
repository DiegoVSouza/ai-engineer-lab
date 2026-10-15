# Roadmap Aluno — AI Engineer (First Trial)

Roadmap prático para se posicionar como **AI Engineer** com foco em sistemas multi-agentes, produção, observabilidade e visibilidade internacional.

## Legenda

| Cor | Significado | Como tratar |
|---|---|---|
| 🔵 Azul | **Saber fazer na prática** | Construir, rodar e deixar código funcionando |
| 🟡 Amarelo | **Saber falar sobre** | Dominar conceitos e trade-offs para entrevistas e discussões técnicas |
| 🔴 Vermelho | **Trabalhar em paralelo** | Rodar ao longo de todo o roadmap, sem esperar o resto terminar |

## Visão geral

| # | Bloco | Tipo | Resultado esperado |
|---|---|---|---|
| 1 | Multi-agentes e Orquestração | 🔵 Prática | Mesmo caso de uso implementado em vários frameworks |
| 2 | AI Engineering em Produção | 🔵 Prática | Agentes robustos, avaliados, seguros e otimizados |
| 3 | Observabilidade e Confiabilidade | 🔵 Prática | Tracing, métricas, dashboards e alertas |
| 4 | Mensageria e Sistemas Assíncronos | 🔵 Prática | Processamento assíncrono, eventos e deploy na AWS |
| 5 | Projeto AI Engineer Internacional | 🔵 Prática | Projeto de portfólio end-to-end, documentado em inglês |
| 6 | Aprofundamento / Próximo Nível | 🟡 Conceitual | Repertório para system design e entrevistas |
| 7 | Ativação LinkedIn Estratégica | 🔴 Paralelo | Visibilidade, networking e candidaturas |

---

## 1. 🔵 Multi-agentes e Orquestração

**Objetivo:** construir e comparar sistemas multi-agentes com diferentes frameworks, entendendo quando cada abordagem é adequada.

### Tarefas

- [ ] **Arquitetura supervisor-worker**: construir com agentes especializados, delegação, estado compartilhado e critérios de finalização.
- [ ] **LangGraph**: implementar multi-agentes incluindo paralelismo, retries, checkpoints e human-in-the-loop.
- [ ] **CrewAI**: implementar o *mesmo caso de uso* e comparar delegation, tasks, tools e workflows.
- [ ] **AutoGen, Semantic Kernel e LlamaIndex**: implementar um fluxo equivalente em cada um, identificando quando cada abordagem é adequada.

### Entregáveis

- Um caso de uso único implementado em 5 frameworks (LangGraph, CrewAI, AutoGen, Semantic Kernel, LlamaIndex).
- Tabela comparativa: facilidade de uso, controle de fluxo, gestão de estado, maturidade, observabilidade.

### Critério de pronto

- Consigo explicar por que escolheria cada framework para um cenário diferente.
- O supervisor sabe quando parar (critério de finalização explícito).

---

## 2. 🔵 AI Engineering em Produção

**Objetivo:** transformar protótipos em sistemas confiáveis, avaliáveis, seguros e econômicos.

### Tarefas

- [ ] **Tool Calling com Structured Outputs**: validação de schemas, retries, timeouts e tratamento de falhas.
- [ ] **Pipeline de avaliação** para agentes: dataset de testes, métricas de qualidade, regressão e avaliação de tool calls.
- [ ] **Guardrails**: prompt injection, uso indevido de ferramentas, dados sensíveis e limites de execução.
- [ ] **Custo e latência**: streaming, caching, seleção de modelo e controle de tokens.

### Entregáveis

- Camada de tools com schemas validados (ex.: Pydantic) e política de retry/timeout.
- Dataset de avaliação versionado + script de execução de evals no CI.
- Conjunto de guardrails com testes adversariais.
- Relatório de otimização (antes/depois de custo e latência).

### Critério de pronto

- Uma mudança de prompt ou modelo roda os evals e acusa regressão automaticamente.
- Limites de execução (passos, tokens, tempo) estão configurados e testados.

---

## 3. 🔵 Observabilidade e Confiabilidade

**Objetivo:** enxergar o que o sistema de IA está fazendo em produção e agir antes que o usuário perceba o problema.

### Tarefas

- [ ] **OpenTelemetry**: instrumentar agentes e APIs com traces, métricas e logs correlacionados.
- [ ] **Tracing ponta a ponta**: LLM → agente → tool → banco → resposta, identificando latência, erros e loops.
- [ ] **Monitoramento**: tokens, custo, latência, taxa de erro, retries e sucesso das tarefas dos agentes.
- [ ] **Dashboards e alertas** com métricas técnicas e de negócio para um serviço de IA em produção.

### Entregáveis

- Trace completo de uma requisição atravessando todos os componentes.
- Dashboard com: custo por requisição, p50/p95 de latência, taxa de erro, retries, taxa de sucesso por tarefa.
- Alertas configurados (ex.: custo anômalo, aumento de erro, loops de agente).

### Critério de pronto

- Dado um incidente simulado, consigo localizar a causa pelo trace em minutos.

---

## 4. 🔵 Mensageria e Sistemas Assíncronos

**Objetivo:** desacoplar tarefas longas de IA da camada de API, com resiliência e deploy reproduzível.

### Tarefas

- [ ] **Processamento assíncrono de tarefas AI**: filas, workers, retries, dead-letter queue e idempotência.
- [ ] **Arquitetura orientada a eventos**: Kafka ou AWS SQS/SNS integrada a agentes e APIs FastAPI.
- [ ] **Execução desacoplada de tarefas longas**: status, persistência de estado e recuperação após falhas.
- [ ] **Containerização e deploy**: Docker e CI/CD em AWS.

### Entregáveis

- API FastAPI que enfileira tarefas e expõe endpoint de status.
- Workers consumindo da fila com DLQ e tratamento de idempotência.
- Pipeline CI/CD (build, testes, deploy) com imagem Docker publicada.

### Critério de pronto

- Derrubo um worker no meio de uma tarefa e ela é retomada sem duplicar efeitos.
- Deploy acontece por pipeline, sem passos manuais.

---

## 5. 🔵 Projeto AI Engineer Internacional

**Objetivo:** projeto-vitrine que reúne tudo e prova capacidade de entregar um sistema real, com documentação em inglês.

### Tarefas

- [ ] **Aplicação end-to-end de multi-agentes** para um problema empresarial real, usando supervisor-worker, RAG, tools e MCP.
- [ ] **Exposição da solução** com FastAPI, autenticação, processamento assíncrono, mensageria, PostgreSQL/Redis e observabilidade.
- [ ] **Qualidade e segurança**: evals automatizados, guardrails, tracing, métricas de custo/latência e testes de regressão.
- [ ] **Documentação pública em inglês**: arquitetura, decisões técnicas, benchmark de modelos e documentação técnica.

### Stack de referência

| Camada | Tecnologias |
|---|---|
| Orquestração | LangGraph (supervisor-worker), MCP, RAG |
| API | FastAPI + autenticação |
| Dados | PostgreSQL, Redis |
| Assíncrono | Kafka ou SQS/SNS, workers |
| Qualidade | Evals, guardrails, testes de regressão |
| Observabilidade | OpenTelemetry, dashboards |
| Infra | Docker, CI/CD, AWS |

### Critério de pronto

- Um recrutador internacional entende o problema, a arquitetura e os resultados lendo apenas o README.
- Há números concretos: custo, latência, qualidade nos evals.

---

## 6. 🟡 Aprofundamento / Próximo Nível

**Objetivo:** saber *falar* com profundidade sobre arquitetura, trade-offs e segurança, o que é decisivo em entrevistas de nível sênior.

### Tópicos

- [ ] **Padrões de arquitetura multi-agentes**: supervisor-worker, handoff, planner-executor, parallel agents e human-in-the-loop.
- [ ] **Comparação de frameworks** (LlamaIndex, Semantic Kernel, CrewAI, AutoGen) em arquitetura, estado, ferramentas, memória, observabilidade e produção.
- [ ] **AI system design**: escalabilidade, filas, caching, rate limiting, model routing, reliability e controle de custos.
- [ ] **Segurança de aplicações agentic**: IAM, isolamento de ferramentas, secrets, prompt injection e controle de permissões.

### Como estudar

- Para cada tópico, escrever um resumo de 1 página com trade-offs e um exemplo prático.
- Treinar a explicação em voz alta (inglês e português), como numa entrevista.
- Praticar perguntas de system design: "Como você escalaria um agente que atende 10 mil usuários simultâneos?"

---

## 7. 🔴 Ativação LinkedIn Estratégica (em paralelo)

**Objetivo:** gerar visibilidade e oportunidades enquanto constrói, sem esperar o projeto ficar pronto.

### Tarefas

- [ ] **Headline**: atualizar destacando AI Engineer, LLMs, Agentic AI, RAG, Multi-Agent Systems, MCP e produção.
- [ ] **Conteúdo em inglês**: publicar estudos técnicos do projeto, arquitetura supervisor-worker, observabilidade e benchmarks entre frameworks.
- [ ] **Interação semanal** com AI Engineers, Staff Engineers, founders e recruiters de empresas brasileiras e internacionais.
- [ ] **Networking e candidaturas**: conectar com recruiters e profissionais internacionais e aplicar estrategicamente para vagas de AI Engineer no Brasil, EUA, Europa e remoto global.
- [ ] **Portfólio público**: transformar o projeto em repositório com README em inglês, arquitetura, demonstração, métricas, decisões técnicas e link para o código.

### Rotina sugerida

| Frequência | Ação |
|---|---|
| Semanal | 1 post técnico + 5 a 10 interações relevantes |
| Semanal | Novas conexões com recruiters e engenheiros |
| A cada marco | Publicar o aprendizado (ex.: benchmark de frameworks) |
| Contínuo | Candidaturas estratégicas (Brasil, EUA, Europa, remoto) |

---

## Ordem sugerida de execução

1. Blocos **1 → 2 → 3 → 4** (fundação prática), com o **bloco 7** rodando em paralelo desde a semana 1.
2. **Bloco 5** consolida tudo em um projeto-vitrine.
3. **Bloco 6** estudado continuamente, intensificando antes das entrevistas.

## Checklist final

- [ ] Mesmo caso de uso em 5 frameworks, com comparação documentada
- [ ] Evals, guardrails e otimização de custo/latência funcionando
- [ ] Observabilidade ponta a ponta com dashboards e alertas
- [ ] Sistema assíncrono com fila, DLQ, idempotência e deploy na AWS
- [ ] Projeto internacional publicado com README em inglês
- [ ] Repertório de system design e segurança agentic
- [ ] LinkedIn ativo com conteúdo, networking e candidaturas
