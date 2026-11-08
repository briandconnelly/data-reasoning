# Investigation: why did weekly checkout conversion fall from 3.1% (wk 2026-06-01) to 2.5% (wk 2026-06-08)?

## Problem

- Decision informed: whether to roll back v3.4.1 / change the summer-sale campaign, or leave both alone.
- Falsifiable question: what accounts for the drop in orders/sessions between 2026-06-01..07 and 2026-06-08..14 (UTC, all sessions)?
- Success criteria: answered means one or more explanations account for the drop and survive a discriminating test, or the data is shown unable to separate them.
- Stop condition: conclude when no named unresolved alternative could reverse the rollback decision; otherwise stop with limits.
- Effort budget: 15 queries.

## Hypotheses

| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | descriptive (estimand: week-2 conversion of sessions landing on /lp/summer-sale minus week-1 overall conversion; and week-2 vs week-1 conversion excluding that page) | The drop is a composition shift: /lp/summer-sale (absent in wk1, ~11.5% of wk2 sessions) brings lower-converting traffic | summer-sale conversion below the wk1 rate, and non-summer-sale wk2 conversion close to wk1 | summer-sale converts at or above wk1 rate | summer-sale-page conversion must be below the wk1 overall rate (a diluting segment cannot convert at least as well as the baseline) | T1 | sessions (+ orders attribution, see Data Validity) |
| H2 | causal | The v3.4.1 checkout refactor (deployed 2026-06-10 14:00Z) lowered conversion | conversion on the non-summer-sale sessions falls after the deploy relative to before it | no fall after deploy | conversion step must occur at or after the deploy, not before it (6/8-6/9 pre-deploy non-summer-sale conversion must be above post-deploy) | T2 | sessions, orders by client_version, deploys.log |
| H3 | data-artifact | Session or order logging is incomplete in some device x day cell (mobile sessions 6/13-14 drop to ~240 vs ~330-440), distorting the ratio | an independent signal (orders/day, checkout_reached/day) stays normal on days when sessions fall, i.e. sessions are missing, not traffic | orders and checkout_reached fall in proportion to sessions | orders/day must not fall in proportion with the mobile-session drop on 6/13-14 | T3 | sessions, orders by day |
| H4 | descriptive (estimand: wk2-minus-wk1 conversion after standardizing to wk1 device mix) | Device mix shift (mobile share) explains the drop | device-standardized drop much smaller than raw drop | standardized drop ~ raw drop | device mix must differ between weeks enough, and device conversion rates must differ, to move the total by >=0.2pp | T4 | sessions by device (orders lack device: use checkout_reached as the device-level outcome) |

## Sources

| id | Origin (file, query, system) | Acquired | Coverage notes |
| --- | --- | --- | --- |
| S1 | data/s1-conversion/sessions.csv (9171 rows) | local file, 2026-11-08 | 2026-06-01T08:00Z..06-14T16:58Z; fields session_id, timestamp, landing_page, device, checkout_reached |
| S2 | data/s1-conversion/orders.csv (268 rows) | local file | 06-01..06-14; no session_id, no device, no landing_page: cannot be joined to sessions |
| S3 | data/s1-conversion/deploys.log (3 lines) | local file | v3.3.9 06-03, v3.4.1 06-10 14:00Z, v3.4.2 06-12 (logging only) |

## Data Validity

- Collection method: unknown export of web sessions and orders; no export contract provided.
- Coverage matrix: wk1 260-275 desktop / 327-353 mobile per day; wk2 desktop 320-370 per day, mobile 390-440 on 6/8-6/12 then 242 and 238 on 6/13 and 6/14. Week x landing_page x device: /lp/summer-sale has 0 sessions in wk1 and 1053 in wk2 (503 desktop / 550 mobile); /home and /product are present in both weeks on both devices. No tablet rows. Orders per day 17-23 on every day.
- Field population: no empty values in the fields used; device in {desktop, mobile}; checkout_reached in {yes,no}; orders client_version in {3.4.0, 3.4.1}.
- Coverage baseline: no independent schedule or denominator for sessions. Coverage is unverifiable for sessions; the mobile 6/13-14 dip is the one anomaly flagged for H3.
- Known instrument failures: none stated.
- Source completeness semantics:
S1: UNKNOWN — no export contract or independent session counter; its own missingness pattern cannot establish whether the 6/13-14 mobile dip is lost rows or real traffic.
S2: UNKNOWN — no export contract or independent order counter; orders cannot be linked to sessions, so a session-level conversion by page is unavailable from S2.
- Sensitivity checks performed: see Tests.

Definition: conversion = orders (S2) / sessions (S1) per week, to be checked against the quoted 3.1% and 2.5%. Segment-level conversion uses checkout_reached (S1) as proxy because orders carry no segment; the proxy's relation to orders is checked in T0.

## Tests

| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T0 | (definition) | orders/sessions ~3.1% wk1 and ~2.5% wk2 | count | CONTRADICTED | wk1 orders/sessions 131/4200=3.12%; wk2 137/4971=2.76%, not 2.5%. checkout_reached/sessions gives 3.12% and 2.51% (125/4971), matching both quoted figures, so the quoted metric is checkout_reached/sessions; orders = checkout_reached exactly on 6/1-6/12 each day, then orders exceed checkout_reached by 6 on 6/13 and 6 on 6/14 (S1 S2) |
| T1 | H1 | summer-sale checkout_reached rate < wk1 overall checkout_reached rate; wk2 rate excluding summer-sale within ~0.2pp of wk1 | rates by week x landing page, with bootstrap 95% CI on the contrast | CONSISTENT | summer-sale 0.57% (6/1053) vs wk1 3.12%, contrast CI95 [-3.22,-1.84]pp; summer-sale is 21.2% of wk2 sessions; wk2 excl. summer-sale 3.04% vs wk1 3.12%, contrast -0.08pp with CI95 [-0.84,+0.64]pp (so within the 0.2pp tolerance but the CI cannot exclude a ±0.8pp change). /home 2.71->2.68%, /product 3.93->3.76% (S1). Confound check: summer-sale desktop/mobile split 503/550 so it is not a device artifact (T4); aggregation check: page-level rates both fall by <=0.17pp, so no reversal |
| T2 | H2 | non-summer-sale checkout_reached rate lower in post-deploy (06-10 14:00Z+) than pre-deploy wk2 window (06-08..06-10 14:00Z) | split wk2 at deploy; CI on contrast; also orders per session by client_version over time | NON_DISCRIMINATING | pre 3.19% (n=1601) vs post 2.93% (n=2317), contrast -0.25pp, CI95 [-1.35,+0.81]pp contains 0 and the direction predicted, so a real effect of ~1pp relative to ~0.8pp noise cannot be separated; detection limit ~1pp (about a third of the rate). Daily non-summer-sale rates 6/10-6/12 (3.50, 2.83, 3.17) repeat wk1's 6/3-6/5 values; orders 23,17,20 equal wk1's 21,17,19 pattern, no visible step at the deploy. Deploy is not randomized; design cannot identify a causal effect (S1 S2 S3) |
| T3 | H3 | orders/day and checkout_reached/day fall in proportion to the mobile dip on 6/13-14 | daily orders, checkout_reached by device | CONTRADICTED | mobile sessions 440 (6/12) -> 242, 238 (6/13-14) while orders stay 23 and 17 (normal range 17-23); orders exceed logged checkout_reached by 12 over the two days where they are equal on all other days. Reading: about 380 mobile sessions (~190/day) and ~12 checkouts missing from S1; the prediction that orders fall in proportion failed, deterministic count comparison, no adequacy bound needed. Size of effect on the headline: adding back ~380 sessions and 12 checkouts gives 137/5351=2.56% vs 2.51%, +0.05pp. S1 completeness has no independent denominator (UNKNOWN), this rests on S2 as a partial independent signal (S1 S2) |
| T4 | H4 | device-standardized wk2-wk1 checkout_reached change differs from raw by >=0.2pp | direct standardization | CONTRADICTED | mobile share 56.0% wk1 vs 51.1% wk2; wk2 rates desktop 2.22%, mobile 2.79% reweighted to wk1 mix = 2.54% vs raw 2.51%: difference 0.03pp < 0.2pp. Deterministic arithmetic on the records, a true instance could not fail it by sampling. Device is not downstream of the exposure under study. (S1) |

## Amendments

- 2026-11-08: T0 outcome recorded as CONTRADICTED for orders/sessions; the quoted 3.1%/2.5% are checkout_reached/sessions. T1/T2/T4 use that metric as preregistered. T3 also surfaced a possible session under-recording on 6/13-14 mobile; noted as a limitation, no new hypothesis added.

## Conclusion

- Answer: the drop is mostly a composition effect. A new landing page, /lp/summer-sale, appears only in week 2 and carries 21.2% of week-2 sessions at a 0.57% checkout rate. Excluding it, week-2 conversion is 3.04% against 3.12% in week 1 (-0.08pp, CI95 [-0.84,+0.64]pp). The summer-sale traffic accounts for about 0.53pp of the 0.61pp drop.
- Best supported: H1 (T1). The v3.4.1 deploy (H2) is not shown to matter, but its effect cannot be excluded below about 1pp; the data cannot tell. This is associative wording: nothing randomized the traffic mix.
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | descriptive | UNRESOLVED | best supported: T1 CONSISTENT, discriminating against H2 and H4 because the non-summer-sale rate is flat while the summer-sale rate is 0.57% |
  | H2 | causal | UNRESOLVED | T2 NON_DISCRIMINATING, CI [-1.35,+0.81]pp; deploy is not an identifying design |
  | H3 | data-artifact | UNRESOLVED | T3 shows probable missing mobile sessions on 6/13-14 (orders exceed logged checkouts by 12), but effect on the headline is +0.05pp and S1 completeness has no independent baseline |
  | H4 | descriptive | REFUTED | T4: standardized 2.54% vs raw 2.51%, the necessary >=0.2pp prediction failed |
- Limitations: S1 and S2 completeness UNKNOWN (no export contract or independent counters); orders cannot be joined to sessions or pages, so page-level conversion uses checkout_reached; the 6/13-14 mobile session shortfall is unverified; a small checkout regression after v3.4.1 (<~1pp) is not excluded; why summer-sale traffic converts poorly (traffic quality, landing-to-checkout path, offer) is untested and unattributed. Continuation for the deploy question: causal-identification-review (not installed here).
