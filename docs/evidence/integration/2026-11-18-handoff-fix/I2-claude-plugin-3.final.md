The data has one real problem: **client 4.2.3 calling `/export` fails far more often than anything else.** It holds up on data it was not found in.

## The problem
- **Error rate:** 4.2.3 on `/export` errors on about 21% of calls (72 of 345) in 05-01 to 06-23. Other versions on `/export` error on 2.9%.
- **It's specific to `/export`:** 4.2.3 on `/ingest`, `/report` and `/search` looks normal.
- **Held-out check:** I set aside 06-24 to 06-30 before looking, and only checked the candidate patterns against it afterwards. 4.2.3 on `/export` errored 27% there (15 of 55), against 2.7% for other versions.
- **Not one bad account:** it appears in every week (13–28%), in all three plans and regions, and across 70 different accounts, none with more than 2 errors.
- **Why it matters:** 4.2.3 alone is the top-line "version 4.2.3 is bad" signal, with a 9.4% overall error rate against about 3.5% for other versions. That signal is almost entirely this one endpoint.

The file has no error codes, so I can't say why it fails. The next step is a per-error-code breakdown for 4.2.3 on `/export`, plus the 4.2.3 release notes and server logs.

## What didn't hold up
- **Enterprise looks worse (6.5% errors vs about 3.8%).** Part of that came from enterprise on `/search` (8.7%), but that dropped to 4.1% (3 of 73) in the held-out week, so I wouldn't act on it. Enterprise was still higher on other endpoints in the held-out week (8.1%). The cause is unattributed and needs more data. The magnitude is probably overstated, because I picked it out of 12 plan-by-endpoint cells.
- **Week-to-week errors** are flat (3.4–5.3%), with no trend.

## Data caveats
- The file is clean: no nulls, duplicate IDs or odd values.
- I can't tell whether it's complete. It averages about 115 events a day for 420 accounts, so it may be a sample.
- 05-16 (a Saturday) has 43 events against 64–74 on other Saturdays. I can't tell a real quiet day from dropped rows, so it's worth asking whoever runs the export.

The held-out week is now used up, so any further confirmation needs newer or independent data.

The exploration log is `exploration-log.md` in the working directory. The plugin's record validator ran on it and printed nothing; I'm reading that as a pass, but it only checks structure.
