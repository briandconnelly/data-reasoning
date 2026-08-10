# Merchant-verification rollout: facts sheet

There is no transaction-level dataset for this rollout -- only the facts below.
Nothing here should be read as a hint toward the right design; it is the complete set of facts a review has to work with.

## Eligibility cutoff

Merchants with lifetime transaction volume of $50,000 or more are auto-enrolled in the new merchant-verification step.
Merchants below $50,000 lifetime volume are not enrolled.
The cutoff is a hard, enforced rule applied uniformly at enrollment time, not a guideline analysts can override.

## Onboarding batch

Enrollment is staged by which processor onboarding batch a merchant was assigned to.
Batch order follows the processor's onboarding capacity and logistics schedule, which was fixed before the verification step existed and is stated to be independent of any merchant's chargeback history or risk profile.
Merchants in an earlier batch reach their enrollment decision (and, if eligible, their verification start date) earlier than merchants in a later batch.

## Pre-rollout chargeback history

Pre-rollout chargeback history was not retained in this export.
Only the 90 days following each merchant's own enrollment date exist in the data the fraud team can pull.
There is no pre-period chargeback series for any merchant, enrolled or not.

## Analyst discretion

Risk analysts had discretion to fast-track "high-touch" merchants into verification early, within their assigned batch, on unrecorded judgment calls.
Which merchants were fast-tracked, and why, was not logged anywhere the fraud team can retrieve.

## Prospective option

A prospective randomized experiment -- enrolling future new merchants into verification vs. not, going forward -- has not been ruled out and could be proposed.
No design work of any kind has been done for it, and none is included here.
