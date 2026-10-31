---
name: threejs-ui-background
description: Implement a Three.js scroll-driven city/scene background behind HTML UI (halftone post-processing, camera track, instanced buildings, baked models, adaptive performance). Use with ui-scene-composition when coding the scene.
---
# Three.js UI background

Read `references/recipes.md` for the recipes. Summary: importmap three@0.160, EffectComposer + halftone/outline/finish passes, CatmullRomCurve3 camera track with `frameAt(t)`, merged/instanced geometry, models baked to texture-free Int16 base64 (no GLTFLoader), scroll-driven assemble/disassemble, layout cache, DPR cap 1.5, adaptive resolution, reduced-motion = render once.
