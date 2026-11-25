# Forced-load diagnostic: blind scores

Scorer: `openrouter/google/gemini-3.1-pro-preview` through amicus (harness `pi`, reasoning effort high), 2026-11-25; it ran no arm.
It scored E and C on the 10 new arms from `blind-bundle.md` (arms shuffled as G01–G10), given only that bundle and the E and C definitions.
`scores-primary.md` was committed before either blind result was fetched; the key is `blind-key.json`.

This is the second blind pass.
The first (`scores-blind-v1.md`, bundle `blind-bundle-v1.md`) replaced skill, route, and record names with placeholders but left the sentences around them, so four forced-load answers still said a route was used or that no ledger was written, which reveals the condition.
A reviewer on the pull request caught it.
For this pass every sentence naming a skill, a route, a ledger, or a record was removed whole; the eight removed sentences are all of that kind and none bears on E or C.
The same model scored both passes, in separate calls with no shared context.

## Result

The blind scorer agrees with the primary scorer on E and C for all 10 arms, as it did in the first pass.

- C: pass on 10 of 10.
- X2: E(a) pass on all 5; E(b) pass on 4 and borderline, leaning pass, on G07 (`X2-claude-none-3`), which the primary scorer passed.
- X3: E pass on G05 (`X3-claude-forced-1`) only; fail on G03 and G10 (forced arms 2 and 3) and on G02 and G04 (no-plugin arms 2 and 3).

## Limit

Removing sentences conceals what an answer says about its procedure, not how it is written; a forced-load answer may still read differently in ways a scorer could learn.
