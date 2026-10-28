# Conservative credential rotation

Rotate configured authorized credentials by the durable aggregate accounted-attempt ordinal after reservation. Preserve the existing aggregate authority and all limits; do not multiply quota or retrospectively assign history to accounts. This enables credential rotation with conservative shared ceilings while separate account identities/billing remain unverified. Never retry a failure through another key. A changed root source fingerprint requires renewed P00 candidate provenance before generation.
