# Investigation: Did Assist cause faster recovery, and how many responder-hours are credibly attributable?

Route: full. Assignment was a single cutover (all pilot incidents opened >= 2026-06-08T00:00Z get Assist), no holdout, no randomization: nothing identifies the causal contrast, and >=2 live explanations exist. Assumption named: assignment = calendar time.

## Problem

- Decision informed: expand Assist company-wide; and whether Finance books responder-hour savings in the rollout plan.
- Falsifiable question: for incidents opened 2026-06-01..06-14 in the identity and storage groups, (a) did Assist cause lower time-to-close (closed_at - opened_at, hours) and lower responder_minutes, and (b) how many responder-hours can be credibly attributed.
- Success criteria: answered means each explanation for the headline drop is tested on a preregistered prediction, the attributable-hours figure is either bounded or declared not available, and a recommendation is stated with what the data cannot establish.
- Stop condition: conclude when no unresolved alternative could reverse the recommendation; otherwise stop with limits.
- Effort budget: 25 queries (scripts).

## Orientation findings (pre-registration; schema/coverage only, no cause-outcome contrast inspected)

- incidents 420 rows unique ids, 30/day across 14 days, 105 per workflow x group cell. workflow == (opened_at >= 06-08T00:00Z) for every row: no straddlers, confirms the user's assignment description.
- activity 409 rows, unique, no orphan ids. 11 incidents have no activity row (1 manual, 10 assist; 6 of the 11 sev1, 3 sev2... see below). No null fields inside activity rows.
- Severity mix differs by period (manual sev1/2/3 = 28/84/98; assist = 14/42/154). Composition shift present at the design level.
- staffing.csv: active_responders rose 12->14 (identity) and 11->13 (storage) exactly at 06-08, scheduled_responder_hours ~+20/day per group; interruption_minutes also rose.
- incidents_opened in staffing is a flat 15/group/day.

## Hypotheses

| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | causal | Assist workflow itself shortened time to close | within-severity time to close lower in Assist week | no within-severity difference | within severity strata (sev1, sev2, sev3 separately) median time to close is lower in Assist week for every stratum | T1 | S1,S2 |
| H2 | causal | The added responder capacity that started at the cutover (+2 active responders per group) shortened time to close | capacity step coincides with the cutover date and with the drop | no capacity step at cutover | active_responders rise at the cutover date and not earlier (step must coincide) | T2 | S3 |
| H3 | descriptive (estimand: severity-standardized difference in median time to close, Assist week minus manual week, weights = pooled severity mix) | The headline drop is largely a shift in severity composition (fewer sev1/2 in the Assist week), not a change within severity | marginal drop much larger than standardized drop; sev share of sev1/2 lower in Assist week | standardized drop about equal to marginal | the severity-standardized difference must be smaller in magnitude than the marginal difference | T3 | S1,S2 |
| H4 | data-artifact | The headline median is computed on closed incidents only; 11 incidents (10 Assist) have no closure record, which biases the Assist median | Assist-week median moves materially if absent incidents are treated as closing at the extract time (right-censored at 06-22T23:59Z) | median stable under censoring bound | the Assist-week median time to close under worst-case censoring (absent = still open at extract) must differ from the closed-only median by more than the observed headline gap's uncertainty interval | T4 | S1,S2 |
| H5 | causal | Assist adds work on genuinely difficult (sev1/sev2) incidents: responder minutes and handoffs are higher or not lower under Assist | sev1/2 responder_minutes and handoffs higher (or equal) in Assist week | lower in Assist week | sev1/2 mean responder_minutes in Assist week must be >= manual week (a lower value refutes as the outcome contrast, subject to the identification caveat below) | T5 | S1,S2 |

