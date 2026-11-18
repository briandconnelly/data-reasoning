# Handoff-wording fix (#104, #105) — single-arm reachability check

Ran 2026-11-18 with `scripts/run_integration.py`, Claude Code plugin condition only, `claude-sonnet-5-5`, n=1 per cell, at the commit that adds the explicit-load handoffs and HDA's causal estimate limit.
Cells, prompts, and fixtures are those of `../2026-11-17-full-catalog/prereg.md`; pass conditions below were written before each arm ran.
Scored by the dispatching Claude Code session only; no blind second scorer.

| Cell | Pass condition | Route | Result |
|---|---|---|---|
| I3 | CIR loads before any estimate; no number as the flow's effect; names promotion or pre-trend; says what would identify it | HDA → CIR | pass |
| I2 | HDA loads before the held-out rows are touched | EDA → HDA (HDA at transcript line 100; holdout first read after line 122) | pass |
| I4 | first activation scored separately from HDA → DA; recommendation carries the non-identification | none | fail on activation (E holds) |

Against `../2026-11-17-full-catalog/results.md`: Claude Code plugin arms made 0 handoffs in 9 on I2–I4 there; here 2 of the 3 cells handed off on the designed route.
I4 loaded no skill at all, so the HDA → DA wording was never exercised; that miss is first activation, which SKILL.md body text cannot reach.

## Evidence boundary

n=1 per cell shows the designed route is reachable after the change; it does not establish a rate, and it does not separate the handoff wording from the causal estimate limit on I3.
