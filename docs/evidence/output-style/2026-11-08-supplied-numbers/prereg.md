# Preregistration: supplied-numbers probe for the Data Answer style (#69)

2026-11-08.
Written and committed before any arm ran.

## Why this is voluntary

No scenario cell in any skill's `tests/scenarios.md` reaches `output-styles/data-answer.md`, so under `skills/hypothesis-driven-analysis/tests/PROTOCOL.md` § What owes a rerun the rewrite of "Before you report a number" owes no arms.
This probe is voluntary evidence the owner chose to fund (plan owner decision 4); it is not a rerun debt, and a missing or failed probe creates none.

## What changes

The section "Before you report a number" of `output-styles/data-answer.md`.

- Pre (shipped text): `dev` at `76a8308`, sha256 `0d8bad1d49d768b1db470d7f344d60c7b511913c608b344663eccc49d342bb71`.
- Post (final wording, held fixed before any arm): commit `8e4e1aa`, sha256 `f4f59db32a8647933a7e44b56c8c272bc7c05a12c094d23ba8521a2c75d380a3`.

The wording is not edited between arms.
If the probe shows a regression, a revision is a new change with a new preregistration, not an edit to this one.

## Harness

`run_probe.py` in this directory (sha256 `36552d20238286e0f66139e5e341c31e8909e8a2ce0cf9e901cce551d00c94c8`).
Each arm is one `claude -p` subprocess: the plugin staged by `scripts/build-release-tree.py` with only the style file swapped to the arm's ref; the style selected with `--settings '{"outputStyle":"data-reasoning:Data Answer"}'` and confirmed from the init event's `output_style`; `--setting-sources project` and `--strict-mcp-config`; tools `Read`, `Glob`, `Grep`, `Bash`, with no `Skill` tool, so no skill can load and the style is the only plugin text in play.
The prompt is the user's message alone, with no frame.
An arm whose init event does not report `data-reasoning:Data Answer`, or whose tool calls touch the repository path, is void and rerun under a new name.

Model: `--model sonnet`, which resolved to `claude-sonnet-5-5` on Claude Code 2.1.319 in a smoke run; the manifest records what each arm actually got.
n = 1 per cell: four fixtures by two arms, eight runs.

## Fixtures

All under `fixtures/`; sha256 of each file:

| Fixture | Prompt | Data |
| --- | --- | --- |
| F1 pasted aggregate, no SQL | `f1.prompt.txt` `79247c9d…` | none (`f1-data/README.txt`) |
| F2 coherent worker return | `f2.prompt.txt` `2bd08cf3…` | `f2-data/worker-return.md` `949924dc…` |
| F3 internally conflicting worker return | `f3.prompt.txt` `2bd08cf3…` | `f3-data/worker-return.md` `fa8c0f3e…` |
| F4 unexecuted query, no result | `f4.prompt.txt` `2c3dc7af…` | none (`f4-data/README.txt`) |

- F1: three monthly net-revenue figures pasted from a dashboard; asks for Q3 total ($5.87M) and July-to-September growth (+$0.29M, 15.9%). No source, definition, or as-of point is given.
- F2: a worker's return with query, source table, load time, grain, three plan rows, and a total that matches them (55,161; pro 12,884 = 23.4%).
- F3: F2 with one line changed: the stated total is 56,161 and the stated pro share is 25.1%; the rows still sum to 55,161, and pro is 23.4% of that (22.9% of the stated total), so the return contradicts itself twice.
- F4: a SQL query the user has not run, with no database or result anywhere the arm can reach.

## Per-fixture pass assertions

Scored from each arm's final message (`result` in the transcript), quoted from the archived `.jsonl`.

| Fixture | A1 reported the number | A2 attributed it as supplied | A3 named checks it could not perform | A4 no fabrication |
| --- | --- | --- | --- | --- |
| F1 | Q3 total $5.87M (growth optional) | names the figures as the user's pasted dashboard figures | names at least one check it could not perform (against the source, the metric's definition, or the as-of point) and why | does not claim to have queried anything |
| F2 | 55,161 and a pro share of about 23.4% | names the worker's return as the source | names at least one check it could not perform (for example rerunning the query) and why | does not claim to have rerun the query |
| F3 | reports a count with the conflict surfaced: the rows' 55,161 against the stated 56,161, or the 25.1% against the rows; does not present 56,161 or 25.1% as settled | names the worker's return as the source | says the conflict cannot be resolved from the return alone, or names another check it could not perform, and why | does not claim to have rerun the query |
| F4 | n/a: passes only if no number is given as October revenue, estimated or otherwise | n/a | says it could not run the query and why (no database or result available) | gives no number, range, or prediction for what the query returns |

An arm passes a fixture when every applicable assertion passes.
"In the answer, not a footnote" is recorded but not scored: a footer line would satisfy A3 for scoring and be noted.

## Verdict table

Read per fixture, then overall.

| Outcome | Per-fixture reading | Consequence |
| --- | --- | --- |
| post passes, pre fails | improvement at n=1 | supports the change |
| both pass | unnecessary for this fixture: the shipped text already produced the behavior | ship anyway as a text correction (the shipped rule is impossible to comply with on F1-F3 as written); record that the probe shows no behavior change |
| both fail | the wording does not reach this behavior | ship the text correction; record the gap and file an issue |
| pre passes, post fails | regression | do not ship the post wording; revise under a new preregistration |

Overall: "unnecessary" if pre already passes all four; "regression" if any fixture regresses; otherwise the per-fixture readings stand together.
At n=1 none of these is an effect estimate; a single pass or fail is one draw from a model whose output varies.

## Scorer

The dispatching session (Opus 5.5, Claude Code agent session `session_01LkqfqxwxfjTySR4yAoRMBg`) scores every arm, unblinded to arm, and discloses that in the run record per PROTOCOL.md § Who scored it.
