# 007 — The likelihood-ratio sweep, a fifth verdict, and loss orientation

Status: accepted, 2026-11-09.

## Question

Two defects in § Numeric Policy, both reproduced before any wording changed.

The first: a likelihood ratio stated as a range was "carried through the posterior range … never swept on its own", so a record could take `robust` while its own supported ratio range alone reversed the preferred action.
Prior odds 1, a point prior class, losses 1, and a ratio of 0.1–10 give posterior odds 0.1–10 around a threshold of 1, and both checkers returned no findings.
The checker's prior and loss flip formulas already used both ends of the ratio product, but switched off whenever the prior class or loss range was a point, called anything within 1% a point, and padded every flip comparison by 1%.

The second: "hold wins where posterior odds exceed one over the loss ratio" named an action nothing defined, and never said which losses form the ratio or that the ratio is of differences.
For losses ship = (10, 0) and hold = (1, 1) over (true, false), the threshold odds are 1/9; reading the ratio as the raw 10:1 gives 1/10, and at odds 0.105 the two readings recommend different actions.

## Positions

*Widen `prior-sensitive` to absorb a ratio-range flip.* No new vocabulary, and the owner gets the record back either way.
Rejected because the crossover would then report prior odds for a flip the prior did not cause: with a point prior class there is no prior-odds interval to move through, and an owner told to reconsider the prior would be reconsidering the wrong input.
The verdict's job is to say which input the choice turns on.

*A fifth verdict, `evidence-sensitive`, after the existing sensitive clauses and before `robust`.* Adopted.
It keeps every existing clause's meaning and precedence: the prior and loss clauses already read the ratio range at both ends, so a flip they can reach stays theirs, and `evidence-sensitive` takes only what neither can — in practice a point prior class and a point or non-flipping loss range with a ratio range that straddles.
Its crossover reports the likelihood-ratio product at which the action flips, under its own axis phrase, so the record names the input the evidence would have to pin down.

*Infer orientation from the order of the Actions slot.* Rejected: valid records list `ship now vs hold one week` and recommend hold, and arbitrary listing order must stay valid.
*Name it.* Adopted: one Decision-frame slot, Favored if true, names the action with the lower loss when the proposition is true, in the Actions slot's words, with `none needed` under `dominated`.
The loss ratio is then defined as the ratio of incremental losses with both differences positive, and every case where either difference is not positive — dominance and statewise ties — belongs to the `dominated` clause before any division.

## Judgement calls

- **The tie.** The old text said both "a tie counts as a flip" and "a range that is a single point cannot flip".
  The ruling keeps both halves and separates them: comparisons are exact, a range reaching the threshold at an endpoint flips there, and a point never flips on its own.
  When the combined inputs reach the threshold but no range flips on its own — every input a point at an exact tie, or a stated threshold range straddling alone — the record is `prior-sensitive`, the first sensitive clause, with the prior-odds crossover.
  The alternative was a sixth verdict or leaving such a record with no legal verdict; both were judged worse than routing an indifferent decision back to the owner under the first sensitive label.
  This is a judgement call, not a derivation, and the owner may overrule it.
- **Exactness.** "Point" now means endpoint equality, and every decision-boundary comparison is exact; the checkers read decimals as exact fractions so binary rounding cannot decide a boundary.
  Rounding tolerance remains only where a stated number (posterior odds, a crossover) is compared with a computed one.
- **The structural validator does arithmetic.** `instruments/check_record.py` now recomputes the ordered rule when every number it needs is a decimal, and stays silent otherwise; `../../hypothesis-driven-analysis/decisions/006-instruments-are-not-a-live-self-check.md` records the scope step and its bound.

## Verification before the change shipped

The changed checkers were run against every archived decision record under `tests/runs/` (read-only, with the new slot added to an in-memory copy): no record's arithmetic finding changed under `tests/check_decision.py`, and the one new `instruments/check_record.py` finding (`2026-11-08-no-supported-prior/da-s1-pre`) repeats a finding `tests/check_decision.py` already made on that record.
The suites' known-positive records (`VALID_DECIDE`, its no-prior and dominated variants, and every record built in `tests/test_check_decision.py`) needed only the new slot.

## Open owner question

How a stated Decision threshold relates to the threshold the loss ratio implies is out of scope here: a stated threshold keeps governing exactly as before, and the checker still widens it by 1/L across the swept loss range.

## Reopening condition

A measured arm shows `evidence-sensitive` chosen where the prior or loss clause applies, or the Favored if true slot recorded against the Consequences table; or an owner rules differently on the exact tie.

## Where the rules live

`../SKILL.md` § Numeric Policy holds the orientation rule, the ordered verdict rule with `evidence-sensitive`, and the tie and point rulings; `../references/decision-record-template.md` holds the slot's spelling and sentinel.
This record points; it does not restate them.
The preregistered measurement is `../tests/runs/artifacts/2026-11-09-evidence-sweep/prereg.md`, with its reachability assessment beside it.
