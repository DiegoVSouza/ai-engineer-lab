# PLAN â€” Unified local stack

allowed_write_paths: `docker-compose.yml`; `ops/stack/**`; `scripts/stack.py`; `.env.example`; `.gitignore`; `README.md`; `docs/knowledge/self-hosted-stack.md`; `docs/harness/lab-stack/**`; `.planning/projects/lab-stack/**`; `.planning/decisions.md`; `artifacts/evidence/lab-stack/**`.

1. Add generated secrets/TLS and persistent PostgreSQL/Keycloak provisioning with stable loopback issuer and verified internal HTTPS.
2. Wire existing product Dockerfiles, installed package gates, isolated database users, local queue setup, and shared observability into one Compose application.
3. Add operator commands and a redacted acceptance script covering tenant identity, revocation, P04/P05 workers, persistence, and runtime health; run and save evidence.
4. Document startup, endpoints, credentials, backup/restore boundaries and limitations; review staged changes and create an atomic lab commit.

Forbidden: product source changes, sibling source imports, existing stack removal, destructive volume operations, external deployment, paid/provider calls or fabricated metrics.

llm_mode: fake.
Validation: Compose config/build/up --wait; package gate; `python scripts/stack.py check`; controlled container recreation and repeated data/identity checks; root harness checker and staged diff review.
Stop condition: if an occupied port or unsupported runtime blocks startup, preserve unrelated stacks, correct the local configuration, and retain incomplete evidence until acceptance passes.
Plan review: accepted; root owns only integration and operations files. Product sources are read-only.
