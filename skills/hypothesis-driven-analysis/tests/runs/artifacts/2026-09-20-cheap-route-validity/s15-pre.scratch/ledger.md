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
Scripts: load.py, a1.py (strata + bootstrap), a2.py (missingness, bounds), a3.py (standardization, hours, staffing). 95% intervals committed in advance; incident-level bootstrap (stratified for standardization).

| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T1 | H1 | within-severity Assist-week median TTC not higher than manual-week (sev3 and each severity) | stratified median contrast, bootstrap | CONTRADICTED (contrast does not identify a causal effect, so it cannot refute H1 by itself) | sev3 median 2.78h->5.03h (diff CI +1.93..+2.50); sev2 8.54->12.33 (+3.0..+4.3); sev1 18.33->27.65 (+7.7..+12.0). Pooled closed-only median 7.27->5.44 (diff CI -2.2..+1.7, includes 0); pooled mean 7.14->7.53 (CI -0.6..+1.4). Confound/reversal check: aggregation reversal (Simpson) between pooled and within-severity (S1,S2). Reopen within 72h: 0/209 manual vs 9/200 Assist, all 9 in sev1 (9 of 9 closed Assist sev1). |
| T2 | H2 | missing-record share differs by workflow; bounds shift Assist mean | exact hypergeometric; fill missing with TTC = age at extract (lower bound on true) | CONSISTENT | 10 of 11 missing rows are Assist (p=0.005); Assist sev1 5/14 missing vs 0/28 manual (p=0.002); all missing incidents were >=205h old at extract, so "not yet matured" is not the reading. Filling: Assist mean TTC 7.5h -> >=20.3h; manual 7.1 -> 9.1; median barely moves (5.44->5.50), so the headline median is insensitive to it, means/sev1 are not. Completeness semantics remain UNKNOWN. |
| T3 | H3 | severity-standardized difference smaller than raw | direct standardization to pooled mix 10/30/60 (sev1/2/3), stratified bootstrap | CONSISTENT (see amendment on wording) | mix: manual 13/40/47% sev1/2/3, Assist 7/20/73%. TTC median: raw -1.83h, standardized +3.42h (CI +3.09..+3.71); TTC mean raw +0.39, std +3.46 (CI +3.27..+3.67); responder-min mean raw +0.65, std +34.4 (CI +32.5..+36.1). Mix step is on 06-08: sev3 per day 14 -> 21-22. |
| T4 | H4 | staffing step at 06-08; within-period TTC tracks staffing/interruption | staffing table; daily residual-TTC vs interruption_minutes corr | NON_DISCRIMINATING | active responders 12->14 identity, 11->13 storage; scheduled hours 1282->1524 (+19%); mean interruption min/day identity 12->74, storage 29->59. Step is perfectly collinear with cutover; within-week corr -0.10 (n=28), no power to separate. Detection limit: a single step cannot be split from Assist. Assist is not faster within severity, so capacity is not needed to explain a speed-up that did not occur; it does mean the Assist week used more staff. |
| T5 | H5 | sev1 responder minutes/TTC not lower under Assist | sev1 contrast, missing rows as bound | CONSISTENT | sev1 (closed): responder minutes 242->311 median (CI +55..+89), mean +72 (CI +61..+82); TTC +10h; handoffs 6->0 (recording change or practice change unknown). 5 of 14 Assist sev1 have no activity row; if still open they make this worse, so the missing rows cannot rescue Assist. Associative only; severity itself may be assigned differently under Assist. |

## Amendments
- Post-hoc note on T3: the preregistered wording ("smaller in magnitude") did not anticipate a sign reversal; the standardized difference (+3.4h) is larger in magnitude than the raw (-1.8h). The intended claim (the headline drop is a mix effect) is what the test evaluated: the drop disappears and reverses. Recorded CONSISTENT with this caveat rather than CONTRADICTED; H3 is descriptive and cannot be REFUTED by this either way.

## Conclusion
- Answer: The data do not show that Assist caused faster recovery, and they support no bookable responder-hour saving. The dashboard drop in median time to close (7.3h -> 5.4h among closed incidents) comes from the mix: the Assist week has half as many sev1 and 1.5x as many sev3 incidents. Within every severity, Assist-week incidents closed slower (sev3 +2.2h, sev2 +3.8h, sev1 +9.3h) and used more responder minutes. Pooled mean time to close and mean responder minutes are flat (7.1 vs 7.5h; 90 vs 91 min). Nothing identifies a causal effect (single cutover, no holdout, staffing raised +2 per group at the same moment, severity mix moved at the same moment, and 10 of the 11 incidents lacking activity rows are Assist ones).
- Best supported: H3 (mix shift explains the headline; T3) and H5 as an association (hard incidents are slower and more expensive under Assist; T5). H2 makes Assist look better than it should on means, not on the median.
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | causal | UNRESOLVED | T1 contradicts the predicted direction within every severity, but a before/after contrast without a comparison group cannot refute a causal hypothesis; nothing supports it either |
  | H2 | data-artifact | UNRESOLVED | T2 CONSISTENT: missing rows concentrate in Assist and in sev1; source semantics UNKNOWN |
  | H3 | descriptive | UNRESOLVED | best supported for the headline (T3): drop reverses after severity standardization; assumes severity is not itself changed by Assist |
  | H4 | causal | UNRESOLVED | T4 NON_DISCRIMINATING: staffing step collinear with cutover |
  | H5 | causal | UNRESOLVED | best supported as an association (T5 CONSISTENT); not identified |
- Limitations: no comparison group, one week each side; severity may be downstream of Assist (the step in mix at cutover is compatible with re-triage as well as a real change in incident mix; direction of the bias in the stratified comparison is unknown); activity rows missing for 11 incidents (UNKNOWN semantics; estimates on present rows are selection-sensitive, direction unknown, though every plausible reading makes Assist no better); handoffs recording may differ by workflow; responder_minutes definition unverified; no cost data for the extra staffing; two groups only; identity and storage are pooled, but severity-level mean TTC runs the same direction in both groups (checked).
