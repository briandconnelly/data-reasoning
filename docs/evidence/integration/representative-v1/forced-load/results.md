# Forced-load diagnostic on Claude Code: results

Ran 2026-11-25 against `prereg.md` in this directory, at `dev` `d13fa35` plus that file.
Scorer: primary, the dispatching Claude Code session (Claude Fable 5.2), unblinded; blind, `openrouter/google/gemini-3.1-pro-preview`, on E and C.
The two scorers agree on all 10 new arms; the block-1 no-plugin arms were scored in `../scores-primary.md` and `../scores-blind.md`.

## Result

Passing arms of 3 on Claude Code (`claude-sonnet-5-5`, 2.1.332).
Every forced-load arm loaded `hypothesis-driven-analysis`; no no-plugin arm loaded a skill.

| Cell | Skill loaded on instruction | No plugin | Reading fixed in advance |
| --- | --- | --- | --- |
| X2 forecast check | 3/3 | 2/3 | both pass: loading does not change the scored outcome |
| X3 two churn models | 1/3 | 0/3 | both fail: loading does not change the scored outcome |

- X2: with the skill loaded, all three arms reported the October–December 2025 backtest at 23.8% (one as 24%); without it, two of three did.
  All six arms rejected the model.
- X3: all six arms chose Model B with 302 against 173.
  One forced-load arm said accuracy at the 0.5 cutoff does not fit the decision; the other five never mentioned accuracy.
- Loading cost time on X3 (median 28 s against 17 s) and little on X2 (34 s against 31 s).

## What follows

By the reading fixed in advance, neither cell justifies work on first activation for this kind of ask on Claude Code.
On these two asks the model's unaided answer is already as good, by these columns, as its answer with the skill read.

Beside the first run (`../results.md`): on Codex the same skill loaded unprompted on X3 and all three plugin arms passed E, so the skill's effect on that column differs by host; this diagnostic does not say why.

## Limits

- n=3, one model, two synthetic cells; each reading is directional.
- An instructed load is not natural activation, and the instruction sentence is itself a difference between the two conditions.
- It says nothing about asks other than these two: the decision ask in #108 and the multi-skill handoffs in #104 were not run.
- X3's E has two required parts; five of six arms failed only the first (saying accuracy is not the measure) while comparing at the right depth.
