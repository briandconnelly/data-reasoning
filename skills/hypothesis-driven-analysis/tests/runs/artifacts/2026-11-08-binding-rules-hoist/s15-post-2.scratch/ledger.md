# Investigation: Did Assist (cutover 2026-06-08 00:00Z, no holdout) cause faster recovery, and how many responder-hours are attributable?

## Problem
- Decision informed: expand Assist company-wide; whether Finance books responder-hour savings.
- Falsifiable question: for incidents opened 06-01..06-14 in identity and storage, did Assist reduce time to close and responder minutes?
- Success criteria: answered means causal attribution is either identified or shown not identifiable, with the credible hour figure (or none) stated.
- Stop condition: conclude when the unresolved rivals cannot be separated by available local data; stop with limits.
- Effort budget: 25 tool calls.
Assumption (headless): assignment = calendar cutover, so nothing identifies the effect; route full.

## Hypotheses
| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | causal | Assist shortened time to close for incidents in pilot groups | like-for-like (severity x group x channel) close time falls post-cutover | no like-for-like drop | within matched strata, post median close time is lower than pre | T1 | incidents, activity |
| H2 | causal | Staffing increase (12->14, 11->13 responders at 06-08) shortened closes | drop concentrated where capacity rose, hours/incident rose | no capacity change | active_responders must step up at 06-08 | T2 | staffing |
| H3 | data-artifact | The headline median is inflated by right-censored/missing closes or close-time recording differences, not true recovery | missing activity rows or close-field coverage differs by workflow/severity/period | coverage equal across arms | activity rows missing/differing by workflow x severity | T3 | incidents vs activity |
| H4 | descriptive (estimand: severity/channel mix share, post minus pre) | Composition shift (more easy incidents post) explains the median drop | mix of severity/channel differs post | mix equal | severity share must differ pre vs post | T4 | incidents |
| H5 | causal | Assist increases work on hard (sev1/sev2) incidents (handoffs, minutes, reopen) while helping easy ones | sev1 minutes/handoffs/reopens not lower post | none | the hard-incident contrast must show no reduction in sev1 minutes | T5 | activity |

## Sources
| id | Origin | Acquired | Coverage notes |
| --- | --- | --- | --- |
| S1 | incidents.csv (420 rows) | frozen extract 06-22 23:59Z | all incidents 06-01..06-14 |
| S2 | activity.csv (409 rows) | same | 11 fewer rows than incidents |
| S3 | staffing.csv (28 rows) | same | group x day daily snapshot |

## Data Validity
- Collection method: incidents (S1) joined to activity (S2) by id; staffing is a daily snapshot (S3). Workflow label matches opened_at vs cutover in 420/420 rows.
- Coverage matrix: S2 lacks 11 of 420 incidents: pre 1 (sev3), post 10 (sev1 x5 of 14 = 36%... 4 shown in sev1 list plus INC0211 etc.; sev2 x2, sev3 x3); post-sev1 close data exists for only 9 of 14 sev1 incidents.
- Field population: all populated where row exists; no negative durations; max close lag 1919 min (<32h).
- Coverage baseline: incidents.csv (every incident opened) is the independent denominator.
- Known instrument failures: none documented. Staffing interruption minutes ~3x higher post.
- Source completeness semantics: S2: UNKNOWN — absent activity row could mean still open at extract, unrecorded, or export incomplete; the missingness pattern (concentrated post, sev1) cannot discriminate and no export contract was given.
- Sensitivity checks performed: bootstrap 95% CIs (2000 resamples within severity x period); no known positive needed since contrasts are well away from zero.

## Tests
| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T1 | H1 | stratified post median close < pre | stratified diff, bootstrap 95% | CONTRADICTED | S1,S2: within every severity post is slower; pre-mix-standardized mean close +233 min [218,247]; sev1 +621 [541,711], sev2 +221, sev3 +132. Unidentified contrast (severity may be downstream of Assist; missing rows) so does not refute alone |
| T2 | H2 | staffing steps up at 06-08 | staffing table | CONSISTENT | S3: responders 11.5->13.5 (+2/group), scheduled hours 91.6->108.9/group-day; incidents/day flat at 15; interruption min 21->67 |
| T3 | H3 | activity missing/differs by arm x severity | coverage matrix | CONSISTENT | S2: 10 of 11 missing rows are post; 5 sev1; post sev1 has 9/14 closes. Direction of bias unknown |
| T4 | H4 | severity mix differs | crosstab | CONSISTENT | S1: sev3 share 46.7%->73.3%, sev1 13.3%->6.7%, sev2 40%->20%; raw median 436->326.5 min but mean 428.5->451.9 |
| T5 | H5 | sev1 minutes not lower | stratified | CONSISTENT | S2: sev1 median responder min 242->311, handoffs 6->0 (n=9 closed), reopens 0 -> 9 overall post (all sev1 median 1) |

## Amendments

- 2026-11-08: no amendments; no hypotheses added after seeing data. Coverage-matrix line in Data Validity written post-hoc during analysis (orientation).
## Conclusion

- Answer: The data cannot show Assist caused faster recovery. The headline median drop (436->326.5 min) is a composition effect: the severity mix shifted to sev3. Mean close time rose (428.5->451.9) and within every severity post-cutover is slower. Mean responder minutes per incident are flat (90.2 vs 90.9). No responder-hours saving is credibly attributable; point estimate is zero-to-negative. Expansion is not supported by this evidence.
- Best supported: H4 (composition) for the headline, via T4; H2 (staffing +2/group same instant) is a live unseparated rival for any effect; H3 unresolved.
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | causal | UNRESOLVED | T1 CONTRADICTED but contrast unidentified (no holdout, concurrent staffing change, severity possibly downstream of Assist), so cannot refute |
  | H2 | causal | UNRESOLVED | T2 CONSISTENT; staffing step cannot be separated from Assist; no discriminating test |
  | H3 | data-artifact | UNRESOLVED | T3 CONSISTENT; completeness UNKNOWN |
  | H4 | descriptive | UNRESOLVED | best supported for headline (T4 CONSISTENT, discriminates from H1 as raw vs stratified diverge) |
  | H5 | causal | UNRESOLVED | T5 CONSISTENT on small n; unidentified |
- Limitations: one cutover, 7 days each side, no holdout; staffing +2 responders and interruption minutes tripled at the same time; severity assigned at open may be affected by Assist (stratifying on it is conditional on a possible mediator); 11 incidents without activity rows (5 sev1 post) with unknown meaning; reopens only observed post; associative only. Continuations: causal-identification-review (e.g. staggered rollout/holdout in non-pilot groups), decision-analysis for expand/no-expand under uncertainty.