Notes: an exposure-outcome contrast here comes from an unidentified design and cannot alone mark a causal hypothesis REFUTED (SKILL.md Conclusion); it leaves them UNRESOLVED. T2 and T4 are non-contrast tests.
Secondary (non-necessary, cannot refute anything): reopen rate and handoffs overall; interruption_minutes; daily time series to see whether the drop is a step at 06-08 or pre-existing drift; group-level consistency (identity vs storage).
Primary outcomes: time to close (hours), responder_minutes. Interval method: bootstrap 95% (committed before reading), 5000 resamples, on the contrast itself.

## Sources

| id | Origin (file, query, system) | Acquired | Coverage notes |
| --- | --- | --- | --- |
| S1 | incidents.csv (420 rows; opened 06-01..06-14) | frozen local export | complete by count vs staffing incidents_opened (15/group/day = 420) |
| S2 | activity.csv (409 rows; extract 06-22T23:59Z) | frozen local export | 11 incidents without activity row |
| S3 | staffing.csv (28 rows, daily x group) | frozen local export | complete 14 days x 2 groups |

## Data Validity

- Collection method: incidents and activity are separate exports keyed on incident_id; staffing is a daily operating snapshot. No export contract or documentation of what an absent activity row means is available.
- Coverage matrix: (to be filled at week x group x severity in T-data step).
- Field population: activity fields 100% populated on rows present; row presence is the gap.
- Coverage baseline: incidents.csv row count matches staffing.incidents_opened (30/day; total 420). No independent baseline exists for the activity file.
- Known instrument failures: dashboard median (per the dashboard team) unspecified: unknown whether it includes open incidents.
- Source completeness semantics: S2 (activity.csv): UNKNOWN — the 11 missing rows could be still-open incidents, unrecorded closures, or an incomplete export; the file's own missingness pattern (10 of 11 in Assist week, mostly higher severity) cannot discriminate these readings, and the 7-day maturity note addresses timing, not export completeness.
- Join: incidents (1 row per id) left-joined to activity (1 row per id); expected 1:1 at incident grain; test uniqueness on both sides; reconcile 420 = 409 matched + 11 unmatched.
- Sensitivity checks performed: bootstrap CI on contrast, coverage 95%; bound analysis for the 11.

## Tests

| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T1 | H1 | within each severity stratum Assist-week median time to close is lower; within-stratum contrast intervals computed | stratified medians + bootstrap 95% CI | CONTRADICTED | sev1 +9.3h (CI 7.7..12.0), sev2 +3.8h (3.0..4.3), sev3 +2.3h (1.9..2.5): Assist slower in every stratum (S1,S2; analysis_out.txt). Unidentified contrast, so this cannot refute H1 alone; severity may be downstream of Assist (unverifiable) |
| T2 | H2 | active_responders steps up on 06-08 and not before | inspect S3 | CONSISTENT | 12->14 identity, 11->13 storage on exactly 06-08, flat for 06-01..06-07; scheduled hours ~+17/day/group; interruption minutes 21->67/day (S3, analysis_out.txt). Coincident with cutover: capacity and Assist are not separable |
| T3 | H3 | severity-standardized median diff smaller in magnitude than marginal diff | direct standardization, pooled mix, bootstrap | CONTRADICTED (as worded) | marginal median diff -1.83h; standardized diff +3.42h (CI 3.10..3.73), standardized mean diff +3.46h vs marginal mean +0.39h. Magnitude is larger, not smaller, because the sign reversed: wording error, see Amendment 2. Deterministic-in-sign comparison, interval excludes the marginal value (S1,S2). adequacy: 0 (deterministic prediction under this estimand) (variants: any composition-only mechanism) |
| T4 | H4 | worst-case censoring moves Assist median by more than the CI half-width of the headline contrast | bound analysis with 11 absent incidents | CONTRADICTED | Assist median 5.44 closed-only; 5.50 if absent = still open at extract; 5.375..5.50 across all placements of the 10 absent incidents; headline diff stays -1.77..-1.89 vs -1.83 observed (S1,S2, analysis3_out.txt). Coverage matrix probed. Bounds the median headline only, not the stratified sev1 picture (5 of 14 Assist sev1 have no record) |
| T5 | H5 | sev1/2 mean responder_minutes Assist >= manual; handoffs likewise | contrast + bootstrap CI | CONSISTENT (minutes); handoffs mixed | sev1 +72 min (CI 62..82), sev2 +38 min (34..42), sev3 +26 min (25..28). Handoffs sev1 0.44 vs 5.93 (lower), sev2 3.95 vs 3.01 (higher). All 9 closed Assist sev1 incidents were reopened within 72h vs 0 of 28 manual sev1 (S1,S2) |

