# Design System: Colagem Urbana, versão Noite (vidro quebrado × vermelho)

Versão 1.0 · Oct 27, 2026 · @Diego Vieira

Um sistema de design e direção de arte para **qualquer tipo de projeto** (landing, portfólio, dashboard, app, documentação, loja, evento, blog) que mantém sempre a mesma identidade: **cidade noturna em colagem punk, breu, papel rasgado, um vermelho só, vidro quebrado, meio-tom e um foco só.**

Este documento adapta o sistema universal *Colagem Urbana* (tema claro, acento rosa) para o visual do **Jardim digital: colagem 3D v5** (`jardim-colagem-3d-v5.html`): fundo quase preto, vermelho `#e5121f`, papel `#f2ede4`, túnel de vidro quebrado, skyline com janelas acesas, números gigantes vazados, objetos que se estilhaçam, pontilhado em três tons, Anton e letras recortadas. A estrutura de seções é a mesma do sistema universal; o que mudou é a **identidade visual**.

> **Marcas usadas neste documento.** **[v5]** = existe no HTML e foi extraído dele. **[proposta]** = derivado para uso universal e **não existe** no HTML. Onde não há marca, vale como regra de sistema.

Tudo que era específico do "Jardim" (notas, estágios `semente/broto/árvore`, torre, metrô, skate) virou **conceito genérico** com nome neutro (seção 2). O que é identidade (paleta curta, recorte, sombra dura, foco único, vidro, breu) continua igual em qualquer projeto.

### O que muda em relação ao sistema universal

| Ponto | Universal (Fotocópia · rosa) | Esta versão (Noite · vermelho) |
| --- | --- | --- |
| Tema padrão | Claro: papel sujo e tinta preta | **Escuro: breu `#050505`.** Papel só nas superfícies de foco |
| Acento | Rosa-choque em três níveis | Vermelho `#e5121f`. O v5 usa um nível só; aqui ele ganha três (4.2) |
| Fundo | Cidade com avenida, sol e céu | Túnel de vidro quebrado, skyline noturna, viaduto, avenida com rastros de luz. Sem sol |
| Tipografia | Big Shoulders, Londrina, Courier Prime, JetBrains Mono | **Anton**, Playfair Display 900, Special Elite, Courier Prime |
| Objeto-símbolo | Monta conforme o scroll se aproxima | **Estilhaça quando a seleção assenta** e se recompõe |
| Sombra do cartão | Deslocada em acento | Deslocada: `--dred` em repouso, `--red` em foco |
| Pós-processo | Pontilhado + contorno | Pontilhado K/R/P + contorno + RGB-split + grão + vinheta à esquerda |
| Movimento | Só scroll | Scroll + movimento ambiente (metrô, rastros, retalhos, faixa) + eventos curtos. Tudo para em `prefers-reduced-motion` |
| Cartão em repouso | Tira escura | Cartão escuro `#0c0c0c`, o mesmo item em outro estado |

---

## 1. Resumo e princípios

A estética parte do clima punk e diagonal de cartazes de fotocópia e de interfaces de ação urbanas, **à noite**. **Só usamos técnicas** (cor, ângulo, recorte, pontilhado, vidro). Nenhum asset, fonte, logo ou personagem de qualquer jogo ou marca entra no projeto.

**Regra de ouro:** o fundo conta a cidade, o cartão conta o conteúdo. Só uma coisa grita por vez, e tudo que está atrás aponta para o foco. No v5 isso é literal: a câmera voa por um túnel de vidro quebrado e o cartão de papel é o ponto mais claro da tela.

### Os sete princípios

1. **Caos ordenado.** Em repouso, toda forma obedece a poucas direções: cartões a ±1° a ±1,2°, plaquinha a −2,5°, faixa a −3°, riscos na mesma diagonal (−0,55 rad ±0,15), câmera com **uma** inclinação lateral constante (0,2 rad). O caos solto é **cinético** e mora só na camada da frente (retalhos e skates girando), com orçamento fixo (seção 5).
2. **Um foco só.** Em cada tela existe um elemento principal (cartão em foco, manchete, formulário). Vidro, prédios, viaduto e fios apontam para ele; o fundo escurece à esquerda para dar chão ao texto.
3. **Profundidade legível.** Não há céu nem sol: a pessoa precisa saber onde é em cima (viaduto, fios), onde é embaixo (avenida) e onde são os lados (prédios) antes de ler. A câmera desce numa diagonal constante.
4. **Paleta curta.** Breu, papel e **um acento**. O vinho `--dred` só faz sombra. A hierarquia vem de contraste e escala, não de cor extra.
5. **Texto sempre sobre superfície opaca.** Nunca coloque texto direto sobre a cena. Barra fixa, cartão, plaquinha e `.lead` têm fundo sólido (`--ink`, `--card` ou `--paper`).
6. **Movimento com significado e custo medido.** O scroll é a câmera. O movimento ambiente é decoração barata e **para** em `prefers-reduced-motion`. Explosão, tremor e RGB-split disparam só quando a seleção assenta, nunca nos itens que passam durante o scroll.
7. **Degradação graciosa.** O conteúdo funciona sem JavaScript, sem WebGL e sem fontes externas. O efeito é camada, nunca dependência. **[v5]** Sem WebGL, `body.nogl` troca a cena por um degradê diagonal.

---

## 2. Vocabulário genérico (como adaptar a qualquer projeto)

O v5 usa termos do projeto Jardim. Aqui eles ganham nomes neutros. Ao começar um projeto novo, preencha a coluna "No meu projeto".

| Conceito genérico | Era no Jardim | Papel | No meu projeto (exemplos) |
| --- | --- | --- | --- |
| **Item** | Nota | Unidade de conteúdo navegável | Projeto, produto, artigo, episódio, métrica, etapa, lição |
| **Cartão** | `.cw` / `.item` | O item em dois estados: **repouso** (escuro, também faz o papel de tira de lista) e **foco** (papel) | Case aberto, produto selecionado, card do KPI |
| **Selo de status** | `.cap` (`semente/broto/árvore`) | Estado do item | `rascunho / revisão / publicado`, `novo / em estoque / esgotado` |
| **Meta** | `.m` (data, tempo, `#tag`) | Linha de dados do item | Data, duração, categoria |
| **Índice** | `.idx` (botões 01 a 05) | Orientação e salto entre itens | Navegação por seção, paginação, passos |
| **Objeto-símbolo** | Sólido estilhaçável (torre, metrô, caminhão, skate, torre-pérola) | Um objeto 3D ou SVG que representa o item ativo | Ícone do produto, ferramenta, ilustração do tema |
| **Vidro** | Painéis de vidro quebrado | Anel de cacos por onde a câmera passa, um por item | Moldura de transição entre seções |
| **Número fantasma** | Numeral gigante vazado atrás da cena | Marca o item ativo no fundo | "01", "02"… ou outro símbolo do projeto |
| **Cenário** | Cidade noturna (Tóquio/Xangai) | O mundo atrás do conteúdo | Cidade (padrão) ou outro mundo com a mesma pilha de camadas |
| **HUD** | `.hud` | Estado atual da cena | "02/05 · objeto · nome · categoria" |
| **Manchete** | `.plate` (letras recortadas) + `.hl` (Anton) | Logo e título principal | Nome do projeto, slogan |
| **Faixa** | `.band` | Faixa diagonal com palavras-chave em rolagem | Slogan, categorias, avisos |
| **Listras** | `.wipe` | Transição de troca de item | Troca de rota, de aba, de passo |
| **Comando** | *(não existe no v5)* | **[proposta]** Linha mono que dá voz de terminal ao item | `$ projeto abrir 03` |

> **Cenário alternativo:** a cidade noturna é o padrão da direção de arte. Se o projeto pedir outro mundo (porto, deserto, estação espacial), mantenha **a mesma pilha de camadas** (seção 6), a mesma paleta e as mesmas regras de condução do olhar. Troque só a geometria das camadas L2 e L3.

### Exemplo preenchido: o Jardim digital **[v5]**

| Nº | Título do item | Selo | Tag | Objeto-símbolo |
| --- | --- | --- | --- | --- |
| 01 | como queimei um esp32 (e o que aprendi) | broto | #hardware | Torre de transmissão (treliça, estilo Tóquio) |
| 02 | diário no terminal, parte 2 | árvore | #terminal | Metrô elevado |
| 03 | o bot da cantina caiu domingo às 3 da manhã | semente | #bots | Caminhão de entrega (modelo Kenney) |
| 04 | ferramentas que não largo | árvore | #terminal | Skate |
| 05 | carta pra mim daqui a um ano | semente | #diário | Torre-pérola (estilo Xangai) |

