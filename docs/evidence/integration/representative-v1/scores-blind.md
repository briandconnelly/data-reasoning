# Representative suite v1: blind scores

Scorer: `openrouter/google/gemini-3.1-pro-preview` through amicus (harness `pi`, reasoning effort high), 2026-11-25; it ran no arm.
It scored E and C on all 40 arms from `blind-bundle.md`, where skill names, record names, links, and paths are redacted and arms are shuffled under IDs B01–B40.
It was given only that bundle and the E and C definitions from `prereg.md` § Scoring, in a directory holding nothing else.
The ID-to-arm key is `blind-key.json`; it was kept outside the repository until the scores were returned.
`scores-primary.md` was committed before this result was fetched.

## Result

The blind scorer agrees with the primary scorer on E and C for all 40 arms.

- C: pass on 40 of 40.
- E pass on every X1 arm (8) and E(a) pass on every X2 arm (8).
- E(b) fail on B29 (`X2-claude-none-1`) and B33 (`X2-claude-plugin-1`): neither reports the 23.8% origin.
- X3 E fail on B16 (`X3-codex-none-1`), B37 (`X3-codex-none-2`), B30 (`X3-codex-none-3`), B23 (`X3-claude-none-1`), and B34 (`X3-claude-plugin-1`): none says accuracy at a threshold is not the measure.
  The primary scorer marked `X3-codex-none-3` borderline and scored it fail; the blind scorer scored it fail outright.
- It used no borderline label.
