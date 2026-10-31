# Plano de adaptação — encaixar o plano React + Go no Harness Kit existente

> **Para quem executa (Codex).** Este documento é a terceira peça na raiz, junto de `harness-kit-v2.1.md` (o kit) e `plano-harness-saas-react-go.md` (o plano React+Go). Sua tarefa: **adaptar o harness que já roda neste repositório** para também construir o frontend React (e o backend Go) usando o plano React+Go, **sem instalar um segundo orquestrador e sem criar uma segunda fonte de verdade de progresso**.
> Convenções do kit: `[VERIFICAR]` = confirmar na doc oficial / no repo antes de afirmar. `<PLACEHOLDER>` = preencher com o valor real. Nada aqui foi executado; é especificação.

---

## 0. Regras inegociáveis desta adaptação

1. **O kit é o orquestrador. Não instalar o GSD Core.** O H00 do plano React+Go (instalar, fixar versão, ensaiar o GSD) fica **substituído** por B0–B4 abaixo. Dele aproveitamos apenas os **contratos de engenharia**: API primeiro, migrações reversíveis, gates, rastreabilidade, release.
2. **Uma fonte de verdade por responsabilidade.** Progresso vive em `docs/harness/feature_list.json` + `docs/harness/progress.md`. Não criar `.planning/STATE.md`, `ROADMAP.md` nem equivalentes que escrevam progresso em paralelo. Se algo gerado precisar existir, marcar como **projeção gerada**, nunca editada à mão.
3. **Inspecionar antes de escrever.** Ler o estado atual do repo (`harness.yaml`, `.harness/kit-version`, `.harness/modules.lock`, `AGENTS.md`, `CLAUDE.md`, `feature_list.json`, `progress.md`, `scripts/`, `shared/`, `.claude/`, CI) e **preservar o que já existe e funciona**. Registrar alterações preexistentes e sua autoria. Não recriar a raiz sobre projeto existente.
4. **Não sobrescrever `AGENTS.md` / `CLAUDE.md` sem merge.** Acrescentar seções; manter `AGENTS.md` < 200 linhas e apontando para documentos especializados. `CLAUDE.md` continua importando `@AGENTS.md`.
5. **Poda e simplicidade.** Só ligar módulo que tenha justificativa no `harness.yaml`. Não trazer do plano React+Go o que é resquício do plano científico original (`run-registry.parquet`, `artifacts/runs/<run_id>/`, hipóteses, freeze de protocolo, ARIA, viés temporal).
6. **Evidência, não declaração.** Ausência de comando, execução ou artefato exigido = `incomplete`, nunca `pass`. Teste vermelho é sinal; corrigir a causa raiz, não remover o teste.
7. **Escritas single-threaded por padrão.** Começar sequencial. Backend e frontend em paralelo só depois do contrato de API congelado e com paths disjuntos garantidos por hook (seção 6).
8. **Não inventar.** Sintaxe de hooks/skills/subagentes do Codex, flags de ferramentas de codegen e nomes de pacotes: confirmar (`[VERIFICAR]`) e registrar em `docs/harness/capabilities.json` o que foi realmente descoberto.

---

## 1. Fase B-1 — Descoberta (obrigatória, antes de B0)

Produzir `docs/harness/adaptation-discovery.md` respondendo, **a partir do repo** (não do que este documento supõe):

| Pergunta | Onde olhar | Efeito |
|---|---|---|
| O SaaS tem **agente de IA embutido** ou o harness só constrói o app? | código, `agent/`, `harness.yaml` (`product.has_agent`), docs | Define o perfil (seção 2) |
| Estrutura: monorepo (`frontend/` + `backend/`) ou repos separados? | árvore do repo | Caminhos de `allowed_write_paths` e stacks |
| Versões reais de Go, Node, gerenciador de pacotes, Codex CLI | `go.mod`, `package.json`, shell | Comandos dos stacks |
| Já existe contrato de API (OpenAPI/proto)? Codegen? | `docs/`, `backend/`, CI | Decide se B3 cria ou adota |
| Já existem migrações? Ferramenta? | `backend/migrations/` ou equivalente | Hook de migrações aplicadas |
| Estado atual do `feature_list.json` e `progress.md` | `docs/harness/` | Onde encaixar as fases P00–P15 |
| Inconsistência de versão do kit: arquivo `harness-kit-v2.1.md` vs `kit_version: 2.0.0` | `harness.yaml`, `.harness/kit-version`, `VERSION` | Alinhar antes de qualquer upgrade (seção 9) |
| `.claude/agents/*.md` existentes (backend-engineer, frontend-engineer, etc.) | `.claude/agents/` | Reaproveitar, não duplicar |