Estrutura de dados do item: `[título, "data, tempo", tag, selo, resumo]`. O texto do HUD vem de um array paralelo `OBJ[]` ("torre de transmissão · hardware").

---

## 3. Níveis de adoção

Nem todo projeto precisa de cena 3D. Escolha o nível mais baixo que resolve, e suba só se houver motivo.

| Nível | O que entra | Quando usar | Custo |
| --- | --- | --- | --- |
| **0. Núcleo** | Tokens, tipografia, cartões, botões, selos, rodapé. Fundo liso `--ink` com riscos | Dashboards, apps, documentação, formulários, e-commerce | Mínimo |
| **1. Camadas 2D** | Núcleo + pilha L0 a L6 em SVG/CSS com parallax por scroll | Landing, portfólio, blog, campanhas | Baixo |
| **2. Cena 3D** | Núcleo + cena Three.js com câmera guiada pelo scroll, vidro, skyline e pós-processo | Peça de destaque, experiência de marca, showcase | Alto (medir em celular real) |

**Regra:** o Nível 2 sempre cai para o Nível 1, e o Nível 1 sempre cai para o Nível 0. O conteúdo é o mesmo nos três.

> **[v5]** O HTML implementa o Nível 2 e um fallback mínimo (`body.nogl`: `linear-gradient(115deg, ink 0 52%, dred 52% 55%, ink 55%)`). O Nível 1 completo é **[proposta]**.

### Escolha de tema

| Tema | Quando | Papel | Observação |
| --- | --- | --- | --- |
| **Breu** (escuro) | Padrão. Cena 3D, landing, apps de uso noturno | `--ink #050505`, texto `--paper` | **[v5]** Tema base. O breu é quase preto **de propósito**; nunca `#000` |
| **Papel** (claro) | Documentação longa, impressão, leitura diurna | Fundo `--paper`, texto `--ink`, cartões e tiras continuam escuros | **[proposta]** Mesmo acento, mesma estrutura, só troca superfícies |

---

## 4. Tokens

**Trocar tema ou acento é trocar valores, nunca estrutura.** Os componentes usam só estes nomes. Nenhuma cor solta no CSS.

### 4.1 Cor

```css
/* Padrão: acento vermelho, tema Breu */
:root, [data-theme="breu"] {
  /* Neutros [v5] */
  --ink:#050505;          /* fundo da página, névoa da cena, texto sobre papel */
  --card:#0c0c0c;         /* cartão em repouso */
  --ink-2:#111111;        /* listra de transição, painéis neutros */
  --paper:#f2ede4;        /* texto sobre breu, cartão em foco, rodapé, contornos */
  --mut:#cfc9be;          /* texto secundário sobre breu */
  --paper-ink:#1c1c1c;    /* descrição dentro do cartão em foco */
  --white:#ffffff;

  /* Superfícies da página [proposta: no v5 é ink/paper direto] */
  --page:var(--ink);
  --on-page:var(--paper);

  /* Acento em três níveis (ver 4.2) */
  --red:#e5121f;          /* formas, manchete, faixa, numeral, sombra do cartão em foco, fundo de botão, cena 3D */
  --red-text:#ff4a52;     /* [proposta] texto pequeno de acento sobre breu */
  --dred:#6d0a12;         /* sombra do cartão em repouso, fallback sem WebGL, prédios tintados */
  --on-red:#ffffff;       /* texto sobre fundo --red */

  /* Atmosfera */
  --fog:var(--ink);       /* névoa e fundo da cena: IDÊNTICOS, sempre */

  /* Feedback [proposta] (use com glifo + texto, nunca só cor) */
  --ok:#5fd38d; --warn:#ffb340; --err:#ff4a52;
}

/* Tema Papel [proposta]: mesmo acento, páginas claras */
[data-theme="papel"] {
  --page:var(--paper);
  --on-page:var(--ink);
  --red-text:#c8101b;     /* 5,08:1 sobre papel; --red só dá 4,06 */
  --ok:#1f7a3a; --warn:#b34700; --err:#c8101b;
}
```

**Cinzas de cena [v5].** A cena 3D usa uns poucos cinzas e tons tintados. Eles ficam **só na cena** e nunca competem com o foco.

| Valor | Onde |
| --- | --- |
| `#0b0b0b`, `#1a1a1a` | Cacos de vidro (66% e 20%), carroceria do trem |
| `#262626`, `#2a2a2a` | Riscos de velocidade, retalhos, veículos |
| `#222222` | Pilares do viaduto |
| `#2a0508` | Viga do viaduto |
| `#303030`, `#4a4a4a`, `#5a0a10` | Prédios (cinza escuro, cinza claro, vinho). **`#4a4a4a` é o teto de claridade** |
| `#120808` | Janela apagada |
| `#ff1a2a` | Luz pontual vermelha que acompanha a câmera |

> **Regra do breu:** `--ink`, `--fog` e `scene.background` são o **mesmo valor**. A distância some na cor do fundo, sem corte.

### 4.2 Os três níveis do acento

O acento tem três valores porque a mesma cor não passa em contraste em todos os usos. O v5 usa só `--red`; os outros dois são **[proposta]** para componentes novos.

| Token | Uso | Nunca usar em |
| --- | --- | --- |
| `--red` | Formas grandes, manchete, faixa, numeral, HUD, sombra do cartão em foco, barras de cabeçalho e rodapé, cena 3D, **fundo de botão com `--on-red`** | Texto pequeno (4,31:1 sobre breu) |
| `--red-text` | Texto pequeno e título ativo sobre breu ou cartão escuro. No tema Papel, texto de acento sobre papel | Fundo de botão |
| `--dred` | Sombra do cartão em repouso, prédios tintados, fundo do fallback `nogl` | Texto (1,65:1 sobre breu) |

### 4.3 Presets de acento

O padrão é vermelho. Para outro projeto, troque **só estes quatro valores**. Medidos contra WCAG 2.x sobre `--ink #050505`.

| Preset | `--red` | `--red-text` | `--dred` | `--on-red` | Observação de contraste |
| --- | --- | --- | --- | --- | --- |
| **Vermelho** (padrão, v5) | `#e5121f` | `#ff4a52` | `#6d0a12` | `#ffffff` | Branco sobre `--red` 4,73; `--red` sobre breu 4,31 (forma e texto grande); `--red-text` 6,17 |
| **Rosa** | `#e6008a` | `#ff2fa3` | `#6b0045` | `#050505` | Branco sobre `--red` só 4,44: use tinta (4,59). `--red` sobre breu 4,59; `--red-text` 6,01 |
| **Laranja** | `#ff7a1a` | `#ff7a1a` | `#7a3a0a` | `#050505` | Tinta sobre `--red` 7,81. **Branco só 2,61: nunca texto branco sobre laranja** |
| **Azul** | `#0057ff` | `#5c8cff` | `#002a73` | `#ffffff` | Branco sobre `--red` 5,52. `--red` sobre breu só 3,70 (forma); `--red-text` 6,45 |

> O token se chama `--red` porque no v5 ele é vermelho. Nos outros presets o nome continua, o valor muda.

Regras para criar um preset novo:

1. Escolha **um** acento. Nunca dois competindo.
2. Meça `--on-red` sobre `--red`: mínimo **4,5:1**.
3. Meça `--red-text` sobre `--ink` e sobre `--card`: mínimo **4,5:1**.
4. `--red` pode ficar abaixo disso, mas então só vale para forma e texto grande (24 px+, ou 19 px negrito+).
5. `--dred` é um tom de cerca de metade do brilho do acento. Só faz sombra.
6. **A cena 3D lê as cores dos tokens.** No v5 elas estão fixas no JavaScript (`0xe5121f`, `0xff1a2a`, `vec3(.898,.071,.122)` no shader); para trocar o preset, leia `getComputedStyle` uma vez no boot **[proposta]**.

### 4.4 Contraste medido (WCAG 2.x)

