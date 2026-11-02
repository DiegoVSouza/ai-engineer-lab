# Plano de correção dos rótulos de status e do que falta (2026-11-02)

Origem: mapeamento dos selos dos 8 cards do portfólio (`projects/p07/src/content/caseIndex.ts`) contra os `feature_list.json` de cada projeto, as evidências em `artifacts/evidence/` e o site no ar. Este plano **não executa nada**. Cada fase abaixo vira `SPEC.md` + `PLAN.md` + `VERIFY.md` no projeto dono antes de qualquer código (AGENTS.md, regra 1).

## Execução em 2026-11-02 (atualizado durante a rodada)

Decisões do dono: 1=C, 2=A, 3=A, 4=A, todos os "go" autorizados, Turnstile já configurado, FPS fica `PENDING`.

Feito e com evidência:
- **D15 (novo):** o CI hospedado do P07 estava vermelho no commit publicado (`143ef9c`) e o gate local também. Eram 5 testes e2e escritos para o layout antigo da home, mais uma corrida no teste do menu. Corrigidos sem afrouxar o contrato (commit `54d196e`). Gate completo do P07: exit 0, unit 73, e2e 50.
- **D1/D2/D3:** P05 `demo-live-v1` e P06 `console-design-system` atualizados. Console: e2e na stack real em P06 `7898c8a` passou (3 passou, 1 pulado por desenho) e a renovação silenciosa do token passou em 4,1 min. O console **não** está no Pages por decisão do dono (roda no Fly). P07 está no ar; o selo não diz mais "não publicado".
- **D5:** P01 ligado a uma execução de 119 testes em modo fake; `framework-quality-metrics` registrado como `PENDING`.
- **D6/D10:** catálogo cobre P00 a P08 e o lab; selos derivados do catálogo (`src/content/seal.ts`); `status-truth.test.ts` (vermelho antes, verde depois).
- **D8 (opção C):** quatro features do P05 viraram `PASS_KEYCLOAK_ON_FLY; THIRD_PARTY_IDP_PENDING`. `durable-authorization-snapshot` e `mcp-external-token-introspection` não foram mexidas: a evidência na Fly não cobre lease de 15 min nem revogação de job na fila.
- **D9:** P00 `local-services-and-hosted-ci` dividido em CI hospedado (verde) e e2e de serviços locais (`PENDING`).
- **F4.12:** trace de uma triagem real no Jaeger da Fly (60 traces, 287 spans, `agent.triage`, 4 `llm.inference`, 3 chamadas MCP), sem chave de conteúdo. Métricas de produção seguem `PENDING`.
- **F4.13 (opção A):** adaptador no P05 (`demo_live.py`): cada recibo liquidado reporta os tokens reais ao `ExecutionLimits`. TDD, `check_fast` exit 0. **Ainda não implantado na Fly.**
- **F4.14 (opção A):** `P04-RAG` removido do P04 com ADR em `decisions.md`; execução do P04 na Fly registrada (`202`, tarefa `done`).
- **D12 (triagem):** os 4 achados de senha são constantes de teste ou mock (`CLIENT_SECRET` de um Keycloak local de teste no P05; um valor de fixture impresso numa mensagem de asserção no P01). Nenhum segredo real.
- Stack da Fly foi acordada uma vez (61 s), usada e desligada de novo (`artifacts/evidence/fly/status-truth-session/`).

Segundo defeito real achado pelo CI hospedado: "Back to the surface" aterrissava na estação anterior em 3D (scroll 2080, estação em 3303). Corrigido em `9ad435e` (`SceneHost.tsx`), com o gate completo verde (unit 73, e2e 50).

Publicado nesta rodada (autorizado): push dos 10 repositórios, CI hospedado verde em todos (P07 vermelho em `f2efce2`, verde em `bd1d3b1`), deploy do portfólio no Pages com árvore limpa, adaptador do P05 na Fly com uma run live depois do deploy. Stack da Fly desligada ao fim.

Medido: Lighthouse no site no ar, 5 execuções cada: móvel mediana de performance 83 (LCP 1985 ms, TBT 613 ms), desktop 85 (LCP 481 ms, TBT 356 ms); acessibilidade, boas práticas e SEO 100 em todas. Os números de 96 reportados antes eram uma execução sortuda.

