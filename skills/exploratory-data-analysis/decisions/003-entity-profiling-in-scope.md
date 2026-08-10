# 003 — An ask that names an entity and wants its story is profile work

Status: accepted, 2026-08-10.

## Context

Two questions, and the second is the one that made this a decision rather than a wording tweak.
Does an ask that names an account, a customer, a branch, or a segment, and wants that entity's story, belong to this skill at all?
And if it does, is a wider description enough to cover it?

### The evidence that raised it

A stratified sample of 150 questions from one internal data agent's traffic was hand-classified by shape.
Ten carried the entity-profiling shape — a named entity, no effect to explain, no claim to check — and none of the ten handed over a dataset.
That is roughly one ask in fifteen arriving in a shape the description did not name.
The corpus is private; it is neither quoted nor committed anywhere in this repo, and no query in `tests/eval/` is drawn from it, paraphrased from it, or modeled on it.
Every eval query is synthetic, over an invented public library system.

### Why a wider description alone was rejected

Before this change, `SKILL.md@a772557` read "Then run Orient exactly as above; the orientation record is the deliverable".
Orient produces schema, grain, provenance, coverage, and missingness — a statement about a table's shape.
An entity narrative is not that artifact.
Widening the trigger alone would have pulled traffic into a route whose stated deliverable does not answer the ask, which is worse than not triggering: the skill would have arrived and then produced the wrong thing.
So the route had to say what an entity profile produces before the description was allowed to claim the ask.

## Decision

Entity profiling is in scope, on the profile route, and the route now states its entity variant.

### The three edits

1. The description names the entity shape and one example phrasing, and adds an entity-shaped counter-example to the exclusion clause.
2. The routing table's `profile` row extends its observable condition to a named entity and names the second deliverable.
3. § Profile Route gains the entity variant: what Frame-lite pins, how Orient's absence-semantics rule applies to an entity, what the entity record is, and that a change over time is reported as a change.

`skills/exploratory-data-analysis/SKILL.md` § Profile Route is the single home for the entity variant.
Nothing here restates it, and nothing else in the repo may.
The boundary against adjudication is not owned here either: the `out: adjudicate` routing row stays authoritative for it, and the description's new counter-example gestures at that row rather than competing with it.

### The measurement

A 50-query synthetic trigger eval (`tests/eval/`), five arms, run against the description in isolation with `skill-creator`'s `run_eval.py`.
Model `claude-opus-5`, `--timeout 390`, `--num-workers 1`, `--runs-per-query 3`, and 0 harness warnings on every run.

| Arm | Baseline | Edited |
| --- | --- | --- |
| P0 (positive control) | 1.000 | 1.000 |
| P1 (entity profiling, the target class) | 0.167 | 0.517 |
| N1 (adjudication-shaped minimal pairs) | 0.000 | 0.000 |
| N2 (bounded descriptive) | 0.000 | 0.000 |
| F (frontier, recorded never scored) | 0.000 | 0.000 |

Gate 1, that the instrument can surface a known positive: P0 baseline 1.000 >= 0.8 — PASS.
Gate 2, that the gap is real: P1 baseline 0.167 <= 0.5 — PASS.
Gate 3, all four conditions: ΔP1 +0.350 >= +0.30; P0 edited 1.000 >= 0.8; N1 edited 0.000 <= 0.2 and ΔN1 0.000 <= +0.10; N2 edited 0.000 <= 0.2 — PASS.
The edit stands; nothing was reverted.

A blind holdout of five entity-profile queries, written after the edit and never seen while it was drafted, scored H = 0.933 unscored against any gate.

### What the P1 movement is, and is not

The obvious confound is lexical memorization.
The edit introduced the phrase "tell me about this account", and 8 of the 20 P1 queries carry a "tell me … about" phrasing.
If ΔP1 were that artifact, those 8 should dominate the movement.
They do not: the 8 overlapping queries moved 0.042 → 0.375 (Δ +0.333), while the 12 non-overlapping ones moved 0.250 → 0.611 (Δ +0.361).
The gain is if anything larger away from the introduced phrasing than on it, which is evidence against a lexical artifact rather than a limitation to disclose.

