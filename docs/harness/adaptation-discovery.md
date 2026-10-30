# Adaptation discovery (phase B-1)

Answers to section 1 of `plano-adaptacao-react-go-no-harness-kit.md`, taken from the repository on 2026-10-30. Where the plan assumed something the repository contradicts, the repository wins.

| Question | Finding | Evidence | Effect |
| --- | --- | --- | --- |
| Does the SaaS embed an AI agent? | Yes, in P05 (`has_agent: true`, profile `agent-saas`, RAG, MCP). The console itself has no agent and calls P05 over HTTP. | `projects/p05/harness.yaml` | New project uses a `has_agent: false` profile. Agent trifecta stays owned by P05. |
| Monorepo or separate repositories? | Separate. Each `projects/<pid>` has its own Git; the lab Git ignores `projects/`. | `.gitignore`, `AGENTS.md` | Frontend is new independent project `projects/p06`, not a `frontend/` directory in the lab. |
| Real versions of Go, Node, package manager, Codex | Go 1.26.1 is installed but no `go.mod` exists anywhere. Node 24.12.0, npm 11.6.2, pnpm installed, no `package.json` anywhere. Codex CLI 0.166.0. | Shell, `git ls-files`, `find projects` | **No Go backend.** The backend is P05 (Python/FastAPI). The `stack-go` module and the plan's Go phases do not apply. npm is used because it ships with Node. |
| Existing API contract or codegen? | `projects/p05/openapi.yaml`, OpenAPI 3.1 exported from FastAPI and checked by `scripts/export_openapi.py --check`. No client codegen. Five responses are untyped `dict`. | P05 sources | Adopt it, do not create `docs/contracts/`. Type the loose responses in P05, then generate the client. |
| Migrations and tool? | Plain SQL `projects/p05/migrations/00{2,3,4}_*.sql` applied by `PostgresStore.migrate()`, idempotent, forward-only, no down files. | P05 sources | Reversibility is an open gap for phase item 4. |
| State of `feature_list.json` and `progress.md` | Present per project. Schemas are not the plan's P00–P15 model; P05 uses `{"features": [...]}` with status strings. | `projects/*/docs/harness/` | Keep each project's existing shape. P06 uses the same `{"features": [...]}` shape, no second progress source. |
| Kit version inconsistency (v2.1 document vs `kit_version: 2.0.0`) | Does not exist. `harness-kit/VERSION` is 2.1.0 and all six projects record 2.1.0. | `harness-kit/VERSION`, `harness.yaml` | Nothing to align. |
| Existing `.claude/agents/*.md` | None. `.claude/` holds only local settings. | `.claude/` | No adapters to reuse. Execution stays sequential. |

## Gaps the plan did not foresee

- The API has no way to list pending approvals, and the worker does not update `Ticket.status`. An approver would have to decide a refund without seeing the amount. P05 needs additive `GET /v1/approvals`.
- The browser needs a public PKCE client. `--import-realm` skips an existing realm, so changing the realm file would not reach the running local volume or the deployed Fly realm; the client must be applied idempotently through the admin API.
- `python scripts/stack.py checkout` fails on the current tree because `ops/stack/projects.lock.json` pins old commits. Tracked for production readiness.

## Decisions

1. **Profile:** `workflow-automation` is the closest kit profile with `has_agent: false`. A `web-saas` profile is not added: `AGENTS.md` rule 3 requires a dedicated kit phase validated in two real projects, and only one frontend exists. `harness.yaml` of P06 carries the plan's `saas:` block locally. A kit proposal is left for when a second web project exists.
2. **Stack:** React 19, TypeScript, Vite, `openapi-typescript` + `openapi-fetch`, `oidc-client-ts`, Vitest, Playwright with axe. No router or state library, to stay inside the bundle budget.
3. **Design system adoption:** Level 0 (core) of `DESIGN_SYSTEM_COLAGEM_URBANA_NOITE.md`, tema Breu, red preset. A work console gets no 3D scene.
4. **Same-origin API:** nginx serves the console and proxies `/api/` to P05, so P05 gains no CORS surface.
5. **Not adopted from the plan:** GSD Core, `stack-go`, `.planning/STATE.md` duplicates, the Go+React rehearsal (B4). The plan's B4 tests a Go harness that does not exist here. Contract drift, scope and a11y are enforced by P06's own gates instead.
