**The clearest API problem in the logs is `/export` on client version 4.2.3.** About one in five recorded events in that group was marked `error` in both months. I used May to find the pattern and held June back to check whether it repeated.

| Comparison | May | June holdout |
|---|---:|---:|
| `/export`, client 4.2.3 | 21.8% (41/188) | 21.7% (46/212) |
| `/export`, other versions | 2.6% (25/964) | 3.2% (31/978) |
| `/search`, enterprise | 12.8% (35/274) | 4.1% (12/292) |
| `/search`, other plans | 3.4% (30/888) | 2.9% (27/944) |

The `/export` gap held in every June week. Matching the comparison traffic to the 4.2.3 traffic mix by week, plan, and region left an **18.5 percentage-point gap**. The 46 June errors were spread across 44 accounts. Across the other endpoints combined, June’s recorded error rate for 4.2.3 was 2.4%, compared with 2.9% for the other versions.

**The large May enterprise `/search` gap did not recur in June.** It fell from 9.4 percentage points to 1.2 points. Accounting for week, client version, and region put the June gap at 1.8 points. The May spike remains unexplained.

Overall, the file contains **6,924 events and 305 errors (4.4%)**. The recorded error rate fell from 4.8% in May to 4.1% in June. All 61 UTC dates were represented, with no duplicate event IDs or blank fields. The export lacks independent request totals, error codes, and retry linkage, so coverage and root cause remain unknown. The replicated finding is the elevated **recorded event error rate** for the `/export` and 4.2.3 combination.

[Exploration log](/tmp/api-exploration-log.md) · [June validation checks](/tmp/api-confirmation.md)
