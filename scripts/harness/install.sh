#!/usr/bin/env bash
# Publica skills e agents do harness. Confirme no bootstrap onde SEU Codex descobre cada um.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
mkdir -p "$ROOT/.agents/skills" "$ROOT/.codex/agents-md" "$ROOT/.claude/agents" "$ROOT/.claude/skills"
for s in "$ROOT"/harness/skills/*/; do n=$(basename "$s"); rm -rf "$ROOT/.agents/skills/$n" "$ROOT/.claude/skills/$n"; cp -r "$s" "$ROOT/.agents/skills/$n"; cp -r "$s" "$ROOT/.claude/skills/$n"; done
cp "$ROOT"/harness/agents/*.md "$ROOT/.claude/agents/"
cp "$ROOT"/harness/agents/*.md "$ROOT/.codex/agents-md/"
echo "skills: $(ls "$ROOT/.agents/skills" | wc -l)  agents: $(ls "$ROOT/.claude/agents" | wc -l)"
echo "Reinicie a sessão do Codex e confirme a descoberta (registre em docs/harness/capabilities.json)."
