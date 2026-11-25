# Handoff-wording fix (#104, #105) — Claude Code reruns

Ran 2026-11-18 with `scripts/run_integration.py`, Claude Code plugin condition only, `claude-sonnet-5-5`, n=3 per cell, at the commit that adds the explicit-load handoffs and HDA's causal estimate limit (`619b147`; no plugin file changed after it).
Cells, prompts, fixtures, and criteria are those of `../2026-11-17-full-catalog/prereg.md`.
Primary scores: `scores-primary.md` (dispatching Claude Code session, not blind).
Blind scores: `scores-blind.md` (Codex via amicus, final messages only, skill names redacted).
Disagreements are reported, not reconciled.

## Route

| Cell | Designed route | 2026-11-17 (before) | 2026-11-18 (after) |
|---|---|---|---|
| I1 | none | — | none 3/3, answer 23 in 3/3 |
| I2 | EDA → HDA | 0/3 (EDA only) | 1/3 (EDA only in 2/3) |
| I3 | HDA → CIR | 0/3 (HDA only) | 3/3 |
| I4 | HDA → (CIR) → DA | 0/3 (no skill 2/3) | 0/3 (no skill 3/3) |

## Evidence boundary (E)

| Cell | Primary | Blind |
|---|---|---|
| I2 | 3/3 | 3/3 |
| I3 | 3/3 | 2/3 + 1 borderline (-3) |
| I4 | 2/3 + 1 borderline (-2) | 0/3: 1 fail (-1), 2 borderline |

Against 2026-11-17, where every Claude Code I3 arm offered a 31–43 s trend-adjusted effect, no I3 arm here gives a number as the flow's effect.
I3-claude-plugin-3's suggested review wording ("only part of that can be credited to the flow") implies a positive contribution: primary scored C borderline, blind scored E borderline.
I4's misses come from arms that loaded no skill, so neither changed text was in play; the scorers disagree on whether "0 attributable hours" and "an upper bound on Assist's own effect" cross the boundary.

## Reading

- **#105 (I3):** the designed route was taken in 3/3 and no arm gave the effect a number, against 0/3 and 3/3 numbers before. The change bundles the handoff wording with the causal estimate limit, so these runs do not say which did it.
- **#104:** reachable on I2 and I3; on I2 the handoff is taken 1 time in 3 — the other two arms confirmed on their own held-back week and offered the handoff as a follow-up, which keeps E but skips the designed route.
- **I4:** first activation fails (tracked in #108); body text cannot reach it.

n=3 per cell; these are counts, not rates.

## Note, 2026-11-25: the prompt named the condition (#128)

All 12 archived prompts here show an absolute data path inside a workspace named after the arm (`int-<cell>-claude-plugin-<n>-*`), so `plugin` appears in every one.
This run is plugin-only, so every arm saw the same `plugin` label and the cue makes no difference between arms within it.
Disclose it in any comparison with a run whose prompt exposure differed: the 2026-11-17 full-catalog run, whose prompts named `plugin` or `none` by condition (`docs/evidence/integration/2026-11-17-full-catalog/results.md` § Note, 2026-11-25: the prompt named the condition), and the 2026-11-25 I3 runs, whose prompts showed other labels (`docs/evidence-status.md` § Handoffs and routing).
The cue's effect on behaviour is unknown.
No count above changes.
