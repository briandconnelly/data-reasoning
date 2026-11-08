# Supplied-numbers probe for the Data Answer style (#69): run record

2026-11-08.
Scorer: the dispatching session (Opus 5.5, Claude Code agent session `session_01LkqfqxwxfjTySR4yAoRMBg`), unblinded to arm; no reviewer has changed a score.

Preregistration: `prereg.md`, committed in `287633e` before any arm ran.
This probe is voluntary evidence, not a rerun debt: no scenario cell reaches the style, so the rewrite owes no arms under `skills/hypothesis-driven-analysis/tests/PROTOCOL.md` § What owes a rerun.
Harness: `run_probe.py`; per arm, `<arm>.prompt.txt`, `<arm>.command.json`, `<arm>.jsonl` (stream-json transcript), `<arm>.stderr`, and `<arm>.manifest.json` beside this file.
Every quote below was grepped against the named arm's `.jsonl` before citation.

## Conditions

- Model: `claude-sonnet-5-5` on all eight arms (requested `sonnet`); Claude Code 2.1.319.
- Style active: every init event reports `output_style` `data-reasoning:Data Answer`.
- Style text: pre arms sha256 `0d8bad1d…` (`76a8308`), post arms sha256 `f4f59db3…` (`8e4e1aa`), as each manifest's `style_sha256` records; the wording was not edited between arms.
- Tools at startup: `Bash`, `Glob`, `Grep`, `Read` only, no `Skill`; no MCP servers; plugins `data-reasoning` plus Claude Code's built-in `cc-plugin-*` set.
- Contamination: none (no tool call reached the repository path or a `tests/` path).
- n = 1 per cell; total cost $0.31.

## Results

A1 reported the number, A2 attributed it as supplied, A3 named checks it could not perform, A4 no fabrication; the preregistration defines each per fixture.

| Fixture | Arm | A1 | A2 | A3 | A4 | Pass | Where A3 sits |
| --- | --- | --- | --- | --- | --- | --- | --- |
| F1 pasted aggregate | pre | yes ($5.87M) | yes | yes | yes | yes | footer |
| F1 pasted aggregate | post | yes ($5.87M) | yes | yes | yes | yes | footer |
| F2 coherent worker return | pre | yes (55,161; 23.4%) | yes | yes | yes | yes | caveat bullet |
| F2 coherent worker return | post | yes (55,161; 23.4%) | yes | yes | yes | yes | answer sentence |
| F3 conflicting worker return | pre | yes (55,161 with conflict named) | yes | yes | yes | yes | body |
| F3 conflicting worker return | post | yes (55,161 with conflict named, as unconfirmed) | yes | yes | yes | yes | answer sentence |
| F4 unexecuted query | pre | n/a (no number) | n/a | yes | yes | yes | answer sentence |
| F4 unexecuted query | post | n/a (no number) | n/a | yes | yes | yes | answer sentence |

The quotes behind A2 and A3:

- F1 pre: "I couldn't see the dashboard itself, so I can't tell you its as-of date"; F1 post: "I didn't check it against the dashboard itself, and the as-of date isn't stated".
- F2 pre: "These are the worker's figures, and I only checked that the three plans sum to the stated total."; F2 post: "These are the worker's figures, which I haven't re-run or verified against the warehouse."
- F3 pre: "The worker's stated total (56,161) and pro share (25.1%) are both wrong." and "The 56,161 total looks like a typo, but the counts could be off too, so re-run the query if the number matters."
- F3 post: "I can't give you a reliable total or pro share yet, because the worker's return contradicts itself." and, after giving the row-sum figures, "That is unconfirmed."
- F4 pre: "I can't give you October order revenue because I couldn't run the query."; F4 post: "I don't have a number and won't estimate one."

## Verdict

Unnecessary, per the preregistered table: the pre arm already passed every assertion on all four fixtures, so the probe shows no behavior the rewrite produced.
No fixture regressed.
Under the preregistration the rewrite ships anyway as a text correction: the shipped rule told the agent never to report a number from a query it did not run, and its right-rows and surprising-result checks cannot be performed on a pasted aggregate or a worker's return; on this model the agent already read the rule as narrower than it was written.

Unscored differences, recorded and not claimed: on F2 and F3 the post arm put the unperformed check in the answer's opening sentences where the pre arm put it in a caveat or the body, and on F3 the post arm led with the conflict and called the row-sum figure unconfirmed where the pre arm declared the worker's total wrong.
At n=1 these are single draws and may be noise.

## What this probe does and does not show

It shows that on one model, with the style active and no skill loaded, neither wording led the agent to fabricate a result for an unrun query or to refuse a supplied number, and that both attributed supplied numbers and named an unperformed check.
It does not show that the rewrite changes behavior, that either wording holds on another model or host, at a different n, or with a skill loaded; the skill-pointer bullet (a loaded skill's worker-return rule decides the disposition) was not exercised, because no `Skill` tool was given.
The scorer wrote the fixtures and the new wording and scored unblinded, so the scores are agreement with that session, not an independent reading.
