# Prompt de continuação — llm-live-readiness (2026-10-31)

> **Antes de enviar, decida três coisas** (só você pode): (1) manter ou riscar a atestação do `gossett_backend`; (2) manter ou ajustar os limites finitos da seção "Autorizações"; (3) ler a seção "O que só você pode fechar" e aceitar que a avaliação humana não será feita pelo agente. O resto é copiar e colar a partir de `--- INÍCIO DO PROMPT ---`.

--- INÍCIO DO PROMPT ---

Continue e conclua o trabalho técnico de llm-live-readiness em `C:\estudo\Golpe\lab`. Execute no mesmo turno; não entregue apenas leitura, plano ou commit, e não peça outra mensagem "continue". Encerre somente quando todo item técnico autorizado estiver concluído e validado, ou quando cada item restante tiver evidência atual de uma dependência específica indisponível e não houver nenhuma tarefa independente autorizada sobrando.

## Leitura obrigatória antes de qualquer escrita

`AGENTS.md`, `harness/GSD-LITE-PLUS.md`, `harness/skills/lab-commits/SKILL.md`, depois `.planning/llm-live-readiness/`: `AUTHORIZATION.md`, `STATUS.md`, `WORK.md`, `CONTINUATION-PLAN.md`, `CONTINUITY-2026-10-30.md`, `EXECUTOR-HANDOFF.md` e as fases 040–048. Antes de tocar em cada projeto, leia seu `AGENTS.md`, `harness.yaml`, `docs/harness/decisions.md`, `progress.md`, as fases recentes, o código relevante e o Git **daquele** repositório. Cada `projects/<pid>` tem Git próprio; o Git da raiz ignora `projects/`. Não deduza estado a partir de conversa — confirme nos arquivos e ledgers.

## Estado verdadeiro no momento deste prompt

Fase048 está reconciliada: o gate isolado adicional autorizado para `local-reviewed-operation-040-v1` (P04) **rodou, foi consumido e FALHOU** com exit 1. Limpeza, namespace, labels, hash de saída protegida e o diff completo de inventário Docker passaram; `provider_accessed: false`, `live_operation_invoked: false`, sem replay. Duas causas foram diagnosticadas offline e já estão documentadas: (a) o `prepare-gate.py` daquela fase arquiva só a árvore do p04 e nunca popula a raiz do lab no snapshot, então `test_applied_migration_rechecks_without_reacquiring_campaign_lease` quebra — defeito do script descartável da fase, não do código revisado; (b) `check_full.py` chamava `scripts/service_scenarios.py` com o interpretador global em vez de `uv run --locked`, causando `ModuleNotFoundError: boto3` — **já corrigido** no commit `96b5b28` do p04, ainda **não validado** por nenhum gate.

Contabilidade corrente a confirmar nos ledgers antes de usar: política canônica SHA `f8428a8da06fd551e6a41d3d009db69d1d31c620eda68ef21a02ff1dbcc32cdf`, cap global 4.148, autorização paga USD 0. Visão do provedor: 90 tentativas, conservador 31.991 input / 8.380 output, uma reserva histórica de uso desconhecido. Capacidade operacional reutilizável: **P00 4/10 usadas (6 restam), P02 1/4 (3 restam), P03 1/4 (3 restam), P05 8/8 esgotada**. Reservas lógicas retidas: **P01 12 chamadas, P04 6 chamadas**. Holdout 84 e confirmação 60 de P00 permanecem protegidos. Nunca some a visão lógica com a do provedor.

## Autorizações concedidas por este prompt

Estas são explícitas e finitas. Não peça novamente nem as amplie; qualquer ampliação exige reserva finita nova e migração testada antes do uso.

1. **P00 (T6)** — autorizo exatamente **um** novo gate fake completo isolado, em snapshot novo e caminho de scratch válido, mais a congelação do binding corrente após PASS. Depois disso, autorizo usar até **6 chamadas** do envelope operacional de dez já migrado — nenhuma chamada nova além dele. O gate deve rodar só após as correções offline do runner estarem commitadas e com regressão direta passando.
2. **P01 (T1)** — autorizo **um** novo workflow sintético com identidade estável distinta, no máximo **4 chamadas** dentro das 12 lógicas já retidas, após candidato e manifesto frescos committados e um gate fake isolado PASS. Não reviva nem replique o escopo consumido; preserve o resultado INCOMPLETE anterior e os arquivos modificados intencionalmente de P01 (`artifacts/evidence/check-fast.txt`, `check-full.txt`, `artifacts/runs/latest/results.json`).
3. **P04 (T4)** — autorizo **um** novo gate fake completo isolado com identidade/fase distintas, com preparação de snapshot corrigida (a raiz do lab precisa existir no snapshot: `scripts/harness/`, `shared/policies/`, `.runtime/llm-live-readiness/`), e — somente após PASS integral desse gate e de todos os preflights — **um** workflow sintético de no máximo **3 chamadas** dentro das 6 lógicas retidas, 12.288 input / 1.536 output, modelo explícito `openai/gpt-oss-20b`, timeout 30s, USD 0 pago, sem fallback e sem replay.
4. **P02 e P03 (T2/T3)** — não precisam de nova chamada live. Mantenha 3/4 de cada intactas. Trabalho autorizado aqui é só offline: fechar pendências de documentação/reconciliação que existirem.
5. **P05 (T5)** — envelope esgotado em 8/8. Nenhuma chamada. Só trabalho offline.
6. **Atestação de host/Docker** — o host é meu; eu atesto que o container `gossett_backend` e sua troca de identidade são meus e não pertencem a nenhuma fase deste programa. Registre isso como atestação do usuário (não como verificação por API) e trate a divergência histórica como **documentada e excluída como bloqueador** para validação isolada nova. Continua **proibido mutar, parar, remover ou limpar** `gossett_backend` ou qualquer recurso Docker não comprovadamente seu.

