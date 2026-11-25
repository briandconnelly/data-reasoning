# 008 — A state that an observation rules out

Status: proposed, 2026-11-24; owner decision pending (issue #114).

## Question

A decide record cannot say that a verified observation rules a state out.
`../references/decision-record-template.md` § Slot notes says "Odds and likelihood ratios are positive", and `tests/check_decision.py` fails any evidence row whose ratio's lower endpoint is at or below zero ("must parse as a positive ratio or range").
The symmetric case, an observation impossible under the other state, has no form at all: the checker's range pattern accepts only finite decimals, so an unbounded ratio cannot be written.
The forms left are a small positive ratio, which invents a magnitude no source supports, or the missing-ratio form, which discards decisive evidence.
No archived run has hit this; it is a gap in the format, and how often real use meets it is unknown.

Two constraints bind any answer.
The provenance rules live in `../SKILL.md` § Data Rules and § Numeric Policy, with their rationale in `003-numeric-provenance-policy.md`.
The binary scope, and the checker's refusal to approximate outside it, are `004-binary-scope.md`'s.

## Two observations that look alike

*Elimination.*
Let D be the accepted evidence, the whole observation as recorded, and H the proposition.
Under a stated model, D's likelihood ratio is P(D | H) / P(D | not-H).
D eliminates a state when its likelihood under that state is exactly zero and its likelihood under the other state is positive: the ratio is then exactly 0 or exactly unbounded.
The zero must come from a structural exclusion in the model (a logical or mechanical reason, such as the observed behaviour requiring a code path the suspected build does not contain), never from a frequency.
Imperfect detection does not by itself make the ratio finite: a process that records a true event with probability 0.8 and never records an event that did not occur gives 0.8 against 0, which is still unbounded.
What makes it finite is a positive probability of D under the eliminated state, which arises through false positives, or through failure of the assumptions behind the exclusion.
If D has zero likelihood under both states, conditioning on it is undefined; the disposition is model review (the binary model or its exclusion assumptions are wrong), never a ratio.

*Zero events in a finite sample.*
Under n independent Bernoulli trials with a common event rate p, zero events has probability (1 − p)^n, positive for every p below 1.
The ratio between two states is therefore finite and positive whenever each state assigns the zero count positive likelihood; that conditional is the whole claim, not "finite sample implies finite ratio".
For example, 100 independent weeks with p = 0.02 under H and p = 0.005 under not-H give, at zero events, (0.98 / 0.995)^100 ≈ 0.219.
A zero count alone supports an upper confidence bound on the rate: for zero of n Bernoulli trials the exact one-sided 95% bound is 1 − 0.05^(1/n) (≈ 0.0295 at n = 100), and under a Poisson model over n exposure units it is −ln(0.05)/n (≈ 0.0300), the "rule of three".
The sampling model must be named, because host-weeks drawn from the same hosts can share host-level failures and are then not independent trials.
A confidence bound is neither a state-conditional predictive probability, so it supplies no likelihood ratio by itself, nor evidence of a structural zero.
The current positive-ratio rule stops a zero count from being recorded as elimination, and any change must keep it doing so.

## Positions

The options below are compared at exact structural endpoints only: a ratio of exactly `0` or exactly unbounded.
Ranges that reach an endpoint are a separate choice, listed last.

*A. Exact endpoints inside the decide record.*
Allow an exact `0` or unbounded ratio in the Evidence table and carry it through the existing arithmetic.
What it would cost, through the machinery in `../SKILL.md` § Numeric Policy:

- **Posterior odds.** An exact zero ratio makes posterior odds exactly `0` and an unbounded one makes them unbounded; the template's "Odds and likelihood ratios are positive" excludes both, and slot grammar and checker parsing (`_RANGE`, `parse_range`) would need a token for infinity.
- **Joint evidence.** Two items, one impossible under each state, multiply to 0 × ∞; that is the both-zero case above and takes the model-review disposition, which `004`'s out-of-scope report already resembles.
- **Sweeps and crossovers.** At an exact endpoint every finite positive prior gives the same posterior (0 or unbounded), so no finite positive prior crossover exists and the prior clause can never flip the action; the sweep runs but tests nothing.
  The Crossover slot and the checker require a positive flip point (`_crossover_value`, and the sensitive-verdict check that fails a Crossover at or below zero).
- **Ties.** The threshold is strictly positive in the checker, so odds of exactly `0` never tie it, and unbounded odds need an ordering against it before the exact-comparison rule can apply.
- **Loss gates.** The loss ratio r is built from loss differences in both states (§ Numeric Policy), and one of those states can no longer occur, so r would weigh a difference that cannot affect the decision.
  Loss class follows sourcing, not state probability, so an owner-supplied loss in the eliminated state stays belief-grade and the loss cap does not fire on it; but a `sensitivity-only` loss there would still cap the verdict at `loss-sensitive`.
  The position therefore owes a ruling on whether r and the cap read losses in an eliminated state.
- **Validators.** The positivity check is a numeric guard in the dev checker, `tests/check_decision.py`.
  The shipped validator, `instruments/check_record.py`, parses no numeric ratio: it checks each evidence row's provenance class and the paired missing-ratio sentinels, so it changes only if the chosen form adds a sentinel or slot.

*B. Exact endpoints, decided by the one-state comparison.*
Record the exact `0` or unbounded ratio in the Evidence table, so the evidence keeps a numeric form, but take the verdict from the surviving-state comparison in C rather than from the odds arithmetic.
It costs the grammar and parsing work of A and a rule that an exact endpoint switches the verdict path, but spares the sweep, crossover, and tie rulings.

*C. A resolved proposition outside the odds form.* Recommended.
The record states D, the structural reason D is impossible under the eliminated state, and why D's likelihood under the surviving state is positive, and then leaves the odds form.
Resolving the state does not remove the decision: with S the surviving state, the expected loss difference given D is L(A, S) − L(B, S), and the record still has to compare it.
That comparison keeps the provenance rules, the missing-loss gate, and the uncertainty checks of § Numeric Policy, applied to the surviving-state losses.
Strict preference: a supported difference with one sign everywhere in its stated range names that action.
Tie: a difference of exactly zero prefers neither action.
Unsupported or sign-changing: a difference that lacks belief-grade losses, or whose stated range spans zero, returns the choice to the owner.
It cannot reuse the `dominated` clause as written: with losses A = (1, 0) and B = (1, 5) over (S, eliminated), `dominated` prefers A, though in the surviving state both cost 1 and the actions tie.
Likelihood ratios stay strictly positive, so the zero-count guard keeps working unchanged, and the sweeps, crossovers, ties, and loss ratio never meet `0` or infinity.

*D. Ranges that reach an endpoint.*
A range such as `0.5` to unbounded still admits finite values on both sides of the threshold, so it is not elimination and C does not apply; it would need its own sweep semantics.
`../SKILL.md` § Numeric Policy already counts a range endpoint that reaches the threshold as a flip there, and that rule would have to say what an endpoint at infinity does.
This is a separate owner choice and not part of the recommendation.

## What argues for the recommendation

Options A and B spend their cost making arithmetic produce an answer D already gave: once a state is impossible, priors, sweeps, and crossovers have nothing left to vary.
C adds no new number, so the provenance rules are untouched, and keeps `004`'s scope, since the both-zero case still lands on model review.
It also puts the burden where a reviewer can check it: the record must justify the structural exclusion in words, rather than writing `0` in a cell where it looks like any other ratio.
What it gives up is uniformity: a ruled-out record has a different shape from every other decide record, and whether an exclusion is structural is a judgement the checker cannot make.

On the voi route, if the state is settled and a signal would reveal only that same state, its gross information value is zero; a signal about the surviving-state losses, or about an exclusion assumption, is a different calculation.

## Contract changes each option owes

`../SKILL.md` § Routing reserves `out: direct` for bounded, unasserted, non-causal facts the records settle, and `decide` for a choice under uncertainty with a full record.
Keeping a resolved proposition on `decide` (A, B, or C) changes § The Decide Route: its blocks and its closed list of six verdicts would need a form for the surviving-state comparison, whether a seventh verdict, a sentinel set on the belief slots, or a ruling inside an existing verdict.
Routing it to `out: direct` would change § Routing, because a resolved causal proposition with a loss comparison is not a bounded non-causal fact, and would drop the record that carries the comparison's provenance.

## Reversing the recommendation

If the owner prefers A, the work is:

1. Decide in § Numeric Policy that an exact `0` or unbounded ratio is admissible only under the elimination condition above, that a finite-sample zero count never qualifies, and that the both-zero case goes to model review.
2. Give the template's slot notes a spelling for an unbounded endpoint and for zero and unbounded posterior odds.
3. Rule, in § Numeric Policy, what each verdict clause and the exact-tie rule do at those endpoints, and whether r and the loss cap read losses in an eliminated state.
4. Change the parse and positivity checks in `tests/check_decision.py` (prior odds, evidence ratio, crossover, threshold) to match, with fixtures for each endpoint, and touch `instruments/check_record.py` only if a sentinel or slot is added.
5. Measure DA-S12 and DA-S13 and every existing cell the edited sentences reach.

Reversing to B is steps 1, 2, and 4 plus the surviving-state comparison of C; D is a separate change on top of either.

## Open owner questions

- Accept C, or reverse to A or B?
- Under C, which form carries the surviving-state comparison in § The Decide Route: a seventh verdict, a sentinel set on the belief slots, or a ruling inside an existing verdict?
- Does a resolved proposition stay on `decide`, or does § Routing change to send it elsewhere?
- When an exclusion rests on an assumption (the build manifest is complete), is the ratio exact, or does the assumption's failure probability make it finite?
- Is D wanted at all?

## Reopening condition

A measured arm shows agents misclassifying a finite-sample zero count as elimination under whichever form ships, or a real decision arrives where the eliminated state cannot be cleanly separated from a surviving one and the chosen form cannot express it.

## Where the rules live

Nothing here is a rule yet.
Once the owner decides, semantics go in `../SKILL.md` § Numeric Policy, routing in § Routing, the record shape and verdict list in § The Decide Route, the representation in `../references/decision-record-template.md` § Slot notes, and enforcement in `tests/check_decision.py` (and `instruments/check_record.py` if the form adds a sentinel or slot), each in its one home; this record will point at them.
The paired scenario cells are DA-S12 and DA-S13 in `../tests/scenarios.md`.