Não feito, com causa (detalhe em `projects/p07/.planning/phases/006-status-truth/VERIFY.md`):
- Avaliação de qualidade de modelo: o P00 controla a campanha e o ledger; uma rodada paralela contornaria esse contador.
- Rotação das senhas demo: a API admin do Keycloak está desligada na imagem pública, e as senhas são publicadas de propósito em `/api/status`. Precisa de decisão sua.
- Teste do Turnstile de ponta a ponta: um desafio humano não é automatizável; as chaves estão ativas (`startAvailable: true`).
- E2E público 2 de 3: a rodada 1 falhou por ruído de console (`fetch('data:,')` bloqueado pela CSP, provável script do Turnstile). Não mexi na CSP nem no teste sem decisão sua.
- Menu cobrindo parte do rodapé no fim da página (visto em `home-3d.png` a 1280x720), índice de metrô no celular, símbolo herói nas páginas de caso, FPS em aparelho real, SCENE-005.
- Avaliação de segurança D12: os 4 achados de senha eram constantes de teste; allowlist por arquivo exato com motivo (`docs/harness/public-readiness-allowlist.json`).

## 0. Regras que governam a execução

- Evidência = comando, exit code e saída em `artifacts/` do projeto. Sem isso o item fica `incomplete` ou `PENDING` (regras 4 e 5).
- Cada projeto tem Git próprio e só edita o próprio `allowed_write_paths`. `harness-kit/` não é tocado (regra 3).
- Commit local atômico `type(scope): imperative English description`, depois de revisar o staged diff. **Push, deploy, mensagem externa e run live acima do teto continuam exigindo autorização explícita** (regra 9).
- Teto de modelo USD 10 e teto Fly USD 5 valem. Os contadores já gastos entram no cálculo; não reiniciam por fase nova.
- Teste vermelho é sinal: corrigir a causa, não relaxar o teste (regra 6).

## 1. Diagnóstico (o que está errado e por quê)

| ID | Problema | Fonte | Tipo |
| --- | --- | --- | --- |
| D1 | Selo P05+P06 diz "smoke live pendente", mas há smoke live com `llm_mode: live` e deploy no Fly | `p05/docs/harness/feature_list.json` `demo-live-v1` (`LIVE_SMOKE_PENDING; FLY_DEPLOY_PENDING`) contra `artifacts/evidence/fly/p05-live-smoke.txt`, `web-deploy.txt` | rótulo velho |
| D2 | P06 `console-design-system` ainda `REAL_STACK_E2E_PENDING; PAGES_DEPLOY_PENDING`, e o limite cita "P05 na 0.4.4" (hoje 0.4.5) | `p06/docs/harness/feature_list.json`, `p07/src/data/projects.ts` linha 126, `fly/console-deploy-006/` | rótulo velho |
| D3 | Selo P07+P08 diz "ainda não publicado", mas `diego-portfolio-ai.pages.dev` responde 200 e há e2e público | `W2-W3-status.md`, `artifacts/evidence/pages/*.json` | rótulo velho |
| D4 | `p07/docs/harness/progress.md` não registra o deploy nem as fases 003 a 005 | `progress.md` | registro incompleto |
| D5 | P01 mostra "verificado offline" com 6 de 7 features `claimed` e sem campo `evidence` | `p01/docs/harness/feature_list.json` | afirmação sem prova no catálogo (há evidência em `p01/artifacts/evidence/`, só não está ligada) |
| D6 | Selo do Lab/P08 ("processo em uso, resultado por projeto") não é um status; P07 e P08 não estão no catálogo (`meta` só tem p00 a p06) | `caseIndex.ts`, `catalog.generated.json` | selo vago e catálogo incompleto |
| D7 | P04 "sem execução em nuvem" pode estar velho: existem `fly/p04-redis-queue-acceptance.txt` e `p04-remote-build.txt` | `fly/` | a confirmar |
| D8 | P05 tem 8 features `partial` com `INCOMPLETE_EXTERNAL_IDP_*`, mas já existe Keycloak 26.8.1 real no Fly com `oidc-acceptance.txt` e `mcp-oidc-acceptance.txt` | `fly/` | possível fechamento por evidência |
| D9 | P00 `local-services-and-hosted-ci` está `incomplete`, mas o CI hospedado ficou verde nos 9 repositórios | `W2-W3-status.md` | possível fechamento por evidência |
| D10 | Os selos são texto escrito à mão e não derivam das features. Nada impede que voltem a divergir | `caseIndex.ts` | causa raiz de D1 a D3 |
| D11 | Texto "publicado" no selo do P00 é ambíguo (publicado o relatório ou o projeto?) | `caseIndex.ts` | redação |
| D12 | Auditoria pública: 4 `assigned_password` (P05 `scripts/check_keycloak_oidc.py` linhas 16, 23, 25; P01 `red-legacy-boundary.txt:104`), 2 em wheelhouse, e caminho local do usuário em 16 arquivos do lab e 10 do P00 | `audit-w3-final.json` | higiene, não verificado |
| D13 | Último deploy do portfólio saiu com árvore suja (`dirty: true`) | `artifacts/evidence/pages/portfolio-20261102T102556.json` | rastreabilidade |
| D14 | Três commits do P08 sem trailer `Co-Authored-By` (já enviados) | `W2-W3-status.md` | nota, **não reescrever histórico** |

