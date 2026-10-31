# Diagramas no portfólio: avaliação

Avaliação de 2026-10-31 para mostrar como cada projeto funciona. Medições: `projects/p07/artifacts/evidence/diagram-eval/`. Decisão: seção "Flow diagrams" de `projects/p07/.planning/phases/003-real-portfolio/SPEC.md`.

## Conclusão

**Mermaid fica nos READMEs do GitHub. No site, usamos componente próprio `FlowDiagram`: layout calculado por ELK no build, SVG desenhado em React com os tokens do design system.** Nenhum motor de layout vai para o navegador.

## Restrições que decidem

1. CSP estrita: `style-src 'self'`, sem `unsafe-inline`.
2. No máximo 100 KB gzip de JS inicial por rota.
3. Conteúdo legível sem JavaScript (princípio 7 do design system).
4. Só tokens: a aparência precisa ser colagem, não o tema de uma biblioteca.
5. Movimento só em `transform` e `opacity`, respeitando `prefers-reduced-motion`.

## Medições

Mesmo fluxo de seis nós, Chrome real, com a CSP do site. Bundle minificado com esbuild, `react` externo, gzip.

| Candidato | JS gzip | Violações de CSP | Funciona sem JS | Resultado |
| --- | --- | --- | --- | --- |
| Mermaid 12.2 | 1.499,9 KB em 106 chunks, com todos os tipos de diagrama | **98**, setas somem | Não | Reprovado no site |
| D2 0.1.33 no navegador (WASM) | 5.849,6 KB | n/a | Não | Reprovado no site |
| D2 no build, SVG inline | 0 | **19**, layout quebrado | Sim | Reprovado: o SVG traz `<style>` próprio |
| D2 no build, via `<img>` | 0 | 0 | Sim | Funciona, mas sem tokens nem interação |
| React Flow 12.12 | 59,9 KB + CSS | 0 | Não testado | Passa, mas consome 60% do orçamento |
| ELK 0.12 no navegador | 442,3 KB | n/a | Não | Reprovado no navegador |
| **ELK no build + React SVG** | **0 para layout** | **0** | **Sim** | **Escolhido** |

Referências de tamanho: dagre 3.1 17,0 KB; Rough.js 4.6 9,1 KB; Motion 14.9 47,6 KB; Cytoscape 3.34 140,5 KB; Viz.js 3.31 479,6 KB.

Limites da medição: os 1,5 MB do Mermaid somam todos os tipos de diagrama, e um fluxograma baixa só parte disso. O número de violações é de um único fluxo. O custo em runtime do `FlowDiagram` ainda não existe para medir; o protótipo gerou 1,3 KB de HTML estático. A primeira rodada do React Flow saiu em branco por erro de JSX no teste, corrigido e repetido (`xyflow-retest.json`).

Não medidos: LikeC4 (usa React Flow e Graphviz, então herdaria o peso) e Excalidraw (ferramenta de edição, não renderizador leve).

## Por que não React Flow, mesmo passando na CSP

- Serve para edição, pan e zoom, que um leitor de portfólio não precisa. Em celular, pan compete com a rolagem.
- 60 KB para desenhar caixas fixas.
- Sem pré-render testado, o diagrama some sem JavaScript.

Se um dia houver um editor de fluxos, volta a ser a escolha certa.

## Por que Mermaid continua

GitHub renderiza Mermaid nativamente nos READMEs, sem CSP nossa no caminho. O site exporta cada fluxo para um bloco Mermaid, então README e site nascem da mesma fonte.

Adrian Roselli testou SVG do Mermaid com leitores de tela e ouviu texto corrido, sem estrutura. Por isso todo diagrama do site tem versão em lista aninhada.

## O que torna o diagrama interessante

Caixas e setas não são o diferencial. O que quase ninguém mostra:

- **O diagrama acende com a execução real.** No demo live, cada passo da run acende seu nó.
- **Cenários de falha.** Um botão mata o worker, ou tenta aprovar o próprio reembolso, e o fluxo mostra o que acontece.
- **Cada nó é uma prova.** Abre o arquivo real, no commit exato, e um teste falha se o caminho não existir.

## Fontes

[Comparativo de diagramas como código](https://diagrams.so/learn/diagram-as-code-comparison) · [Alternativas ao Mermaid](https://infrasketch.net/blog/best-diagram-as-code-tools-2026) · [FAQ do D2](https://d2lang.com/tour/faq/) · [elkjs](https://github.com/kieler/elkjs) · [LikeC4](https://github.com/likec4/likec4) · [Tutorial ELK com React Flow](https://www.hackernoon.com/creating-a-simple-diagram-by-using-elkjs-and-react-flow) · [Adrian Roselli, fluxogramas no GitHub](https://adrianroselli.com/2022/03/maybe-dont-use-flow-charts-on-github.html) · [Léonie Watson, SVG acessível](https://tink.uk/accessible-svg-flowcharts/) · [NHS Scotland, alternativa em texto](https://www.turasdesignsystem.nhs.scot/accessibility/flowchart-text-alternatives/)
