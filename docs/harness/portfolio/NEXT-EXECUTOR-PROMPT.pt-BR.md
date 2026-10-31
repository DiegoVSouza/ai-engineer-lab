# Prompt de execução — portfólio real do Diego (2026-10-31)

> **Antes de enviar, decida uma coisa (só você pode):** marque na seção "Autorizações" o que vale nesta rodada. Por padrão, o executor faz só o trabalho local, sem push, deploy nem chamada live. Se quiser mais, troque `NÃO` por `SIM` na linha correspondente. A pergunta sobre o `newsAR` e os repositórios em destaque está na mesma seção.

--- INÍCIO DO PROMPT ---

Continue a construção do portfólio em `C:\estudo\Golpe\lab`. Execute no mesmo turno até o limite autorizado; não entregue só leitura ou plano. Este prompt é autocontido: você não tem acesso à conversa que o gerou.

## Objetivo

Portfólio de **Diego Vieira Gonçalves de Souza, AI Engineer**, em React, seguindo `DESIGN_SYSTEM_COLAGEM_URBANA_NOITE.md`. Os projetos do lab são os projetos do portfólio. Um recrutador entende o perfil na primeira tela, e um engenheiro aciona o modelo real, vê cada passo, abre o código no commit exato, roda o teste e lê a documentação.

## Leitura obrigatória antes de qualquer escrita

1. `AGENTS.md` (regras do lab; valem sobre este prompt em caso de dúvida) e `harness/skills/lab-commits/SKILL.md`.
2. `projects/p07/.planning/phases/003-real-portfolio/SPEC.md` e `PLAN.md`: **a spec é a fonte de verdade do produto**. Etapas W0 a W11 estão lá.
3. `docs/decisions/ADR-001-frontend-on-cloudflare-pages.md` e `ADR-002-portfolio-as-product.md`.
4. `docs/harness/public-readiness.md`: resultado da auditoria.
5. `docs/knowledge/portfolios-de-ai.md`: pesquisa.
6. `docs/harness/frontend-platform/`: `SPEC`, `PLAN`, `VERIFY`, `rollback.md`.
7. `DESIGN_SYSTEM_COLAGEM_URBANA_NOITE.md`.
8. `AGENTS.md`, `docs/harness/progress.md` e `docs/harness/feature_list.json` de cada projeto antes de editá-lo.

## Estado verdadeiro no momento deste prompt

| Repo | HEAD | Observação |
| --- | --- | --- |
| lab | commit deste prompt | Remoto privado `ai-engineer-lab` |
| P00 | `bce4d20` | Privado, 116+ commits sem push. `.git` pertence ao usuário do sandbox do Codex |
| P01 | `9af1dbc` | Privado, 80+ sem push. Clone limpo falha |
| P02 | `06dbd3e` | Privado, 29+ sem push |
| P03 | `ea0bf50` | Privado, 49+ sem push |
| P04 | `a97f4ff` | Privado, 87+ sem push |
| P05 | `4b78b9f` | Privado, 63+ sem push. Clone limpo falha |
| P06 | `1994b4c` | Sem remoto. Clone limpo falha |
| P07 | último commit: handoff | Sem remoto. Site atual é provisório; a spec o substitui |
| P08 | `52ed222` | Sem remoto. `colagem-ui` 0.3.0 |

Pronto e verificado localmente: `colagem-ui` (P08) com contraste testado; P06 e P07 sobre o pacote; P05 com CORS por allowlist (`CORS_ALLOWED_ORIGINS`); `ops/stack/idp_clients.py` com várias origens; `ops/pages/deploy.ps1` em dry-run por padrão; MIT em todos os repos; auditoria de segredos limpa.

Não existe ainda: nada público, nenhum deploy no Cloudflare, demo live, conteúdo real do portfólio, rotas pré-renderizadas. O Fly segue em `LLM_MODE=fake`.

Hoje: Wrangler autenticado com `pages (write)`, plugin Cloudflare instalado, Docker Desktop disponível, `fly auth whoami` responde.

## Decisões do dono (não reabrir)

