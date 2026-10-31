# WASTELAND_DESIGN.md

Especificação de design inspirada na identidade visual de *Tony Hawk's American Wasteland* (PS2, 2005): capa, logo e menu do jogo. Escrita para que uma IA (ou pessoa) reproduza **a versão clara e a versão dark** de um blog/site, mantendo a base TUI do projeto "Jardim digital" (glifo de estágio, comando em cada nota, índice lateral, rodapé de teclas).

Implementação de referência: a página publicada "Jardim digital: mais 6 direções", direções 5 (clara) e 6 (dark). Se houver conflito entre este texto e a referência, a referência vale para o que está visível, e este texto vale para as regras e justificativas.

---

## 0. Como a IA deve usar este documento

1. Leia as seções 2 a 5 e monte os tokens (CSS custom properties) antes de qualquer componente.
2. Construa os componentes da seção 6 usando só os tokens, sem cores soltas.
3. Monte o fundo (seção 7) como camadas separadas, com parallax e fallback.
4. Use ícones só das bibliotecas da seção 8, inline, e os SVGs próprios da seção 9.
5. Rode o checklist da seção 11 antes de entregar.

Regras gerais:
- Tudo que é só enfeite (respingos, olho, skyline, palmeiras, "LOS ANGELES" desbotado) é `aria-hidden="true"` e `pointer-events:none`.
- Nenhuma informação pode depender só de cor. O estágio da nota é sempre glifo + texto (`○ semente`, `◐ broto`, `● árvore`), e a nota ativa tem marca própria (faixa lateral, `▶`, cor).
- Respeite `prefers-reduced-motion` e `prefers-color-scheme`.

---

## 1. O que a pesquisa mostrou (e o que ela não mostrou)

Fatos confirmados em fontes:
- O jogo é da Neversoft, lançado em outubro de 2005, passa em Los Angeles e é um mundo aberto sem tempo de carregamento. Foi o primeiro da série em que dava para andar de BMX na campanha toda.
- A história gira em torno do caderno de desenhos da Mindy e do zine que ela publica, chamado "American Wasteland".
- Segundo o Punknews, o jogo foi desenhado em torno de Los Angeles nos anos 70 e 80. A trilha é feita de covers de punk e hardcore clássico, por bandas emo e pop punk da época (My Chemical Romance, Fall Out Boy, Thursday, entre outras).
- Sobre a arte do encarte da trilha, o Punknews diz que imita o *London Calling*, do The Clash. A Wikipédia cita o disco homônimo do Clash. As fontes divergem, então não use isso como fato em texto do site.
- Anúncios da época usam a frase "get a taste of no load times" e a legenda "unlimited skating in the vast wasteland of skate culture, L.A.".

Fatos vindos dos prints enviados pelo usuário (capa, contracapa, menu):
- Paleta: branco sujo e cinza, preto de tinta, **rosa-choque** e respingos de **verde neon**. Não há lilás nem roxo.
- Logo: barra preta de tinta com borda irregular; "TONY HAWK'S" em stencil branco; "AMERICAN WASTELAND" em letras recortadas de revista, em blocos rosa e brancos, com uma estrela no lugar do A.
- Menu: tiras pretas levemente tortas, texto em maiúsculas com leve deformação, opção ativa em rosa, parede grafitada ao fundo, olho de monstrinho, cartazes colados.
- Capa: fotografia em preto e branco com raios, palmeiras, viaduto em diagonal, skyline de LA em rosa, letreiro HOLLYWOOD, "LOS ANGELES" desbotado, respingos rosa e verde, papel riscado.

Não foi possível confirmar:
- A fonte original do logo. As fontes abaixo são aproximações do Google Fonts, não o original.
- Valores exatos de cor. Os hex deste documento foram amostrados a olho dos prints e ajustados para contraste.

---

## 2. Princípios visuais

