# Design System: Colagem Urbana (versão universal)

Versão 1.0 · Oct 26, 2026 · @Diego Vieira

Um sistema de design e direção de arte para **qualquer tipo de projeto** (landing, portfólio, dashboard, app, documentação, loja, evento, blog) que mantém sempre a mesma identidade: **colagem urbana punk, papel recortado, tinta, meio-tom, diagonais e um foco só.**

Este documento generaliza dois sistemas anteriores:

- *Design system: cenário 3D de colagem urbana* (Jardim digital v7): cena 3D ordenada, câmera guiada por scroll, ponto de fuga sobre o cartão.
- *Design system mesclado: Jardim 3D × Wasteland*: tokens unificados, dois temas, tiras tortas, letras recortadas, camadas 2D e regras de contraste.

Tudo que era específico do "Jardim" (notas, estágios `semente/broto/árvore`, comando `jardim ler N`, objetos como torre e skate) virou **conceito genérico** com nome neutro (ver seção 2). O que é identidade (paleta curta, recorte, sombra dura, foco único, movimento só por scroll) continua igual em qualquer projeto.

---

## 1. Resumo e princípios

A estética parte do clima punk e diagonal de interfaces de jogos de ação urbanos e de cartazes de fotocópia. **Só usamos técnicas** (cor, ângulo, recorte, pontilhado). Nenhum asset, fonte, logo ou personagem de qualquer jogo ou marca entra no projeto.

**Regra de ouro:** o fundo conta o mundo, a tira (ou cartão) conta o conteúdo. Só uma coisa grita por vez, e tudo que está atrás aponta para o foco.

### Os sete princípios

1. **Caos ordenado.** Toda forma obedece a poucas direções. Rotação aleatória é o que faz uma composição parecer bagunça. Inclinações são pequenas, constantes e alternadas (±0,6° a ±1,5°).
2. **Um foco só.** Em cada tela existe um elemento principal (cartão, manchete, formulário). Linhas, chão, formas e sombras apontam para ele.
3. **Céu, chão e horizonte legíveis.** Mesmo em 2D, a pessoa precisa saber onde é em cima e onde é embaixo antes de ler.
4. **Paleta curta.** Tinta, papel e **um acento**. A hierarquia vem de contraste e escala, não de cor extra.
5. **Texto sempre sobre superfície opaca.** Nunca coloque texto direto sobre o fundo decorativo. Tira, cartão ou painel têm fundo sólido.
6. **Movimento com significado e custo medido.** O scroll é a câmera. Nada pisca nem repete em loop por padrão. `prefers-reduced-motion` é respeitado.
7. **Degradação graciosa.** O conteúdo funciona sem JavaScript, sem WebGL, sem fontes externas e sem imagens. O efeito é camada, nunca dependência.

---

## 2. Vocabulário genérico (como adaptar a qualquer projeto)

Os sistemas de origem usavam termos do projeto Jardim. Aqui eles ganham nomes neutros. Ao começar um projeto novo, preencha a coluna "No meu projeto".

| Conceito genérico | Era no Jardim | Papel | No meu projeto (exemplos) |
| --- | --- | --- | --- |
| **Item** | Nota | Unidade de conteúdo navegável | Projeto, produto, artigo, episódio, métrica, etapa, lição |
| **Cartão em foco** | Cartão da nota ativa | Item ativo em detalhe | Case aberto, produto selecionado, card do KPI |
| **Tira** | Tira da nota | Versão compacta do item em listas | Linha de lista, resultado de busca, item de menu |
| **Selo de status** | Selo de estágio (`semente/broto/árvore`) | Estado do item, sempre glifo + texto | `rascunho / revisão / publicado`, `novo / em estoque / esgotado` |
| **Comando** | `$ jardim ler N` | Linha mono que dá voz de terminal ao item | `$ projeto abrir 03`, `$ pedido ver 1042` |
| **Índice** | Índice lateral 01 a 05 | Orientação e salto entre itens | Navegação por seção, paginação, passos |
| **Objeto-símbolo** | Objeto-herói (torre, skate…) | Um objeto 3D ou SVG que representa o item ativo | Ícone do produto, ferramenta, ilustração do tema |
| **Cenário** | Cidade com avenida | O mundo atrás do conteúdo | Cidade (padrão), ou outro mundo com a mesma estrutura de camadas |
| **HUD** | HUD inferior | Estado atual da cena | "02 / 05 · projeto · categoria" |
| **Manchete** | Título em letras recortadas | Logo e título principal da página | Nome do projeto, slogan |

> **Cenário alternativo:** a cidade é o padrão da direção de arte. Se o projeto pedir outro mundo (porto, deserto, estação espacial), mantenha **a mesma pilha de camadas** (seção 6), a mesma paleta e as mesmas regras de condução do olhar. Troque só a geometria das camadas L3 e L4.

---

## 3. Níveis de adoção

Nem todo projeto precisa de cena 3D. Escolha o nível mais baixo que resolve, e suba só se houver motivo.

| Nível | O que entra | Quando usar | Custo |
| --- | --- | --- | --- |
| **0. Núcleo** | Tokens, tipografia, tiras, cartão, botões, selos, rodapé. Fundo liso de papel com riscos | Dashboards, apps, documentação, formulários, e-commerce | Mínimo |
| **1. Camadas 2D** | Núcleo + pilha L0 a L6 em SVG/CSS com parallax por scroll | Landing, portfólio, blog, campanhas | Baixo |
| **2. Cena 3D** | Núcleo + cena Three.js com câmera guiada pelo scroll, meio-tom e contorno em pós-processo | Peça de destaque, experiência de marca, showcase | Alto (medir em celular real) |

**Regra:** o Nível 2 sempre cai para o Nível 1, e o Nível 1 sempre cai para o Nível 0. O conteúdo é o mesmo nos três.

### Escolha de tema

