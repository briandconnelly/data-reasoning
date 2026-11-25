# Representative suite v1: results

Ran 2026-11-25 against `prereg.md`, at `dev` `a4889e3` plus the dated notes in that file.
Scorer: primary, the dispatching Claude Code session (Claude Fable 5.2), unblinded; blind, `openrouter/google/gemini-3.1-pro-preview`, on E and C only.
The two scorers agree on E and C for all 40 arms (`scores-primary.md`, `scores-blind.md`).

## What ran

- 10 canaries, one per runnable cell per host, all passing the criteria in the 2026-11-25 note; not scored.
- 40 scored arms: Codex (`gpt-6.2-sol`, codex-cli 0.172.0) blocks 1–3, 30 arms; Claude Code (`claude-sonnet-5-5`, 2.1.332) block 1, 10 arms.
- No invalid execution and no replacement.
- R3 and R4 did not run: they have no frozen prompt.
- Deviation from the 84-arm design, recorded before any scored arm: Claude Code stopped at block 1 because none of its plugin arms loaded a skill, so Claude Code gets counts and no verdict.

## Codex: verdict per cell

Counts are passing arms of 3, where an arm passes on both E and C (C alone on R1 and R2).

| Cell | Plugin | No plugin | Verdict |
| --- | --- | --- | --- |
| R1 routine lookup | 3/3 | 3/3 | not distinguished at n=3: the baseline already does this |
| R2 routine means | 3/3 | 3/3 | not distinguished at n=3: the baseline already does this |
| X1 supplier decision | 3/3 | 3/3 | not distinguished at n=3: the baseline already does this |
| X2 forecast backtest | 3/3 | 3/3 | not distinguished at n=3: the baseline already does this |
| X3 churn models | 3/3 | 0/3 | directional lift |

Suite reading on Codex: one cell with a directional lift, none with a regression.

What the X3 lift is, and is not.
All six Codex X3 arms chose Model B and reported 302 against 173 churners in the top 500, so C passes 6/6 and no arm was misled by accuracy.
The difference is in E: the three plugin arms said Model A leads on accuracy at the 0.5 cutoff and that the list is built by rank; the three no-plugin arms compared at the top 500 without saying accuracy is the wrong measure (one tabulated accuracy without comment).
So the plugin changed what the answer told the reader about the rejected metric, not which model was recommended.

## Claude Code: counts only

One arm per cell and condition, so no verdict.

| Cell | Plugin | No plugin |
| --- | --- | --- |
| R1 | 1/1 | 1/1 |
| R2 | 1/1 | 1/1 |
| X1 | 1/1 | 1/1 |
| X2 | 0/1 (E(b) fail) | 0/1 (E(b) fail) |
| X3 | 0/1 (E fail) | 0/1 (E fail) |

No Claude Code plugin arm loaded a skill, in the five canaries or the five scored plugin arms, so the two conditions ran the same instructions apart from the skill listing.
On X2 both arms rejected the model and ran rolling backtests on monthly totals, but neither reported the October–December 2025 origin the column requires.

## Routing and records, Codex plugin arms

Skill loads were confirmed by hand; see the harness note below.

- First activation: pass on 9 of 9 challenge arms (`decision-analysis` on X1, `hypothesis-driven-analysis` on X2 and X3).
- Routine cells: no skill load in 6 of 6 arms; unnecessary ceremony passes 6/6, and 6/6 without the plugin.
- X1: a decision record was written, recognized by `instruments/check_record.py`, retained, and named in the final message in 3 of 3 arms; in all 3 it was created after the arm's first computed result.
- X2 and X3: no record file was created anywhere in 6 of 6 arms.

## Cost, descriptive

Codex medians per arm, plugin against no plugin: X1 56 s and 159k loaded tokens against 24 s and 87k; X2 32 s and 94k against 24 s and 69k; X3 38 s and 126k against 18 s and 51k; R1 and R2 within 1 s and 3k tokens of each other.
Per-arm values are in `scores-primary.md`.
The preregistration draws no verdict from cost.

## Maintenance signals, as preregistered

- **X2, X3 → #116.**
  The Codex plugin condition passes X2 (3/3) and X3 (3/3), so no method reference is triggered on Codex.
  Closing either row needs a pass on both hosts, and Claude Code has no verdict, so both rows stay open.
- **R1, R2 → descriptions.**
  L is 0 for every skill on both hosts: no description change.
- **Activation.**
  Not assessable within a condition on either host: every Codex challenge plugin arm passed first activation and no Claude Code plugin arm did, so neither host has both groups.
- **Conflicting signals.** None.

## Limits of this run

- n=3 per condition on one host and one model; each label above is directional.
- Claude Code has one arm per condition and no verdict.
- R3 and R4, the representative sample, are not built, so this run covers two routine and three synthetic challenge cells only.
- On X1, X2, and both routine cells the no-plugin baseline passed 3/3, so those cells could not show a lift; they can only show the plugin did not make answers worse.
- The X3 result rests on a two-part column whose first part (saying accuracy is not the measure) no no-plugin arm met; a reader who weighs only the recommendation would call X3 not distinguished.

## Harness note

`observed_route` in `scripts/run_integration.py` searches the whole Codex command item, output included.
Reading one `SKILL.md` therefore counts every skill that file names: the manifests list `causal-identification-review` and `decision-analysis` on the X2 and X3 Codex plugin arms, where the commands show only `hypothesis-driven-analysis` was read.
The routing columns here use the hand-confirmed loads.
The same extractor produced the Codex routes in the 2026-11-17 full-catalog manifests.
