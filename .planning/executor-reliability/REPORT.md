# Local executor reliability changes

The workspace now requests high reasoning effort through `.codex/config.toml`. The user-level default remains unchanged. Explicit session/client overrides and project trust can affect adoption; verify effective effort in a subsequent rollout. This is a configuration mitigation, not evidence that low effort caused early termination.

`python scripts/harness/audit_codex_rollout.py <explicit-rollout.jsonl>` streams a local rollout and emits per-turn model, effort, assistant phase counts and tool-call counts. It does not export message text, tool arguments/results or arbitrary event metadata. Exit 1 indicates malformed records (including an unfinished final line); rerun against a completed file before interpreting this as corruption. Exit 2 indicates an unreadable file. The diagnostic never resumes a session or replays work.

The inspected session retained commentary and final_answer metadata. Its contexts include gpt-6-luna/medium, gpt-6.1-terra/low and gpt-6.1-sol/low. This invalidates any comparison assuming equal model/effort settings. Local phase presence does not prove phase preservation in API requests. Transport-level finish reasons remain UNKNOWN; no runtime binary or wire adapter owned by this repository was found to patch. A valid behavioral comparison requires the same task snapshot, permissions, effort and available tools; no such provider experiment was authorized or run here.

Official configuration references checked on 2026-10-30:
- https://learn.chatgpt.com/docs/config-file/config-basic
- https://learn.chatgpt.com/docs/config-file/config-reference

No automatic continuation hook was installed: it could repeat effectful or uncertain operations. Existing live budgets, reservations, gate counters and stop conditions remain authoritative. The high setting can consume more Codex reasoning capacity; it does not change the projects' Groq budgets or authorize paid provider calls.

Planning commit: f0a0ba9. Implementation commit: see Git history for `fix(executor): add workspace effort and rollout diagnostics`.
