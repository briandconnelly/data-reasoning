One real problem showed up, and it held up on data I had set aside before looking. The structural validator on my exploration log came back clean, and that only checks structure, not whether the analysis is right.

**Real problem: `/export` calls from client version 4.2.3 fail far more often than anything else.**
- **Exploration window (May 1 to June 16):** 66 of 290 calls errored (22.8%). Everything else ran at 3.5%.
- **Held-out check (June 17 to 30, 1,664 rows I had not looked at):** 21 of 110 errored (19.1%) against 3.0% for the rest. The 95% bootstrap interval for the difference is 9 to 24 points, so it doesn't include zero.
- **It needs both factors.** `/export` on other versions fails 2.8% of the time, and 4.2.3 on other endpoints fails 3.7%.
- **It isn't one bad account.** It shows up in every plan, region and week, across 64 different accounts.
- **Size:** I'd put the true rate nearer 19% than 23%, since the first number came from searching many combinations. It's about 1 in 5 export calls on a version that makes up roughly 17% of traffic.
- **Cause unknown:** the file has no error codes, latency or request details. I can tell you where the failures are, not why.

**Not confirmed: enterprise accounts may have more errors outside that cell.**
- In the first window, enterprise ran at 5.7% against about 2.7% for other plans.
- On the held-out rows it was 4.0% vs 2.6%, but the interval (−0.7 to +3.6 points) includes zero. That doesn't rule it out, but I wouldn't report it as real.

**Unexplained: May 16 has only 43 events, against a typical 124 a day.**
- The shortfall is spread across most hours, so it isn't a clean outage window.
- The file can't tell a real traffic dip from missing records or an incomplete export. Checking gateway counts for that day would settle it.

**Otherwise the data is clean:** all 61 days are present, with no duplicates or empty fields. Error rates are flat week to week, with no trend.

The log with the full looks, leads and held-out outcomes is at `exploration-log.md` in your working directory. The next step I'd take is pulling error codes for `/export` on 4.2.3 and checking what changed in that client version.
