# ADR-002 — The portfolio is a product, and every claim is verifiable

Status: direction from the owner on 2026-10-31; items marked **owner** are open. Research: `docs/knowledge/portfolios-de-ai.md`. Spec: `projects/p07/.planning/phases/003-real-portfolio/SPEC.md`.

## Decisions made by the owner

1. **Pages project name: `diego-portifolio-ai`.** The `*.pages.dev` name cannot be renamed without deleting the project, and the spelling differs from the English and Portuguese words (see open item 1).
2. **No Go.** The backend stays in Python (P04, P05). `stack-go` and the Go phases of `plano-harness-saas-react-go.md` do not apply. That file is kept as history.
3. **Fly for APIs, Cloudflare Pages for fronts** (ADR-001 stands).
4. **Lab projects are the portfolio's projects.** A recruiter must be able to see each one, use a demo, validate the code and read the documentation.
5. **`colagem-ui` and the Colagem Urbana Noite design system are the only visual language.**

## Decisions derived from the research

6. **Positioning: evidence you can check.** Not "I build agents". The site's promise is that a stranger can verify each claim, and that failures stay visible. P00's 27/36 and its `FAIL_PROVISIONAL` verdict are shown, not hidden.
7. **One story, not nine cards.** The projects are presented as one system, SupportOps, with P05 + P06 as the flagship. Depth over count: one flagship, then full cases, then standard cases, all on one template.
8. **Case template taken from the best page read.** TL;DR, try it, how it works, decisions ending in "Rejected:", results split into Measured and Not measured, failure gallery, validate it yourself, what I would do differently.
9. **Every number is an evidence record** with mode (`fake`, `replay`, `live`), command, exit code, commit and a permalink. A number without one fails the build. A `fake` result is never shown as model quality.
10. **Three demo tiers.** Tier 0 recorded replay inside the site, always available. Tier 1 the real stack on Fly with `LLM_MODE=fake`. Tier 2 a real model, only after a spend decision. Each demo says which tier it is.
11. **Prerendered real routes instead of hash routes,** so pages are indexable, shareable with a preview, and readable without JavaScript, as the design system requires.
12. **Level 1 stays.** Level 2 (Three.js) is a later phase, after the content is verified.
13. **AI assistance is disclosed.** The projects were built with coding agents under the lab's harness. Hiding that would be false, and directing agents under gates is itself the skill on show.
14. **Stay on Pages.** Cloudflare recommends Workers for new projects, but the owner chose Pages, it still works, `_headers` carries over, and moving a static site later is cheap. Revisit if a Workers-only feature becomes necessary.

## Consequences

- A public-readiness gate comes first: secrets over full Git history, license, private evidence, clean-clone run, hosted CI.
- Making repositories public and pushing are irreversible in practice: a secret that was ever public must be treated as leaked. Each needs an explicit go.
- A public demo means public abuse: Keycloak admin path, demo credentials, data reset and rate limits must be handled first.
- `colagem-ui` grows by a minor version for the new generic components.

## Open items, owner

1. **Spelling.** `diego-portifolio-ai` is what the owner chose. `diego-portfolio-ai` is the English spelling and it would appear in every link sent to a recruiter. Decide before the first deploy; afterwards a rename means delete and recreate. A custom domain removes the question.
2. **Repository visibility**, per repository, after the audit.
3. **License** for public code.
4. **Demo budget ceiling** for Fly, and whether Tier 2 exists at all.
5. **Personal content:** name as shown, bio, CV, contact, target role, and the wording of the AI-assistance statement.
6. **Custom domain.**