| Par | Razão | Uso |
| --- | --- | --- |
| `#f2ede4` sobre `#050505` | 17,48 | Texto no Breu |
| `#f2ede4` sobre `#0c0c0c` | 16,78 | Texto no cartão em repouso (opacidade total) |
| `#cfc9be` sobre `#0c0c0c` | 11,88 | Descrição em repouso |
| `#050505` sobre `#f2ede4` | 17,48 | Cartão em foco, rodapé |
| `#1c1c1c` sobre `#f2ede4` | 14,62 | Descrição no cartão em foco |
| `#fff` sobre `#050505` | 20,38 | Texto sobre barra e plaquinha |
| `#fff` sobre `#e5121f` | 4,73 | Botão, toggle ativo, índice ativo, tag do cartão |
| `#050505` sobre `#e5121f` | **4,31** | Faixa (Anton 24 px+). **Só texto grande** |
| `#e5121f` sobre `#050505` | **4,31** | HUD, numeral, formas. **Só texto grande ou decoração** |
| `#e5121f` sobre `#0c0c0c` | **4,13** | Idem, sobre o cartão |
| `#ff4a52` sobre `#050505` | 6,17 | Texto pequeno de acento |
| `#ff4a52` sobre `#0c0c0c` | 5,92 | Texto pequeno de acento no cartão |
| `#c8101b` sobre `#f2ede4` | 5,08 | Texto de acento no Papel |
| `#e5121f` sobre `#f2ede4` | **4,06** | **Não usar em texto pequeno** |
| `#6d0a12` sobre `#050505` | **1,65** | **Só sombra, nunca texto** |
| Cartão em repouso a 50% de opacidade | **4,62** (texto), **3,56** (descrição) | Medido sobre cena escura; cai mais com papel ou vermelho atrás. Ver anti-padrões |

### 4.5 Tipografia

Quatro famílias do Google Fonts. São **aproximações do estilo**, nenhuma é a fonte original de qualquer jogo.

| Papel | Fonte | Peso | Onde | Reserva |
| --- | --- | --- | --- | --- |
| Display | Anton | 400 | Manchete (`.hl`), título do cartão, HUD, numeral, faixa, botões do índice. **Sempre em MAIÚSCULAS** | `Impact, sans-serif` |
| Letras recortadas | Anton + Playfair Display + Special Elite | 400 / 900 / 400 | **Só logo e plaquinha** | `sans-serif` / `Georgia, serif` / `"Courier New", monospace` |
| Corpo e interface | Courier Prime | 400, 700 | Texto, rótulos, botões, meta, rodapé | `ui-monospace, monospace` |
| Numeral grande | Anton, só contorno | 400 | Numeral do cartão (`-webkit-text-stroke:2px`) e número fantasma da cena | `Impact` |
| Kanji das placas | Anton + CJK do sistema | 900 | Placas de neon da cena | `"Noto Sans CJK JP","Hiragino Sans","Yu Gothic",sans-serif` |

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Anton&family=Special+Elite&family=Playfair+Display:wght@900&family=Courier+Prime:wght@400;700&display=swap">
```

```css
:root {
  --f-display: "Anton", Impact, sans-serif;
  --f-body:    "Courier Prime", ui-monospace, monospace;
  --f-serif:   "Playfair Display", Georgia, serif;      /* só letras recortadas */
  --f-type:    "Special Elite", "Courier New", monospace; /* só letras recortadas */
}
body { font: 16px/1.6 var(--f-body); }
```

| Elemento | Tamanho | Observação |
| --- | --- | --- |
| Logo | 24 px | Letras recortadas |
| Plaquinha (`.plate`) | `clamp(40px, 8vw, 92px)`, rotação −2,5° | Letras recortadas, `white-space:nowrap` |
| Manchete (`.hl`) | `clamp(30px, 5.6vw, 68px)` / 1,06 | Anton, maiúsculas, largura máx. 15 em |
| Título do cartão | `clamp(26px, 3.4vw, 38px)` / 1,1, espaçamento `.03em` | Anton, maiúsculas |
| Numeral do cartão | 70 px (54 px no mobile) | Só contorno de 2 px |
| Corpo | 16 px / 1,6 | Descrição com largura máx. 50 ch; `.lead` 46 ch |
| Meta | 14 px | |
| Rótulos (selo, nav, toggles, plaquinha-rótulo) | 12 a 13 px, negrito, maiúsculas, espaçamento `.08em` a `.2em` | |
| Botão | 16 px, negrito, maiúsculas, `.08em` | |
| HUD | `clamp(36px, 6vw, 64px)` | Anton em `--red`, sombra de texto dura |
| Faixa | `clamp(24px, 3.6vw, 36px)`, `.08em` | Anton, maiúsculas |

Regras:

- **Uma manchete grande por tela.** No máximo três tamanhos de texto corrido por tela.
- Letras recortadas (ransom note) **só em logo e plaquinha**, nunca em texto corrido nem no cartão em foco.
- Corpo em 16 px mínimo. Linhas curtas (46 a 70 caracteres).
- Letras recortadas: 3 famílias × 3 kits de cor (`k0` papel/tinta, `k1` vermelho/branco, `k2` tinta/papel com anel de 2 px), rotação por letra de ±4,8°, deslocamento vertical de ±1 px, caixa alta em cerca de metade das letras.
- Kanji ou outro alfabeto como textura precisa de família CJK/sistema declarada: nenhuma das fontes acima cobre isso. Teste em máquina sem a fonte.
- O texto crítico precisa continuar legível se o Google Fonts falhar.

### 4.6 Forma, sombra e espaçamento

```css
:root {
  --cut-card: polygon(0 3%,6% 0,34% 2%,66% 0,100% 3%,99% 50%,100% 97%,68% 100%,36% 98%,4% 100%,0 55%);
}
```

| Token | Valor | Observação |
| --- | --- | --- |
| `--cut-card` | Polígono de 11 pontos acima | Recorte do cartão **e** da sua sombra |
| `--tilt-card` | `−1,2°` nos ímpares, `+1°` nos pares; pares ganham deslocamento lateral `clamp(0, 5vw, 70px)` | Em foco: rotação ×0,4 e `scale(1.04)` |
| `--shadow-card` | Pseudoelemento `::after` deslocado `8px 8px` em `--dred` (repouso) e `9px 9px` em `--red` (foco), mesmo recorte, `z-index:-1` | **Sempre dura, sem blur** |
| `--tape` | Fita adesiva `::before`: 96 × 26 px, `#f2ede4c0`, `rotate(-4deg)`, `top:-13px; left:42px` | Assinatura do cartão |
| `--dots` | `radial-gradient(currentColor 1.2px, #0000 1.7px) 0 0 / 8px 8px`, opacidade `.12`, `clip-path: polygon(0 0,55% 0,0 100%)` | Meio-tom decorativo no canto do cartão |
| `--border` | `2px solid var(--paper)` (toggles, índice), `3px` no botão | Contorno de papel sobre breu |
| `--rule` | Cabeçalho: `border-bottom 3px --red`. Rodapé: `border-top 6px --red`. `.lead`: `border-left 8px --red`. Faixa: `border-block 4px --ink` + anel `0 0 0 4px --paper` | Barras de cor que ancoram cada bloco |
| `--ring` | `0 0 0 2px var(--paper)` (letras `k2`), `0 0 0 1px currentColor` (`kbd`) | Contorno duro, sem blur |
| `--text-shadow` | `3px 3px 0 var(--ink)` | HUD |
| `--block` | Retângulo `--red` com `skewX(-28deg) rotate(-3deg)` atrás da manchete (`left:-16%; top:30%; width:66%; height:44%`) | Bloco diagonal do herói |
| `--space-*` | 4, 8, 12, 16, 24, 32, 48, 64 px | Escala única. Margem lateral responsiva: `clamp(14px, 4vw, 36px)` |
| `--hit` | `44px` (botões principais 48 px) | Área mínima de toque |
| `--focus` | `outline:3px solid var(--paper); outline-offset:4px` | Foco visível em tudo que é interativo |

> **Sombra com `clip-path`:** `drop-shadow` repinta a cada quadro e é cortada por `clip-path` no mesmo elemento. Use o pseudoelemento deslocado com o mesmo recorte, como o v5 faz. **[v5]** O código registra que a troca de `filter: drop-shadow` por `::after` foi feita por desempenho.

### 4.7 Camadas de empilhamento (`z-index`)

| Camada | z-index |
| --- | --- |
| Fundo (canvas 3D ou 2D) | 0 |
| Conteúdo (herói, cartões, rodapé) | 2 |
| Transição de listras | 12 |
| HUD | 13 |
| Cabeçalho fixo e índice lateral | 14 |
| Modal / diálogo | 50 **[proposta]** |
| Toast | 60 **[proposta]** |

### 4.8 Movimento

