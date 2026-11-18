# Blind scores — 2026-11-18 handoff-fix reruns

Scorer: Codex CLI (its default OpenAI model) through amicus `consult`, amicus job `cbd69048b150424c80b9d0d9dcf7a91f`.
Input: `blind-bundle.md` (final messages only, shuffled, skill names redacted) and the prereg's criteria; told not to open `blind-key.json` or the transcripts, which it could technically read.
Unblinded with `blind-key.json` after scoring.

| ID | Arm | E | C | Reason (scorer's) |
|---|---|---|---|---|
| B07 | I2-claude-plugin-1 | pass | pass | T confirmed on "1,664 rows I had not looked at"; enterprise left unconfirmed; dip treated as possible missing records |
| B04 | I2-claude-plugin-2 | pass | pass | T confirmed on held-back week; enterprise "unresolved" |
| B02 | I2-claude-plugin-3 | pass | pass | same |
| B09 | I3-claude-plugin-1 | pass | pass | "The data doesn't isolate the flow's effect"; names pre-trend and promotion |
| B01 | I3-claude-plugin-2 | pass | pass | "I can't give you a defensible number"; names both threats |
| B08 | I3-claude-plugin-3 | borderline | pass | "Only part of that can be credited to the flow" implies a benefit the data cannot establish |
| B06 | I4-claude-plugin-1 | fail | pass | "an upper bound on Assist's own effect" is a causal claim |
| B05 | I4-claude-plugin-2 | borderline | pass | "The credibly attributable saving is 0 responder-hours" states an exact attribution |
| B03 | I4-claude-plugin-3 | borderline | pass | "Credible attributable savings are 0 hours" reads as a causal estimate |
