# Specification

Run the P06 console as its own service behind the existing commands: `python scripts/stack.py up|down` locally and `fly-up|fly-down` on Fly.

- Compose gains `idp-clients`, a one-shot that applies the public PKCE client through the Keycloak admin API, and `web`, which starts only after P05 is healthy and the client exists.
- Fly gains `supportops-lab-web` in the allowlisted inventory. `fly-up` applies the same client against the deployed Keycloak.
- `python scripts/stack.py check` also proves the console serves, reaches P05, and that the client rejects the password grant.