One N1 entry is less independent than the arm mean suggests.
The description's new counter-example is the phrase "why did this account's spend drop", and N1 carries "Why did this account's spend drop last month?".
That query scored 0.000 at baseline, before the phrase existed, so nothing is circular — but its post-edit 0.000 is not independent evidence that the exclusion clause works.

One P1 query regressed: "Describe the makerspace's usage patterns." moved 0.667 → 0.000.
It is the only P1 member that lost ground; every other query held or improved.
At three runs per query a single query's swing is within noise, and the same entity appears in the holdout at a high rate.
It is recorded because a record that reports only improvements is not trustworthy.

### When to reopen this

Reopen if `hypothesis-driven-analysis`'s description changes so that it claims entity asks more strongly than it does today.
Reopen if a later measurement shows N1 drifting above 0.2 in deployment.

### Limitations

These are the terms on which the numbers above may be read.

1. **The harness measured one skill with no competitors present.**
   `hypothesis-driven-analysis` was not installed during any run, and its description claims "break it down" and "what's driving it" verbatim, so it would contest this class in deployment.
   An ordinary skill roster was present in both arms, but no sibling data-reasoning skill was.
   N1's 0.000 is therefore evidence that this description does not claim adjudication asks, not evidence about which skill wins when both are loaded.
2. **The ten corpus questions are not a single class.**
   P1 models the cleanest sub-shape among them, and the remainder are not represented by any arm.
3. **The edit bundles the entity clause with compression of four existing phrases.**
   The description is at the 1,024-character ceiling — 1,021 characters of YAML source, 1,019 rendered — so the clause could not be added without cutting elsewhere.
   A null result could not have been attributed to the entity clause alone.
4. **All three runs tested the YAML-escaped string, not the rendered one.**
   The harness's `parse_skill_md` strips the outer quotes without unescaping doubled apostrophes, so every arm saw `what''s` where the file renders `what's`.
   This is symmetric across baseline, edited, and holdout, and the escaped string differs from the rendered one only in those two characters, so the Δ comparison holds — but no arm was tested against the description exactly as the shipped file renders it.
5. **P1 edited = 0.517 means roughly half the target class still does not trigger.**
   The edit is a measured improvement, not a solution.
6. **The holdout's 0.933 is weaker evidence of generalization than the raw number suggests.**
   The P1 queries pair an entity with a specific behavioral facet ("hold queue behaviour", "question volume and mix"), some of which skirt the description's own bounded-query exclusion.
   The holdout's five are canonical "full picture / overall story" asks that echo the description's vocabulary directly, which is the easier half of the shape.
   At n = 5, a single 2/3 run moves the mean by 0.067.
   The holdout also reuses P1's own entities — query 1 the Riverside branch and the makerspace, query 2 the large-print collection, query 4 the summer reading program and the Eastside branch — so blind to the edit is not the same as independent of the fixture.

## Consequences

- The profile route now has two deliverables, and the difference between them is stated only in § Profile Route.
  A future edit to that section is the only place the entity variant can change.
- The absence-semantics rule carries more weight than it did: § Profile Route states how it applies to an entity, and `tests/scenarios.md` B10 preregisters that behavior.
- No behavioral arm has run.
  Every number above is a trigger rate — which skill activates — and says nothing about what the route produces once it does.
  B10 is authored, not run.
- `check-citations` covers this file and `tests/scenarios.md`, so the quote above is held against the commit it pins. It does not validate the new Profile Route text's intra-file pointers: a planted `§ Nonexistent Section` reference passes the hook. Section pointers inside `SKILL.md` are held by review only.
- The post-deployment spot check — corpus-shaped queries with all four skills installed, the only test where inter-skill competition is real — is owed and not done.
  `run_eval.py` cannot carry it, because it scores one description in isolation.
  `tests/scenarios.md`'s trigger scenarios can, because they load a catalog carrying both this skill's description and `hypothesis-driven-analysis`'s, and T13 and T14 preregister the entity minimal pair there.
  Those two are authored and unrun, they carry two descriptions rather than four, and their queries are synthetic, so they narrow the debt rather than discharge it.
