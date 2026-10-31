# Design system mesclado: Jardim 3D × Wasteland

Oct 26, 2026 · @Diego Vieira

## Resumo

A mescla junta o cenário 3D do Jardim v7 (meio-tom, câmera em perspectiva, ponto de fuga sobre o cartão) com a base do WASTELAND\_DESIGN.md (tiras tortas, letras recortadas, TUI, parallax em camadas, tema claro e dark). O resultado é **um sistema com a paleta do Wasteland (papel sujo, preto de tinta, rosa-choque e verde neon), dois temas e o acento em tokens**, e o 3D é uma camada que pode ser trocada pelas camadas 2D de Wasteland.

**Regra de ouro:** o fundo conta a cidade, a tira conta a nota. Só uma coisa grita por vez, e tudo que está atrás aponta para a tira ou para a manchete.

| Vem de | O que entra |
| --- | --- |
| Jardim v7 | Cena 3D ordenada (céu, horizonte, chão, fileiras), ponto de fuga sobre o cartão, meio-tom e contorno em pós-processo, montagem por scroll, qualidade adaptativa |
| Wasteland | Tiras com corte irregular, manchete em letras recortadas, selo de estágio, comando `$ jardim ler N`, índice lateral, rodapé de teclas, tema claro e dark, parallax 2D, respingos, regras de contraste |
| Novo na mescla | Acento variável (`--hot`), dois temas (Asfalto e Fotocópia), 2D como fallback do 3D, regra de movimento unificada |

O que não muda: nenhum ativo, fonte ou logo de ATLUS, Atari/Activision ou Neversoft. Só técnicas e estética.

## Conflitos e decisões

Os dois sistemas discordam em seis pontos. Cada linha abaixo diz quem ganha e por quê.

| Ponto | Jardim 3D | Wasteland | Decisão da mescla |
| --- | --- | --- | --- |
| Cor de acento | Vermelho `#e11b22` | Rosa-choque `#e6008a` | **Rosa do Wasteland em todo o sistema**, incluindo a cena 3D. O acento segue como token `--hot*`. O verde neon fica só em respingos |
| Fundo | Preto quase puro, névoa vinho `#2b060b` | Claro sujo; dark em carvão arroxeado, "nunca preto puro" | Página clara por padrão. A cena 3D é noturna, com névoa rosada `#2a0a1c`; tiras ficam `#111` ou `#060507` |
| Superfície do conteúdo | Cartão de papel `#f0ece4` com sombra vermelha | Tira preta com corte irregular | As duas existem: tira para lista e navegação, cartão de papel para a nota em foco sobre o 3D, com sombra rosa |
| Fundo em movimento | Cena 3D guiada pelo scroll | Parallax CSS em 6 camadas | 3D é a camada principal; as camadas 2D entram sem WebGL, com movimento reduzido ou em tela pequena |
| Movimento | Câmera e montagem guiadas pelo scroll; trém e tráfego animados | "Nada pisca, nenhuma animação em loop" | Vale a regra mais rígida: movimento só por scroll. Trém e tráfego ficam parados por padrão e só se mexem com o controle "movimento: on" |
| Letras recortadas | Manchete em título normal | Recorte em logo e manchete | Recorte só na manchete e no logo, nunca no cartão em foco |

Dois pontos em que Wasteland já resolvia o que o Jardim deixava solto: o contraste do rosa e do vermelho em texto pequeno, e a ideia de que um selo de estágio nunca depende só de cor.

## Tokens unificados

Os componentes usam só estes nomes. Trocar de tema ou de acento é trocar valores, nunca estrutura.