| Tema | Quando | Papel | Observação |
| --- | --- | --- | --- |
| **Fotocópia** (claro) | Padrão de páginas de leitura, apps, docs | Papel sujo claro, tinta preta | Tema base |
| **Asfalto** (dark) | Cena 3D noturna, painéis, ferramentas de uso longo | Carvão arroxeado, "nunca preto puro" | Usar com cena 3D |

---

## 4. Tokens

**Trocar tema ou acento é trocar valores, nunca estrutura.** Os componentes usam só estes nomes. Nenhuma cor solta no CSS.

### 4.1 Cor

```css
/* Padrão: acento rosa-choque, tema Fotocópia */
:root, [data-theme="photocopy"] {
  /* Neutros */
  --ink:#111111;          /* texto, bordas, sombras duras */
  --paper:#f5f4f0;        /* fundo da página */
  --paper-card:#f0ece4;   /* cartão em foco (papel mais quente) */
  --white:#ffffff;

  /* Tira (superfície escura de lista/navegação) */
  --strip:#111111; --strip-ink:#ffffff; --strip-mute:#d8d8d8;

  /* Acento em três níveis (ver 4.2) */
  --hot:#d6007d;          /* texto pequeno sobre papel claro, fundo de botão */
  --hot-on-dark:#ff2fa3;  /* texto/título ativo sobre tira ou painel escuro */
  --hot-fill:#e6008a;     /* formas, manchete, sombra do cartão, cena 3D */
  --on-hot:#ffffff;       /* texto sobre fundo --hot */
  --spray:#3dff2e;        /* só respingos e decoração, nunca texto */

  /* Atmosfera */
  --fog:#2a0a1c;          /* névoa, horizonte e fim do chão (cena noturna) */
  --ghost:rgba(0,0,0,.05);
  --halftone:rgba(17,17,17,.20);
  --scratch:rgba(0,0,0,.04);

  /* Feedback (use com glifo + texto, nunca só cor) */
  --ok:#1f7a3a; --warn:#b34700; --err:#c8101b;
}

/* Tema Asfalto (dark): mesmo acento, papel carvão arroxeado, tira quase preta */
[data-theme="asphalt"] {
  --paper:#221e26; --ink:#f1efe8;
  --strip:#060507;
  --ghost:rgba(255,255,255,.05);
  --halftone:rgba(255,255,255,.12);
  --scratch:rgba(255,255,255,.04);
}
```

> **Cuidado no Asfalto:** sobre o papel carvão `#221e26`, `--hot` (`#d6007d`) mede só **3,24:1** e **não vale para texto pequeno**. No tema escuro, texto de acento sobre o papel usa `--hot-on-dark`. `--hot` continua válido como **fundo de botão** com texto branco.

### 4.2 Os três níveis do acento

O acento tem três valores porque a mesma cor não passa em contraste em todos os usos.

| Token | Uso | Nunca usar em |
| --- | --- | --- |
| `--hot-fill` | Formas grandes, manchete, sombras, cena 3D, respingos, bordas do rodapé | Texto pequeno |
| `--hot` | Texto pequeno sobre papel claro, fundo de botão com `--on-hot` | Texto sobre fundo escuro |
| `--hot-on-dark` | Texto e título ativo sobre tira ou painel escuro, e texto de acento no Asfalto | Fundo de botão |

### 4.3 Presets de acento

O padrão é rosa-choque. Para outro projeto, troque **só estes cinco valores** (mais `--fog` se houver cena). Todos foram medidos contra WCAG 2.x.

| Preset | `--hot` | `--hot-on-dark` | `--hot-fill` | `--on-hot` | `--fog` sugerida | Observação de contraste |
| --- | --- | --- | --- | --- | --- | --- |
| **Rosa** (padrão) | `#d6007d` | `#ff2fa3` | `#e6008a` | `#ffffff` | `#2a0a1c` | `--hot` sobre papel 4,59; branco sobre `--hot` 5,05; `--hot-fill` só decoração/texto grande |
| **Vermelho** (Jardim v7) | `#c8101b` | `#ff4a52` | `#e5121f` | `#ffffff` | `#2b060b` | `--hot` sobre papel 5,38; branco sobre `--hot` 5,92; `--hot-on-dark` sobre tira 5,71 |
| **Laranja** | `#b34700` | `#ff7a1a` | `#ff7a1a` | `#ffffff` | `#2a1205` | Branco sobre `--hot` 5,5. **Branco sobre `--hot-fill` só 2,61: nunca texto branco sobre a forma laranja**, use tinta `#111` (7,24) |
| **Azul** | `#0047d6` | `#5c8cff` | `#0057ff` | `#ffffff` | `#06122e` | `--hot` sobre papel 6,64; branco sobre `--hot` 7,31; `--hot-on-dark` sobre tira 5,98 |

Regras para criar um preset novo:

1. Escolha **um** acento. Nunca dois competindo.
2. Meça `--hot` sobre `--paper` e `--on-hot` sobre `--hot`: mínimo **4,5:1**.
3. Meça `--hot-on-dark` sobre `--strip` e sobre o papel do Asfalto: mínimo **4,5:1**.
4. `--hot-fill` pode ficar abaixo disso, mas então só vale para forma e texto grande (24 px+, ou 19 px negrito+).
5. A `--fog` é um tom muito escuro do acento. Ela deve ser **idêntica** à cor do horizonte e do fim do chão.

### 4.4 Contraste medido (WCAG 2.x)

| Par | Razão | Uso |
| --- | --- | --- |
| `#111` sobre `#f5f4f0` | 17,16 | Texto no tema claro |
| `#f1efe8` sobre `#221e26` | 14,24 | Texto no Asfalto |
| `#fff` sobre `#111` | 18,88 | Texto na tira |
| `#111` sobre `#f0ece4` | 16,03 | Texto no cartão em foco |
| `#d8d8d8` sobre `#111` | 13,25 | Texto secundário na tira |
| `#ff2fa3` sobre `#060507` | 5,99 | Título ativo na tira dark |
| `#ff2fa3` sobre `#111` | 5,56 | Título ativo na tira clara |
| `#ff2fa3` sobre `#221e26` | 4,83 | Texto de acento no Asfalto |
| `#fff` sobre `#d6007d` | 5,05 | Texto em botão/fundo rosa |
| `#d6007d` sobre `#f5f4f0` | 4,59 | Texto pequeno rosa no papel claro |
| `#d6007d` sobre `#221e26` | **3,24** | **Não usar para texto** |
| `#fff` sobre `#e6008a` | **4,44** | **Só texto grande** |
| `#e6008a` sobre `#f5f4f0` | **4,03** | **Só decoração ou texto grande** |

