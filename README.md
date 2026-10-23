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

With the six project repositories checked out under `projects/` and Docker Compose installed, run from this directory:

```powershell
python scripts/stack.py checkout
docker compose up -d --build --wait --wait-timeout 300
python scripts/stack.py credentials
python scripts/stack.py check
```

`checkout` clones missing product repositories at the commits in `ops/stack/projects.lock.json` and verifies existing checkouts without changing them. Access to those Git repositories is required.

The root Compose application runs P04 and P05 APIs/workers, P03 observability, and a persistent HTTPS Keycloak server. The package gate executes the installed P00 foundation, P01 orchestrator, and P02 toolkit before P05 starts. Each product keeps its own repository; the integration uses pinned wheels and existing Dockerfiles.

| Service | Local URL |
| --- | --- |
| P05 API / Swagger | http://localhost:48000/docs |
| P04 async API / Swagger | http://localhost:48004/docs |
| Keycloak admin | https://localhost:38443/admin/ |
| Grafana | http://localhost:43000 |
| Prometheus | http://localhost:49090 |
| Jaeger | http://localhost:46686 |

Credentials and TLS keys are generated once in Docker volumes. `credentials` shows the local account passwords only when requested. P05 validates Keycloak tokens over verified internal HTTPS; its worker delegates to MCP with short-lived internal tokens. All published ports bind to loopback. P04's independent demo API has no identity layer and stays local.

This stack uses `LLM_MODE=fake` and local SQS/SNS emulation. PostgreSQL, Keycloak identity, Redis, Grafana, and Prometheus data persist in named volumes. LocalStack broker messages and Jaeger traces are ephemeral; drain jobs before stopping the broker. Completed tasks remain in PostgreSQL. Model quality is PENDING.

The initial Keycloak certificate uses a generated local CA. Export the public CA with `python scripts/stack.py ca` and trust it in your browser if needed. See the [Portuguese operator guide](docs/knowledge/self-hosted-stack.md) for login, tokens, port changes, persistence, and backup boundaries.
