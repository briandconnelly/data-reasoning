# Investigation: How much did launching /lp/summer-sale improve checkout conversion?

## Problem

- Decision informed: whether the summer-sale campaign is credited with a conversion lift (budget/renewal decisions for the campaign).
- Falsifiable question: what explains checkout conversion behavior for the site (and for the /lp/summer-sale segment specifically) from 2026-06-01 through 2026-06-14, before vs. after the campaign's first observed traffic on 2026-06-08?
- Success criteria: answered means either (a) a defensible causal estimate of the campaign's effect on checkout conversion is produced, or (b) it is established that no such number is available from this data, with what the data does show reported instead.
- Stop condition: conclude when no named unresolved alternative could reverse the answer, or when the identification question itself is settled (assignment mechanism is not stated as random or as-good-as-random anywhere in the fixture).
- Effort budget: ~20 shell probes over the 3 provided files (small local CSV/log fixture, no metered cost).

## Assumption stated (per skill's causal-routing guidance)

Nothing in the fixture states that traffic to /lp/summer-sale was randomly assigned, or that users were assigned to "see campaign" vs "not see campaign" by any mechanism independent of the outcome.
/lp/summer-sale is simply a new landing page that starts receiving sessions on 2026-06-08 — a launch, not an experiment.
Per SKILL.md's causal-routing section, this is the unidentified-assignment case: no comparison group is stated to be interchangeable with the exposed group.
Route: **full** (causal claim, no identifying design, and a same-window confound is visible in the data — a checkout-form deploy on 2026-06-10 — so more than one live explanation must be told apart).

## Hypotheses

| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | causal | Launching the campaign caused an increase in site-wide checkout conversion | site-wide conversion rate, weekday-matched, is higher after 2026-06-08 than before | site-wide conversion rate is flat or lower after 2026-06-08, weekday-matched | weekday-matched post-launch site-wide conversion rate must not be lower than pre-launch | T1 | sessions.csv, weekday-matched daily rates |
| H2 | descriptive (estimand: /home and /product checkout-reached rate, weekday-matched, post-launch minus pre-launch) | The blended-rate move is a composition artifact: campaign traffic is a new, low-converting segment added on top of unchanged existing channels | /home and /product per-weekday conversion counts are unchanged pre vs. post launch | /home or /product conversion counts shift materially pre vs post | /home and /product weekday-matched counts must not diverge outside sampling noise | T2 | sessions.csv by landing_page x day |
| H3 | causal (rival) | The 2026-06-10 checkout-form-refactor deploy (v3.4.1), not the campaign, drove any conversion change in this window | a discontinuity appears at 06-10, distinguishable from the 06-08 launch date, in /home and /product conversion | no discontinuity at 06-10 in /home or /product conversion | /home and /product conversion must show a level shift at 06-10 if this is the driver | T2 (same data, different date cut) | sessions.csv by day, deploys.log |
| H4 | data-artifact | checkout_reached (sessions.csv) does not reliably measure completed purchases (orders.csv), so a conversion metric built on it is untrustworthy | daily checkout_reached=yes counts diverge materially from daily orders.csv counts | the two counts match day for day | any day where the two counts diverge is a coverage/measurement finding requiring caveat, not necessarily a refutation of H1/H2 | T3 | sessions.csv, orders.csv, day totals |

## Sources

| id | Origin (file, query, system) | Acquired | Coverage notes |
| --- | --- | --- | --- |
| S1 | `sessions.csv` (9172 rows incl. header) | read in full via shell | 2026-06-01..2026-06-14, fields: session_id, timestamp, landing_page, device, checkout_reached |
| S2 | `orders.csv` (269 rows incl. header) | read in full via shell | 2026-06-01..2026-06-14, fields: order_id, timestamp, amount, client_version; no join key to sessions.csv |
| S3 | `deploys.log` (3 lines) | read in full via shell | releases v3.3.9 (06-03, /product copy), v3.4.1 (06-10, checkout form refactor + cart service bump), v3.4.2 (06-12, logging only) |