| Token | Valor | Observação |
| --- | --- | --- |
| `--ease-cut` | `cubic-bezier(.7,0,.3,1)` | Corte seco, estilo "wipe" |
| Transição de troca | 4 listras `skewX(-18deg)`, 0,5 s, escalonadas 0,04 s. Cores: `--red`, `--paper`, `#111`, `--red`. Largura 30 vw, posições −6, 20, 46 e 72 vw | Só `transform`; roda no compositor |
| Cartão | `transform .25s`, `opacity .3s` | Em foco: `scale(1.04)` |
| Tremor do cartão (`wig`) | 0,9 s, `ease-in-out`, **2 repetições**, anima o `clip-path` | Sempre finito. Única animação de `clip-path`, curta de propósito |
| Faixa em rolagem | `translateX(-50%)`, 18 s, `linear`, infinito | Decorativa, `aria-hidden`; **para** em reduced-motion |
| Suavização do scroll | `1 - exp(-4.5 · dt)` | Independente de FPS |
| Parallax do ponteiro | `1 - exp(-4 · dt)`, câmera ±0,7 em x e ±0,4 em y | Desligado em reduced-motion |
| Explosão do objeto | Dispara 140 ms **depois** que a seleção assenta; decai `exp(-2.6 · dt)` | Intensidade `1,2` |
| Tremor de câmera | Amplitude 0,35, decai `exp(-5 · dt)` | Só quando a seleção assenta |
| RGB-split | `uVel · .0035`, limitado a ±2,5, mais um pulso de `glitch` (decai `exp(-6 · dt)`) | Velocidade do voo alimenta o efeito |
| Pontilhado | Célula de `5px × DPR`, a 45° | Três tons: breu, vermelho, papel |
| Contorno | Limiar 0,34 sobre a diferença de luminância, cor papel | Barato; sem normais nem profundidade extras |

---

## 5. Hierarquia e condução do olhar

O olho vai primeiro ao elemento mais proeminente e depois segue contraste, escala e agrupamento. A sequência desejada é fixa:

1. **Cartão em foco e manchete** (papel sobre breu: 17,5:1 e a maior mancha clara da tela).
2. **Objeto-símbolo** (vermelho, papel e preto em três tons, ao lado do cartão).
3. **Contexto** (vidro, skyline, viaduto, avenida), que só sustenta os dois primeiros.

Máximo de três tamanhos de texto e dois elementos grandes (o foco e o objeto).

### Como as formas apontam para o foco

- **Trilho em diagonal descendente.** As âncoras da câmera seguem `(i·3 + sin(i·1,3)·1,4, −i·1,7 + cos(i·1,1)·.8, −i·4,2)`: a câmera voa para a direita, para baixo e para a frente. É a única diagonal da composição.
- **Câmera.** FOV 58. Posição `(cp.x − 1,6 + px·.7, cp.y + 1,8 + py·.4, cp.z + 7,5)`, `up = (−sin 0,2, cos 0,2, 0)` (uma inclinação lateral constante), `lookAt(ca.x + 1, ca.y − .2, ca.z − 3)` com `ca = C(T + .35)`.
- **Conteúdo à esquerda, objeto à direita.** Cartão com largura máx. de 540 px à esquerda. Objeto-símbolo em `(a.x + 4,6, a.y − .2, a.z − 2,2)` no desktop e em `(a.x + 1,4, a.y + 2,4, a.z − 3)` quando a tela é mais alta que larga (**proporção < 1, não largura em pixels**).
- **Vinheta à esquerda.** O pós-processo multiplica a cor por `mix(.5, 1, smoothstep(0, .6, x))`: a zona de texto fica mais escura que o resto. O contraste máximo é do foco.
- **O vidro emoldura.** Um anel de cacos (raios 7,6 a 19) fica à frente de cada item; a câmera passa pelo buraco central.
- **Tudo na mesma direção.** Viaduto, avenida, fios e rastros seguem o trilho. Rotação aleatória de linhas longas é proibida.
- **O foco cobre o ponto de fuga.** O número fantasma e o objeto-símbolo ficam fora da área de texto.

### Pistas de profundidade

| Pista | Como aparece |
| --- | --- |
| Perspectiva linear | Viaduto, avenida, rastros de luz e fios convergem seguindo o trilho |
| Altura relativa | Viaduto no alto (+9), avenida embaixo (−11), prédios crescendo para fora |
| Tamanho relativo | Objeto-símbolo em `0,55 + 0,95·near`: o ativo cresce, os outros encolhem |
| Oclusão | Vidro na frente, fileira de prédios atrás, número fantasma no fundo (`z −15`) |
| Gradiente de textura | Janelas em grade 16 × 4 com `NearestFilter`, mais finas com a distância |
| Perspectiva atmosférica | `Fog(--ink, 8, 40)`: o que está longe some no breu |

### Orçamento de elementos (por cena) **[v5]**

| Elemento | Quantidade | Regra |
| --- | --- | --- |
| Objeto-símbolo ativo | 1 em cor e escala cheia | Os outros ficam cinza `#2b2b2b` (`vec3(.17)`) e menores |
| Número fantasma em destaque | 1 | Os outros a 12% de opacidade |
| Anéis de vidro | 1 por item | ~40% dos cacos são omitidos de propósito |
| Prédios | 56 | Uma geometria mesclada |
| Placas de neon verticais | até 14 | Só nos prédios acima de 26 de altura |
| Riscos de velocidade | 60 | Mesma diagonal, mesmas 3 cores + papel |
| Retalhos de papel | 36 | **Giram em 3 eixos**: único elemento de caos solto, só na frente |
| Skates girando | 16 | Idem, só na frente |
| Trens | 2 × 6 vagões | Em movimento ambiente |
| Rastros de luz | 46 | Vermelho num sentido, papel no outro |
| Veículos | 9 (5 caminhões, 4 motos) | Modelos Kenney |
| Vãos de fio | 36 | Papel a 60% de opacidade |
| Cores saturadas além do acento | 0 | |
| Itens "gritando" ao mesmo tempo | 1 | |

### Teste do olho semicerrado

Antes de entregar, borre a captura. Se o que sobra não for o foco, o fundo está forte demais.

```js
// Playwright
await page.addStyleTag({ content: 'html{filter: blur(10px)}' });
await page.screenshot({ path: 'squint.png' });
```

---

## 6. Pilha de camadas (anatomia do cenário)

O fundo é sempre a mesma pilha, do mais distante ao mais próximo. Com WebGL, L1 a L6 viram **uma cena 3D**; sem WebGL, com movimento reduzido ou em tela estreita, as mesmas camadas vêm como SVG com parallax **[proposta]**.

| Nível | Papel | Versão 3D **[v5]** | Versão 2D (SVG/CSS) **[proposta]** | Parallax (v) |
| --- | --- | --- | --- | --- |
| **L0** | Breu / horizonte | `scene.background` e `Fog(--ink, 8, 40)` | `--ink` + degradê diagonal (`nogl` do v5) | 0 |
| **L1** | Número fantasma | Plano 20 × 20 com Anton 430 px: preenchimento `--red` a 30%, contorno de 12 px `--paper`, rotação −0,18 rad, em `z −15` | Numeral gigante em CSS com `-webkit-text-stroke` | 0,10 |
| **L2** | Skyline | 56 prédios, janelas acesas (30% vermelho, 8% papel, resto `#120808`), faróis vermelhos, até 14 placas de neon | Skyline SVG em `--dred` e cinzas, janelas em grade | 0,35 |
| **L3** | Infraestrutura | Viaduto com trilhos e 18 pilares, 2 trens, avenida com 46 rastros e 9 veículos, 36 vãos de fio | Viaduto e pista diagonais em SVG | 0,55 |
| **L4** | Vidro quebrado | 1 anel por item, 4 raios (7,6 · 10,2 · 14 · 19), cacos extrudados a 0,12, gira com o scroll | Polígonos SVG em `--card`, `--ink-2` e uns poucos `--red` | 0,75 |
| **L5** | Objeto-símbolo | 1 sólido por item (toon de 3 tons), estilhaça ao assentar | SVG chapado nas mesmas 3 cores | 0,85 |
| **L6** | Frente | Riscos, retalhos, skates, fios | Riscos CSS na diagonal e retalhos SVG | 0,90 |
| **Tela** | Pós-processo | Pontilhado, contorno, RGB-split, grão, vinheta esquerda | Pontos CSS **só** aqui | n/a |
| **UI** | Barra, cartão, índice, HUD | HTML por cima do canvas | Igual | n/a |

**Regras de cada camada**

| Camada | Regra |
| --- | --- |
| Breu | Névoa, fundo e fim do chão têm exatamente a mesma cor |
| Número fantasma | Um em destaque; atrás do foco, nunca na frente do texto |
| Skyline | Alturas 18 a 66, espaçamento irregular **controlado**, lados paralelos à avenida. Cinza máximo `#4a4a4a` |
| Infraestrutura | Todas as faixas seguem o trilho da câmera (`lane(dx, dy, dz)`) e convergem |
| Vidro | Cores por vértice: 66% `#0b0b0b`, 20% `#1a1a1a`, 9% `--red`, 5% `--paper`. Nada de azulado |
| Objeto-símbolo | Um por vez, à direita do cartão, cinza quando inativo |
| Frente | Poucos elementos, todos na paleta. Só aqui vale rotação solta |
| Tela | Pontilhado, contorno, grão e vinheta uniformes; unem 3D e papel |

