# Plan — frontend platform

Order matters: each phase has its own repository and SDD folder; the lab root only holds this overview and the ops changes.

| Phase | Where | Content | Needs go from owner |
| --- | --- | --- | --- |
| F0 | lab root | ADR-001, this SPEC/PLAN/VERIFY | no |
| F1 | `projects/p08` (new, `colagem-ui`) | Tokens, fonts, level 0 components, level 1 layers, contrast and axe tests, squint screenshot, tarball with SHA-256 | no |
| F2 | `projects/p07` | Replace local CSS with `colagem-ui`, level 1 (2D layers, `data-bg` selector), cut cards, seals with glyph, plate, band, footer; Pages config (`_headers`, `_redirects`) | no |
| F3 | `projects/p06` | Same migration at level 0, `apiBase` and IdP from `config.json`, wake state, cross-origin client, Pages config | no |
| F4 | `projects/p05` + lab `ops/stack/idp_clients.py` | `CORS_ALLOWED_ORIGINS` (default empty), preflight tests; Keycloak client with several origins | no, but P05 version bump and Fly redeploy do |
| F5 | lab root | Rollback plan, Pages projects, `wrangler pages deploy`, `fly deploy` of P05 with CORS, public e2e, retire `supportops-lab-web` | **yes, per command group** |
| F6 | `projects/p07` | Level 2 Three.js scene with level 1 fallback | later |

Dependencies: F1 → F2, F3. F4 → F5. F2, F3, F4 → F5.

allowed_write_paths per phase: F1 `projects/p08/**`; F2 `projects/p07/**`; F3 `projects/p06/**`; F4 `projects/p05/**`, `ops/stack/idp_clients.py` and its test; F5 `ops/**`, `fly/**`, `docs/harness/lab-stack/**`.

forbidden_changes: `harness-kit/`, importing a sibling source tree, a hex color outside tokens, `*` in CORS, secrets or API tokens in Git, deploy or login without go, weakening a test.

Stop conditions: three failed attempts on one failure; any step that would publish, log in, spend or restart a Fly machine.

Packaging: p08 builds `colagem-ui-<version>.tgz` with `npm pack`; consumers install `file:vendor/colagem-ui-<version>.tgz` and record version, SHA-256 and source commit in `docs/harness/sources.lock.json`.
