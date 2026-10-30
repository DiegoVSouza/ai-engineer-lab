# Specification

Decide from evidence whether the stack is usable in production. Fix what can be fixed locally, and turn the rest into concrete items. `python scripts/harness/production_readiness.py` checks the running stack and saves one result per item; nothing is marked ready without a command, exit code and stored output.
