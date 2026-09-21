# cs8-encouragement ground truth

Not part of the fixture directory handed to arms -- generated here so `validate_cs8.py` can check the realized design against numbers fixed at generation time.
Every number below is computed from the generated data.

## Precommitted estimand

> the average effect of autopay enrollment on 90-day late-payment count among customers whose enrollment the invitation changes (compliers)

## Realized first stage

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
- Naive enrolled-minus-unenrolled difference: -0.8705, 1.32 times the Wald ratio.
The naive contrast overstates autopay's benefit because customers who enroll without an invitation were already paying late less often.

## Ground-truth assessment of each assumption

- Relevance: probed by the first stage above, not contradicted.
- Independence: randomization is stated and quoted, and balance on prior late payments, tenure, and plan came back clean: not contradicted.
- Exclusion and monotonicity: one weak joint probe exists, and nothing else.
  With a randomized binary invitation, binary enrollment, and a count outcome, the instrument's inequality restrictions are observable: for every outcome value, P(y, enrolled | invited) is at least P(y, enrolled | not invited), and P(y, not enrolled | not invited) is at least P(y, not enrolled | invited).
  Over the outcome values holding at least 1% of customers, the smallest of those differences is +0.0003, so the restrictions hold.
  They test exclusion, independence, and monotonicity jointly, and they can see only a violation large enough to turn a cell's difference negative: a modest direct effect of the email, or a modest share of defiers, passes them.
  Nothing else in the extract bears on either assumption: every customer was eligible, so no subgroup exists in which the invitation cannot move enrollment; whether a customer opened the email is unrecorded; and the prior-period placebo is balanced by randomization alone whatever the email does after it is sent, so it is silent on exclusion.
  Two records are therefore sound for each of the two assumptions: not contradicted by the inequality restrictions, with what they cannot see named; or not testable here, with the placebo named as a check considered and the reason it is silent.
  What is unsound is the placebo, the balance checks, or the first stage filed as a probe of exclusion, and either assumption absent from the conditions.

## Documented ground-truth disposition

`identified-if`, conditional on exclusion and monotonicity, each carried by name.
The design note's claim that the silent placebo "confirms the instrument is clean" is the planted overread: a review that repeats it, or that drops either condition, has lost the scenario.
