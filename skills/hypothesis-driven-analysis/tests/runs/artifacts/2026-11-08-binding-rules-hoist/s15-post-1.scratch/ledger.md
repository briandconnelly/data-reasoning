# Investigation: Did Assist (cutover 2026-06-08 00:00Z, both groups, no holdout) cause faster recovery, and how many responder-hours are attributable?

## Problem
- Decision informed: expand Assist company-wide; whether Finance books responder-hour savings.
- Falsifiable question: among incidents opened 06-01..06-14 in identity+storage, is Assist associated with / does it cause lower time-to-close (hours) and responder minutes per incident?
- Success criteria: answered means each rival below is tested, and either an identified effect with interval exists or the data is stated not to identify one.
- Stop condition: conclude when no unresolved rival could reverse the recommendation; otherwise stop with limits.
- Effort budget: 25 tool calls.
- Route: full (assignment = single cutover, no holdout; co-occurring changes are live rivals). Assignment assumption: nothing identifies the effect.

## Hypotheses
| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
|---|---|---|---|---|---|---|---|
| H1 | causal | Assist caused faster close | within severity strata, assist TTC lower; extra incl. censored incidents | no within-stratum drop | within-severity TTC median must be lower under assist (sign-test/bootstrap interval for contrast excludes 0 in drop direction) | T1 | incidents+activity |
| H2 | descriptive (estimand: share of sev1/sev2 among incidents, assist week minus manual week) | Composition shift: easier mix in assist week explains headline drop | sev mix shifts toward sev3; standardizing to fixed mix shrinks the drop | mix equal | severity share of sev3 must differ between weeks | T2 | incidents |
| H3 | data-artifact | 11 incidents lack activity rows (10 assist, skewed hard); closed-only medians are survivor-biased | missing rows concentrated in assist/high severity; bounding with imputed worst-case reverses/shrinks drop | missing balanced | missing rate must differ by workflow | T3 | both |
| H4 | causal | Concurrent staffing increase (12→14, 11→13 responders at cutover) explains faster close / changes minutes | staffing step coincides with cutover; scheduled hours per incident up ~20% | staffing flat | active_responders must step up at 06-08 | T4 | staffing |
| H5 | descriptive (estimand: responder minutes, handoffs, reopen rate per incident, assist minus manual, severity-stratified) | Assist adds work on hard incidents (responder claim) | sev1/sev2 minutes/handoffs/reopens higher under assist | not higher | sev1 mean responder minutes must be higher under assist | T5 | activity |

## Sources
| S1 | incidents.csv, 420 rows, opened 06-01..06-14 | local frozen export | all days both groups present; workflow = f(opened_at >= 06-08) exactly |
| S2 | activity.csv, 409 rows | extract 06-22 23:59Z | 11 incidents lack rows (10 assist, 1 manual) |
| S3 | staffing.csv, 28 rows | daily snapshot | 14 days x 2 groups complete |

## Data Validity
- Collection: exports; no contract for activity.csv completeness.
- Coverage: workflow x group x severity counts and missing counts seen in orientation (assist: 14 sev1, 42 sev2, 154 sev3; manual: 28/84/98; missing rows assist sev1 5/14).
- Source completeness semantics: S2: UNKNOWN — an absent activity row could be still-open, unrecorded, or export-incomplete; nothing in the data separates these (7+ days maturity addresses timing only).
- Sensitivity: bounds under alternative missing-row treatments (T3).

## Tests
| T1 | H1 | within-severity TTC lower under assist | stratified medians, bootstrap CI on contrast | CONTRADICTED | assist slower in every stratum: sev1 +9.3h (CI 7.7..11.9), sev2 +3.8h (3.0..4.3), sev3 +2.3h (1.9..2.5); adequacy: deterministic sign, intervals exclude drop (variants: any severity-stratified effect); caveat: severity may be post-exposure, so H1 stays UNRESOLVED (unidentified contrast) |
| T2 | H2 | sev3 share differs; standardized contrast | direct standardization | CONSISTENT | sev3 share 46.7%→73.3%; sev1/2 counts exactly halved; pooled median -1.8h (CI -2.2..+1.7 includes 0); standardized to manual mix assist +3.9h slower |
| T3 | H3 | bounds | worst/best-case for missing | CONSISTENT | 10/11 missing rows assist, 5/14 assist sev1 missing; filling changes within-stratum conclusion not at all (assist still slower); but completeness UNKNOWN |
| T4 | H4 | staffing step at 06-08 | daily table | CONSISTENT | responders 11.5→13.5, scheduled hrs/day 91.6→108.9, interruptions 20.7→66.7 min/day; coincident with cutover, confounded |
| T5 | H5 | sev1/2 minutes higher under assist | stratified means/medians, handoffs, reopen | CONSISTENT | sev1 minutes 242→311 (CI +55..+89), sev2 99.5→139.5, sev3 39→65; sev1 reopens 0/28 → 9/9 observed; handoffs lower in sev1 (6→0) |

## Amendments
(none)

## Conclusion
- Answer: No evidence Assist sped recovery; headline median drop is a severity-mix artifact. Attributable hours: none credible (point ~0).
- Per-hypothesis summary:

  | id | claim | status | basis |
  |---|---|---|---|
  | H1 | causal | UNRESOLVED | T1 contradicts within strata but severity may be post-exposure; unidentified design |
  | H2 | descriptive | UNRESOLVED | best supported for headline (T2) |
  | H3 | data-artifact | UNRESOLVED | T3; completeness UNKNOWN |
  | H4 | causal | UNRESOLVED | T4 coincident staffing change |
  | H5 | descriptive | UNRESOLVED | T5 consistent |
- Limitations: no holdout; staffing/interruption changes at cutover; S2: UNKNOWN.
