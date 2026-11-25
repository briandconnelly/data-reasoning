# db-03 orders partition loss

Last night the orders partition on `db-03` was lost. We must choose by noon
between rolling back to build 411 and keeping build 412 with a hotfix.

Every fact in these files was verified by the storage on-call lead this
morning; none is in dispute.

Files:

- `evidence/incident-timeline.md`: what was lost, and when.
- `evidence/storage-topology.md`: where the orders partition was held.
- `evidence/compaction-design.md`: the build-412 compaction job's design.
- `evidence/process-accounting.csv`: every process that executed on db-03
  during the incident window.
- `evidence/deploy-log.csv`: which build each database host was running.
- `evidence/db-03-device-log.txt`: db-03's disk controller log for the window.
- `evidence/owner-losses.md`: the decision owner's losses for each action.
