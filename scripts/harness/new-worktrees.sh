#!/usr/bin/env bash
# Uso: new-worktrees.sh p01 p02 ...  → cria ../lab-wt/<pid> em branch proj/<pid>
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"; WT="$ROOT/../lab-wt"; mkdir -p "$WT"
git -C "$ROOT" rev-parse --git-dir >/dev/null 2>&1 || { echo "Rode 'git init' e faça um commit inicial antes."; exit 1; }
for p in "$@"; do
  [ -d "$WT/$p" ] && { echo "já existe: $p"; continue; }
  git -C "$ROOT" worktree add -b "proj/$p" "$WT/$p" && echo "criado: $WT/$p"
done