- Python no backend. **Sem Go.**
- Fronts no Cloudflare Pages, APIs no Fly. Projeto `diego-portfolio-ai`; console `supportops-console`.
- **Demo sempre em live.** Máquinas com autostop, sempre prontas para live. Sem fake para visitante.
- Usar as 4 chaves Groq até onde as organizações gratuitas permitirem. **Teto de USD 10 em modelos**, por precaução.
- **Teto de USD 5 no Fly.**
- React dinâmico: pré-render, hidratação e Pages Functions. Sem SSR de página inteira.
- Licença MIT. Título "AI Engineer", em inglês.
- Dados pessoais vêm de `Diego_Souza_AI_Engineer_EVT_PT.docx`, na raiz. **Esse arquivo nunca entra no Git, e o telefone nunca entra no site.** Leia com `pandoc <arquivo> -t plain --wrap=none`.
- Pode dizer que foi construído com um harness que aplica as melhores práticas de engenharia de AI. Venda ao máximo, dentro da regra de evidência.

## Autorizações desta rodada

| Ação | Autorizado |
| --- | --- |
| W1b, W2, W5, W6, W7, W9: trabalho local, commits locais, testes, Docker local | **SIM** |
| W3: push, criar repos, tornar público | NÃO |
| W4: smoke live do P05 dentro do teto (código offline do W4 é SIM) | NÃO |
| W8: deploy no Fly, secrets, Cloudflare, Turnstile, cost guard em produção | NÃO |
| W10: publicar o portfólio | NÃO |

Destacar o `newsAR` e outros repos públicos: **PENDENTE**. Deixe marcado como `PENDING` no conteúdo.

Sem `SIM` explícito, não execute. Uma autorização vale para o que está escrito, não para o que parecer vizinho (regra 9 e seção de continuidade do `AGENTS.md`). Prepare diff e dry-run do que estiver bloqueado e siga para o próximo item autorizado.

Permanecem sempre em vigor: nada de gastar o orçamento protegido do P00 (84 holdout, 60 confirmação), nada de chamada live sem autorização, nada de imprimir segredo, nada de `--no-verify`, nada de enfraquecer teste. Se achar um segredo: pare, relate, não publique.

## Ordem de trabalho

Siga o `PLAN.md`. Detalhe do próximo passo:

### W1b — verificar antes de construir

Registre em `docs/harness/portfolio/W1b-findings.md`, com fonte e data:

1. Machines API do Fly: dá para calcular custo sem acordar máquina? Dá para ler estado com token só-leitura? O cost guard é viável?
2. Créditos pré-pagos do Fly: o que a documentação atual diz. Fórum tem relatos conflitantes.
3. Groq: limites reais em `console.groq.com/settings/limits` exigem o dono; termos sobre várias organizações; rate limit por organização.
4. Ordem mínima de wake para o fluxo do demo, e quais apps podem seguir dormindo.
5. Turnstile: origem exata para a CSP só em `/demo/`.

Se algo não puder ser verificado, registre como `PENDING`; não presuma.

### W2 — tornar cada repo clonável e apresentável

**P05: wheels.** `artifacts/packages/.gitignore` contém `*`, então **as 5 wheels de `pyproject.toml` estão fora do Git** (`supportops_ai_toolkit-0.2.0`, `supportops_agents-0.1.1`, `supportops_foundation-1.0.1`, `supportops_obs-0.3.1`, `supportops_async-0.1.4`). Versione exatamente essas cinco, com exceções no `.gitignore`. Confirme os hashes contra `uv.lock`. Mantenha fora os ledgers `.sqlite` e as demais wheels.

**P01: acoplamento com o lab.** `tests/test_accounted_core.py:271` usa `PROJECT.parents[1] / "scripts/harness"`, e a linha 451 referencia `scripts/harness/live_provider_transport.py`. Os scripts `scripts/diagnostic_operation.py`, `revalidation_operation.py`, `reviewed_operation_027.py` e `second_diagnostic_operation.py` também importam esse módulo. Escolha a solução que preserva o que o teste prova: copiar o módulo com origem e hash registrados, ou marcar como teste de integração do lab com skip explícito e motivo quando o lab não existir. **Skip silencioso é proibido.** Confira também os outros testes que falharam: foram 1 falha e 19 erros no total.

**P06: CRLF.** `scripts/contract-check.mjs:30` compara bytes. Normalize fim de linha na comparação. Adicione `.gitattributes` se fizer sentido e mantenha o teste de que cliente desatualizado falha.

**CI de todos.** Workflows nunca rodaram em runner limpo, e estão errados:

