# Specification

Give the Fly stack the same operator contract as `python scripts/stack.py up|down`: one command up, one command down.

- **Up:** `pwsh -File ops/fly/deploy.ps1 -Action Up` prepares secrets once, creates missing stack apps and volumes, wakes existing machines, deploys every app in dependency order, starts everything, and waits for health.
- **Down:** `pwsh -File ops/fly/deploy.ps1 -Action Down` stops every machine, disables public autostart, and states which volumes survive. `-DestroyData -ConfirmDestroy supportops-lab` is the only path that removes apps and volumes.
- **Status:** `-Action Status` reports machines and volumes per app without changing anything.
- `python scripts/stack.py fly-up|fly-down|fly-status` are thin wrappers so local and Fly share one entry point. `python scripts/stack.py down --volumes` must actually reach Compose (argparse currently rejects it).

Guarantees: a single allowlisted inventory, and every Fly call that names an app is rejected if the app is outside it; volumes are reported explicitly; failures exit non-zero; `-DryRun` prints the plan and mutates nothing.

Out of scope: a real deploy. No Fly mutating command runs in this phase.
