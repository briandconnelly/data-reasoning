Route: estimation (assignment stated as random; one comparison; no rival explanations to separate).
Goal: decide whether B is worth adopting given a minimum worthwhile absolute gain of 1 percentage point.
Estimand: ITT effect of assignment to B vs A on P(signup within 2 weeks) = p_B - p_A, absolute, in percentage points.
Population: the 2,000 distinct visitors randomized in this experiment (1,000 per arm).
Uncertainty method: 95% interval (committed before reading), Wald and Newcombe score for the difference, plus a 5,000-draw parametric bootstrap check.
Practical threshold: +1.0 pp.
Stop condition: single pre-specified contrast; stop once the interval is computed and compared with the threshold.
Source: S1 signups.csv (2 rows of counts). Coverage: assigned = signed_up + did_not_sign_up in both arms (100+900, 120+880); outcome_unknown = 0 in both arms, so there is no missing-outcome bias to bound. Completeness semantics of S1: counts per arm; the "within two weeks" window is taken as complete (no unknowns). Cannot check from the file whether the 2-week follow-up was matured for every visitor; recorded as an assumption.
Result: A 100/1000 = 10.0%; B 120/1000 = 12.0%; diff = +2.0 pp. SE 1.40 pp. 95% CI: Wald [-0.74, +4.74] pp; Newcombe [-0.75, +4.76]; bootstrap [-0.7, +4.8]. z = 1.43. Bootstrap share of draws with diff >= 1 pp: ~76% (descriptive, not a probability that the true effect >= 1 pp).
Limitations: interval includes 0 and includes the 1 pp threshold, so the data do not establish a gain of >= 1 pp nor rule out no effect or a small harm. Counts only: the randomization, one-row-per-visitor, and interference/crossover cannot be verified from the file. Effect is of assignment (ITT).
Script: est.py