1. **Fotocópia suja com tinta de spray.** Base clara e granulada, preto pesado, uma única cor berrando (rosa) e uma cor de acento mínima (verde, só em respingos).
2. **Tiras, não cartões.** Conteúdo vive em faixas pretas quase retas, com cortes irregulares (clip-path) e rotação de menos de 1 grau.
3. **Letras recortadas só no título.** O recorte (ransom) é reservado ao logo e à manchete. No resto, texto legível.
4. **Profundidade de cartaz de rua.** Fundo em camadas (skyline, palmeiras, viaduto, respingos) que se mexem em velocidades diferentes.
5. **Uma coisa barulhenta por vez.** Se a manchete e o fundo estão carregados, as notas ficam limpas.

O que **não** é este estilo: neon azul, fundo preto puro, gradiente suave, cantos arredondados grandes, sombras borradas.

---

## 3. Tokens

### 3.1 Claro (padrão)

```css
:root, [data-theme="light"] {
  --paper:      #f5f4f0;  /* fundo */
  --ink:        #111111;  /* texto principal e contornos */
  --strip:      #111111;  /* tira da nota */
  --strip-ink:  #ffffff;  /* texto sobre a tira */
  --strip-mute: #d8d8d8;  /* comando e metadados sobre a tira */
  --pink:       #e6008a;  /* blocos grandes, respingos, sombra dura */
  --pink-ink:   #d6007d;  /* rosa para TEXTO pequeno ou fundo com texto branco */
  --pink-on-dark:#ff2fa3; /* rosa sobre tira preta */
  --green:      #3dff2e;  /* só respingos, nunca texto */
  --white:      #ffffff;
  --ghost:      rgba(0,0,0,.05);   /* LOS ANGELES desbotado */
  --halftone:   rgba(17,17,17,.20);
  --scratch:    rgba(0,0,0,.04);   /* riscos diagonais */
}
```

### 3.2 Dark

```css
[data-theme="dark"] {
  --paper:      #221e26;  /* carvão arroxeado, nunca preto puro */
  --ink:        #f1efe8;
  --strip:      #060507;
  --strip-ink:  #ffffff;
  --strip-mute: #d8d8d8;
  --pink:       #e6008a;
  --pink-ink:   #d6007d;
  --pink-on-dark:#ff2fa3;
  --green:      #3dff2e;
  --white:      #ffffff;
  --ghost:      rgba(255,255,255,.05);
  --halftone:   rgba(255,255,255,.12);
  --scratch:    rgba(255,255,255,.04);
}
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) { /* repita os valores de [data-theme="dark"] */ }
}
```

Regras de troca: a página segue `prefers-color-scheme` por padrão; um atributo `data-theme` no `<html>` força um dos dois. No dark, as tiras ganham sombra dura rosa (`drop-shadow(5px 5px 0 var(--pink))`) para se destacarem do fundo, e botões, índice e olho ganham contorno claro.

### 3.3 Contraste medido (WCAG 2.x)

| Par | Razão | Uso |
|---|---|---|
| `#111` sobre `#f5f4f0` | 17,16 | texto no claro |
| `#fff` sobre `#111` | 18,88 | texto na tira |
| `#f1efe8` sobre `#221e26` | 14,24 | texto no dark |
| `#fff` sobre `#060507` | 20,34 | texto na tira dark |
| `#ff2fa3` sobre `#060507` | 5,99 | título ativo na tira dark |
| `#ff2fa3` sobre `#111` | 5,56 | título ativo na tira clara |
| `#d8d8d8` sobre `#060507` | 14,27 | comando na tira |
| `#fff` sobre `#e6008a` | **4,44** | **abaixo de 4,5: só texto grande (24px+ ou 19px negrito+)** |
| `#e6008a` sobre `#f5f4f0` | **4,03** | **só decoração ou texto grande** |
| `#fff` sobre `#d6007d` | 5,05 | texto pequeno em fundo rosa |
| `#d6007d` sobre `#f5f4f0` | 4,59 | texto pequeno rosa no claro |

Para texto pequeno rosa ou texto branco em fundo rosa (selo do estágio, botão), use `--pink-ink` (`#d6007d`). O `--pink` (`#e6008a`) fica para blocos grandes, respingos e a manchete.

---

## 4. Tipografia

| Papel | Fonte (Google Fonts) | Peso | Observação |
|---|---|---|---|
| Logo, manchete, botões | Big Shoulders Stencil Display | 800 | aproxima o stencil do logo; maiúsculas |
| Títulos das notas | Londrina Solid | 400 | maiúsculas, `letter-spacing:.05em` |
| Corpo | Courier Prime | 400 e 700 | cara de fotocópia, boa leitura |
| Comando, rodapé, metadados | JetBrains Mono | 400 e 700 | base TUI |

