**The clearest problem in the logs is `/export` on client version 4.2.3.** In the June 16–30 events I reserved for verification, 22 of 115 exports on 4.2.3 were marked `error` (**19.1%**), compared with 16 of 498 on other versions (**3.2%**). That’s a **15.9 percentage-point gap**.

| `/export` error rate | Client 4.2.3 | Other versions |
|---|---:|---:|
| May 1–June 15, initial review | 22.8% (65/285) | 2.8% (40/1,444) |
| June 16–30, verification | 19.1% (22/115) | 3.2% (16/498) |

The gap appeared in both halves of the verification window, in every region and plan, and among accounts that used both version groups. The 22 errors on 4.2.3 came from 22 distinct accounts. Outside `/export`, 4.2.3 had a **2.5%** recorded error rate versus **3.2%** for other versions. That makes the export and version combination the priority for investigation.

**Enterprise `/search` had a smaller, earlier spike that didn’t persist.** From May 1–14, enterprise search recorded **16.7%** errors (21/126) versus **3.2%** for other plans (13/405). By June 16–30, the rates were **3.4%** (5/146) and **3.8%** (18/480), respectively.

The export contains **6,924 events across 420 accounts**, with **305 marked `error` (4.4%)**. All 61 days are represented, event IDs are unique, and every field is populated. The CSV has no independent request totals, HTTP codes, or retry identifiers. The repeated `/export` gap is established for the recorded events. Its cause, the true production error rate, and the number of unique failed requests remain unknown.
