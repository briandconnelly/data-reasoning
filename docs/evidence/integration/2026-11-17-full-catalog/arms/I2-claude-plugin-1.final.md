Two things in the logs look real, and I'm less sure of a third.

I used 7 of a planned 20 queries. The full record, with the looks register and the search behind each lead, is in `exploration-log.md` in the working directory. The log passes the structural validator, which checks format only, not whether the analysis is right.

## What the data is
There are 6,924 events from 2026-05-01 to 2026-06-30, spread over 420 accounts. The file has no empty fields, no duplicate IDs and no malformed timestamps. Volume follows a normal weekday/weekend rhythm. 4.4% of events are errors. The only status values are `ok` and `error`, with no latency, error codes or reasons.

## Real: client 4.2.3 fails on `/export`
- **Rate:** 4.2.3 on `/export` errors on 72 of 345 events (21%). Every other version on `/export` errors at 2.9%. 4.2.3 on the other endpoints is normal, at 3.6%.
- **Spread:** it appears on all three plans and all three regions. It spans 232 accounts, and the five worst account-level counts make up about 10% of the errors. It's steady week to week rather than an incident burst.
- **Other cells:** the next most unusual version-and-endpoint cell out of 36 is 10% on 69 events.
- **Holdout:** I held back the last week (06-24 to 06-30) while searching. It shows 15 of 55 errors (27%) for 4.2.3 on `/export`, against 2.4% for everything else.
- **Significance:** a shuffle test puts the chance of this by luck below 0.02%.
- **Limit:** the file records only that it happens. The cause would have to come from server logs or a comparison of the 4.2.3 export code with 4.2.0. 4.2.3 is also among the most-used versions, so this affects a lot of traffic.

## Real, but a data gap: no APAC events for 73 hours
- **Gap:** from 05-13 22:55Z to 05-17 00:01Z, APAC logged nothing, while EU and NA kept going. The next-longest APAC gap is 6 hours. This is also why May 14–16 looked like a volume dip.
- **Open question:** this file can't tell a real APAC outage from lost logging. Ask whoever owns the APAC log pipeline about 05-13 to 05-17.
- **Side effect:** any APAC statistic that includes those days is understated.

## Weak, don't act on it: enterprise errors in May
Enterprise accounts show more errors even without 4.2.3 (5.3% against about 2.9%). The excess is mostly on `/search` and `/report` in May and early June, and it disappears from about 06-08. I looked at many slices, the weekly counts are small, and I never checked it on the holdout week. Treat it as probably overstated until someone checks server logs.

## Limits
The file can't show whether it is all traffic or a sample, so absence of events means different things depending on the source. The 4.2.3 result is a pattern in the logs, not a diagnosed cause.