Se uma resposta não puder ser obtida do repo e mudar materialmente o plano, **registrar a pergunta em `docs/harness/decisions.md` e perguntar ao responsável**; não escolher silenciosamente.

---

## 2. Fase B0 — Perfil e `harness.yaml`

### 2.1 Escolha de perfil

- **Sem agente embutido no produto:** `product.has_agent: false`; criar o perfil novo `profiles/web-saas.yaml` (não existe no kit v2.x; é contribuição de volta ao kit).
- **Com agente embutido:** perfil `agent-saas` (já existe), o que liga `risk.multi_tenant: true` → `governance: full` e exige trifecta mapeada e `security.md`.

### 2.2 Alterações no `harness.yaml` (mínimas)

```yaml
project:
  type: web-saas                 # ou agent-saas, conforme B-1
  stack:
    backend: go                  # hoje o kit só lista python | ts | none → estender (ver 3.1)
    frontend: react-ts
  kit_version: <versão real após alinhar>

builder:
  long_running: true
  clean_context_reviewer: true
  stop_hook_runs_check: true

risk:
  multi_tenant: <true|false conforme produto>
  sensitive_data: <true|false>
  irreversible_actions: [<ex.: delete_record, charge_card, migrate_schema>]
  governance: <lite|full pela regra do kit>

# NOVO bloco, específico de SaaS web (ver módulos na seção 3)
saas:
  api_contract: { format: openapi, path: docs/contracts/openapi.yaml, client_codegen: <ferramenta [VERIFICAR]> }
  migrations:   { dir: backend/migrations, tool: <ferramenta [VERIFICAR]>, reversible_required: true }
  frontend_budget: { max_bundle_kb: <PLACEHOLDER>, a11y_check: true }
  perf_budget:  { api_p95_ms: <PLACEHOLDER> }
  release:      { rollback_plan_required: true, observability_min: [structured_logs, metrics, tracing] }
```

`harness_init.py` / `harness_upgrade.py` devem aceitar os novos valores sem quebrar projetos antigos (valores desconhecidos → erro claro, não ignorar). Atualizar `.harness/modules.lock` com os módulos novos.

---

## 3. Fase B1 — Stacks e módulos novos

O kit é pensado para agentes e não cobre app web. Criar estes módulos (em `modules/` do kit **e** instanciados neste projeto), cada um com entregável verificável:

| Módulo | Camada | Liga quando | Entregável |
|---|---|---|---|
| `stack-go` | S | `stack.backend == go` | comandos de `check-fast`/`check-full` para Go |
| `stack-react-ts` | S | `stack.frontend == react-ts` | comandos para React/TS |
| `api-contract` | S | `saas.api_contract` presente | OpenAPI + teste de contrato + cliente TS gerado |
| `db-migrations` | S | `saas.migrations` presente | regra e hook de migrações |
| `frontend-quality` | S | frontend presente | orçamento de bundle + checagem de a11y |
| `release` | S | sempre em SaaS | rollback, observabilidade mínima, release notes |

### 3.1 Comandos por stack (adaptar à ferramenta real encontrada em B-1)

