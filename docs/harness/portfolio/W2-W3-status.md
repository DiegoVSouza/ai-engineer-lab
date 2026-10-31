# W2 and W3 status

Run 2026-10-31. Evidence: `artifacts/evidence/public-readiness/` (`clean-clone-w2.json`, `clean-clone-w2-p06-p07.json`, `audit-w3.json`). Nothing was made public in this run.

## W2: make each repository clonable

| Item | Result |
| --- | --- |
| P05 wheels | The five wheels named by `pyproject.toml` are tracked, hashes match `uv.lock`. The ignore file keeps ledgers and the other wheels out |
| P01 lab coupling | One test (`test_root_transport_encoder_parity_is_offline_and_utf8`) needs the lab's `live_provider_transport.py`. It is skipped with a printed reason outside the lab. The 19 other errors came from the `frameworks` dependency group not being synced, plus a dataset hash that broke on CRLF |
| P06 CRLF | `contract:check` normalizes line endings, with a test for CRLF and for a stale client. `.gitattributes` pins the contract |
| P00, P05 lab coupling | Found only by hosted CI on Linux. P00: two modules and one test module need lab files; they are skipped with a printed reason outside the lab (64 tests skipped there). P05: one test, same treatment |
| Executable bit | P00 scripts with a shebang had no mode bit; ruff failed on Linux |
| CI workflows | P06, P07, P08: Node setup, `npm ci`, Chrome. P01: `uv sync --all-groups`. P04: Terraform installed and full history fetched. P03 and P04 print the gate record on failure |
| HEAD size | The 37 third-party wheels (about 52 MB) are removed from the lab HEAD, manifest and hashes kept. History not rewritten |
| READMEs | Each README opens with a short case; Mermaid is exported from the site's flow data |
| Untracked files in P00 to P05 (244) | Not touched, not versioned in bulk |

Windows clean clone, fast gate: all nine pass after the fixes. Linux was checked by **hosted CI**, not by the local container check (the local run was stopped for memory and not repeated). `scripts/harness/linux_clean_check.py` exists and is untested.

## W3: GitHub

- `public_readiness.py` with the CV-free secret files: 0 local credential values in any history, 0 credential patterns. Six findings, the same classes as the earlier audit: four test or mock strings in P01 and P05, two in third-party wheel text kept in the lab history. No new finding.
- All nine project repositories and the lab were **pushed to private repositories** to get hosted CI. New private repositories: `supportops-console`, `diego-portfolio-ai`, `colagem-ui`.
- No repository was made public. Visibility stays a separate step, one repository at a time, after its hosted CI is green.
