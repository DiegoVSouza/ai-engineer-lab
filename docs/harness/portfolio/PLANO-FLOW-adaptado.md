# Plano de flow do portfólio, adaptado à nossa arquitetura

Base: `PLANO_IMPLEMENTACAO_PORTFOLIO_flow.md` (na raiz do lab). Este arquivo diz o que do plano foi adotado, o que mudou por causa da arquitetura que já existe, e o que falta. Contratos de cena: `projects/p07/src/content/scenes.json` e `projects/p07/docs/cenas.md`.

## O que muda por causa da nossa arquitetura

| Plano | Nosso caso | Por quê |
| --- | --- | --- |
| Vite + JS puro | React 19 + TypeScript, prerender estático de 28 rotas | Já existe, testado, com CSP estrita e e2e. Reescrever perderia isso |
| Three.js 0.160 | Three.js 0.187.0, pinada, cena em chunk lazy | Já medido sob a CSP do site |
| `projects/*.json` com métricas escritas à mão | Casos em `src/content/cases`, números só por token `{ev:id}` de registros de evidência | Regra do owner: número sem evidência não entra (EV-001). As métricas de exemplo do plano (latência, acerto) são inventadas e não entram |
| `status`: ao_vivo / gravado / em_construcao | Modo do registro (`fake`, `replay`, `live`, `service`) com glifo e palavra | É o que a evidência prova. "Ao vivo" só se houve run live |
| Hash `#projeto-slug` numa página | Rota real `/projects/<slug>/` prerenderizada | Link direto já cai na estação com HTML completo e SEO |
| Quatro abas na estação | Documento de seções em ordem fixa + índice lateral | Ordem fixa é testada; abas esconderiam conteúdo da primeira leitura e dos buscadores. Mantém-se a ideia de "estado discreto, não scroll preso" |
| Demo em iframe | Stack real acordada sob pedido após verificação humana; página `/demo/` mostra status, orçamento, contas e log de runs reais | O console é outra origem com login próprio. Os estados do plano (acordando, sem resposta, limite atingido, sem demo) já existem lá |
| Só português | Português e inglês | Já feito e testado (I18N-001) |
| Skills de terceiros (seção 9) | Não instaladas | O plano pede aprovação. Nada foi instalado |

## Fases do plano contra o que existe

| Fase do plano | Situação |
| --- | --- |
| 0 conteúdo e estrutura | Feita (HTML sem JS em todas as rotas, contraste, teclado, WhatsApp e telefone) |
| 0.5 cenas e fluxo | **Feita agora**: `scenes.json` + `src/scenes.test.ts` (o build falha se faltar prova, gatilho, quadro, fallback de movimento reduzido, caminho no celular ou foco) + `docs/cenas.md`. **Falta sua decisão sobre o estilhaço** (abaixo) |
| 1 estação | Feita como caso de uso próprio (seções, índice lateral, diagrama com lista em texto). Abas não adotadas |
| 2 superfície 2D | Camadas do nível 1 via `colagem-ui` (`Layers`) + pontilhado em CSS (`.screen-dots`, só no nível 1, atrás do conteúdo). Feito |
| 3 cena 3D | Feita: cidade, prédios com janelas, viaduto e trem, rastros, anéis de vidro, objetos-símbolo, câmera pelo scroll, qualidade adaptativa, pausa em aba oculta, perda de contexto. Passe de pontilhado **feito** (cores dos tokens como uniforms, célula `5 * dpr`, toggle e tecla `h`, escolha lembrada). Falta o RGB split e a vinheta à esquerda |
| 4 correções do v5 | Retalhos e rastros posicionados antes de parar: **corrigido agora** (havia o bug de empilhar na origem; `data-at-origin=0` testado). Região `aria-live` "Projeto 3 de 8" **feita** |
| 5 crachá e paleta | Crachá/contato feito. Paleta `/` e Ctrl+K **feita** (carregada em chunk próprio para caber nos 100 KB) |
| 6 auditoria | e2e com axe e contraste em 28 rotas, dois tamanhos, CSP, sem JS, teclado: feita. Teste do olho semicerrado, Lighthouse e FPS em celular real: pendentes |

## O que foi mudado nesta rodada

- Contratos de cena como dado, validados no build (7 cenas, 11 estados).
- Tela em retrato fica no nível 1 (sem canvas), como pede o plano.
- Bug herdado do v5 corrigido: instâncias móveis empilhadas na origem nos modos estáticos.
- Quadros estáticos por cena salvos pelo e2e em `projects/p07/artifacts/evidence/portfolio-w7b/`.

## Decisões que precisam de você

1. **Estilhaço (cena S1).** Opção A: manter como está (padrão, custo zero). Opção B: ao abrir um caso, os cacos vão para os nós do diagrama daquele caso, para o efeito carregar informação (cerca de um dia de trabalho). Registrado em `docs/cenas.md`. Continuo na A até você escolher.
2. **Abas na estação.** Mantive seções em ordem fixa. Se você quiser mesmo as quatro abas (Demo, Arquitetura, Decisões, Números), eu faço como melhoria progressiva: sem JS tudo aparece empilhado, com JS vira abas. Custo: reescrever o teste de ordem das seções.

## Próximos passos que não precisam de decisão

RGB split e vinheta à esquerda, só quando a seleção assenta (regra do design system). Medição de FPS em celular real (SCENE-005): depende de um aparelho. Teste do olho semicerrado e Lighthouse.
