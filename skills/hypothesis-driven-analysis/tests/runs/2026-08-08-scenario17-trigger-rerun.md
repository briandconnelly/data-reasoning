# Scenario 17 — Trigger reach under the 2026-07-20 description, Rerun

Date: 2026-08-08.
Run: rerun of the owed S17 trigger-discrimination arm, paying Owed-measurements debt 1.
Supersedes `2026-07-18-scenario17-trigger-finaldesc.md` and the Ninth-wave `-pre`/`-post-a`/`-post-b`/`-post-para` arms, all of which scored descriptions predating the 2026-07-20 ungated edit that the S18 section of `tests/scenarios.md` says supersedes the recorded S2, S3, S17, and S18 runs.
Model: Sonnet.
Catalog (stated, skill not named): hypothesis-driven-analysis + exploratory-data-analysis + systematic-debugging, per `dispatch-facts.md`.
Prompt: Scenario 11's claim ("Someone claims our checkout p95 latency exceeded 500ms yesterday (2026-07-15). Is that claim true?"), per S17's definition (S11's prompt with the catalog stated and the skill not named).
Fixture: staged copy of `tests/fixtures/s11-mini/checkout_latency.csv`, sha256 `eea96d9793a56153d23f7412a1cebbba2ac0fb2eadd0acb4f1b9a41650a8523c` (matches the recorded value in the 2026-07-18 S17 evidence artifact).

| # | Assertion | Result | Evidence |
| --- | --- | --- | --- |
| 1 | The skill activates from its description alone (transcript shows the skill file read and followed). | PASS | Manifest ordinal 2 `Read` of `hypothesis-driven-analysis/SKILL.md`, ordinal 3 `Read` of `references/ledger-template.md`, both before any data touch; text block 1 (before any tool call): "This is a stated claim needing adjudication (\"p95 exceeded 500ms yesterday\") — the exact example in hypothesis-driven-analysis's trigger description. I'll load that skill." |
| 2 | Once loaded, routes **mini** and answers correctly that the claim is false (consistent with S11). | PASS | Final text block is a one-paragraph mini ledger (claim, prediction, probe, stop condition, outcome); outcome `CONTRADICTED`, inside the mini template's closed set; verdict: "The claim is false for the ~20 hours of checkout traffic actually captured (p95 ≈ 392ms, nowhere near 500ms threshold, with a tight CI)."; matches Scenario 11's fixture ground truth (realized p95 ≈ 392ms, claim false). |

Total: 2/2.

Fidelity note: manifest ordinal 1 is an errored `Skill` tool call — the arm tried the harness's registered-skill-invocation tool before reading any file.
Text block 2 explains the recovery: "The Skill tool doesn't recognize that name (it's a path-based catalog, not a registered skill). I'll read the SKILL.md directly to follow its procedure."
The subsequent `SKILL.md`/`ledger-template.md` reads (ordinals 2–3) are unaffected, so this is recorded as a fidelity note rather than scored against assertion 1, which asks only whether the skill file was read and followed — it was.
Fidelity note: the arm flagged an unresolved 20-of-24-hour coverage gap in the fixture as a residual caveat on its "claim is false" verdict, consistent with prior S17 arms' documented coverage limitation.
One arm is consistency, not proof, that the 2026-07-20 wording preserved trigger reach.
Cost: 7 tool calls; no token figure reached the scoring session (`dispatch-facts.md`), so none is recorded rather than reconstructed.
Evidence: `tests/runs/artifacts/2026-08-08-trigger-rerun-evidence.md`.
