# 007 — Per-assumption assessments ship as an unmeasured clarification

Status: accepted, 2026-09-20, on issue #40.
The owner's decision, taken on the cross-model reviewer's recommendation.

## Question

The per-route procedure gave every named assumption a probe and defined the one favorable disposition as carrying "the probes supporting each".
An assumption with no probe that settles it — exclusion for an instrument, exchangeability for an observational comparison — then had no record that was both faithful to the text and favorable: the design was stranded short of its conditional disposition, or a check that was silent on the assumption was filed beside it as support.
A fix was drafted: a closed per-assumption assessment vocabulary in which no value says "supported", a rule that a silent check is not a probe, a stated precedence for the dispositions, and checker gates for all of it.
The repository's Iron Law says a wording change is measured before it is trusted.
Should this one ship without arms?

## Positions

*Measure it as preregistered (not taken).*
A wave was preregistered — a new cell, CS8, with baseline, pre, and post arms, and CS3 and CS6b as regression cells — and its design was reviewed four times before any arm ran.
Every pass ended no-go, and the fourth said why the wave could no longer decide anything: three fixtures in a row turned out to leave the assumption some weak observable implication, so a knowledgeable arm on the old wording can meet "every assumption gets a probe" with a weak bound and pass every assertion.
One pre arm against one post arm on a pass-everything comparison then cannot tell the wording change from domain knowledge.

*Measure it properly (not taken now; the reopening condition).*
Make the primary endpoint the two errors the issue names — a silent diagnostic credited to the assumption, or the stranded disposition chosen only because no probe was known — and run repeated independent pre and post arms.
That is a sound design and a much larger spend than the wave preregistered, for a change whose textual case does not rest on it.

*Ship it as a clarification that claims nothing about behavior (adopted).*
The text contradicted itself, and the contradiction is visible on the page without an arm: the favorable disposition asked for support that some assumptions cannot have.
One horn of the consequence is in the archive — the CS7 arm of 2026-08-09 that "correctly refused" the favorable disposition because an assumption "had no discriminating evidence available in the data", answered then by adding a fact to the fixture and not a state to the skill.
The preregistration wrote this outcome down before any review: a cell landing where the change is not needed leaves the text "the owner's call as an unmeasured clarification of a contradiction the text does contain".

## What settled it

Four design-review passes, recorded with every finding and its disposition in `../tests/runs/artifacts/2026-09-20-untestable-assumptions/design-review.md`.
They did not show the wording to work; they showed that the measurement as designed could not show it either way, and they removed a run of defects from the wording, the checker, and the fixture that a single arm would not have found.
The substantive thing they settled is that strict untestability almost never survives the presence of outcome data, so the wording does not depend on it: an implication the review can name owes its probe however weak, a weak probe that could have been contradicted is assessed as not contradicted with its blind spot named, a bound nothing could violate is a silent check, and the untestable value is the review's own finding, which its row makes contestable by naming the checks considered and why each is silent.

What this decision does not claim: that the wording changes what an agent does.
No arm has run against it.
CS8 ships as a regression scenario with zero arms, and the cells whose decision points traverse the edited text — CS3, CS4, CS6b, CS7 stage 1, and CS8 — are recorded as owed against it in `../tests/scenarios.md` § Owed measurements.

## Reopening condition

Any of: a scored arm on this wording credits a silent diagnostic to an assumption, or strands a design for want of a probe; a regression cell moves off its documented disposition under the restated precedence; or a wave with the endpoint described under "Measure it properly" is funded.
The third is the one that would turn this from a clarification into a measured claim.

## Where the rule lives

`../SKILL.md` § Per-route procedure, the single home for the assessment values, what each means, and the disposition precedence.
`../references/identification-review-template.md` carries the slots and points there; `../tests/check_review.py` enforces the shape.