### 4.5 Tipografia

Duas fontes de display e duas monoespaçadas. São **aproximações do estilo**, nenhuma é a fonte original de qualquer jogo.

| Papel | Fonte | Peso | Onde | Reserva |
| --- | --- | --- | --- | --- |
| Logo e manchete | Big Shoulders Stencil Display | 800 | Stencil, maiúsculas | `Impact, sans-serif` |
| Título de item | Londrina Solid | 400 | Tira e cartão, `letter-spacing:.05em` | `Impact, sans-serif` |
| Corpo | Courier Prime | 400, 700 | Texto do cartão, 16 px, `line-height:1.55` | `monospace` |
| Comando, rótulos, rodapé, dados | JetBrains Mono | 400, 700 | Base TUI, 12 px | `monospace` |
| Numeral grande | Londrina Solid, só contorno | 400 | O "02" do cartão, `-webkit-text-stroke` | `Impact` |

```css
:root {
  --f-stencil: "Big Shoulders Stencil Display", Impact, sans-serif;
  --f-title:   "Londrina Solid", Impact, sans-serif;
  --f-body:    "Courier Prime", ui-monospace, monospace;
  --f-mono:    "JetBrains Mono", ui-monospace, monospace;
}
```

Regras:

- **Uma manchete grande por tela.** No máximo três tamanhos de texto por tela.
- Letras recortadas (ransom note) **só em logo e manchete**, nunca em texto corrido nem no cartão em foco.
- Linhas curtas (60 a 70 caracteres). Corpo em 16 px mínimo.
- Se usar kanji ou outro alfabeto como textura, declare uma família CJK/sistema própria: nenhuma das quatro fontes cobre isso. Teste em máquina sem a fonte.
- O texto crítico precisa continuar legível se o Google Fonts falhar.

### 4.6 Forma, sombra e espaçamento

| Token | Valor | Observação |
| --- | --- | --- |
| `--cut-strip` | `polygon(0 5%,3% 0,100% 3%,98% 100%,2% 95%)` | Corte irregular da tira e da manchete. Alternar variações por `nth-child` |
| `--cut-card` | `clip-path` com 4 cantos cortados (ou 3 polígonos de 11 pontos) | Borda de papel rasgado do cartão |
| `--tilt-strip` | `±0.6deg`, alternando | Rotação da tira |
| `--tilt-card` | `±1deg` a `±1.5deg`, alternando | Rotação do cartão |
| `--shadow-hard` | `4px 4px 0 var(--ink)` | Botões e painéis. **Sempre dura, sem blur** |
| `--shadow-card` | deslocamento de 8 px em `--hot-fill` | Cartão em foco, via pseudoelemento com o mesmo recorte |
| `--border` | `3px solid var(--ink)` | Painéis, índice, botões |
| `--space-*` | 4, 8, 12, 16, 24, 32, 48, 64 px | Escala única. Nada fora dela |
| `--hit` | `44px` | Área mínima de toque |
| `--focus` | `outline:3px solid currentColor; outline-offset:3px` | Foco visível em tudo que é interativo |

> **Sombra com `clip-path`:** `drop-shadow` repinta a cada quadro e é cortada por `clip-path` no mesmo elemento. Use um pseudoelemento deslocado com o mesmo recorte (cartão) ou aplique `filter: drop-shadow(5px 5px 0 var(--hot-fill))` no **wrapper**, nunca no elemento recortado (tiras no Asfalto).

### 4.7 Camadas de empilhamento (`z-index`)

| Camada | z-index |
| --- | --- |
| Fundo (2D ou canvas 3D) | 0 |
| Conteúdo (tiras, cartões) | 10 |
| Índice lateral, HUD | 20 |
| Cabeçalho fixo | 30 |
| Transição de listras | 40 |
| Modal / diálogo | 50 |
| Toast | 60 |

### 4.8 Movimento

| Token | Valor | Observação |
| --- | --- | --- |
| `--ease-cut` | `cubic-bezier(.7,0,.3,1)` | Corte seco, estilo "wipe" |
| Transição de troca | 4 listras `skewX(-18deg)`, 0,5 s, escalonadas 0,04 s | Só `transform`; roda no compositor |
| Tremor do cartão | `wig` 0,9 s, **2 repetições** | Sempre finito; loop infinito cansa |
| Suavização do scroll | `1 - exp(-4.5 · dt)` | Independente de FPS |
| Pontilhado (3D) | Célula de 5 px × DPR, a 45° | Troca o degradê por 3 tons (tinta, acento, papel) |
| Contorno (3D) | Luminância com limiar 0,34, cor papel | Barato; evita renderizar normais e profundidade extras |

---

## 5. Hierarquia e condução do olhar

O olho vai primeiro ao elemento mais proeminente e depois segue contraste, escala e agrupamento. A sequência desejada é fixa:

1. **Cartão/tira em foco e manchete** (maior contraste da tela).
2. **Objeto-símbolo** (acento e papel, ao lado do cartão, dá significado).
3. **Contexto** (cenário, chão, céu), que só sustenta os dois primeiros.

Máximo de três tamanhos de texto e dois elementos grandes (o foco e o objeto).

### Como as formas apontam para o foco

