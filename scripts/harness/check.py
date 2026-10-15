#!/usr/bin/env python3
"""Gate estrutural: arquivos obrigatórios, front matter, links relativos, seções das specs, higiene de números."""
import argparse, re, pathlib, sys
ap = argparse.ArgumentParser(); ap.add_argument("--root", default="."); ap.add_argument("--project"); ap.add_argument("--docs", action="store_true")
a = ap.parse_args(); R = pathlib.Path(a.root).resolve(); errs = []; warns = []
def need(p):
    if not (R / p).exists(): errs.append(f"ausente: {p}")
for p in ["AGENTS.md","README.md","harness/GSD-LITE-PLUS.md",".planning/PROJECT-SPEC.md",".planning/ROADMAP.md",".planning/STATE.md",".planning/decisions.md",
          "harness-kit/VERSION","harness-kit/bootstrap/harness_init.py","scripts/harness/new-project.py",
          "docs/standards/README-STANDARD.md","docs/standards/KNOWLEDGE-STANDARD.md"]: need(p)
for pid in ["P00","P01","P02","P03","P04","P05"]:
    if not list((R/"specs").glob(f"{pid}-*.md")): errs.append(f"spec ausente: {pid}")
# front matter de agents/skills
for f in list((R/"harness/agents").glob("*.md")) + list((R/"harness/skills").glob("*/SKILL.md")):
    t = f.read_text(encoding="utf-8")
    m = re.match(r"---\nname: (.+)\ndescription: (.+)\n", t)
    if not m: errs.append(f"front matter inválido: {f.relative_to(R)}")
    elif f.name != "SKILL.md" and m.group(1) != f.stem: errs.append(f"name != arquivo: {f.name}")
# The original P00-P05 briefs are retained as a curriculum archive.
# Their structure is still checked while they remain in the repository.
SEC = ["## Objetivo","## Entregáveis","## Public API","## Fases","## Verificação","## README exigido","## Documentação de conhecimento","## Fora de escopo"]
for f in (R/"specs").glob("P0*.md"):
    t = f.read_text(encoding="utf-8")
    for s in SEC:
        if s not in t: errs.append(f"{f.name}: falta seção '{s}'")
# links relativos em markdown
LINK = re.compile(r"\]\((?!https?:|#|mailto:)([^)\s]+)\)")
for f in R.rglob("*.md"):
    if any(x in f.parts for x in (".git","node_modules",".agents",".claude",".codex","lab-wt")): continue
    for l in LINK.findall(f.read_text(encoding="utf-8")):
        tgt = (f.parent / l.split("#")[0]).resolve()
        if l.split("#")[0] and not tgt.exists(): errs.append(f"link quebrado {f.relative_to(R)} -> {l}")
# docs gate: README de projeto
if a.docs and a.project:
    rd = R/"projects"/a.project/"README.md"
    if not rd.exists(): errs.append(f"README ausente: {rd.relative_to(R)}")
    else:
        t = rd.read_text()
        for s in ["## Problem","## Architecture","## Quickstart","## Results","## Design decisions","## Limitations","## Testing"]:
            if s not in t: errs.append(f"README sem seção {s}")
        if re.search(r"\b(p50|p95|cost|latency)[^\n]*\d", t) and "PENDING" not in t and not (R/"artifacts/runs").exists():
            warns.append("README cita métricas sem artifacts/runs")
for w in warns: print("WARN", w)
for e in errs: print("ERRO", e)
print(f"check: {'FAIL' if errs else 'OK'} ({len(errs)} erros, {len(warns)} avisos)")
sys.exit(1 if errs else 0)
