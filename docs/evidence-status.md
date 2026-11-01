# Evidence status

What this plugin's skills claim versus what has been measured, as of the dates named below.
This page carries the measurement status that the README used to; the decision records and run records it cites remain the authorities.

## Handoffs and routing

Exploration generates hypotheses and never confirms them; adjudication is `hypothesis-driven-analysis`'s work; `causal-identification-review` is the constructive continuation when adjudication concludes nothing identifies the effect, or when a claimed design needs its identifying assumptions checked before anyone trusts it.
`decision-analysis` is the constructive continuation when a decision hangs on what an investigation left `UNRESOLVED`: it consumes ledgers and review records as evidence, and its verdicts recommend without authorizing.
All four skills carry the same authorization gate; its text lives once in `scripts/shared-sections/authorization-gate.md` and is rendered into each skill by `scripts/check-shared-sections.py`, which fails when a rendered copy drifts or is hidden.
Paths under `tests/`, `scripts/`, and `jev/` in these records refer to the development repository (<https://github.com/briandconnelly/data-reasoning>); an installed plugin does not carry them.

The handoff from exploration to hypothesis-driven analysis is a design claim, not a measured one.
Who scored each measured result, and what an unlabelled record is presumed to be, is disclosed per `skills/hypothesis-driven-analysis/tests/PROTOCOL.md` § Who scored it.
`hypothesis-driven-analysis` has an archived scenario suite behind it (`skills/hypothesis-driven-analysis/tests/`).
`exploratory-data-analysis` has measured description-trigger arms only (`skills/exploratory-data-analysis/tests/runs/2026-08-11-t13-trigger.md`, `skills/exploratory-data-analysis/tests/runs/2026-08-11-t14-trigger.md`, and the repaired rerun; the lift is recorded in `skills/exploratory-data-analysis/decisions/005-generic-speech-acts-claimed.md`); its behavior scenarios in `tests/scenarios.md` are authored and unrun.
No run has yet exercised that handoff.
Per `skills/hypothesis-driven-analysis/tests/scenarios.md` § "Owed measurements as of 2026-08-08", `hypothesis-driven-analysis`'s description was re-validated on 2026-08-08 against the then two-skill shipped surface plus a `systematic-debugging` stand-in, not the four skills that now ship.
`causal-identification-review`'s description has n=1 trigger cells (CS1, CS2, CS6a) against a three-skill catalog; `decision-analysis`'s has none.
Routing between all four skills rests on zero arms run against the full catalog — the freeze in `skills/exploratory-data-analysis/decisions/006-description-freeze-until-measured.md` holds every description until that changes.
Treat the routing between them, and the handoff itself, as unverified.
`causal-identification-review`'s measurement wave 1 (n=1 per cell) was scored on 2026-08-09 and then partly reopened the same day: CS4 and CS7 moved to "redesign and re-measure" and owe fresh arms before the wave is complete (`skills/causal-identification-review/tests/scenarios.md` § "Global verdict table", addendum).
`decision-analysis`'s original scenarios remain unrun (`skills/decision-analysis/tests/scenarios.md`); focused VoI wording checks are recorded in `skills/decision-analysis/tests/runs/2026-09-04-voi-pricing.md`, with no observed behavioral lift over the old wording for the archived input snapshots.
Treat its routing and its premium as unmeasured.

## Owed evidence

Three pieces of evidence are owed and not started, named here so the gap is not mistaken for an oversight (external review, 2026-09-15):

- An end-to-end integration suite for the shipped four-skill workflow, on both hosts: a direct answer that loads no skill, exploration handing a lead to adjudication, adjudication handing a dead end to identification review, and an `UNRESOLVED` ledger entering a decision record.
  Every arm run so far exercises one skill in isolation; none shows an agent choosing the right skill, keeping the evidence boundary across a handoff, or finishing the user's task.
- A frozen representative suite kept alongside the adversarial catalogs.
  The catalogs' rule that a baseline already passing means the scenario is too easy finds failures; it cannot estimate practical benefit, because ordinary tasks a baseline already handles still pay the skill's context and ceremony.
  The representative suite keeps such tasks, and scores accuracy, unnecessary ceremony, latency, and total context cost.
- Measured simplification experiments: the repository's checkers preserve wording and provenance, but nothing yet establishes whether each accumulated rule still earns its context cost.

## Remediation wave of 2026-09-15

The skill wording this remediation changed was measured on 2026-09-15 on the cells that reach it, with a baseline arm, a pre-edit arm, and a post-edit arm per cell (`skills/hypothesis-driven-analysis/tests/runs/artifacts/2026-09-15-remediation-wave-prereg.md` § Results).
Two sentences reached behavior — the estimation route's data-validity inheritance, and (after one revision and a second wave) the profile route's rule that a record names each change with its date; the exploration degraded mode's Frame-lite naming did not change behavior at n=1 and stays as a clarification carrying no measured claim; the decision-analysis degraded mode for a missing prior and its verdict-precedence paragraph each failed a preregistered condition and were withdrawn, so the review's finding 7 and A2 remain owed.
The run records say which is which, with the owner's decision on each.

## Context cost

The scenario measurements count the procedure, not the prose: loading a skill has a fixed context cost the scenario arms do not meter.
As of 2026-09-15, after the remediation's final state (`wc -w skills/*/SKILL.md skills/*/references/*.md`): `hypothesis-driven-analysis` is 6,419 words plus a 3,180-word ledger template and a 700-word subagent brief; `decision-analysis` is 3,227 plus an 897-word template (the template grew by its slot notes); `causal-identification-review` is 2,440 plus 492; `exploratory-data-analysis` is 2,540 plus 843.
Co-loading two skills — the designed handoff case — pays the verbatim authorization gate (~350 words) and a near-duplicate costly-collection section once per skill loaded.
Reducing that duplication means extracting the shared contract, which edits `hypothesis-driven-analysis` and is deferred on the terms in `skills/exploratory-data-analysis/decisions/001-shared-gate-authority.md` § Consequences.