**Meio-tom sem duplicar:** meio-tom e contorno do 3D são do renderizador. Os pontos de CSS (`--dots`) são só o detalhe do cartão e do fallback 2D.

---

## 7. Componentes

O conteúdo é HTML por cima do canvas, fora do 3D, para manter texto nítido, selecionável e acessível. Todos usam apenas os tokens da seção 4.

### 7.1 Componentes de conteúdo

| Componente | Regra |
| --- | --- |
| **Logo e plaquinha** | Letras recortadas (3 famílias × 3 kits). Versão visual `aria-hidden`, texto real em `.sr`. Rótulo `.plate-l` acima: fundo `--ink`, 13 px negrito, `.2em`, rotação −2° |
| **Manchete** | `.hl` em Anton, maiúsculas, `clamp(30px, 5.6vw, 68px)`. Atrás dela, o bloco `--red` inclinado (`--block`) |
| **Lead** | Parágrafo em `--ink`, `border-left: 8px solid var(--red)`, padding 10 × 14, largura 46 ch |
| **Faixa** | Barra `--red`, texto `--ink` em Anton, `rotate(-3deg)`, margem lateral negativa, borda dupla (tinta + anel de papel). Palavras separadas por `★` em rolagem. `aria-hidden` |
| **Cartão em repouso** | Fundo `--card`, recorte `--cut-card`, rotação alternada, sombra `--dred`, fita adesiva, numeral de contorno `--red`, selo em papel, descrição em `--mut`. **[v5]** opacidade `.5` (`.92` no mobile) |
| **Cartão em foco** | Fundo `--paper`, texto `--ink`, descrição `--paper-ink`, numeral em contorno `--ink`, sombra `--red` a 9 px, rotação ×0,4, `scale(1.04)`, tremor `wig` ×2. **Sem letras recortadas** |
| **Selo de status** | **[v5]** Etiqueta (`.cap`): 12 px, negrito, `.16em`, maiúsculas; papel sobre tinta em repouso, tinta sobre papel em foco. **[proposta]** Glifo + nome (`○ semente`, `◐ broto`, `● árvore`), ativo com `▶`. **Nunca só cor** |
| **Meta** | Linha com data/tempo à esquerda e `#tag` à direita. A tag é um bloco `--red` com texto `--on-red` (`--ink` no cartão em foco), 14 px negrito |
| **Comando** | **[proposta]** `$ <verbo> <objeto> N` em Courier Prime 12 px, `--mut`. Presente em todo item |

**Regra de coerência (repouso ↔ foco).** Os dois estados do cartão têm **a mesma ordem de informação**: *selo, título, resumo, meta.* O repouso mostra tudo, mais apagado; o foco mostra tudo, mais claro.

### 7.2 Navegação e controles

| Componente | Regra |
| --- | --- |
| **Cabeçalho** | Fixo, fundo `#050505f0`, `border-bottom: 3px solid var(--red)`. Logo à esquerda, links em 13 px negrito maiúsculas (`.12em`), toggles à direita. Links somem abaixo de 760 px |
| **Toggles** | Botões `.tg`: 12 px, borda 2 px `--paper`, altura 44 px, `aria-pressed`. Ativo: fundo e borda `--red`, texto `--on-red`. `qualidade` e `pontilhado` só aparecem **depois** que o 3D iniciou |
| **Índice lateral** | Fixo à direita, centrado na vertical. Botões 48 × 44 em Anton 18 px, fundo `#050505cc`, borda 2 px `--paper`. Atual: `--red`, `translateX(-8px) scale(1.12)`, `aria-current`. Some abaixo de 900 px |
| **HUD** | Canto inferior esquerdo. Numeral `01/05` em Anton `--red` com sombra dura; rótulo "nota" acima e "objeto · nome · categoria" em caixa `--ink`. `pointer-events:none` |
| **Listras** | Quatro faixas em diagonal. **Só quando a pessoa escolhe** o item (clique, teclado, `Esc`, botão "descer"). Quando só passa pelo scroll, não dispara nada |
| **Rodapé** | Fundo `--paper`, texto `--ink`, `border-top: 6px solid var(--red)`, atalhos em `<kbd>`. Mostra teclas em desktop e dica de toque em `(hover:none)` |
| **Som** | Toggle `som: off/on`. Pulso de onda quadrada de 520 para 880 Hz, ganho 0,04. **Desligado por padrão** |

### 7.3 Ações e formulários

| Componente | Regra |
| --- | --- |
| **Botão principal** | **[v5]** Fundo `--red`, borda `--red`, texto `--on-red`, Courier Prime 16 px negrito maiúsculas, altura mínima 48 px, sem sombra, sem arredondamento |
| **Botão secundário** | **[v5]** Fundo `--ink`, borda 3 px `--paper`, texto `--paper` |
| **Estados do botão** | **[proposta]** Hover/ativo: desloca 2 px e fundo `--red` mais claro; desabilitado: opacidade 0,5, `cursor:not-allowed`, motivo em texto |
| **Botão perigoso** | **[proposta]** Fundo `--paper`, borda 3 px `--red-text`, glifo `✕` + verbo claro. (O acento já é vermelho, então o perigo se distingue pelo glifo e pela palavra, não pela cor) |
| **Campo de texto** | **[proposta]** Fundo `--card`, borda 3 px `--paper`, sem arredondamento, Courier Prime 14 px, rótulo **sempre visível** acima. Foco: `--focus` |
| **Checkbox / rádio / switch** | **[proposta]** Quadrados (rádio = losango), borda 3 px `--paper`, marcado com `■` ou `✕` em `--on-red` sobre `--red` |
| **Erro de campo** | **[proposta]** Borda `--err` + glifo `✕` + mensagem em texto abaixo do campo, ligada por `aria-describedby` |

### 7.4 Feedback e containers **[proposta]**

Nenhum destes aparece no v5. Todos seguem a mesma linguagem: recorte, borda de papel, sombra dura.

| Componente | Regra |
| --- | --- |
| **Toast / alerta** | Cartão em repouso com corte irregular, glifo + texto (`✓ salvo`, `! atenção`, `✕ erro`), z-index 60. Some sozinho em 5 s **e** tem botão de fechar |
| **Modal** | Cartão em foco centralizado sobre película `--ink` a 80%. Foco preso dentro; `Esc` fecha |
| **Tabela de dados** | Cabeçalho em `--card` com texto `--paper`; linhas alternando `--ink` e `--ink-2`; números em Courier Prime, à direita |
| **Gráfico** | `--red` para a série principal; papel e cinzas para o resto; barras retas, sem sombra; rótulo direto |
| **Abas** | Cartões em repouso lado a lado; ativa em `--paper` com `▶` |
| **Progresso** | Barra reta 12 px, borda 3 px `--paper`, preenchimento `--red`, valor ao lado |
| **Estado vazio** | Cartão com numeral em contorno, texto curto e um botão principal |
| **Carregando** | Texto `carregando…` ou barra de progresso. Sem spinner infinito |

### 7.5 Estados (visibilidade do status)

- O item ativo aparece em **cinco lugares ao mesmo tempo**: cartão em foco, índice (`aria-current`), HUD, objeto-símbolo em cor e número fantasma em destaque. Se um não acompanha, é bug.
- Em sistemas sem 3D, os três primeiros bastam.
- Estado desabilitado: opacidade 0,5 **mais** `cursor:not-allowed` e texto explicando o motivo quando possível.

---

## 8. Layout e responsividade

| Faixa | Largura | Comportamento **[v5]** |
| --- | --- | --- |
| Mobile | até 760 px | Links do cabeçalho somem; toggles menores; cartão com recuo de 78 px para o numeral de 54 px; opacidade do cartão `.92`; célula com 70 vh; faixa com margem de −20 vw |
| Tablet | 761 a 900 px | Índice lateral oculto abaixo de 900 px |
| Desktop | acima de 900 px | Cena completa, índice fixo à direita, cartão à esquerda |

- Container `.wrap`: largura máx. 1100 px, margem lateral `clamp(14px, 4vw, 36px)`, respiro final de 120 px.
- Herói: `min-height: 100svh`, com 90 px de respiro no topo por causa do cabeçalho fixo.
- Cada item ocupa `min-height: 86vh`, centrado; os pares se deslocam para a direita (até 70 px).
- **O layout da cena (objeto à direita ou acima) segue a proporção da tela** (`largura / altura < 1`), não um breakpoint em pixels.
- A zona de conteúdo fica sempre sobre o lado mais escuro da cena (vinheta à esquerda).
- Teste obrigatório em **360 px** e **1000 px**.
- Áreas de toque de 44 px, com 8 px de espaço entre alvos.

---

## 9. Movimento