- **Ponto de fuga sobre o cartão.** Em 3D: `camera.setViewOffset(w, h, Math.round(w*.17), 0, w, h)` no desktop, `0` no mobile (cartão centralizado). Desloca a imagem sem girar a câmera.
- **Tudo na mesma direção.** Avenida, trilhos, fios, linhas de velocidade e raios seguem a tangente do voo da câmera. Rotação aleatória de linhas longas é proibida.
- **Horizonte acima do centro**, câmera inclinada 4° a 8° para baixo e uma única inclinação lateral constante (0,14 rad). Uma só diagonal dá dinamismo sem desorientar.
- **O foco cobre o ponto de fuga.** Sol, objeto-símbolo e formas decorativas ficam **fora** da área de texto.
- **Faixa central escurecida.** A área atrás da tira ou cartão fica mais escura e menos saturada. O contraste máximo é do foco.

### Pistas de profundidade (cena 3D e camadas 2D)

| Pista | Como aparece |
| --- | --- |
| Perspectiva linear | Faixas, trilhos e fios convergem para o ponto de fuga |
| Altura relativa | O que está longe sobe na tela; horizonte acima do centro |
| Tamanho relativo | Elementos repetidos em tamanho parecido; o menor parece mais distante |
| Oclusão | Fileira externa aparece atrás da interna |
| Gradiente de textura | Janelas e detalhes ficam mais finos e densos com a distância |
| Perspectiva atmosférica | Névoa na cor do horizonte apaga o que está longe |

### Orçamento de atenção (por tela)

| Elemento | Limite |
| --- | --- |
| Objetos-símbolo visíveis | 1 |
| Astros no céu | 1 |
| Cores saturadas além do acento | 0 (o verde `--spray` só em respingos) |
| Elementos girando ao acaso | 0 (rotação só no objeto-símbolo) |
| Retalhos de papel soltos | até 10, só no céu |
| Linhas de velocidade | cerca de 44, todas alinhadas à tangente |
| Itens "gritando" ao mesmo tempo | 1 |

### Teste do olho semicerrado

Antes de entregar, borre a captura. Se o que sobra não for o foco, o fundo está forte demais.

```js
// Playwright
await page.addStyleTag({ content: 'html{filter: blur(10px)}' });
await page.screenshot({ path: 'squint.png' });
```

---

## 6. Pilha de camadas (anatomia do cenário)

O fundo é sempre a mesma pilha de sete níveis, do mais distante ao mais próximo. Com WebGL, L1 a L5 viram **uma cena 3D**; sem WebGL, com movimento reduzido ou em tela estreita, as mesmas camadas vêm como SVG com parallax.

| Nível | Papel | Versão 3D | Versão 2D (SVG/CSS) | Parallax (v) |
| --- | --- | --- | --- | --- |
| **L0** | Papel / horizonte | `scene.background` e `Fog(--fog)`; domo de céu com degradê | `--paper` + riscos diagonais | 0 |
| **L1** | Céu e texto fantasma | Sol único com fendas, acima do horizonte | Palavra gigante desbotada (nome do lugar/tema) | 0,10 |
| **L2** | Luz e raios | Raios radiais alinhados à tangente, meio-tom em pós-processo | Meio-tom e raios CSS | 0,20 |
| **L3** | Cidade / estrutura | Duas fileiras de prédios por lado, viaduto, trem | Skyline SVG no acento | 0,35 |
| **L4** | Meio-plano | Postes, fios, tráfego, objetos urbanos | Palmeiras/postes SVG | 0,55 |
| **L5** | Chão | Avenida com faixa central, bordas em `--hot-fill`, calçadas, tracejado | Viaduto/pista diagonal SVG | 0,75 |
| **L6** | Respingos e recortes | Retalhos de papel no céu (até 10 peças) | Respingos `--hot-fill` e `--spray` | 0,90 |
| **UI** | Tiras e cartão | HTML por cima do canvas | Igual | n/a |

**Regras de cada camada**

| Camada | Regra |
| --- | --- |
| Horizonte | A névoa e o fim do chão têm exatamente a cor do horizonte, para a distância "sumir" sem corte |
| Céu | Um único astro, acima do cartão, nunca atrás dele |
| Chão | Todas as linhas seguem o trilho da câmera e convergem |
| Cidade | Espaçamento regular, alturas crescendo para fora, lados paralelos à avenida |
| Objeto-símbolo | Um por vez, à direita do cartão, montado quando o item está ativo |
| Frente | Linhas de velocidade alinhadas à tangente; poucos pedaços de papel |
| Tela | Pontilhado, contorno, ruído e vinheta uniformes; unem 3D e papel |

**Meio-tom sem duplicar:** meio-tom e contorno do 3D são do renderizador. Os pontos de CSS são **só** do fallback 2D.

---

## 7. Componentes

O conteúdo é HTML por cima do canvas, fora do 3D, para manter texto nítido, selecionável e acessível. Todos usam apenas os tokens da seção 4.

### 7.1 Componentes de conteúdo

| Componente | Regra |
| --- | --- |
| **Logo e manchete** | Barra `--strip` com `clip-path: var(--cut-strip)`. As três primeiras palavras em stencil branco; o resto em letras recortadas (4 estilos ciclando, `--hot-fill` e branco). Versão visual `aria-hidden`, texto real em `.sr` |
| **Tira** (lista) | Fundo `--strip`, corte irregular alternado por `nth-child`, rotação ±0,6°. **Ativa:** faixa `inset 10px 0 0 var(--hot-on-dark)`, título em `--hot-on-dark`, selo com `▶` |
| **Cartão em foco** | Papel `--paper-card`, quatro cantos cortados, sombra deslocada em `--hot-fill`, rotação ~1,5°, numeral de contorno (`02`). Opaco quando ativo, escurecido quando não. **Sem letras recortadas** |
| **Selo de status** | Adesivo branco, `rotate(-2deg)`, sombra `2px 2px 0 var(--hot)`. Texto: **glifo + nome** (`○ rascunho`, `◐ revisão`, `● publicado`). Ativo: fundo `--hot`, texto `--on-hot`, prefixo `▶`. **Nunca só cor** |
| **Comando** | `$ <verbo> <objeto> N` em JetBrains Mono 12 px, `--strip-mute`. Presente em todo item |
| **Tag** | Mono 12 px, borda 2 px `--ink`, fundo `--paper`, sem arredondamento |