## Data Validity

- Collection method: flat CSV/log fixture files, presumably synthetic/generated for this test scenario; no external system to query.
- Coverage matrix (day x landing_page, checkout_reached=yes / total): /home and /product both present every day 06-01..06-14 at stable per-weekday volumes (400/200 on Mon-Fri, ~311/149-154 on the weekend); /lp/summer-sale present only 06-08..06-14 (160/day Mon-Fri, ~126-127 weekend) — consistent with a launch on 06-08, not a data gap.
- Field population: `landing_page`, `device`, `checkout_reached` are populated on all data rows (1 header row per file, excluded from counts above).
- Coverage baseline: no independent traffic denominator exists outside sessions.csv itself; /home and /product volumes repeat identically by weekday (e.g. Mon 06-01 = Mon 06-08 = 400 /home, 200 /product sessions), which is closer to a synthetic fixed schedule than to noisy real traffic, but is internally consistent and used as its own baseline for the weekday-matched comparison.
- Known instrument failures: none documented; see T3 for an observed count mismatch treated as a possible instrument issue rather than a documented one.
- Source completeness semantics: S1/S2 — orders.csv has no session_id or order-to-session join key, so "checkout_reached=yes" and "order recorded" cannot be reconciled at the row level, only at the daily-count level. UNKNOWN whether a day-level count mismatch reflects unrecorded sessions, unrecorded orders, or a timestamp/day-boundary artifact — no evidence in the fixture discriminates between these readings, so S1/S2 daily-count agreement is treated as corroborating, not as proof of joinability, and any mismatch is reported as a limitation, not attributed to a specific cause.
- Sensitivity checks performed: normal-approximation 95% CI on the weekday-matched difference of proportions for H1/T1; known-positive check run first on /product vs /home (a pair the raw rates show differing) to confirm the same method/sample sizes can detect a real difference before trusting a null-ish result on the pre/post contrast.

## Tests

| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T0 | (method check) | the two-proportion normal-approx CI method detects a known real difference (/product vs /home, whole-period rates) | compute 95% CI on /product-rate minus /home-rate | CONSISTENT (known positive obtained) | /product 104/2703=3.85%, /home 146/5415=2.70%; diff +1.15pp, 95% CI (+0.31pp, +2.00pp) — excludes 0, confirming the test is not underpowered by construction |
| T1 | H1 | weekday-matched (Mon-Fri) site-wide conversion rate post-launch (06-08..06-12) must not be lower than pre-launch (06-01..06-05) | orders/checkout_reached counts by day, summed Mon-Fri each period, over total sessions | CONTRADICTED | pre: 93/3000=3.10%; post: 97/3800=2.55%; diff -0.55pp, 95% CI (-1.35pp, +0.25pp) — point estimate is a decrease and the interval sits almost entirely below 0, discriminating against a meaningful increase (S1) |
| T2 | H2 | /home and /product per-weekday checkout_reached counts are unchanged pre vs post launch | pair each pre-launch weekday with its post-launch counterpart (Mon 06-01↔06-08, Tue 06-02↔06-09, ... Fri 06-05↔06-12) and compare /home, /product counts | CONSISTENT | exact match on all 5 weekday pairs: /home 10/11/12/10/11 both pre and post; /product 7/8/9/7/8 both pre and post (S1) — zero detectable movement in the pre-existing channels |
| T3 (H3) | H3 | /home and /product show a level shift at 06-10 (deploy date) distinct from 06-08 (launch date) | inspect the same weekday-paired counts for a break specifically at the Wednesday (06-03↔06-10) pair vs the other 4 pairs | CONTRADICTED | Wed pair (06-03↔06-10) matches exactly (12/9 both), identical to every other weekday pair; no discontinuity attributable to the 06-10 deploy is visible in /home or /product (S1, S3) |
| T4 (H4) | H4 | daily checkout_reached=yes counts equal daily orders.csv counts, every day | compare day-level counts from S1 and S2 | CONTRADICTED (partially) | counts match exactly for all 12 days 06-01..06-12; diverge on the weekend, 06-13 (checkout_reached=17 vs orders=23) and 06-14 (checkout_reached=11 vs orders=17) (S1, S2) |

