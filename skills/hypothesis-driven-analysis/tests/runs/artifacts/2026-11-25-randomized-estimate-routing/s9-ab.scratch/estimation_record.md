Goal: decide whether B should replace A on the signup page.
Estimand: difference in signup rate per visit, B minus A (and relative lift), under random assignment.
Population: visitors to the signup page, 2026-07-01..07-14, as sampled by those two weeks.
Uncertainty method: 95% Wald interval on difference of proportions (committed before reading); cross-check by day-level bootstrap (10,000 resamples of days).
Practical threshold: none supplied by user; assumed any lift whose interval excludes 0 is relevant, flagged for user to supply.
Stop condition: single pass; the data cannot be tightened further.
Coverage: 14 days x 2 variants, no gaps; visits A 14,089 / B 13,961 (sample-ratio z=0.76, consistent with 50/50). Outcome completeness semantics: not documented (assumed every signup recorded; UNKNOWN beyond that).
Result: A 583/14089 = 4.14%; B 666/13961 = 4.77%; diff +0.63 pp, 95% CI [+0.15, +1.12] pp; relative +15% (day-bootstrap [+3%, +28%]).
Limitations: randomization is as stated, not verified; two weeks only (novelty effects, weekly seasonality covered 2 cycles); counts of signups per visit not per unique visitor (repeat visits may break independence); no downstream quality/retention measure.
Script: work/est.py
