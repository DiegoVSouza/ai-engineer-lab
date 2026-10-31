# Specification — frontend platform (lab phase)

Goal: P06 and P07 are React fronts built on one implementation of `DESIGN_SYSTEM_COLAGEM_URBANA_NOITE.md`, deployed to Cloudflare Pages, calling Fly APIs. See ADR-001.

## Requirements

| ID | Rule | Owner |
| --- | --- | --- |
| DS-001 | Every color, font, shadow, cut and spacing comes from `colagem-ui/tokens.css`. A test fails on a hex value in a consumer's CSS or TSX. | p08, checked in p06 and p07 |
| DS-002 | Token pairs meet the contrast table in design system 4.4. A test computes WCAG ratios from the token values and fails below 4.5:1 for small text pairs, or when `--red` or `--dred` is used for small text. | p08 |
| DS-003 | Status is glyph plus word, never color alone (`○ ◐ ●` seal, `▶` active). | p08 |
| DS-004 | `prefers-reduced-motion` stops every ambient animation; events are finite; only `transform` and `opacity` animate (documented `wig` exception). Tested. | p08 |
| DS-005 | Content works without JavaScript beyond the app shell, without WebGL and without external fonts (self-hosted Fontsource). | p06, p07 |
| DS-006 | Squint test: a Playwright screenshot with `blur(10px)` is saved as evidence for the home and one detail screen of each front. Judged by the owner; recorded as `review_mode=human_pending` until then. | p06, p07 |
| FE-001 | Static build only; runtime values come from `config.json` generated at build (no secrets). | p06, p07 |
| FE-002 | P06 calls P05 and Keycloak cross-origin with a `connect-src` that names exactly those origins. | p06 |
| FE-003 | Cold Fly services show the wake state with elapsed seconds and a retry; no endless spinner. | p06, p07 if it calls an API |
| API-002 | P05 answers CORS preflight only for origins in `CORS_ALLOWED_ORIGINS`; unknown origin gets no `Access-Control-Allow-Origin`; no `*`. | P05 |
| SEC-002 | Keycloak client `supportops-web` lists the Pages origin and the local origin, nothing else. | lab root |
| OPS-001 | Public e2e (Playwright + axe) passes against the Pages URLs before `supportops-lab-web` is retired. | p06, lab root |
| OPS-002 | Rollback plan for Pages and the previous Fly web image is written before cutover. | lab root |
| PERF-001 | Initial JS ≤ 100 KB gzip for p07 (level 1) and ≤ 120 KB for p06 (OIDC). | p06, p07 |

## Adoption

| Product | Level | Theme / preset | Vocabulary (design system section 2) |
| --- | --- | --- | --- |
| P06 console | 0 | breu / vermelho | Item = ticket or approval; Seal = ticket and approval state; Command = `$ ticket open 12` |
| P07 portfolio | 1 | breu / vermelho | Item = project; Seal = verified / claimed / partial / open; ghost number = P00..P06; Command = `$ project open 05` |

## Out of scope

Three.js scene (own later phase), sound, a kit `web-saas` profile, custom domains, analytics, changes to P05 business rules.
