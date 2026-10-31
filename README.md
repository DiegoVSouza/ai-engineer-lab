# AI Engineer Lab

This repository is a factory for independent AI portfolio projects. The reusable implementation lives in [`harness-kit/`](harness-kit/); each generated directory under `projects/` owns its own Builder, Product, and Shared layers.

## Create a project

```powershell
python scripts/harness/new-project.py ticket-triage --type agent-app
```

Supported profiles are `agent-app`, `mcp-server`, `rag-pipeline`, `workflow-automation`, `eval-infra`, `agent-saas`, and `internal-agent`. The command creates `projects/ticket-triage`, copies the selected profile into `harness.yaml`, resolves the required modules, and records the kit version in `.harness/`.

Then complete `docs/harness/decisions.md` and create the first `SPEC.md`, `PLAN.md`, and `VERIFY.md` before writing product code.

## Design

`harness-kit-v2.1.md` is the design reference. The lab adapts it as follows:

- `harness-kit/` is the Kit layer and is changed only through a dedicated, verified phase.
- `projects/<name>/` is one independent repository-shaped product; it does not import another portfolio project.
- `harness.yaml` selects modules and is the product's harness source of truth.
- The SDD process, evidence requirement, fake/replay/live modes, and external-effect authorization remain mandatory for every project.

The older `specs/P00–P05` collection is retained as a SupportOps curriculum archive. It is no longer the required build order.

## Useful commands

```powershell
python scripts/harness/check.py --root .
python scripts/harness/new-project.py --help
python harness-kit/bootstrap/harness_init.py --help
```

## Run the SupportOps projects together

With the seven project repositories checked out under `projects/` and Docker Compose installed, run from this directory:

```powershell
python scripts/stack.py checkout
python scripts/stack.py up
python scripts/stack.py credentials
python scripts/stack.py check
```

### One command up, one command down

| | Local (Docker Compose) | Fly.io |
| --- | --- | --- |
| Up | `python scripts/stack.py up` | `python scripts/stack.py fly-up` |
| Down, data kept | `python scripts/stack.py down` | `python scripts/stack.py fly-down` |
| State | `python scripts/stack.py status` | `python scripts/stack.py fly-status` |
| Down, data destroyed | `python scripts/stack.py down --volumes` | `python scripts/stack.py fly-down -DestroyData -ConfirmDestroy supportops-lab` |
| Preview | not needed, nothing leaves the machine | append `-DryRun` |

Both sides make the same promises. Each touches only its own application: Compose scopes to the project, and Fly commands refuse any app outside `ops/fly/stack-apps.ps1`. Plain `down` keeps data: named volumes locally, Fly volumes on Fly, where each surviving volume is listed on exit. Data is destroyed only by the explicit flag. A failed step returns a non-zero exit code.

`down` removes this Compose application's containers and networks, so `down` followed by `up` is a non-destructive restart. Fly `down` stops every machine and disables public autostart, so requests cannot wake the stack; `up` is safe to repeat, creating anything missing, redeploying, starting in dependency order and waiting for health. The `fly-*` commands wrap `pwsh -File ops/fly/deploy.ps1 -Action Up|Down|Status`, and `-Action Reconcile` finishes a partial `Up` without rebuilding; `ops/fly/power.ps1 -Action Start|Stop|Status` resumes or suspends machines without a deploy. Fly commands need `flyctl` and PowerShell 7, spend real money, and change a public deployment.

`checkout` clones missing product repositories at the commits in `ops/stack/projects.lock.json` and verifies existing checkouts without changing them. Access to those Git repositories is required. The pinned commits exist locally and have not been pushed, and P06 has no remote yet, so a fresh machine cannot clone them until they are published.

The root Compose application runs the P06 console, P04 and P05 APIs/workers, P03 observability, and a persistent HTTPS Keycloak server. The package gate executes the installed P00 foundation, P01 orchestrator, and P02 toolkit before P05 starts. Each product keeps its own repository; the integration uses pinned wheels and existing Dockerfiles.

| Service | Local URL |
| --- | --- |
| Console | http://localhost:48080 |
| P05 API / Swagger | http://localhost:48000/docs |
| P04 async API / Swagger | http://localhost:48004/docs |
| Keycloak admin | https://localhost:38443/admin/ |
| Grafana | http://localhost:43000 |
| Prometheus | http://localhost:49090 |
| Jaeger | http://localhost:46686 |

Credentials and TLS keys are generated once in Docker volumes. `credentials` shows the local account passwords only when requested. P05 validates Keycloak tokens over verified internal HTTPS; its worker delegates to MCP with short-lived internal tokens. All published ports bind to loopback. P04's independent demo API has no identity layer and stays local.

This stack uses `LLM_MODE=fake` and local SQS/SNS emulation. PostgreSQL, Keycloak identity, Redis, Grafana, and Prometheus data persist in named volumes. LocalStack broker messages and Jaeger traces are ephemeral; drain jobs before stopping the broker. Completed tasks remain in PostgreSQL. Model quality is PENDING.

The initial Keycloak certificate uses a generated local CA. Export the public CA with `python scripts/stack.py ca` and trust it in your browser if needed. See the [Portuguese operator guide](docs/knowledge/self-hosted-stack.md) for login, tokens, port changes, persistence, and backup boundaries.
