# 005 — Generic speech acts claimed, with measured gain and cost

Status: accepted, 2026-08-18.
Disposes of issue #17.

## Context

Decision 004 measured that the shipped description triggers on `Profile X.` far more than on generic phrasings of the same request — `Tell me about X.`, `Give me an overview of X.`, `Give me a rundown on X.` — and named that gap as the thing a future widening would need to beat.
Issue #17 asked for that widening.
A preregistration, `tests/eval/2026-08-15-widening-prereg.md`, fixed the screening rule, the confirmatory gates, and the ship discipline before any arm of this wave ran.
This record states what the wave settled; the screening decision and the gate notes hold the numbers and are not restated here beyond what the wave's own decision rules require.

## Decision

Two edits shipped, in the order the prereg required: a compression, then the widening.

### The compression (arm B)

Commit `cd5d2b6` dropped the lead-purpose clause `, to confirm, never to conclude from`, shrinking the shipped description to 983 characters to free budget for the widening edit.
Gate 1 (`AvB-gate1.md`) measured this compression against the shipped description (arm A) on the fresh crossed-pair fixture and the cost arms, and found it a null everywhere it could bite: every per-speech-act contrast interval and the pooled generic contrast interval included zero, and the N1 and N2 change intervals included zero.
**VERDICT: PASS.**
The compression buys space without measurably changing triggering behaviour in either direction.

### The widening (arm C3)

Three candidates were screened against the shipped description on the ceiling-probe subset (`screening-decision.md`), 2 runs per query per arm, pooled generic rate as the ranking statistic:

- C1: shipped 0.2083, C1 0.3750, delta +0.1667.
- C2: shipped 0.1667, C2 0.5000, delta +0.3333.
- C3: shipped 0.1250, C3 0.5417, delta +0.4167.

Per the prereg's winner rule (highest pooled generic rate, ties broken toward fewer edits against B), C3 won outright with no tie to break, and its delta against its own pair's shipped arm (+0.4167) cleared the 0.25 proceed threshold.
C3 went forward as arm C into the confirmatory wave.

Commit `4c72ca2` applied C3 to the shipped description, at 1021 characters.
The confirmatory wave ran three gates against it, all on the fresh crossed-pair fixture and the cost arms, 3 runs per query per arm:

- **Gate 2 — gain (B vs C3).** Pooled generic rate rose from 0.0667 (baseline/B) to 0.5778 (treatment/C3), meeting the >= 0.5 floor; the pooled generic lift interval was [+0.2889, +0.7333], excluding zero (`BvC-gates.md`).
  **VERDICT: PASS.**
- **Gate 3 — cost (B vs C3).** The N1 change interval was [0, +0.1333] and the N2 change interval was [0, 0]; both included zero, as required (`BvC-gates.md`).
  **VERDICT: PASS.**
- **Gate 4 — seam.** `run_trigger.py` T13 routed 5/5 to `exploratory-data-analysis` and T14 routed 5/5 to `hypothesis-driven-analysis` under C3 (`seam-gate4.md`).
  **VERDICT: PASS.**

Gate 1 (the compression's null result, above) also had to pass before the confirmatory wave could proceed, and did.
All four gates passed, so both commits shipped per the prereg's ship rule.

## Order diagnostics

Recorded per the prereg, not gating.

Gate 1's fresh fixture: run-order means moved by up to 0.05 across the three runs, and baseline/treatment-first splits differed by up to 0.0833 (`AvB-gate1.md`) — consistent with a null, no directional order effect evident.
Gate 1's cost arms: by-run and by-which-first rates matched or nearly matched across splits (`AvB-gate1.md`).
Gates 2/3's fresh fixture: treatment triggered substantially more than baseline in every run and under both orderings — baseline-first 0.2000 vs 0.6000, treatment-first 0.3167 vs 0.7667 (`BvC-gates.md`) — consistent with a genuine treatment effect rather than an order artifact.
Gates 2/3's cost arms: the small treatment-arm bump (2/96 invocations) was order-independent (`BvC-gates.md`).
The screening pairs (C1/C2/C3) each showed baseline-first vs treatment-first splits differing by as much as 0.25–0.31 (`screening-decision.md`), a reminder from decision 004 that position effects at screening scale are the same order of magnitude as effects worth detecting, and why the confirmatory wave counterbalanced and reported order diagnostics on every comparison.

## These rates supersede 004's table as the baseline

Decision 004's per-speech-act table (`profile` 0.833, `overview` 0.100, `tell-me-about` 0.133, `rundown` 0.033) was measured under the shipped 2026-08-11 description and was the baseline that record said a widening must beat.
That widening has now run.
The pooled generic rate under the shipped description, remeasured in this wave's fresh fixture, was 0.0667 (Gate 2/3, `BvC-gates.md`); under C3 it is 0.5778, lift interval [+0.2889, +0.7333].
Any future widening work measures against C3's rates and this wave's crossed-pair instrument (`crossed-pairs-2026-08-15.json`), not against 004's table.

## Limits

The wave measured one domain per fixture: an invented municipal transit agency, ten entity-facet bases, in the confirmatory fixture (`crossed-pairs-2026-08-15.md`).
It did not test domain generality beyond that, per the prereg's "Not measured by this wave" section.
It measured triggering only, not downstream behaviour; decision 004's recorded limitation — no behavioural arm has ever run for this skill — still stands.
C3 is the two-edit candidate: it combines an activity-naming opening with a phrasing-does-not-matter clause replacing part of the exemplar list, per `candidates-2026-08-15.md`.
**Which of these two mechanisms carries the measured lift is unmeasured**; the prereg named this attribution gap before the wave ran and it was not closed.
The seam instrument (`run_trigger.py`) reads the main checkout's `SKILL.md` at a hardcoded path (`REPO = Path("/Users/bdc/projects/data-reasoning")`, line 26), not the worktree's copy, regardless of the harness's own working directory.
Gate 4's first attempt missed this and measured the shipped description, not C3; the correction, the evidence, and the re-run against the main checkout are documented in `seam-gate4.md`'s correction section.
The four-skill deployment check remains owed, per decision 003's statement of that debt, unchanged by this wave.

## When to reopen

- If a follow-up further widens the description, this record's rates (pooled generic 0.5778 under C3) are the baseline it must beat, and `crossed-pairs-2026-08-15.json` is the instrument.
- If anyone wants to know which of C3's two mechanisms drives the lift, that requires a new crossed comparison isolating them; this wave did not run one.
- If `hypothesis-driven-analysis`'s description changes so that it claims entity asks more strongly, the seam results here become stale, as decision 004 already noted for its own seam results.
