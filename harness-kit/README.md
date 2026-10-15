# Harness Kit

This directory is the reusable source for independent AI portfolio projects. It implements the Kit layer from `../harness-kit-v2.1.md`; each generated project owns its Builder, Product, and Shared layers.

Create a project from the lab root:

```powershell
python scripts/harness/new-project.py ticket-triage --type agent-app
```

The command creates `projects/ticket-triage`, writes its profile, and initializes only the modules selected by that profile. Re-run it only after making an intentional kit upgrade; initialization never overwrites an existing generated file.

The canonical project configuration is `harness.yaml`. The generated project's `AGENTS.md`, `docs/harness/`, and `.harness/modules.lock` are derived artifacts and should be reviewed with the profile.
