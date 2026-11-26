# Incident timeline

- 01:40: the orders partition on db-03 was last read successfully.
- 02:55: queries against the orders partition on db-03 began failing.
- 03:10: on-call confirmed the partition's files were gone from db-03's local
  disk.

The incident window is 01:40 to 03:10 on 2026-11-24.
