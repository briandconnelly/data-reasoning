# 008 — Data validity on `mini` and `direct`: measured, and left unwritten

Decided 2026-09-20, on issue #38.

## Question

The estimation route inherits the full route's data-validity obligations by name; `mini` and `direct` inherit nothing of the kind, and the Mini Route Template has no slot for population, grain, or what an absent record means.
So a simple claim can be settled, or a figure reported, on the wrong rows — a duplicating join, an export that ends early — with every obligation the skill states satisfied.
Should the two cheap routes inherit those obligations, and should a join check exist at all, given that § Plan has none?

## What was decided

**The gap on the page is real, and no wording was added to close it**, because the arms that were measured did not fall into it.
A draft was written, reviewed twice, and measured; it is archived as a patch beside the run record and is not in the skill.

## Positions

*Inherit by pointer, the way the estimation route does.* The precedent is exact — the same gap one route over, fixed on 2026-09-15 and measured as reaching behavior on S9.
This was the draft: a § Routing subsection pointing `mini` and `direct` at § Plan and § Analysis, a join check homed in § Plan, a disposition for a validity condition that stays unresolved, and a template slot.

*Keep `direct` out: its ceremony is "None; answer and stop".* Rejected at design time by both the author and the cross-model reviewer — a wrong figure is as wrong on `direct` as anywhere, and a check that writes no record is compatible with no ceremony.
The measurement then gave this position its only support: the one regression the wave recorded is a `direct` arm carrying the full route's completeness vocabulary into a notes file on a bounded descriptive query.

*Measure first, and let the result decide.* Adopted, per the Iron Law, and this time the declining outcome was written down in advance: the wave's rules said before any arm ran that if every new cell showed no incremental behavior, nothing ships as measured.
The regression half of the wave was left partial — S15 was machine-checked and not fully scored — so the decline is the conservative reading of an unclosed wave, not the firing of its complete rule.

## What settled it

Scenario 22: four cells, each planting one fault on which the answer turns and closing every other, run as no-skill baseline, `main`'s wording, and the draft wording.
All twelve scored arms found the planted fault and none settled the claim on the wrong rows, the four baselines included.
When the first three cells came back that way, the catalog's own rule — a baseline that passes everything means the scenario is too easy — was applied once, with a harder packet specified after those results were read and before any arm read it: a region-shaped hole inside an otherwise whole quarter, the shape the catalog records the skill missing on S1 three times.
All three arms found that too.

The arms on `main`'s wording did not stumble into it.
On the hard packet the pre arm precommitted, in its own ledger, that "the file must have no region x day holes, else the sum is a lower bound of unknown completeness", and built a day-by-region coverage matrix on `mini`, which nothing on that route asks for.
`decisions/005` declined wording on the same ground with a weaker preregistration behind it: adding prose that changes no measured behavior has a cost — a measured token premium that the draft raised by a further 3–20% on these cells, one more subsection to keep consistent, and a body that only accrues because deletion owes arms.

## Why the gap is nonetheless real

Nothing in the result says the cheap routes are safe on the wrong rows.
It says one current model profiles keys, date ranges, and crossed coverage unprompted on small local files.
The textual premise of issue #38 stands, and three things the wave did not reach could still make it bite: a weaker model; a fault that takes domain knowledge to see, such as the wrong revenue definition, which the issue names and no packet plants; and data behind a query interface, where profiling is not free and an agent has a reason to skip it.

One unpreregistered observation is recorded because it is the most useful thing the wave found for whoever reopens this.
Where coverage was unresolved, arms on `main`'s wording put two labels and a hedge in the ledger's Outcome cell, and arms on the draft put one label with its condition.
The draft's disposition sentence may therefore reach the *record* even where it does not reach the *answer*; the wave scored the answer.

An open disagreement is recorded too.
The reviewer held that, with completeness unknown, covered rows can never let a verdict stand, which would turn S11's long-standing FALSE-with-limitation into `NON_DISCRIMINATING`.
The draft instead let such a verdict stand only as conditional on a named assumption.
With no wording shipped the disagreement decides nothing today; it is the first thing a future draft has to settle, and it is the owner's call because it changes a catalog expectation.

## Reopening condition

Any of: a scored arm on `mini` or `direct`, on any model the suite runs, that settles a claim or reports a figure on the wrong rows with the fault discoverable from the data it was given; a fixture whose fault a no-skill baseline misses and which the draft's pointer demonstrably reaches; or a decision to score the Outcome cell's single label, preregistered as such.
Scenario 22's twelve scored arms, across four cells, stand as the regression check for that reopening.
The draft to start from, and the two review passes it survived, are in `tests/runs/artifacts/2026-09-20-cheap-route-validity/` (`draft-wording.patch`, `design-review.md`).

## Where the rule lives

Nowhere new.
The data-validity obligations stay where `SKILL.md` § Plan and § Analysis state them for the full route, and § Estimation Route's pointer to them is unchanged.
The measurement is `tests/runs/2026-09-20-scenario22-cheap-route-validity.md`, preregistered in `tests/runs/artifacts/2026-09-20-cheap-route-validity-prereg.md`.
