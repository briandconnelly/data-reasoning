# Investigation: How much did launching /lp/summer-sale improve checkout conversion? (2026-06-01..06-14)

Route: full. Assignment = "someone launched it" (no randomization stated; could not ask - headless). Assumption named: nothing identifies the effect.

## Problem
- Decision informed: whether to credit/continue the campaign for a conversion lift.
- Falsifiable question: did site-wide session->checkout_reached rate rise after the 06-08 campaign launch, and is any rise attributable to the campaign (vs. the 06-10 v3.4.1 checkout refactor, traffic mix, instrumentation)?
- Success criteria: answered = a number is reported only if a design identifies it; otherwise report what is estimable and what is not.
- Stop condition: conclude when the campaign effect is shown identifiable or shown confounded with a rival that no available test separates.
- Effort budget: 15 tool calls.

## Hypotheses
| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | causal | The campaign raised checkout conversion of its own visitors / overall | summer-sale sessions convert above non-campaign sessions in the same days; non-campaign sessions flat 06-08..06-09 | no difference | the overall conversion rate must be higher in 06-08..06-09 (post-launch, pre-refactor) than 06-01..06-07 | T1 | sessions |
| H2 | causal | The 06-10 v3.4.1 checkout-form refactor raised conversion | rate steps up on/after 06-10 among non-campaign sessions | no step among non-campaign sessions | non-campaign sessions' rate must be higher after 06-10 than 06-08..06-09 | T2 | sessions, deploys.log |
| H3 | descriptive (estimand: campaign share of sessions and its effect on mix-weighted overall rate by landing page) | Overall change is a composition shift (campaign landing sessions have a different baseline) not a per-session change | per-landing-page rates stable pre vs post, overall moves via mix | per-page rates move | per-page rates for /home and /product must be unchanged pre vs post | T3 | sessions |
| H4 | data-artifact | Instrument/coverage gap (mobile sessions drop 06-13..06-14; checkout_reached vs orders mismatch) distorts rates | rate changes concentrated in the mobile 06-13/14 cells; orders/day not tracking | rates stable across cells | mobile session counts on 06-13/14 must be below the 06-08..06-12 level (observed in orientation: yes - holds) and rates in that cell must differ from adjacent days | T4 | sessions by day x device, orders |

## Sources
| id | Origin | Acquired | Coverage notes |
| --- | --- | --- | --- |
| S1 | data/s1-conversion/sessions.csv (9171 rows, 14 days) | 2026-11-08 | no nulls, no dup ids; mobile 06-13/14 = 242/238 vs ~430 prior |
| S2 | data/s1-conversion/orders.csv (268 rows) | 2026-11-08 | client_version 3.4.0/3.4.1 only; 268 orders vs 256 checkout_reached=yes |
| S3 | data/s1-conversion/deploys.log | 2026-11-08 | v3.4.1 checkout refactor 06-10 14:00Z; v3.4.2 logging only 06-12 |

## Data Validity
- Collection method: unknown (no export contract). Sessions have landing_page, device, checkout_reached.
- Coverage matrix: day x device session counts (orientation): stable ~260-270 desktop / 330-350 mobile 06-01..07; desktop ~350 from 06-08 (campaign adds ~160 sessions/day on /lp/summer-sale 06-08..06-12, ~127 06-13/14); mobile 06-13/14 falls to ~240 with no campaign-page decline of the same size. Hour-level and landing x device crossing to be added in T4.
- Field population: all fields 100% populated, no nulls.
- Coverage baseline: none independent (no traffic counter) -> coverage unverifiable, not clean.
- Known instrument failures: v3.4.2 "logging only" 06-12 could change event logging.
- Source completeness semantics: S1: UNKNOWN - no export contract or sentinel rows to discriminate unrecorded vs absent sessions. S2: UNKNOWN - 268 orders vs 256 sessions reaching checkout, no reconciliation key.
- Sensitivity checks: bootstrap 95% CI on contrasts (committed 95%).

## Tests
| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T1 | H1 | overall rate 06-08..09 > 06-01..07, 95% CI on difference excludes 0 | two-proportion diff + bootstrap | NON_DISCRIMINATING | overall 3.12% -> 2.43%, diff -0.68pp, 95% CI [-1.6, +0.24]pp (S1); interval contains small positive values; contrast unidentified (launch not assigned). Campaign sessions convert 0.31% vs 3.00% non-campaign same days (diff -2.7pp, CI [-3.8,-1.5]). Confound/aggregation check: reversal not present, drop is composition (H3) |
| T2 | H2 | non-campaign rate after 06-10 > 06-08..09 | diff + CI | NON_DISCRIMINATING | 3.00% -> 3.05%, diff +0.05pp, CI [-1.1,+1.1]pp (S1,S3); cannot detect <~1.1pp; also unidentified (single release) |
| T3 | H3 | /home,/product rates unchanged pre vs post | diff + CI | CONSISTENT | /home 2.71%->2.63%->2.70%; /product 3.93%->3.75%->3.77% (S1); non-campaign overall 3.12%->3.00%, diff -0.12pp CI [-1.2,+0.95]; overall drop explained by ~21-24% of sessions being low-converting /lp/summer-sale |
| T4 | H4 | rate in mobile 06-13/14 cell differs from adjacent days | day x device x landing rates | NON_DISCRIMINATING | mobile rate 2.8% (06-08..12) vs 2.7% (06-13/14), mobile session count drop unexplained, no baseline to verify coverage; does not change conclusion |

## Amendments
(none)

## Conclusion
- Answer: No improvement is visible. Overall session->checkout rate went from 3.12% (06-01..07) to 2.43% (06-08..09) and 2.55% after 06-10; campaign sessions reach checkout at 0.3-0.7% vs ~3.0% for everything else. Non-campaign conversion is flat (3.1%->3.0%). A causal lift number is not available from this data: the launch was not randomized and coincides with the 06-10 refactor and traffic changes.
- Best supported: H3 (composition shift), via T3: per-page rates unchanged, overall dip arises from adding low-converting campaign sessions.
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | causal | UNRESOLVED | T1 NON_DISCRIMINATING; unidentified contrast cannot refute; point estimate negative |
  | H2 | causal | UNRESOLVED | T2 NON_DISCRIMINATING; no step detected, detection limit ~1.1pp |
  | H3 | descriptive | UNRESOLVED | best supported for the overall dip (T3 CONSISTENT) |
  | H4 | data-artifact | UNRESOLVED | T4 NON_DISCRIMINATING; coverage unverifiable |
- Limitations: no counterfactual; S1/S2 completeness UNKNOWN; mobile session drop 06-13/14 unexplained; 268 orders vs 256 checkout sessions unreconciled.
