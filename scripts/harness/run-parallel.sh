#!/usr/bin/env bash
# Uso: run-parallel.sh p01 p02 p03 p04
# Abre uma sessão por worktree (tmux se houver) e imprime o prompt de kickoff.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; WT="$ROOT/../lab-wt"
for p in "$@"; do
  PROMPT="Leia AGENTS.md e specs/${p^^}-*.md. Execute sdd-plan $p, depois sdd-plan-check, sdd-execute, sdd-verify, sdd-gate e sdd-docs. Escreva somente em projects/$p e .planning/projects/$p."
  if command -v tmux >/dev/null; then
    tmux new-session -d -s "lab-$p" -c "$WT/$p" "codex \"$PROMPT\"" 2>/dev/null || echo "sessão lab-$p já existe"
    echo "tmux attach -t lab-$p"
  else
    echo "== $p =="; echo "cd $WT/$p && codex \"$PROMPT\""
  fi
done