- **Go — `check-fast`:** `gofmt -l` (deve ser vazio), `go vet ./...`, `golangci-lint run` (se existir), `go test ./... -short`. **`check-full`:** `go test ./... -race -cover` + teste de contrato.
- **React/TS — `check-fast`:** `eslint`, `tsc --noEmit`, `vitest run` (unit). **`check-full`:** testes completos, build de produção (medir bundle), e2e (ex.: Playwright `[VERIFICAR]`), checagem de a11y.
- Mensagens de erro **instrutivas**: dizer *como corrigir*, não só que falhou (princípio do kit).
- Se o repo já usa outra ferramenta (ex.: `jest`, `pnpm`, `make`), **adotar a existente**; não trocar por preferência.

### 3.2 `api-contract` — contrato primeiro

- Fonte de verdade: `docs/contracts/openapi.yaml` (ou `.proto`, se já for o padrão do repo), versionamento semântico + changelog.
- **Gate G-CONTRACT:** validar o schema; regenerar o cliente TS e exigir `git diff --exit-code` limpo; detectar breaking change não versionado.
- Frontend **consome** o contrato; não inventa endpoint. Mudou o contrato → classificar (`breaking | additive`), versionar, invalidar derivados gerados, atualizar o cliente.

### 3.3 `db-migrations`

- Migrações reversíveis (`up` + `down`), nunca destrutivas sem backup registrado, **nunca editadas depois de aplicadas**.
- Hook PreToolUse: bloquear edição/remoção de migração já aplicada (determinar "aplicada" por histórico do git ou tabela de controle `[VERIFICAR]`), com mensagem dizendo para criar uma migração nova.

### 3.4 `release`

- Release notes, plano de rollback, observabilidade mínima (logs estruturados, métricas, tracing) como critério de "entregue". Build verde ≠ pronto para produção.

---

## 4. Fase B2 — Portar constituição e requisitos para o estado do kit

### 4.1 Constituição

Criar `docs/protocol/constitution.md` com os princípios do plano React+Go (API primeiro; migrações reversíveis; segurança; observabilidade mínima; orçamento de performance; a11y mínima; privacidade de dados; proveniência de decisões; **nenhuma claim de "pronto" sem evidência automatizada e revisão**). Referenciar do `AGENTS.md` com uma linha. Alteração substantiva → ADR em `docs/decisions/`.

### 4.2 Requisitos viram campo do `feature_list.json`

Não criar `REQUIREMENTS.md` como estado paralelo. Os IDs vivem em um catálogo estático `docs/protocol/requirements.md` (somente definição, sem status) e **cada feature referencia seus IDs**:

| ID | Significado |
|---|---|
| `API-001` | contrato de API versionado |
| `SEC-001` | autenticação/autorização mínimas |
| `MIG-001` | migração de schema reversível |
| `OBS-001` | observabilidade mínima por feature |
| `PERF-001` | orçamento de performance |
| `A11Y-001` | acessibilidade mínima do frontend |

Estender o schema de cada item do `feature_list.json` (**campos fixos; o agente só edita `passes`**):

```json
{
  "id": "P03-T01",
  "phase": "P03",
  "title": "<objetivo em uma frase>",
  "requirement_ids": ["API-001"],
  "allowed_write_paths": ["backend/internal/handlers/", "backend/migrations/", "frontend/src/api/"],
  "forbidden_changes": ["contrato_de_api_sem_versionar", "schema_sem_migracao", "credenciais_em_codigo"],
  "engineering_risk": "breaking_change | additive | none",
  "verification": {
    "unit_test": "<o que valida>",
    "negative_test": "<rejeita payload inválido/não autorizado>",
    "contract_test": "<valida request/response contra o OpenAPI>",
    "command": "<comando executável definido antes de fechar>"
  },
  "acceptance": "<comportamento observável demonstrado por teste automatizado>",
  "passes": false
}
```

- **Migrar o backlog existente** sem perder histórico: cada item atual ganha os campos novos (vazios com justificativa onde não se aplicam, nunca omitidos em silêncio).
- Fases do roadmap P00–P15 viram **features** (ou grupos de features) com `passes`. Detalhar só H/B atual e **P00**; as demais ficam como roadmap com critério de saída (autenticação, domínio principal, faturamento etc.) até haver informação suficiente.
- `P00`: scaffold do monorepo (Go + React), CI mínimo, schemas e health-check (`make doctor` ou equivalente).

