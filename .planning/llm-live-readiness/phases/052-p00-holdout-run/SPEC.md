# P00 holdout run (single use)

The owner chose the most honest measurement (2026-11-06): run the protected holdout once with the few-shot candidate that scored 25/36 on development. 28 holdout cases x 3 trials = 84 calls, inside the primary ceiling that already reserves them (no new policy delta, USD 0 paid, owner total-loss cap USD 5.00, independent review waived by the owner).

The authorization is bound to the sha256 of the prompt, schema, dataset and rubric. Editing any of them closes the holdout. Results are reported as measured, whatever they are. No tuning after viewing results; any changed candidate needs fresh confirmation (the 60-call confirmation reserve stays untouched here).
