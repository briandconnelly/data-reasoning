# Primary scores — 2026-11-18 handoff-fix reruns

Scorer: the dispatching Claude Code session (claude-opus-5-5), not blind to condition or route.
Criteria: `../2026-11-17-full-catalog/prereg.md` § Scoring.

| Arm | Route | R | E | C | Note |
|---|---|---|---|---|---|
| I1-claude-plugin-1 | none | pass | n/a | pass | 23 |
| I1-claude-plugin-2 | none | pass | n/a | pass | 23 |
| I1-claude-plugin-3 | none | pass | n/a | pass | 23 |
| I2-claude-plugin-1 | EDA → HDA | pass | pass | pass | HDA loaded (line 100) before the holdout was first read (line 122) |
| I2-claude-plugin-2 | EDA | fail | pass | pass | confirmed T on a pre-set 7-day holdout itself; offers the handoff only as a follow-up |
| I2-claude-plugin-3 | EDA | fail | pass | pass | same as -2 |
| I3-claude-plugin-1 | HDA → CIR | pass | pass | pass | explicitly declines a trend-corrected figure |
| I3-claude-plugin-2 | HDA → CIR | pass | pass | pass | "I'd avoid presenting 41 s … as the flow's effect" |
| I3-claude-plugin-3 | HDA → CIR | pass | pass | borderline | suggested review wording says "only part of that can be credited to the flow", implying a non-zero effect |
| I4-claude-plugin-1 | none | fail | pass | pass | no skill loaded |
| I4-claude-plugin-2 | none | fail | borderline | pass | states causation unestablished, but headlines "the point estimate is a cost of roughly 110 responder-hours" |
| I4-claude-plugin-3 | none | fail | pass | pass | no skill loaded |
