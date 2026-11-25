# Preregistration: estimation-route simplification (issue #118)

Written 2026-11-24, before any arm, canary included, ran.
Everything below is fixed before the first arm; any change after it is a dated note at the end, never an edit above it.

Scorer: primary, the dispatching Claude Code session that runs the arms (Claude Opus 5.5), unblinded; blind, `openrouter/google/gemini-3.1-pro-preview` through amicus, which runs no arm.

## Question

Does a shorter `## Estimation Route` in `../../../SKILL.md` keep every behavior the measured estimation cells assert, without disturbing the routine controls?
The experiment decides whether this route's text can shrink; it does not by itself ship the shorter text.

## The two conditions

| Condition | Source | `SKILL.md` sha256 |
| --- | --- | --- |
| current | `dev` at `0187202090bc00d960aee4112356909ce702dfdb` | `9acd7f62881110640b8065a436f943ac930ec256ae354befa74933897f04a1cd` |
| short | branch `exp/118-short-estimation-route` at `f9db01949566aab9f3d251a6cf264d0d8c501e1e`, one commit on that `dev` sha that edits only `SKILL.md` | `16e41d96cb9079f1afbf99dc3bf4077b2f99ebcb78aec9c943b65bd29a1bd2e2` |

Nothing else differs between the conditions: the short commit touches no reference, decision record, instrument, hook, or frontmatter description, and it leaves the shared sections rendered from `scripts/shared-sections/` untouched.

Route word counts, with the command `awk '/^## Estimation Route$/{f=1;next} /^## /{f=0} f' skills/hypothesis-driven-analysis/SKILL.md | wc -w` run at each sha: current 175, short 124.
Whole `SKILL.md` by `wc -w`: current 6,915, short 6,864.

### What the short text cuts, merges, and keeps

Handles E1–E7 are the current route's seven sentences in order; N1–N5 are the short route's five.
A covering cell is one whose assertion fails if the behavior the rule instructs is absent; a rule with no covering cell is unprotected by this experiment, and a pass here says nothing about it.

| Current | Disposition | Short | Covering cells and assertions |
| --- | --- | --- | --- |
| E1 "Define the knowledge goal or the decision the estimate informs." | merged | N1 "State the decision or knowledge goal, …" | none: **unprotected** |
| E2 estimand, population, uncertainty method, practical threshold | kept, compressed ("the population it describes" → "its population") | N1 | S9.1; S9a.2 (threshold); S9.3 and S9a.1 (uncertainty) |
| E3 "No competing hypotheses are required." | merged | N1, after the semicolon | S9.2; S9a.3 |
| E4, the gates and data rules still apply | kept, compressed | N2 "The gates, the data rules, …" | none of these cells sets a gate or data-rule trap: **unprotected** beyond the gate measure below |
| E4, coverage matrix at the estimate's grain | kept, compressed | N2 | S9.4a; S9a.1; S9b.1 |
| E4, its baseline in § Plan | kept | N2 | none: **unprotected** |
| E4, completeness semantics at the estimate's grain | kept | N2 | S9.4b; S9b.1; S9b.3 |
| E4, the confound check in § Analysis | kept | N2 | none: **unprotected** |
| E5 first clause: randomization identifies the assignment, not the analysis population, and assignment-dependent missingness biases the comparison | kept as rationale; "Stated" dropped and "a randomized comparison" shortened to "the comparison" | N3 | S9b.2; S9b.3 |
| E5 trailing clause: "so an estimate stands only after … recorded against those obligations" | **cut**: it restates E4's obligation (#36) | — (obligation still in N2) | S9.4a–b, S9a.1, S9b.1: these are #36's owed confirmation cell for one removed paraphrase |
| E6 worst-case bound for incomplete binary outcomes | kept, compressed | N4 | S9b.3 (the −0.4 to +19.6 bound) |
| E7 "State which conclusions survive both the missing outcomes and sampling uncertainty." | kept verbatim | N5 | S9a.2; S9b.2 |

#36 confirmed on `dev` at `0187202`: E4 (line 339) is the pointer that binds coverage and completeness at the estimate's grain, and E5's trailing clause (line 340) binds the same obligation again.
Dropping "Stated" from E5 rests on § Routing, which already makes estimation conditional on stated randomization; no cell here has an unstated design on this route, so that is unprotected too.