O scroll é a câmera. Em cima dele há três tipos de movimento, cada um com regra própria.

| Tipo | O que é | Regra |
| --- | --- | --- |
| **Scroll (principal)** | Câmera no trilho, número fantasma, vidro girando (`z = fase + T·0,18`) | Sempre ativo, suavizado |
| **Ambiente** **[v5]** | Trens, rastros, veículos, retalhos, skates, faixa em rolagem | Decorativo, barato, sem significado de conteúdo. **Para** em reduced-motion. **[proposta]** Controle `movimento: on/off` |
| **Evento** **[v5]** | Listras, explosão do objeto, tremor do cartão, tremor de câmera, RGB-split | Só quando a pessoa **escolhe** ou quando a seleção **assenta**. Sempre finito |

| Situação | Comportamento |
| --- | --- |
| Padrão | Scroll + ambiente + eventos |
| `prefers-reduced-motion: reduce` | Sem suavização do scroll, sem parallax do ponteiro, vidro parado, objetos inteiros (`uExp = 0`), sem tremor, sem RGB-split, sem listras, sem faixa em rolagem, sem trens, rastros, veículos, retalhos nem skates em movimento |
| Aba escondida | Para o loop de render |
| Rolagem programática | Trava o "seguir o scroll" por ~950 ms, para não brigar com ela |

**Em CSS:**

```css
@media (prefers-reduced-motion: reduce) {
  .track, .cell.sel .item, .wipe.go i { animation: none !important; }
  .cw { transition: none; }
}
```

Animar apenas `transform` e `opacity`. Exceção consciente **[v5]**: o tremor `wig` anima `clip-path`, mas só 2 vezes por item. Nunca animar `width`, `height`, `top`, `left`, `filter` ou `box-shadow`.

---

## 10. Seletor de modo (3D, 3D estático ou 2D)

A decisão é tomada **uma vez**, no carregamento.

**[v5]** O HTML decide só por WebGL: se `new WebGLRenderer` falha, adiciona `nogl` ao `body` e interrompe o script.

```css
body.nogl { background: linear-gradient(115deg, var(--ink) 0 52%, var(--dred) 52% 55%, var(--ink) 55%) fixed; }
```

**[proposta]** Seletor com três modos:

```js
const can3D = (() => {
  try { return !!document.createElement('canvas').getContext('webgl2'); }
  catch { return false; }
})();
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const mode = can3D ? (reduce ? '3d-static' : '3d') : '2d';
document.documentElement.dataset.bg = mode;
```

```css
[data-bg^="3d"] .layer { display: none; }   /* esconde as camadas 2D quando há 3D */
[data-bg="2d"] canvas#gl { display: none; }
```

- `3d-static`: renderiza a cena **uma vez**, na posição inicial, e para. Para isso, posicione as instâncias (trens, rastros, veículos, retalhos, skates) antes de parar o loop; ver "Limites conhecidos" na seção 17.
- Em `2d`, no mobile: remova L4 e reduza o deslocamento do parallax para `10vh`.
- Teste cada modo **forçando** `data-bg` manualmente.

---

## 11. Receita 3D com Three.js (Nível 2)

Ordem de construção do v5. Cada passo depende do anterior; **não comece pelos objetos.** Versão: `three@0.160.0` via importmap (jsDelivr).

1. **Trilho da câmera.** `CatmullRomCurve3` com uma âncora por item (de −1 a N). `C(t)` mapeia `t ∈ [−1, N]` para `u ∈ [0, 1]`. Scroll vira `t` com as posições dos cartões **medidas uma vez** (no carregamento, em `load`, em `fonts.ready` e num `ResizeObserver` do container). Nada de ler layout durante o scroll. Suavize: `1 − exp(−4,5 · dt)`.
2. **Faixas paralelas.** `lane(dx, dy, dz)` desloca todas as âncoras. Viaduto `lane(22, 9, −8)`, trilhos a ±0,55, avenida `lane(−5, −11, 2)`. **É ela que garante a ordem.** `frameAt(t)` devolve ponto, tangente e direita, usados pela skyline e pelos fios.
3. **Breu e névoa.** `scene.background` e `Fog` na mesma cor `--ink` (`Fog(8, 40)`). Luz ambiente 0,35, direcional 2,4, ponto vermelho `#ff1a2a` (intensidade 300) que acompanha a câmera.
4. **Skyline.** 56 prédios alternando os lados (distância lateral 11 a 28, altura 18 a 66), numa **única geometria mesclada** com cor por vértice e textura de janelas emissiva (64 × 128, grade 16 × 4, `NearestFilter`). Faróis vermelhos nos topos e até 14 placas de neon verticais (kanji, `REDE`, `24H`, `ESP32`).
5. **Infraestrutura.** Viaduto (tubo + 18 pilares instanciados), 2 trens de 6 vagões em `InstancedMesh`, avenida com 46 rastros (vermelho num sentido, papel no outro) e 9 veículos, 36 vãos de fio em `LineSegments`.
6. **Número fantasma.** Um plano por item com `CanvasTexture` de Anton 430 px. Repinte quando a fonte carregar (`document.fonts.load`).
7. **Vidro.** `buildPane()`: 4 anéis de pontos com ruído, ligados em quadriláteros ou pares de triângulos (40% de chance), ~40% omitidos, extrudados a 0,12, inclinados e **mesclados**. Um anel por item, no trilho um pouco à frente do item.
8. **Objeto-símbolo.** Um por item, em `fit(geometria, 5 a 5,6)`. Geometria `toNonIndexed` com `aCenter` e `aRand` por face. Material com `onBeforeCompile`: sombreamento chapado de três tons (papel, vermelho, preto) por normal de face; cinza `.17` quando inativo (`uAct`).
9. **Frente.** Riscos (`InstancedMesh`, 60), retalhos (36), skates (16) e fios.
10. **Pós-processamento.** `RenderPass` → pontilhado + contorno → acabamento, nessa ordem.
11. **Câmera.** Posição, `up` e `lookAt` da seção 5, com parallax do ponteiro e tremor.

### Estilhaçar ao assentar

Ao contrário do sistema universal (que monta o objeto conforme o scroll), o v5 mantém o objeto **inteiro** e o **estilhaça quando a seleção assenta**; ele se recompõe sozinho.

```js
// seleção assenta 140 ms depois do evento "notechange"
solids[i].userData.burst = 1;              // e shake = glitch = 1 se não for reduced-motion
// por quadro
burst *= Math.exp(-2.6 * dt);              // recompõe
u.uExp.value = reduce ? 0 : near * .015 + burst * 1.2;
u.uAct.value = Math.min(1, near * 1.3);    // 0 = cinza, 1 = cor
```

```glsl
// vertex shader, por face (aRand escalona a saída de cada peça)
float ee = uExp * uExp * 1.2;              // o quadrado mantém o objeto inteiro quando uExp é pequeno
vec3 dir = normalize(aCenter + vec3(.001));
vec3 rel = rotAxis(vec3(aRand - .5, .6, 1. - aRand), ee * (1. + aRand * 2.) * 2.5) * (position - aCenter);
transformed = aCenter + dir * ee * (1.2 + aRand * 2.8) + rel * (1. - .2 * ee);
```

```glsl
// fragment: toon de 3 tons pela normal de face; aleatório quando desmontado
vec3 toon = nl > .5 ? PAPEL : (nl > -.05 ? VERMELHO : PRETO);
```

### Modelos externos

Caminhão e moto são **GLB do Kenney (MIT) embutidos em base64** (~90 KB e ~95 KB). O `GLTFLoader` faz `parse` do buffer, junta as malhas numa geometria só, e um `LoadingManager` troca qualquer textura por um GIF de 1 px (assim não há erro `Couldn't load texture`). Se o parse falha, o caminhão cai para uma geometria de caixas (`mkTruckFB`). Torre, metrô, skate e torre-pérola são **geradas por código**. Anote a orientação de cada modelo (qual eixo é o comprimento) e rotacione na montagem.

### Pós-processamento em dois shaders

1. **Pontilhado + contorno.** Luminância `√(dot(c, [.2126, .7152, .0722]))`. Grade de pontos a 45° (`a = .7853`), célula `5 · DPR`. Três tons: breu `(.02,.02,.025)`, vermelho `(.898,.071,.122)`, papel `(.949,.929,.894)`. Contorno por diferença de luminância com limiar `.34`, pintado de papel.
2. **Acabamento.** RGB-split pela velocidade do voo (cópia deslocada em vermelho), **vinheta à esquerda** (`×mix(.5,1,smoothstep(0,.6,x))`) e **grão** (`±.035`).

**Teste de organização:** desligue o pontilhado (tecla `h`). Se a cena não continua legível, o 3D está escondido pelo efeito, não organizado.

