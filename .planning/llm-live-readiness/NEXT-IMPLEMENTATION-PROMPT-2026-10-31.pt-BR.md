# Prompt de implementação — terminar o produto (2026-10-31)

> Copie e cole a partir de `--- INÍCIO DO PROMPT ---`. As decisões do usuário já estão embutidas; não há nada para preencher.

--- INÍCIO DO PROMPT ---

Termine a implementação do produto em `C:\estudo\Golpe\lab` até ficar usável em produção. Execute no mesmo turno; não entregue apenas leitura, plano ou commit, e não peça outra mensagem "continue". A prioridade é **código funcionando**, não campanha de avaliação.

## Leitura obrigatória antes de qualquer escrita

`AGENTS.md`, `harness/GSD-LITE-PLUS.md`, `harness/skills/lab-commits/SKILL.md`, `README.md`, `docs/knowledge/self-hosted-stack.md`, `docker-compose.yml`, `scripts/stack.py`, `ops/stack/`, `ops/fly/`, `fly/`. Depois `.planning/llm-live-readiness/`: `AUTHORIZATION.md` (seção de 2026-10-31), `STATUS.md`, `WORK.md`. Para o front, leia os três documentos da raiz: `plano-adaptacao-react-go-no-harness-kit.md`, `plano-harness-saas-react-go.md` e `DESIGN_SYSTEM_COLAGEM_URBANA_NOITE.md`. Antes de tocar em cada projeto, leia seu `AGENTS.md`, `harness.yaml`, `docs/harness/decisions.md`, `progress.md`, `feature_list.json`, as fases recentes e o Git **daquele** repositório. Cada `projects/<pid>` tem Git próprio; o Git da raiz ignora `projects/`. Não deduza estado de conversa — confirme nos arquivos.

## Decisões do usuário já tomadas

1. **Produto antes de avaliação.** Avaliação humana, qualidade de modelo, holdout e promoção ficam adiados por decisão do usuário até todo o código estar pronto. Não abra campanha nova de avaliação para "mostrar progresso". Escopos live finitos existem em `AUTHORIZATION.md` e seguem concedidos, mas **não** são a próxima ação.
2. **Falta o front.** Hoje não existe nenhum frontend no repositório: nenhum `package.json`, nenhum diretório `frontend/`/`web/`/`ui/`. A API alvo é a do P05 (`projects/p05/supportops_platform/api/app.py`), com rotas `/v1/tickets`, `/v1/tickets/{id}`, `/v1/tickets/{id}/triage`, `/v1/tickets/{id}/feedback`, `/v1/tickets/{id}/approve`, `/v1/tickets/{id}/refund-approvals`, `/v1/approvals/{id}/decision`, `/v1/tasks`, `/v1/tasks/{id}`, `/healthz`, `/metrics`, autenticada por token Keycloak e escopada por tenant.
3. **Um comando para subir e derrubar, local e Fly.** Local já tem `python scripts/stack.py up` e, desde 2026-10-31, `python scripts/stack.py down` (remove containers e redes desta aplicação Compose; volumes nomeados sobrevivem; `--volumes` descarta dados). O lado Fly tem `ops/fly/deploy.ps1` e `ops/fly/power.ps1 -Action Start|Stop` e precisa alcançar a mesma paridade de um comando, documentada.
4. **Documentar sempre.** Toda entrega atualiza a documentação na mesma tarefa, não depois.
5. **`gossett_backend` está resolvido e fechado.** É de outro projeto do usuário (Compose project `gosset`), nunca usado por este lab, e o bloqueio era falso positivo: contagem 102 → 102 com o mesmo nome em `missing` e `added`, porque o container está em crash-loop e o comparador ainda comparava a string volátil de portas publicadas. Corrigido em `projects/p04/scripts/docker_inventory_identity.py`. **Continua proibido** mutar, parar, remover ou podar `gossett_backend` ou qualquer recurso fora de um namespace de fase comprovadamente seu.

## Fila de implementação

Trabalhe um item por vez, do topo para baixo, em fase SDD própria com ID livre. Antes de código: `SPEC.md` + `PLAN.md` + `VERIFY.md` com 2–4 tarefas, `allowed_write_paths` concretos, `forbidden_changes`, validação, orçamento e condições de parada.

