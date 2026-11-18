The validator ran with no findings. That is a structural check only, not a claim that the analysis is right.

## Summary

The file holds 6,924 events from 2026-05-01 to 2026-06-30, across 420 accounts and 4 endpoints. Overall, 4.4% of events are errors. The data is clean: no duplicates, no empty fields, and every day is present. There's a normal weekday/weekend rhythm. The overall error rate is flat by week. Two things hold up as real, and one looked like a problem but is fading.

### 1. Client version 4.2.3 fails on `/export` (holds up)
- Requests from client 4.2.3 to `/export` error about **21%** of the time. Every other version on `/export` errors about **2.7%**.
- On other endpoints, 4.2.3 looks normal, so this is specific to `/export`.
- I tried to break it three ways, and it survived all three:
  - **Not a few bad accounts:** the errors are spread over 70 accounts, with at most 2 each.
  - **Not a plan, region or week mix effect:** it appears in every plan, region and week.
  - **Same accounts, different version:** among the 231 accounts that used both 4.2.3 and other versions on `/export`, errors were 20.9% on 4.2.3 and 2.4% on other versions.
- I also checked it on a held-out week (2026-06-24 to 06-30) that I didn't look at while searching. It was worse there, at **27% (15 of 55)** against 2.7% for other versions.
- **Not known:** why it fails. The file has no error reason or status code, so I can't tell a client bug from the server mishandling 4.2.3 requests. The next step is to pull error details for 4.2.3 `/export` from the gateway logs.

### 2. APAC has no events for 73 hours (a data problem, cause unknown)
- No APAC events were logged from **2026-05-13 22:55Z to 2026-05-17 00:01Z**, which includes two weekdays. NA and EU were normal. No other gap in any region exceeds 7.3 hours.
- This file can't say whether APAC had an outage, a logging or export gap, or no traffic. To find out, compare it against gateway or load-balancer counts for those dates.
- If it was a real outage, it was invisible in this data. If it was a logging gap, any APAC analysis over that window is incomplete.

### 3. Enterprise `/search` errors were elevated, then faded (probably not a current problem)
- The error rate was 8.8% against about 3.5% for other plans, peaking at 22.6% in week 19 and falling to about 3% by week 25.
- The held-out week had 3 errors in 73 requests, which can't be told apart from baseline. It looks like a transient issue that has mostly cleared. The size of the early spike is probably overstated, because I picked it out by searching. Check whether an incident or deploy was recorded for weeks 19–22.

### Other notes
- The raw enterprise (6.5%) and `/export` (5.9%) error rates looked elevated. Part of that is the 4.2.3 effect and the rest is the enterprise `/search` episode. I found no separate problem there.
- Counts are per logged event, not per user, and I had no independent source to check coverage against.

The log, with looks, leads and the held-out check, is at `exploration-log.md` in the working directory. I used about 11 of the 25 tool calls I'd budgeted.
