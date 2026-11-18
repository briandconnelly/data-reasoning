The clearest recurring problem in the logs is **`/export` on client version `4.2.3`**. About 22% of those events recorded an error in both months, versus about 3% for other versions using the same endpoint. I also verified a three-day gap in APAC records. Whether that gap reflects missing logs or a traffic interruption is unresolved.

| Signal | May | June holdout | What held up |
|---|---:|---:|---|
| `/export` on `4.2.3` vs. other versions | 21.8% (41/188) vs. 2.6% (25/964) | 21.7% (46/212) vs. 3.2% (31/978) | The gap appeared in all three regions and every June week. It stayed at 18.5 percentage points after accounting for region, plan, and half-month. The 46 June errors spanned 44 accounts, and other endpoints showed much smaller version differences. |
| Enterprise `/search` vs. other plans | 12.8% (35/274) vs. 3.4% (30/888) | 4.1% (12/292) vs. 2.9% (27/944) | The May spike was present in the logs. The June gap fell below the 3-point threshold I set before checking June and reversed in the second half. |

**APAC had zero records from May 14 through May 16 UTC.** EU and North America recorded 221 events over those dates, and APAC had records on every other date in the file. A second count reproduced the gap. Independent gateway counts would help distinguish a logging gap from a traffic interruption.

Across both months, the file contains **6,924 events from 420 accounts**, with 305 errors (4.4%). The 400 `/export` events on `4.2.3` account for 87 errors, or **29% of all recorded errors**. The file has unique event IDs and no blank fields. Without independent traffic counts or error details, it establishes the recurring association but leaves production-wide rates and root cause unresolved.
