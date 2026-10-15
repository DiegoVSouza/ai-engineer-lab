# README-STANDARD — README altamente explicativo (todo projeto)

Idioma: **inglês** (`README.md`) + `README.pt-BR.md`. Gate G-DOCS valida as seções com `check.py --docs`.
Regra: todo comando foi executado; todo número vem de `artifacts/runs/<run_id>` (cite o id) ou é `PENDING`.

## Seções obrigatórias (nesta ordem)
1. **Título + pitch** (2 frases: problema e resultado) + badges de CI.
2. `## Problem` — contexto de negócio (SupportOps Desk), quem sofre, por que é difícil.
3. `## Solution at a glance` — 5 bullets + uma imagem/GIF/asciinema (ou `PENDING`).
4. `## Architecture` — diagrama Mermaid + fluxo de uma requisição passo a passo + tabela de componentes (responsabilidade, tecnologia, por quê).
5. `## Quickstart` — ≤5 comandos, pré-requisitos, tempo estimado, saída esperada; modo `fake` primeiro.
6. `## How it works` — explicação por módulo, com links para o código.
7. `## Results` — tabela com custo, latência p50/p95, qualidade nos evals, taxa de sucesso; método e `run_id`.
8. `## Design decisions` — 5–8 ADRs resumidas (decisão, alternativas, trade-off).
9. `## Testing` — como rodar unit/contrato/evals/adversarial; o que cobre.
10. `## Security & reliability` — guardrails, limites, idempotência, modelo de ameaças resumido.
11. `## Limitations & next steps` — honesto.
12. `## Repo map` e `## License / Contributing`.

## Qualidade
- Um leitor externo entende problema, arquitetura e resultados só pelo README.
- Sem jargão sem definição na primeira aparição; glossário curto se preciso.
- Sem afirmações sem evidência; "PENDING" é aceitável, número inventado não.