```html
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Big+Shoulders+Stencil+Display:wght@800&family=Londrina+Solid:wght@400;900&family=Courier+Prime:wght@400;700&family=JetBrains+Mono:wght@400;700&display=swap">
```

Fallbacks obrigatórios: `Impact, sans-serif` para as duas display, `monospace` para as outras.

Tamanhos: manchete `clamp(30px, 5.6vw, 52px)`, logo 30px, título de nota `clamp(20px, 3vw, 26px)`, corpo 16px com `line-height:1.55`, comando 12px, selo 13px negrito.

---

## 5. Layout

- Container máximo 1000px. Padding do palco `22px clamp(14px, 4vw, 40px)`.
- Grade principal: coluna do índice de 170px + coluna de notas. Abaixo de 760px vira uma coluna.
- Lista de notas: 1 coluna no mobile, 2 colunas a partir de 760px, e a **primeira nota ocupa as duas colunas**.
- Ordem: nav, hero (manchete, frase, botões, comando), corpo (índice + notas), rodapé de teclas.
- Teclas: `j` e `k` navegam, `Enter` ou `Espaço` abrem, teclas numéricas trocam de variação quando houver seletor.

---

## 6. Componentes

### 6.1 Logo e manchete (letras recortadas)

A manchete fica sobre uma **barra de tinta**: fundo `--strip`, padding `14px 26px 18px`, borda irregular por clip-path:

```css
.hl { background: var(--strip); clip-path: polygon(0 5%, 3% 0, 100% 3%, 98% 100%, 2% 95%); }
```

Dentro dela, as **três primeiras palavras** são stencil branco (`.st`) e o resto vira letras recortadas (`.r`), uma por caractere, ciclando 4 estilos:

```css
.r  { display:inline-block; padding:0 .12em; margin:.04em .02em; line-height:1.1;
      font:800 1em "Big Shoulders Stencil Display", Impact, sans-serif; box-shadow:2px 2px 0 #111; }
.r0 { background:var(--pink);  color:#fff;          text-transform:uppercase; }
.r1 { background:#fff;         color:var(--pink);   transform:rotate(-3deg); }
.r2 { background:#fff;         color:#111;          text-transform:uppercase; transform:rotate(2deg); }
.r3 { background:var(--pink);  color:#fff;          transform:rotate(-1.5deg) translateY(-2px); }
.w  { display:inline-block; white-space:nowrap; margin:0 .14em; }
.st { display:inline-block; margin:0 .2em; font:800 1em "Big Shoulders Stencil Display", Impact, sans-serif;
      letter-spacing:.05em; text-transform:uppercase; color:#fff; }
```

Geração em JS (acessível: a versão visual é `aria-hidden`, e o texto real fica num `.sr`):

```js
const rn = (t, k) =>
  `<span aria-hidden="true">` +
  t.split(" ").map((w, wi) => wi < k
    ? `<span class="st">${w}</span>`
    : `<span class="w">` + [...w].map((c, i) => `<span class="r r${(i + wi) % 4}">${c}</span>`).join("") + `</span>`
  ).join(" ") + `</span><span class="sr">${t}</span>`;
// manchete: rn(texto, 3)   logo: rn("jardim", 0)
// .sr { position:absolute; left:-9999px }
```

Os blocos `.r1` e `.r2` são brancos e precisam do `box-shadow` escuro para não sumirem sobre o fundo claro. No dark, o `box-shadow` pode virar `#000`.

### 6.2 Nota (tira do menu)

- Fundo `--strip`, texto `--strip-ink`, padding `20px 28px 22px 34px`.
- Corte irregular, alternando por `nth-child`:
  - ímpares: `clip-path: polygon(0 5%, 100% 0, 98% 95%, 1% 100%)`
  - pares: `clip-path: polygon(1% 0, 100% 4%, 99% 100%, 0 94%)`
