# Investigation: Did Assist (cutover 2026-06-08 00:00Z, no holdout) cause faster recovery, and how many responder-hours are attributable?

## Problem
- Decision informed: expand Assist company-wide; whether Finance books responder-hour savings.
- Falsifiable question: for the 420 pilot incidents opened Jun 1-14 (identity, storage), does time-to-close / responder_minutes differ by workflow beyond what composition, staffing and missing close records explain?
- Success criteria: answered means a causal effect is either identified with an interval or established as not identifiable, with a bounded descriptive number.
- Stop condition: conclude after tests T1-T5 or when no available test could change the recommendation.
- Effort budget: 15 queries.

## Hypotheses
| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | causal | Assist shortened time to close | Within matched severity strata, assist median ttc < manual | no within-stratum drop | Within-stratum assist ttc not lower in the majority of strata | T1 | incidents, activity |
| H2 | descriptive (estimand: severity/channel mix by week) | Headline drop is composition: assist week had a lighter severity mix | Severity-standardized median difference much smaller than raw | standardized ~ raw | Mix differs between weeks | T2 | incidents |
| H3 | data-artifact | Missing close records (11 incidents, concentrated in assist, sev1) bias the assist-week closed-only median downward | Incidents without activity are concentrated in assist and in hard (sev1) cases; bounding them as slow widens/erases the gap | missingness balanced | Missing rate differs by workflow | T3 | incidents, activity |
| H4 | causal | Concurrent staffing increase (12->14, 11->13 responders) rather than Assist | Staffing step coincident with cutover | no step | Staffing changed at cutover | T4 | staffing |
| H5 | causal | Assist adds work on hard incidents (responder claim) | Within sev1/high-handoff, assist minutes/handoffs/reopens >= manual | lower or equal | Assist minutes in sev1 not lower than manual | T5 | activity |

## Sources
| id | Origin | Acquired | Coverage notes |
| --- | --- | --- | --- |
| S1 | incidents.csv (420 rows) | local frozen export | 210 manual / 210 assist, 15/day/group |
| S2 | activity.csv (409 rows) | extract 2026-06-22 23:59Z | 11 incidents have no row |
| S3 | staffing.csv (28 rows) | daily snapshot | complete 14 days x 2 groups |

## Data Validity
- Collection method: exports; workflow field = workflow active at open.
- Coverage matrix: (week x workflow x group x has-activity) manual identity 104/1 missing, storage 105/0; assist identity 98/7, storage 102/3. Severity x week x has-activity computed in T3.
- Field population: activity fields populated in all 409 rows.
- Coverage baseline: incidents_opened in staffing (15/day/group) reconciles to incidents.csv 420.
- Known instrument failures: none documented.
- Source completeness semantics: S2: UNKNOWN — no export contract or sentinel; absent row could mean still open at extract, unrecorded, or export incomplete, and the missingness pattern cannot discriminate these.
- Sensitivity checks performed: bootstrap 95% intervals on contrast (below).

## Tests
| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T1 | H1 | within-severity assist ttc lower | stratified medians + bootstrap CI of contrast, 95% | CONTRADICTED | Assist minus manual median ttc (h) [95% CI]: sev1 +9.3 [7.7,12.0] (n 28/9); sev2 +3.8 [3.0,4.3]; sev3 +2.25 [1.9,2.5]; raw -1.8 [-2.2,+1.7]. Severity may be downstream of Assist so this does not identify the effect; confound check = severity stratification, reversal found |
| T2 | H2 | mix differs, standardized diff < raw | chi-sq/ counts; direct standardization | CONSISTENT | sev1 28->14, sev2 84->42, sev3 98->154 at constant 15 incidents/day/group; sev1 exactly 4/day -> 2/day from Jun 8. Standardized mean ttc 6.06h manual vs 9.52h assist; minutes 77 vs 112 |
| T3 | H3 | missing concentrated in assist/sev1; bounds | counts; worst-case bounds | CONSISTENT | missing 1/210 manual vs 10/210 assist; assist sev1 5/14 missing. Imputing missing as slowest leaves assist raw median 5.5h vs 7.27h, so headline median is robust to it but sev1 stratum is not estimable |
| T4 | H4 | staffing step at Jun 8 | staffing means pre/post | CONSISTENT | active responders 12->14 identity, 11->13 storage (+2) on Jun 8; scheduled hours ~94->114 and ~87->104; interruption minutes also rose |
| T5 | H5 | sev1 assist minutes not lower | sev1 comparison | CONSISTENT | sev1 median responder minutes +69 [55,89] and ttc +9.3h vs manual; sev2 +40, sev3 +26 min; n=9 assist sev1 closed, 5 unclosed |

## Amendments
- 2026-06-22 (none): no amendments.

## Conclusion
- Answer: The data does not show Assist caused faster recovery, and no responder-hours can be credibly booked. The headline median drop (-1.8h, CI -2.2 to +1.7, includes 0) is not distinguishable from zero; mean ttc (7.1h to 7.5h) and mean responder minutes (90.2 to 90.9) did not fall. Within every severity stratum, Assist incidents closed slower and took more responder minutes. The raw median fell because the severity mix shifted toward sev3.
- Best supported: H2 composition/mix shift (descriptive) together with H4 staffing co-change as rivals to any Assist effect; H5 (extra work on hard incidents) is consistent in the data.
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | causal | UNRESOLVED | Within-stratum contrast points to slower, but design (no holdout, concurrent staffing +2, severity mix change possibly downstream of Assist) does not identify; no refutation from unidentified contrast |
  | H2 | descriptive (estimand: severity mix by week) | UNRESOLVED | Best supported as explanation of the headline; sev1 halved at exactly the cutover |
  | H3 | data-artifact | UNRESOLVED | Missing close records concentrated in assist (10 of 11) and sev1; completeness UNKNOWN |
  | H4 | causal | UNRESOLVED | Staffing step coincident with cutover; effect on ttc not separable |
  | H5 | causal | UNRESOLVED | Consistent with responders' claim, same identification limit as H1 |

- Limitations: single cutover, no holdout, one week each side; week-of-June-8 events confounded; severity is possibly assigned after Assist touches the incident, so stratifying on it may mis-state the effect and the sev1 halving itself is unexplained (reclassification versus real change); 11 incidents without close records with unknown meaning; 9 sev1 closed assist incidents; no cost/quality data beyond reopen counts. Continuation: causal-identification-review for a staggered or holdout design; decision-analysis for the expansion choice under uncertainty.
