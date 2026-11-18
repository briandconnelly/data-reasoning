The one real problem in this log is that client version 4.2.3 fails on `/export` at roughly 10 times the rate of every other version. It held up when I checked it on data I hadn't used to find it.

## What's going on

- **Overall:** the log has 6,924 events, 61 days, 420 accounts, and 4.4% errors. It is structurally clean, with no duplicate IDs, no empty fields and no missing days. Volume follows a normal weekday/weekend rhythm, and the weekly error rate is flat at about 3.4–5.3%.
- **4.2.3 on `/export`:**
  - The first six weeks showed a 20.9% error rate for 4.2.3 on `/export`, against 2.9% for other versions on the same endpoint.
  - 4.2.3 isn't elevated on `/ingest` or `/search`, so the problem is specific to `/export`.
  - It shows up on every plan, region and week, and it's spread over 87 different accounts, with no account having more than 3 errors.
  - The higher error rate on `/export` overall comes entirely from 4.2.3.

## How I checked it

I held back the last 7 days (06-24 to 06-30) and wrote down what would count as a pass or fail before looking at them. In that window, 4.2.3 on `/export` failed 15 of 55 times (27.3%), against 6 of 222 (2.7%) for other versions. 4.2.3 off `/export` was normal (2.0% against 2.4%). It passed my pre-set bar of at least 3 times the other versions' rate and at least 10% absolute.

- **What this rules out:** the pattern being an artifact of the earlier weeks I searched.
- **What it doesn't rule out:** that 4.2.3 logs errors differently, or that the export itself is incomplete. The last week comes from the same file, not an independent source.
- **Not tested:** why it happens. The data shows the association only.

## Leads that didn't hold up

- **Enterprise errors on `/search`:** enterprise runs at 8.7% there, against about 3.5% for other plans. On the held-back week it was 4.8% against 2.2%, but that's only 3 errors. It missed my 6% bar without being contradicted, so I'd call it unresolved. It came from sifting about 24 small cells, so it could easily be noise.
- **Volume dip on 05-14 to 05-16:** daily counts were 95, 83 and 43, below the usual pattern. The shortfall is spread across hours and endpoints, with no clean outage gap. This file can't tell low traffic from dropped records. Checking it needs an independent traffic count (gateway or billing) for those days.

## Caveats

- The file looks like a sample or extract, and there's no independent count to check its completeness against.
- Magnitudes like "21%" were picked because they were the biggest gaps, so they're probably somewhat overstated. The 27% on the held-back week is the better estimate.
- The record validator ran and printed no findings. I didn't capture an exit code, so treat that as a likely clean pass, not a confirmed one.

## What to do next

The cheapest next step is to look at what 4.2.3 changed in its export path, and to check whether `/export` errors from that version share an error code or message. If you want that cause settled formally, I can hand the 4.2.3 finding to a proper investigation.

The full record is in `exploration-log.md`, with the scripts in `scripts/`, both in the working directory.
