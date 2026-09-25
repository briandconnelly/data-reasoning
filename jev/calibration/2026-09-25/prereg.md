# Jev calibration against a person, preregistration

Written 2026-09-25, before any person scored a point, before any Jev question in this directory was asked of any run, and before the label-to-run mapping below was shown to the scorer.
It tests the reopening condition in `skills/hypothesis-driven-analysis/decisions/009-jev-is-a-second-scorer.md`.
Once the scorer starts, nothing in this file changes; anything learned after that goes in `results.md`, dated, beside this file.

## Question

Outside its abstain band, does Jev agree with a person as often as the agent scorer does, on points neither was tuned on?

## Sample, fixed by rule

- Source: the 2026-09-20 cheap-route wave, `skills/hypothesis-driven-analysis/tests/runs/artifacts/2026-09-20-cheap-route-validity/`, whose arms have archived transcripts and written files.
- Cells: S2, S9, S11, S13, S14, each with its `pre` and `post` arm, so 10 runs.
- Excluded cells: S22, whose items the 2026-09-24 pilot graded; S15, whose ledgers the dispatching session read closely while building `jev/semantic_check.py`; the canary arms, which are fixture validation.
- Items: each cell's catalog assertions in `skills/hypothesis-driven-analysis/tests/scenarios.md`, minus any that needs the order of the agent's tool calls, which the evidence below does not contain: S14.2 (plan written before the first metered query) and S14.4 (no re-pull) are out.
  S9.4a and S9.4b are out because the pilot graded them.
- That part of the sample is 13 items over 10 runs, 26 points.

What the dispatching session knew when it wrote that rule: the wave's own run record (`skills/hypothesis-driven-analysis/tests/runs/2026-09-20-scenario22-cheap-route-validity.md` § Regression cells), read on 2026-09-24, scores those 26 points PASS except S2.2 on one S2 arm.
An always-PASS grader would therefore agree with the agent scorer on 25 of 26, and a test built on those points alone could barely tell two scorers apart.
So, before any question was asked of any run and before anyone scored, the sample was widened by a second rule, chosen by the repo owner over two alternatives (adding only an S9 no-skill run, or keeping 26 points):

- Source: the no-skill baseline arms of the 2026-09-15 remediation wave, `skills/hypothesis-driven-analysis/tests/runs/artifacts/2026-09-15-remediation-wave/`: `da-s1-baseline`, `da-s8-baseline`, and `b10-baseline`.
  The agent scorer failed most of their catalog items, which is why they were chosen; the choice is by arm, not by point.
- Items: each cell's catalog assertions minus any the pilot graded (DA-S1.5a–e, DA-S8.2, DA-S8.4, B10.5a–c), any that needs a checker script (DA-S1.1 and DA-S8.1, which require `check_decision.py`), and any whose check needs arithmetic recomputed (DA-S1.3): DA-S1.2, DA-S1.4, DA-S8.3, and B10.1–B10.4.
  Arithmetic is excluded because it belongs in code for either scorer, not because Jev is weak at it.
- These runs had no skill loaded, so `packet.md` gives them one reading rule — content that does the named job passes whatever it is headed — and the definitions their items use.

The full sample is 20 items over 13 runs, 33 points; `packet.md` lists them with their text.

## Evidence both scorers see

For each run, the same three fields: the prompt the agent received, its final answer, and every file it wrote that decodes as text (`jev/grade.py` `arm_state`).
Every string is redacted with `arm-[A-Za-z0-9_-]+` → `arm-run`, because the harness writes the arm's name, including `pre` or `post`, into its paths.
The person reads this evidence in a scoring sheet, and Jev reads it as its state; neither sees transcripts beyond it.

## Blinding

- Runs are labelled A–M in a shuffled order.
  The mapping is withheld from the scorer until scoring ends; its sha256, over the file's bytes including a trailing newline, is `bd275bb54c6d2afe699bf76dc9487bfc79edae77a046957c7a9ef153d95e9eb0`, and the file is committed with the results so the hash can be checked.
- The person does not see Jev's answers, the agent scorer's labels, or the wave's run record while scoring.
- The person scores in a private claude.ai page built from the same redacted evidence, which stores each label in the page's own database; the labels are exported to `human-labels.json` and committed before Jev runs.
- Jev is not asked any question in `wave.json` until the person's labels are committed.

## Questions and pass rule

- The Jev questions are Codex's, written from `packet.md`'s rubric alone under an instruction not to open `skills/*/tests/` or `jev/`, and committed as `questions-codex-raw.json` (the 13 items of the first rule) and `questions-codex-raw-baselines.json` (the 7 of the second), and in `wave.json`, with this file.
  The first set took three requests: the first returned no questions because Codex counted the items as 12 and would not guess the thirteenth, and the second none because the requested reply shape conflicted with the consult tool's response schema; neither returned any question text, so neither shaped the set.
  The dispatching session does not edit the questions; a defect found later is reported in `results.md`, not repaired.
- Model `jev-1.13.0`; abstain band 0.4–0.6 on p(pass): above 0.6 is PASS, below 0.4 is FAIL, anything between is an abstention.
- One run of Jev over the 33 points is the scored run.
  Three more identical runs are made afterwards and reported only as a stability check: they cannot replace the scored run.

## Analysis, fixed now

The person's labels are the reference for everything below.

1. **Jev, outside the band**: agreements over the points Jev did not abstain on, with that denominator stated.
2. **Jev, all points**: agreements over all 33, counting an abstention as not agreeing.
3. **Agent scorer**: agreements over all 33, using the labels in the two waves' run records (the 2026-09-20 record's § Regression cells and its S2 note; the 2026-09-15 DA and B10 records' baseline columns), transcribed into `agent-labels.json` after the person's labels are committed.
4. **Always PASS**: agreements over all 33 for a grader that marks every point PASS.
   This is the floor: a figure at or below it shows nothing, because the sample is mostly PASS.
5. Abstentions: count and list.
6. Every point where Jev and the person disagree, and every point where the agent scorer and the person disagree, listed with the item text and a one-line reading of the evidence.

**Decision rule.** The reopening condition is met when all three hold:

- (1) is at least (3);
- (1) exceeds (4);
- Jev abstains on at most 11 of the 33 points, so a high rate outside the band cannot come from abstaining on the hard ones.

If it is met, decision 009 is reopened on whether Jev can carry a first-pass score; if not, the decision stands.
Either way, the result is recorded in `results.md` and in decision 009's reopening condition, with this caveat attached: 33 points from two waves cannot separate two scorers that differ by one or two points, so a difference that small is reported as no difference.

## What this does not test

- Jev on material with many more FAILs than the seven or so the baseline runs contribute.
- Items that need the tool-call order.
- The semantic check, which has its own reopening condition.
- Any model other than `jev-1.13.0`.
