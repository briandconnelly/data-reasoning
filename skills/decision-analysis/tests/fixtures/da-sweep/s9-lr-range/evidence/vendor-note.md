# Vendor note SV-2291: persistence of checksum mismatches across a re-read

Published by the controller vendor, revision 3.

Across the vendor's field population of this controller family, a mismatch that
reflects real on-disk corruption persists across an immediate re-read more
often than a transient mismatch does. The ratio of the two persistence rates
(persists given real corruption, divided by persists given a transient fault)
depends on the controller firmware revision: the vendor measures it at
0.5 on the oldest supported revision and 4 on the
newest, and gives no figure in between. Firmware revisions in a customer fleet
are not exposed by the controller's management interface.
