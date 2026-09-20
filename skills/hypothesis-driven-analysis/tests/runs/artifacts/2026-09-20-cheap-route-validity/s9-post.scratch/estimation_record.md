# Estimation record: B vs A signup page

Route: estimation (user states each visitor was randomly assigned; design identifies the effect; no prior claim; no rivals to tell apart).

Goal: decide whether to ship B over A; report how much better.
Estimand: difference in signup probability per visit, p_B - p_A (percentage points), plus relative lift p_B/p_A - 1. Pooled over the 14 days (visit-weighted).
Population: visitors to the signup page 2026-07-01..07-14, randomized to A or B. Generalizes to future visitors only if they resemble these two weeks (unverified).
Uncertainty method: 95% CI (committed before reading): Newcombe/Wilson for the difference in proportions, cross-checked with a two-proportion z-test and a day-block bootstrap (resample days) to check day-to-day overdispersion. Relative lift CI by bootstrap.
Practical threshold: none supplied by the user. Report the CI so the user can compare with their own minimum worthwhile lift; no invented threshold.
Stop condition: one pooled estimate + interval + one robustness check (day-level consistency, allocation balance/SRM). No further slicing.

Data validity (orientation, done before any effect computed):
- S1 signups.csv, 28 rows = 14 dates x 2 variants, exactly one row per (date, variant); no missing dates; no nonnumeric values; signups <= visits everywhere.
- Coverage baseline: expected schedule 14 days x 2 variants — matches. No segment field beyond variant.
- Completeness semantics: rows are daily aggregates; no absent cells, so no absent-record inference is needed. Whether all events reached the file is not independently verifiable (no second source): declared below.
- S1: UNKNOWN — no export contract or independent count to discriminate whether every visit/signup was captured; assumed to affect both arms equally (randomization).
- Randomization is stated by the user, not verified; check via sample-ratio (visits split ~50/50).

Result (details in analysis_output.txt):
- A: 583/14,089 = 4.14%. B: 666/13,961 = 4.77%.
- Difference +0.63 pp (95% CI +0.15 to +1.12 pp, Newcombe; day-block bootstrap +0.14 to +1.12). Relative lift +15% (bootstrap 95% CI +3% to +28%). z=2.57, p=0.010.
- Robustness: visits split 50.3/49.7 (SRM z=0.76, no imbalance); B beat A on 9 of 14 days; day-level paired t=2.42 (13 df), consistent with pooled result.
Limitations: randomization taken from the user's statement; the split shows no imbalance but does not prove it. Two weeks only (no check of novelty effects or weekly seasonality beyond 2 cycles); signups = the only outcome (no downstream quality/retention); file completeness unverifiable (S1 UNKNOWN); no practical threshold supplied. Interval is wide relative to the point estimate.
