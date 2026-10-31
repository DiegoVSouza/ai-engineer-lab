---
name: collage-wasteland-merge
description: Build or restyle a page using the merged Jardim-3D x Wasteland design system (two themes, accent tokens, 3D scene with 2D parallax fallback, ransom headline, TUI strips). Use when asked for the merged/mixed Jardim + Wasteland style or when both a 3D city background and light/dark skate-zine UI are wanted.
---
# Jardim 3D x Wasteland (merged)

One system: two themes (`asphalt` dark, `photocopy` light) and a accent tokens. Read `references/WASTELAND_DESIGN.md` for component details; the 3D scene follows `$ui-scene-composition` and `$threejs-ui-background`.

## Decisions (do not revisit without asking)
- Palette is Wasteland's in every theme: paper #f5f4f0, ink #111, hot pink, neon green only in splashes (never text). The 3D scene is re-tinted pink (fog #2a0a1c), no red.
- Accent tokens: `--hot-fill` #e6008a (shapes, headline, 3D), `--hot` #d6007d (small text on paper, button fill with white text), `--hot-on-dark` #ff2fa3 (text on black strips). #e6008a fails as small text (4.03:1 on paper, white on it 4.44:1): large text or decoration only.
- Themes: `photocopy` (default, light) and `asphalt` (dark, paper #221e26, strip #060507); use asphalt when the 3D night scene is on.
- Background is one 7-level stack (paper, sky/ghost text, light/halftone, city, midground, ground, splashes). WebGL2 and width > 700px and no reduced-motion → 3D; reduced-motion → 3D rendered once; else 2D SVG layers with CSS parallax. Set `data-bg` on `<html>`.
- Motion: scroll-driven only. No loops by default; trains/traffic move only with an explicit "movimento: on" control.
- Content sits on opaque surfaces: black strip (lists) or paper card (active note over 3D). Same info order in both: stage badge, title, summary, command, tag.
- Ransom letters only in logo/headline, with `aria-hidden` visual + `.sr` real text.
- Always TUI base: stage glyph + text, `$ jardim ler N`, side index, key footer (j/k/Enter/Space).
- Fonts: Big Shoulders Stencil Display, Londrina Solid, Courier Prime, JetBrains Mono, with fallbacks.
- Never use ATLUS/Persona or Tony Hawk/Neversoft/Activision assets, logos, characters or fonts.

## Build order
tokens+type → plain HTML components → 2D layers → mode switch → 3D scene → postprocessing → baked models → scroll assemble + adaptive quality → checklist (squint test, 360px/1000px, keyboard, forced `data-bg` modes, real-device FPS).
