# Computation Checks

These checks catch a computed number that is wrong because of how it was computed, not because of what the world did.
SKILL.md's Analysis section says when they run.
Record each check run, and its outcome, in one line beside the result.

A failed check is a discrepancy, not yet a mechanism: whether it can promote a `data-artifact` hypothesis is settled by the promotion rule in SKILL.md's Plan section.

## Join fan-out

A join fans out when it returns more than one row per row of the original grain — typically when the key is not unique on the side being joined in.
Compare the row count before and after each join, and count rows per original grain key afterward; any key with more rows than the intended join cardinality is fan-out.
A distinct count of the grain key cannot detect it, because duplicated rows keep the same key.

Fan-out does not distort every aggregate.
What follows holds only for aggregates over the original side's values, computed over the metric's filtered and grouped input, with every intended row retained: a field the joined side contributes is a different input, and a join that also drops rows — an inner join with unmatched keys, or a filter on a joined-side field — can change any aggregate, a maximum and a distinct count included.
When every original row in a reported group repeats the same number of times, that group's counts and sums scale by that factor, a signed sum included, while its mean, minimum, maximum, distinct count, and any ratio whose numerator and denominator both scale stay unchanged — values 2 and 4 duplicated once each still average 3.
Duplication that is uniform across the whole table can still be uneven within a group, once a filter or grouping splits it.
When rows repeat unevenly, a mean, a rate, or a signed sum can move in either direction — duplicating only the 2 lowers that average to 8/3 — while a minimum, a maximum, and a distinct count of those values still hold.

Before attributing a discrepancy in the reported metric to fan-out, recompute that metric with the join corrected to its intended cardinality and compare the two.
Hold the population, filters, metric definition, and snapshot fixed — for example, aggregate the joined side to one row per grain key before joining, or replace a many-match lookup with the as-of or current-row match it was meant to be.
Only when that correction keeps every intended match is the difference fan-out's effect on the metric; arbitrarily keeping one row per grain key can attach the wrong match and change the metric for a different reason.

## Average of averages

Averaging group-level means or rates weights every group equally whatever its size.
Name the weighting the claim's estimand calls for first, then confirm the aggregation implements it.
An equal-weight figure and a pooled figure computed from the underlying numerator and denominator answer different questions; when they disagree, the error is whichever one does not match the estimand, not automatically the pre-aggregated one.

## Incomplete periods

A period still accumulating data — the current day, week, or month, or a window whose late-arriving records have not landed — is not comparable with a closed one.
Only an append-only count or a sum of nonnegative values reads low; a signed sum, a mean, or a rate can move either way, depending on which records arrive late; the completeness-semantics rules in SKILL.md's Analysis section govern any claim about the direction of that bias.
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