**Regra de coerência (tira ↔ cartão).** Tira e cartão são **dois estados do mesmo item**, com a mesma ordem de informação: *selo de status, título, resumo, comando, tag.* A tira mostra título, selo e comando; o cartão mostra tudo.

### 7.2 Navegação e controles

| Componente | Regra |
| --- | --- |
| **Cabeçalho** | Fixo, borda inferior `--hot-fill`, botões de controle com `aria-pressed` |
| **Índice lateral** | Caixa de papel, borda 3 px `--ink`, sombra `5px 5px 0 var(--hot)`. Itens 01 a N como botões; o ativo em `--hot`, maior e deslocado 8 px. Fixo à direita; some abaixo de 900 px |
| **HUD inferior** | Número do item em stencil no acento + rótulo do objeto ("objeto · nome · categoria"). Liga cena e conteúdo |
| **Controles de cena** | `som`, `qualidade: auto/baixa/alta`, `pontilhado: on/off`, `movimento: off/on`. Contorno 2 px `--ink`, ativo em `--hot` |
| **Transição de listras** | Só quando a pessoa **escolhe** o item (clique/teclado). Quando só passa pelo scroll, não dispara nada |
| **Rodapé** | Barra `--strip`, `border-top:6px solid var(--hot-fill)`, atalhos em `<kbd>`, aviso "sem rastreadores · não pisca", créditos de terceiros |

### 7.3 Ações e formulários

| Componente | Regra |
| --- | --- |
| **Botão principal** | Fundo `--hot`, texto `--on-hot`, borda 3 px `--ink`, sombra `4px 4px 0 var(--ink)`, stencil 20 px, altura mínima 44 px. Hover/ativo: desloca 2 px e reduz a sombra para 2 px (sem blur) |
| **Botão secundário** | Fundo `--paper`, texto `--ink`, mesma borda e sombra |
| **Botão perigoso** | Igual ao principal, mas fundo `--err`, com glifo `✕` + verbo claro |
| **Campo de texto** | Fundo `--white` (claro) ou `--strip` (Asfalto), borda 3 px `--ink`, sem arredondamento, mono 14 px, rótulo **sempre visível** acima. Foco: `--focus` + sombra dura |
| **Checkbox / rádio / switch** | Quadrados (rádio = losango), borda 3 px, marcado com `■` ou `✕` em `--ink` sobre `--hot` |
| **Erro de campo** | Borda `--err` + glifo `✕` + mensagem em texto, abaixo do campo |

### 7.4 Feedback e containers

| Componente | Regra |
| --- | --- |
| **Toast / alerta** | Tira com corte irregular, glifo + texto (`✓ salvo`, `! atenção`, `✕ erro`), z-index 60. Some sozinho em 5 s **e** tem botão de fechar |
| **Modal** | Cartão em foco centralizado sobre uma película `--ink` a 70%. Foco preso dentro; `Esc` fecha |
| **Tabela de dados** | Cabeçalho em tira `--strip`; linhas alternando `--paper` e `--ghost`; números em mono, alinhados à direita |
| **Gráfico** | Acento para a série principal; neutros para o resto; barras retas, sem sombra; rótulo direto, não só legenda |
| **Abas** | Tiras lado a lado; ativa com faixa em `--hot-on-dark` e `▶` |
| **Progresso** | Barra reta 12 px, borda 3 px, preenchimento `--hot`, valor em mono ao lado |
| **Estado vazio** | Cartão com numeral em contorno, comando em mono e um botão principal |
| **Carregando** | Texto mono `carregando…` ou barra de progresso. Sem spinner infinito por padrão |

### 7.5 Estados (visibilidade do status)

- O item ativo aparece em **três lugares ao mesmo tempo**: cartão opaco, índice no acento e HUD. Se um não acompanha, é bug.
- Em tema Asfalto, tiras ganham contorno interno `inset 0 0 0 2px #4a4452` (separador sutil, decorativo) e a sombra de `drop-shadow` no wrapper.
- Estados desabilitado: opacidade 0,5 **mais** `cursor:not-allowed` e texto explicando o motivo quando possível.

---

## 8. Layout e responsividade

| Faixa | Largura | Comportamento |
| --- | --- | --- |
| Mobile | até 700 px | Modo 2D. Coluna única, cartão centralizado, deslocamento `10vh`, sem L2 e L5, índice vira barra inferior ou some |
| Tablet | 701 a 1000 px | 3D permitido, índice lateral oculto abaixo de 900 px |
| Desktop | acima de 1000 px | 3D completo, índice lateral fixo, ponto de fuga deslocado 17% |

- Grade de 12 colunas, espaçamentos da escala da seção 4.6.
- Coluna de leitura limitada a 60-70 caracteres.
- A zona de conteúdo (tira/cartão) fica sempre sobre o terço mais escuro da cena.
- Teste obrigatório em **360 px** e **1000 px**.
- Áreas de toque de 44 px, com 8 px de espaço entre alvos.

---

## 9. Movimento

**Vale a regra mais rígida:** só o scroll move a cena (câmera, montagem e desmontagem dos objetos). Nada pisca nem repete em loop por padrão.

| Situação | Comportamento |
| --- | --- |
| Padrão | Movimento só por scroll |
| `movimento: on` (controle do visitante) | Libera trem, tráfego e retalhos animados. Persiste só como preferência do visitante, desligado por padrão |
| `prefers-reduced-motion: reduce` | Modo `3d-static` (cena renderizada uma vez) ou `2d` sem parallax; sem transições, sem tremor, sem fantasma de velocidade, objetos montados |
| Aba escondida | Para o loop de render |

**Em CSS:**

```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation: none !important;
    transition: none !important;
    scroll-behavior: auto !important;
  }
}
```

Animar apenas `transform` e `opacity`. Nunca animar `width`, `height`, `top`, `left`, `filter` ou `box-shadow`.

---

## 10. Seletor de modo (3D, 3D estático ou 2D)

A decisão é tomada **uma vez**, no carregamento.