- Rotação: pares `.7deg`, ímpares `-.6deg`.
- Título: Londrina Solid, maiúsculas, `letter-spacing:.05em`.
- **Ativa:** faixa lateral `box-shadow: inset 10px 0 0 var(--pink-on-dark)` e título em `--pink-on-dark`, selo com `▶`.
- No dark: contorno interno `box-shadow: inset 0 0 0 2px #4a4452` (a ativa mantém a faixa rosa) e `filter: drop-shadow(5px 5px 0 var(--pink))` no wrapper `.cell` (o filtro vai no pai, porque o clip-path do filho cortaria a sombra).

### 6.3 Selo do estágio (adesivo de papel)

Pequeno rótulo branco, texto `#111`, `padding:0 10px`, `transform:rotate(-2deg)`, `box-shadow:2px 2px 0 var(--pink)`. Conteúdo: glifo + nome (`◐ broto`). Ativo: fundo `--pink-ink`, texto branco, prefixo `▶`.

### 6.4 Comando

Linha `$ jardim ler <b>N</b>` em JetBrains Mono 12px, cor `--strip-mute`, opacidade 1. Isso é a base TUI e deve existir em toda nota.

### 6.5 Olho de monstrinho

Adesivo circular no canto superior direito da **primeira nota** (SVG da seção 9). Dark: contorno `--ink`.

### 6.6 Índice lateral

Caixa clara com `border:3px solid #111`, `box-shadow:5px 5px 0 var(--pink)`, `transform:rotate(-1.5deg)`. Dark: fundo `#2d2832`, borda e texto `--ink`.

### 6.7 Botões

Principal: fundo `--pink-ink`, texto branco, `border:3px solid #111`, `box-shadow:4px 4px 0 #111`, Big Shoulders 800 20px, `rotate(-2deg)`. Secundário: sem borda, texto `--ink`, sublinhado de 2px com `text-underline-offset:5px`. Dark: borda `--ink`, sombra `#000`. Altura mínima 44px.

### 6.8 Adesivo da página e chip de comando

Adesivo: fundo branco, texto `#111`, borda 2px, sombra `3px 3px 0 var(--pink)`, `rotate(-3deg)`. Texto sugerido: "sem load, sempre" (eco do anúncio). Chip `$ jardim plantar nova-nota`: fundo `--strip`, texto `--strip-ink`.

### 6.9 Rodapé

Barra `--strip` com `border-top:6px solid var(--pink)` (eco do chão rosa da capa), teclas em `<kbd>` com contorno de 1px, e aviso "sem rastreadores · não pisca".

---

## 7. Fundo e parallax (imitando a capa)

### 7.1 Composição por camadas

Da mais distante para a mais próxima. A velocidade é a fração do scroll aplicada na camada (0 = parada, 1 = acompanha o conteúdo).

| # | Camada | Conteúdo | Velocidade | Claro | Dark |
|---|---|---|---|---|---|
| L0 | Papel | cor `--paper` + riscos diagonais `repeating-linear-gradient(112deg, transparent 0 38px, var(--scratch) 38px 40px)` | 0 | branco sujo | carvão arroxeado |
| L1 | Texto fantasma | "LOS ANGELES" em Big Shoulders 800, 60 a 130px, rotação -3deg, cor `--ghost` | 0.10 | cinza muito claro | branco a 5% |
| L2 | Meio-tom e raios | pontos de meio-tom no canto superior esquerdo (máscara diagonal) e raios finos saindo do alto | 0.20 | pontos `#111` a 20% | pontos brancos a 12% |
| L3 | Skyline e letreiro | skyline de LA (SVG 9.4) e placa HOLLYWOOD | 0.35 | rosa, opacidade .9, junto ao rodapé | rosa, opacidade .55 |
| L4 | Palmeiras | 2 a 3 silhuetas (SVG 9.5), uma maior à direita | 0.55 | `#111` a 85% | `#060507` a 90% com brilho rosa `drop-shadow(0 0 12px #e6008a55)` |
| L5 | Viaduto | diagonal no canto inferior esquerdo (SVG 9.6) em tons de cinza | 0.75 | cinzas médios | cinzas escuros `#3a3440` e `#15121a` |
| L6 | Respingos | rosa e verde (gerador 9.3), alguns pontos soltos que cruzam as outras camadas | 0.90 | rosa e verde cheios | rosa e verde cheios + leve brilho |

