# Storage topology: orders partition

The orders partition was held only on db-03's local disk. It had no replica,
was not on any shared volume, and was not on network storage. No other host
mounted or could reach db-03's local disk.
