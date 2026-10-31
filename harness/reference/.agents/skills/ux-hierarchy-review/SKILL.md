---
name: ux-hierarchy-review
description: Review a UI for visual hierarchy, usability and accessibility, with concrete fixes. Use when asked to audit, critique or polish a page, especially expressive designs with heavy backgrounds or motion.
---
# UX hierarchy review

Check in order, report findings as file:line + fix:
- Squint test: is the primary content first? Count competing high-contrast elements (max 1–2).
- Nielsen heuristics: visible status, consistency, error prevention, recognition over recall.
- Contrast ≥ 4.5:1 for text over busy backgrounds (use solid panels, not transparency).
- Motion: honor `prefers-reduced-motion` (WCAG 2.3.3); no flashing; provide quality/pause control.
- Keyboard: visible focus, logical order, nav reachable.
- Performance: measure on a real device; adaptive resolution; no layout reads per frame.
- Fallbacks: no-WebGL/offline still shows content; credits for third-party assets.
