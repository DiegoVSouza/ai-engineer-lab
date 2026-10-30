# Specification

Bind one replacement P04 workflow, `local-reviewed-operation-040-v1` / `fixture-reviewed-operation-040`, to the user's latest `faz isso` continuation instruction. It replaces neither the stopped `-038-` operation nor its evidence. The scope is at most one workflow, three provider calls, 12,288 input tokens, 1,536 output tokens, 30 seconds per provider call, explicit `openai/gpt-oss-20b`, and USD 0 paid.

The phase only installs and tests the root guard. It does not reserve, dispatch, migrate capacity, call a provider, build Docker resources, change ledgers, or alter `gossett_backend`.
