# P00 — Fundação: como falar sobre testes de LLM e contratos

## Resumo de 1 página
Antes de construir agentes, fixei a base: um domínio Pydantic congelado, um cliente LLM com três modos (fake, replay, live) e um dataset sintético com golden set. Isso torna a lógica de controle testável sem custo e sem flakiness, e permite 4 projetos em paralelo sem conflito.

## Conceitos
- **LLM não é determinístico** → separe *lógica de controle* (roteamento, retries, limites) de *qualidade de texto*. A primeira se testa com fakes; a segunda com evals.
- **Fake / Replay / Live**: fake = roteiro programado; replay = respostas gravadas (cassettes) para benchmarks reproduzíveis; live = provedor real com orçamento.
- **Contrato congelado**: `shared/domain` versionado com semver; mudança via ADR evita quebra silenciosa entre projetos.
- **Dados sintéticos com seed**: reprodutibilidade; golden set com casos de fronteira (injection, inadimplência, reembolso alto).

## Trade-offs
| Decisão | Alternativa | Quando mudar |
|---|---|---|
| Cassettes JSONL próprias | VCR/libs prontas | se precisar de HTTP-level replay |
| uv workspace | Poetry/pip-tools | se o time já padroniza |

## Perguntas de entrevista
1. *How do you test code that calls an LLM?* — Separate control logic (deterministic fakes) from quality (evals over a golden set); use replay for reproducible benchmarks.
   *PT:* Separo lógica de controle (fakes determinísticos) de qualidade (evals em golden set); uso replay para benchmarks reproduzíveis.
2. *Why freeze a domain contract?* — Parallel teams need a stable interface; breaking changes go through ADR + version bump.
3. *How do you avoid flaky CI with LLMs?* — CI runs fake mode only; live runs are budgeted and manual.
4. *How do you report an LLM evaluation honestly?* — Freeze the candidate, bind prompt, schema, dataset and rubric by hash, run the unseen split once, and report the interval, the limits and what was waived.
   *PT:* Congelo o candidato, amarro prompt, schema, dataset e rubrica por hash, rodo o split inédito uma única vez e reporto intervalo, limites e o que foi dispensado.
5. *Why not quote the development score as accuracy?* — The director rules were written after reading those tickets, so 182/192 is in-sample; the single-use final split gave 54/60.
   *PT:* As regras do director foram escritas depois de ler esses tickets, então 182/192 é in-sample; o split final de uso único deu 54/60.
6. *What does the 90% measure?* — The whole system (prompt, code-decided tools, deterministic director) on Groq `openai/gpt-oss-20b`, not the bare model.
   *PT:* O sistema inteiro (prompt, ferramentas decididas em código, director determinístico) no Groq `openai/gpt-oss-20b`, não o modelo puro.
(Adicionar ≥7 após a execução.)

## Números para citar
Fonte: `projects/p00/artifacts/evidence/summaries/free-final-c1.json` e `projects/p00/docs/harness/failures.md`.
- Split final inédito, uso único (2026-11-07): 54/60 = **90,0%** (Wilson 95%: 79,9% a 95,3%); 18 de 20 casos acertaram as 3 tentativas; 0 falhas críticas. Escalações 6/12, respostas 36/36, pedidos de detalhe 12/12.
- Desenvolvimento (64 casos x 3): 157/192 (81,8%) só o prompt; 182/192 (94,8%) com o director, **in-sample**.
- Holdout lacrado antigo (dataset anterior, prompt few-shot): 29/84 (34,5%); não comparável.
- Limites: 20 casos e dataset sintético escrito pelo assistente; revisão independente dispensada pelo dono (`WAIVED_BY_OWNER`), isso não é verificação independente. A revisão humana foi feita pelo dono em 2026-11-09 (atestado do dono, `OWNER_REVIEWED`).
- `PENDING`: tamanho do dataset em outras versões, tempo do CI, e2e de serviços locais completo.