## Amendments

- 2026-09-20: orientation note correction: the 11 incidents without activity rows are 1 manual sev3 and 10 Assist (5 sev1, 2 sev2, 3 sev3); the "6 of 11 sev1" wording above was wrong. Counts taken from listing, not a cause-outcome contrast.
- 2026-09-20: T3 wording error acknowledged. The preregistered necessary prediction ("standardized diff smaller in magnitude than marginal") did not anticipate a sign reversal; the standardized effect is larger in magnitude and opposite in sign. The outcome as written is recorded as CONTRADICTED and H3 is reported REFUTED as preregistered; the substantive point (the headline drop is not present within severity) is reported in Conclusion with this caveat, not by editing the prediction.
- 2026-09-20: no new hypotheses added; no additional data requested. Extra descriptive checks (daily series, reopen rate, group split, counterfactual responder-hours) are secondary and cannot refute anything.

## Conclusion

- Answer: the data do not show that Assist caused faster recovery, and no responder-hour saving can be credibly attributed. The dashboard's median drop (7.27h -> 5.44h, -1.83h) is a real descriptive fact, robust to the 11 missing records, but it coincides with (a) a shift toward sev3 incidents (47% -> 73%) and (b) a +2 responder-per-group staffing step at the same instant. Within every severity stratum, Assist-week incidents closed slower and used more responder minutes; overall mean time to close and mean responder minutes are flat (7.14h vs 7.53h; 90.2 vs 90.9 min).
- Best supported: H3 (composition) explains the headline drop; H5 (extra work on hard incidents) is consistent on minutes. H1 stays unresolved with all available evidence pointing against a benefit; H2 cannot be separated from Assist by this design.
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | causal | UNRESOLVED | T1 contradicted at every stratum, but the contrast is unidentified (single cutover, no holdout, staffing step, severity possibly downstream), so it cannot refute; no evidence supports a benefit |
  | H2 | causal | UNRESOLVED | T2 consistent (capacity step exactly at cutover); not separable from Assist, and the outcome moved the opposite way within strata |
  | H3 | descriptive (estimand: severity-standardized difference in median time to close) | REFUTED | necessary prediction refuted as preregistered (magnitude wording, T3) because the standardized effect reversed sign to +3.4h; substantively best supported as the explanation of the headline (drop disappears and reverses within severity). Wording error disclosed in Amendment 2 |
  | H4 | data-artifact | REFUTED | T4: median headline moves at most 0.1h under any placement of the 10 absent Assist incidents; coverage matrix probed. Does not clear the stratified sev1 results, which rest on 9 of 14 Assist sev1 incidents |
  | H5 | causal | UNRESOLVED | T5 consistent on minutes in all strata (+26 to +72 min); unidentified contrast, so it cannot be promoted to a causal effect |

- Limitations: single cutover with no holdout; staffing +2 per group and interruption minutes rose at the same instant; severity is assigned at intake and may itself be affected by Assist (if so, stratified contrasts are biased in an unknown direction, while the unstratified means show no benefit either way); 11 incidents have no activity record and the meaning of absence is UNKNOWN (S2), 5 of 14 Assist sev1 incidents are among them; sev1 Assist n=9 closed, all reopened; one week per arm and two groups; no cost of Assist, no quality outcomes beyond reopen/handoff. Not covered: whether Assist would help under a different design; company-wide generalization beyond two pilot groups.