## 2. Fases

### F0. Intake e spec (sem código de produto)

1. Abrir `projects/p07/.planning/phases/006-status-truth/` com `SPEC.md`, `PLAN.md`, `VERIFY.md`. Requisitos: STAT-001 (todo selo deriva de feature com evidência), STAT-002 (catálogo cobre P00 a P08), STAT-003 (selo contradiz feature falha o build).
2. Para P01, P04, P05, P06: uma mini-fase `status-reconcile` em cada `.planning/phases/` com `allowed_write_paths` = só `docs/harness/feature_list.json`, `docs/harness/progress.md`, `artifacts/evidence/status-reconcile/`.
3. Registrar em `docs/harness/decisions.md` do P07 que a regra de selo muda de texto manual para derivado.

Saída: três arquivos por fase. Gate: `sdd-plan-check` do harness.

### F1. Verificar o estado atual (somente leitura, e um smoke se preciso)

Objetivo: confirmar cada D antes de mudar rótulo. Nada de afirmar por memória.

1. Reler o conteúdo de `fly/console-deploy-006/e2e-fly-attempt3.txt`, `smoke.txt`, `status-final.txt` para dizer se o e2e na stack real passou (fecha D2).
2. Reler `fly/p04-redis-queue-acceptance.txt` e `p04-remote-build.txt` (D7).
3. Reler `fly/oidc-acceptance.txt` e `mcp-oidc-acceptance.txt` e comparar com o que cada feature P05 `INCOMPLETE_EXTERNAL_IDP_*` exige no VERIFY da fase (D8). Se o IdP no Fly for o mesmo Keycloak do próprio lab, decidir por escrito se conta como "externo". Essa decisão é **do dono** (ver seção 4).
4. Conferir o CI hospedado atual dos 9 repositórios (`gh run list`, só leitura) e salvar a saída (D9).
5. Rodar `curl` nas duas URLs Pages e no `/api/status` do portfólio; salvar status e hash do commit servido (D3, D13).
6. Só se o item 1 não bastar: um smoke live do P05 (uma triagem, custo de ordem USD 0,0003 pela última medição; registrar o custo real). **Precisa de "go" porque acorda a stack e gasta modelo.**

Saída: `projects/p07/artifacts/evidence/status-truth/F1-*.txt` e um quadro D-por-D com `confirmado`, `refutado` ou `precisa de decisão`.

### F2. Corrigir a fonte de verdade (feature lists)

Em cada repositório, um commit por item, com a evidência apontada no campo `evidence`.

| Projeto | Mudança | Pré-condição |
| --- | --- | --- |
| P05 | `demo-live-v1`: trocar `LIVE_SMOKE_PENDING; FLY_DEPLOY_PENDING` por `PASS_LIVE_SMOKE; FLY_DEPLOYED` com `evidence` = `p05-live-smoke.txt`, `p05-live-deploy-2.txt`. Manter qualquer pendência real (qualidade do modelo) | F1.6 ou `p05-live-smoke.txt` bastar |
| P05 | Features `INCOMPLETE_EXTERNAL_IDP_*`: fechar só as que a evidência F1.3 provar, o resto continua `partial` | decisão do dono sobre "externo" |
| P06 | `console-design-system`: atualizar para o que F1.1 provar; limite do `projects.ts` sai de "0.4.4" para a versão realmente verificada, ou vira texto sem versão fixa | F1.1 |
| P01 | Ligar as 6 features `claimed` à evidência existente (`check-full.txt`, `core-tool-safety`, `dispatch-process-recovery-013`, etc.), com `status` explícito. Onde não houver prova, rodar o teste e salvar saída | F1 |
| P04 | Atualizar para o que F1.2 provar; se houver aceitação em nuvem, criar feature própria com a evidência | F1.2 |
| P00 | `local-services-and-hosted-ci`: fechar com a saída do CI verde (F1.4) e com `doctor.md` atual | F1.4 |
| P07 | Criar `docs/harness/feature_list.json` real (build, i18n, a11y, e2e público, cena 3D, cost guard) e registrar deploy e fases 003 a 005 em `progress.md` (D4) | F1.5 |
| P08 | Idem para `colagem-ui` (versão atual, contraste, layout de fluxo 0.4.4) | — |

