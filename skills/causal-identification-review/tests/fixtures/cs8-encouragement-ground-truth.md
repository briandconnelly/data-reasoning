# cs8-encouragement ground truth

Not part of the fixture directory handed to arms -- generated here so `validate_cs8.py` can check the realized design against numbers fixed at generation time.
Every number below is computed from the generated data.

## Precommitted estimand

> the average effect of autopay enrollment on 90-day late-payment count among customers whose enrollment the invitation changes (compliers)

## Realized first stage (from the by-arm counts)

- Enrollment rate, invited: 0.4520.
- Enrollment rate, not invited: 0.1480.
- Difference: 0.3040 (z = 27.23, 95% interval 0.2821 to 0.3259).

## Realized balance by `invited`

- `late_payments_prior_90d` mean: invited 1.0760, not invited 1.0993, difference -0.0233 (95% interval -0.0850 to +0.0384), standardized difference -0.0191.
- `tenure_months` mean: invited 60.3067, not invited 59.6383, standardized difference +0.0194.
- `plan` share `basic`: invited 0.5113, not invited 0.5307, standardized difference -0.0387.
- `plan` share `standard`: invited 0.3420, not invited 0.3353, standardized difference +0.0141.
- `plan` share `premium`: invited 0.1467, not invited 0.1340, standardized difference +0.0365.

## Realized contrasts in `late_payments_90d`

- Intent-to-treat difference (invited minus not invited): -0.2000 (z = -6.55, 95% interval -0.2599 to -0.1401).
- Wald ratio (intent-to-treat difference over first-stage difference): -0.6579.

## Ground-truth assessment of each assumption

- Relevance: probed by the first stage from `enrollment_by_arm.csv`, not contradicted.
- Independence: randomization is stated and quoted, and balance on prior late payments, tenure, and plan came back clean: not contradicted.
- Exclusion: one weak joint bound, and nothing else.
  If the invitation is independent of outcomes, reaches late payments only through enrollment, and moves no customer's enrollment the wrong way, the two arms' outcome distributions can differ only among customers whose enrollment it moves, so their total-variation distance cannot exceed the first-stage difference.
  The bound follows from independence, exclusion, and monotonicity together, not from exclusion alone; a record that uses it says so.
  The distance is 0.0790 against a first-stage difference of 0.3040, so the bound holds, and with that much slack it could be broken only by a large violation of one of the three: a direct effect of the email on a large share of customers, say, or a large share whose enrollment it moves the wrong way.
  Enrollment exists only as counts by arm, so the joint distribution of invitation, enrollment, and outcome -- which the instrument's inequality restrictions need -- cannot be formed.
  Every customer was eligible, so no subgroup exists in which the invitation cannot move enrollment.
  Whether a customer opened the email is unrecorded.
  The prior-period placebo is balanced by randomization alone whatever the email does after it is sent, so it is silent on exclusion.
  A customer-level enrollment field, or a randomized arm sent an email with no enrollment content, would make it testable in earnest.
  Two records are therefore sound: not contradicted by that bound, with its blind spot named; or not testable here, with the placebo named as a check considered and the reason it is silent.
  A review is not required to know the bound; it is required not to mistake the placebo, the balance checks, or the first stage for a probe of exclusion.
- Monotonicity: defiers are unobservable, and without customer-level enrollment the inequality restrictions that could expose a large share of them cannot be formed.
  Its only observable implication is the sign of the first stage, which is positive; the same two records are sound.

## Documented ground-truth disposition

`identified-if`, conditional on exclusion and monotonicity, each carried by name.
The design note's claim that the silent placebo "confirms the instrument is clean" is the planted overread: a review that repeats it, or that drops either condition, has lost the scenario.
