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
(Adicionar ≥7 após a execução.)

## Números para citar
`PENDING` (tamanho do dataset, tempo do CI).