---

## 12. Desempenho

| Medida | Valor | Por quê |
| --- | --- | --- |
| Leituras de layout durante scroll | 0 | `getBoundingClientRect` força layout; meça uma vez e use `ResizeObserver` |
| DPR máximo | 1,5 | Pixels extras custam mais que ganham com pontilhado |
| `antialias` | desligado | O pontilhado já quebra as bordas |
| `powerPreference` | `high-performance` | Pede a GPU dedicada |
| Escalas de resolução | 1, 0,8, 0,65, 0,5 | Passos pequenos, com verificação |
| Janela de medição | 45 quadros | Evita decidir por ruído |
| Limiares | baixa acima de 27 ms; sobe abaixo de 17,5 ms; trava de 6 s | Histerese: lacuna entre descer e subir |
| Aquecimento | 90 quadros ignorados; quadros acima de 250 ms descartados | Compilação de shaders não conta |
| Redimensionar | debounce de 140 ms; ignora mudança de altura menor que 120 px | Barra de URL do celular não recria alvos de render |
| Malhas | Prédios, faróis, vidro, vigas e fios mesclados; riscos, retalhos, skates, trilhos, trens, pilares e veículos em `InstancedMesh` | Poucas draw calls (estimativa por leitura do código: 45 a 50; **não medido**) |
| Sombra do cartão | `::after` com `clip-path` | `drop-shadow` repinta todo quadro |
| Granulação | No shader | `div` com `mix-blend-mode` é cara |
| Controles manuais | `qualidade: auto / baixa / alta`, `pontilhado: on / off` | Quem sabe mais que o medidor decide |

**Qualidade adaptativa, com ressalvas.** Reduzir resolução só ajuda se o gargalo for preenchimento de pixels (não vértices nem draw calls). Use histerese, confira se o FPS realmente melhorou, trave novas reduções por um tempo e ofereça controle manual.

**No 2D:** anime só `transform`. Imagens em SVG ou formatos leves, `loading="lazy"` abaixo da dobra.

**Orçamentos de partida (ajuste por projeto):** JS inicial do Nível 0 e 1 abaixo de 100 KB comprimido; Nível 2 abaixo de 500 KB **sem** modelos; LCP abaixo de 2,5 s em rede 4G. O v5 inteiro tem ~300 KB, dos quais ~185 KB são os dois GLB em base64.

> **O que nunca foi medido:** o FPS em GPU real. Antes de publicar, meça em um celular de entrada e em um notebook sem placa dedicada.

---

## 13. Acessibilidade

- **Fundo decorativo.** Canvas, listras, faixa e HUD têm `aria-hidden="true"`; o canvas e as listras têm `pointer-events:none`.
- **Status nunca só por cor.** Glifo + texto; item ativo com `▶` além da cor **[proposta]**. No v5 o item ativo é marcado por `aria-current` no índice, além da cor e do tamanho.
- **Texto sobre superfície opaca**, com os contrastes da seção 4.4.
- **Letras recortadas.** Versão visual `aria-hidden`, texto real em `.sr` (visualmente oculto, lido por leitor de tela).
- **Cartões.** `article` com `tabindex="0"` e `aria-label="Nota N: título"`; lista semântica (`ul`/`ol`); botões do índice com `aria-label`.
- **Teclado.** `j`/`k` ou `↓`/`↑` navegam, `Enter`/`Espaço` abrem, `Esc` volta ao topo, `h` liga/desliga o pontilhado. Foco visível de 3 px em `--paper`. Ao escolher por teclado, o foco vai para o cartão e a rolagem acompanha, travando a seleção automática por ~950 ms.
- **Alvos de toque** de 44 px.
- **Movimento.** WCAG 2.3.3 (AAA) pede que animação por interação possa ser desligada; parallax e movimento por scroll podem causar reações vestibulares. Por isso `prefers-reduced-motion` e, **[proposta]**, o controle `movimento`.
- **Som.** Desligado por padrão, com `aria-pressed`.
- **Sem WebGL / sem JS.** Classe `nogl` troca o fundo por degradê diagonal CSS; o conteúdo completo continua disponível.
- **Idioma e leitura.** `lang="pt-BR"`, `<title>` por página, hierarquia de títulos real, links com texto descritivo.
- **Formulários.** Rótulo visível, erro em texto, `aria-describedby` ligando a mensagem ao campo.

---

## 14. Receita de implementação

Construa nesta ordem. Cada passo funciona sozinho antes do próximo.

1. **Tokens e tipografia** (seção 4). Nenhuma cor solta depois disso.
2. **Conteúdo e componentes em HTML puro:** cabeçalho, herói, faixa, lista de cartões, índice, rodapé. A página já precisa ser legível e navegável por teclado.
3. **Fundo 2D** com as camadas L0 a L6 e parallax CSS **[proposta]**. Este é o modo `2d` final.
4. **Seletor de modo** (seção 10), gravando `data-bg` no `<html>`.
5. **Cena 3D** (seção 11), só se `data-bg` for `3d` ou `3d-static`.
6. **Pós-processamento:** pontilhado, contorno, RGB-split, grão, vinheta.
7. **Modelos** em base64 com fallback por geometria e créditos no rodapé.
8. **Eventos:** listras, estilhaçar ao assentar, tremor, qualidade adaptativa.
9. **Revisão** com o checklist (seção 16) e o teste do olho semicerrado.

Para projetos de Nível 0 ou 1, pare no passo 2 ou 3.

### Estrutura do arquivo **[v5]**

```text
<canvas id="gl" aria-hidden>          fundo 3D
<div class="wipe" aria-hidden>        4 listras de transição
<header class="top">                  logo · links · toggles (som, qualidade, pontilhado)
<ol class="idx">                      índice lateral 01..N
<main class="wrap">
  <section class="hero">              plaquinha-rótulo · plaquinha · manchete · lead · botões
  <div class="band" aria-hidden>      faixa diagonal
  <ul class="items">                  um <li class="cell"> > <article class="cw"> > <div class="item">
<footer class="foot">                 atalhos · aviso · créditos
<div class="hud" aria-hidden>         numeral · objeto
<script>                              conteúdo, seleção, teclado, som, medição de posições
<script type="module">                cena Three.js, pós-processo, qualidade adaptativa
```

O primeiro script expõe `window.JD = { cells, centers }` e dispara o evento `notechange`; o módulo da cena só **lê** esse estado. Assim o conteúdo funciona mesmo que a cena falhe.

---

## 15. Anti-padrões

| Não faça | Por quê | Faça |
| --- | --- | --- |
| Girar elementos ao acaso fora da camada da frente | Parece bagunça, não colagem | Inclinações pequenas e constantes; rotação solta só em retalhos e skates |
| Mais de um acento | Perde o "uma coisa grita" | Um acento; hierarquia por contraste e escala |
| Texto direto sobre a cena | Contraste imprevisível | Cartão, plaquinha ou painel opaco |
| Cartão em repouso a 50% de opacidade sobre cena clara | O contraste cai a 3,6:1 ou menos (4,62 no melhor caso) | Repouso com opacidade ≥ 0,85 ou cor opaca mais apagada |
| Sombras com blur | Quebram a linguagem de recorte e custam performance | Sombra dura deslocada, `text-shadow: 3px 3px 0` |
| Cantos arredondados | Linguagem de UI genérica | Recorte `--cut-card` e `clip-path` |
| Letras recortadas em texto corrido | Ilegível | Só em logo e plaquinha |
| Loop sem parar em reduced-motion | Viola a regra de movimento | Tudo ambiente atrás de `prefers-reduced-motion` |
| Explosão ou tremor a cada item que passa durante o scroll | Vira ruído | Só quando a seleção assenta (140 ms) |
| `--red` em texto pequeno sobre breu (4,31) ou sobre papel (4,06) | Reprova contraste | `--red-text` |
| `--dred` como texto | 1,65:1 | Só sombra e fundo decorativo |
| `#000` puro como fundo | Perde o tom da cena; fog e fundo deixam de combinar | Breu `#050505` em fundo e névoa |
| Cinza de cena mais claro que `#4a4a4a` | Prédio compete com o foco | Cinzas de cena da seção 4.1 |
| Status só por cor | Exclui quem tem daltonismo | Glifo + texto |
| Efeito escondendo cena desorganizada | Falha no teste do pontilhado | Organizar primeiro, estilizar depois |
| Cores fixas no JavaScript da cena | Troca de preset exige caçar hex no código | Ler os tokens uma vez no boot |
| Copiar logo, fonte, personagem de jogo ou marca | Direito autoral | Só técnicas e estética |
| Ler layout a cada frame | Jank | Cache e `ResizeObserver` |
| Dois focos competindo | Olho não sabe onde ir | Um foco; o resto aponta para ele |

