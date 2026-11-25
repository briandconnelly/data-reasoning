# 008 — A state that an observation rules out

Status: proposed, 2026-11-24; owner decision pending (issue #114).

## Question

A decide record cannot say that a verified observation rules a state out.
`../references/decision-record-template.md` § Slot notes says "Odds and likelihood ratios are positive", and `tests/check_decision.py` fails any evidence row whose ratio's lower endpoint is at or below zero ("must parse as a positive ratio or range").
The symmetric case, an observation impossible under the other state, has no form at all: the checker's range pattern accepts only finite decimals, so an unbounded ratio cannot be written.
The forms left are a small positive ratio, which invents a magnitude no source supports, or the missing-ratio form, which discards decisive evidence.
No archived run has hit this; it is a gap in the format, and how often real use meets it is unknown.

Two constraints bind any answer.
`003-numeric-provenance-policy.md`: every number names its provenance, and a number nobody can source is not a belief.
`004-binary-scope.md`: the odds-form arithmetic, with one crossover, is defined only for one binary proposition and two actions, and the checker rejects what it cannot compute rather than approximating it.

## Two observations that look alike

*An observation impossible under one state.*
The observation cannot occur if the state holds, for a reason that is not a frequency: a logical or mechanical exclusion, such as the observed behaviour requiring a code path the suspected build does not contain.
Its probability under that state is zero, and no further sampling changes that.
It eliminates the state only if the observation itself is certain; when the observation can be misread or misreported, its probability under the eliminated state is the false-report probability, which is positive, and the ratio is finite again.

*Zero events in a finite sample.*
Zero of n trials under a state whose event rate is p has probability (1 − p)^n, which is positive for every p below 1.
The ratio of that probability between the two states is therefore positive and finite, and the existing machinery records it as an ordinary ratio range with its reference class.
What a zero count supports is an upper bound on the rate, not a rate of zero: the exact one-sided 95% upper bound for zero of n is 1 − 0.05^(1/n), close to 3/n for large n (the "rule of three").
It bounds the rate only from above, says nothing that would exclude small positive rates, and its width is set by n, so recording it as elimination would turn a sample-size limit into a certainty.
The current positive-ratio rule is what stops that conversion, and any change must keep it doing so.

## Positions

*Exact endpoints inside the decide record.*
Allow a ratio of exactly `0`, and an unbounded upper endpoint, in the Evidence table, and carry them through the existing arithmetic.
What it would cost, through the machinery in `../SKILL.md` § Numeric Policy:

- **Posterior odds.** A zero ratio makes posterior odds exactly `0` and an unbounded one makes them unbounded; the template's "Odds and likelihood ratios are positive" excludes both, and both slot grammar and checker parsing (`_RANGE`, `parse_range`) would need a token for infinity.
- **Joint evidence.** Two items, one impossible under each state, multiply to 0 × ∞, which is undefined; the record would need a rule that such evidence contradicts the binary model, which is `004`'s out-of-scope case, not a number.
- **Sweeps.** At a zero ratio every prior in the swept class gives posterior odds `0`, so the prior clause can never flip the action and the `prior-sensitive` verdict becomes unreachable whatever the class; the sweep still runs but tests nothing.
  A ratio range `0–x` makes the evidence clause compare a range touching zero against the threshold, which flips the action whenever x carries the odds past it.
- **Crossovers.** The Crossover slot and the checker require a positive flip point (`_crossover_value`, and the sensitive-verdict check that fails a Crossover whose number is at or below zero); a likelihood-ratio crossover at zero or at infinity would need its own spelling.
- **Ties.** The exact-tie ruling compares posterior odds with a threshold that the checker requires to be strictly positive; odds of `0` never tie it, but an unbounded odds endpoint has no exact comparison to make until infinity is given an ordering.
- **Loss gates.** The loss ratio r is built from loss differences in both states (§ Numeric Policy), and one of those states can no longer occur, so r would weigh a difference that cannot affect the decision.
  Loss class follows sourcing, not state probability, so an owner-supplied loss in the eliminated state stays belief-grade and the loss cap does not fire on it; but a `sensitivity-only` loss there would still cap the verdict at `loss-sensitive`.
  The position therefore owes a ruling on whether r and the cap read losses in an eliminated state.
- **Shipped validator.** `instruments/check_record.py` does no verdict arithmetic (`007-evidence-sweep-and-loss-orientation.md` § Judgement calls), so it needs only grammar changes here; the arithmetic lands on the dev checker.

Each of these is a rule with a home, so this position edits § Numeric Policy, the template's slot notes, and `tests/check_decision.py` at once, and owes arms for every cell whose decision point crosses the edited sentences.

*A resolved proposition outside the odds form.* Recommended.
A proposition that a certain observation rules out is resolved, so the record leaves the odds form: it states the eliminating observation, why the observation is impossible under the eliminated state, and why the observation itself is not in doubt, and then compares the two actions' losses in the surviving state alone.
Likelihood ratios stay strictly positive, so the zero-count guard above keeps working unchanged, and the sweeps, crossovers, ties, and loss gates are never asked to handle `0` or infinity.
The comparison in one state is a loss comparison with no probability in it, close in kind to the `dominated` clause; whether it reuses that clause, a sixth verdict, or a sentinel set is the representation question the owner's acceptance would open (see Open owner questions).

## What argues for the recommendation

The exact-endpoint position spends its whole cost making arithmetic produce an answer the observation already gave: once a state is impossible, priors, sweeps, and crossovers have nothing left to vary.
The resolved path keeps `003`'s rule intact, since it adds no number at all, and keeps `004`'s, since contradictory joint evidence still has nowhere to land but the out-of-scope report.
It also keeps the burden in the right place: the record must justify the impossibility and the certainty of the observation in words a reviewer can check, rather than writing `0` in a cell where it looks like any other ratio.
What it gives up is uniformity: a ruled-out record has a different shape from every other decide record, and an analyst unsure whether the observation is certain must choose between the two forms, which is a judgement the checker cannot make.

## Reversing the recommendation

If the owner prefers exact endpoints, the work is:

1. Decide in § Numeric Policy that a ratio of `0` or an unbounded ratio is admissible only under the impossibility condition above, and that a finite-sample zero count never qualifies.
2. Give the template's slot notes a spelling for an unbounded endpoint and for zero and infinite posterior odds, and rule how 0 × ∞ is reported.
3. Rule, in § Numeric Policy, what each verdict clause and the exact-tie rule do at those endpoints, and whether the loss cap reads losses in an eliminated state.
4. Change the parse and positivity checks in `tests/check_decision.py` (prior odds, evidence ratio, crossover, threshold) to match, with fixtures for each endpoint.
5. Measure DA-S12 and DA-S13 and every existing cell the edited sentences reach.

## Open owner questions

- Accept the resolved path, or reverse to exact endpoints?
- Under the resolved path, which form carries the one-state comparison: the `dominated` clause, a new verdict, or a sentinel set on the belief slots?
- Does a resolved record still route through `decide`, or does an observation that settles the proposition make the ask `out: direct` before any record is written?
- Is an observation that is certain but whose impossibility rests on an assumption (the build manifest is complete) eliminating, or does the assumption's failure probability make the ratio finite?

## Reopening condition

A measured arm shows agents misclassifying a finite-sample zero count as elimination under whichever form ships, or a real decision arrives where the eliminated state cannot be cleanly separated from a surviving one and the resolved path cannot express it.

## Where the rules live

Nothing here is a rule yet.
Once the owner decides, semantics go in `../SKILL.md` § Numeric Policy, the representation in `../references/decision-record-template.md` § Slot notes, and enforcement in `tests/check_decision.py`, each in its one home; this record will point at them.
The paired scenario cells are DA-S12 and DA-S13 in `../tests/scenarios.md`.
