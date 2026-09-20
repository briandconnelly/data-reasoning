# Investigation: Did Assist cause faster recovery, and how many responder-hours can be credibly attributed to it? (identity + storage, incidents opened 2026-06-01..06-14)

Route: full. Assignment was a single cutover at 2026-06-08T00:00Z, no holdout, one week before/after -> nothing identifies the effect; every co-occurring change is a live rival.
Assumption named: no randomization or independent assignment. "Every incident followed the workflow active when it opened" makes exposure well-defined; it does not make the week-over-week comparison a counterfactual.
Headless: consultation gate skipped; assumptions stated here.

## Problem
- Decision informed: expand Assist company-wide; whether Finance books responder-hour savings in the rollout plan.
- Falsifiable question: for incidents opened in the two pilot groups, is the fall in time to close (opened_at -> closed_at, hours) and responder_minutes in the Assist week attributable to Assist, and how much?
- Success criteria: answered = (a) we say whether the data identifies an Assist effect, (b) we give a credible attributable range for responder-hours (or say none), (c) each rival below has a recorded outcome.
- Stop condition: conclude when every hypothesis has a recorded outcome and no available test in these three files could reverse the answer; else stop with limits.
- Effort budget: 25 script runs.
- Practical threshold: a >=10% reduction in median TTC or mean responder minutes within severity that survives worst-case handling of missing records, in the credible interval, would support expansion on efficacy; the saving is bookable only if its lower bound is > 0.

## Hypotheses
| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | causal | Assist caused the fall in time to close (and responder minutes) | Assist-week TTC lower within each severity, on comparably closed incidents; reopens not higher | within-severity TTC flat/higher | within-severity Assist-week median TTC must not be higher than manual-week in sev3 (bulk of volume) | T1 | incidents, activity |
| H2 | data-artifact | 11 incidents (10 assist) have no activity row; if they are still-open/unrecorded hard incidents, closed-only comparisons flatter Assist | missing rows concentrate in Assist and in sev1; bounding them (as open >= extract age) moves the Assist median/mean materially | missing rows spread evenly across weeks/severity; bounds do not move the estimate | the missing-record share must differ between Assist and manual weeks | T2 | incidents joined to activity |
| H3 | descriptive (estimand: overall median TTC and mean responder minutes, Assist week minus manual week, direct-standardized to the pooled severity mix) | The headline drop is largely a shift in severity mix (Assist week has far fewer sev1, more sev3) rather than faster handling | raw drop shrinks materially after severity standardization | standardized drop ~ raw drop | the standardized difference must be smaller in magnitude than the raw difference | T3 | severity, ttc, rm |
| H4 | causal | The concurrent capacity step at cutover (+2 active responders per group, ~+20% scheduled hours, same 15 incidents/day) explains the fall, not Assist | staffing rises exactly at 06-08 and per-responder load falls; TTC in queue-sensitive sev3 falls | staffing flat across cutover | active_responders/scheduled hours must rise at the cutover (deterministic from staffing.csv); discrimination from Assist needs within-week variation | T4 | staffing |
| H5 | causal | Assist adds work on genuinely hard incidents (responders' claim) | sev1 / top-decile incidents show higher responder minutes/handoffs/TTC under Assist | not higher | sev1 (closed and bounded) responder minutes under Assist must not be lower than manual | T5 | incidents, activity |

Other fields are consistency checks (reopened_within_72h, handoffs, interruption_minutes), not separate hypotheses.
Orientation findings recorded so far (before any workflow-outcome contrast was read): severity mix and missing-record counts by workflow x severity; staffing step.

## Sources
| id | Origin | Acquired | Coverage notes |
| --- | --- | --- | --- |
| S1 | incidents.csv (420 rows, 06-01..06-14, 2 groups) | frozen export, extract 2026-06-22T23:59Z | all ids unique; workflow perfectly aligned with opened_at >= 06-08 |
| S2 | activity.csv (409 rows) | same | 11 incidents from S1 have no row: 1 manual (identity sev3), 10 assist (7 identity, 3 storage; 5 sev1, 2 sev2, 3 sev3) |
| S3 | staffing.csv (28 rows, daily x group) | same | complete 14 days x 2 groups; incidents_opened = 15/day/group throughout |

## Data Validity
- Collection method: unknown beyond file names; activity = "recorded resolution activity as of the extract".
- Coverage matrix: incidents by workflow x severity x service_group (orientation, above): S1 Assist sev1 14 vs manual 28; missing activity 5/14 Assist sev1, 2/42 sev2, 3/154 sev3; manual 0/28, 0/84, 1/98. To be completed by day in ledger appendix.
- Field population: closed_at, responder_minutes, handoffs, reopened populated 100% on rows present (checked).
- Coverage baseline: staffing.incidents_opened = 15/day/group -> 420 total = S1 rows, so S1 is complete versus S3. No independent denominator for S2.
- Known instrument failures: none stated. Dashboard "median time to close" definition unknown; likely computed over closed incidents only.
- Source completeness semantics:
S2: UNKNOWN — a missing activity row could mean still open at extract, activity unrecorded, or export incomplete; nothing in the files separates these, and its own missingness pattern (concentrated in Assist sev1) cannot. The 7-day maturity argument addresses timing only. Any quantity computed on S2-present rows is selection-sensitive, direction unknown; bounds computed as sensitivity only.
S1: complete against S3 daily incidents_opened.
S3: no absent-record issue bearing on conclusions.
- Sensitivity checks performed: see Tests (bootstrap CI for contrasts, 95% committed; incident resample; bounds for missing rows).

## Tests
| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T1 | H1 | Assist-week median TTC not higher than manual-week within sev3 and within each severity; reported with 95% bootstrap CI on the contrast | stratified medians, incident bootstrap 5000 | NOT_TESTED | |
| T2 | H2 | missing share differs by workflow; worst-case bound (missing = open, TTC >= extract age) shifts Assist median/mean | counts + Fisher-type exact/permutation, bounds | NOT_TESTED | |
| T3 | H3 | severity-standardized difference smaller than raw | direct standardization, bootstrap CI | NOT_TESTED | |
| T4 | H4 | staffing step at 06-08; within-period daily TTC vs staffing/interruption | staffing table; daily correlation (weak by construction) | NOT_TESTED | |
| T5 | H5 | sev1 and long-tail responder minutes/handoffs not lower under Assist | sev1 contrast, bounds for missing, top-decile share | NOT_TESTED | |

## Amendments
(none)

## Conclusion
(pending)
