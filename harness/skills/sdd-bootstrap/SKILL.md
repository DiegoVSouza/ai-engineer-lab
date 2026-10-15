---
name: sdd-bootstrap
description: Instala o harness, verifica o ambiente e roda o ensaio H00.
---

1. Leia `AGENTS.md` e `harness/GSD-LITE-PLUS.md`.
2. Inspecione git, Python, uv, Docker, Codex (versão e onde descobre skills/agents). Registre em `docs/harness/capabilities.json`.
3. Rode `bash scripts/harness/install.sh`; reinicie a sessão se necessário e confirme que as skills aparecem.
4. Acione `sdd-researcher` para fixar versões em `docs/harness/sources.lock.json`.
5. Ensaio H00 em branch temporária: feature de brinquedo (spec → plano com checker reprovando plano sem teste negativo → implementação → mutação que o verifier reprova → interrupção e retomada via STATE). Relatório em `docs/harness/H00-VERIFICATION.md` com comandos, logs e hashes.
6. Só marque G-HAR após o ensaio. Depois, siga `specs/00-MASTER-PLAN.md`.

Regras: `AGENTS.md` vale sempre; evidência antes de dizer 'pronto'.
