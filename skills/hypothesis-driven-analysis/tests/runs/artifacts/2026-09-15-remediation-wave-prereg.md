# Preregistration: 2026-09-15 remediation wave

Written before any arm ran.
This wave measures the agent-read wording that the 2026-09-15 external-review remediation changed, on the cells whose decision points traverse it, per `../../PROTOCOL.md` § What owes a rerun.
It is the PROTOCOL step 1 artifact for every cell below; the step 2 entanglement pass, the step 3 design review, and the step 4 canary rule are recorded here too, so the scored runs can point at one document.

## What changed, and which cells reach it

| Change | File and section | Cells that reach it | Cells that do not |
| --- | --- | --- | --- |
| Estimation route inherits the coverage matrix (§ Plan) and completeness semantics and confound check (§ Analysis); randomization identifies assignment, not the analysis population | `hypothesis-driven-analysis/SKILL.md` § Estimation Route | S9 | every `full`, `mini`, `direct` scenario |
| Degraded mode for no defensible prior or likelihood ratio, with worked example | `decision-analysis/SKILL.md` § Degraded Modes | DA-S1, DA-S3 | DA-S4..S7 (no update sequence, or a different route) |
| Precedence when both sensitivities fire: `prior-sensitive`, loss crossover in Conditions | `decision-analysis/SKILL.md` § Verdict | DA-S3 | DA-S1 (losses elicited, so only the prior flips) |
| Profile route separates dated sequence (recorded) from attribution (unresolved, handed off) | `exploratory-data-analysis/SKILL.md` § Profile Route | B10 | B1..B9 (explore route) |
| No-file-tools degraded mode names Frame-lite on the profile route | `exploratory-data-analysis/SKILL.md` § Degraded Modes | B10-nofile (a with-skill arm with Read, Glob, Grep only) | every arm with file tools |
| Data rules as four bullets; authorization-gate rationale relabelled | EDA § Data Rules; the shared gate in all four skills | none — same obligations, same words | all |

The scorer for the decision-analysis cells, `decision-analysis/tests/check_decision.py`, licensed only `none needed` in the belief slots before this wave.
It now licenses the degraded mode's `none supported — see Robustness` sentinel and a `none supported` evidence row, with tests; without that, an arm following the skill would fail the skill's own checker, and the cell would score the checker rather than the wording.

## Harness

Every arm is one `claude -p` subprocess run by `../../run_arm.py`, model `sonnet` (resolved model recorded per arm), `--setting-sources project` so the machine's installed release of this plugin and its hook are absent, cwd a scratch directory outside the repo, tools Read/Write/Edit/Bash/Glob/Grep (B10-nofile: Read/Glob/Grep).
A with-skill arm is told the SKILL.md path in this working tree and to follow it; a baseline arm is told nothing about skills.
Both are forbidden to read any `tests/` tree other than the named fixture, and are told their final message is the report.
The frame is verbatim in `run_arm.py`; each arm's exact prompt, transcript, tool manifest, files written, and the sha256 of the prompt, transcript, skill file, and every fixture file are archived under `2026-09-15-remediation-wave/`.
The catalog prompts are used verbatim with the fixture path made absolute (`2026-09-15-remediation-wave/prompts/`).
Scorer: the dispatching session (Fable), against the assertions below, with every quote grepped against the archived transcript or written file before it is cited.

## Cells

| Cell | Skill | Arms | Fixture | Catalog assertions | Added assertion (the changed sentence) |
| --- | --- | --- | --- | --- | --- |
| S9 | hypothesis-driven-analysis | baseline, with-skill | `s9-ab/signups.csv` (existing) | S9.1–S9.3 | S9.4 |
| DA-S1 | decision-analysis | baseline, with-skill | `da-s1-ledger/` (new, validated) | DA-S1.1–S1.4 | DA-S1.5 |
| DA-S3 | decision-analysis | baseline, with-skill | `da-s1-ledger/` | DA-S3.1–S3.2 | DA-S3.3 |
| B10 | exploratory-data-analysis | baseline, with-skill | `b10-entity/` (new, validated) | B10.1–B10.4 | B10.5 |
| B10-nofile | exploratory-data-analysis | with-skill, Read/Glob/Grep only | `b10-entity/` | B10.1, B10.4 | B10.6 |

Added assertions, each checkable from the archived output:

- **S9.4** — the report records the analysis population's coverage (both variants present on all 14 days, visits and signups populated) and what an absent day or unrecorded visitor would mean for the estimate, as the changed sentence requires; an interval alone does not satisfy it.
- **DA-S1.5** — with no elicited prior, Prior odds and Posterior odds read `none supported — see Robustness`; the reference-class ratio (9/10 vs 2/10, LR 4.5) stays in the Evidence table as `estimated-from-data-in-hand` naming `reference_class.csv`, the 20-rollout class, and the 40 ms gap condition; Robustness sweeps a `sensitivity-only` prior class applying that ratio and reports the prior-odds crossover (threshold 0.1 ÷ 4.5 ≈ 0.022); the verdict is `prior-sensitive` and Recommended action reads `returned to owner`.
  The record passes `check_decision.py` and `instruments/check_record.py --final`.
- **DA-S3.3** — with neither prior nor losses supplied, both sensitivities fire; the verdict is `prior-sensitive`, Conditions states the loss-ratio crossover as well, and Recommended action reads `returned to owner`.
  DA-S3's own assertion "at most `loss-sensitive`" is read as "a sensitive verdict, not `robust`"; the precedence rule decides which label, and DA-S3.3 scores that.
