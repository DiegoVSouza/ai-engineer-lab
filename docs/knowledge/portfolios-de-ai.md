# Pesquisa: como portfólios de AI mostram projetos

Pesquisa de 2026-10-31 para a fase de portfólio do P07. Li páginas reais de portfólios, além de guias. Revisado com as decisões do dono (demo sempre live). Decisões derivadas daqui: `docs/decisions/ADR-002-portfolio-as-product.md`. Spec: `projects/p07/.planning/phases/003-real-portfolio/SPEC.md`.

## Confiabilidade

- Quase todo guia sobre o tema é blog de curso, bootcamp ou serviço de carreira. O que vale é a **convergência qualitativa**, e os exemplos reais que dá para inspecionar.
- **Nenhum número de recrutador é usado aqui.** Tempos de "7 s", "11 s", "30 s" e "90 s", "87% checam GitHub", "80% mais engajamento" e "3× mais callbacks" não têm fonte primária e se contradizem. Tratei como folclore.
- Não achei estudo revisado por pares sobre como recrutadores avaliam GitHub ou portfólio de AI.
- Dois portfólios da lista não abriram (404): `hharsha98` e `resume-sehlani`. A saída em tempo de execução da demo da Gopika não foi capturada, só a estrutura.

## O que converge

| Sinal forte | Sinal fraco |
| --- | --- |
| Poucos projetos profundos | Muitos demos rasos ou clones de tutorial |
| Demo clicável, sem cadastro | Só notebook, ou projeto que o avaliador não consegue rodar |
| Evals com número, conjunto e comando | "Funciona bem" sem medida |
| Falhas documentadas e o que mudou | Só caminho feliz |
| Custo e latência aproximados | Modelo citado sem motivo |
| Decisões com alternativas rejeitadas | Lista de ferramentas |
| README que abre com problema e decisão | README que abre com instalação |
| Dados e usuário específicos | Corpus genérico, "chat com PDF", wrapper de API |
| Papel pessoal declarado | Autoria vaga |

Divergências reais: um guia pede um projeto profundo, outro dois ou três, outro três a cinco. "Agente" é sinal forte num guia e, noutro, "construir um agente" como objetivo é o maior erro: agente precisa de estado, condição de parada, teto de custo e avaliação por iteração. O lab já tem isso.

Rubrica útil, da JobRoadMaps: **Specificity** (números e ferramentas nomeadas), **Evidence** (algo que um estranho verifica sem confiar no autor), **Focus** (especialidade clara), **Process** (raciocínio de decisão visível), **Currency** (sinais de manutenção), **Voice** (registro humano, muitas vezes via limite admitido).

## Portfólios reais lidos

| Portfólio | O que aproveitar | Limite |
| --- | --- | --- |
| Franco Cazal (`francocazal.com`) | Melhor modelo de case: TL;DR, problema, decisões terminando em "Rules out:", tradeoffs aceitos, resultados com run ID, "o que eu faria diferente". Mostra variação: sete runs de 80% a 96%. Publica resultados negativos. Links para arquivos, ADRs e golden set. | Sem demo hospedada; precisa de Docker Compose |
| Gopika Jaideep (Netlify) | Página de evals como produto: "Replay recorded results", gate de CI simulado, mutation testing, red-team em replay. Rotula "Illustrative replay". Demo RAG mostra router, guard, retrieve, generate, verify com trace. | Muitos números vêm sem link para o run |
| ethanthemaxxx/ai-portfolio | Seções **Measured** e **Not measured, so not claimed**. Tabela Projeto / Demo / "The decision worth reading about". "every number on this page comes from a command you can run". Demos sem cadastro, em fixture, e diz isso. | Só README e demos simples |
| longda/ai-engineer | Admite que recursos live só rodam localmente, para evitar custo e conta | Unidade é objetivo, não projeto |
| Simon Willison | Currency: release, prompt exato, demo jogável. Voz própria | Blog, não vitrine |
| Hamel Husain | Autoridade em evals; error analysis antes de escrever evals | Sem demo |
| Jason Liu, swyx | Atribuição externa, alcance | Depende de audiência que ainda não temos |
| TwilightCore (`tccore-portfolio`) | Case de eval e monitoramento bem estruturado | Métricas sem método e sem repo: exemplo do que evitar |

Padrões técnicos de demo vistos: fixture sem modelo real, relay em tier grátis com fallback extrativo, recuperação no navegador sem servidor, e replay gravado rotulado. Para trace público, o caminho seguro é fixture anonimizada.

Do lado de avaliação, o método de Hamel Husain é: olhar traces reais, categorizar falhas à mão, priorizar, e só então escrever evals. Mostrar esse processo vale mais que uma nota final. A ligação com portfólio é inferência minha, não fonte.

## O que o lab já tem e quase ninguém mostra

