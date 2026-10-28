# Rotation continuity audit

Audit the actual campaign transport before resuming P00 C2. Preserve all historical attempts, UUIDs, receipts, reservations and unknown usage. Account topology and Free billing are user attestations. Paid authorization is USD 0.

The campaign uses scripts/harness/live_provider_transport.py; the generic GroqKeyRotationTransport is not sufficient evidence about campaign retries. Selection currently derives from accounted_attempts after reservation. Verify crash persistence, attribution and organization limits before declaring those controls complete. Do not infer historical account attribution.