```js
const can3D = (() => {
  try { return !!document.createElement('canvas').getContext('webgl2'); }
  catch { return false; }
})();
const narrow = matchMedia('(max-width:700px)').matches;
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const mode = can3D && !narrow ? (reduce ? '3d-static' : '3d') : '2d';
document.documentElement.dataset.bg = mode;
```

```css
[data-bg^="3d"] .layer { display: none; }   /* esconde as camadas 2D quando há 3D */
[data-bg="2d"] canvas#scene { display: none; }
```

- `3d-static`: renderiza a cena uma vez, na posição inicial, e para.
- Em `2d`, no mobile: remova L2 e L5 e reduza o deslocamento do parallax para `10vh`.
- Teste cada modo **forçando** `data-bg` manualmente.
- Parallax 2D: `animation-timeline: scroll()` com fallback em JS.

---

## 11. Receita 3D com Three.js (Nível 2)

Ordem de construção que funcionou. Cada passo depende do anterior; **não comece pelos objetos.** Versão sugerida: `three@0.160.0` via importmap.

1. **Trilho da câmera.** `CatmullRomCurve3` com uma âncora por item. Scroll vira parâmetro `t` (posições dos cartões medidas uma vez e guardadas em cache; nada de ler layout durante o scroll). Suavize: `1 - exp(-4.5 · dt)`.
2. **Trilho estendido.** Amostre a curva e prolongue as pontas em linha reta (+80 unidades de cada lado) para a cena continuar além do último item.
3. **Faixas paralelas.** `laneCurve(lateral, altura)` desloca o trilho para o lado usando a tangente. Avenida, viaduto, postes e tráfego usam essa função. **É ela que garante a ordem.**
4. **Céu e chão.** Domo de céu invertido que acompanha a câmera, cores por vértice; fita de chão (`ribbon`) gerada ao longo do trilho; `Fog` com a **mesma cor** do horizonte.
5. **Estrutura em ritmo.** Para cada lado e fileira, um volume (prédio) a cada 6,4 ou 7,4 unidades de arco, alinhado à tangente, altura crescendo para fora. Tudo numa **única geometria mesclada** com cor por vértice e textura de janelas emissiva.
6. **Objeto-símbolo.** Um por item, na posição `p + R·6,6 + T·2,2` do ponto do trilho (`R` = direita, `T` = tangente).
7. **Pós-processamento.** Pontilhado, contorno e acabamento, nessa ordem.
8. **Ponto de fuga.** `setViewOffset` no fim, depois de olhar o cartão no navegador.

### Montagem pelo scroll

O objeto-símbolo está desmontado e se monta conforme a distância do item ao scroll cai a zero. Ele desmonta ao sair.

```js
// uExp = 0 inteiro, 1.05 desmontado
u.uExp.value = Math.min(1.05, Math.max(0, Math.abs(i - Tcur) * 1.2 - .1));
```

```glsl
// vertex shader, por face (aRand escalona a saída de cada peça)
float ee = clamp(uExp * (.75 + .5 * aRand) - .05, 0., 1.);
ee = ee * ee * 1.4;   // o quadrado mantém o objeto inteiro quando a distância é pequena
transformed = aCenter + dir * ee * (1.2 + aRand * 2.8) + rel * (1. - .2 * ee);
```

A geometria é `toNonIndexed` com `aCenter` e `aRand` por face. Cor: sombreamento chapado em três tons (papel, acento, preto) pela normal da face quando montado; tons aleatórios quando desmontado.

### Modelos externos

Converta antes para **geometria pura** (posições em `Int16`, maior dimensão 1, texturas removidas) e embuta em base64. Assim não precisa de `GLTFLoader`, abre offline e não dá erro `Couldn't load texture`. Referência de peso: torre 31 KB, skate 45 KB, caminhão 22 KB, moto 23 KB. Anote a orientação de cada modelo (qual eixo é o comprimento) e rotacione na montagem.

### Pós-processamento em três passes

1. `RenderPass` da cena.
2. Pontilhado: pontos a 45° em tinta, acento e papel + contorno por luminância (limiar 0,34).
3. Acabamento: fantasma de velocidade **dentro da paleta**, granulação e escurecimento à esquerda para dar fundo ao texto.

**Teste de organização:** desligue o pontilhado. Se a cena não continua legível, o 3D está escondido pelo efeito, não organizado.

---

## 12. Desempenho

| Medida | Valor | Por quê |
| --- | --- | --- |
| Leituras de layout durante scroll | 0 | `getBoundingClientRect` força layout; meça uma vez e use `ResizeObserver` |
| DPR máximo | 1,5 | Pixels extras custam mais que ganham com pontilhado |
| `antialias` | desligado | O pontilhado já quebra as bordas |
| Escalas de resolução | 1, 0,8, 0,65, 0,5 | Passos pequenos, com verificação |
| Janela de medição | 45 quadros | Evita decidir por ruído |
| Limiares | baixa acima de 27 ms; sobe abaixo de 17,5 ms; trava de 6 s | Histerese: lacuna entre descer e subir |
| Aquecimento | 90 quadros ignorados | Compilação de shaders não conta |
| Redimensionar | debounce de 140 ms; ignora mudança de altura menor que 120 px | Barra de URL do celular não recria alvos de render |
| Draw calls | ~35 a 45 | Prédios, postes, chão e trilhos mesclados; veículos e linhas em `InstancedMesh` |
| Sombra do cartão | `::after` com `clip-path` | `drop-shadow` repinta todo quadro |
| Granulação | No shader | `div` com `mix-blend-mode` é cara |

**Qualidade adaptativa, com ressalvas.** Reduzir resolução só ajuda se o gargalo for preenchimento de pixels (não vértices nem draw calls). Use histerese, confira se o FPS realmente melhorou, trave novas reduções por um tempo e ofereça controle manual (`qualidade: auto/baixa/alta`). Antes de baixar a resolução, mescle malhas pequenas.

**No 2D:** anime só `transform`. Imagens em SVG ou formatos leves, `loading="lazy"` abaixo da dobra.

