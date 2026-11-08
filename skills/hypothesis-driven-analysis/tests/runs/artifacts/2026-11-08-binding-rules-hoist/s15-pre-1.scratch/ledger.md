# Investigation: Did Assist cause faster recovery, and how many responder-hours can be credibly attributed?

Route: full. Assignment was a single cutover (no holdout); nothing identifies the effect, and several co-occurring changes are live rivals. Assumption named: no randomization, no concurrent control.

## Problem

- Decision informed: book responder-hour savings in the rollout plan and expand Assist company-wide, or not.
- Falsifiable question: among incidents opened 2026-06-01..06-14 in identity and storage, did Assist (on from 06-08 00:00Z) cause lower time-to-close (closed_at - opened_at) and responder_minutes, and how many responder-hours does that credibly imply?
- Success criteria: answered means the headline drop is decomposed into what survives the rivals (staffing, mix, missing closures), with an interval, or it is stated that the data cannot identify the effect.
- Stop condition: conclude when no named unresolved alternative could reverse the booking/expansion recommendation; otherwise stop with limits.
- Effort budget: 15 tool calls.

## Hypotheses

| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | causal | Assist shortened time to close for incidents it handled | Post-cutover TTC lower within severity strata | No within-stratum drop | Within-severity median TTC among closed incidents must not be higher post than pre | T1 | incidents, activity |
| H2 | data-artifact | The headline median is biased by missing closures: unclosed/unexported incidents are concentrated in hard (sev1) Assist-week incidents, so closed-only medians are survivor-selected | Missing-activity rate differs by period and severity; bounding the missing as slow erases the drop | Missing rate is similar and bounds do not move the sign | Missingness rate must differ between periods (or by severity within period) | T2 | incidents, activity |
| H3 | causal | The staffing increase at cutover (+2 responders/group, about +20 scheduled hours/day) explains the speedup | Staffing step coincides exactly with cutover; cannot be separated from Assist | n/a | Staffing must rise at cutover | T3 | staffing |
| H4 | descriptive (estimand: share of sev1+sev2 among opened incidents, post minus pre) | Case mix shifted toward easier incidents | Severity/channel mix is easier post | Mix is stable | Share of sev3 post must exceed pre | T4 | incidents |
| H5 | causal | Assist adds work on hard incidents (responder claim): responder_minutes, handoffs, reopens up for sev1/2 | Higher responder_minutes/handoffs/reopen in sev1-2 post | No increase | Sev1-2 responder_minutes median must not be lower post than pre | T5 | incidents, activity |

## Sources

| id | Origin | Acquired | Coverage notes |
| --- | --- | --- | --- |
| S1 | incidents.csv (420 rows, unique ids) | local frozen export, extract 2026-06-22T23:59Z | every incident opened 06-01..06-14 per user; workflow col equals period perfectly |
| S2 | activity.csv (409 rows, unique ids, no blanks) | same | 11 incidents have no row: 1 pre, 10 post (sev1 7, sev2 2, sev3 3 minus... see T2) |
| S3 | staffing.csv (28 rows, 14 days x 2 groups) | same | complete grid; incidents_opened = 15/day/group constant |

## Data Validity

- Collection method: exports; no field definitions given for activity.csv (meaning of an absent row is not documented).
- Coverage matrix: period x group x severity counts above (orientation); 15 incidents/day/group in staffing matches 210 per week per... 105/week/group x2 = 210/wk, total 420 ok.
- Field population: activity fields 100% populated for rows present.
- Coverage baseline: staffing incidents_opened (independent denominator) reconciles to 420 incidents; says nothing about activity completeness.
- Known instrument failures: none stated.
- Source completeness semantics:
S2: UNKNOWN — absent activity row could mean still open at extract, closure unrecorded, or export incomplete; the file's own missingness pattern cannot discriminate these, and no export contract or sentinel is available.
- Sensitivity checks performed: bootstrap CI for contrasts at 95% (committed before reading); bounding analyses for missing closures.

## Tests

| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T1 | H1 | within-severity median TTC post <= pre | stratified medians, bootstrap 95% CI on contrast | CONTRADICTED | S1,S2: median TTC pre->post sev1 18.3->27.7h (CI +7.7,+11.6), sev2 8.5->12.3h (+3.0,+4.3), sev3 2.8->5.0h (+1.9,+2.5); both groups unchanged in sign. Deterministic sign; closed-only so post understated if missing are slow. Stratifier (severity) may itself be downstream of Assist - see limits. Contradiction of the necessary prediction comes from an unidentified contrast, so H1 stays UNRESOLVED |
| T2 | H2 | missing rate differs by period/severity | counts | CONSISTENT | S1,S2: missing 1/210 pre vs 10/210 post; post sev1 5/14 missing vs pre 0/28. Meaning of absence UNKNOWN. Aggregate with missing censored at extract: -1.77h, headline unchanged, so missingness does not explain the headline; it biases within-sev1 comparison |
| T3 | H3 | staffing steps up at 06-08 | staffing means pre/post | CONSISTENT | S3: active responders 12->14 / 11->13; scheduled hrs/day/group 91.6->108.9 (+19%); interruption min 20.7->66.7. Perfectly collinear with cutover; cannot be separated |
| T4 | H4 | sev3 share post > pre | mix tables | CONSISTENT | S1: sev3 46.7%->73.3%, sev2 40%->20%, sev1 13.3%->6.7% (n=210 each). Within-severity medians all rose (T1), so this composition shift produces the whole headline drop (Simpson reversal). Severity is a pre-treatment field only if assigned at open; if Assist changed triage/labeling it is downstream - cause of the mix shift unattributed |
| T5 | H5 | sev1-2 responder_minutes post > pre | stratified medians, handoffs, reopens | CONSISTENT | S1,S2: median responder min sev1 242->311 (CI +55,+89), sev2 99.5->139.5 (+30,+48), sev3 39->65. Raw mean 90.2 vs 90.9 min (no change); pre-mix-standardized +37 min/incident. Handoffs inconsistent: sev1 5.9->0.4, sev2 3.0->4.0, sev3 0.5->1.5. Reopens 1 total, uninformative. Associative only |

## Amendments

- none

## Conclusion

- Answer: The data does not support the claim that Assist caused faster recovery, and supports booking no responder-hour savings. The headline median drop (7.3h -> 5.4h) is a composition effect: the Assist week had far fewer sev1/sev2 incidents (sev3 47% -> 73%). Within every severity, and in both service groups, time to close and responder minutes are higher in the Assist week. Total responder hours are flat (314 vs 303 h; mean 90.2 vs 90.9 min/incident). Attributable savings: none credible; the standardized point estimate is +130 h/week more work, but is itself not causal.
- Best supported: associative only. H4 (mix shift) accounts for the headline; H3 (staffing +2/group, interruptions tripled) is a perfectly collinear co-change; H5 (extra work on hard incidents) is directionally consistent with responder reports but not identified.
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | causal | UNRESOLVED | T1 contradicts the speedup within strata, but the contrast is unidentified (single cutover, staffing step, possible downstream severity), so it cannot refute; no discriminating evidence supports it |
  | H2 | data-artifact | UNRESOLVED | best supported for a bias in sev1 comparison (T2 CONSISTENT: 5 of 14 Assist sev1 have no closure vs 0 of 28); does not drive the headline |
  | H3 | causal | UNRESOLVED | T3 CONSISTENT that staffing stepped up at cutover; no test separates it from Assist |
  | H4 | descriptive | UNRESOLVED | best supported as the arithmetic source of the headline (T4 CONSISTENT) |
  | H5 | causal | UNRESOLVED | T5 CONSISTENT; direction matches the responders' claim but unidentified |
- Limitations: no holdout, no concurrent control, one week per arm, so Assist is inseparable from the staffing step, interruption change, week-of effects, and any change in how severity/intake is assigned. Why sev1/sev2 volume halved is unattributed (may be real, triage change, or Assist side effect). Missing closures: S2 completeness UNKNOWN, direction of bias on within-stratum medians unknown. Median bootstraps in the pooled comparison are bimodal-mixture and wide. Handoff counts move inconsistently. Continuation: causal-identification-review for a staggered or holdout design, decision-analysis for the rollout decision across the unresolved set (neither confirmed installed).
