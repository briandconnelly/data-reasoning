# Investigation: How much did the /lp/summer-sale launch improve checkout conversion?

## Problem
- Decision informed: whether to credit/continue the campaign for conversion gains.
- Falsifiable question: change in session->checkout_reached rate, 2026-06-01..14, attributable to the launch of /lp/summer-sale (first sessions 06-08).
- Success criteria: answered = a causal number is given only if identified; otherwise state what is and isn't determinable.
- Stop condition: conclude once rivals (mix, checkout release, instrumentation) are tested; stop with limits if no comparison group identifies the effect.
- Effort budget: 12 queries.
- Assumption (headless, cannot ask): launch was not randomized; nothing identifies the effect. Route: full.

## Hypotheses
| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | causal | Campaign launch raised checkout conversion of site traffic | Post-launch rate on non-campaign pages (/home,/product) is not lower than pre | no rise anywhere | Overall rate rises after 06-08 launch | T1 | S1 |
| H2 | descriptive (estimand: overall rate change as pure mix of landing-page rates) | Overall change is composition: summer-sale sessions convert at a different rate than others, within-page rates flat | Within-page pre/post rates on /home,/product flat; overall moves with mix | within-page rates shift | Non-campaign pages' rate unchanged pre vs post (interval includes 0) | T2 | S1 |
| H3 | causal | v3.4.1 checkout refactor (06-10) changed conversion | step at 06-10 not 06-08 on non-campaign pages | no step at 06-10 | Non-campaign rate differs 06-10+ vs 06-08/09 | T3 | S1,S3 |
| H4 | data-artifact | Mobile session undercount 06-13/14 distorts denominators | mobile sessions drop with no matching order drop; checkout rate shifts when dropped days excluded | rate robust to excluding days | Excluding 06-13/14 changes post rate beyond noise | T4 | S1,S2 |

## Sources
| id | Origin | Acquired | Coverage notes |
| --- | --- | --- | --- |
| S1 | sessions.csv (9171 rows) | given | 06-01..14; summer-sale only from 06-08 |
| S2 | orders.csv (268) | given | 06-01..14 |
| S3 | deploys.log | given | 06-10 v3.4.1 checkout refactor |

## Data Validity
- Collection method: provided CSV exports (session log, order log) and deploy log; generating system not documented.
- Coverage matrix: see below.
- Field population: landing_page, device, checkout_reached populated on all rows.
- Coverage detail (orientation, counts only): summer-sale sessions 0 before 06-08, ~160/day after. Mobile sessions fall ~45% on 06-13/14 on every landing page (/home 212->123 etc.) while desktop stable: instrument gap or traffic drop, unknown.
- Coverage baseline: no independent session denominator -> unverifiable.
- Source completeness semantics: sessions.csv: UNKNOWN — no export contract or independent count discriminates unrecorded vs absent mobile sessions on 06-13/14.
- Orders (268) vs checkout_reached=yes (256) differ; orders not used as the outcome.
- Sensitivity: bootstrap/Wilson 95% intervals on contrasts.

## Tests
| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T1 | H1 | overall rate rises post | pre vs post, 95% CI of difference | CONTRADICTED | S1: 3.12% (131/4200) -> 2.52% (125/4971), diff -0.60pp [-1.29,+0.08]; unidentified pre/post contrast (concurrent v3.4.1 release, no comparison group) so cannot refute alone; campaign pages 6/1053 = 0.57% |
| T2 | H2 | non-campaign flat | /home+/product pre vs post CI | CONSISTENT | S1: 3.12% -> 3.04%, diff -0.08pp [-0.83,+0.67]; mix check by page: /home 2.71%->2.68%, /product 3.93%->3.76% |
| T3 | H3 | step at 06-10 | non-campaign 06-08/09 vs 06-10..14 CI | NON_DISCRIMINATING | S1: 3.00% -> 3.05%, diff +0.05pp [-1.11,+1.22]; interval wide, cannot exclude a +/-1pp refactor effect; deviation: window 06-10..14 not ..12 |
| T4 | H4 | robust to excluding 06-13/14 | recompute | CONSISTENT | S1: overall diff -0.57pp [-1.29,+0.16] excl 06-13/14 vs -0.60pp incl; artifact does not drive result; cause of mobile drop unknown (coverage UNKNOWN) |

## Amendments
(none)

## Conclusion
- Answer: No improvement is measurable, and none can be credited to the campaign. Overall checkout rate went 3.12% -> 2.52% (-0.60pp, 95% CI -1.29 to +0.08) after the 06-08 launch; summer-sale sessions converted at 0.57% (6/1053), far below other pages (~3.0%). Non-campaign pages were flat (-0.08pp). The observed shift is dilution by low-converting campaign traffic, not lift. The causal effect is not identified (launch not randomized, no comparison group, v3.4.1 checkout release 06-10 overlaps).
- Best supported: H2 (mix/dilution) - discriminating evidence T2 (within-page rates flat).
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | causal | UNRESOLVED | overall rate fell, but pre/post contrast unidentified; cannot refute; no evidence of lift |
  | H2 | descriptive | UNRESOLVED | best supported: non-campaign rates flat, campaign pages 0.57% |
  | H3 | causal | UNRESOLVED | T3 non-discriminating, wide interval |
  | H4 | data-artifact | UNRESOLVED | result robust to excluding affected days; mobile drop 06-13/14 unexplained, coverage UNKNOWN |

- Limitations: 14 days; only 6 conversions on campaign pages; checkout_reached (256) vs orders (268) disagree; mobile session drop 06-13/14 unexplained; no causal identification. Continuation: causal-identification-review (holdout/geo design) if installed.