```css
/* Padrão: paleta Wasteland (rosa-choque + verde neon), tema Fotocópia */
:root, [data-theme="photocopy"] {
  --ink:#111111; --paper:#f5f4f0; --white:#ffffff;
  --strip:#111111; --strip-ink:#ffffff; --strip-mute:#d8d8d8;
  --hot:#d6007d;          /* texto pequeno rosa, fundo de botão com texto branco */
  --hot-on-dark:#ff2fa3;  /* título ativo sobre tira preta */
  --hot-fill:#e6008a;     /* blocos grandes, respingos, cena 3D, manchete */
  --spray:#3dff2e;        /* só respingos, nunca texto */
  --ghost:rgba(0,0,0,.05); --halftone:rgba(17,17,17,.20); --scratch:rgba(0,0,0,.04);
  --fog:#2a0a1c;          /* névoa e horizonte da cena 3D (noite rosada) */
}
/* Tema Asfalto (dark): mesmo rosa, papel carvão arroxeado, tira quase preta */
[data-theme="asphalt"] {
  --paper:#221e26; --ink:#f1efe8; --strip:#060507;
  --ghost:rgba(255,255,255,.05); --halftone:rgba(255,255,255,.12); --scratch:rgba(255,255,255,.04);
}
```

Regra de combinação: a paleta é a do Wasteland nos dois temas. Fotocópia é o padrão da página; Asfalto é o tema usado quando há cena 3D, porque o 3D é uma cena noturna. O acento continua sendo um token (`--hot*`), então trocar a cor depois é trocar três valores.

### Contraste medido (WCAG 2.x)

| Par | Razão | Uso |
| --- | --- | --- |
| `#111` sobre `#f5f4f0` | 17,16 | texto no tema claro |
| `#f1efe8` sobre `#221e26` | 14,24 | texto no Asfalto |
| `#fff` sobre `#111` | 18,88 | texto na tira |
| `#ff2fa3` sobre `#060507` | 5,99 | título ativo na tira dark |
| `#ff2fa3` sobre `#111` | 5,56 | título ativo na tira clara |
| `#fff` sobre `#d6007d` | 5,05 | texto pequeno em fundo rosa |
| `#d6007d` sobre `#f5f4f0` | 4,59 | texto pequeno rosa no papel |
| `#fff` sobre `#e6008a` | **4,44** | **só texto grande (24px+, ou 19px negrito+)** |
| `#e6008a` sobre `#f5f4f0` | **4,03** | **só decoração ou texto grande** |

O rosa `#e6008a` é ótimo para formas e manchete, mas fica abaixo de 4,5:1 como texto pequeno. Por isso há três níveis: `--hot-fill` para formas, `--hot` para texto sobre papel e fundo de botão, `--hot-on-dark` para texto sobre tira. Valores medidos no documento Wasteland (os mesmos aqui).

## Tipografia

As duas famílias de display (Big Shoulders Stencil Display e Londrina Solid) e as duas monoespaçadas de Wasteland valem para o sistema inteiro. O Jardim v7 usava fontes do sistema; a mescla passa a usar esta pilha.

| Papel | Fonte | Peso | Onde |
| --- | --- | --- | --- |
| Logo e manchete | Big Shoulders Stencil Display | 800 | recortes e stencil, maiúsculas |
| Título de nota | Londrina Solid | 400 | tira e cartão em foco, `letter-spacing:.05em` |
| Corpo | Courier Prime | 400, 700 | texto do cartão, 16px, `line-height:1.55` |
| Comando, rótulos, rodapé | JetBrains Mono | 400, 700 | base TUI, 12px |
| Numeral grande | Londrina Solid, só contorno | 400 | o "02" do cartão, `-webkit-text-stroke` |

Fallbacks: `Impact, sans-serif` para as duas display e `monospace` para as outras. O texto crítico sempre aparece em mono ou sem serifa se o Google Fonts falhar. Fonte com kanji (se usar caracteres japoneses como textura) precisa de fallback próprio, porque nenhuma das quatro cobre CJK; teste antes.

As fontes são aproximações do estilo; nenhuma é a original de qualquer jogo.

## Pilha de camadas

O fundo é sempre a mesma pilha de sete níveis, do mais distante ao mais próximo. Com WebGL, as camadas L1 a L5 viram **uma cena 3D** com a ordem do Jardim v7; sem WebGL, com movimento reduzido ou em tela estreita, as mesmas camadas vêm como SVG com parallax de Wasteland.

