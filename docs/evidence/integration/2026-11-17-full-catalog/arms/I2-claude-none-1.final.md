**Short version:** one problem holds up. Version 4.2.3 of the client fails on `/export` about 7 times as often as everything else. There's a second, smaller pattern on enterprise `/search` that looks real but needs more checking. Nothing else stands out.

**Dataset:** 6,924 events from 2026-05-01 to 2026-06-30, across 420 accounts. There are no duplicate IDs and no missing values. The overall error rate is 4.4% (305 errors). Volume is about 130 per weekday and about 70 per weekend day. Daily error rate bounces between 0% and 10%, which is what noise looks like at 70–160 events a day. There's no trend and no spike.

## 1. Client 4.2.3 on `/export`: real

| | Events | Errors | Error rate |
|---|---|---|---|
| 4.2.3 + `/export` | 400 | 87 | **21.7%** |
| everything else | 6,524 | 218 | 3.3% |

I tested whether this could be an artifact, and it held up each time:
- **Not a one-off:** 4.2.3 is fine on `/ingest` (1.5%) and `/search` (3.7%). The other 4.x versions are at 0.6–5.6% on `/export`.
- **Not one customer:** the 87 errors are spread over 82 different accounts, and no account has more than 2.
- **Not a plan or region effect:** the rate is 20–25% on all three plans and 21–23% on all three regions.
- **Not a transient incident:** it's present throughout both months, at 17–29% in every half-month window. It hasn't been fixed or gotten worse.
- **Not a small-sample fluke:** the gap is about 17 standard errors.

4.2.3 is also our 3rd most-used version (1,187 events), so this affects a lot of traffic. It accounts for 87 of the 305 errors, or 29% of all errors from 17% of traffic. Whatever 4.2.3 changed in its export path is the first place I'd look. Rolling users off 4.2.3 would be a reasonable stopgap.

## 2. Enterprise `/search`: probably real, less certain

Enterprise accounts have a higher error rate than the other plans (6.5% vs about 3.8%). About half of that gap comes from 4.2.3 `/export`. After removing it, enterprise `/search` is still high:
- **Enterprise `/search`:** 8.3% (47 of 566)
- **Other plans' `/search`:** 3.1% (57 of 1,832)

That's about 5 standard errors, so it's unlikely to be chance. Two cautions: I found it by slicing the data many ways, and I haven't ruled out a cause I can't see in this file, such as enterprise customers sending heavier queries. Treat it as a lead worth a look, not a conclusion.

## Limits
- **Status:** the log only says `ok` or `error`, with no error codes, messages or latency. I can show where failures cluster but not why.
- **Volume:** there are no request-volume or customer-impact figures, so I can't size the business effect.
- **Tools:** pandas wasn't installed, so I used plain Python. Nothing was modified.

Do you want me to dig further into the enterprise `/search` pattern, or write up the 4.2.3 finding for whoever owns the export code?