---

## 16. Checklist de entrega

**Sistema**
- [ ] Só tokens no CSS dos componentes; tema e acento trocam sem editar componentes.
- [ ] Preset de acento medido: `--on-red` sobre `--red` e `--red-text` sobre `--ink` e `--card`, todos ≥ 4,5:1.
- [ ] Texto pequeno de acento usa `--red-text`; `--red` só em formas e texto grande.
- [ ] `--ink`, `--fog` e `scene.background` com o mesmo valor.
- [ ] Letras recortadas só em logo e plaquinha, com `aria-hidden` e texto real em `.sr`.
- [ ] Nenhum ativo, logo, personagem ou fonte original de jogo ou marca.

**Composição**
- [ ] Teste do olho semicerrado: o foco continua sendo a primeira coisa vista.
- [ ] Um ponto focal único; conteúdo à esquerda, objeto à direita.
- [ ] Viaduto no alto, avenida embaixo, prédios nos lados.
- [ ] Todas as faixas longas alinhadas ao trilho da câmera.
- [ ] Orçamento da seção 5 respeitado; cinza de cena ≤ `#4a4a4a`.
- [ ] Item ativo marcado em todos os lugares (7.5), com marca além da cor.

**Movimento e modos**
- [ ] Explosão, tremor e RGB-split só quando a seleção assenta.
- [ ] `prefers-reduced-motion` honrado: cena posicionada uma vez, sem animação contínua e **sem instâncias empilhadas na origem**.
- [ ] Modo 3D, 3D estático e 2D testados (forçando `data-bg`).
- [ ] Sem WebGL a página mostra o fallback, sem erro no console.

**Qualidade**
- [ ] Desempenho medido em celular real, com qualidade adaptativa funcionando.
- [ ] Navegação por teclado (`j`, `k`, `Enter`, `Espaço`, `Esc`, `h`) e foco visível.
- [ ] Testado em 360 px e 1000 px, em retrato e paisagem.
- [ ] Fontes com fallback; legível se o Google Fonts falhar; kanji e acentos testados.
- [ ] Conteúdo completo disponível sem JavaScript e sem WebGL.
- [ ] Créditos de modelos 3D e ícones de terceiros no rodapé.

---

## 17. Lições registradas no código (v5)

O HTML não traz um histórico de versões, mas os comentários do código registram decisões e correções. Esta tabela só reúne o que está lá.

| Sintoma | Causa | Correção registrada no código |
| --- | --- | --- |
| Sombra do cartão repintando a cada quadro | `filter: drop-shadow` num elemento com `clip-path` | Pseudoelemento `::after` com o mesmo recorte |
| Explosão e tremor disparando em itens que só passam | Evento ligado à troca de item durante o scroll | Dispara 140 ms **depois** que a seleção assenta |
| Seleção brigando com a rolagem programática | `scrollIntoView` + "seguir o scroll" | `lockScroll` de ~950 ms |
| Jank no scroll | Leitura de layout por quadro | Posições medidas uma vez, `ResizeObserver` |
| Barra de URL do celular recriando alvos de render | `resize` a cada mudança de altura | Debounce de 140 ms e limite de 120 px |
| Qualidade ruim por picos de compilação | Shaders compilando nos primeiros quadros | Aquecimento de 90 quadros e descarte de `dt > 0,25` |
| Erro de textura externa nos modelos Kenney | GLB com textura referenciada | `LoadingManager` que troca texturas por GIF de 1 px |
| Item 01 sem marca no carregamento | Seleção inicial igual ao índice atual | Índice começa em `−1` |
| Fonte nova mudando o tamanho das posições | Medição antes da fonte carregar | Medir de novo em `fonts.ready` e em `load` |

**Limites conhecidos** (observados na leitura do código; **não testados** em navegador):

- **Reduced-motion e instâncias.** Retalhos, skates, trens, rastros e veículos só recebem matriz dentro do bloco `if(!reduce)`. Com movimento reduzido eles ficam na matriz identidade, ou seja, na origem. Corrija posicionando uma vez antes de parar.
- **Cartão em repouso.** A opacidade 0,5 deixa o contraste dependente do que passa atrás (seção 4.4).
- **Contraste do vermelho.** `--red` sobre breu é 4,31, abaixo de 4,5 para texto pequeno. O v5 só o usa em texto grande, mas qualquer componente novo precisa de `--red-text`.
- **Cores fixas no JS.** Trocar de preset exige editar a cena.
- **HUD `aria-hidden`.** O estado atual só chega a leitor de tela pelo `aria-current` do índice.
- **Selo e comando.** O v5 não tem glifo no selo nem linha de comando.
- **Título.** O `<title>` do arquivo diz "v4" e o nome do arquivo diz "v5".
- **FPS em GPU real** nunca foi medido.

**Princípio que ficou:** o caos só funciona quando é organizado. Toda forma do fundo deve apontar para o foco, e o vidro quebrado só emoldura, nunca esconde.

### Decisões desta versão (para consulta)

| Ponto | Decisão |
| --- | --- |
| Cor de acento | Um acento único em todo o sistema, incluindo a cena 3D, como token `--red*` |
| Fundo | Breu `#050505` na página, na névoa e no fundo da cena |
| Superfície do conteúdo | Cartão escuro em repouso; cartão de papel para o item em foco |
| Fundo em movimento | 3D é a camada principal; sem WebGL entra o degradê diagonal (Nível 0) |
| Movimento | Scroll + ambiente + eventos curtos; tudo para em reduced-motion |
| Letras recortadas | Só em logo e plaquinha, nunca no cartão em foco |
| Objeto-símbolo | Estilhaça ao assentar a seleção, em vez de montar pelo scroll |

---

## 18. Como usar este documento com IA (Codex, Claude Code etc.)

Cole o trecho abaixo no `AGENTS.md`, `CLAUDE.md` ou no início do prompt, junto com este arquivo.

```md
# Direção de arte: Colagem Urbana, versão Noite

Siga DESIGN_SYSTEM_COLAGEM_URBANA_NOITE.md.

- Nível de adoção deste projeto: [0 núcleo | 1 camadas 2D | 2 cena 3D]
- Preset de acento: [vermelho | rosa | laranja | azul]
- Tema padrão: [breu | papel]
- Vocabulário: Item = [...], Selo de status = [...], Objeto-símbolo = [...]

Regras inegociáveis:
1. Só tokens do documento. Nenhuma cor solta, nem no JavaScript da cena.
2. Um foco por tela; todo o resto aponta para ele.
3. Texto sempre sobre superfície opaca (cartão, plaquinha, barra).
4. Sombra dura, sem blur; cantos cortados, sem arredondamento.
5. Fundo e névoa na mesma cor (--ink). Nunca #000.
6. Texto pequeno de acento usa --red-text, nunca --red.
7. Status em glifo + texto, nunca só cor.
8. Eventos (explosão, tremor, listras) só quando a seleção assenta ou a pessoa escolhe.
9. Respeite prefers-reduced-motion; o conteúdo funciona sem JS, sem WebGL e sem fontes externas.
10. Nada de ativos, fontes, logos ou personagens de jogos ou marcas.
11. Ao terminar, rode o checklist da seção 16 e o teste do olho semicerrado.
```

Skills úteis (de terceiros; confirme caminhos e versões na sua ferramenta): `frontend-design` (anthropics/skills), `web-design-guidelines` (vercel-labs/agent-skills), `ui-ux-pro-max` (nextlevelbuilder), e skills `threejs-*` para o Nível 2.

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
- *Design System: Colagem Urbana (versão universal)*: estrutura, princípios, níveis de adoção, regras de contraste e acessibilidade.
- `jardim-colagem-3d-v5.html` (Jardim digital: colagem 3D v5): paleta, tipografia, cena, componentes, pós-processo, valores de desempenho e todos os itens marcados **[v5]**.

**Créditos de modelos e bibliotecas**
- Caminhão e moto: Kenney (kenney.nl, Starter Kits), licença MIT.
- Torre de transmissão, metrô, skate, torre-pérola, prédios e vidro: geometria gerada por código.
- Three.js `0.160.0` via jsDelivr (importmap).
- Fontes via Google Fonts: Anton, Playfair Display, Special Elite, Courier Prime (licença OFL). Em qualquer projeto novo, liste os créditos no rodapé.

**Aviso:** esta estética é inspirada em jogos e cartazes de terceiros. Use em projetos próprios; não reproduza logos, personagens nem imagens de nenhum deles. Os contrastes e os presets foram calculados pela fórmula WCAG 2.x; os valores de qualidade adaptativa vêm do v5 e precisam de validação em celular real. Os itens **[proposta]** não foram testados.
