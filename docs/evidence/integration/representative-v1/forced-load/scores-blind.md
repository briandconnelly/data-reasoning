# Forced-load diagnostic: blind scores

Scorer: `openrouter/google/gemini-3.1-pro-preview` through amicus (harness `pi`, reasoning effort high), 2026-11-25; it ran no arm.
It scored E and C on the 10 new arms from `blind-bundle.md` (skill, route, and record names and paths redacted; arms shuffled as F01–F10), given only that bundle and the E and C definitions.
`scores-primary.md` was committed before this result was fetched; the key is `blind-key.json`.

The blind scorer agrees with the primary scorer on E and C for all 10 arms.

- C: pass on 10 of 10.
- X2: E(a) pass on all 5; E(b) pass on 4 and borderline, leaning pass, on F02 (`X2-claude-none-3`), which the primary scorer passed.
- X3: E pass on F07 (`X3-claude-forced-1`) only; fail on F08 and F09 (forced arms 3 and 2) and on F03 and F06 (no-plugin arms 2 and 3).
