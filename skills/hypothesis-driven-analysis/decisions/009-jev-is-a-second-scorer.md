# 009 — Jev is a second scorer, not a scorer

Decided 2026-09-24.

## Question

Every scored claim in this repo rests on one agent reading archived arms, sometimes corrected by a second model's review, and the representative suite and n≥5 cells stay unpaid partly because that reading is expensive.
TypeSafe's Jev answers narrow typed questions cheaply.
Should it score arms, route prompts, or check ledgers, and on what terms?

## What was decided

**Jev is optional development tooling that runs beside the existing scorer and never replaces it.**
It lives in `jev/`, outside the release tree and outside every skill, hook, and instrument.
Its output marks points for a person to read; it is never itself a measured result.

## Positions

*Use Jev as the grader, and make n≥5 per cell affordable.* This was the proposal's first idea, and it is what the cost argues for.
The pilot does not support it: blind questions agreed with the agent scorer on 39–40 of 49 points, and about half the misses were Jev reading errors, not rubric problems.

*Put a routing hint in a hook.* It would bypass the frozen descriptions without ever measuring them.
It also sends user prompts to a third party from inside the plugin, and hook output is agent-read prose, which under decision 006 owes measured arms.
Declined outright, and not built.

*Add a `--semantic` mode to `instruments/check_record.py`.* Decision 006 keeps the instrument stdlib-only and fixture-neutral, and a network call inside the live hook's validator breaks the first and makes "not checked" a routine hook outcome.
Built instead as a separate script that nothing imports.

*Second scorer with an abstain band.* Adopted.
It keeps the part of the proposal the pilot supports — cheap flags on the points where a scorer is most likely wrong — and nothing the pilot contradicts.

## What settled it

The pilot (`jev/pilot/2026-09-24/record.md`), in three results.

The honest agreement figure was 80%, against an agent reference, from questions written blind to it; the near-perfect figure came from questions written after reading the reference, which measures the author's hindsight, not Jev.

The points where Jev sat near 0.5 were the points the agent scorer had itself got wrong and corrected on review, which is the property a second scorer needs and a sole scorer cannot use.

The semantic check flagged a hypothesis that both scorers had accepted as legitimately refuted, the same failure mode as the over-cautious refutation rule this skill has already had to walk back once.
A check that punishes a correct refutation cannot be trusted as a gate, whatever it catches elsewhere.

One more thing surfaced on the way: the pilot first called its reference labels human scores, and they were not; the disclosure gap behind that is issue #51, not this record.

## Reopening condition

A person scores 20–30 fresh item-arm points blind to Jev, with the questions and the abstain band frozen first.
If Jev's agreement with that person, outside the band, matches or beats the agent scorer's, whether Jev can carry a first-pass score is worth reopening.
For the semantic check, the condition is a question set that passes the known-legitimate S15 plan and still flags the planted-bad ledger, with neither case used to write it.
A new Jev version reopens nothing by itself; it only resets the calibration.

## Where the rule lives

`jev/README.md` § Rules for using the output.