## Amendments

- none.

## Conclusion

- Answer: this data does not support a causal estimate of how much the campaign improved checkout conversion, and what it does show is not an improvement.
  Site-wide, weekday-matched conversion went from 3.10% (pre-launch) to 2.55% (post-launch), a decrease whose 95% CI (-1.35pp, +0.25pp) sits almost entirely below zero — the opposite of the asked-for "improvement."
  The pre-existing channels (/home, /product) show byte-for-byte identical conversion counts on every matched weekday before and after the launch, including across the 06-10 checkout-form deploy — no channel outside the new landing page moved at all.
  The apparent site-wide dip is arithmetic, not evidence of harm either: /lp/summer-sale itself converts far below the rest of the site (6/1053 = 0.57% over its whole run vs. 2.70-3.85% elsewhere), so adding that segment on top of an unchanged base necessarily pulls the blended rate down. There is no comparison group here that tells you what conversion would have been without the campaign — only a before/after site average contaminated by that composition shift.
- Best supported: H2 (composition artifact) — via T2's exact match on every weekday pair, which independently refutes H1 and H3's implicit claim that some broad, non-page-specific effect (marketing halo, or the concurrent deploy) moved conversion for existing traffic. That refutation does not depend on the unidentified before/after contrast itself, so it stands even though nothing here identifies a causal effect.
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | causal | REFUTED | necessary prediction (post-launch rate not lower than pre-launch) failed under T1, an adequate test at the claim's own site-wide, weekday-matched grain |
  | H2 | descriptive (estimand: /home+/product weekday-matched rate, post minus pre) | UNRESOLVED | best supported — T2 CONSISTENT (exact match, no detectable movement); "UNRESOLVED" per the skill's closed status set, but this is the strongest-evidenced explanation and no rival explains the same exact-match observation |
  | H3 | causal | REFUTED | necessary prediction (a level shift at 06-10 distinguishable from 06-08) failed under T3 — the Wednesday weekday pair spanning the deploy is identical to every other pair |
  | H4 | data-artifact | UNRESOLVED | T4 shows agreement on 12/14 days and a divergence confined to the two weekend days; not promoted to REFUTED of H1/H2 because the weekday-matched comparison those hypotheses were tested on excludes the weekend days where the mismatch appears |
- Limitations:
  - No design here identifies a causal effect of the campaign: assignment to "see /lp/summer-sale" is not stated as random or as-good-as-random, so even the negative result above is associative, not a causal effect size — it rules out a *positive* causal story at the site-wide grain more than it estimates a negative one.
  - The weekend (06-13, 06-14) checkout_reached-vs-orders mismatch (T4) is unexplained: source completeness semantics are UNKNOWN for whether this reflects unrecorded sessions, unrecorded orders, or a day-boundary/timezone artifact. This does not affect the Mon-Fri comparison T1/T2/T3 rely on, but it means weekend-inclusive statistics (e.g. the whole-period /lp/summer-sale rate of 0.57% quoted above) should be treated as approximate.
  - What, if anything, is depressing /lp/summer-sale's own conversion rate (0-2 per 160 sessions/day) is not investigated here — device mix, offer mismatch, and page performance are all live candidates but none was tested; this is an open question, not a finding.
  - Constructive continuation: if a causal number is actually needed, `causal-identification-review` (when installed) is the next step — it would need a design this fixture does not contain (e.g., a stated randomized holdout, or a plausible as-good-as-random comparison group) to identify the effect at all.
