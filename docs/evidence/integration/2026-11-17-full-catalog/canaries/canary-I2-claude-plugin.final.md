Two real problems hold up, and one candidate I dropped because it didn't replicate. The file is structurally clean and nothing is missing: 6,924 events from 2026-05-01 to 06-30, no duplicates, no blank cells, and every day present.

## Real problems

**1. Client 4.2.3 fails on `/export` about 19–23% of the time.**
- On `/export`, 4.2.3 errors at 22.8% in May–mid-June, against 2.8% for every other version. 4.2.3 on the other endpoints looks normal.
- It shows up in every plan, region and week, so it isn't a spike or a single account.
- I first noticed it in 4.2.3's overall rate of 10%, against 3–4% for the other versions.
- It held up on the last 14 days of the file (6/17–6/30), which I hadn't looked at while forming the idea: 19.1% against 3.2%.
- The file has no error-code column, so I can't tell you what the errors are. The next step is to look at error logs for 4.2.3 `/export` calls and check whether a fixed client build exists.

**2. The `apac` region has no events for 73 hours, from 2026-05-13 22:55Z to 05-17 00:01Z.**
- `eu` and `na` kept normal volume throughout. The longest gap in any region otherwise is about 6 hours. Apac is normally about 25% of traffic, and it returns at that share afterward.
- It also explains the odd dip in total volume on May 14–16.
- This could be an apac outage, or apac logging or export that stopped. The file can't tell them apart. Compare against gateway or load-balancer metrics for that window.

## Dropped
Enterprise `/search` looked bad at 9.7% errors against 3.3% elsewhere. On the held-out 14 days it was 3.5% against 3.5%, so I treated it as noise from slicing the data many ways.

## Caveats
- Only about 115 events a weekday for 420 accounts is low for an API log, so the file may be sampled. I couldn't confirm that. Counts are only comparable within this file.
- I used the held-out 14 days to test findings 1 and the dropped candidate, so there's no untouched data left for a further check on 4.2.3. That would need new data or logs.

The working log, including the full list of what I examined, is `exploration-log.md`. The structural validator reported no findings.