- P00: 27/36 passes em campanha real, 9/12 casos únicos, Wilson 95% [0,47; 0,91], famílias que falharam (ambíguo 0/6, limites do provedor 0/3), e veredito `FAIL_PROVISIONAL` assumido, com orçamento de holdout protegido.
- P05: fluxo live com recibos conferidos e trace correlacionado sem conteúdo; controle duplo de reembolso.
- P04: lease, DLQ e recuperação testados em serviço.
- P03: privacidade em spans testada.
- Processo: SDD, gates, ledger de orçamento, evidência por fase.

O diferencial não é "tenho agentes". É: **um estranho pode verificar cada afirmação, e as falhas estão à vista**. Vale também para a nota ruim do P00, que é o melhor material do portfólio.

## Lacunas críticas encontradas no lab

1. **Os seis repositórios no GitHub estão privados**, com 29 a 116 commits sem push. P06, P07 e P08 não têm remoto. Hoje um recrutador não vê código nenhum.
2. **`stack.py checkout` não funciona numa máquina nova**: commits fixados não estão publicados. "Clone e rode" precisa ser provado.
3. **CI hospedado está `incomplete`** no P00. Sem ele não há selo público.
4. **Rotas com hash** não indexam, e o design system pede conteúdo sem JavaScript.
5. **O console exige login**, e as senhas demo precisam de rotação antes de abrir ao público (`fly-deployment.md`).
6. **`idp.fly.dev` expõe o admin do Keycloak** como caminho público, ponto a verificar e fechar antes de divulgar.

## Hospedagem

- Cloudflare diz: para projeto novo, use Workers em vez de Pages; Pages continua funcionando, e o investimento novo vai para Workers. `_headers` e `_redirects` funcionam nos dois.
- Pages Free: 20.000 arquivos, 25 MiB por arquivo, 500 builds por mês, e `_headers` com 100 regras e 2.000 caracteres por linha. A CSP do console cabe.
- **O subdomínio `*.pages.dev` não pode ser renomeado**: mudar exige apagar o projeto e criar outro.
- Fly: máquina parada faz boot do zero. `min_machines_running = 1` evita cold start, com custo. Suspend preserva memória e acorda mais rápido.

## Fontes

Portfólios: [Franco Cazal](https://francocazal.com/projects/whisper-docs) · [repo](https://github.com/FrancoCazal/Portfolio) · [Gopika Jaideep](https://gopika-jaideep.netlify.app) · [repo](https://github.com/GopikaJaideep/portfolio) · [ethanthemaxxx/ai-portfolio](https://github.com/ethanthemaxxx/ai-portfolio) · [longda/ai-engineer](https://github.com/longda/ai-engineer) · [Simon Willison](https://simonwillison.net/) · [Hamel Husain](https://hamel.dev/) · [Jason Liu](https://jxnl.co/) · [swyx](https://www.swyx.io/) · [TwilightCore](https://tccore-portfolio.pages.dev/projects/llm-eval-monitoring-dashboard)

Guias (opinião): [JobRoadMaps](https://jobroadmaps.com/portfolios/ai-engineer) · [techinterview](https://www.techinterview.org/post/3233475399/ai-portfolio-built-with-ai-2026-interviews/) · [Dataquest](https://www.dataquest.io/blog/ai-projects/) · [Coderhouse](https://www.coderhouse.com/articles/ai-engineer-portfolio-projects-llm-apps) · [DataExpert](https://www.dataexpert.io/blog/ultimate-guide-ai-engineering-portfolios) · [SlateGit](https://slategit.com/blog/how-recruiters-screen-github-2026) · [DEV, READMEs](https://dev.to/kazkozdev/i-studied-how-github-readmes-are-actually-evaluated-here-are-the-5-things-that-matter-2epd) · [Fonzi, case study](https://fonzi.ai/blog/engineering-case-study)

Evals: [Lenny's Newsletter, Hamel Husain](https://www.lennysnewsletter.com/p/building-eval-systems-that-improve) · [ChatPRD](https://www.chatprd.ai/how-i-ai/hamel-husains-guide-to-ai-evals-with-error-analysis)

Traces: [Microsoft Foundry Trace Replay](https://learn.microsoft.com/azure/foundry/observability/how-to/trace-agent-replay) · [Invariant Explorer](https://invariantlabs.ai/blog/explorer)

Infra: [Cloudflare Workers best practices](https://developers.cloudflare.com/workers/best-practices/workers-best-practices/) · [Migrar de Pages para Workers](https://developers.cloudflare.com/workers/static-assets/migration-guides/migrate-from-pages/) · [Limites do Pages](https://developers.cloudflare.com/pages/platform/limits/) · [Domínios no Pages](https://developers.cloudflare.com/pages/configuration/custom-domains/) · [Fly autostop](https://fly.io/docs/launch/autostop-autostart/) · [Cloudflare agent setup](https://developers.cloudflare.com/agent-setup/prompt.md)
