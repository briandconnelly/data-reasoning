The May–June logs show **persistent `/export` failures on client 4.2.3**, **elevated enterprise `/search` failures in May**, and **three days of missing APAC events**. I rechecked both error patterns after excluding the dates with missing APAC data. Both held up.

The file contains 6,924 events across 420 accounts, with 305 errors (4.4%). The overall error rate fell from 4.76% in May to 4.06% in June, mainly because search errors fell. The export problem persisted through the end of June.

| Finding | What held up |
|---|---|
| **`/export` on client 4.2.3** | **87 of 400 requests failed (21.75%)**, versus **56 of 1,942 (2.88%)** on other versions. The rate was nearly identical in May and June, and the gap appeared in every region and plan. Among the 248 accounts that used both 4.2.3 and other versions for exports, the rates were 21.80% versus 2.47%. The failures reached 82 accounts across 47 days. On the other endpoints combined, 4.2.3 had essentially the same error rate as other versions. |
| **Enterprise `/search` in May** | **35 of 274 requests failed (12.77%)**, versus **30 of 888 (3.38%)** for other plans. The gap held across all three regions and both halves of May. Matching the comparison for region and client version gave a 3.35% baseline. Enterprise search fell to **12 of 292 (4.11%)** in June, and the decline also held among enterprise accounts that used search in both months. |
| **APAC events missing May 14–16 UTC** | APAC recorded **zero events across all endpoints** for three full days, while EU and North America recorded 221. Every other date had APAC traffic. Comparable Thursdays, Fridays, and Saturdays suggest roughly **90 APAC events** would ordinarily appear over those three days. The file establishes the gap. Independent request or logging telemetry would distinguish a traffic interruption from a collection failure. |

I’d investigate the `/export` path for 4.2.3 first. That combination produced **29% of all recorded errors on 6% of traffic**. The logs identify where the failures concentrate. They contain only `ok` or `error` status, so the underlying failure mechanism remains unverified.
