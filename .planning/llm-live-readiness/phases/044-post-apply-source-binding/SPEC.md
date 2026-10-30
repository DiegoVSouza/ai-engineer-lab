# Specification

Remove the obsolete P00 historical-source-blob constraint after the phase039 migration is durably `APPLIED`. The migration must still require the original P00 blob while preparing or applying, and a changed P00 source may be accepted only after the append-only audit proves both `prepared` and `applied`. This is an offline binding repair; it cannot change policy, ledgers, reservations, gate counters, or authorize provider dispatch.