Limites que permanecem em vigor, sem exceção: USD 0 pago, sem upgrade de plano, sem troca de provedor/modelo, sem fallback silencioso, sem replay de chamada ou gate consumido, sem liberar reserva desconhecida, sem reiniciar contador por sessão/fase/ID novo, sem tocar holdout/confirmação, sem deploy público, sem push/PR/merge, sem mensagem externa, sem dados de cliente, sem reembolso real, sem `terraform apply`, sem `--no-verify`.

## Fila finita — trabalhe um projeto por vez

| ID | Próxima ação concreta |
|---|---|
| T0 | Reauditar contabilidade em modo somente-leitura após cada operação/migração nova. Nunca mutar histórico, UUID ou prefixo. |
| T6 / P00 | Investigar offline a falha de fixture Git 128 das tentativas anteriores (stderr não era impresso — capture-o), corrigir a causa, commitar, rodar regressão direta e só então consumir o único gate autorizado. Após PASS, congelar binding e, se quiser, usar as 6 chamadas. Preserve as modificações não commitadas de P00 e o snapshot em `additional-validation-040/.git/snapshot/`. |
| T1 / P01 | Fase nova com ID livre (próximo: 028). Identidade distinta, candidato/manifesto frescos committados, testes offline de histórico/no-replay/reserva, gate fake isolado, depois no máximo 4 chamadas. |
| T4 / P04 | Fase nova com ID livre (próximo: 043). Corrigir a preparação de snapshot, validar a correção do `check_full.py` já commitada, inventariar Docker antes/depois, namespace exclusivo, provar posse antes de qualquer limpeza, consumir o único gate autorizado e, só com PASS, despachar no máximo 3 chamadas. |
| T2 / T3 | Nenhuma chamada. Verificar se há reconciliação ou documentação em aberto e fechá-la. |
| T5 | Nenhuma chamada. Só fechamento documental. |
| T7 | Preparar o pacote de revisão para humanos sem fabricar nenhum julgamento. Ver a seção abaixo. |
| Extra | O arquivo solto `35356` na raiz do lab é debris de PowerShell (nome = PID, conteúdo = caminho) de um gate já encerrado. Remova-o num commit `chore` isolado, ou registre por que não. Também avalie criar a entrada ausente em `docs/knowledge/**` descrevendo este programa, conforme o fluxo do `AGENTS.md`. |

## Laço de execução

Escolha a tarefa executável → implemente → valide em ambiente locked/fake → salve comando, cwd, exit e saída sanitizada em `artifacts/` do dono → se falhar, registre diagnóstico e contador persistente, corrija a causa raiz e revalide no mesmo turno → revise o diff staged → commit local atômico em inglês via lab-commits → atualize `STATUS.md`/`WORK.md`/`CONTINUITY` → siga para a próxima tarefa.

`max_tries: 3` por falha (tentativa inicial mais duas correções), sem reiniciar contador por sessão, fase ou ID novo. Preserve todo FAIL/INCOMPLETE; nunca enfraqueça asserção, esconda skip nem troque label esperado para passar. Retry de teste local **não** autoriza replay live, efeito externo nem contorno de quota. Ao esgotar tentativas ou faltar recurso real, registre o bloqueio exato e siga para itens independentes.

Antes de qualquer chamada ao modelo: confirme a documentação oficial atual da Groq, o catálogo autenticado, o limite observado menor, o bound completo de input, timeout finito, ausência de retry/fallback e reservas duráveis. Antes de qualquer ciclo Docker: salve identidades e estados de containers/redes/volumes/imagens, valide cache, portas e namespace exclusivo, e prove posse antes de limpar. Preserve volumes anônimos históricos. Não presuma gateway do container para o host.

## O que só eu posso fechar

Avaliação humana de qualidade, revisão independente, aprovação de dataset/rubrica, avaliação de holdout e promoção **não** serão feitas por você e não podem ser inferidas, simuladas ou declaradas. Prepare o material de revisão e me diga exatamente quais julgamentos faltam, em quais casos, e qual comando seguro eu rodo para revisar. Não declare "pronto", "live aprovado" nem qualidade revisada com esses gates pendentes. Integração de corpus/identidade externa real de P02/P04 e aceitação de IdP de produção de P05 também seguem como dependências externas, não como falha sua.

## Relatório final

Reporte por projeto e por gate: PASS/FAIL/INCOMPLETE, commits e fingerprints exatos, comandos com cwd e exit code, evidência salva, tentativas e paradas, consumo versus reservas, incerteza de billing, e a lista exata de decisões humanas pendentes. Se o host interromper o turno, persista antes o checkpoint, o contador por falha e o próximo comando, e retome daí.

--- FIM DO PROMPT ---
