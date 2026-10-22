# Plan

allowed_write_paths: `.planning/projects/harness-kit/phases/002-ignore-local-environments/`, `scripts/harness/check.py`, `artifacts/harness/`.

1. Exclude virtual-environment directories from the Markdown link scan.
2. Read project READMEs explicitly as UTF-8 on every platform.
3. Run the root harness gate and two project documentation gates.

No project runtime, fixture, or contract changes are allowed.
