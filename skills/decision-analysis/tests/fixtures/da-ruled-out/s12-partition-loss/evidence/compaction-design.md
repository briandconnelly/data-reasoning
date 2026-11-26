# Compaction job (build 412): design

The compaction job rewrites partitions on the host where it executes. It opens
partition files through the local filesystem only, holds no network storage
client, and issues no remote commands, so it can modify data only by executing
on the host that holds that data.
