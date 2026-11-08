# Investigation: How much did launching /lp/summer-sale improve checkout conversion?

Route: full. Assignment of exposure = "someone launched it" (campaign launched site-wide ~2026-06-08, not randomized); stated in request, no design identifies the effect. Assumption named: nothing identifies the effect; interactive clarification unavailable (headless).

## Problem

- Decision informed: whether to credit/continue the summer-sale campaign for conversion gains.
- Falsifiable question: did checkout conversion (sessions with checkout_reached=yes / sessions) rise after the campaign launch, and how much of any rise is attributable to the campaign, 2026-06-01..2026-06-14, all sessions in sessions.csv?
- Success criteria: answered means either an identified effect estimate with interval, or a demonstration that the number is not available from this data plus what the data does show (descriptive contrasts with intervals).
- Stop condition: conclude when no named unresolved alternative could reverse the answer; otherwise stop with limits.
- Effort budget: 15 tool calls.

## Hypotheses

| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | causal | The campaign launch raised site-wide checkout conversion | site-wide rate in 06-08..06-09 (launch, before v3.4.1) is above 06-01..06-07 | rate flat/below | site-wide rate 06-08..06-09 must exceed the pre-period rate (a campaign effect on conversion cannot appear as no change in the launch window unless offset; offset by a co-change is the stated limit) | T1 | sessions |
| H2 | causal | The v3.4.1 checkout-form refactor (2026-06-10T14:00Z) changed conversion | rate on non-campaign sessions steps at the deploy | no step in non-campaign sessions | non-campaign rate must differ after the deploy vs before it; a step before the deploy cannot be caused by it | T2 | sessions, deploys.log |
| H3 | descriptive (estimand: checkout rate of /lp/summer-sale sessions minus checkout rate of non-campaign sessions, same period 06-08..06-14) | Campaign traffic itself converts differently from other traffic, so any site-wide change is composition | campaign-session rate differs from non-campaign rate | equal rates | the two rates must differ by an interval excluding 0 | T3 | sessions |
| H4 | data-artifact | Mobile session records are missing on 06-13..06-14 (mechanism: mobile tracking loss) distorting rates | independent order count stays flat while mobile sessions halve | orders also fall ~half | daily orders (independent of session log) must not fall while mobile sessions fall | T4 | orders, sessions |

## Sources

| id | Origin | Acquired | Coverage notes |
| --- | --- | --- | --- |
| S1 | data/s1-conversion/sessions.csv (9171 rows) | local read | 06-01..06-14T16:56; fields session_id, timestamp, landing_page, device, checkout_reached |
| S2 | data/s1-conversion/orders.csv (268 rows) | local read | no session link, no device/landing page; client_version only |
| S3 | data/s1-conversion/deploys.log | local read | 3 releases, v3.4.1 2026-06-10T14:00:07Z |

## Data Validity

- Collection method: unknown (no export contract provided).
- Coverage matrix (orientation, day x device x landing page, S1): non-campaign sessions steady ~600/day 06-01..06-12 (desktop ~265, mobile ~335); campaign sessions 160/day from 06-08 (first appears 06-08). On 06-13 and 06-14 mobile sessions drop ~45-50% on every page (e.g. /home mobile 228 -> 123), desktop unchanged; hourly view shows the drop spans all hours. 06-14 ends 16:56 (partial day). No expected schedule or independent denominator for sessions beyond S2 orders.
- Field population: all five session fields 100% populated (no empty values); session_id unique.
- Coverage baseline: unverifiable for sessions except via orders (T4).
- Known instrument failures: none documented.
- Source completeness semantics:
S1: UNKNOWN — no export contract; the mobile 06-13/14 drop is either lost records or real traffic, and the source's own missingness cannot discriminate (T4 uses S2 as independent check).
S2: UNKNOWN — no export contract; no session link.
- Sensitivity checks performed: Wilson/bootstrap 95% intervals committed in advance for all rate contrasts (coverage 95%).

## Tests

| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T1 | H1 | site-wide rate 06-08..06-09 > 06-01..06-07 | two-proportion diff, 95% interval | NON_DISCRIMINATING | S1: 37/1520=2.43% vs 131/4200=3.12%, diff -0.68pp CI[-1.62,+0.25]; the interval brackets 0 and the predicted rise is only excluded above +0.25pp; unidentified pre/post contrast, so it cannot refute a causal claim anyway |
| T2 | H2 | non-campaign rate differs after 06-10T14:00Z vs before (06-08..06-10T14) | diff, 95% interval, split by device | NON_DISCRIMINATING | S1,S3: 2.93% vs 3.19%, diff -0.25pp CI[-1.35,+0.85]; mobile +0.12pp CI[-1.05,+1.30], desktop -0.54pp CI[-1.69,+0.61]; interval contains 0 and the effect sizes of interest (~1pp), so no step detected but detection limit ~1.1pp |
| T3 | H3 | campaign rate != non-campaign rate in 06-08..06-14 | diff, 95% interval | CONSISTENT | S1: 6/1053=0.57% vs 119/3918=3.04%, diff -2.47pp CI[-3.17,-1.76]; same in mobile (-2.40pp) and desktop (-2.55pp); excluding 06-13/14: 4/800=0.5% vs 93/3000=3.1%, diff -2.6pp CI[-3.39,-1.81]. Non-campaign sessions flat at 600/day, so campaign sessions are purely additive |
| T4 | H4 | orders/day does not fall on 06-13/14 while mobile sessions fall | compare S2 daily orders to S1 | CONSISTENT | S1,S2: orders equal checkout_reached=yes count exactly on 06-01..06-12; on 06-13 orders 23 vs 17 yes, 06-14 17 vs 11 -> sessions log missing ~6 checkout sessions/day while orders did not fall. Affects 06-13/14 rates only (T1 window unaffected; T3 sensitivity run without those days) |

## Amendments

- 2026-11-08: no amendments; no hypotheses added after seeing data.

## Conclusion

- Answer: no improvement is visible in the data (and no causal number is available). Checkout conversion did not rise after launch: 2.43% (06-08..09) vs 3.12% (06-01..07), diff -0.68pp, 95% CI [-1.62, +0.25]pp. Campaign sessions convert at 0.57% (6/1053) vs 3.04% for other traffic (diff -2.47pp, CI [-3.17, -1.76]). Non-campaign traffic is flat at 600 sessions/day and non-campaign conversion is unchanged (3.00% vs 3.12%), so the campaign added low-converting traffic and diluted the blended rate. A causal "how much improved" number is not available: the launch was not randomized and v3.4.1 (checkout refactor, 06-10) overlaps.
- Best supported: H3 (descriptive composition/dilution), via T3 (discriminating: campaign and non-campaign rates differ with CI excluding 0).
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | causal | UNRESOLVED | T1 NON_DISCRIMINATING: no rise observed (point estimate -0.68pp, CI upper bound +0.25pp) but the pre/post contrast is unidentified (no holdout, v3.4.1 overlaps), so a masked effect cannot be excluded |
  | H2 | causal | UNRESOLVED | T2 NON_DISCRIMINATING; detection limit about 1.1pp |
  | H3 | descriptive | UNRESOLVED | best supported (T3 CONSISTENT) |
  | H4 | data-artifact | UNRESOLVED | T4 CONSISTENT: session log appears to lose mobile/checkout sessions on 06-13/14; affects only those days |
- Limitations: no randomization or holdout; the campaign effect on users who would have arrived anyway (cannibalization of home/product traffic) is not separable — non-campaign volume was flat, which argues against cannibalization but does not prove it; orders have no landing page so order-level attribution is not possible; campaign sessions are few (1053) and rare checkouts (6) make the campaign-rate interval wide in relative terms; 06-14 is a partial day; source completeness for both files is UNKNOWN; v3.4.1 effect not detectable below ~1.1pp. For a design that could identify the effect, causal-identification-review (when installed) is the continuation; a holdout/geo or randomized landing-page split would be needed.