### 4.3 Rastreabilidade

`scripts/harness/trace.py` **gera** `docs/harness/traceability.csv` a partir de `requirements.md`, `feature_list.json` e dos testes vinculados. Colunas: `requirement_id, phase_id, feature_id, api_spec_path, code_symbol, test_id, ci_run_id, release_id, status, evidence_path`. Campos não aplicáveis ficam vazios **com justificativa**. Cobertura textual de requisito não conta como evidência de comportamento. O CSV é gerado, não editado.

---

## 5. Gates → onde entram no kit

| Gate do plano React+Go | Onde roda no kit |
|---|---|
| G-SPEC (plano concreto: requisitos, contrato, orçamento, aceite) | pré-trabalho do worker + `check-fast` valida o item do `feature_list.json` |
| G-CODE (testes, lint, revisão do diff) | `check-fast` antes do commit; `reviewer` de contexto limpo |
| G-CONTRACT (schema, sem breaking não versionado, cliente sincronizado) | `check-full` + CI |
| G-QUALITY (cobertura, performance no orçamento, a11y) | `check-full` + CI |
| G-DEPLOY (staging, smoke, e2e) | gate de release (K8) |
| G-RELEASE (notes, rollback, aprovação, observabilidade) | gate de release (K8) |
| G-HAR (harness funciona: executa, detecta erro, retoma) | critérios de B4 |

Regra: `passes: true` só com `check-full` verde. Aprovação automática registra `review_mode=automated` + comando + limitações; **não** converter verificação automática em "humano aprovou". Decisão material indeterminada (mudar contrato público, remover dado de usuário) → perguntar ao responsável do produto.

---

## 6. Fase B3 — Contrato primeiro e hook de `allowed_write_paths`

1. Criar (ou adotar, se já existir) `docs/contracts/openapi.yaml` e o pipeline de codegen do cliente TS; ligar ao G-CONTRACT.
2. **Hook PreToolUse de escopo:** ler a feature corrente (`passes: false`, a de menor ordem) do `feature_list.json` e **negar escrita fora de `allowed_write_paths`**, com mensagem instrutiva ("este arquivo não pertence ao escopo de <id>; atualize o plano ou abra outra feature"). Sintaxe do hook no Codex: `[VERIFICAR suporte]`; se o Codex não suportar hooks equivalentes, implementar o mesmo gate como verificação em `check-fast` (diff vs `allowed_write_paths`) e registrar a limitação em `capabilities.json`.
3. Hook de migrações (3.3) e de segredos em código (`credenciais_em_codigo`): bloquear padrões óbvios; segredos permanecem fora de alcance (`.env` negado).
4. **Paralelismo liberado somente** depois do contrato congelado: backend e frontend em features com paths disjuntos (garantidos pelo hook), integração serial. Máximo 3 subagents simultâneos, dentro do limite real da sessão `[VERIFICAR]`.

---

## 7. Papéis e agentes (sem duplicar orquestração)

| Papel do plano React+Go | No kit |
|---|---|
| Principal | O próprio worker do kit (uma unidade de trabalho por sessão) |
| `backend-engineer` (Go) | Adaptador em `.claude/agents/` (+ equivalente Codex `[VERIFICAR]`); um executor por tarefa |
| `frontend-engineer` (React) | Idem; **consome o contrato**, não inventa endpoints |
| `security-auditor` / `qa-engineer` | Variações do `reviewer` de contexto limpo (só vê diff + descrição) |

Se já existirem `.claude/agents/*.md`, transformá-los em contratos autocontidos e prefixar em caso de colisão de nomes. Cada handoff inclui: objetivo, IDs, documentos necessários, commit inicial, paths autorizados, comandos de validação, orçamento e condição de parada. Não carregar o código-base inteiro no contexto.

---

## 8. Fase B4 — Ensaio de aceitação (feature de brinquedo)

Em **branch/diretório temporário**, sem tocar o backlog real. Duas tarefas: endpoint Go com uma regra simples + tela React que o consome. Regra sugerida: "um item só pode ser marcado como concluído se a data de vencimento já passou ou é hoje" (igualdade explícita; fixtures: válido, inválido, fronteira).

