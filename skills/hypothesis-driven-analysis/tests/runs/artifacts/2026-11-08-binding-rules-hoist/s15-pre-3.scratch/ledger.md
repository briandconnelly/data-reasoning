# Investigation: Did Assist (cutover 2026-06-08 00:00Z, no holdout) cause faster recovery; credible responder-hours?

## Problem
- Decision informed: expand Assist company-wide; book responder-hour savings.
- Falsifiable question: for pilot incidents opened Jun 1-14, did Assist reduce time-to-close / responder minutes?
- Success criteria: answered = effect attributable or declared not identifiable, with what is estimable.
- Stop condition: conclude after tests T1-T5 or when nothing further can change the answer.
- Effort budget: 25 tool calls.
Route: full (before/after, single cutover, no comparison group; unidentified assignment). Assumption named: nothing identifies the effect.

## Hypotheses
| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | causal | Assist shortened time to close | Post-week close times lower within comparable strata (severity, channel, group) | no within-stratum drop | Within-stratum median close time is lower post | T1 | incidents, activity |
| H2 | data-artifact | Closure records missing for non-random incidents (409 of 420 in activity), biasing post-week medians | Missing rate differs by workflow/severity | equal | Unrecorded closures concentrated in the post period or hard cases | T2 | incidents, activity |
| H3 | descriptive (estimand: severity/channel mix by workflow) | Case mix shifted between weeks | Mix differs pre vs post | same mix | Severity/channel distribution differs between weeks | T3 | incidents |
| H4 | causal | Concurrent staffing increase (12->14, 11->13 responders at cutover) explains speedup | Post-week staffing higher; close time falls with capacity | no staffing change | Staffing rose at cutover | T4 | staffing |
| H5 | causal | Assist adds work on hard incidents (heterogeneity: sev1 or handoffs/reopens worse) | Hard-incident minutes/handoffs/reopens higher post | no | Sev1/sev2 responder minutes or reopen/handoffs not lower post | T5 | incidents, activity |

## Sources
| id | Origin | Acquired | Coverage notes |
| S1 | incidents.csv | frozen, extract 2026-06-22 23:59Z | 420 rows |
| S2 | activity.csv | same | 409 rows |
| S3 | staffing.csv | same | 28 rows (2 groups x 14 days) |

## Data Validity
- Collection method: frozen CSV exports; incidents = all opened Jun 1-14, activity = recorded closures at 2026-06-22 23:59Z, staffing = daily snapshot.
- Coverage matrix: incidents 105/group/week (210 pre, 210 post, matches staffing 15/day/group); closures missing pre 1/210, post 10/210 (sev1 post 5/14, sev2 2/42, sev3 3/154; identity 7, storage 3).
- Field population: closed_at/minutes/handoffs/reopen present for 409/420; other fields complete.
- Source completeness semantics:
  S2: UNKNOWN — missing rows could be unclosed, unrecorded or unexported; nothing in the files discriminates them.
- Coverage baseline: staffing incidents_opened (15/day/group) is independent denominator for S1.

## Tests

| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T1 | H1 | within-stratum medians lower post | stratified medians, bootstrap 95% CI on contrast | CONTRADICTED (adequacy: 0 ± 0 (variants: all strata); deterministic direction, sev1/2/3 post slower by +9.3/+3.8/+2.3h, CIs exclude 0) | S1,S2 a.py |
| T2 | H2 | missingness differs by workflow | crossed table | CONSISTENT (pre 1/210 missing, post 10/210; sev1 post 5/14) | S1,S2 |
| T3 | H3 | mix differs | crosstab | CONSISTENT (sev3 47%->73%, sev1 13%->7%) | S1 |
| T4 | H4 | staffing rose | staffing means | CONSISTENT (12->14, 11->13 responders; sched hrs ~94->113) | S3 |
| T5 | H5 | hard incidents worse post | by severity minutes/handoffs/reopen | CONSISTENT (sev1 min 242->311, reopen 0->1 of 9) | S1,S2 |

## Amendments
(none)

## Conclusion
- Answer: Headline median drop (7.27h->5.44h) is a composition artifact (Simpson's paradox); within every severity stratum Assist-week incidents closed slower and used more responder minutes. Mean close time and mean minutes are flat (7.1 vs 7.5h; 90 vs 91 min). No savings are attributable; standardized to pre-week mix, post is ~+3.8h and ~+37 min slower per incident (associative only). Causation not identified either way; evidence does not support expansion or booking savings.
- Best supported: composition shift (H3) explains the headline; H5 and H4 are live, unidentified contributors; no benefit of Assist is supported.
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | causal | REFUTED | necessary prediction (within-stratum faster) failed in all strata; refutation rests on stratified contrast, caveat: staffing co-change could mask a benefit, so Assist-harm itself is unresolved |
  | H2 | data-artifact | UNRESOLVED | 10 post vs 1 pre missing closures, 5 of 14 post sev1; semantics UNKNOWN, direction unknown |
  | H3 | descriptive | UNRESOLVED | mix shift to sev3 fully explains the headline; mix cause unknown |
  | H4 | causal | UNRESOLVED | staffing up ~2 responders concurrent; not separable from Assist |
  | H5 | causal | UNRESOLVED | hard incidents worse post, consistent with responders' claim; not identified |
- Limitations: no comparison group; staffing, interruptions and mix changed at cutover; mix shift itself may be downstream of Assist (triage/severity reclassification), so standardizing assumes it is not; S2 completeness UNKNOWN; sev1 post n=9 closed.
