# Scenario 2 — Non-trigger guard under the 2026-07-20 description, Rerun

Date: 2026-08-08.
Run: rerun of the owed S2 trigger-discrimination arm, paying Owed-measurements debt 1.
The 2026-07-20 ungated description edit (adding "break it down" as a quoted diagnostic trigger, among other changes) superseded every prior S2/S3/S17/S18 run, per the S18 section of `tests/scenarios.md` ("It supersedes the recorded S2, S3, S17, and S18 runs, which all scored the old description and must be re-run").
This run supersedes `2026-07-18-scenario2-trigger-finaldesc.md` and `2026-07-18-scenario2-trigger-postdesc.md`, both of which scored pre-2026-07-20 wording.
Model: Sonnet.
Catalog (stated, skill not named): hypothesis-driven-analysis + exploratory-data-analysis + systematic-debugging — the current two-skill shipped surface plus a debugging stand-in, per `dispatch-facts.md`.
Prompt: Scenario 2's bare median question.
Fixture: staged copy of `tests/fixtures/s1-conversion/orders.csv`, sha256 `39486b25560ac523af351bf4376d1fe9e4c8d2c267c63b95e7e9fa7b1ada1ddc` (matches the recorded value in the 2026-07-18 S17 evidence artifact).

| # | Assertion | Result | Evidence |
| --- | --- | --- | --- |
| 1 | Routes direct: computes the median and answers. | PASS | Manifest ordinal 1 `Bash` (`cat -A`/`head`/`wc -l`), ordinal 2 `Read` of `orders.csv`, ordinal 3 `Bash` (python median computation); final text block: "The median order value in June was **$76.36**, based on all 268 orders in the file (all timestamps fall in June 2026)." |
| 2 | No ledger, no hypothesis language, no PPDAC ceremony. | PASS | Zero `Write`/`Edit`/`NotebookEdit` rows in the manifest (machine-checked, planted positive validated — see evidence artifact); no `Read` of `hypothesis-driven-analysis/SKILL.md` anywhere in the manifest. |

Total: 2/2.

Verbatim skill-selection sentence (text block 1, before any tool call): "No skill needed — this is a bounded descriptive query (compute a median from given data), not a hypothesis to test or open-ended exploration."
Fidelity note: unlike the two 2026-07-18 probes (`-finaldesc` stated its choice only in the opening block after the fact was recoverable, `-postdesc` likewise), this arm placed its skill-choice statement before its first tool call as instructed — no placement drift to record here.
One arm is consistency, not proof, that the guard held under the 2026-07-20 wording.
Cost: 3 tool calls; 33,154 subagent tokens (harness-reported, `dispatch-facts.md`).
Evidence: `tests/runs/artifacts/2026-08-08-trigger-rerun-evidence.md`.