**Orçamentos de partida (ajuste por projeto):** JS inicial do Nível 0 e 1 abaixo de 100 KB comprimido; Nível 2 abaixo de 500 KB sem modelos; LCP abaixo de 2,5 s em rede 4G.

> **O que nunca foi medido:** o FPS do 3D rodou só em renderização por software (~7 FPS), que não diz nada sobre GPU real. Antes de publicar, meça em um celular de entrada e em um notebook sem placa dedicada.

---

## 13. Acessibilidade

- **Fundo decorativo.** Toda camada de fundo, 2D ou 3D, tem `aria-hidden="true"` e `pointer-events:none`.
- **Status nunca só por cor.** Glifo + texto; item ativo com `▶` além da cor.
- **Texto sobre superfície opaca**, com os contrastes da seção 4.4.
- **Letras recortadas.** Versão visual `aria-hidden`, texto real em `.sr` (visualmente oculto, lido por leitor de tela).
- **Teclado.** Todo controle acessível: `j`/`k` ou setas navegam, `Enter`/`Espaço` abrem, `Esc` volta ao topo ou fecha, `h` liga/desliga o pontilhado. Foco visível de 3 px. Ao escolher por teclado, o foco vai para o cartão e a rolagem acompanha, travando a seleção automática por ~1 s.
- **Alvos de toque** de 44 px.
- **Movimento.** WCAG 2.3.3 (AAA) pede que animação por interação possa ser desligada; parallax e movimento por scroll podem causar reações vestibulares. Por isso `prefers-reduced-motion` e o controle `movimento`.
- **Sem WebGL / sem JS.** Classe `nogl` troca o fundo por degradê diagonal CSS; o conteúdo completo continua disponível.
- **Idioma e leitura.** `lang` correto, `<title>` por página, hierarquia de títulos real (`h1` a `h3`), links com texto descritivo.
- **Formulários.** Rótulo visível, erro em texto, `aria-describedby` ligando a mensagem ao campo.

---

## 14. Receita de implementação

Construa nesta ordem. Cada passo funciona sozinho antes do próximo.

1. **Tokens e tipografia** (seção 4). Nenhuma cor solta depois disso.
2. **Conteúdo e componentes em HTML puro:** manchete, tiras, selos, comando, índice, rodapé. A página já precisa ser legível e navegável por teclado.
3. **Fundo 2D** com as camadas L0 a L6 e parallax CSS. Este é o modo `2d` final.
4. **Seletor de modo** (seção 10), gravando `data-bg` no `<html>`.
5. **Cena 3D** (seção 11), só se `data-bg` for `3d` ou `3d-static`.
6. **Pós-processamento:** meio-tom, contorno por luminância, passe final.
7. **Modelos assados** em base64, com créditos no rodapé.
8. **Montagem por scroll** (`uExp`, `ee`) e qualidade adaptativa.
9. **Revisão** com o checklist (seção 16) e o teste do olho semicerrado.

Para projetos de Nível 0 ou 1, pare no passo 2 ou 3.

---

## 15. Anti-padrões

| Não faça | Por quê | Faça |
| --- | --- | --- |
| Girar elementos ao acaso | Parece bagunça, não colagem | Inclinações pequenas, constantes e alternadas |
| Mais de um acento | Perde o "uma coisa grita" | Um acento; hierarquia por contraste e escala |
| Texto direto sobre o fundo | Contraste imprevisível | Tira, cartão ou painel opaco |
| Sombras com blur | Quebram a linguagem de recorte e custam performance | Sombra dura deslocada |
| Cantos arredondados | Linguagem de UI genérica | Cantos cortados e `clip-path` |
| Letras recortadas em texto corrido | Ilegível | Só em logo e manchete |
| Animação em loop por padrão | Cansa, viola a regra de movimento | Só por scroll; loop atrás de `movimento: on` |
| `--hot-fill` em texto pequeno | Reprova contraste | `--hot` ou `--hot-on-dark` |
| `--hot` como texto no Asfalto | 3,24:1 | `--hot-on-dark` |
| Status só por cor | Exclui quem tem daltonismo | Glifo + texto |
| Efeito escondendo cena desorganizada | Falha no teste do pontilhado | Organizar primeiro, estilizar depois |
| Copiar logo, fonte, personagem de jogo ou marca | Direito autoral | Só técnicas e estética |
| Ler layout a cada frame | Jank | Cache e `ResizeObserver` |
| Dois focos competindo | Olho não sabe onde ir | Um foco; o resto aponta para ele |

---

## 16. Checklist de entrega

**Sistema**
- [ ] Só tokens no CSS dos componentes; tema e acento trocam sem editar componentes.
- [ ] Preset de acento medido: `--hot` sobre papel, `--on-hot` sobre `--hot`, `--hot-on-dark` sobre tira e sobre o Asfalto, todos ≥ 4,5:1.
- [ ] Texto pequeno de acento usa `--hot` ou `--hot-on-dark`; `--hot-fill` só em formas e texto grande.
- [ ] Letras recortadas só em logo e manchete, com `aria-hidden` e texto real em `.sr`.
- [ ] Nenhum ativo, logo, personagem ou fonte original de jogo ou marca.

**Composição**
- [ ] Teste do olho semicerrado: o foco continua sendo a primeira coisa vista.
- [ ] Um ponto focal único; ponto de fuga cai nele.
- [ ] Horizonte visível, com céu acima e chão abaixo.
- [ ] Elementos longos alinhados à tangente da câmera.
- [ ] Orçamento de atenção respeitado (nada compete com o foco em contraste).
- [ ] Status em glifo + texto; item ativo com marca além da cor.

**Movimento e modos**
- [ ] Movimento só por scroll; `movimento: on` desligado por padrão.
- [ ] `prefers-reduced-motion` honrado: cena posicionada uma vez, sem animação contínua.
- [ ] Modo 3D, 3D estático e 2D testados (forçando `data-bg`).
- [ ] Sem WebGL a página mostra o fundo 2D, sem erro no console.

