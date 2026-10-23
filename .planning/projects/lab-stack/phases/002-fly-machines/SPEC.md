# SPEC — Publish the portfolio runtime on Fly.io

Deploy the runnable P04 and P05 services, Keycloak, shared PostgreSQL/Redis and observability in `iad`. Keep P00–P03 libraries and instrumentation packaged in the product services rather than creating idle machines. Use minimal viable machine sizes, private networking for data services, persistent storage and backups, and stop HTTP machines after idle traffic. Keep fake-model mode and record model evaluation as PENDING.

Acceptance requires reproducible Fly configuration, explicit secret setup, healthy public API/Keycloak endpoints, private-only data services, documented backup/restore and checkpoint procedures, and machine policies that do not stop active workers or stateful dependencies. Do not remove local containers or volumes until their checkpoints and data backups are verified.
