# cs7-seam ground truth

Not part of the fixture directory handed to arms -- kept here so stage 1's record can be checked against a precommitted estimand, per `skills/causal-identification-review/tests/scenarios.md` CS7.

## Precommitted estimand

> the local average effect of instant-checkout eligibility on 90-day default rate at the credit-score-680 discontinuity

Stage 1's record must state this estimand in matching terms for stage 2 to reuse verbatim.

## Design ground truth

- No manipulation at the cutoff: the running variable's density is smooth through 680 by construction.
- Covariate balance at the cutoff: `account_tenure_months` and `income` are continuous functions of `credit_score` alone (no jump at 680), so they are balanced immediately around the cutoff.
- No other stated confound at the cutoff: unlike CS3/CS4, this fixture plants no concurrent change, no differential pre-trend, and no selection story.
- Planted local treatment effect: eligible accounts default 6pp less often than the smooth score-only baseline predicts, so the discontinuity is a real, non-flat signal.
