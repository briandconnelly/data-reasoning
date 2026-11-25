# Forced-load diagnostic: primary scores

Scorer: the dispatching Claude Code session (Claude Fable 5.2, the orchestrator), unblinded, 2026-11-25.
Committed before the blind scorer's result was fetched.
Columns as `../prereg.md` § Scoring defines them; E and C from each arm's `.final.md` only.
All 10 new arms completed with `claude-sonnet-5-5` on Claude Code 2.1.332.
Skill loads confirmed by hand: each of the six forced-load arms made one `Skill` call, for `hypothesis-driven-analysis`; no no-plugin arm loaded a skill.

| Arm | E | C | Passes | Scorer's reason |
| --- | --- | --- | --- | --- |
| `X2-claude-forced-1` | E(a) pass, E(b) pass | pass | yes | "Sep-2025 origin (same time of year, forecasting Oct–Dec 2025) 23.8%" |
| `X2-claude-forced-2` | E(a) pass, E(b) pass | pass | yes | origin 2025-09-30, 23.8% |
| `X2-claude-forced-3` | E(a) pass, E(b) pass | pass | yes | September 2025 origin, "averaging 24% absolute", within 3 points |
| `X2-claude-none-1` (block 1) | E(a) pass, E(b) fail | pass | no | no origin with training data all before October 2025 |
| `X2-claude-none-2` | E(a) pass, E(b) pass | pass | yes | "Sep 2025, Oct–Dec 2025, 23.8%" |
| `X2-claude-none-3` | E(a) pass, E(b) pass | pass | yes | "Oct 2025 (same season as now) … 23.8%" |
| `X3-claude-forced-1` | pass | pass | yes | tabulates accuracy at 0.5 and says "That metric doesn't fit this decision" |
| `X3-claude-forced-2` | fail | pass | no | compares at the top 500; never mentions accuracy |
| `X3-claude-forced-3` | fail | pass | no | compares at the top 500; never mentions accuracy |
| `X3-claude-none-1` (block 1) | fail | pass | no | never mentions accuracy |
| `X3-claude-none-2` | fail | pass | no | never mentions accuracy |
| `X3-claude-none-3` | fail | pass | no | never mentions accuracy |

| Cell | Forced-load | No plugin | Condition result |
| --- | --- | --- | --- |
| X2 | 3/3 | 2/3 | both pass |
| X3 | 1/3 | 0/3 | both fail |

Every X3 arm in both conditions chose Model B and reported 302 against 173.
Median wall-clock: X2 forced 34 s against 31 s without; X3 forced 28 s against 17 s without.