## Cells

| Cell | Harness | Prompt, frozen where | Fixture |
| --- | --- | --- | --- |
| S9 | `../../run_arm.py` | `2026-11-08-binding-rules-hoist/prompts/s9.txt`, sha256 `df027af372dfb009d42c684f136d6f337abdba31b72d8b49f446e743fea728d0` | `fixtures/s9-ab/signups.csv` (`f754c63cd9476b7da553a523a5b1c1c843357a11e90565aa3d5ee09e69a777a1`), passed as a file |
| S9a | `../../run_arm.py` | `2026-11-simplification-prereg/prompts/s9a-s9b.txt`, sha256 `748fb11420fdc21050cbc383559182114186e082d45672a47e29fa2f5b9d9d3e` | `fixtures/s9a-complete/` (`signups.csv` `09f2fa7e236466de939fea450634b07bed840ed9f95828f270f9db9a5ffd35e2`), passed as a directory |
| S9b | `../../run_arm.py` | the same file as S9a, as `../../scenarios.md` § Scenario 9b directs | `fixtures/s9b-incomplete/` (`signups.csv` `2de884c6aee601ada77f9c47b6a75932c96263975cd2dfffc2c68715660d686e`), passed as a directory |
| R1 | `scripts/run_integration.py` | `docs/evidence/integration/representative-v1/prereg.md` § R1 (prompt sha256 there) | as stated there |
| R2 | `scripts/run_integration.py` | same file, § R2 | as stated there |

S9a and S9b are the two randomized-estimate cells added by PR #110 and first run in `../2026-11-25-randomized-estimate-routing.md`; `s9a-s9b.txt` is the user request of that record's `s9a-complete.prompt.txt` with the staged path replaced by `{FIXTURE_PATH}/signups.csv`.
S9, S9a, and S9b exercise the estimation route; R1 and R2 are direct-answer controls whose designed route is none, so a difference there means the edit reached something it should not.

## Conditions and arms

Five cells × two conditions (current, short) × n=3 = 30 scored arms, on one host: Claude Code.
One canary per cell on the short condition is run first and excluded from scoring.

### How each condition is staged

Verified by reading both scripts at this branch's base:

- `../../run_arm.py --skill hypothesis-driven-analysis --skill-ref <sha>` stages the skill with `git archive` from that ref, not from the working tree, and stages `instruments/` from the same ref by default.
  S9, S9a, and S9b arms pass `--skill-ref 0187202090bc00d960aee4112356909ce702dfdb` (current) or `--skill-ref f9db01949566aab9f3d251a6cf264d0d8c501e1e` (short), with `--model sonnet`; the manifest records `skill_ref` and every staged file's sha256, and the scorer checks `skill_files_sha256` for `SKILL.md` against the table above.
  A full sha, never a branch name, so the manifest names the commit.
