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