| Nível | Papel | Versão 3D (Jardim v7) | Versão 2D (Wasteland) |
| --- | --- | --- | --- |
| L0 | Papel | `scene.background` e `Fog(--fog)` | `--paper` + riscos diagonais |
| L1 | Céu e texto fantasma | Domo com gradiente vertical e sol em fenda | "LOS ANGELES" desbotado, v=0.10 |
| L2 | Luz e raios | Raios radiais alinhados à tangente, meio-tom em pós-processo | Meio-tom e raios CSS, v=0.20 |
| L3 | Cidade | Fileiras rítmicas de prédios, viaduto e trens, modelos assados | Skyline SVG rosa, v=0.35 |
| L4 | Meio-plano | Postes, fios, tráfego, objetos urbanos | Palmeiras SVG, v=0.55 |
| L5 | Chão | Fitas de pista, calçadas, bordas em `--hot-fill`, tracejado | Viaduto diagonal SVG, v=0.75 |
| L6 | Respingos e recortes | Retalhos de papel no céu (10 peças) | Respingos rosa e verde, v=0.90 |
| UI | Tiras e cartão | HTML sobre o canvas, z-index acima | igual |

### Regras da composição 3D

1. Ponto de fuga sobre o cartão ou a tira ativa: `camera.setViewOffset(w,h,Math.round(w*.17),0,w,h)` no desktop, 0 no mobile.
2. A cor da névoa é a cor do horizonte. A névoa é o que separa céu de chão.
3. Linhas longas (fios, trilhos, raios) seguem a tangente da câmera, nunca ficam soltas.
4. A faixa central da tela, atrás da tira, fica mais escura e menos saturada; o contraste máximo é da tira.
5. A tira ou o cartão tem fundo opaco. Nunca coloque texto direto sobre a cena.
6. Meio-tom e contorno são do renderizador; os pontos de CSS de Wasteland são só para o fallback 2D, para não ter meio-tom duplo.

### Troca de 3D para 2D

A decisão é feita uma vez, no carregamento:

```js
const can3D = (() => { try { const c = document.createElement('canvas'); return !!(c.getContext('webgl2')); } catch { return false; } })();
const narrow = matchMedia('(max-width:700px)').matches;
const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
const mode = can3D && !narrow ? (reduce ? '3d-static' : '3d') : '2d';
document.documentElement.dataset.bg = mode;
```

`3d-static` renderiza a cena uma vez, na posição inicial, e para (correção testada na v7). No modo `2d`, no mobile, remova L2 e L5 e reduza o deslocamento para `10vh`, como em Wasteland.

## Componentes

Todos usam apenas os tokens da seção 3. Medidas e cortes vêm de Wasteland, exceto onde indicado.

| Componente | Regra |
| --- | --- |
| Logo e manchete | Barra `--strip` com `clip-path: polygon(0 5%,3% 0,100% 3%,98% 100%,2% 95%)`. Três primeiras palavras em stencil branco; o resto em letras recortadas (4 estilos ciclando, `--hot-fill` e branco). Versão visual `aria-hidden`, texto real em `.sr` |
| Tira da nota (lista) | Fundo `--strip`, corte irregular alternado por `nth-child`, rotação de ±0,6°. Ativa: faixa `inset 10px 0 0 var(--hot-on-dark)`, título em `--hot-on-dark`, selo com `▶` |
| Cartão em foco (Jardim) | Papel `#f0ece4`, quatro cantos cortados, sombra deslocada em `--hot-fill`, rotação de \~1,5°, numeral de contorno `02`. É a nota ativa quando há cena 3D; a tira vira a versão compacta da mesma nota na lista |
| Selo de estágio | Adesivo branco, `rotate(-2deg)`, sombra `2px 2px 0 var(--hot)`. Texto: glifo + nome (`○ semente`, `◐ broto`, `● árvore`). Ativo: fundo `--hot`, texto branco, prefixo `▶` |
| Comando | `$ jardim ler N` em JetBrains Mono 12px, `--strip-mute`. Presente em toda nota |
| Índice lateral | Caixa de papel, borda 3px `--ink`, sombra `5px 5px 0 var(--hot)`. No cartão do Jardim, os números 01 a 05 viram os botões do índice, com o ativo em `--hot` |
| Botões | Principal: fundo `--hot`, texto branco, borda 3px `--ink`, sombra `4px 4px 0 var(--ink)`, Big Shoulders 20px. Altura mínima 44px. Foco: `outline:3px solid currentColor; outline-offset:3px` |
| Controles de cena | Três botões no topo: `som`, `qualidade: auto`, `pontilhado: on`, mais `movimento: off`. Contorno 2px `--ink`, ativo em `--hot` |
| Rodapé | Barra `--strip`, `border-top:6px solid var(--hot-fill)`, teclas `j k Enter Espaço` em `<kbd>`, aviso "sem rastreadores · não pisca". Créditos de modelos aqui |

