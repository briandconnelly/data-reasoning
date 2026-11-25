# Representative suite v1: primary scores

Scorer: the dispatching Claude Code session (Claude Fable 5.2, the orchestrator), unblinded, on 2026-11-25.
Written and committed before the blind scorer's result was fetched.
Columns are defined in `prereg.md` § Scoring; E and C are read from each arm's `.final.md` only.

40 scored arms: Codex blocks 1–3 (30) and Claude Code block 1 (10), per the 2026-11-25 notes in `prereg.md`.
Every arm's manifest status is `completed`, with model `gpt-6.2-sol` on codex-cli 0.172.0 or `claude-sonnet-5-5` on Claude Code 2.1.332.

## Answer columns

| Cell | Host | Condition | Arms | E | C | Passing arms |
| --- | --- | --- | --- | --- | --- | --- |
| R1 | Codex | plugin | 3 | n/a | 3/3 | 3/3 |
| R1 | Codex | none | 3 | n/a | 3/3 | 3/3 |
| R2 | Codex | plugin | 3 | n/a | 3/3 | 3/3 |
| R2 | Codex | none | 3 | n/a | 3/3 | 3/3 |
| X1 | Codex | plugin | 3 | 3/3 | 3/3 | 3/3 |
| X1 | Codex | none | 3 | 3/3 | 3/3 | 3/3 |
| X2 | Codex | plugin | 3 | E(a) 3/3, E(b) 3/3 | 3/3 | 3/3 |
| X2 | Codex | none | 3 | E(a) 3/3, E(b) 3/3 | 3/3 | 3/3 |
| X3 | Codex | plugin | 3 | 3/3 | 3/3 | 3/3 |
| X3 | Codex | none | 3 | 0/3 (arm 3 borderline) | 3/3 | 0/3 |
| R1 | Claude Code | plugin | 1 | n/a | 1/1 | 1/1 |
| R1 | Claude Code | none | 1 | n/a | 1/1 | 1/1 |
| R2 | Claude Code | plugin | 1 | n/a | 1/1 | 1/1 |
| R2 | Claude Code | none | 1 | n/a | 1/1 | 1/1 |
| X1 | Claude Code | plugin | 1 | 1/1 | 1/1 | 1/1 |
| X1 | Claude Code | none | 1 | 1/1 | 1/1 | 1/1 |
| X2 | Claude Code | plugin | 1 | E(a) 1/1, E(b) 0/1 | 1/1 | 0/1 |
| X2 | Claude Code | none | 1 | E(a) 1/1, E(b) 0/1 | 1/1 | 0/1 |
| X3 | Claude Code | plugin | 1 | 0/1 | 1/1 | 0/1 |
| X3 | Claude Code | none | 1 | 0/1 | 1/1 | 0/1 |

Scorer's reasons where an arm fails or is borderline:

- **X3 E, applied as written.**
  The column requires both that the answer says accuracy at a threshold is not the measure for a 500-call list and that it compares the models at that depth.
  Every one of the 8 X3 arms compares the models by churners in the top 500 and reports 302 against 173.
  `X3-codex-none-1`, `X3-codex-none-2`, `X3-claude-none-1`, and `X3-claude-plugin-1` never mention accuracy, so they fail the first half.
  `X3-codex-none-3` tabulates accuracy at the 0.5 cutoff beside precision at 500 and says precision at 500 matches the calling policy, without saying accuracy is the wrong measure: borderline, scored fail.
  The three Codex plugin arms state that Model A leads on accuracy at 0.5 and that the list is built by rank.
  No arm on either host chose Model A or reasoned from accuracy.
- **X2 E(b), Claude Code.**
  Both arms report rolling backtests on monthly totals and conclude the model fails the bar, but neither reports the origin whose training data all precede October 2025 (23.8%); `X2-claude-none-1` lists origins from November 2025 on, and `X2-claude-plugin-1` gives a range over 12 origins without that one.
  All six Codex arms report that origin with the three monthly errors (14.1%, 24.5%, 32.8%) and 23.8%.

## Orchestrator-only columns

Skill loads were confirmed by hand from the commands each arm ran, not taken from the manifest's `observed_route`.
For Codex the harness's extractor also searches command output, so the text of one skill's `SKILL.md`, which names the other skills, is counted as loading them: the manifests list three skills on the X2 and X3 Codex plugin arms where only `hypothesis-driven-analysis` was read.

| Cell | Host | Plugin arms | First load (hand-confirmed) | First activation | Records |
| --- | --- | --- | --- | --- | --- |
| R1, R2 | Codex | 6 | none | n/a | none; unnecessary ceremony pass 6/6 |
| X1 | Codex | 3 | `decision-analysis`, then `hypothesis-driven-analysis` | pass 3/3 | decision record: written 3/3, recognized by `check_record.py` (exit 0) 3/3, delivered 3/3; written before results 0/3 |
| X2 | Codex | 3 | `hypothesis-driven-analysis` | pass 3/3 | no record file created anywhere, 0/3 |
| X3 | Codex | 3 | `hypothesis-driven-analysis` | pass 3/3; handoff n/a | estimation record 0/3: no record file created anywhere |
| all five | Claude Code | 5 | none | fail (none) on X1–X3; n/a on R1, R2 | none; unnecessary ceremony pass 2/2 |

No-plugin arms loaded no skill and wrote no record on either host; unnecessary ceremony passes on all 8 routine no-plugin arms.
On X1 Codex each plugin arm computed defect rates and break-even figures before writing its decision record, so the record followed the first result computed after the skill's load.
X2 backtest computed (transcript): pass on all 6 Codex X2 arms, which report identical forecasts (34,290, 32,724, 34,656) from a September 30, 2025 cutoff; n/a for the Claude Code arms' E(b), which fail on the final message.
`data_modified` is set on the two Claude Code X2 arms by `data/__pycache__/analyst_model.cpython-315.pyc`, an interpreter cache; no fixture file changed.

## Cost, descriptive

Median wall-clock seconds and median loaded context tokens per arm (each arm's values are in its manifest and transcript).

| Cell | Codex none | Codex plugin | Claude Code none (1 arm) | Claude Code plugin (1 arm) |
| --- | --- | --- | --- | --- |
| R1 | 10 s, 51.8k | 9 s, 53.4k | 7 s, 146k | 6 s, 150k |
| R2 | 14 s, 50.7k | 13 s, 53.5k | 7 s, 146k | 8 s, 220k |
| X1 | 24 s, 86.6k | 56 s, 159k | 23 s, 294k | 28 s, 303k |
| X2 | 24 s, 69.3k | 32 s, 93.9k | 31 s, 290k | 30 s, 296k |
| X3 | 18 s, 50.8k | 38 s, 126k | 17 s, 147k | 21 s, 151k |
