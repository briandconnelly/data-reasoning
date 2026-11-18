# Blind second scores

Scorer: `openrouter/google/gemini-3.1-pro-preview` through amicus pi (job c25f737e12ec45f68980e1ba5d6a1a3c, reasoning high, $0.27), 2026-11-17.
Input: `blind-bundle.md` (final messages shuffled, skill names and record filenames redacted); unblinded with `blind-key.json` after the scores returned.
The scorer marked I1 E as PASS where the rubric says n/a; read as n/a.
Its borderline note: the three I3 answers that present a trend-adjusted range with caveats were scored E FAIL.

| Arm | Blind ID | E | C |
|---|---|---|---|
| I1-claude-none-1 | A28 | pass | pass |
| I1-claude-none-2 | A40 | pass | pass |
| I1-claude-none-3 | A41 | pass | pass |
| I1-claude-plugin-1 | A10 | pass | pass |
| I1-claude-plugin-2 | A31 | pass | pass |
| I1-claude-plugin-3 | A36 | pass | pass |
| I1-codex-none-1 | A43 | pass | pass |
| I1-codex-none-2 | A21 | pass | pass |
| I1-codex-none-3 | A11 | pass | pass |
| I1-codex-plugin-1 | A03 | pass | pass |
| I1-codex-plugin-2 | A39 | pass | pass |
| I1-codex-plugin-3 | A20 | pass | pass |
| I2-claude-none-1 | A08 | fail | pass |
| I2-claude-none-2 | A44 | fail | pass |
| I2-claude-none-3 | A23 | fail | pass |
| I2-claude-plugin-1 | A26 | pass | pass |
| I2-claude-plugin-2 | A35 | pass | pass |
| I2-claude-plugin-3 | A32 | pass | pass |
| I2-codex-none-1 | A27 | fail | pass |
| I2-codex-none-2 | A07 | fail | pass |
| I2-codex-none-3 | A47 | fail | pass |
| I2-codex-plugin-1 | A42 | pass | pass |
| I2-codex-plugin-2 | A33 | pass | pass |
| I2-codex-plugin-3 | A48 | pass | pass |
| I3-claude-none-1 | A01 | fail | fail |
| I3-claude-none-2 | A45 | fail | fail |
| I3-claude-none-3 | A38 | fail | fail |
| I3-claude-plugin-1 | A16 | fail | pass |
| I3-claude-plugin-2 | A24 | fail | pass |
| I3-claude-plugin-3 | A19 | fail | pass |
| I3-codex-none-1 | A06 | pass | fail |
| I3-codex-none-2 | A25 | pass | fail |
| I3-codex-none-3 | A04 | pass | fail |
| I3-codex-plugin-1 | A17 | pass | fail |
| I3-codex-plugin-2 | A30 | pass | fail |
| I3-codex-plugin-3 | A09 | pass | fail |
| I4-claude-none-1 | A12 | pass | pass |
| I4-claude-none-2 | A18 | pass | pass |
| I4-claude-none-3 | A22 | pass | pass |
| I4-claude-plugin-1 | A13 | pass | pass |
| I4-claude-plugin-2 | A15 | pass | pass |
| I4-claude-plugin-3 | A34 | pass | pass |
| I4-codex-none-1 | A02 | pass | pass |
| I4-codex-none-2 | A46 | pass | pass |
| I4-codex-none-3 | A29 | pass | pass |
| I4-codex-plugin-1 | A05 | pass | pass |
| I4-codex-plugin-2 | A37 | pass | pass |
| I4-codex-plugin-3 | A14 | pass | pass |
