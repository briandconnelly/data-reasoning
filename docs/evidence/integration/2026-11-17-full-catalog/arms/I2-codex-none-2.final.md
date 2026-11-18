**The clearest reliability problem was `/export` on client version `4.2.3`.** It returned errors on **21.8% of requests (87/400)**, versus **2.9% (56/1,942)** on other versions. That’s 7.5 times the error rate and 29% of all recorded errors from just 5.8% of recorded requests.

The finding held up in both months, in every weekly bucket, and in all nine region-by-plan groups. Among the 248 accounts that used both `4.2.3` and another version for exports, the rates were 21.8% and 2.5%, respectively. Errors affected 82 accounts, and resampling by account put the 95% interval for the excess error rate at roughly **15 to 23 percentage points**. Other endpoints on `4.2.3` had a combined 3.4% error rate. The logs establish a persistent problem specific to this endpoint and version combination. They contain only `ok` and `error` outcomes, so the cause remains unknown.

Two other findings held up on closer inspection:

| Finding | What the logs show |
|---|---|
| **APAC disappeared from the logs for 73 hours and 6 minutes** | There were zero APAC events between May 13 at 22:55 and May 17 at 00:01 UTC. EU and NA still recorded 225 events across all four endpoints, and the next-longest APAC gap was 7 hours and 18 minutes. The gap is real. Whether it reflects missing telemetry, a routing change, or a service interruption is unresolved. |
| **Enterprise `/search` had an early-May error spike that eased** | May 1–24 had 31 errors in 213 requests (14.6%), spread across 23 accounts and all three regions. From May 25 through June 30, the rate fell to 16 in 353 (4.5%). Other plans stayed near 3% across both periods. |

Across the full May–June UTC window, the file contained **6,924 events from 420 accounts**, with **305 errors (4.4%)**. The overall error rate fell from 4.8% in May to 4.1% in June, while `/export` on `4.2.3` stayed near 22% in both months.
