---
name: ui-scene-composition
description: Compose a 3D or layered background scene for a UI so it guides the eye to the content (cards, titles). Use when building hero/landing backgrounds, parallax or scroll-driven scenes, or when a scene feels chaotic, flat or competes with the text.
---
# UI scene composition

Rule: organized chaos. Every background shape must point to the focal content.

1. Pick ONE focal point (card/title). Put the vanishing point on it (`camera.setViewOffset`).
2. Build layers back to front: sky (gradient + one light source) → horizon (fog color = horizon color) → ground with lane lines → rhythmic rows of mid-ground masses → foreground accents → UI.
3. Depth cues: size falloff, fog, overlap, converging lines, contrast falling with distance.
4. Align long shapes (streaks, wires, rails) to the camera tangent, never random.
5. Attention budget: only the focal content gets max contrast; background stays darker/less saturated near it.
6. Verify with the squint test (blur the screenshot: is the focal content still first?).
7. Respect `prefers-reduced-motion` and keep a performance budget.

Details and code: see `../threejs-ui-background/references/recipes.md`.