Regras:
- A skyline e o viaduto ficam na metade de baixo da tela; o canto superior direito recebe respingos rosa; o verde aparece só em pontos pequenos nas laterais.
- No dark, nunca aplique `mix-blend-mode`; troque as cores diretamente pelos tokens. O resultado precisa ser previsível em qualquer navegador.
- Texto de conteúdo sempre fica em z-index acima do fundo, e a faixa de leitura (as tiras) tem fundo opaco, então o fundo nunca atrapalha a leitura.

### 7.2 Estrutura HTML

```html
<div class="bg" aria-hidden="true">
  <div class="layer" style="--d:.10"> <!-- L1 texto fantasma --> </div>
  <div class="layer" style="--d:.20"> <!-- L2 meio-tom e raios --> </div>
  <div class="layer" style="--d:.35"> <!-- L3 skyline --> </div>
  <div class="layer" style="--d:.55"> <!-- L4 palmeiras --> </div>
  <div class="layer" style="--d:.75"> <!-- L5 viaduto --> </div>
  <div class="layer" style="--d:.90"> <!-- L6 respingos --> </div>
</div>
<main class="content"> … </main>
```

```css
.bg { position:fixed; inset:0; overflow:hidden; z-index:0; pointer-events:none;
      background-color:var(--paper);
      background-image:repeating-linear-gradient(112deg, transparent 0 38px, var(--scratch) 38px 40px); }
.layer { position:absolute; inset:-20vh 0; will-change:transform; }
.content { position:relative; z-index:1; }
```

Se o fundo ficar só dentro de um palco em caixa (como na página de referência), troque `position:fixed` por `position:absolute` dentro do palco e use o scroll da página como timeline do mesmo jeito.

### 7.3 Movimento: CSS puro com fallback

```css
@media (prefers-reduced-motion: no-preference) {
  @supports (animation-timeline: scroll()) {
    .layer { animation: drift linear both; animation-timeline: scroll(root); }
    @keyframes drift {
      from { transform: translate3d(0, calc(var(--d) * 18vh), 0); }
      to   { transform: translate3d(0, calc(var(--d) * -18vh), 0); }
    }
  }
}
```

Fallback em JS para navegadores sem `animation-timeline` (só quando não há preferência de movimento reduzido):

```js
if (!CSS.supports("animation-timeline: scroll()") &&
    !matchMedia("(prefers-reduced-motion: reduce)").matches) {
  let y = 0, ticking = false;
  const layers = [...document.querySelectorAll(".layer")];
  addEventListener("scroll", () => {
    y = scrollY;
    if (!ticking) { ticking = true; requestAnimationFrame(() => {
      layers.forEach(l => l.style.transform = `translate3d(0, ${-y * (+l.style.getPropertyValue("--d")) * .18}px, 0)`);
      ticking = false; }); }
  }, { passive:true });
}
```

Observações de suporte (da pesquisa, com divergência entre fontes): o `animation-timeline` roda no Chrome 115+ e no Safari 26+. Quanto ao Firefox, uma fonte diz que exige flag e outra diz que já tem suporte, então **teste** e mantenha o fallback. Navegador sem suporte ignora a regra e a página aparece estática, o que é aceitável.

Limites de desempenho e conforto:
- Anime só `transform` (nunca `top`, `background-position` ou `filter`).
- Máximo de 6 camadas no desktop; no mobile (`max-width:700px`) remova L2 e L5 e reduza o deslocamento para `10vh`.
- Com `prefers-reduced-motion: reduce`, nenhuma camada se mexe: o fundo fica estático, com as camadas empilhadas na posição inicial.
- Sem parallax em elementos de conteúdo, só no fundo.

### 7.4 Variação por tema

O fundo troca junto com o tema, pelos tokens da seção 3, sem trocar a estrutura. O claro lembra a capa original (alto contraste, preto sobre branco, rosa). O dark vira a mesma cena à noite: silhuetas mais escuras que o fundo, skyline rosa mais apagada, brilhos rosa nas bordas das palmeiras.

---

## 8. Ícones de bibliotecas (SVG)