### Regra de coerência

O cartão do Jardim e a tira de Wasteland são dois estados da mesma nota. Mesma ordem de informação em ambos: selo de estágio, título, resumo, comando, tag. A tira mostra título, selo e comando; o cartão mostra tudo.

No tema Asfalto, as tiras ganham `filter: drop-shadow(5px 5px 0 var(--hot-fill))` no wrapper (não no elemento com `clip-path`, que cortaria a sombra) e contorno interno `inset 0 0 0 2px #4a4452`.

## Movimento, desempenho e acessibilidade

**Movimento:** vale a regra mais rígida dos dois sistemas. Só o scroll move a cena (câmera, montagem e desmontagem dos objetos). Nada pisca nem repete em loop por padrão. Tréns, tráfego e retalhos animados ficam parados e só se mexem com o controle `movimento: on`, que persiste só como preferência do visitante.

| Situação | Comportamento |
| --- | --- |
| `prefers-reduced-motion: reduce` | Modo `3d-static` (cena renderizada uma vez) ou `2d` sem parallax; sem transições |
| Sem WebGL2 | Modo `2d` com camadas SVG de Wasteland |
| Largura até 700px | Modo `2d`, sem L2 e L5, deslocamento `10vh` |
| Frame lento | Resolução adaptativa: escalas 1, .8, .65, .5; janela de 45 frames; desce acima de 27 ms, sobe abaixo de 17,5 ms; trava de 6 s; aquecimento de 90 frames |
| Aba escondida | Para o loop de render |

**Desempenho:** DPR máximo 1,5, antialias desligado, geometria mesclada, modelos assados sem textura, cache das leituras de layout (685 para 0 no Jardim v4), debounce de resize de 140 ms. No 2D, anime só `transform`.

**Acessibilidade:**

- Toda camada de fundo, 2D ou 3D, é `aria-hidden="true"` e `pointer-events:none`.
- Estágio da nota: glifo + texto, nunca só cor. Nota ativa tem `▶` além da cor.
- Texto sempre sobre superfície opaca (tira ou cartão), com os contrastes da seção 3.
- Teclado: `j`/`k` navegam, `Enter` ou `Espaço` abrem, foco visível de 3px.
- Conteúdo completo disponível sem JavaScript e sem WebGL.

Limite honesto: o FPS do 3D não foi medido em GPU real; os testes rodaram em renderização por software (cerca de 7 fps), só para conferir layout e erros. Os valores de qualidade adaptativa vêm do Jardim v7 e precisam ser validados em celular.

## Receita de implementação

Construa nesta ordem; cada passo funciona sozinho antes do próximo.

