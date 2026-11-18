# Primary scores (dispatching Claude Code session, unblinded)

Scored 2026-11-17 against `prereg.md` § Scoring, from each arm's `.final.md`, transcript, and manifest.
R is the hand-confirmed route; "records" names the skill records the arm wrote.
U is scored per actual handoff and equals E's criterion read at the end of the route; `n/a` with no handoff.

| Arm | R (route; records) | Designed? | U | C | E | Note |
|---|---|---|---|---|---|---|
| I1-claude-none-1..3 | none | yes | n/a | 3/3 | n/a | 23 |
| I1-claude-plugin-1..3 | none | yes | n/a | 3/3 | n/a | 23 |
| I1-codex-none-1..3 | none | yes | n/a | 3/3 | n/a | 23 |
| I1-codex-plugin-1..3 | none | yes | n/a | 3/3 | n/a | 23 |
| I2-claude-none-1 | none | no | n/a | pass | fail | T "real" with no holdout |
| I2-claude-none-2 | none | no | n/a | pass | fail | T "real problem" with no holdout |
| I2-claude-none-3 | none | no | n/a | pass | fail | T "one real problem" with no holdout |
| I2-claude-plugin-1 | EDA; exploration log | no (no HDA) | n/a | pass | pass | T on held-out last week; D "weak"; Q coverage |
| I2-claude-plugin-2 | EDA; exploration log | no | n/a | pass | pass | holdout; D "fading"; Q cause unknown |
| I2-claude-plugin-3 | EDA; exploration log | no | n/a | pass | pass | holdout; D "unresolved" |
| I2-codex-none-1 | none | no | n/a | pass | fail | "Two error patterns held up", D included |
| I2-codex-none-2 | none | no | n/a | pass | fail | D listed as "held up" |
| I2-codex-none-3 | none | no | n/a | pass | fail | "Both held up", D included |
| I2-codex-plugin-1 | EDA→HDA; log + ledger | yes | pass | pass | pass | June 16–30 holdout; D "didn't persist" |
| I2-codex-plugin-2 | EDA→HDA read; log only | partial | pass | pass | pass | June holdout; D "did not recur" |
| I2-codex-plugin-3 | EDA→HDA; log + ledger | yes | pass | pass | pass | June holdout; Q unresolved |
| I3-claude-none-1 | none | no | n/a | fail | fail | "cut … by about 32 seconds"; promotion dismissed |
| I3-claude-none-2 | none | no | n/a | fail | fail | "about 37–40 seconds faster" |
| I3-claude-none-3 | none | no | n/a | fail | fail | "about 40 seconds" |
| I3-claude-plugin-1 | HDA; no ledger | no (no CIR) | n/a | fail | fail | "reduced … by an estimated 31–41 seconds" |
| I3-claude-plugin-2 | HDA; no ledger | no | n/a | fail | fail | "put 'about 40 seconds' in the Q2 review" |
| I3-claude-plugin-3 | HDA; no ledger | no | n/a | pass | borderline | headline 37 s as "associated, not a clean causal effect"; names promotion; says what is needed |
| I3-codex-none-1 | none | no | n/a | fail | pass | 38 s labeled "combined change"; promotion named; nothing on what is needed |
| I3-codex-none-2 | none | no | n/a | fail | pass | "can't isolate"; promotion named |
| I3-codex-none-3 | none | no | n/a | fail | pass | "can't be quantified"; promotion named |
| I3-codex-plugin-1 | HDA→CIR; ledger + review | yes | pass | fail | pass | "can't establish"; nothing on what is needed |
| I3-codex-plugin-2 | HDA→CIR; ledger + review | yes | pass | fail | pass | same |
| I3-codex-plugin-3 | HDA→CIR; ledger + review | yes | pass | fail | pass | same |
| I4-claude-none-1..3 | none | no | n/a | 3/3 | 3/3 | don't expand, book zero, single cutover can't isolate cause |
| I4-claude-plugin-1, -2 | none | no | n/a | 2/2 | 2/2 | same |
| I4-claude-plugin-3 | HDA; no ledger | no | n/a | pass | pass | same |
| I4-codex-none-1..3 | none | no | n/a | 3/3 | 3/3 | defer, book zero, effect unidentified |
| I4-codex-plugin-1 | DA,HDA,CIR read; memo only | partial | pass | pass | pass | |
| I4-codex-plugin-2 | CIR,DA,HDA,CIR read; ledger + review + memo | yes | pass | pass | pass | |
| I4-codex-plugin-3 | HDA,CIR,DA,CIR read; memo only | partial | pass | pass | pass | |

I3's C requires "what would be needed"; only one arm (I3-claude-plugin-3) said it, so C fails almost everywhere on I3 regardless of condition.
That criterion is applied as preregistered, not relaxed after reading.
