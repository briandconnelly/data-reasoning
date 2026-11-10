# 007 — The likelihood-ratio sweep, a fifth verdict, and loss orientation

Status: accepted, 2026-11-09; revised 2026-11-10 after a cross-model design review.

## Question

Two defects in § Numeric Policy, both reproduced before any wording changed.

The first: a likelihood ratio stated as a range was carried through the posterior and never swept, so a record could take `robust` while its own supported ratio range alone reversed the preferred action.
Prior odds 1, a point prior class, losses 1, and a ratio of 0.1–10 give posterior odds 0.1–10 around a threshold of 1, and both checkers returned no findings.
The dev checker's prior and loss flip tests already read the ratio range at both ends, but switched off whenever the prior class or loss range was a point, called anything within 1% a point, and padded every flip comparison by 1%.

The second: the threshold rule named a "hold" action nothing defined, and never said which losses form the ratio or that it is a ratio of differences.
For losses ship = (10, 0) and hold = (1, 1) over (true, false), the threshold odds are 1/9; reading the ratio as the raw 10:1 gives 1/10, and at odds 0.105 the two readings recommend different actions.

## Positions

*Widen `prior-sensitive` to absorb a ratio-range flip.* No new vocabulary, and the owner gets the record back either way.
Rejected because the crossover would then report prior odds for a flip the prior did not cause: with a point prior class there is no prior-odds interval to move through, and an owner told to reconsider the prior would be reconsidering the wrong input.

*A fifth verdict, after the existing sensitive clauses and before `robust`.* Adopted.
It leaves the prior and loss clauses' meaning and precedence as they were — they already read the ratio range at both ends — and takes only the flips neither can reach, so its crossover names the input the evidence would have to pin down.

*Infer orientation from the order of the Actions slot.* Rejected: valid records list `ship now vs hold one week` and recommend hold, and arbitrary listing order must stay valid.
*Name it in a slot.* Adopted, with the incremental loss ratio defined against the named action; the slot, its sentinel, and the definition live in `../SKILL.md` § Numeric Policy and the template.

*Sweep every input jointly, widening the stated threshold by the inverse of each swept loss for the ratio test as well.* Tried in the first draft and withdrawn on review: on a record with prior odds 0.5, a ratio of 1, a loss ratio of 1, and a stated threshold of 0.1, it demanded `prior-sensitive` where the base checker accepted `robust`, which is a change to the threshold contract this wave does not settle.
The adopted ratio test reads the stated (or loss-supplied) threshold at the stated prior and losses; every record the base checker accepted is still accepted unless a ratio range reverses its action or an exact comparison now decides differently, which the dev suite holds by a differential test against a frozen copy of the base checker.

## Judgement calls

- **The exact tie (an owner may overrule).** The old text said both that a tie counts as a flip and that a single-point range cannot flip; when every input is a point and posterior odds equal the threshold, neither clause gave the record a verdict.
  The choice made was to route that record back to the owner under the first sensitive label rather than add a sixth verdict or leave it with no legal verdict.
  The first draft also sent a stated threshold range straddling on its own to the same label; that case was dropped with the joint sweep, because it belongs to the unsettled threshold contract below.
- **Exactness.** The base checker's 1% point tolerance and flip padding decided boundaries by rounding; for example a prior class of 0.999–1.001 at a threshold of 1 passed as `robust`.
  The checker now reads decimals as exact fractions; tolerance stays only where a stated number is compared with a computed one.
- **Live arithmetic in the shipped validator: considered and deferred.** The first draft had `instruments/check_record.py` recompute the ordered rule.
  It was taken out because it exceeded the brief, would change what the PostToolUse hook does for every user, and would confound measurement: arms stage the validator from the skill ref, so its findings would hand an arm the expected verdict.
  The shipped validator gained only the verdict in its closed set and the slot with its sentinel coupling; all arithmetic is in `tests/check_decision.py`.
  Reopening condition for this point: a measured arm shows agents delivering records whose own arithmetic contradicts their verdict at a rate the structural checks cannot catch, and a preregistered measurement of a validator that does the arithmetic, with its hook messages, has run.

## Verification

The changed dev checker was run read-only against every archived decision record under `tests/runs/`, with the new slot added to an in-memory copy; the run record of that comparison is the branch's verification report, and no archived record's arithmetic finding changed.

## Measurement

Run on 2026-11-10 (`../tests/runs/2026-11-10-evidence-sweep.md`): on both new cells the pre text already produced the right reasoning and action in 3 of 3 arms, so the preregistration's row 7 fired — no behavioral lift at n=3 — and the change ships as a vocabulary and checker fix rather than a measured improvement in reasoning.
What the arms did show is the gap the first defect named: with no fifth verdict, the pre arms on the likelihood-ratio cell labelled a correct analysis `prior-sensitive`, one saying the closed set "has no value for a flip driven by an unswept likelihood ratio", and all three records failed the base checker.
The first packet for the orientation cell was entangled with the likelihood-ratio rule (a 20-per-arm reference class supported a straddling interval) and was redesigned before any scored arm.

## Open owner question

How a stated Decision threshold relates to the threshold the loss ratio implies is not settled here: a stated threshold keeps governing as before, and the prior clause still widens it by the inverse of each swept loss, as the base checker did.

## Reopening condition

A measured arm shows `evidence-sensitive` chosen where the prior or loss clause applies, or the Favored if true slot filled against the Consequences table; or an owner rules differently on the exact tie or on the threshold contract.

## Where the rules live

`../SKILL.md` § Numeric Policy holds the orientation rule, the ordered verdict rule, and the tie and point rulings; `../references/decision-record-template.md` holds the slot's spelling and sentinel.
This record points; it does not restate them.
The preregistered measurement is `../tests/runs/artifacts/2026-11-09-evidence-sweep/prereg.md`, with its reachability assessment beside it.
