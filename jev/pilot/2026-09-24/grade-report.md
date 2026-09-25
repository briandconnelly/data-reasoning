# Jev second-scorer report: 2026-09-24 pilot: Codex blind questions against the agent-scored 2026-09-15 and 2026-09-20 waves

Model jev-1.13.0; questions 52581cbad2cf8514; abstain band [0.4, 0.6]; 82544 input tokens.
Reference scorer: the dispatching session (Fable), with the cross-model (Codex) review corrections the run records note; not a human.

Counts (control): agree 6
Counts (reference): abstain 3, agree 38, disagree 8

## For a person to read

Disagreements and abstentions are where the rubric text, the reference, or Jev may be wrong.
Read the arm before deciding which.

| arm | item | kind | reference | Jev p(pass) | status |
| --- | --- | --- | --- | --- | --- |
| s9-pre | S9.4a | reference | PASS | 0.26 | disagree |
| s9-pre | S9.4b | reference | FAIL | 0.75 | disagree |
| b10-baseline | B10.5b | reference | FAIL | 0.97 | disagree |
| b10-pre | B10.5b | reference | FAIL | 0.97 | disagree |
| b10-pre | B10.5c | reference | PASS | 0.41 | abstain |
| b10-post | B10.5b | reference | FAIL | 0.96 | disagree |
| b10-post | B10.5c | reference | PASS | 0.58 | abstain |
| da-s1-post | DA-S1.5a | reference | FAIL | 0.62 | disagree |
| da-s8-pre | DA-S8.2 | reference | PASS | 0.21 | disagree |
| da-s8-post | DA-S8.4 | reference | PASS | 0.55 | abstain |
| w2-da-s8-post | DA-S8.4 | reference | FAIL | 0.62 | disagree |
