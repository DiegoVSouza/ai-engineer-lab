# Public-readiness audit

Run 2026-10-31, read-only. Commands: `python scripts/harness/public_readiness.py`, `python scripts/harness/clean_clone_check.py`. Evidence: `artifacts/evidence/public-readiness/`.

**Verdict: no secret found in any Git history. Not ready to go public yet: three repositories fail a clean clone.** Nothing was pushed or made public.

## Secrets

Scope: every blob reachable from every ref in 10 repositories (lab, P00–P08), commit messages, and the contents of tracked archives (`.whl`, `.tar`, `.tgz`, `.zip`). Checked 13 credential patterns plus the literal value of 20 local credentials from `.env` and the Fly secrets file. The tools never print or store a value.

| Finding | Count | Conclusion |
| --- | --- | --- |
| Local credential values in history | 0 | Clean |
| Provider, GitHub, Fly or cloud key patterns | 0 | Clean |
| `client_secret=CLIENT_SECRET`, test `token_secret`, mock `repr` in P05 and P01 | 4 | False positives, read by hand with values masked |
| Example private key in botocore docs, `pydantic/types.py` | 2 | Third-party text inside a wheel |

An earlier run reported 453 hits. That was the audit's own bug: `GROQ_MODEL`, a public model name, was treated as a secret. Only credential-named variables count now.

Limits: patterns can miss a credential of an unknown format that was never in the local files. Deleted Fly secrets from older rotations were not checked. `.env` itself was never tracked.

## Clean clone

| Repo | Result | Cause | Fix |
| --- | --- | --- | --- |
| P00 | PASS through a bundle | Local clone is refused because `.git` belongs to the Codex sandbox user. Local only | None needed for the public repository |
| P01 | **FAIL** | Tests import `live_provider_transport` from the lab's `scripts/harness` | Vendor or package the module, or skip with a stated reason outside the lab |
| P02, P03, P04 | PASS | | |
| P05 | **FAIL** | `uv.lock` points to `artifacts/packages/supportops_async-0.1.4-py3-none-any.whl`, which is not tracked | Track the wheel, or publish it |
| P06 | **FAIL** | `contract:check` compares bytes, and a Windows clone has CRLF | Normalize line endings in the check |
| P07, P08 | PASS | | |

Fast gates only. `check_full.py` and service gates did not run in clean clones. No run was made on Linux, where hosted CI will run. `stack.py checkout` still needs the pinned commits to be pushed.

## Found after the audit

- P05: `artifacts/packages/.gitignore` ignores **all five** wheels in `pyproject.toml`, not only `supportops_async`, which was just the first error.
- CI: workflows never ran on a clean runner. P06 runs `npm` with no Node setup or `npm ci`; P07 and P08 need the same check. P00–P05 run `check_full.py` with no `uv sync`.

## Other findings

| Finding | Where | Action |
| --- | --- | --- |
| Commits not pushed | P00 116, P01 80, P02 29, P03 49, P04 87, P05 63 | Push on go |
| No remote | P06, P07, P08 | Create on go |
| Untracked files, mostly evidence | P00 56, P01 54, P02 4, P03 20, P04 80, P05 30 | Owner's earlier work, untouched. Decide per repository. They include local live ledgers (`.sqlite`) in P05, which must stay out of Git |
| Local username in paths | 118 files in history: lab 11, P00 10, P01 5, P02 10, P03 3, P04 52, P05 6 | Harmless, not a secret. Accept in history |
| Third-party wheels | 37 in lab evidence, 52 MB | Remove at HEAD before going public; check their licenses if kept |
| Duplicated source in evidence | P04 `source.tar` files, 3.4 and 7.6 MB | Accept or remove at HEAD |
| LICENSE | Added MIT to P00–P08 and the lab | Done |
| CV | `Diego_Souza_AI_Engineer_EVT_PT.docx` has a phone number | Ignored by Git |
| `colagem-ui` package metadata | P06 and P07 pin a tarball that still says `UNLICENSED` | Repack at 0.4.0 |
| README quality, hosted CI on fresh runners | All | W2 |