1. **Tokens e tipografia** (seções 3 e 4). Nenhuma cor solta depois disso.
2. **Conteúdo e componentes em HTML puro**: manchete, tiras, selos, comando, índice, rodapé. A página já precisa ser legível e navegável por teclado.
3. **Fundo 2D** com as camadas L0 a L6 e o parallax CSS de Wasteland (`animation-timeline: scroll()` com fallback em JS). Este é o modo `2d` final.
4. **Seletor de modo** (`can3D`, `narrow`, `reduce`) gravando `data-bg` no `<html>`.
5. **Cena 3D** apenas se `data-bg` for `3d` ou `3d-static`: importmap `three@0.160.0`, domínio de céu, névoa, chão, fileiras, trilha de câmera, `setViewOffset`. Esconda as camadas 2D com `[data-bg^="3d"] .layer{display:none}`.
6. **Pós-processamento**: meio-tom, contorno por luminância e passe final (fantasma de velocidade, grão, vinheta à esquerda).
7. **Modelos assados** em geometria sem textura, embutidos em base64, com créditos no rodapé.
8. **Montagem por scroll** (`uExp`, `ee`) e qualidade adaptativa.
9. **Revisão** com o checklist e o teste do olho semicerrado.

A receita detalhada do 3D, com fórmulas e código, está no documento "Design system: cenário 3D de colagem urbana" (Jardim v7). A mescla não repete esse código.

## Checklist de entrega

- [ ] Só tokens no CSS dos componentes; tema e acento trocam sem editar componentes.
- [ ] Texto pequeno de acento usa `--hot` ou `--hot-on-dark`; `#e11b22` só em formas.
- [ ] Estágio da nota em glifo + texto; nota ativa com marca além da cor.
- [ ] Manchete e logo recortados com `aria-hidden` e texto real em `.sr`.
- [ ] Modo 3D, 3D estático e 2D testados (forçando `data-bg`).
- [ ] Sem WebGL a página mostra o fundo 2D, sem erro no console.
- [ ] Teste do olho semicerrado: a tira ou o cartão continua sendo a primeira coisa vista.
- [ ] Ponto de fuga e horizonte visíveis; linhas longas seguem a tangente.
- [ ] Movimento só por scroll; `movimento: on` desligado por padrão.
- [ ] FPS e qualidade adaptativa medidos em celular real.
- [ ] Foco visível e `j`, `k`, `Enter`, `Espaço` funcionando.
- [ ] Testado em 360px e 1000px.
- [ ] Fontes com fallback; legibilidade se o Google Fonts falhar.
- [ ] Créditos de modelos 3D e de ícones (Game Icons, se usado) no rodapé.
- [ ] Nenhum ativo, logo, personagem ou fonte original de jogo.
- [ ] Nenhuma frase afirma como fato o que o Wasteland marca como incerto (fonte do logo, arte do encarte).

## Fontes, créditos e uso no Codex

**Origem desta mescla:**

- Jardim v7 e o documento "Design system: cenário 3D de colagem urbana" (esta conversa): cena 3D, tokens vermelhos, teste do olho semicerrado, desempenho.
- WASTELAND\_DESIGN.md (anexado): tokens claro e dark, tiras, letras recortadas, camadas 2D, contrastes do rosa. As fontes e os valores de cor desse arquivo são aproximações declaradas por ele mesmo; as fontes do logo original não foram confirmadas.
- As fontes externas do documento do Jardim (NN/g, Adobe, CUNY, W3C WCAG 2.3.3, Codrops, Maxime Heckel, entre outras) continuam valendo para a parte 3D e de hierarquia.

**Créditos de modelos:** torre de rádio, Poly by Google (CC BY 3.0); skate, cg\_world; caminhão e moto, Kenney (MIT).

**Uso no Codex:** o pacote de skills enviado antes ganhou uma skill nova, `collage-wasteland-merge`, que aponta para este sistema. Instale em `.agents/skills/` no projeto (caminho vindo de guias de terceiros; confirme na sua versão do Codex) e cite `$collage-wasteland-merge` no prompt.

Esta marca e esta estética são inspiradas em jogos de terceiros. Use em projeto pessoal; não reproduza logos, personagens nem imagens de nenhum deles.