**Qualidade**
- [ ] Desempenho medido em celular real, com qualidade adaptativa funcionando.
- [ ] Navegação por teclado (`j`, `k`, `Enter`, `Espaço`, `Esc`) e foco visível.
- [ ] Testado em 360 px e 1000 px.
- [ ] Fontes com fallback; legível se o Google Fonts falhar; kanji/acentos testados.
- [ ] Conteúdo completo disponível sem JavaScript e sem WebGL.
- [ ] Créditos de modelos 3D e ícones de terceiros no rodapé.

---

## 17. Lições da evolução (v1 a v7)

| Versão | Sintoma | Causa | Correção |
| --- | --- | --- | --- |
| v3 | Fundo pesado e travando | Muita geometria, sem orçamento de camadas | Menos objetos, merge de geometria, pós-processo simples |
| v4 | Cena sem profundidade clara; jank | Camadas soltas, leituras de layout a cada frame | Cache de layout, DPR limitado, resolução adaptativa |
| v5 | Objetos "estilhaçados" em repouso | Rotação por face escalada de forma linear | Curva não linear `ee*ee*1.4`, montagem guiada pelo scroll |
| v6 | Erro de textura externa; "confuso, sem céu nem chão" | Modelo com textura externa; caos sem hierarquia | Modelos assados sem textura; recomeço com cenário ordenado |
| v7 | Cena legível, ponto de fuga no cartão | Céu, chão, linhas de fuga, fileiras rítmicas | Ordem de camadas e orçamento de atenção |
| Mescla | Dois sistemas discordando | Acento, fundo, movimento e letras recortadas diferentes | Tokens unificados, dois temas, 2D como fallback do 3D, movimento mais rígido vence |

**Limites conhecidos:** o sol pode ficar parcialmente atrás do cartão e do cabeçalho; objetos claros e achatados (como um skate) podem ler como placa; o FPS em GPU real nunca foi medido.

**Princípio que ficou:** o caos só funciona quando é organizado. Toda forma do fundo deve apontar para o foco.

### Decisões herdadas da mescla (para consulta)

| Ponto | Decisão |
| --- | --- |
| Cor de acento | Um acento único em todo o sistema, incluindo a cena 3D, como token `--hot*` |
| Fundo | Página clara por padrão; cena 3D noturna com névoa na cor `--fog`; tiras `#111` ou `#060507` |
| Superfície do conteúdo | Tira para lista e navegação; cartão de papel para o item em foco |
| Fundo em movimento | 3D é a camada principal; 2D entra sem WebGL, com movimento reduzido ou em tela pequena |
| Movimento | Vale a regra mais rígida: só por scroll |
| Letras recortadas | Só em manchete e logo, nunca no cartão em foco |

---

## 18. Como usar este documento com IA (Codex, Claude Code etc.)

Cole o trecho abaixo no `AGENTS.md`, `CLAUDE.md` ou no início do prompt, junto com este arquivo.

```md
# Direção de arte: Colagem Urbana

Siga DESIGN_SYSTEM_COLAGEM_URBANA.md.

- Nível de adoção deste projeto: [0 núcleo | 1 camadas 2D | 2 cena 3D]
- Preset de acento: [rosa | vermelho | laranja | azul]
- Tema padrão: [photocopy | asphalt]
- Vocabulário: Item = [...], Selo de status = [...], Comando = [...]

Regras inegociáveis:
1. Só tokens do documento. Nenhuma cor solta.
2. Um foco por tela; todo o resto aponta para ele.
3. Texto sempre sobre superfície opaca (tira, cartão, painel).
4. Sombra dura, sem blur; cantos cortados, sem arredondamento.
5. Status em glifo + texto, nunca só cor.
6. Movimento só por scroll; respeite prefers-reduced-motion.
7. O conteúdo funciona sem JS, sem WebGL e sem fontes externas.
8. Nada de ativos, fontes, logos ou personagens de jogos ou marcas.
9. Ao terminar, rode o checklist da seção 16 e o teste do olho semicerrado.
```

Skills úteis (de terceiros; confirme caminhos e versões na sua ferramenta): `frontend-design` (anthropics/skills), `web-design-guidelines` (vercel-labs/agent-skills, baixa regras da internet ao rodar), `ui-ux-pro-max` (nextlevelbuilder), e skills `threejs-*` para o Nível 2.

---

## 19. Fontes e créditos

**Base teórica**
- Nielsen Norman Group: hierarquia visual e teste do olho semicerrado.
- Adobe: linhas de fuga (leading lines) na composição.
- CUNY (*Sensation and Perception*): pistas monoculares de profundidade.
- Nielsen: 10 heurísticas de usabilidade.
- W3C WCAG 2.x e 2.3.3: contraste, animação por interação, movimento reduzido.
- Maxime Heckel (pós-processamento estilo Moebius), fórum do three.js (pixel ratio adaptativo) e Codrops (cinematic scroll): técnica 3D.
- Análises públicas de interface de jogos urbanos de ação: usadas **apenas** para entender técnicas (cortes diagonais, recortes, alto contraste).

**Origem deste sistema**
- *Design system: cenário 3D de colagem urbana* (Jardim v7).
- *Design system mesclado: Jardim 3D × Wasteland*.
- WASTELAND_DESIGN.md (anexado ao mesclado): tokens claro/dark, tiras, letras recortadas, camadas 2D, contrastes do rosa. Fontes e cores desse arquivo são aproximações declaradas por ele mesmo.

**Créditos de modelos usados nos exemplos:** torre de rádio, Poly by Google (CC BY 3.0); skate, cg_world; caminhão e moto, Kenney (MIT). Em qualquer projeto novo, liste os créditos dos modelos usados no rodapé.

**Aviso:** esta estética é inspirada em jogos e cartazes de terceiros. Use em projetos próprios; não reproduza logos, personagens nem imagens de nenhum deles. Os contrastes dos presets adicionais (vermelho, laranja, azul) foram calculados pela fórmula WCAG 2.x; os valores de qualidade adaptativa vêm do Jardim v7 e precisam de validação em celular real.
