# Computation Checks

These checks catch a computed number that is wrong because of how it was computed, not because of what the world did.
SKILL.md's Analysis section says when they run.
A check that fails is a concrete failure mechanism, so it can promote a `data-artifact` hypothesis; a check that passes is recorded in one line beside the result.

## Join fan-out

A join on a key that is not unique on one side multiplies rows, and every sum or count over the result inflates.
Compare the row count before and after each join, and count rows per original grain key afterward; any key with more rows than the intended join cardinality is fan-out.
A distinct count of the grain key cannot detect it, because duplicated rows keep the same key.

## Average of averages

Averaging group-level means or rates weights every group equally whatever its size.
Name the weighting the claim's estimand calls for first, then confirm the aggregation implements it.
An equal-weight figure and a pooled figure computed from the underlying numerator and denominator answer different questions; when they disagree, the error is whichever one does not match the estimand, not automatically the pre-aggregated one.

## Incomplete periods

A period still accumulating data — the current day, week, or month, or a window whose late-arriving records have not landed — is not comparable with a closed one.
A count or sum over it reads low, but a mean or rate can move either way, depending on which records arrive late; the completeness-semantics rules in SKILL.md's Analysis section govern any claim about the direction of that bias.
Compare only closed periods, or equal-length windows aligned on the same elapsed time, and state the data's completeness horizon.

## Denominator drift

A rate is comparable across periods only if its numerator and denominator mean the same thing in each.
Confirm that no definition, filter, eligibility rule, or event instrumentation changed between the compared periods; when one did, the change is a candidate explanation, not a background detail.

## Timezone and boundary alignment

Sources stamped in different timezones, or one source bucketed in local time and another in UTC, shift events across day and week boundaries.
Confirm every source's timestamp zone and that bucket boundaries match before comparing or joining across sources.

## Magnitude sanity

Check the result against a figure known independently — a total from another system, a prior period, a population size.
A result off by a round factor (10×, 100×, 2×, 7×) usually signals a unit, scale, duplication, or day-versus-week error rather than a real effect.
