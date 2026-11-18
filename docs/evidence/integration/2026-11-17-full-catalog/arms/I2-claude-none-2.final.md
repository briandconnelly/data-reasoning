Two things stand out in the logs, and one of them is a real problem. I checked both before writing this up.

**The dataset:** 6,924 events from 2026-05-01 to 2026-06-30, across 420 accounts. There are no duplicate IDs, no missing fields and no malformed timestamps. The overall error rate is 4.4% (305 errors), and it is flat across the two months and across hours of the day. Weekdays run at about 130 events a day and weekends at about 70.

**1. Client 4.2.3 on `/export` fails about 22% of the time. This is a real problem.**
- Those 400 calls had 87 errors (21.8%). Everything else combined had 218 errors in 6,524 calls (3.3%).
- It's specific to that combination. 4.2.3 on other endpoints errors at 3.4%, and `/export` on other versions errors at 2.9%.
- It isn't a mix effect:
  - Every plan shows it: enterprise 25%, growth 22%, starter 20%.
  - Every region shows it: apac 21%, eu 23%, na 22%.
  - It's there in both months (21.8% in May, 21.7% in June), so it isn't a one-off incident.
- It isn't one bad account. 82 of the 249 accounts that used this combination hit errors.
- It also explains why enterprise looks worst overall (6.5%). Without these calls enterprise drops to 5.3%, which is still the highest plan, so I can't fully explain that residual from this data.

My read is that 4.2.3 has an `/export` regression that has been live for the whole period. The logs show where it fails but not why. Check the 4.2.3 release changes to `/export`. If an upgrade path exists, 4.2.3 users are the ones who need it.

**2. There are no APAC events from 2026-05-14 to 2026-05-16. This is real in the data, but I can't tell what caused it.**
- APAC normally logs 30–34 events a day. Then it logs exactly 0 for three full days, and about 14 on the 17th as it recovers. NA and EU are normal throughout, apart from a weekend dip.
- It's complete silence from every APAC account, not a drop, so it looks like an APAC outage or an ingestion/logging gap rather than a change in user behavior. The logs only record that no events arrived, so they can't say whether the API was down or the logging was. Check infra and incident records for those dates.
- It's also why the volume dip on 05-14 to 05-16 looked odd.

**Looked at and not worth acting on:**
- 4.1.2 on `/report` had 7 errors in 74 calls (9.5%), against about 3 expected. That's too few calls to say anything, so I'd just keep an eye on it.
- `/export` is the worst endpoint overall (6.1%), but that's almost entirely the 4.2.3 issue above.
- The hourly error rates (2–7%) are noise at these sample sizes.

I only had the CSV, with no deploy history or incident records, so the causes above are hypotheses. The data itself supports the 4.2.3 `/export` failure rate and the 3-day APAC gap.