- P06 e P07 (e P08, confira): `python scripts/check_fast.py` chama `npm` sem `setup-node` nem `npm ci`.
- P00 a P05: `python scripts/check_full.py` sem `uv sync`. Veja o que cada gate exige, e separe o que depende de serviços.
- Playwright usa `channel: "chrome"`: instale no runner ou use `chromium` no CI.
- `catalog:check` do P07 cai em `skipped` sem irmãos: mantenha assim.

Rode `python scripts/harness/clean_clone_check.py --base <diretório-vazio-no-scratch>` até passar. Para P00, clone via `git bundle` (ver armadilhas). Teste também em Linux, com container Docker local, porque o CI roda lá.

**HEAD limpo.** Remova do HEAD as 37 wheels de terceiros em `artifacts/evidence/llm-live-readiness/additional-validation-043/` do lab, 52 MB, preservando manifesto e hashes. **Não reescreva histórico.** Arquivos não versionados de P00 a P05 (244 no total) são trabalho anterior: não apague nem versione em massa. Avalie evidência útil caso a caso e relate.

**READMEs.** Cada `README.md` vira case curto: problema, decisão principal, o que foi medido, como rodar, limites, link da documentação. Mantenha `README.pt-BR.md`. Não invente número: copie da evidência.

Gate: `clean_clone_check.py` todo verde, `check_fast.py` em cada repo, `public_readiness.py` sem achado novo (rode com `--secret-file .env artifacts/checkpoints/pre-fly-final-20261023/fly-secrets.json`).

### W4 — código offline do live no P05

Guardas `accounted_guard_required` (`agents/live_groq.py`) e `live refund/approval workflow is not enabled` (`agents/triage.py:171`) ficam até o substituto contabilizado existir. Construa `demo-live-v1` sobre os recibos de `agents/accounted.py`, com ledger persistente em Postgres, fail closed em USD 10, teste de fronteira e concorrência, failover de chaves em 429, e `llm_usage` por passo na API (aditivo: regenere o cliente do P06). Tudo testado em `LLM_MODE=fake` e com transporte falso.

### W5 a W7 e W9 — produto

Conforme a spec. Faça o flagship completo antes dos demais cases. O conteúdo atual do P07 diz "seven projects": substitua. Número de projeto só com registro `Evidence`; dado do CV só em `profile.ts`, rotulado como carreira. Republicar `colagem-ui` 0.4.0 corrige o `UNLICENSED` no tarball usado por P06 e P07. Atualize `sources.lock.json` em ambos.

Copy em inglês e pt-BR, primeira pessoa, específica, sem adjetivo onde cabe número. O CV em inglês é rascunho até o dono revisar.

## Armadilhas conhecidas deste ambiente

- **Heredoc longo no Git Bash falha** com `unexpected EOF`, e nada roda. Use a ferramenta de escrita de arquivos.
- `Path.write_text` no Windows grava CRLF. Use `write_bytes`, e normalize ao comparar.
- **`grep -r`, `du` e Glob na raiz travam**: há `.venv` e snapshots enormes em `projects/*/artifacts`. Busque em caminhos específicos.
- `git clone` local do P00 falha por ownership do `.git`. **Não altere `safe.directory` global.** Use `git bundle create` e clone do bundle.
- Servidor `preview` antigo mascara build novo. Mantenha `reuseExistingServer: false`, e encerre servidores no fim.
- Testes em jsdom: `import.meta.url` não é `file:`. Use `process.cwd()`.
- jsdom não mede contraste. Só o teste em Chrome real prova; no papel, foi ele que achou os defeitos.
- CSP `style-src 'self'` bloqueia `<style>` injetado. Use CSSOM em testes.
- Linhas de `_headers` têm limite de 2.000 caracteres.
- `*.pages.dev` não renomeia.

## Definição de concluído

Sem evidência, é `incomplete`. Cada etapa salva comando, exit code e saída em `artifacts/`, atualiza `VERIFY.md`, `progress.md` e `feature_list.json` do projeto, e faz commit local atômico depois de revisar o diff. Atualize também `projects/p07/.planning/phases/003-real-portfolio/VERIFY.md` e `docs/harness/frontend-platform/VERIFY.md`.

Pare em: três tentativas falhas na mesma falha, segredo encontrado, gasto projetado acima de um teto, ou ação sem `SIM`.

Ao terminar, relate em português ao dono: o que foi concluído com evidência, o que falhou, o que está bloqueado e por quê, e a lista exata de `SIM` necessários para a próxima rodada.

--- FIM DO PROMPT ---
