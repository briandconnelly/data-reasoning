# Estimation record: B vs A signup conversion
Goal: decide whether to ship B instead of A; how much lift.
Estimand: difference in signup rate per visit, B minus A (and relative lift), over the population of visitors to the signup page under the same traffic as the 2-week test. Pooled (total signups / total visits) per variant.
Population: visitors 2026-07-01..07-14 (per file), randomized per visitor (stated by user). Generalizes to similar future traffic only.
Uncertainty method: 95% CI committed in advance; Wald/Newcombe for risk difference on pooled counts, plus day-level bootstrap (resample days, paired) as robustness for day-to-day overdispersion.
Practical threshold: not supplied by user; will report whether the CI excludes 0 and the size in absolute pp; threshold = user's call.
Stop condition: one pooled estimate + CI + coverage/overdispersion check; no further data available.
Coverage plan: date x variant matrix, 14 days x 2; check every cell present, visits balanced (randomization sanity), signups<=visits.

Result (S1 = data/signups.csv, 28 rows, 14 days x 2 variants, all cells present, no gaps):
A 583/14089 = 4.14%; B 666/13961 = 4.77%. Diff +0.63pp, 95% CI [+0.15, +1.12]pp (Wald), day-bootstrap [+0.13, +1.12]pp. Relative lift +15% (bootstrap 95% [+3%, +28%]). z=2.57, p~0.01.
SRM check: visits 14089 vs 13961, chi2=0.58 (no imbalance). B>A on 9/14 days. Week1 diff +0.8pp, week2 +0.4pp (not tested formally; noisy).
Limitations: user's threshold unknown; completeness of signups export unverifiable (visits balanced, no missing cells); two weeks only; signups per visit not per unique visitor if visitors repeat.
