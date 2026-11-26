# Owner's losses

Supplied by the storage on-call lead, who decides, in hours of service impact.
"The job" is the build-412 compaction job.

| action | the job wrote to or deleted a partition file in the window | it did not |
| --- | --- | --- |
| roll back to build 411 | 0 | 4 |
| keep build 412 with a hotfix | 6 | 1 |
