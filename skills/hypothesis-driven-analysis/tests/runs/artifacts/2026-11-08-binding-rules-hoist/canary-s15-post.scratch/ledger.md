# Investigation: Did Assist cause faster recovery / how many responder-hours attributable / expand?

## Problem
- Decision informed: expand Assist company-wide; whether Finance books responder-hour savings.
- Falsifiable question: among the 420 incidents opened 2026-06-01..06-14 (identity, storage), did opening under Assist (from 06-08 00:00Z) cause lower time-to-close (hours from opened_at to closed_at) and lower responder_minutes per incident?
- Success criteria: answered means each live explanation of the headline drop has a tested necessary prediction, and the report states whether a causal number is available or not.
- Stop condition: conclude when the tests below are run; stop with limits if no design identifies the effect (assignment = single cutover, no holdout, concurrent changes).
- Effort budget: 15 tool calls.
- Assignment assumption (stated, not asked: non-interactive): all pilot incidents switched at one instant, both groups together; nothing identifies the effect.

## Hypotheses
| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
|---|---|---|---|---|---|---|---|
| H1 | causal | Assist caused shorter time to close and fewer responder minutes within comparable incidents | within severity strata, Assist closes faster | no within-stratum drop | within-severity (and within-group) median close time is lower under Assist | T1 | S1,S2 |
| H2 | descriptive (estimand: change in closed-incident median time-to-close, Assist week minus manual week, that is due to severity mix: standardized-to-manual-mix median/mean minus raw) | The headline drop is a composition shift: more sev3 under Assist week | severity share of sev3 higher in Assist week; reweighting to manual mix shrinks the drop | mix equal | sev3 share must be higher in Assist week | T2 | S1,S2 |
| H3 | data-artifact | Closed-only median is biased by missing activity rows (open/unrecorded), concentrated in Assist, likely hard incidents | activity-missing rate differs by workflow and skews to high severity | missing balanced | missing rate must differ by workflow (Assist > manual) | T3 | S1,S2 |
| H4 | causal | Concurrent staffing/capacity change (responders 12/11 -> 14/13, scheduled hours up) explains speed-up | staffing step at 06-08 coincides; close time falls with hours per incident | staffing flat | staffing must step up at 06-08 | T4 | S3 |
| H5 | causal | Assist adds work on genuinely hard (sev1/sev2) incidents (handoffs, minutes, reopens) | within sev1/2 Assist has higher minutes/handoffs/reopen | no | Assist responder_minutes or handoffs on sev1 not lower | T5 | S1,S2 |
Orientation findings (not amendments): 11/420 incidents lack activity rows (10 Assist incl. 5 of 14 sev1; 1 manual); staffing step at 06-08 visible in coverage inspection; incident counts per group-day are a constant 15.

## Sources
| id | Origin | Acquired | Coverage |
|---|---|---|---|
| S1 | incidents.csv (420 rows, unique ids) | local frozen export, extract 06-22 23:59Z | 15/group/day all 28 cells, no nulls |
| S2 | activity.csv (409 rows, unique, all ids in S1) | same | 11 incidents absent, see below |
| S3 | staffing.csv (28 rows) | same | complete group x day |

## Data Validity
- Collection method: local frozen exports; generation process not documented.
- Coverage matrix: incident counts 15 in every date x group cell (workflow flips at 06-08 for both). Activity missing by date x group: 06-05 id1, 06-08 id1/storage2, 06-10..13 identity 1 each, 06-14 identity2/storage1; by workflow manual 1, assist 10; by severity assist sev1 5, sev2 2, sev3 3; manual sev3 1.
- Field population: all fields 100% populated in the rows present.
- Coverage baseline: staffing.incidents_opened = 15 matches S1 (independent denominator for opened). No independent denominator for closures.
- Known instrument failures: none documented. Dashboard median presumably over rows with closed_at.
- Source completeness semantics: S2: UNKNOWN — absent activity row could be still-open, unrecorded closure, or export gap; its own missingness pattern cannot discriminate and 7-day maturity addresses timing not completeness. Closed-incident statistics are selection-sensitive, direction unknown.
- Sensitivity checks performed: bootstrap 95% CI around contrasts (committed 95% before reading); bounding for missing.

