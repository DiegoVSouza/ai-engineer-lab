# Recipes (from Jardim v7)

## Camera
- Track: CatmullRomCurve3 with straight extensions at the ends; `laneCurve(lat,h)` offsets along the normal.
- Vanishing point on the card: `camera.setViewOffset(w,h, narrow?0:Math.round(w*.17),0,w,h)`.
- Roll 0.14 rad: `camera.up.set(-Math.sin(.14),Math.cos(.14),0)`; look slightly down: `lookAt(pos+T*30, pos.y-4.2, …)`.

## Scene order
Sky dome (vertex-color gradient + slit sun) → `Fog(0x2b060b,10,64)` matching the horizon → ground ribbons (road, sidewalks, red edges, dashes) → building rows (lat 10.5/19, spacing 6.4/7.4, heights 5–15/12–32, merged, emissive window texture) → poles/wires left, viaduct/trains right → traffic → radial streaks along the tangent → paper scraps.
Clamp curve params: `u=Math.min(1,u)` before `getPointAt`.

## Scroll assemble/disassemble
`uExp=min(1.05,max(0,|i-Tcur|*1.2-.1))`; in shader `ee=clamp(uExp*(.75+.5*aRand)-.05,0,1); ee=ee*ee*1.4`. Toon 3-tone color by face normal; random tones only when exploded.

## Models
Strip GLB textures, merge, quantize to Int16, embed base64. Credit sources in the footer.

## Performance
Cache layout reads, DPR ≤1.5, antialias off, SCALES [1,.8,.65,.5], 45-frame window, >27 ms down, <17.5 ms up, 6 s lock, 90-frame warm-up, resize debounce 140 ms. Reduced motion: place once, stop animating.