Use sempre **inline** (copie o `<svg>` para o HTML) com `stroke="currentColor"`, traço de 2px, 20 a 24px, `aria-hidden="true"` quando houver texto ao lado. Não carregue ícones por CDN em páginas publicadas: se a página rodar sob uma política de segurança restrita (como a do Artifact do Claude), a imagem remota é bloqueada.

| Biblioteca | Licença | Atribuição | Ícones úteis (nomes verificados na pesquisa) |
|---|---|---|---|
| **Lucide** | ISC | não obrigatória | `tree-palm` (palmeira), `bike` (BMX), `spray-can` (spray), `terminal`, `search`, `rss`, `scan-eye` e `eye-closed` (família do olho; confirme o `eye` simples antes de usar) |
| **Tabler Icons** | MIT | manter a licença no repositório | `skateboard`, `skateboarding`, `skull`, `spray`, `sparkles`, `spider` |
| **Game Icons** | CC BY 3.0 | **obrigatória** (créditos no site) | `skateboard` e milhares de ícones de jogo; só use se aceitar a atribuição |

Mapeamento sugerido:

| Lugar | Ícone |
|---|---|
| Tag `#terminal` | Lucide `terminal` |
| Tag `#hardware` | Lucide `bike` ou Tabler `skateboard` |
| Tag `#bots` | Tabler `skull` |
| Tag `#diário` | Tabler `spray` ou Lucide `spray-can` |
| Botão RSS | Lucide `rss` |
| Divisor decorativo | Tabler `sparkles` |
| Adesivo "no load" | Tabler `skateboarding` |

Os glifos de estágio (`○ ◐ ●`) **continuam sendo texto**, não ícones, porque são a base TUI e funcionam sem imagem.

---

## 9. SVGs próprios (desenhar, não buscar)

Estes elementos são específicos da capa e não existem nas bibliotecas. Os SVGs abaixo são ponto de partida, e podem ser redesenhados para ficar mais irregulares.

### 9.1 Estrela (substitui o "A" de AMERICAN no logo)

```html
<svg viewBox="0 0 24 24" width="1em" height="1em" aria-hidden="true">
  <polygon points="12,2 15,9 22,9.3 16.5,14 18.2,21 12,17.3 5.8,21 7.5,14 2,9.3 9,9" fill="currentColor"/>
</svg>
```

### 9.2 Olho de monstrinho

```html
<svg viewBox="0 0 48 48" width="48" height="48" aria-hidden="true">
  <circle cx="24" cy="24" r="20" fill="#fff" stroke="#111" stroke-width="3"/>
  <path d="M8 20l6 3M10 32l5-3M36 10l-2 5" stroke="#d1002f" stroke-width="1.5" fill="none"/>
  <circle cx="27" cy="26" r="9" fill="#8a5a2b"/><circle cx="27" cy="26" r="4.5" fill="#111"/>
</svg>
```

### 9.3 Gerador de respingos

Pontos com raio decrescente conforme se afastam do centro. Use semente fixa para o resultado não mudar a cada carga.

```js
function splat(cx, cy, n, color, seed = 7) {
  let s = seed; const rnd = () => (s = (s * 16807) % 2147483647) / 2147483647;
  let out = "";
  for (let i = 0; i < n; i++) {
    const a = rnd() * Math.PI * 2, d = Math.pow(rnd(), 1.6) * 90;
    const r = Math.max(.8, 7 * (1 - d / 100) * rnd() + .8);
    out += `<circle cx="${(cx + Math.cos(a) * d).toFixed(1)}" cy="${(cy + Math.sin(a) * d).toFixed(1)}" r="${r.toFixed(1)}" fill="${color}"/>`;
  }
  return `<svg viewBox="0 0 200 200" aria-hidden="true">${out}</svg>`;
}
// splat(100,100,70,"#e6008a")  e  splat(100,100,12,"#3dff2e",3) para pontos verdes
```

### 9.4 Skyline de Los Angeles (rosa)

```html
<svg viewBox="0 0 400 100" preserveAspectRatio="none" aria-hidden="true">
  <path fill="#e6008a" d="M0 100V70h20V50h14V30h16v20h12V60h18V20h14v40h16V45h20V70h18V35h14V55h20V25h16v45h18V60h20V40h14v30h20V55h18V80h30V100z"/>
</svg>
```

