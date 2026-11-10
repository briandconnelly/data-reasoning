# Vendor note SV-2291: persistence of checksum mismatches across a re-read

Published by the controller vendor, revision 3.

For a checksum mismatch on this controller family, compare how often it
persists across an immediate re-read when it reflects real on-disk corruption
with how often it persists when it reflects a transient fault. The ratio of
those two persistence rates (persists given real corruption, divided by
persists given a transient fault) lies between 0.5 and 4
on every firmware revision this controller family has shipped, and the vendor
gives no narrower figure for any single revision: the ratio depends on the
revision, and the bound covers all of them. Firmware revisions in a customer
fleet are not exposed by the controller's management interface.
