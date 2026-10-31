# ADR-002 — The portfolio is a product, and every claim is verifiable

Status: direction from the owner on 2026-10-31; items marked **owner** are open. Research: `docs/knowledge/portfolios-de-ai.md`. Spec: `projects/p07/.planning/phases/003-real-portfolio/SPEC.md`.

## Decisions made by the owner

1. **Pages project name: `diego-portfolio-ai`.** The `*.pages.dev` name cannot be renamed without deleting the project.
2. **No Go.** The backend stays in Python (P04, P05). `stack-go` and the Go phases of `plano-harness-saas-react-go.md` do not apply. That file is kept as history.
3. **Fly for APIs, Cloudflare Pages for fronts** (ADR-001 stands).
4. **Lab projects are the portfolio's projects.** A recruiter must be able to see each one, use a demo, validate the code and read the documentation.
5. **`colagem-ui` and the Colagem Urbana Noite design system are the only visual language.**

## Decisions derived from the research

6. **Positioning: evidence you can check.** Not "I build agents". The site's promise is that a stranger can verify each claim, and that failures stay visible. P00's 27/36 and its `FAIL_PROVISIONAL` verdict are shown, not hidden.
7. **One story, not nine cards.** The projects are presented as one system, SupportOps, with P05 + P06 as the flagship. Depth over count: one flagship, then full cases, then standard cases, all on one template.
8. **Case template taken from the best page read.** TL;DR, try it, how it works, decisions ending in "Rejected:", results split into Measured and Not measured, failure gallery, validate it yourself, what I would do differently.
9. **Every number is an evidence record** with mode (`fake`, `replay`, `live`), command, exit code, commit and a permalink. A number without one fails the build. A `fake` result is never shown as model quality.
10. **The demo is always live** (revised, see below). Recorded live runs are the labelled fallback, never a silent substitute.
11. **Prerendered real routes instead of hash routes,** so pages are indexable, shareable with a preview, and readable without JavaScript, as the design system requires.
12. **Level 1 stays.** Level 2 (Three.js) is a later phase, after the content is verified.
13. **AI assistance is disclosed.** The projects were built with coding agents under the lab's harness. Hiding that would be false, and directing agents under gates is itself the skill on show.
14. **Stay on Pages, with Pages Functions for dynamic data.** Cloudflare's guidance and plugin recommend Workers + Static Assets for new sites. This is a deliberate deviation: the owner chose Pages, it gives the short `pages.dev` URL, Functions cover the need, and `_headers` carries over. Cron needs one small separate Worker.

## Consequences

- A public-readiness gate comes first: secrets over full Git history, license, private evidence, clean-clone run, hosted CI.
- Making repositories public and pushing are irreversible in practice: a secret that was ever public must be treated as leaked. Each needs an explicit go.
- A public demo means public abuse: Keycloak admin path, demo credentials, data reset and rate limits must be handled first.
- `colagem-ui` grows by a minor version for the new generic components.

## Revision, 2026-10-31, owner decisions

15. **Always live.** Visitors reach `LLM_MODE=live`. Machines keep autostop and stay ready to start live.
16. **Use the four Groq keys as far as the free organizations allow, with a USD 10 precaution ceiling** on models.
17. **USD 5 ceiling on Fly.** Fly has no hard cap, so this needs our own guard, plus prepaid credit if it behaves as documented.
18. **Dynamic React:** prerender, hydrate, and Pages Functions for runtime data.
19. **MIT** for all repositories.
20. **Identity:** Diego Vieira Gonçalves de Souza, AI Engineer, in English. CV facts come from the owner's CV, are labelled as career history, and the phone number is not published.
21. **Harness statement approved:** the projects were built under a harness that applies AI engineering best practices.
22. **Maximum selling within the evidence rule.** The site argues hard; numbers still need a source.

Consequences: live is a real P05 feature, not a flag, because the existing guards refuse unaccounted calls and the live refund workflow. Those guards stay until the accounted path replaces them. P00's protected budget is untouched. Public text reaches a real model, so the triage stays tool-free and refunds simulated.

23. **Own `FlowDiagram` on the site, Mermaid in READMEs.** ELK runs at build time and React draws the SVG. Measured: Mermaid and inline D2 break the strict CSP, and React Flow costs 60 KB for pan and zoom nobody needs. See `docs/knowledge/diagramas-no-portfolio.md`.

## Open items, owner

1. Review of the copy and the English CV.
2. Every stage is authorized for the executor, under the conditions in `docs/harness/portfolio/NEXT-EXECUTOR-PROMPT.pt-BR.md`.
3. Custom domain, later.

Closed on 2026-10-31: `newsAR` is not used and no other repository is featured. Groq accounts and key rotation confirmed fine by the owner.
