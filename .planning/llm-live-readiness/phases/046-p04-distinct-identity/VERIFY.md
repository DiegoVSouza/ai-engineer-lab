# Verification plan

PASS: `python -m unittest discover -s scripts/harness -p test_p01_p04_revalidation.py -v`, cwd lab, exit0, 11 tests. Tests cover exact new scope, old P04 identity rejection, tampered limits, retained history and reservation/no-replay. Provider access0, paidUSD0. This phase is not a P04 full gate and cannot dispatch.