- **B10.5** — the entity record states both dated events — plan changed to `enterprise-annual` in 2026-03, billed volume fell from 2026-04 — as facts with their dates.
  B10.4 already forbids attributing one to the other; B10.5 is the other half of the changed sentence, that dated sequence is recorded rather than suppressed.
- **B10.6** — with no file tools, Frame-lite (entity, identifier, sources, timeframe, budget; no reservation) appears as response text before any exploration output, and the response says the precommitment is only as strong as the visible message order.

## Expected outcomes

- S9: baseline passes S9.2–S9.3, fails S9.1 on the threshold (as in 2026-07-16), and fails S9.4; with-skill passes all four.
  At-risk: with-skill reads the pointer and records coverage as a one-line aside without saying what absence would mean, which fails S9.4's second half.
- DA-S1: baseline gives a recommendation with an invented confidence number and no record; with-skill passes DA-S1.1–S1.5.
  At-risk: with-skill invents a prior (`sensitivity-only` or elicited from nothing) and puts it in Evidence and update, failing DA-S1.5 and the checker; or drops the sourced ratio because the prior is missing.
- DA-S3: baseline decides unconditionally; with-skill passes DA-S3.1–S3.3.
  At-risk: with-skill labels the verdict `loss-sensitive` (losses are the more salient gap) and omits the prior crossover, failing DA-S3.3; or treats the ledger's H1 as a claim to re-adjudicate.
- B10: baseline profiles the whole file, reads both empty months as inactivity, and attributes the drop to the plan change; with-skill passes B10.1–B10.5.
  At-risk: with-skill suppresses the sequence entirely to stay clear of attribution, failing B10.5 — the failure the changed sentence exists to prevent.
- B10-nofile: with-skill emits Frame-lite in the response before reading files.
  At-risk: it emits the explore route's Frame with a reservation, or emits nothing before its first Read.

## Reachable verdicts (every row written before any arm ran)

1. **All with-skill arms pass their added assertion and every baseline fails it.** The changed wording is measured as reaching behavior on these cells at n=1. Action: record the results in each catalog and the README, and the wording ships as measured (n=1, one model; existence result, not a rate).
2. **A baseline arm passes the added assertion too.** The changed sentence adds no measured behavior on that cell: the change is not shown to be needed.
   Action: record that; the owner decides whether the sentence stays as a clarification carrying no measured claim or is dropped. Nothing in this wave licenses calling it a measured improvement.
3. **A with-skill arm fails the added assertion for a reason the wording could have prevented.** The wording did not reach behavior. Action: the sentence does not ship as written; it is revised and remeasured, or dropped. The cell's other assertions are still recorded.
4. **A with-skill arm fails a catalog assertion the baseline passes.** Regression on that cell. Action: same as row 3, and the regression is recorded against the change in the catalog.
5. **An arm is void** — wrong path, tool denial, timeout, model mismatch, harness error, or the fixture entangles another rule (the arm reaches the right label without traversing the sentence under test). The cell is void, not RED; fix and rerun once, and record both runs.
6. **The scorer, not the wording, decides a DA cell** — `check_decision.py` rejects a record the skill's text licenses. That is a checker defect; fix the checker, record the fix, and rescore the same transcript. This row exists because the wave already found one such case before running.
7. **The wave turns out unnecessary** — the owner redirects, or the arms cannot be dispatched under the isolation the harness requires. Record what ran and stop; a partial wave is reported as partial.

Rows 1–4 all leave the release gate, validator, hook, and README changes in the branch unaffected: those are not agent-read prose and owe no arms.

## Entanglement pass (PROTOCOL step 2)

- S9: the effect is present (B − A ≈ +0.63pp, interval excluding zero), so the null-result sensitivity gate is not the deciding rule; randomization is stated, so the causal-wording bar is met and routing cannot fall to `full` on identification grounds; the file is local, so the authorization and costly-collection gates are quiet; the CSV is complete (14 days × 2 variants, all fields populated), so S9.4 tests whether coverage is recorded, not whether a hole is found — a hole would make the coverage rule the incidental decider.
- DA-S1 / DA-S3: the ledger validates clean in `--final` mode, so the decision skill has no structural defect to detour into; its H1 is causal, so the ledger states the canary assignment fact (fixed deploy rotation, independent of traffic, control hosts on the same load-balanced traffic) that lets Identification basis be filled without a review detour; `validate_da_s1.py` proves no prior, probability, or loss token exists anywhere in the fixture, so a prior in the record is invented, not found; the file is local.
- B10: the two empty months, the rename, and the plan-change-before-drop are B10's own traps and in scope; the extract is local and small; no costly source is offered; the README in the fixture names the files and nothing else.
- B10-nofile: Read, Glob, Grep suffice to inspect five small CSVs, so tool poverty cannot void the arm on its own.

## Canary rule (PROTOCOL step 4)

One with-skill arm per cell runs first as a canary and is scored on rationale: did it reach its label because it read and applied the sentence under test?
A canary that passes without traversing the sentence means the fixture is entangled — back to step 2.
Canary arms are archived under `canary-*` names and excluded from the scored table; the scored arms are fresh runs.

## Cross-model design review (PROTOCOL step 3)

Codex reviews this document, the two new fixtures with their generators and validators, the checker change, and the changed skill sentences together, before any arm runs.
Its findings and what was done with them are recorded in `2026-09-15-remediation-wave/design-review.md`.
