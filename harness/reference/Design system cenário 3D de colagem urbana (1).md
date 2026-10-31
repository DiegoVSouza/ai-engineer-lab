# Design system: cenário 3D de colagem urbana

Oct 25, 2026 · @Diego Vieira

## Resumo

Este estilo é uma interface-cena: o conteúdo (cards e títulos) fica no centro de uma cidade 3D ordenada, e tudo ao redor existe para levar o olho até ele. O exemplo de referência é o *Jardim digital* (versão v7), uma landing de notas em preto, vermelho e papel, com câmera guiada pelo scroll.

A estética parte do clima punk e diagonal da UI de Persona 5, mas só usamos técnicas (cor, ângulo, recorte, pontilhado). Nenhum asset, fonte, logo ou personagem da ATLUS entra no projeto.

**Os cinco princípios**

1. **Caos ordenado.** Toda forma obedece a poucas direções, e a principal é a direção do voo da câmera. Rotação aleatória é o que faz uma cena parecer bagunça.
2. **Um foco só.** O card é o ponto de fuga. Chão, prédios, linhas de velocidade e fios apontam para ele.
3. **Céu, chão e horizonte sempre legíveis.** O olho precisa saber onde é em cima e onde é embaixo antes de ler qualquer coisa.
4. **Paleta curta.** Preto, vermelho e papel. A hierarquia vem de contraste e escala, não de cor extra.
5. **Movimento com significado e custo medido.** O scroll é a câmera, o objeto monta quando você chega e desmonta quando você sai, e a página respeita `prefers-reduced-motion` e se adapta ao hardware.