1. Escrever expectativas **antes** do código; o plano da tarefa deve conter teste negativo (um plano deliberadamente sem teste negativo deve ser barrado por G-SPEC).
2. Implementar o caminho correto (handler + validação + componente) e verificar o comportamento.
3. Em cópia descartável, remover a validação de negócio → `check-full` **deve reprovar**. Guardar o log da falha esperada; descartar a cópia defeituosa.
4. Interromper entre tarefas, abrir sessão nova e **retomar só pelo disco** (`progress.md`, `feature_list.json`, git log); sem repetir tarefa concluída.
5. Renomear um campo do contrato → o teste de contrato **reprova** até o cliente TS ser regenerado; evidência da versão anterior não aprova a nova.
6. Tentar escrever fora de `allowed_write_paths` → hook/gate nega com mensagem útil. Tentar editar migração aplicada → bloqueado.
7. Exportar `traceability.csv` e o relatório, distinguindo **passagem / falha esperada / pendência**. Medir duração/custo se disponível; desconhecido permanece desconhecido.

---

## 9. Versionamento e upgrade do kit

- Alinhar a inconsistência: o documento do kit chama-se v2.1, mas conteúdo e `kit_version` dizem 2.0.0. Decidir a versão correta, atualizar `VERSION`, `CHANGELOG.md` e `.harness/kit-version`.
- Registrar esta adaptação no `CHANGELOG.md` do kit como **nova versão minor** (módulos `stack-go`, `stack-react-ts`, `api-contract`, `db-migrations`, `frontend-quality`, `release` e perfil `web-saas`).
- `harness_upgrade.py` deve mostrar o diff de módulos do projeto vs kit e **não** sobrescrever personalizações sem merge.
- Duas "segurança" distintas, em arquivos separados: `docs/harness/security.md` (segurança **do agente**: trifecta, Regra dos Dois) e `docs/harness/app-security.md` (segurança **do app**: authn/authz, segredos, dependências auditadas).

---

## 10. Entregáveis esperados

- `docs/harness/adaptation-discovery.md` (B-1) e `docs/harness/decisions.md` atualizado
- `harness.yaml`, `.harness/modules.lock`, `.harness/kit-version` atualizados
- Módulos novos instanciados + `scripts/check-fast.sh` / `check-full.sh` adaptados
- `docs/protocol/constitution.md`, `docs/protocol/requirements.md`
- `feature_list.json` migrado ao novo schema (histórico preservado)
- `scripts/harness/{check.py,trace.py,verify.py}` e `docs/harness/traceability.csv` (gerado)
- `docs/contracts/openapi.yaml` + codegen + G-CONTRACT no CI
- Hooks/gates de escopo, migrações e segredos (ou fallback em `check-fast`, documentado)
- `docs/harness/capabilities.json` com o que o Codex **realmente** suporta
- `docs/harness/ADAPTATION-VERIFICATION.md`: comandos, logs, exit codes e hashes do ensaio B4

## 11. Critério de aceite da adaptação

A adaptação está pronta quando o harness consegue: **(a)** conduzir uma tarefa de código Go+React dentro do escopo autorizado; **(b)** detectar erro de teste *e* quebra de contrato de API; **(c)** bloquear escrita fora do escopo e edição de migração aplicada; **(d)** retomar numa sessão nova só pelos arquivos persistidos; **(e)** gerar rastreabilidade a partir de uma única fonte de progresso. TOML/YAML parseável, diretórios criados ou checklist preenchido isoladamente **não bastam**.

Se o Codex ou alguma ferramenta necessária estiver indisponível, concluir contratos e verificadores independentes e registrar B-etapas como **bloqueadas ou parciais**; não declarar fallback manual como aprovado.

## 12. Fora de escopo (por enquanto)

Instalar GSD Core; dashboards de agentes; catálogo universal de skills; infraestrutura distribuída; detalhar P01–P15 além de critérios de saída; qualquer fase de produto antes de B4 aprovado.
