# Module catalog

`harness_init.py` resolves the following names and records them in each generated project: `instructions`, `scripts-core`, `permissions`, `skills-base`, `ci-gates`, `long-running`, `reviewer`, `agent-runtime`, `prompts`, `agent-evals`, `tool-specs`, `trace-loop`, `observability`, `governance`, `multi-agent`, and `rag-eval`.

The initializer deliberately generates a small, reviewable baseline. Add a module's substantive implementation only when its profile condition is true and the project's spec needs it.