Cada mudança passa por `python scripts/check_fast.py` do projeto e salva a saída em `artifacts/evidence/status-reconcile/`.

### F3. Derivar os selos (causa raiz D10)

No P07 (`allowed_write_paths`: `scripts/catalog.mjs`, `src/data/`, `src/content/caseIndex.ts`, testes):

1. `scripts/catalog.mjs` passa a ler `feature_list.json` de P00 a P08 (hoje só p00 a p06) e a gerar, por caso, `sealKind` e contagem por estado. Continua só lendo arquivo irmão, sem importar código (regra do `AGENTS.md` do P07).
2. `caseIndex.ts` deixa de ter `label` manual. Cada selo vem de uma tabela de regras:
   - `full`: nenhuma feature `open`/`partial`/`claimed`.
   - `partial`: lista os eixos pendentes, tirados dos sufixos `*_PENDING` e `INCOMPLETE_*` do próprio `status`.
   - `fail`: existe feature `FAIL_*`.
   - Sem feature: selo `none` com a palavra "sem registro", nunca texto livre.
3. Teste `src/status-truth.test.ts` (vermelho antes, verde depois): falha se um selo disser "publicado/no ar" sem registro de deploy em `artifacts/evidence/pages/`, se disser "pendente" sem feature pendente que o justifique, ou se P07/P08 não estiverem no catálogo.
4. Redação revisada (PT e EN), por exemplo:
   - P00: "reprovado provisoriamente, relatório publicado" (D11).
   - P07+P08: "no ar, verificado com e2e público" quando F2 comprovar; pendências reais (FPS em aparelho real, Turnstile) listadas.
   - Lab/P08: troca "processo em uso, resultado por projeto" por um texto derivado (por exemplo, quantos projetos têm gate verde e quantos têm pendência), ou remove o selo e mostra só o grupo.
5. Regenerar `catalog.generated.json`, rodar `python scripts/check_full.py` e o e2e local. Salvar saídas.

### F4. Implementar o que ainda falta

Ordem por risco e por dependência. Marcadores: **[go]** precisa de autorização, **[dono]** depende de você, **[livre]** posso fazer sem autorização nova.

| # | Item | Projeto | Condição de pronto | Marcador |
| --- | --- | --- | --- | --- |
| 1 | Turnstile: criar widget e preencher `TURNSTILE_SITE_KEY` e `TURNSTILE_SECRET`; sem isso `startAvailable:false` | P07, Cloudflare | `/api/status` com `startAvailable:true`; e2e do fluxo de acordar | [dono] (token com `Turnstile Sites Write`) |
| 2 | Lighthouse mobile com mediana de 5 execuções, não uma só | P07 | JSON das 5 execuções e mediana salva; nota corrigida no catálogo | [livre] |
| 3 | SCENE-005: FPS em celular real | P07 | medição de pelo menos um aparelho, modelo e navegador registrados; senão `PENDING` | [dono] (aparelho) |
| 4 | Teste do olho semicerrado em home e demo (só o caso foi refeito) | P07 | capturas antes e depois em `portfolio-w7b/` | [livre] |
| 5 | Índice de linha de metrô no celular; símbolo de cada projeto como herói na página do caso | P07 | spec nova na fase 006 ou 007, teste e2e em 360 px | [livre] |
| 6 | Estilhaço opção B | P07 | decisão do dono; se B, ~1 dia, contrato em `scenes.json` | [dono] |
| 7 | Preços Fly no cost guard: conferir na página oficial e trocar `PENDING` por valor com fonte e data | P07 `worker/cost-guard` | teste do guard com os valores novos | [livre] (leitura de página pública) |
| 8 | Tokens da Cloudflare expiram em 90 dias (criados em 2026-10-31); registrar lembrete de rotação e procedimento | P07 docs | runbook em `docs/harness/` | [livre] |
| 9 | Rotação das senhas das contas demo e saída do `supportops-lab-web` ou decisão registrada de mantê-lo | lab `ops/` | evidência em `artifacts/evidence/fly/` | [go] (mexe em produção) |
| 10 | Bump de versão e wheel do P05 (0.4.5 com o que mudou) e propagação do lock ao P06 | P05, P06 | CI hospedado verde | [go] (push) |
| 11 | P05 `real-model-evaluation` e P00 `funded-replacement-development`: avaliação com cassette ou run live autorizado, medindo qualidade, nunca fixture | P05, P00 | cassette rastreável ou run registrado; o custo entra no contador dos USD 10 | [go] (gasta modelo) |
| 12 | P03 `production-metrics`: exportar traces e métricas da stack real (já há `jaeger-flycast`) e salvar prova | P03, lab `ops/` | trace da triagem live visível no coletor, sem conteúdo de usuário | [go] (acorda stack) |
| 13 | P02 `token-limit-in-agent-path`: o P02 não é dono de runtime. Ou um adaptador real no P05 reporta uso via `ExecutionLimits.consume`, com teste, ou decisão em `decisions.md` de que está fora do escopo e a feature sai | P02, P05 | teste de contrato ou ADR curta | [dono] (escolher o caminho) |
| 14 | P04-RAG: não há corpus nem protocolo de tenant no P04. Decidir: mover a responsabilidade para o P05 (que já tem RAG) e remover a feature do P04 | P04 | ADR curta + feature atualizada | [dono] |
| 15 | P04 e P03 `PRODUCTION_*_PENDING`: aceitação em produção do export de trace | P03, P04 | evidência de F4.12 | [go] |

