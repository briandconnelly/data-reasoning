**The `/export` error spike on client version `4.2.3` held up in the logs.** In the 15 days I reserved for verification, 19.1% of those events were marked `error` (22 of 115), versus 3.2% for other versions on `/export` (16 of 498). That’s a 15.9 percentage-point gap, above the 5-point threshold I set before opening the reserved data.

| Period (UTC) | `/export` on `4.2.3` | `/export` on other versions |
|---|---:|---:|
| May 1–June 15, initial review | 22.8% (65/285) | 2.8% (40/1,444) |
| June 16–30, reserved for verification | 19.1% (22/115) | 3.2% (16/498) |

The gap appeared in both halves of the verification window and in all nine plan-by-region groups. It also persisted when comparing versions within accounts that used both. The 22 errors came from 22 different accounts across 12 days. On other endpoints during the same window, `4.2.3` logged a 2.5% error rate versus 3.2% for other versions.

Across the full export, **305 of 6,924 events (4.4%)** were marked `error`. The flagged pair made up **5.8% of events and 28.5% of errors**. Enterprise accounts also looked worse in the initial review. In the reserved window, their gap versus other plans shrank from 1.56 to 0.68 percentage points after excluding the flagged pair, so the evidence for a broader enterprise issue is weaker.

The file has unique event IDs, populated fields, and records on all 61 days. It has no independent request totals, latency, HTTP codes, or error reasons. The recurring concentration is verified **among logged events**. Its production-wide rate and cause remain unresolved.

[Exploration log](/tmp/api-events-exploration.md) · [Verification ledger](/tmp/api-events-ledger.md)
