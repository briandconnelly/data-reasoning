# Scenario 18 — Trigger discrimination vs a co-loaded analytics skill under the 2026-07-20 description, Rerun

Date: 2026-08-08.
Run: rerun of the owed S18 trigger-discrimination arm, paying Owed-measurements debt 1.
Supersedes `2026-07-20-scenario18-trigger-sonnet-weak.md` and `2026-07-20-scenario18-trigger-opus-strong.md` (the Thirteenth-wave weak/strong arms): both were dispatched 2026-07-20 but, per `tests/scenarios.md`'s own accounting in the "Owed measurements" section, "the two S18 runs are 2026-07-20 but scored the pre-edit text" — the ungated description edit landed the same day, after those runs.
Model: Sonnet, a single rep (not the Thirteenth wave's three-rep weak/strong design).
Catalog (stated, skill not named): analysis (`s18-analytics` stand-in) + hypothesis-driven-analysis + exploratory-data-analysis, per `dispatch-facts.md` — see the catalog-composition deviation note below.
Prompt: Scenario 18's committed prompt ("Weekly checkout conversion dropped from 3.1% to 2.5% (week of 2026-06-01 → week of 2026-06-08). Break it down and tell me what's driving it.").
Fixture: staged copy of `tests/fixtures/s1-conversion/{orders.csv,sessions.csv,deploys.log}`, reached via the `s18-analytics` stand-in's documented paths.

| # | Assertion | Result | Evidence |
| --- | --- | --- | --- |
| 1 | This skill activates from its description even though a data/analytics skill is also offered (transcript shows this skill's file read and followed), rather than the agent using the analytics skill alone. | PASS | Manifest ordinal 1 `Read` of `hypothesis-driven-analysis/SKILL.md` — before any other file is touched, and `skills/analysis/SKILL.md` is never read at all (see fidelity note). Text block 1 (before any tool call): "I'm using the hypothesis-driven-analysis skill: this is a diagnostic \"what's driving the drop\" question about a metric change with multiple plausible explanations, which is exactly its trigger case (not a bounded lookup)." |
| 2 | Once activated, the agent composes rather than defers: it routes **full** for the multi-explanation diagnostic and uses the analytics skill only to reach the data, not as a replacement for the investigation. | PASS | Final answer identifies traffic-mix dilution from `/lp/summer-sale` as the primary driver (with a reweighting check closing ~97% of week 1's level), rules out the 06-10 deploy on timing, and flags an orders-vs-`checkout_reached` discrepancy on 06-13/06-14 as an unresolved data-quality wrinkle — matching Scenario 1's fixture ground truth (composition, deploy red herring, validity trap) and showing no wholesale deferral to a bare data lookup. |

Total: 2/2.

Fidelity note: the arm never read `skills/analysis/SKILL.md` at all (confirmed absent from the manifest) — it reached the raw CSV/log paths directly.
That is consistent with the stand-in's own text, which tells the reader "the harness resolves this to an absolute path per dispatch" for its dataset base, and `dispatch-facts.md` confirms the dispatch included that resolved path.
So assertion 2's "uses the analytics skill only to reach the data" is satisfied in effect — no wholesale deferral occurred, and the data was reached — but not through literal engagement with the analytics skill's file; this is a fidelity observation about *how* this arm reached data, not a defect against the assertion as scored.
Fidelity note: the arm's `ledger.md` was written at manifest ordinal 18, after all four `analyze*.py` writes and their executions (ordinals 10–17) — i.e., after the analysis ran, not before it.
`SKILL.md` states the preregistration rule this bears on (line 170): "Write the investigation ledger to a file from [references/ledger-template.md](references/ledger-template.md) before executing the plan; a ledger that first appears in the final report was not preregistered."
Running `check_prereg.py` against this manifest independently confirms 11 tool_use rows precede the ledger write, most of them the `analyze*.py` scripts themselves rather than orientation (`CLASSIFY`, exit 1; see the evidence artifact).
S18's own assertion table has no preregistration-ordering assertion, so this is not scored as a failure of either assertion above — but it means this run's ledger documents the reasoning after the fact rather than committing to it beforehand, and the final answer's own caveat that the summer-sale finding is "a well-supported hypothesis rather than fully independently confirmed" is consistent with that.
Catalog-composition deviation from the Thirteenth wave (scope note, not a scored finding): this arm's catalog is the current two-skill shipped surface (hypothesis-driven-analysis + exploratory-data-analysis) plus the `s18-analytics` stand-in, whereas the Thirteenth wave's catalog paired hypothesis-driven-analysis directly with the `s18-analytics` stand-in and predates `exploratory-data-analysis`; the S2/S3/S17 arms in this same wave likewise state a visualization-skill-free, two-skill-plus-stand-in catalog where earlier waves' S2/S3/S17 catalogs included a visualization skill (see `tests/runs/artifacts/2026-07-18-scenario17-trigger-evidence.md`'s `pre` arm quote, "not... a visualization request").
See the evidence artifact for the full scope note.
One arm is consistency, not proof; the Thirteenth wave's own 6/6-across-six-reps finding already cautions against reading any small n here as bounding a stochastic deferral rate.
Cost: 18 tool calls; no token figure reached the scoring session (`dispatch-facts.md`), so none is recorded rather than reconstructed.
Evidence: `tests/runs/artifacts/2026-08-08-trigger-rerun-evidence.md`.
