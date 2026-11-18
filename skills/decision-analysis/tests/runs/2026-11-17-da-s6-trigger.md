# DA-S6 — bare forecast handoff (#98)

2026-11-17.
Scorer: the dispatching Claude Code session (Opus), unblinded; the same agent wrote the #98 change and scored these arms.
Not preregistered: the arms were run after the change and its DA-S6 criteria were written, and scored against those criteria.
Model: `claude-sonnet-5-5` on every arm; Claude Code 2.1.327; exit 0 on every arm.
Prompt: "What's the probability churn exceeds 5% next quarter?" (`artifacts/2026-11-17-da-s6/scenario-prompt.txt`), with no data.

## Arms

- **with-skill pre ×3** (`da-s6-pre-*`): `../../hypothesis-driven-analysis/tests/run_arm.py`, `decision-analysis` staged from `dev` `a5a2652`, which asked "what decision would this inform?" before routing; an empty placeholder fixture; no contamination hits.
- **with-skill post ×3** (`da-s6-post-*`): the same harness, staged from `3405fc8`, the wording in this pull request; no contamination hits.
- **trigger ×3** (`da-s6-trigger-*`): `claude -p` in an empty temporary directory with `--setting-sources project` and `--plugin-dir` at `3405fc8`, so all four skills were discoverable through the Skill tool; the init event lists them. `run_arm.py` stages one skill, so this arm used its own command, archived as `da-s6-trigger-*.command.txt`, and had no contamination scan.

## Scored table

H: the response hands toward `hypothesis-driven-analysis` in the same response (or that skill was activated directly) without waiting on a clarifying question. N: no probability, posterior, or decision record from `decision-analysis`.

| Arm | Skill activated | H | N | Notes |
| --- | --- | --- | --- | --- |
| pre-1 | (staged) | fail | pass | Handoff only conditional: the forecast "goes through `hypothesis-driven-analysis`" if the user "just want[s] the forecast" |
| pre-2 | (staged) | fail | pass | Leads with "**What decision would this inform?**"; handoff is the fallback "If there is no decision" |
| pre-3 | (staged) | fail | pass | Treats the question as the method's step: "The method's one question here is: **what decision would this number inform?**" |
| post-1 | (staged) | pass | pass | "**Handoff to `hypothesis-driven-analysis`:**", with the decision question alongside; leaves causal routing to the receiving skill |
| post-2 | (staged) | pass | pass | "I've handed it off there. That skill should pick its own route" |
| post-3 | (staged) | pass | pass | "What to send to `hypothesis-driven-analysis`", with the invitation to name a decision after it |
| trigger-1 | none | fail | pass | No skill invoked; asks for data, and offers an illustrative "roughly a 10–15% chance" for hypothetical inputs |
| trigger-2 | none | fail | pass | No skill invoked; asks for data and gives a formula |
| trigger-3 | none | fail | pass | No skill invoked; asks for data |

## Reading

With `decision-analysis` loaded, the new wording moved the handoff from conditional to immediate, 0/3 to 3/3, with no arm producing a probability in either wording.
At n=3 per arm, unblinded and not preregistered, this is directional evidence for the wording, not a measured lift.
On the trigger arms `decision-analysis` correctly stayed unselected, 3/3, but `hypothesis-driven-analysis` was not activated either: the agent asked for data without loading any skill, matching the 2026-09-24 Jev pilot's majority prediction of no skill (`jev/pilot/2026-09-24/routing.md`).
DA-S6's handoff assertion therefore fails on the trigger condition; whether a data-less bare forecast should activate `hypothesis-driven-analysis` at all is that skill's description question, not this change's.
