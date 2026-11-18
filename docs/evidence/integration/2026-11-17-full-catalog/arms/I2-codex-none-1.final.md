**Two error patterns held up.** `/export` requests from client `4.2.3` failed at about 7.5 times the rate of other versions in both months. Enterprise `/search` had a separate spike in May that largely subsided in June.

| Segment | May error rate | June error rate |
|---|---:|---:|
| `/export`, client `4.2.3` | 21.8% (41/188) | 21.7% (46/212) |
| `/export`, other clients | 2.6% (25/964) | 3.2% (31/978) |
| `/search`, enterprise | 12.8% (35/274) | 4.1% (12/292) |
| `/search`, other plans | 3.4% (30/888) | 2.9% (27/944) |

- **`/export` on `4.2.3` was the biggest issue.** Its 400 events accounted for 5.8% of traffic and 28.5% of all errors. The higher rate held across every week represented in the logs, all three regions, and all three plans. Among the 248 accounts that used both `4.2.3` and another version for exports, the rates were still 21.8% versus 2.5%. The other endpoints showed no comparable spike on `4.2.3`.
- **The May enterprise `/search` spike was widespread.** The 35 errors were spread across 27 accounts and 18 days. The gap held after accounting for week, region, and client version. Removing the worst day still left an 11.3% error rate versus 3.5% for other plans. June showed a much smaller gap.

The logs cover **6,924 events across 420 accounts** from May 1 through June 30, 2026. Overall errors fell from 4.8% in May to 4.1% in June, while the export issue persisted. The file records only `ok` or `error`, so it establishes where failures were concentrated. Root cause, latency, and whether the issues continued after June remain unknown.
