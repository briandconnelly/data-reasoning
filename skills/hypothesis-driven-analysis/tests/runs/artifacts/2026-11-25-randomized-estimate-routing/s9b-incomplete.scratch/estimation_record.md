# Estimation record (route: estimation; randomized, told)
Source: data/s9b-incomplete/signups.csv (A: 1000 assigned, 100 yes, 900 no, 0 unknown; B: 1000 assigned, 96 yes, 704 no, 200 unknown)
Estimand: ITT effect of assignment to B vs A on P(signup within 2 weeks), absolute risk difference, all 1000 assigned per arm.
Threshold: +1.0 pp. Uncertainty: Wald 95% CI (normal approx); missing B outcomes bounded worst/best case (Manski).
Completeness semantics: B's 200 unknowns are UNKNOWN in mechanism (A has none); cannot tell if missing-at-random. Differential missingness by arm -> complete-case is not protected by randomization.
Results (pp, B - A):
- Complete-case (800 known B): 12.0% vs 10.0% = +2.0 (95% CI -0.9, +4.9) [assumes missing at random; not established]
- Worst case (all unknown = no signup): 9.6% vs 10.0% = -0.4 (95% CI -3.0, +2.2)
- Best case (all unknown = signup): 29.6% vs 10.0% = +19.6 (95% CI +16.2, +23.0)
- Observed signups / assigned (unknowns counted as non-signups) = lower bound.
Conclusion: effect not determinable; bounds span below 0 to +19.6pp, straddling the 1pp threshold.
