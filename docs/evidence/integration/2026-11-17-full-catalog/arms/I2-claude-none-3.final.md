There is one real problem in the logs, plus a data gap that is probably an ingestion issue.

**Overview:** The file has 6,924 events from 2026-05-01 to 2026-06-30, across 420 accounts. The overall error rate is 4.4%, with 305 errors. The data is clean: no duplicate IDs, no malformed rows, no out-of-order timestamps, and each account stays on one plan and one region. Traffic follows a normal weekday/weekend pattern.

**1. Client 4.2.3 fails on `/export` about 22% of the time**
- Events on `/export` from client 4.2.3 errored in 87 of 400 cases (21.8%). Every other combination of client version and endpoint sits at roughly 0.6–9%, and the rest of the dataset errors at 3.3%.
- Several things suggest the cause is the 4.2.3 client on `/export` rather than something else:
  - **Not a plan effect:** Enterprise has a higher overall error rate (6.5%), but 4.2.3 `/export` is bad on every plan: 25% on enterprise, 21.5% on growth, 19.9% on starter. Other `/export` traffic on enterprise is only 3.9%.
  - **Not a region effect:** It is about 21–23% in all three regions.
  - **Not one bad account:** The 87 errors are spread across 82 accounts, and no account has more than 2.
  - **Not a one-off incident:** It runs at roughly 15–30% every week for the full two months.
  - **Not chance:** I shuffled the error labels 500 times, and no client-version/endpoint cell came close to 21.8%.
- **Where it matters:** 4.2.3 is about 17% of all traffic and the second most used version. It also accounts for about 114 of the 305 errors.
- **Limits:** The logs only have a status of `ok` or `error`, so I can't say why it fails. The next step is a look at the 4.2.3 changelog for `/export` changes, and at server-side error messages for those requests. This is a correlation, not a confirmed root cause. 4.2.3 may also differ in some way I can't see, such as payload size. 4.3.1 and 4.4.0 don't show the problem on `/export`, so upgrading looks like a likely fix.

**2. APAC data is missing from May 13 22:55Z to May 17 00:01Z**
- That is a gap of about 3 days. The next-longest APAC gap is about 7 hours.
- It explains the low daily counts on May 14–16, such as 43 events on Sat May 16. It looks like a collection or ingestion outage rather than real traffic. I can't tell from this file whether APAC was actually down or only unlogged, so check that.
- APAC's slightly higher error rate of 4.9% is not a concern, since it is within what chance would produce.

**Other things I checked that look fine**
- **Client versions:** Old versions (3.9.4, 4.0.x) are declining and 4.3.1 and 4.4.0 are growing, which looks like normal rollout.
- **Time patterns:** Error rates are flat across the two months, and the hourly variation looks like noise.
- **`/ingest`:** It has the lowest error rate, at 1.9%.