Cada item gera: teste vermelho antes (quando houver código), implementação, `check_fast`, commit atômico, evidência salva e linha em `progress.md`.

### F5. Higiene e segurança

1. Triagem dos 4 `assigned_password`: abrir cada linha e classificar. Se for credencial de teste, mover para constante nomeada `TEST_ONLY` ou variável de ambiente; se for real, **parar e avisar**, trocar o segredo e só então tratar o histórico (que exige sua autorização, regra 9).
2. Adicionar à `public_readiness.py` uma allowlist versionada com motivo, só para os 2 achados de wheelhouse. A allowlist não pode cobrir pasta inteira.
3. Trocar o caminho local do usuário por um marcador nas evidências futuras (um filtro no gravador de evidência). **Não reescrever evidência antiga**; registrar a limitação.
4. D14 vira nota em `failures.md`; histórico não é reescrito.

### F6. Publicação

1. Árvore limpa antes do deploy: commitar ou descartar os PNGs modificados de `p07/artifacts/evidence/portfolio-w7*` (`dirty` tem que sair `false`).
2. `ops/pages/deploy.ps1` em dry-run primeiro; deploy real e `git push` **só com seu "go"**.
3. Rodar o e2e público 3 vezes seguidas, como já foi feito, e salvar.

### F7. Verificação final e critério de aceite

- `check_full.py` verde em P01, P04, P05, P06, P07, P08 e `check_fast.py` em P00, P02, P03, cada saída em `artifacts/`.
- `status-truth.test.ts` verde: nenhum selo sem feature, nenhum "publicado" sem registro de deploy, P07 e P08 no catálogo.
- Lighthouse por mediana, e2e público 3 em 3.
- Todo `PENDING` que sobrar tem causa e dono escritos. Nenhum número novo sem run registrado.
- Quadro final D1 a D14 com `corrigido` + commit, `aceito como pendente` + motivo, ou `bloqueado` + quem destrava.

## 3. Ordem e dependências

```
F0 -> F1 -> F2 -> F3 -> F7
          \-> F5 (paralelo, independe de F2)
F4 itens [livre] podem andar em paralelo a F2 e F3
F4 itens [go] e [dono] ficam em fila até autorização
F6 depende de F3 e dos itens [livre] de F4
```

## 4. Decisões e autorizações que preciso de você

1. O Keycloak do Fly conta como "IdP externo" para fechar as features do P05, ou "externo" significa um provedor de terceiros fora do nosso controle?
2. P02 token-limit (F4.13): adaptador real no P05 ou fora do escopo?
3. P04-RAG (F4.14): mover para o P05 e remover do P04?
4. Estilhaço B (F4.6): sim ou não?
5. Go para: smoke live de confirmação (F1.6), acordar a stack para trace de produção (F4.12), avaliação de qualidade com modelo (F4.11, custo a estimar antes), rotação de senhas e mudança no `supportops-lab-web` (F4.9), push e deploy (F6).
6. Do seu lado: widget Turnstile (F4.1) e um celular para FPS (F4.3).

## 5. O que este plano não cobre

- Reescrever histórico Git (D12, D14), por causa da regra 9.
- Qualquer número de custo ou qualidade: nenhum existe sem run, então continua `PENDING`.
- Alteração em `harness-kit/`, que exige fase própria e validação em dois projetos.