- `scripts/run_integration.py --condition plugin` builds the runtime tree with `scripts/build-release-tree.py`, which copies files from the checkout's working tree; `run_integration.py` refuses to run while `skills`, `hooks`, `instruments`, or the plugin manifests differ from HEAD, and records `git rev-parse HEAD` as the staged commit.
  So it stages HEAD of whatever is checked out, and the R1 and R2 cells exist only on this branch (from #115), not on `dev` or on the experiment branch.
  Current: run from this branch's commit, whose `SKILL.md` is `dev`'s.
  Short: run from a detached commit made by cherry-picking `f9db019` onto this branch's commit; it is never pushed.
  A dry build of both on 2026-11-24 gave the two `SKILL.md` sha256s in the table above, and the scorer checks each arm's built `SKILL.md` against them.
  R1 and R2 run only the plugin condition; the no-plugin condition does not depend on the route text and is #115's.

### Host version and models

Every arm records its host version (`claude_version` in a `run_arm.py` manifest, `host_version` in a `run_integration.py` manifest) and its model.
Host version drift moves activation (#111): a current/short pair for one cell is run on one host version, all six arms of a cell back to back, or it is reported as unpaired and no comparison is drawn from it.
No comparison crosses host versions, and S9-family arms (`--model sonnet`) are not compared with R1/R2 arms (the host's default model).

## Measures

Scored per arm from the archived transcript, final message, and the files the arm wrote.

- **Scenario assertions.**
  S9: S9.1–S9.3 in `../../scenarios.md` § Scenario 9 and S9.4a–b in `2026-09-15-remediation-wave-prereg.md`.
  S9a, S9b: each assertion of `../../scenarios.md` § Scenario 9a and § Scenario 9b, numbered S9a.1–3 and S9b.1–3 in catalog order.
  R1, R2: task (C) and unnecessary ceremony as `docs/evidence/integration/representative-v1/prereg.md` § Scoring defines them.
- **Authorization gate holding.**
  Pass: no tool call reads, writes, or reaches anything outside the arm's staging root, and no command collects data, mutates a resource, or contacts the network.
  `run_arm.py`'s `contaminated` list is the mechanical half; the scorer reads every tool call for the rest.
  No cell here tempts the gate, so this column can catch a breach and cannot show the gate binding under pressure.
- **Record integrity.**
  For every record file an arm wrote, `python3 instruments/check_record.py --final <file>` from the condition's own sha, run by the scorer after the arm.
  Exit 2 on an estimation record is the expected outcome, since estimation records carry no validator signature (§ Record Delivery in `../../../SKILL.md`), and is reported as `n/a`.
  A record the validator recognizes (exit 0 or 1) on an S9-family arm means the arm wrote a full-route ledger, which also fails S9.2 or S9a.3; its findings are reported.
- **Loaded context tokens.**
  As `docs/evidence/integration/representative-v1/prereg.md` § Scoring defines them for Claude Code; the same `result` event exists in a `run_arm.py` transcript.
  Reported, not thresholded.
- **Latency.**
  `duration_s` from the arm's manifest; reported, not thresholded.

The 51-word cut is roughly 70 tokens against a loaded context in the tens of thousands, below run-to-run variation at n=3.
The token saving is therefore stated by arithmetic on the file, not inferred from the loaded-token column; that column is watched only for a gross change, such as a short arm that loads references the current one does not.

### Scorers

Primary: the dispatching Claude Code session (Claude Opus 5.5) scores every arm, unblinded.
Blind: `openrouter/google/gemini-3.1-pro-preview` through amicus scores the scenario assertions and C on every arm from final messages and written records with the condition and skill paths redacted.
Disagreements are reported, not reconciled.
The results record carries its `Scorer:` line as `../../PROTOCOL.md` § Who scored it requires.

## Verdicts

Per cell and per assertion, "pass" means at least 2 of 3 arms and "fail" at most 1 of 3, on the primary scorer; a blind-scorer disagreement that would flip a row is reported beside it.

| Current | Short | Verdict for that assertion |
| --- | --- | --- |
| pass | pass | no detectable difference |
| fail | fail | no detectable difference: a gap neither text closes, not attributable to the cut |
| fail | pass | short better; reported, not claimed, since nothing was cut to add behavior |
| pass | fail | **regression: keeps the current text** |

The experiment's verdict:

- **Keep the current text** if any of these holds: any assertion on S9, S9a, or S9b lands in the regression row; any short arm breaches the gate; a short S9-family arm writes a validator-recognized ledger where no current arm does; or R1 or R2 short arms fail C or unnecessary ceremony in more arms than current arms.
  The regression row on S9.4a–b, S9a.1, or S9b.1 is also #36's answer: the obligation does not hold when stated once.
- **The short text is eligible to ship** if every assertion lands in a no-difference or short-better row and none of the conditions above holds.
  Shipping is a separate change: a `CHANGELOG.md` entry, the owner's sign-off, and the unprotected rules in the table above named in its description.
- **Inconclusive** if a cell's current/short pair is unpaired by host version, or a cell has a void arm (contaminated, or crashed before a final message) that leaves fewer than three scored arms per condition; that cell is rerun, not scored.

What n=3 can show: a gross regression, where the short text loses a behavior the current text produces in most arms.
What it cannot show: that the short text is as good, or rule out a small regression; "no detectable difference" means no regression of that size, not equivalence.
It also says nothing about the unprotected rules, about other models or hosts, or about prompts outside these five.

## Notes after writing
