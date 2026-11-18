One real problem holds up. The rest of the data looks healthy, and one second lead did not hold up.

## What's going on
- **Data quality:** the file is clean. It has 6,924 events over 61 contiguous days (2026-05-01 to 06-30), with no missing values and no duplicate IDs. Traffic has a normal weekday/weekend rhythm.
- **Error rate:** overall errors run at about 4.4% and are flat week to week. No region or plan has a problem on its own.

## The real problem: `/export` on client version 4.2.3
- **Exploration window (05-01 to 06-23):** `/export` calls from client 4.2.3 errored on 72 of 345 (20.9%). `/export` on every other version errored on 50 of 1,720 (2.9%).
- **Held-out week (06-24 to 06-30):** I kept this week out of the exploration and tested only afterwards. 4.2.3 `/export` errored on 15 of 55 (27.3%), against 6 of 222 (2.7%) for other versions. This is a clear replication, with z of roughly 6.
- **Scope:** the problem is specific to the combination. 4.2.3 on other endpoints errors at the normal rate (2.0% in the held-out week, against 2.4% for other versions).
- **Spread:** it is steady week to week, appears in all regions and plans, and touches 70 distinct accounts in the error set. It isn't one noisy customer.
- **Impact:** 4.2.3 `/export` accounts for about 90 of the roughly 305 errors in the whole file.

The data can't tell you why. A version-specific bug is the obvious suspect, but the file has no HTTP codes or error details to confirm that. Start by checking what changed in `/export` handling in 4.2.3.

## The lead that did not hold up: enterprise on `/search`
- In the exploration window, enterprise `/search` errored at 8.8%, against 3.5% for other plans.
- In the held-out week it was 4.1% (3 of 73) against 1.8% (4 of 221). The direction is the same, but there are only 3 errors, so I can't distinguish it from noise.
- I'd call it unresolved, not a problem. It would need more data to settle.

## Caveats
- I can't verify completeness. There is no independent traffic count, and about 114 events a day is low for an API, so the file may be a sample. The 4.2.3 rate should hold either way, but treat the absolute counts as sample counts.
- `status` is only ok or error, with no error codes or latency.
- The held-out week is now used up. Further confirmation of D1 needs new data, for example next week's events or a 4.2.3 rollback comparison.
- Weekends in the data are quiet (about 65 to 80 events), and 05-16 was the lowest day at 43. I looked at this only as a coverage note, not as a lead.

The log, with the looks register and the predictions written before the held-out test, is at `exploration-log.md` in the working directory. I ran the plugin's structural validator on it and it printed no findings. That checks the record's structure, not the analysis.
