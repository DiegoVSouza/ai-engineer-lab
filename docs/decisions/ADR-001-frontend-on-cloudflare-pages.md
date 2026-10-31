# ADR-001 — React fronts on Cloudflare Pages, APIs on Fly, one design system package

Status: accepted by the owner on 2026-10-31 (direction); execution of any deploy still needs explicit go (lab rule 9).
Supersedes: decision 4 ("Same-origin API") in `docs/harness/adaptation-discovery.md`.

## Context

- P06 (console) is a React front served by nginx on Fly (`supportops-lab-web`), which proxies `/api/` to P05 so P05 needs no CORS.
- P07 (portfolio) is a static React site, not deployed.
- `DESIGN_SYSTEM_COLAGEM_URBANA_NOITE.md` is the lab's design system. Today P06 and P07 each carry their own copy of the tokens and hand-made CSS, and neither implements the system's components (cut card with hard shadow, status seal with glyph, plate with cut-out letters, band, footer, toggles, toast, modal, wake/loading states).
- Fly machines autostop. A cold P05 takes about 16 s and Keycloak about 22 s to answer (`docs/harness/lab-stack/fly-deployment.md`).

## Decision

1. **Fronts are static and live on Cloudflare Pages.** Fly runs only APIs, workers and data. The browser calls Fly directly.
2. **One design-system package, `p08` (`colagem-ui`).** React components and a single `tokens.css` implementing the design system. P06 and P07 consume a pinned, checksummed tarball, never a sibling source tree (same pattern as the P00 wheel). Tokens are the only place a color exists.
3. **Adoption level per product** (design system section 3): P06 level 0 (core, a work console), P07 level 1 (2D layers, portfolio). Level 2 (Three.js) is a later phase for P07 and falls back to level 1.
4. **Cross-origin API.** P05 gains an allowlist-based CORS setting (no wildcard; bearer tokens, so no credentials). The Keycloak client accepts more than one origin. A front reads its API and IdP URLs from a build-time `config.json`, not from nginx.
5. **Wake-aware UX.** Because Fly may be asleep, every front shows a "waking the service" state with elapsed time and a retry, using the design system's loading rule (text or bar, no endless spinner).
6. **Retire `supportops-lab-web` on Fly** after the Pages deployment passes its public e2e. Local Compose keeps the nginx image so the full stack still runs offline.
7. **No deploy, login or token creation without an explicit go from the owner** for each of Fly and Cloudflare.

## Consequences

- P05 changes (CORS) belong to P05's own SDD phase and repository, additive, contract unchanged.
- `ops/stack/idp_clients.py` and `ops/fly/stack-apps.ps1` change in the lab root.
- CSP moves from nginx to Pages `_headers`; `connect-src` and `frame-src` must name the Fly API and IdP origins exactly.
- Pages deployments are immutable, so rollback is promoting a previous deployment `[VERIFICAR in Cloudflare docs before the first deploy]`.
- Cloudflare Pages pricing and limits `[VERIFICAR]` before relying on them; no cost figure is stated until checked.
- A third product (p08) is added. It is a library: no deploy, only a tarball.
- Risk: `--red` text contrast. The package forbids `--red` for small text (design system 4.2) and a test measures the token pairs against the system's table.
