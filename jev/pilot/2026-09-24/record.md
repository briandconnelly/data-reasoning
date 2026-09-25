# Jev pilot, 2026-09-24

Does Jev, asked one typed question per rubric assertion, reproduce the labels this repo's scorer assigned to archived arms, and can it route catalog prompts?
Dispatching session: Claude (Opus 5.5); the blind question set and a critique came from Codex through amicus.

## Reference labels are agent labels

The 49 reference points come from four run records whose scorer is "the dispatching session (Fable)", some corrected on cross-model (Codex) review.
No person scored them.
This pilot first described them as human scores; that was wrong, and the scorer-disclosure gap it exposed is issue #51.
Every agreement figure below is agreement with that agent scorer.

## Design

- Items: 15 assertions from S9, B10, DA-S1, DA-S8, and S22 whose references include both PASS and FAIL where the archive has them (`packet.md`).
  DA-S1.5d was dropped after the fact because its rubric was amended after scoring, so the packet's text no longer matches its reference; 14 items remain.
  DA-S8.4's w3 arm was excluded for the same reason.
- Arms: 25 archived arms from the 2026-09-15 remediation wave and the 2026-09-20 cheap-route wave (`wave.json`).
- Controls: 6 constructed points — S22b's verdict question asked of the S22a arms and S22a's asked of the S22b arms — whose correct answer is FAIL.
- Two question sets:
  - Codex's (`wave.json`), written from `packet.md` alone, told not to open `skills/*/tests/`, and with no pointer to the host's draft.
  - The host's (`questions-in-sample.json`), written after the host had read the reference tables.
    It encodes the scorer's unwritten rules and is in-sample; it is kept as evidence of that and is not a validation.

## Results

Every figure below recomputes from a committed file.
`runs/` holds the per-point outputs of the archived runs, and `runs/README.md` says what each file is and what it cannot show.
Agreement is agreeing points over all 49 reference points; an abstention counts as not agreeing.

| question set | runs | reference agreement | controls | source |
| --- | --- | --- | --- | --- |
| Codex, blind, PASS at p > 0.5 or the named choice | 3–6 | 39, 40, 39, 39 of 49 | 6/6 each run | `runs/run3-both.json` … `runs/run6-both.json` |
| Codex, blind, through `grade.py`, abstain band 0.4–0.6 | one later run | 38 of 49 (8 disagree, 3 abstain) | 6/6 | `grade-report.json` |
| host, in-sample, PASS at p > 0.5 or the named choice | 2–6 | 47, 49, 48, 49, 48 of 49 | 6/6 each run | `runs/run2-host-only.json`, `runs/run3-both.json` … `runs/run6-both.json` |

The host set's figures are not a validation: it was written after reading the reference.
A first run of the host set scored 49 of 49 and was overwritten before it was archived; it is not counted.

Identical requests are not deterministic.
Across the archived runs, a yes/no answer's spread from its lowest to its highest value had a median of 0.01 and a maximum of 0.11 (DA-S8.4 on the post arm, 0.47–0.58 from the Codex set), enough to flip a point near 0.5; that is why `grade.py` has an abstain band.
A full pass over 25 arms cost about 80k input tokens.

## The disagreements

The host and Codex read the ten misses of the Codex set's run 3 separately and did not fully agree.

- Genuine Jev errors, by both readings: S9.4b pre (accepted a randomization caveat as a completeness statement), DA-S1.5a post (missed annotations after the sentinel), and DA-S8.4 on w2 (accepted "the crossover falls inside both ranges" as stating the loss crossover).
- Question or rubric scope: B10.5b on three arms — the rubric text says "states that billed volume fell", the scorer required "stated as a change", and Codex's question tested the former; B10.5c pre — the question looked only in the written file, where the handoff is in the final answer.
- Disputed: DA-S8.2 pre, where Jev said no at 0.21 against a PASS reference.
  Codex read it as a Jev error; the host checked the record, whose evidence row cites "S2: 20 past canary rollouts, quota-drawn" and never names `reference_class.csv`, which the question requires by name.
  Read literally, Jev is right and the reference accepted a source id in place of the filename.
- Lenient reference: S9.4a pre, scored PASS while its own evidence cell says "field population not stated".

## Routing probe

`routing.md`: 60 standalone catalog prompts against the frozen descriptions.
Most prompts Jev sends away from their own catalog are that catalog's planted non-trigger or cross-route cases, but no labels file exists, so no accuracy is claimed.
Nine prompts fall below 0.75 confidence in the committed run, against eight in an earlier run that was not kept; the set shifts near the threshold, and its members are candidates for real agent arms, not a fixed list.

## Semantic check

On the S15 post arm's plan-time ledger, the check flags H4 (p≈0.34), a data-artifact hypothesis both scorers accepted as legitimately refuted, and the stop condition (p≈0.35), and flags H1 (p≈0.34), arguably fairly.
It flags a planted-bad ledger as it should.
The question was not reworded to pass the known case, since tuning on the one known negative would repeat the host set's in-sample problem.

## What this does not show

- Agreement with a person: no human labels exist for these points.
- Out-of-sample agreement: the Codex set was blind to the labels, but the items and arms were chosen by someone who had read them.
- Anything about models other than `jev-1.13.0`.

The next honest estimate: a person scores 20–30 fresh item-arm points blind to Jev, the question set is frozen first, and the abstain band is fixed in advance.
