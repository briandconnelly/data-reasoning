# Forced-load diagnostic on Claude Code (#111)

Written 2026-11-25, before any arm in this directory ran.

Question: on the two representative cells where Claude Code's no-plugin and plugin arms both failed the evidence column and no skill loaded (X2, X3; `../results.md`), does the answer change when the designed skill is loaded?
This decides whether work on first activation (#111, #108) is worth its cost on these asks.

## Arms

- Host and model: Claude Code, `--model claude-sonnet-5-5`, as pinned in `../prereg.md`.
- Forced-load arms: cells X2 and X3, plugin installed, n=3 each, named `<cell>-claude-forced-<k>`.
  The prompt is the cell's frozen prompt with one sentence before it: "First load the data-reasoning:hypothesis-driven-analysis skill and follow its instructions."
  That is the wording of the 2026-11-25 I3 explicit-load diagnostic; `hypothesis-driven-analysis` is the designed route of both cells.
  `forced.py` runs them through `scripts/run_integration.py` unchanged, replacing only the rendered prompt; fixtures, staging, manifests, and archiving are the suite's.
- Comparison arms: the suite's own no-plugin slots for these cells, `X2-claude-none-2`, `-3` and `X3-claude-none-2`, `-3`, run into `../arms/` with the unmodified harness, joining the block-1 arms `X2-claude-none-1` and `X3-claude-none-1` for n=3.
  They are run out of block order; this is the only departure from `../prereg.md` § Run order.
- 10 arms in all. An invalid execution, as `../prereg.md` defines it, is rerun once.

## Scoring

E and C as `../prereg.md` § Scoring defines them for X2 and X3, from the final message only, by the primary scorer and by the same blind scorer on a redacted bundle of these 10 arms.
An arm passes on both E and C; a condition passes at 2 of 3.
Skill loads are confirmed by hand; an arm that does not load the skill despite the instruction is reported and not counted as a forced-load arm.

## Reading, fixed in advance

- Forced-load passes and no-plugin fails on a cell: loading helps there, at n=3 and directionally; a description experiment for that kind of ask is justified.
- Both pass or both fail: loading does not change the scored outcome on that cell; no activation work is justified by it.
- Forced-load fails and no-plugin passes: a regression under load, reported as such.
- This is not a plugin-against-no-plugin verdict for the suite: the forced prompt differs from the frozen prompt by the instruction, so Claude Code's suite comparison stays incomplete.

## Limits

One model, n=3, two synthetic cells.
X2's E(b) requires one named backtest origin; a failure there may reflect that rule rather than the skill.
An instructed load is not natural activation: it shows what the skill does once read, not whether a description change would get it read.
