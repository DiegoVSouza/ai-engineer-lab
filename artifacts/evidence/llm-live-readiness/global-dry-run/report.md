# Account-wide campaign dry-run

Status: `INCOMPLETE`. Generation authorized: `false`.

Projects: 6/6; unique semantic cases: 390.

| Project | Dev | Holdout | Pilot calls | Primary calls | Confirmation calls | Additive calls |
|---|---:|---:|---:|---:|---:|---:|
| p00 | 12 | 28 | 6 | 120 | 60 | 186 |
| p01 | 18 | 42 | 24 | 720 | 240 | 984 |
| p02 | 24 | 56 | 6 | 240 | 60 | 306 |
| p03 | 9 | 21 | 6 | 90 | 60 | 156 |
| p04 | 18 | 42 | 18 | 540 | 180 | 738 |
| p05 | 36 | 84 | 24 | 1440 | 240 | 1704 |

Aggregate planned calls: pilot 84, primary 3150, confirmation 840, all additive 4074.

Token ceilings: primary input=PENDING, primary output=PENDING, confirmation input=PENDING, confirmation output=PENDING.

Shared blockers:

- Groq account free-tier quota evidence: PENDING
- Shared cumulative request/input/output/spend ceilings: PENDING
- Cross-project account-wide ledger and lease enforcement: PENDING
- Independent reviewer approval and human review capacity: PENDING
- Authenticated model catalog preflight: REQUIRED BEFORE GENERATION
- Reservation gap: p00.confirmation_input token ceiling missing from project dry-run contract.
- Reservation gap: p00.confirmation_output token ceiling missing from project dry-run contract.
- Reservation gap: p05.primary_input token ceiling missing from project dry-run contract.
- Reservation gap: p05.primary_output token ceiling missing from project dry-run contract.
- Reservation gap: p05.confirmation_input token ceiling missing from project dry-run contract.
- Reservation gap: p05.confirmation_output token ceiling missing from project dry-run contract.

No provider or Docker access occurred.
