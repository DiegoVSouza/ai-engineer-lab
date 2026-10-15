# Verification — Phase 001

## What must be true

1. A profile resolves the required module set and records it — check with a temporary valid project and inspect `.harness/modules.lock`.
2. A complete lethal trifecta is rejected without a security plan — check process exit code and absence of generated metadata.
3. Existing generated files are never overwritten — check process exit code and retained sentinel content.
4. The lab documents independent project intake and per-project SDD evidence — inspect `AGENTS.md`, `README.md`, and `harness/GSD-LITE-PLUS.md`.

## Result

- [x] 1: PASS — `new-project.py` exited 0 and generated the agent runtime, evals, and module lock. Evidence: `artifacts/evidence/harness-kit/positive-bootstrap.log`, `acceptance-assertions.json`.
- [x] 2: PASS — a complete trifecta without `security.md` exited 1 and created no `.harness` metadata. Evidence: `artifacts/evidence/harness-kit/trifecta-rejection.log`, `acceptance-exit-codes.json`.
- [x] 3: PASS — a second initializer run exited 1 and left the generated `AGENTS.md` intact. Evidence: `artifacts/evidence/harness-kit/overwrite-rejection.log`, `acceptance-assertions.json`.
- [x] 4: PASS — source compiled and the root structural gate passed. Evidence: `artifacts/evidence/harness-kit/py-compile.log`, `structural-check.log`, `validation-exit-codes.json`.
