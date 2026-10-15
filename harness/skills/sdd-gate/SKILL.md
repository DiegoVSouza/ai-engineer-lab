---
name: sdd-gate
description: Avalia gates G-CODE, G-CONTRACT, G-SEC do projeto.
---

Argumento: `<pid>`. Rode `python scripts/harness/verify.py --project <pid>`, acione `sdd-security-reviewer`. Gate sem evidência = incomplete. Registre o resultado no STATE.

Regras: `AGENTS.md` vale sempre; evidência antes de dizer 'pronto'.
