# Plano de implementação no Codex — harness de engenharia (SDD) para SaaS em React + Go

> **Nota desta revisão.** Este documento adapta um plano originalmente escrito para pesquisa científica (memória em grafos, hipóteses, protocolo experimental) para o contexto de um **produto SaaS com frontend React e backend Go**. A arquitetura do harness (GSD Core, gates executáveis, uma fonte de verdade por responsabilidade) é agnóstica de domínio e foi preservada. O que era específico de método científico — hipóteses, freeze de protocolo, ARIA, viés temporal de dados — foi substituído por equivalentes de engenharia de produto: contrato de API, migrações de schema, segurança, observabilidade e processo de release.

## 0. Primeira etapa obrigatória — H00: construir e validar o harness SDD no Codex

O produto desta etapa é um harness instalado e exercitado no repositório do usuário (monorepo ou repositórios `frontend/` e `backend/`). Neste documento sua construção está especificada; a instalação ainda não foi executada. H00 precede P00; os identificadores P00–P15 permanecem estáveis como roadmap de fases de produto (autenticação, domínio principal, faturamento, etc. — a detalhar quando houver informação suficiente).

### 0.1 Decisão de arquitetura e pesquisa das fontes

Adotar **GSD Core como orquestrador principal**, acrescentando contratos de engenharia próprios do projeto. O repositório histórico `gsd-build/get-shit-done` está arquivado e indica continuidade em `open-gsd/gsd-core`. Resolver uma release estável dessa continuidade na execução de H00, registrar sua origem e fixá-la. Não usar a branch móvel `next` como dependência reprodutível. [Aviso de migração](https://github.com/gsd-build/get-shit-done), [GSD Core](https://github.com/open-gsd/gsd-core).

O fluxo GSD separa discussão, planejamento, execução, verificação e entrega. Aqui, cada fase recebe também um contrato de qualidade de engenharia (testes, contrato de API, segurança). "Entrega" significa checkpoint local auditável; abrir PR, dar merge ou fazer deploy depende da autorização correspondente. [Explicação do ciclo de fases](https://github.com/open-gsd/gsd-core/blob/next/docs/explanation/the-phase-loop.md).

Spec Kit serve como referência complementar para constituição, requisitos e análise de consistência. **Não instalar um segundo orquestrador concorrente**; aproveitar esses conceitos nos contratos do projeto. [GitHub Spec Kit](https://github.com/github/spec-kit).

As decisões abaixo são **adaptações de engenharia propostas para este produto**, não funcionalidades que se presume já existirem no GSD. O valor do harness é operacional: verificar, reproduzir e rastrear o trabalho de construção do SaaS, não garantir qualidade por si só.

### 0.2 Correções necessárias no processo anterior

| Elemento anterior | Decisão para este projeto | Razão |
|---|---|---|
| Percentuais fixos de degradação de contexto | Retirar como afirmação factual | Não há evidência de limiares universais por modelo/tarefa |
| Novo chat em toda fase | Pacote mínimo de contexto por plano; retomada explícita quando necessário | O executor precisa de contexto suficiente e verificável, sem depender de memória informal |
| Aprovação humana obrigatória em toda fase | Gates executáveis (testes, lint, contrato de API) + revisão humana só para decisões de produto/arquitetura ainda não resolvidas | Preserva supervisão sem contrariar execução autônoma |
| `.planning/status.md` como estado | Migrar para o estado nativo GSD validado na instalação | Evitar duas versões divergentes do progresso |
| Descartar testes que falham para "destravar" a entrega | Preservar testes vermelhos como sinal; corrigir causa raiz | Falha de teste é informação, não obstáculo a remover |
| Desenhar a UI antes de fechar o contrato de API | Definir primeiro o contrato de API (OpenAPI/protobuf); UI pode prototipar em paralelo, mas o contrato é fonte de verdade | Evita retrabalho de frontend a cada mudança de backend |
| Retornar a qualquer fase e regenerar código livremente | Classificar a mudança (breaking change de API, migração de schema), versionar e invalidar clientes/derivados gerados | Mudança de contrato depois de consumidores existentes tem custo e exige plano de migração |
| Lint e revisão de código como garantia suficiente | Acrescentar testes de contrato de API, testes e2e, revisão de segurança e checagem de performance | Qualidade de estilo de código e corretude/segurança são propriedades distintas |
| "Pronto para produção" quando o build passa | Checklist de release rastreável, com plano de rollback e critérios de observabilidade | Build verde não comprova que a feature é segura para os usuários reais |

### 0.3 H00-A — inventário e instalação reproduzível

1. Ler as instruções aplicáveis e inspecionar Git, código (frontend e backend), planos anteriores, agentes, skills e permissões. Registrar alterações preexistentes e preservar sua autoria. Não criar uma nova raiz sobre projeto existente.
2. Identificar Codex, Node/npm, Go, sistema operacional e escopos de instalação. Inspecionar GSD já instalado antes de adicionar outra cópia. Registrar comandos disponíveis e limites reais de subagents.
3. Resolver uma versão publicada do GSD Core, conferir origem, licença e instalador. Guardar versão, integridade do pacote e commit (quando verificável) em `docs/harness/sources.lock.json`. Não inventar commit a partir do número de versão.
4. Usar o instalador com suporte Codex; preferir escopo local, após confirmar suporte de `--local` na release. Não copiar diretamente agentes Claude do repositório upstream. Examinar o diff de configuração; mesclar instruções existentes e impedir duplicações.
5. Reiniciar a sessão se necessário e verificar descoberta real. Registrar em `docs/harness/capabilities.json` os comandos/skills encontrados, caminhos efetivos, escopo, formato de invocação e resultado do smoke. Não presumir que comandos `/gsd-*` de tutoriais sejam invocações válidas no Codex sem confirmar.

A documentação consultada exige transformação pelo instalador, apresenta suporte Codex a partir de CLI 0.130.0 e hooks estáveis a partir de 0.137.0, e declara **indisponíveis no Codex os avisos GSD de consumo de contexto**. Confirmar compatibilidade da release escolhida; gates de engenharia devem funcionar por comandos explícitos, sem depender desses hooks. [Instalação por runtime](https://github.com/open-gsd/gsd-core/blob/next/docs/how-to/install-on-your-runtime.md).

Exemplo parametrizado, a adaptar **somente depois de resolver uma versão e conferir o help**:

```bash
GSD_VERSION='SUBSTITUIR_PELA_RELEASE_VERIFICADA'
npx "@opengsd/gsd-core@${GSD_VERSION}" --help
npx "@opengsd/gsd-core@${GSD_VERSION}" --codex --local
```

O placeholder torna o exemplo deliberadamente incompleto; não executá-lo literalmente. Se o escopo local não for suportado, registrar a incompatibilidade e preparar a instalação apropriada sem alterar silenciosamente a configuração global. Não atualizar automaticamente durante campanhas de implementação.

Para repositório existente (ex.: monorepo com `frontend/` em React e `backend/` em Go), usar o onboarding e a ingestão de documentos suportados pela versão instalada; importar o plano e mapear código antes de gerar roadmap, reaproveitando trabalho já válido. [Onboarding oficial](https://github.com/open-gsd/gsd-core/blob/next/docs/tutorials/onboarding-an-existing-codebase.md).

### 0.4 H00-B — uma fonte de verdade por responsabilidade

Os nomes exatos devem seguir os templates da release instalada. [Tutorial GSD](https://github.com/open-gsd/gsd-core/blob/next/docs/tutorials/your-first-project.md).

| Informação | Fonte canônica proposta | Regra de escrita |
|---|---|---|
| Regras de atuação | `AGENTS.md` | Principal; enxuto, apontando para documentos especializados |
| Princípios de engenharia | `docs/protocol/constitution.md` | Principal; alteração substantiva registrada em decisão |
| Intenção e escopo do produto | `.planning/PROJECT.md` | GSD/principal; referência ao plano de produto |
| Requisitos verificáveis | `.planning/REQUIREMENTS.md` | IDs estáveis; funcionais e não-funcionais |
| Ordem e dependências | `.planning/ROADMAP.md` | GSD/principal; vincular H00 e P00–P15 |
| Posição operacional | `.planning/STATE.md` | GSD/principal; única fonte de retomada operacional |
| Contexto e planos de execução | `.planning/phases/` | Formato nativo da release; ownership por plano |
| Contrato de API | `docs/contracts/openapi.yaml` (ou `.proto`) | Principal; versionamento semântico e changelog |
| Schema de dados | `backend/migrations/` | Principal; migrações reversíveis, nunca editadas após aplicadas |
| Histórico de decisões | `docs/decisions/ADR-*.md` | Acréscimos; decisões superadas preservadas |
| Builds e deploys | `artifacts/runs/<run_id>/` | Runner/CI; manifests e outputs identificados |
| Índice de builds/deploys | `docs/execution/run-registry.parquet` | Gerado dos manifests; reconstruível |
| Evidência de release | `artifacts/evidence/<bundle_id>/` | Builder; testes, cobertura, e2e, relatório de segurança congelados |
| Rastreamento entre camadas | `docs/harness/traceability.csv` | Exportado de requisitos, código e testes vinculados |

`docs/execution/STATE.md` e `docs/execution/tasks.json`, se existirem de um processo anterior, passam a ser **projeções opcionais geradas**, jamais autoridades editadas em paralelo. Migrar decisões para o GSD, registrar a origem e marcar as cópias como geradas. Conflito real entre estados exige reconciliação por commits e evidências; não escolher o arquivo mais recente apenas pelo horário.

Se uma futura release mudar os caminhos, documentar a tradução em `docs/harness/state-map.md`. Não manter dois orquestradores escrevendo progresso.

### 0.5 H00-C — constituição e contratos de engenharia do SaaS

A constituição deve fixar: **contrato de API primeiro** (mudanças de contrato exigem versionamento e não quebram consumidores existentes sem depreciação anunciada); **migrações de schema reversíveis** e nunca destrutivas sem backup; **segurança** (autenticação, autorização, segredos nunca em código-fonte, dependências auditadas); **observabilidade mínima** (logs estruturados, métricas, tracing) antes de considerar uma feature entregue; **orçamento de performance** (latência de API, tamanho de bundle do frontend); **acessibilidade mínima** no frontend React; **privacidade de dados de usuário** (conforme legislação aplicável); **proveniência das decisões técnicas**; **nenhuma claim de "pronto" sem evidência de teste automatizado e revisão de código**.

Separar explicitamente três estados:

- **Código:** implementado e verificado, falhou, ou pendente.
- **Feature:** entregue em staging, entregue em produção, ou revertida.
- **Contrato de API:** estável, em depreciação, ou quebrado sem versionamento (situação a corrigir, nunca a aceitar).

Uma feature pode estar com código correto e testes passando e, ainda assim, estar "não liberada" por decisão de produto — isso não é falha do harness. Nenhuma tarefa deve ter como critério de aceite apenas "o build passou"; o critério é o comportamento observável descrito no plano.

Criar requisitos como `API-001` (contrato de API versionado), `SEC-001` (autenticação/autorização mínimas), `MIG-001` (migração de schema reversível), `OBS-001` (observabilidade mínima por feature), `PERF-001` (orçamento de performance) e `A11Y-001` (acessibilidade mínima do frontend).

Cada plano deve conter os campos nativos exigidos pelo GSD e, em seção suplementar, este contrato de engenharia:

```yaml
# Contrato de conteúdo proposto; adaptar ao template nativo, não ao config do GSD.
engineering_task_id: P03-T01
requirement_ids: [API-001]
objective: expor endpoint de criação de recurso respeitando o contrato versionado
inputs: [docs/contracts/openapi.yaml]
allowed_write_paths: [backend/internal/handlers/, backend/migrations/, frontend/src/api/]
forbidden_changes: [contrato_de_api_sem_versionar, schema_sem_migracao, credenciais_em_codigo]
engineering_risk: breaking_change
verification:
  unit_test: valida regra de negócio isoladamente
  negative_test: rejeita payload inválido/não autorizado
  contract_test: valida request/response contra o schema OpenAPI
  command: definido e executavel antes de fechar o plano
acceptance: comportamento demonstrado por teste automatizado, sem depender de verificação manual
handoff: resumo, diff, comandos, resultados, hashes e proxima acao
```

O exemplo define conteúdo, não afirma que `P03-T01` já existe. Usar a tarefa real e o schema real ao materializar o backlog. Não introduzir campos desconhecidos no `config.json` do GSD.

A matriz de rastreabilidade precisa registrar `requirement_id`, `phase_id`, `plan_path`, `api_spec_path`, `code_symbol`, `test_id`, `build_id`, `deploy_id`, `release_id`, `status` e `evidence_path`. Campos ainda não aplicáveis ficam explicitamente vazios com justificativa. Cobertura textual de um requisito não conta como evidência do comportamento.

### 0.6 H00-D — integrar seus agentes sem duplicar a orquestração

| Papel | Responsabilidade no ciclo | Integração |
|---|---|---|
| Principal/GSD | Escolher próxima fase, reunir decisões, integrar mudanças e persistir estado | Uma única autoridade operacional |
| Planner GSD | Decompor fase em planos executáveis | Recebe contrato de API e requisitos de engenharia |
| Plan checker GSD | Verificar dependências, escopo e aceite antes de executar | Acrescentar revisão de contrato/segurança quando o risco exigir |
| `backend-engineer` (Go) | Implementar handlers, regras de negócio, migrações | Escolher um executor por tarefa; evitar duas camadas recursivas de delegação |
| `frontend-engineer` (React) | Implementar telas, consumo de API, estado de UI | Consome o contrato de API já definido; não inventa endpoints |
| Verifier GSD | Conferir objetivo versus comportamento observado | Recebe comandos e evidências, não só o resumo do executor |
| `security-auditor` / `qa-engineer` | Verificar validade da implementação e cobertura de testes | Relatórios de leitura; principal registra resolução |
| Agents de produto/design existentes | Requisitos de negócio, UX, revisão especializada | Ativar conforme a fase do roadmap |

Ler dependências `.claude/agents/*.md` se existirem; transformá-las em contratos autocontidos. Prefixar agentes próprios quando houver colisão de nomes.

Começar com execução sequencial do harness. Depois do smoke, admitir até três subagents simultâneos, dentro do limite da sessão, com módulos disjuntos (ex.: backend e frontend em paralelo, integração serial). Papéis distintos não exigem processos simultâneos.

Cada handoff inclui: objetivo, IDs, documentos necessários, commit inicial, paths autorizados, comandos de validação, orçamento e condição de parada. Não carregar o código-base inteiro em cada contexto. Persistir artefatos antes de renovar a sessão.

### 0.7 H00-E — gates executáveis e política de autonomia

Construir verificadores pequenos em `scripts/harness/`, sem criar outro scheduler:

```bash
python scripts/harness/check.py --root .
python scripts/harness/trace.py --root .
python scripts/harness/verify.py --phase H00
```

`check.py` valida paths referenciados, arquivos de estado, parsers das configurações, versões registradas e ausência de autoridade operacional duplicada. `trace.py` exporta a matriz e identifica referências órfãs. `verify.py` executa a lista explícita de verificações da fase (testes, lint, contrato de API), registra comando, exit code, output e commit/hashes. Ausência de comando, execução ou artefato exigido produz `incomplete`, nunca `pass`.

| Gate | Evidência mínima | Consequência da falha |
|---|---|---|
| G-HAR: harness | Instalação descoberta, plano executado, retomada e falha detectada | Corrigir H00 antes de P00 |
| G-SPEC: plano | Requisitos, dependências, contrato de API, orçamento e aceite concretos | Corrigir plano antes de escrever o módulo |
| G-CODE: comportamento | Testes unitários/integração relevantes passando, lint, revisão do diff | Abrir correção delimitada |
| G-CONTRACT: contrato de API | Schema validado, sem breaking change não versionado, cliente gerado sincronizado | Impedir merge até corrigir o contrato |
| G-DEPLOY: staging | Deploy em staging, smoke tests e e2e executados | Invalidar/reverter o deploy afetado |
| G-QUALITY: qualidade | Cobertura mínima, performance dentro do orçamento, checagem de acessibilidade | Impedir promoção para produção |
| G-RELEASE: release | Release notes, plano de rollback, aprovação e observabilidade configurada | Corrigir ou adiar a release |

Prosseguir automaticamente em decisões locais cobertas pelo plano. Não converter uma verificação automática em "humano aprovou": registrar `review_mode=automated`, agente/comando e limitações. Consultar o responsável pelo produto se uma decisão material (ex.: mudar contrato público, remover dado de usuário) permanecer indeterminada após usar as escolhas já autorizadas.

Mudança após uma release exige `change_type`, motivo, artefatos afetados, status do contrato de API e plano de reexecução/rollback. Bug invalida derivados afetados; correção não apaga o histórico de deploys anteriores.

### 0.8 H00-F — ensaio obrigatório antes da implementação do produto

Usar diretório/branch temporário separado, sem tocar no backlog real. O ensaio mínimo é uma feature de brinquedo com duas tarefas: um endpoint Go com uma regra de negócio simples e uma tela React que o consome.

1. Especificar a regra (ex.: "um item só pode ser marcado como concluído se sua data de vencimento já passou ou é hoje", com a igualdade explícita). Criar fixtures com casos válido, inválido e de fronteira.
2. Fazer o planner produzir um plano com arquivos e comando de verificação; o plan checker deve detectar um plano deliberadamente sem teste negativo.
3. Executar a implementação correta (handler Go + validação + componente React) e verificar o comportamento com expectativas definidas antes do código.
4. Em cópia descartável, remover deliberadamente a validação da regra de negócio. O verificador deve reprovar. Preservar o log da falha esperada e descartar a cópia defeituosa sem integrá-la ao projeto.
5. Interromper entre tarefas, iniciar contexto novo e recuperar a próxima ação dos arquivos persistidos. Não repetir tarefa concluída nem aceitar sucesso com evidência ausente.
6. Alterar o contrato de API do endpoint (ex.: renomear um campo) e demonstrar que evidência da versão anterior não aprova automaticamente a nova versão — o teste de contrato deve reprovar até o cliente ser atualizado.
7. Exportar matriz, resumo e relatório final com distinção entre passagem, falha esperada e pendência. Medir duração e custo do ensaio quando disponível; valores desconhecidos permanecem desconhecidos.

**Aceite de H00:** descoberta operacional confirmada; configuração preservada; origem/versionamento do GSD registrados; state map consistente; agentes necessários carregados ou fallback sequencial demonstrado; ensaio positivo e negativo observado; falha de contrato de API detectada corretamente; retomada demonstrada; relatório `docs/harness/H00-VERIFICATION.md` com comandos, logs e hashes. TOML parseável, diretórios criados ou checklist preenchido isoladamente não bastam.

Se Codex/GSD estiver indisponível, concluir os contratos e os verificadores independentes; registrar H00 como bloqueado ou parcial. Não declarar um fallback manual como instalação GSD aprovada.

### 0.9 Roadmap inicial e definição de pronto para avançar

| Subetapa | Entrega | Dependência |
|---|---|---|
| H00-A | Inventário, instalação fixada e capabilities reais | Instruções e repositório acessíveis |
| H00-B | Estado canônico e migração documentada | H00-A |
| H00-C | Constituição, requisitos e contrato de plano de engenharia | H00-B |
| H00-D | Agents/skills adaptados (backend-engineer, frontend-engineer), sem colisões | H00-C |
| H00-E | Verificadores e política de gates | H00-C/D |
| H00-F | Ensaio adversarial (feature de brinquedo), retomada e relatório | H00-E |
| P00 | Scaffold do monorepo (Go + React), CI mínimo, schemas e `make doctor`/health-check | G-HAR aprovado |

Mapear esses IDs para os números nativos de fase GSD em `docs/harness/phase-map.csv`; o identificador de engenharia permanece estável mesmo que GSD use outra numeração. Não converter automaticamente cada módulo Go/React em fase. Planejar detalhadamente H00 e a próxima fase (P00); manter o restante (autenticação, domínio principal, faturamento, etc.) como roadmap com critérios de saída até reunir informação suficiente sobre o produto.

Reservar inicialmente **1–3 dias de trabalho para H00**, ajustados após o inventário, sem promessa de duração. O harness está pronto quando consegue conduzir uma tarefa de código, detectar erro (de teste ou de contrato) e retomar com evidência. Não postergar a construção do produto para criar dashboards de agentes, catálogo universal de skills ou infraestrutura distribuída antes de ter o SaaS mínimo rodando.
