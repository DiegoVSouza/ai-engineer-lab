from pathlib import Path

root = Path(__file__).resolve().parents[4]
source = (root / "scripts/harness/migrate_local_operation.py").read_text(encoding="utf-8")
replacements = {
    "ten-call local operation free P00": "eight-call local operation free P01",
    "p00-local-operation-plus10-v1": "p01-local-operation-plus8-v1",
    "a1144017dfc7e44ec4b985a58b061f60321b10b9d7fc43d63897c5c851b80463": "6b678227c7d6ee138ed3495229e8bb365b930cafc9c241dece4df8d42cb6a12c",
    "6b678227c7d6ee138ed3495229e8bb365b930cafc9c241dece4df8d42cb6a12c\"\nP00_CAMPAIGN": "6c87609c7ebc7e58de8d5e9054fe1984ebcd20fec58bf26d0a60f73257ebbfeb\"\nP00_CAMPAIGN",
    "local-operation-envelope/policy-before.json": "p01-operation-envelope/policy-before.json",
    "028-local-operation-envelope": "029-p01-operation-envelope",
    "local-operation-envelope/plan-check.md": "p01-operation-envelope/plan-check.md",
    "local-operation-envelope/validate_plan.py": "p01-operation-envelope/prepare-proposal.py",
    "scripts/harness/migrate_local_operation.py": "scripts/harness/migrate_p01_operation.py",
    'after["projects"]["p00"]': 'after["projects"]["p01"]',
    '("requests", 10)': '("requests", 8)',
    '("input_tokens", 20480)': '("input_tokens", 16384)',
    '("output_tokens", 2560)': '("output_tokens", 2048)',
    'Decimal("0.002304")': 'Decimal("0.0018432")',
    '"authority": "explicit_user_reply"': '"authority": "user_authorized_free_local_operation_as_needed"',
    '"project": "p00"': '"project": "p01"',
    '"additional_calls": 10': '"additional_calls": 8',
    '"additional_input_tokens": 20480': '"additional_input_tokens": 16384',
    '"additional_output_tokens": 2560': '"additional_output_tokens": 2048',
    '"additional_economic_estimate_usd": "0.002304"': '"additional_economic_estimate_usd": "0.0018432"',
    "policy-migrations-local-operation.sqlite": "policy-migrations-p01-operation.sqlite",
}
for old, new in replacements.items():
    if old not in source:
        raise ValueError(f"missing migration template marker: {old}")
    source = source.replace(old, new)
source = source.replace('keys = ("project", "campaign_id", "case_id", "trial")', 'keys = ("campaign_id", "case_id", "trial")')
(root / "scripts/harness/migrate_p01_operation.py").write_text(source, encoding="utf-8", newline="\n")
