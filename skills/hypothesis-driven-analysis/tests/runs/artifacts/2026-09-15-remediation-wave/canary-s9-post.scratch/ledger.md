# Investigation: Is signup-page variant B better than A, and by how much?

## Route

Estimation. The user states visitors were randomly assigned to A or B for the two-week run, which identifies the causal contrast directly — no rival explanation needs to be told apart, and no prior claim is being adjudicated. Per SKILL.md's routing table and its causal-question section: "Is B better than A, and by how much" over a stated random assignment is an estimation task, not `full` or `mini`.

## Estimation Route Record

Goal: decide whether variant B's signup page converts visitors to signups at a higher rate than variant A, and quantify the difference, to inform whether to ship B.
Estimand: difference in per-visitor signup conversion rate, B minus A — rate_B = sum(signups_B)/sum(visits_B), rate_A = sum(signups_A)/sum(visits_A) — pooled over the full two-week run; also reported as relative lift (rate_B/rate_A − 1).
Population: visitors to the signup page during 2026-07-01 through 2026-07-14, the window randomization ran over. The estimate describes this traffic; it does not by itself extrapolate to future traffic mix or seasons outside this window.
Uncertainty method: two independent interval computations, both at 95% coverage (committed before reading either):
  1. Pooled two-proportion Wald interval on the rate difference, using aggregate visit/signup counts across the full window.
  2. Day-level paired interval (14 daily B−A rate differences, one pair per calendar day, t-interval on the mean difference) — a cross-check that does not depend on pooling assumptions and would catch any day-level confound the pooled estimate could mask.
Practical threshold: not stated by the user. No minimum lift was given as the bar for shipping B. Reporting the point estimate and both intervals so the user can apply their own decision threshold (e.g., relative to B's implementation/maintenance cost).
Stop condition: estimate is good enough when both interval methods agree in sign and rough magnitude and exclude zero at the committed coverage; conclude without further collection once that holds, since the two-week dataset is a fixed, complete census of the run (no further data exists to tighten it).

## Sources

| id | Origin | Acquired | Coverage notes |
| --- | --- | --- | --- |
| S1 | /var/folders/q1/yy47kpf51gb44d8wg1ywz4p80000gq/T/arm-canary-s9-post-64tvq61u/data/signups.csv | this session | 28 rows: 14 calendar days (2026-07-01..2026-07-14) × 2 variants (A, B), one row each — confirmed complete, no gaps |

## Data Validity

- Collection method: daily aggregate visits/signups per variant, as provided; no per-visitor log available.
- Coverage matrix (grain = day × variant, the grain both the pooled and paired estimates use): 14 days × 2 variants = 28 cells expected, 28 present. Every cell has both `visits` and `signups` populated with positive integers. No day is missing either variant.
- Field population: `visits` and `signups` are 100% populated across all 28 rows; no nulls, no non-numeric values observed.
- Coverage baseline: expected schedule is one row per variant per calendar day for 14 consecutive days starting 2026-07-01 — matched exactly by inspection of the date column.
- Known instrument failures: none reported or observed.
- Source completeness semantics: S1 is a complete day-level census of the stated run (not a sample), so there is no "absent record" question at the row grain. One real ambiguity remains and is UNKNOWN: whether a day's `signups` count reflects signups from that day's assigned visitors (cohort-attributed) or signups completed that calendar day regardless of visit date (event-day-attributed, which would mix in delayed conversions from visitors assigned on earlier days). S1: UNKNOWN — no data dictionary or field definition was available to distinguish these readings, and the file's own contents cannot establish which convention was used. This does not bias the day-level census total (every visitor and every signup is counted exactly once either way over the full 14-day window, since assignment is per-visitor and stable), but it means single-day rates are a weaker read than the pooled two-week rate.
- Sensitivity checks performed: the pooled two-proportion interval and the independent day-level paired interval were computed from the same underlying counts but via non-nested methods (aggregate-count Wald vs. per-day paired t on 14 fresh daily observations); their agreement is the corroboration this dataset supports without an external comparison group.

## Analysis

Computation (python3, inline, from S1):

- A: visits=14,089, signups=583, rate=4.14%
- B: visits=13,961, signups=666, rate=4.77%
- Point estimate, diff (B−A) = +0.63 percentage points; relative lift = +15.3%
- Pooled two-proportion 95% Wald CI on diff: [+0.15pp, +1.12pp]
- Day-level paired 95% t-interval (df=13) on mean daily diff: [+0.07pp, +1.19pp]
- B's daily rate exceeded A's on 9 of 14 days; the two days B lost by the largest margin (07-10: −1.08pp; 07-06 A lost, B won by +2.31pp — no single day dominates the total)

Confound/aggregation-reversal check: visits per day per variant range narrowly (944–1068), so no variant is disproportionately represented on unusual days; the paired day-level interval, which controls for any day-to-day shock common to both variants that day, agrees in sign and magnitude with the pooled estimate, so pooling is not manufacturing or hiding the effect.

Both intervals exclude zero and agree closely in sign and magnitude (~0.1–1.2pp), so the estimate is not sensitive to the choice of aggregation method.

## Conclusion

- Answer: yes — B converted visitors to signups at a higher rate than A over the two-week run. Point estimate: B is +0.63 percentage points higher (4.77% vs. 4.14%), a +15.3% relative lift. 95% interval on the difference: roughly +0.1 to +1.2 percentage points by either estimation method, excluding zero.
- Basis: stated per-visitor randomization identifies this as the causal effect of variant on conversion for this traffic and window; two independent interval methods (pooled two-proportion, day-level paired) agree in sign and magnitude.
- Limitations:
  - No practical threshold was given by the user for "better enough to act on" — the interval (roughly 0.1–1.2pp, or 15% relative) is reported for the user to compare against B's cost to build/maintain.
  - The estimate generalizes to the traffic and conditions of this specific two-week window; it does not by itself extrapolate to different seasons, traffic sources, or a longer run, since only two weeks were observed.
  - Day-level signup attribution (cohort vs. event-day) is UNKNOWN per the Data Validity section above; this doesn't change the two-week pooled total but means the day-level paired check is a slightly weaker corroboration than a per-visitor log would give. Both interval methods still agree, so this does not change the conclusion.
