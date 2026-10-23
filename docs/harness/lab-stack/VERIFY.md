# VERIFY â€” Unified local stack

Status: PASS_LOCAL_AND_FLY. The root stack remains running; model quality is PENDING.

| Gate | Command | Exit | Evidence |
| --- | --- | ---: | --- |
| Pinned product checkouts | `python scripts/stack.py checkout` | 0 | `artifacts/evidence/lab-stack/checkouts.txt` |
| Compose configuration and final bootstrap build/startup | `docker compose config --quiet`; `docker compose up -d --build --wait --wait-timeout 300` | 0 | `artifacts/evidence/lab-stack/final-startup.txt`; `config.txt` |
| Installed P00â€“P04 provenance and P00/P01/P02 smoke | `docker compose logs packages` | 0 | `artifacts/evidence/lab-stack/packages.txt` |
| Tenant OIDC API/MCP, independent HITL approver, P04/P05 durable workers, metrics/dashboard/trace and token revocation | `python scripts/stack.py check` | 0 | `artifacts/evidence/lab-stack/final-acceptance.txt` |
| Container recreation without volume removal | `docker compose up -d --build --force-recreate --wait --wait-timeout 300` | 0 | `artifacts/evidence/lab-stack/recreate.txt` |
| Stable credentials, CA, identity and completed records after recreation | `python scripts/stack.py persistence` | 0 | `artifacts/evidence/lab-stack/persistence.txt` |
| Published loopback URLs and HTTPS certificate validation | Python urllib with exported public local CA | 0 | `artifacts/evidence/lab-stack/host-endpoints.txt` |
| Existing container preservation and product source isolation | Compare prior inventory and product Git revisions/status | 0 | `artifacts/evidence/lab-stack/preservation.txt` |
| Root harness | `python scripts/harness/check.py --root .` | 0 | `artifacts/evidence/lab-stack/harness.txt` |
| Staged secret and key review | Compare staged blobs with generated credential values and private-key/bearer patterns | 0 | `artifacts/evidence/lab-stack/staged-review.txt` |

The first acceptance exposed missing CA/leaf key identifier extensions required by Python 3.13 strict TLS. The generator now includes SKI/AKI; HTTPS verification remains enabled. Keycloak readiness now checks `/health/ready` rather than a listening socket. The local database and identity state survive full container recreation. LocalStack queues and Jaeger traces are ephemeral. Fly deployment, public endpoint, OIDC, queue, autostart and snapshot evidence is recorded in `.planning/projects/lab-stack/phases/002-fly-machines/VERIFY.md` and `artifacts/evidence/fly/`. Model evaluation remains PENDING.