## Tests
| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
|---|---|---|---|---|---|
| T1 | H1 | Assist median close time lower within each severity | stratified medians + bootstrap CI of contrast | CONTRADICTED | S1,S2 (an.py): Assist slower in every stratum: sev1 +9.3h [7.8,11.8], sev2 +3.8h [3.0,4.3], sev3 +2.25h [1.9,2.5]; same sign in both groups. Contrast is from an unidentified design, so this leaves H1 UNRESOLVED, not refuted. Confound/aggregation reversal check: pooled median -1.83h reverses to positive in all strata (Simpson) |
| T2 | H2 | sev3 share higher in Assist; standardizing shrinks drop | mix + direct standardization | CONSISTENT | sev3 share 46.7% -> 73.3%, sev1 13.3%->6.7%, sev2 40%->20% (S1). Standardized to manual mix: mean ttc 7.14 vs 11.03h, median 7.27 vs 10.7h; raw mean ttc 7.14 vs 7.53. Caveat: severity may itself be downstream of Assist (reclassification); not testable here |
| T3 | H3 | missing rate higher in Assist, skewed severe | counts, Fisher-type test, bounds | CONSISTENT | missing 10/210 Assist vs 1/210 manual, permutation p=0.006; 5 of 14 Assist sev1 missing. If missing are still-open, Assist mean ttc 20.3 vs 9.1h (CI [2.4,20.4]); median unaffected (5.5 vs 7.27). Direction under UNKNOWN semantics not asserted |
| T4 | H4 | staffing steps up at 06-08 | before/after staffing means | CONSISTENT | active responders 12->14 identity, 11->13 storage; scheduled hours 96->114, 87->104; interruption minutes 12->74, 29->59 (S3). Concurrent change that cannot be separated from Assist; its effect on speed is not estimable |
| T5 | H5 | sev1/sev2 Assist responder_minutes/handoffs not lower | stratified means + CI | CONSISTENT | sev1/2 pooled: minutes +35 [14,58], ttc +4.3h [2.5,6.3], reopen 18% vs 0% [8,31]pp. sev1 reopen 9/9 vs 0/28; sev1 handoffs 0.4 vs 5.9 (possible recording change). Necessary prediction (minutes not lower) held; sev3 minutes +26 [25,28] as well |

## Amendments
- 2026-11-08: no amendments; analysis executed per plan (an.py, seed 1, 2000 bootstrap draws, 95% CI committed before reading).

## Conclusion
- Answer: the data does not support that Assist caused faster recovery. The headline median drop is a mix shift (sev3 share 47%->73%) plus censoring of unclosed incidents; within every severity Assist incidents closed slower and used more responder minutes. No responder-hour saving is attributable; the point estimate of the associated change is an increase.
- Best supported: H2 (composition) and H3 (missing activity concentrated in Assist) explain the headline; H4 is a live concurrent change. Association only.
- Per-hypothesis summary:

  | id | claim | status | basis |
  |---|---|---|---|
  | H1 | causal | UNRESOLVED | T1 contradicted in every stratum, but single-cutover contrast with concurrent staffing change does not identify the effect, so it cannot refute; no evidence of a speed-up |
  | H2 | descriptive | UNRESOLVED | best supported for the headline drop (T2 CONSISTENT) |
  | H3 | data-artifact | UNRESOLVED | T3 CONSISTENT; mechanism (still open vs unrecorded) UNKNOWN |
  | H4 | causal | UNRESOLVED | T4 CONSISTENT that staffing stepped up; effect on speed untestable |
  | H5 | causal | UNRESOLVED | T5 CONSISTENT, extra work in all strata; not identified as causal |
- Limitations: no holdout, one cutover, staffing/interruptions changed same day, severity could be downstream of Assist, activity-missing semantics UNKNOWN, handoff/reopen fields look recorded differently for sev1, one week per arm, two groups. Continuation: causal-identification-review (design) and decision-analysis (expand/hold under uncertainty) if installed.