| # | Entrega | Critério de pronto |
|---|---|---|
| 1 | **Validar o que já foi corrigido offline.** `projects/p04/scripts/check_full.py` passou a chamar `service_scenarios.py` via `uv run --locked` (commit `96b5b28`) e o comparador de inventário foi corrigido, mas nenhum gate validou isso ainda. Rode o gate fake isolado do P04 com a preparação de snapshot **corrigida**: o snapshot precisa conter a raiz do lab (`scripts/harness/`, `shared/policies/`, `.runtime/llm-live-readiness/`), não só a árvore do p04 — essa era a segunda causa da falha da fase048. | Gate PASS com `provider_accessed: false`, limpeza de recursos próprios, baseline global inalterado. |
| 2 | **Paridade de um comando no Fly.** Fechar `ops/fly/deploy.ps1` e `ops/fly/power.ps1` para que subir e derrubar sejam um comando cada, com as mesmas garantias do local: nunca tocar app fora do stack, estado de volumes explícito, saída legível, exit code confiável. Documentar lado a lado com o local no `README.md` e no guia em português. | Comandos documentados, `--help`/`-Action` coerentes, sem deploy real executado sem autorização explícita do usuário. |
| 3 | **Frontend.** Seguir `plano-adaptacao-react-go-no-harness-kit.md`, começando pela fase B-1 de descoberta obrigatória (gerar `docs/harness/adaptation-discovery.md` a partir do repo real, não das suposições do documento). Perfil, contrato de API primeiro (OpenAPI do P05), codegen de cliente, orçamento de bundle e `a11y_check`, tema conforme `DESIGN_SYSTEM_COLAGEM_URBANA_NOITE.md`. Entrar no Compose raiz e no Fly como serviço próprio, atrás dos mesmos comandos de up/down. | Front roda no stack local por um comando, consome a API do P05 autenticado por Keycloak, tem teste e verificação de acessibilidade, e está documentado. |
| 4 | **Prontidão de produção.** Revisar health checks, readiness, migrações reversíveis, logs estruturados, métricas, tracing, limites de recurso, política de restart, segredos fora do código e plano de rollback. Registrar o que falta como item concreto, não como texto genérico. | Checklist com evidência por item; nada marcado pronto sem comando, exit code e saída salvos. |
| 5 | **Dívidas abertas.** Remover o debris `35356` da raiz (nome = PID, conteúdo = caminho, sobra de um gate encerrado) em commit `chore` isolado. Criar a entrada ausente em `docs/knowledge/**` descrevendo este programa, conforme o fluxo do `AGENTS.md`. Investigar offline a falha de fixture Git 128 do P00 capturando o stderr, que as tentativas anteriores não imprimiam. | Cada item commitado ou com motivo registrado. |

Itens 1 e 2 destravam o resto e são pequenos; faça-os primeiro. O item 3 é o maior e exige a descoberta B-1 antes de qualquer linha de código de front.

## Laço de execução

Escolha a tarefa executável → implemente → valide em ambiente locked/fake → salve comando, cwd, exit code e saída sanitizada em `artifacts/` do dono → se falhar, registre diagnóstico e contador persistente, corrija a causa raiz e revalide no mesmo turno → revise o diff staged → commit local atômico em inglês via lab-commits → atualize a documentação e o estado → siga para a próxima tarefa.

`max_tries: 3` por falha (tentativa inicial mais duas correções), sem reiniciar contador por sessão, fase ou ID novo. Preserve todo FAIL/INCOMPLETE; nunca enfraqueça asserção, esconda skip nem troque label esperado para passar. Ao esgotar tentativas ou faltar recurso real, registre o bloqueio exato e siga para itens independentes.

Antes de qualquer ciclo Docker: salve identidades e estados de containers, redes, volumes e imagens; valide cache, portas e namespace exclusivo; prove posse antes de limpar. O stack raiz pode estar no ar com dados do usuário — **não** rode `down --volumes` nem pare serviços alheios sem pedir. Preserve volumes anônimos históricos e não presuma gateway do container para o host.

## Limites em vigor

USD 0 pago. Sem upgrade de plano, troca de provedor ou modelo, fallback silencioso, replay de chamada ou gate consumido, liberação de reserva desconhecida, reset de contador, uso de holdout 84 ou confirmação 60. Sem deploy público, push, PR, merge, mensagem externa, dado de cliente, reembolso real, `terraform apply` ou `--no-verify`. Qualquer chamada live fica restrita aos escopos finitos já registrados em `AUTHORIZATION.md` e não é a prioridade desta rodada.

## Relatório final

Reporte por entrega: PASS/FAIL/INCOMPLETE, commits e fingerprints exatos, comandos com cwd e exit code, evidência salva, tentativas e paradas, e o que ficou de fora com o motivo. Não declare "pronto para produção" sem o checklist do item 4 com evidência. Se o host interromper o turno, persista antes o checkpoint, o contador por falha e o próximo comando, e retome daí.

--- FIM DO PROMPT ---