O design de jogo é caro por natureza: o diretor de Persona, Katsura Hashino, diz que cada menu tem design e programa próprios e que isso "é muito trabalhoso" ([Kotaku](https://kotaku.com.au/?p=1366376)). Por isso este documento transforma o que fizemos em regras reutilizáveis, para não redescobrir tudo a cada projeto.

## Anatomia da cena

A cena tem sete camadas, de trás para a frente. Cada uma tem um papel e uma regra; se um elemento não cabe em nenhuma, ele não entra.

| Camada | O que é no Jardím digital | Regra |
| --- | --- | --- |
| 1. Horizonte | Domé de céu com degradê e névoa na mesma cor do horizonte | A névoa e o fim do chão têm a cor do céu, para a distância "sumir" sem corte |
| 2. Céu | Sol vermelho com fendas, em direção ao voo e acima do horizonte | Um único astro. Fica acima do card, nunca atrás dele |
| 3. Chão | Avenida com faixa central, bordas vermelhas, calçadas e linhas cruzadas | Todas as linhas seguem o trilho da câmera e convergem |
| 4. Cidade | Duas fileiras de prédios por lado, postes com fios, viaduto com metrô | Espaçamento regular, alturas crescendo para fora, lados paralelos à avenida |
| 5. Objeto-herói | Um objeto por nota (torre, metrô, caminhão, skate, torre-pérola) | Um só por vez, à direita do card, montado quando a nota está ativa |
| 6. Frente | Linhas de velocidade e poucos pedaços de papel | Linhas alinhadas à tangente do voo, nunca rotacionadas ao acaso |
| 7. Tela | Pontilhado, contorno por luminância, ruído e vinheta à esquerda | Uniforme em toda a imagem; é o que une 3D e papel |

O conteúdo (cards, índice, cabeçalho) é HTML por cima do canvas, fora do 3D. Isso mantém texto nítido, selecionável e acessível.

**Pistas de profundidade usadas**

A cena parece espaço de verdade porque combina as pistas monoculares da percepção ([CUNY, Sensation and Perception](https://pressbooks.cuny.edu/sensationandperception/chapter/oculomotor-and-monocular-depth-cues/)):

| Pista | Como aparece na cena |
| --- | --- |
| Perspectiva linear | Faixas da avenida, trilhos e fios convergem para o ponto de fuga |
| Altura relativa | O horizonte fica acima do centro; o que está longe sobe na tela |
| Tamanho relativo | Prédios repetidos em tamanho parecido, então o menor parece mais longe |
| Oclusão | Prédios da fileira externa aparecem atrás dos da interna |
| Gradiente de textura | Janelas acesas ficam mais finas e densas com a distância |
| Perspectiva atmosférica | Névoa vermelho-escura apaga os prédios distantes |

## Hierarquia e condução do olhar

O olho vai primeiro ao elemento mais proeminente e depois segue uma sequência definida por contraste, escala e agrupamento ([NN/g, visual hierarchy](https://www.nngroup.com/articles/visual-hierarchy-ux-definition/)). Nesta cena, a sequência desejada é fixa:

1. **Card e título** (papel claro sobre fundo escuro, o maior contraste da tela).
2. **Objeto-herói** (vermelho e papel, ao lado do card, dá o significado da nota).
3. **Contexto** (cidade, avenida, céu), que só sustenta os dois primeiros.

O NN/g recomenda no máximo três tamanhos e no máximo dois elementos grandes. Aqui, os dois grandes são o card e o objeto.

**Linhas de fuga que apontam para o card**

Linhas convergentes levam o olho ao ponto onde se encontram, e o ponto de fuga de uma estrada é o exemplo clássico; diagonais dão sensação de movimento e ligam o primeiro plano ao fundo ([Adobe, leading lines](https://www.adobe.com/in/creativecloud/photography/discover/leading-lines-photography.html)). Para isso funcionar:

- Mova o ponto de fuga para onde o card está. No Three.js, `camera.setViewOffset(w, h, w*0.17, 0, w, h)` desloca a imagem 17% para a esquerda, sem girar a câmera. Em tela estreita (card centralizado) o deslocamento é zero.
- Alinhe tudo ao eixo do voo: avenida, trilhos, fios, viaduto e linhas de velocidade usam a tangente do trilho da câmera.
- Mantenha o horizonte acima do centro, cerca de 4° a 8° de inclinação para baixo, e uma inclinação (roll) pequena e constante (0,14 rad). Uma só inclinação dá a diagonal sem desorientar.
- O card cobre o ponto de fuga. Por isso o sol e o objeto ficam fora da área do texto.

**Teste de aperto de olhos**

Antes de entregar, borre a captura e veja o que ainda aparece ([NN/g, squint test](https://www.nngroup.com/videos/squint-test/)). Se o que sobra não for o card, o fundo está forte demais. Um jeito rápido de fazer isso:

```bash
# Playwright: tira a captura e aplica blur de 10px no navegador
await page.addStyleTag({content: 'html{filter: blur(10px)}'});
await page.screenshot({path: 'squint.png'});
```

**Orçamento de atenção**

| Elemento | Limite |
| --- | --- |
| Objetos-herói visíveis montados | 1 |
| Astros no céu | 1 |
| Cores saturadas (além do vermelho) | 0 |
| Elementos girando ao acaso | 0 (rotação só no objeto-herói) |
| Pedaços de papel soltos | até 10, só no céu |
| Linhas de velocidade | cerca de 44, todas alinhadas à tangente |

## Tokens

Valores tirados do código da v7. Mude os tokens, não as regras.

**Cor**

| Token | Valor | Uso |
| --- | --- | --- |
| `--ink` | `#050505` | Fundo, texto sobre papel, sombras |
| `--red` | `#e5121f` | Única cor de destaque: item ativo, linhas, sol, objeto |
| `--dred` | `#6d0a12` | Sombra dura do card, bordas escuras |
| `--paper` | `#f2ede4` | Card, texto sobre escuro, contornos |
| `--mut` | `#cfc9be` | Texto secundário |
| névoa / horizonte distante | `#2b060b` | Cor da `Fog`, do fundo e do fim do chão (devem ser iguais) |
| brilho do horizonte | `#c4141f` a `#050505` | Degradê do domé de céu, do horizonte para o topo |
| chão / avenida / calçada | `#2a1214` / `#080808` / `#2c2c2c` | Superfícies com contraste suficiente para o pontilhado marcar |

**Tipografia**

| Papel | Fonte | Regra |
| --- | --- | --- |
| Títulos e números | Anton (Impact como reserva) | Caixa alta, grande, uma por tela |
| Texto e interface | Courier Prime (mono do sistema como reserva) | 16 px, linha 1,6, linhas curtas |
| Logo e placa do nome | Anton, Playfair Display 900, Special Elite | Letras recortadas (ransom note) só ali, nunca em texto corrido |

**Forma e movimento**

| Token | Valor | Observação |
| --- | --- | --- |
| Recorte do card | `clip-path` com 3 polígonos de 11 pontos | Borda irregular, como papel rasgado |
| Sombra do card | Pseudoelemento deslocado 8 px, `--dred`, mesmo recorte | Substitui `drop-shadow`, que repinta a cada quadro |
| Inclinação do card | ±1°, alternando | Dá ritmo sem bagunçar |
| Transição de nota | 4 listras com `skewX(-18deg)`, 0,5 s, `cubic-bezier(.7,0,.3,1)`, escalonadas 0,04 s | Só `transform`, roda no compositor |
| Tremor do card | `wig` 0,9 s, 2 repetições | Finito; animação infinita cansa |
| Pontilhado | célula de 5 px × DPR, a 45°, em preto, vermelho e papel | Troca o degradê por 3 tons |
| Contorno | Luminância com limiar 0,34, cor papel | Barato; evita renderizar normais e profundidade extras |
| Suavização do scroll | `1 - exp(-4.5 · dt)` | Independente de FPS |
| Área de toque | mínimo 44 px | Botões do cabeçalho e do índice |

O contorno por luminância foi escolha de custo. A técnica de Sobel sobre profundidade e normais dá linhas melhores, mas exige renderizar a cena mais duas vezes por quadro ([Maxime Heckel](https://blog.maximeheckel.com/posts/moebius-style-post-processing)).

## Componentes de interface

O HTML fica por cima do canvas. Cada componente tem um papel na hierarquia.

| Componente | Papel | Regras |
| --- | --- | --- |
| Card da nota | Foco principal | Fundo papel, borda recortada, sombra dura, número grande vazado à esquerda. Opaco quando selecionado, escurecido quando não |
| Índice lateral (01 a 05) | Orientação | Fixo à direita; o item ativo fica vermelho, maior e deslocado 8 px. Some abaixo de 900 px |
| Cabeçalho | Navegação e controles | Fixo, borda inferior vermelha, botões SOM, QUALIDADE e PONTILHADO com `aria-pressed` |
| HUD inferior | Estado | Número da nota em Anton vermelho e rótulo do objeto-herói ("objeto · torre de transmissão · hardware"), que liga a cena ao conteúdo |
| Transição de listras | Feedback de troca | Só quando a pessoa escolhe a nota (clique ou teclado), não quando passa por ela no scroll |
| Rodapé | Atalhos e créditos | Atalhos (setas, j/k, Esc, h) e créditos dos modelos 3D |

**Estados e feedback** (Nielsen, "visibilidade do status do sistema")

- A nota ativa aparece em três lugares ao mesmo tempo: card opaco, índice vermelho e HUD. Se um deles não acompanhar, há bug (já tivemos: a nota 01 abria apagada).
- Mudança de nota por escolha dispara listras, tremor e som opcional; mudança por scroll não dispara nada, só a câmera e a montagem do objeto.
- Controles de qualidade e pontilhado dão à pessoa controle sobre o custo visual ("controle e liberdade").

As dez heurísticas de Nielsen que guiam a revisão estão resumidas em [Princeton, Heuristics explained](https://www.cs.princeton.edu/courses/archive/spring13/cos436/handouts/Heuristics_explained.pdf).

**Teclado e foco**

- Setas para cima e para baixo, `j` e `k` trocam de nota; `Esc` volta ao topo; `h` liga e desliga o pontilhado.
- Foco visível: contorno de 3 px na cor papel com 4 px de afastamento.
- Ao escolher uma nota por teclado, o foco vai para o card e a rolagem acompanha, travando a seleção automática por cerca de 1 s para os dois não brigarem.

## Receita 3D com Three.js

Ordem de construção que funcionou. Cada passo depende do anterior; não comece pelos objetos.

1. **Trilho da câmera.** Uma `CatmullRomCurve3` com um âncora por nota. Scroll vira parâmetro `t` (posições dos cards medidas uma vez e guardadas em cache, sem ler layout durante o scroll). O `t` é suavizado com `1 - exp(-4.5 · dt)`. O mesmo padrão de scroll como "dica do diretor" aparece em [Codrops, cinematic 3D scroll](https://tympanus.net/codrops/2025/11/19/how-to-build-cinematic-3d-scroll-experiences-with-gsap/): capítulos com janela de scroll própria e tomadas de câmera planejadas.
2. **Trilho estendido.** Amostre a curva e prolongue as pontas em linha reta (+80 unidades de cada lado). Toda a cidade usa esse trilho, por isso a cena continua além da última nota.
3. **Faixas paralelas.** Função `laneCurve(lateral, altura)` que desloca o trilho para o lado usando a tangente. Avenida, viaduto, postes e tráfego usam essa função. É ela que garante a ordem.
4. **Céu e chão.** Domé de céu invertido que acompanha a câmera, com cores por vértice; fita de chão (`ribbon`) gerada ao longo do trilho; `Fog` com a mesma cor do horizonte.
5. **Cidade em ritmo.** Para cada lado e cada fileira, um prédio a cada 6,4 ou 7,4 unidades de arco, alinhado à tangente, com altura crescente para fora. Todos os prédios entram numa única geometria mesclada com cor por vértice e textura de janelas emissiva.
6. **Objeto-herói.** Um por nota, na posição `p + R·6,6 + T·2,2` do próprio ponto do trilho (`R` = direita, `T` = tangente). Modelos externos são convertidos antes (veja abaixo).
7. **Pós-processamento.** Pontilhado, contorno e acabamento, nessa ordem.
8. **Ponto de fuga.** `setViewOffset` no fim, depois de olhar para o card no navegador.

**Montagem pelo scroll**

O objeto não explode quando você chega. Ele está desmontado e se monta conforme a distância da nota ao scroll cai a zero, e desmonta ao sair:

```js
// uExp = 0 inteiro, 1.05 desmontado
u.uExp.value = Math.min(1.05, Math.max(0, Math.abs(i - Tcur) * 1.2 - .1));
// no vertex shader, por face (aRand escalona a saída de cada peça)
float ee = clamp(uExp * (.75 + .5 * aRand) - .05, 0., 1.);
ee = ee * ee * 1.4;
transformed = aCenter + dir * ee * (1.2 + aRand * 2.8) + rel * (1. - .2 * ee);
```

A geometria é `toNonIndexed` com `aCenter` e `aRand` por face. Cor: sombreamento chapado em três tons (papel, vermelho, preto) pela normal da face quando montado, mudando para tons aleatórios quando desmontado. O quadrado de `ee` mantém o objeto inteiro quando a distância é pequena.

**Modelos externos**

Converta cada modelo antes, para geometria pura (posições em `Int16`, maior dimensão 1, texturas removidas) e embuta em base64. Assim a página não precisa de `GLTFLoader`, abre offline e não dá o erro `Couldn't load texture` quando o `.glb` aponta para uma imagem externa (foi o que aconteceu com o `colormap.png` do Kenney). Verifique o tamanho: torre 31 KB, skate 45 KB, caminhão 22 KB, moto 23 KB.

Para cada modelo anote a orientação (qual eixo é o comprimento) e rotacione na montagem. Dos nossos, todos (skate e veículos) tinham o comprimento no eixo Z.

**Pós-processamento em três passes**

1. `RenderPass` da cena.
2. Pontilhado: pontos a 45° em preto, vermelho e papel + contorno por diferença de luminância, limiar 0,34.
3. Acabamento: fantasma vermelho por velocidade (dentro da paleta), granulação e escurecimento à esquerda para dar fundo ao texto.

Desligue o pontilhado (botão) e a cena continua legível, o que serve de teste de que o 3D está organizado de verdade, e não escondido pelo efeito.

## Desempenho e acessibilidade

Efeito bonito que trava não serve. O que usamos, com o motivo de cada item:

| Medida | Valor na v7 | Por quê |
| --- | --- | --- |
| Leituras de layout durante o scroll | 0 (eram 685 na v3) | `getBoundingClientRect` força layout; as posições são medidas uma vez, com `ResizeObserver` |
| DPR máximo | 1,5 | Pixels extras custam mais que ganham com pontilhado |
| `antialias` | desligado | O pontilhado já quebra as bordas |
| Escalas de resolução | 1, 0,8, 0,65, 0,5 | Passos pequenos, com verificação |
| Janela de medição | 45 quadros | Evita decidir por ruído |
| Limiares | baixa acima de 27 ms, sobe abaixo de 17,5 ms, com 6 s de trava | Histerese: lacuna entre descer e subir |
| Aquecimento | 90 quadros ignorados | Compilação de shaders não conta |
| Redimensionar | debounce de 140 ms, ignora mudança de altura menor que 120 px | Barra de URL do celular não recria alvos de render |
| Draw calls | cerca de 35 a 45 | Prédios, postes, chão e trilhos mesclados; veículos e linhas em `InstancedMesh` |
| Sombra do card | `::after` com `clip-path` | `drop-shadow` repinta todo quadro |
| Granulação | no shader | Uma `div` com `mix-blend-mode` era cara |

**Qualidade adaptativa, com ressalvas**

A discussão do fórum do Three.js ([pixel ratio por FPS](https://discourse.threejs.org/t/changing-pixelratio-based-on-fps-good-or-bad-idea/34563)) aponta o que importa: reduzir resolução só ajuda se o gargalo for preenchimento de pixels (não vértices nem chamadas de desenho); use histerese; confira se o FPS realmente melhorou e trave novas reduções por um tempo se não melhorou; e ofereça controle manual. Foi por isso que o botão QUALIDADE (auto, baixa, alta) existe. Antes de baixar a resolução, mescle malhas pequenas.

**Acessibilidade**

- **Movimento.** O WCAG 2.3.3 (nível AAA) pede que animação de movimento disparada por interação possa ser desligada, e cita parallax e movimento por scroll como causas de reações vestibulares ([W3C, Animation from Interactions](https://w3c.github.io/wcag/understanding/animation-from-interactions.html)). Técnicas: `prefers-reduced-motion` em CSS e em JavaScript. Na v7, com movimento reduzido: objetos ficam montados, sem giro, sem tremor, sem fantasma de velocidade, sem tráfego animado e sem animação de card.
- **Contraste.** Texto do card em ink sobre papel. O fundo nunca fica atrás de texto fora do card; a vinheta escurece a esquerda para dar fundo à área de leitura.
- **Teclado.** Todo controle é acessível por teclado, com foco visível e área de 44 px.
- **Sem WebGL.** Se o contexto falha, a classe `nogl` troca o fundo por um degradê diagonal em CSS e o conteúdo continua legível.
- **Fontes.** Todas têm reserva do sistema (Impact, mono). Kanji nas placas usam famílias CJK do sistema; em máquina sem elas aparecem quadrados, então confira.

**O que não foi medido**

Os testes rodaram em renderização por software, cerca de 7 FPS, que não diz nada sobre GPU real. Antes de publicar, meça em um celular de entrada e em um notebook sem placa dedicada com o painel de desempenho do navegador.

## Lições da v1 à v7

| Versão | Sintoma | Causa | Correção |
| --- | --- | --- | --- |
| v3 | Fundo pesado e travando | Muita geometria, sem orçamento de camadas | Menos objetos, merge de geometria, pós-processo simples |
| v4 | Cena sem profundidade clara; jank | Camadas soltas, leituras de layout a cada frame | Cache de layout, DPR limitado, resolução adaptativa |
| v5 | Objetos urbanos "estilhaçados" em repouso | Rotação por face escalada de forma linear | Curva não linear `ee*ee*1.4` e montagem guiada pelo scroll |
| v6 | Erro de textura `colormap.png`; "confuso, sem céu nem chão" | GLB com textura externa; caos sem hierarquia | Modelos assados em geometria sem textura; recomeço com cenário ordenado |
| v7 | Cena legível, ponto de fuga no cartão | Céu, chão, linhas de fuga e fileiras rítmicas | Ordem de camadas (seção 2) e orçamento de atenção (seção 3) |

**Limites conhecidos da v7:** o sol fica parcialmente atrás do cartão e do cabeçalho; o skate (nota 04) lê como uma placa clara grande; o FPS não foi medido em GPU real (o teste em máquina headless roda a cerca de 7 fps por renderização em software).

**Princípio que ficou:** o caos só funciona quando é organizado. Toda forma do fundo deve apontar para o cartão ou para o título.

## Checklist de revisão

- [ ] Teste do olho semicerrado: o cartão e o título continuam sendo a primeira coisa vista?
- [ ] Existe um ponto focal único e o ponto de fuga cai nele?
- [ ] Horizonte visível, com céu acima e chão abaixo?
- [ ] Elementos longos (faixas, fios, trilhos) alinhados à tangente da câmera?
- [ ] Orçamento de camadas respeitado (nada compete com o cartão em contraste)?
- [ ] `prefers-reduced-motion` honrado: cena posicionada uma vez, sem animação contínua?
- [ ] Desempenho medido em dispositivo real, com a qualidade adaptativa funcionando?
- [ ] Navegação por teclado e foco visível nos controles?
- [ ] Créditos dos modelos de terceiros no rodapé?
- [ ] Fallback sem WebGL ou offline mostra o conteúdo?
- [ ] Fontes com kanji ou acentos testadas?

## Fontes, créditos e skills para o Codex

### Fontes consultadas

- Nielsen Norman Group: hierarquia visual e o teste do olho semicerrado.
- Adobe: linhas de fuga (leading lines) na composição.
- CUNY: pistas de profundidade.
- Nielsen: 10 heurísticas de usabilidade (Princeton).
- W3C WCAG 2.3.3: animação por interação e movimento reduzido.
- Análises de interface de Persona 5 (mechanicsofmagic, Inverse, Kotaku): usadas apenas para entender técnicas (cortes diagonais, recortes, alto contraste), sem reutilizar ativos da ATLUS.
- Maxime Heckel, fórum do three.js e Codrops (cinematic scroll): pós-processamento, meios-tons e câmera guiada por scroll.
- Documentação do Codex (AGENTS.md) e guias de terceiros (itecsonline, danielvaughan) sobre skills.

### Créditos de modelos

Torre de rádio: Poly by Google (CC BY 3.0). Skate: cg\_world. Caminhão e moto: Kenney (MIT).

### Skills recomendadas

| Skill | Repositório | Para que serve |
| --- | --- | --- |
| frontend-design | anthropics/skills | Direção estética e tipografia que evitam o visual padrão |
| web-design-guidelines | vercel-labs/agent-skills | Revisão de interface; busca as regras em tempo de execução |
| ui-ux-pro-max | nextlevelbuilder/ui-ux-pro-max-skill | Estilos, paletas, pares de fontes e diretrizes de UX |
| threejs-\* | anexadas por você | Fundamentos, materiais, shaders, pós-processamento |

**Instalação no Codex:** `.agents/skills/<nome>/SKILL.md` no projeto ou `$HOME/.agents/skills` para uso global. Esses caminhos vêm de guias de terceiros; a página oficial de skills do Codex não pôde ser acessada, então confirme na sua versão. A skill da Vercel baixa as regras da internet ao rodar, e isso deve ser levado em conta em ambientes sem rede.
