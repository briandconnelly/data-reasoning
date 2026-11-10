# Checksum-mismatch alert on db-07

Tonight at 02:14 the nightly integrity job flagged a block checksum mismatch on
`db-07`. The on-call engineer re-read the block at 02:31 and the mismatch
persisted.

Files:

- `evidence/alert_history.csv` is a census: every checksum-mismatch alert our
  fleet has raised since 2024-01-01, one row each, with the outcome the
  follow-up review confirmed (`confirmed_corruption`). No alert is missing and
  none was sampled. Re-read checks only began this month, so the history does
  not record whether a mismatch persisted.
- `evidence/vendor-note.md` is the storage vendor's published characterization
  of re-reads on this controller family.
