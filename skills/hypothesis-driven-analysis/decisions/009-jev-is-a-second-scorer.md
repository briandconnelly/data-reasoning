# 009 — Jev is a second scorer, not a scorer

Decided 2026-09-24.

## Question

Every scored claim in this repo rests on one agent reading archived arms, sometimes corrected by a second model's review, and the representative suite and n≥5 cells stay unpaid partly because that reading is expensive.
TypeSafe's Jev answers narrow typed questions cheaply.
Should it score arms, route prompts, or check ledgers, and on what terms?

## What was decided

**Jev was adopted as optional development tooling beside the existing scorer, in the role of a second scorer.**
It lives in `jev/`, outside the release tree and outside every skill, hook, and instrument.
The terms on which its output may be used are not stated here; they live where the pointer below says.

## Positions

*Use Jev as the grader, and make n≥5 per cell affordable.* This was the proposal's first idea, and it is what the cost argues for.
The pilot does not support it: blind questions agreed with the agent scorer on 39–40 of 49 points, and about half the misses were Jev reading errors, not rubric problems.

*Put a routing hint in a hook.* It would bypass the frozen descriptions without ever measuring them.
It also sends user prompts to a third party from inside the plugin, and hook output is agent-read prose, which under decision 006 owes measured arms.
Declined outright, and not built.

*Add a `--semantic` mode to `instruments/check_record.py`.* Decision 006 keeps the instrument stdlib-only and fixture-neutral, and a network call inside the live hook's validator breaks the first and makes "not checked" a routine hook outcome.
Built instead as a separate script that nothing imports.

*Second scorer.* Adopted.
It keeps the part of the proposal the pilot supports — a cheap, independent-of-Claude reading whose disagreements point a person at arms worth rereading — and nothing the pilot contradicts.

## What settled it

The pilot (`jev/pilot/2026-09-24/record.md`), in three results.

The honest agreement figure was 39–40 of 49 over four runs against an agent reference, from questions written blind to it; the near-perfect figure came from questions written after reading the reference, which measures the author's hindsight, not Jev.
That rules out a sole scorer.

About half of the blind set's ten misses in its first archived run were not Jev errors: they were a rubric whose text did not say what its scorer required, a question that looked in the wrong place, and a reference that accepted less than its rubric asked.
A second reading that surfaces those is useful even at 80% agreement, provided a person decides each disagreement.
The pilot did not show that Jev's uncertain answers track the scorer's own mistakes; an earlier draft of this record said so from an unarchived run, and the archived runs do not support it.

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
