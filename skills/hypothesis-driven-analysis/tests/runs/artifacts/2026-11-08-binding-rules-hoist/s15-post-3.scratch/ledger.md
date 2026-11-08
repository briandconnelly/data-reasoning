# Investigation: Did Assist cause faster recovery (June 8 cutover), and how many responder-hours are attributable?

## Problem
- Decision informed: expand Assist company-wide; whether to book Finance's responder-hour savings.
- Falsifiable question: among 420 incidents opened 2026-06-01..14 (identity, storage), did Assist change time-to-close (hours) / responder minutes per incident?
- Success criteria: answered = causal effect identified or declared not identifiable; savings number either bounded or declared unavailable.
- Stop condition: conclude after T1-T5; stop with limits if composition/staffing/missingness leave the sign open.
- Effort budget: 15 queries.
- Assignment: single cutover, no holdout, same 2 groups -> nothing identifies effect -> full route.

## Hypotheses
| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | causal | Assist shortened time to close within comparable incidents | within severity strata, Assist TTC lower | within-stratum no difference | within-severity median TTC difference (assist-manual) must be negative | T1 | incidents, activity |
| H2 | descriptive (estimand: share of sev1 among incidents opened, assist vs manual week) | Headline drop reflects severity mix (fewer sev1 in Assist week), not faster handling | mix-standardized difference much smaller than raw | standardized ~ raw | sev1 share must differ between weeks | T2 | incidents |
| H3 | data-artifact | Incidents missing from activity.csv (unclosed/unrecorded), concentrated in hard Assist cases, bias Assist TTC down | missing rows concentrated in Assist and in high severity; bounding them as long-running erases the drop | missing evenly spread | missing rate must be higher in Assist week | T3 | incidents vs activity |
| H4 | causal | Concurrent staffing increase (+2 responders/group at cutover) rather than Assist shortened close | staffing step at June 8 coincides; scheduled hours/incident up | staffing flat | staffing step must occur at 06-08 | T4 | staffing |
| H5 | causal | Assist adds work on hard incidents (responder complaint): responder minutes/handoffs not lower, or higher, on sev1 | sev1 minutes/handoffs/reopens >= manual | lower | sev1 responder-minute difference must be >= 0 | T5 | activity |

## Sources
| id | Origin | Acquired | Coverage notes |
| S1 | incidents.csv | frozen extract 2026-06-22 23:59Z | 420 rows, unique ids |
| S2 | activity.csv | same | 409 rows (11 incidents absent) |
| S3 | staffing.csv | same | 28 rows = 14 days x 2 groups |

## Data Validity
- Collection method: frozen CSV exports of incident, activity and staffing systems; no collection beyond these files.
- Coverage matrix: workflow x group x severity counts of incidents vs activity rows (see Tests T3); absent activity rows: assist 10 (sev1 5/14, sev2 2/42, sev3 3/154), manual 1 (sev3).
- Coverage baseline: staffing incidents_opened = 15/day/group (independent denominator) matches incidents.csv; activity.csv has no independent baseline, so its completeness is unverifiable.
- Notes: incidents per day per group =15 (S3 incidents_opened) vs S1: independent denominator, matches by design. Activity coverage by workflow x group x severity computed in orientation: absent rows assist 12 / manual 1 (see Tests T3).
- Source completeness semantics:
S2: UNKNOWN — no export contract or sentinel; absent rows could be still-open, unrecorded, or export-incomplete, and the missingness pattern cannot discriminate.
- Censoring: closes are observed only for incidents that closed by extract; week-2 maturity >=8 days.

## Tests
| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| T1 | H1 | within sev strata TTC median lower for Assist | stratified medians + bootstrap CI (95%) on contrast | CONTRADICTED | Assist median TTC higher in every stratum: sev1 18.3->27.6h (diff CI +7.7..+11.9), sev2 8.5->12.3 (+3.0..+4.3), sev3 2.8->5.0 (+1.9..+2.5). Design is unidentified (single cutover, staffing step), so this leaves H1 UNRESOLVED, not refuted; adequacy not claimed |
| T2 | H2 | sev1 share lower in Assist week; severity-standardized diff < raw | share table; direct standardization to pooled mix | CONSISTENT | sev1 share 13.3% manual (28/210) vs 6.7% assist (14/210); sev3 46.7% vs 73.3%. Raw median 7.3h->5.4h, but standardized mean TTC 6.1h manual vs 9.5h assist: sign reverses. Assumes severity is not downstream of Assist (unverified) |
| T3 | H3 | missing concentrated Assist/sev1; worst-case bound | missing rates; bound missing as censored at 8d | CONSISTENT | missing 10 assist (5 sev1 of 14) vs 1 manual; counting them as very long raises Assist median only 5.4->5.5h, so it does not create the headline drop; it makes Assist sev1 look better than it is |
| T4 | H4 | staffing step at 06-08 | pre/post staffing | CONSISTENT | active responders 11.5->13.5/group, scheduled hrs/day 91.6->108.9, interruption min 20.7->66.7, all stepping on 06-08. Staffing change is confounded with Assist; its effect is not separable |
| T5 | H5 | sev1 resp-min not lower in Assist | stratified resp-min, handoffs, reopens | CONSISTENT | sev1 mean responder-min 240->312 (diff CI +62..+83), sev2 99->137, sev3 39->65; sev1 n=9 closed in assist; handoffs fall sev1 5.9->0.4 but rise sev2/3; reopens 1 sev1 assist case |

## Amendments
- 2026-11-08: Data Validity slots completed structurally to satisfy the record checker; no prediction or outcome changed.

## Conclusion
- Answer: The headline drop is a severity-mix artifact. Assist week had half the sev1 share; within every severity Assist incidents closed slower and used more responder minutes. Assist did not demonstrably cause faster recovery; the data cannot identify its effect (single cutover, +2 responders/group at the same moment, no holdout). Responder-hours attributable to Assist: none creditable; association points to extra work (about +34 min/incident standardized), not savings.
- Best supported: H2 (mix), with H4 a confounder; H5 consistent with responder reports.
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | causal | UNRESOLVED | T1 CONTRADICTED on non-identified contrast (stratified Assist slower) cannot refute; staffing step masks/mixes effect |
  | H2 | descriptive | UNRESOLVED | best supported (T2 CONSISTENT) |
  | H3 | data-artifact | UNRESOLVED | T3 CONSISTENT for gap, but it does not produce the drop |
  | H4 | causal | UNRESOLVED | T4 CONSISTENT on staffing step; effect unseparated |
  | H5 | causal | UNRESOLVED | T5 CONSISTENT, associative only |
- Limitations: whether severity is assigned independently of Assist unverified; sev1 n=9 closed in Assist week; 11 activity rows absent with UNKNOWN semantics; one week per arm; no counterfactual for time trends or staffing; the sev1 handoff collapse may be a recording change.