Placa HOLLYWOOD: texto em Big Shoulders 800, branco sobre uma laje rosa inclinada, tamanho pequeno, canto direito da skyline.

### 9.5 Palmeira (silhueta)

```html
<svg viewBox="0 0 120 220" aria-hidden="true">
  <path d="M62 215C60 150 66 100 58 50" stroke="currentColor" stroke-width="6" fill="none" stroke-linecap="round"/>
  <g stroke="currentColor" stroke-width="5" stroke-linecap="round" fill="none">
    <path d="M58 50C40 30 20 34 6 52"/><path d="M58 50C46 24 30 14 12 16"/>
    <path d="M58 50C62 22 80 8 104 12"/><path d="M58 50C78 32 98 38 114 56"/>
    <path d="M58 50C52 66 38 72 24 70"/><path d="M58 50C70 66 86 70 100 66"/>
  </g>
</svg>
```

Cor: `#111` no claro e `#060507` no dark, com a opacidade da tabela 7.1.

### 9.6 Viaduto (diagonal)

```html
<svg viewBox="0 0 400 300" aria-hidden="true">
  <path d="M0 40L380 300H320L0 70z" fill="var(--hw-a, #bdbdbd)"/>
  <path d="M0 70L320 300H260L0 120z" fill="var(--hw-b, #5a5a5a)"/>
  <path d="M0 120L260 300H0z" fill="var(--hw-c, #9a9a9a)"/>
</svg>
```

Dark: `--hw-a:#3a3440; --hw-b:#15121a; --hw-c:#2a2530`.

### 9.7 Fita e papel rasgado

Fita: retângulo de 70x20px, `rgba(230,0,138,.35)`, `rotate(-4deg)`. Papel rasgado: `clip-path: polygon()` com 15 a 20 pontos alternando 0 e 8px na borda inferior (o mesmo recurso usado na versão emo punk).

---

## 10. Movimento e interação

- Hover de botão: deslocar 2px e reduzir a sombra para 2px.
- Seleção de nota: sem animação de entrada; só a troca imediata de estado. Foco visível de 3px com `outline: 3px solid currentColor; outline-offset: 3px`.
- Nada pisca, nenhuma animação em loop. O rodapé diz isso e deve continuar verdadeiro.
- `prefers-reduced-motion: reduce` desliga o parallax e qualquer transição.

---

## 11. Checklist de entrega

- [ ] Claro e dark usam só tokens; nenhuma cor solta no CSS dos componentes.
- [ ] Texto pequeno rosa e texto branco em fundo rosa usam `--pink-ink`.
- [ ] Estágio da nota aparece como glifo + texto; nota ativa tem marca além da cor.
- [ ] Logo e manchete têm `aria-hidden` na versão recortada e texto real em `.sr`.
- [ ] Toda camada decorativa tem `aria-hidden="true"` e `pointer-events:none`.
- [ ] Parallax só com `transform`, com `@supports`, fallback em JS e `prefers-reduced-motion`.
- [ ] Ícones inline, `currentColor`, e atribuição incluída se usar Game Icons.
- [ ] Fontes com fallback; página legível se o Google Fonts falhar.
- [ ] Testado em 360px de largura (uma coluna) e em 1000px.
- [ ] Teclado: `j`, `k`, `Enter`, `Espaço` funcionam; foco sempre visível.
- [ ] Nenhuma frase do site afirma como fato o que a seção 1 marca como incerto (fonte do logo, arte do encarte da trilha).

---

## 12. Limitações conhecidas

- As fontes são aproximações do logo original, que não foi identificado.
- Os SVGs da seção 9 são esquemáticos. Para ficar fiel à capa, redesenhe palmeiras, viaduto e skyline com mais irregularidade, ou use ilustrações próprias.
- O parallax foi especificado com base em documentação e artigos, mas **não foi testado** em todos os navegadores. Verifique especialmente Firefox e Safari.
- Esta marca pertence aos donos do jogo. O documento descreve uma estética inspirada nela para um projeto pessoal. Não reproduza o logo, os personagens nem imagens do jogo em um projeto público ou comercial.
