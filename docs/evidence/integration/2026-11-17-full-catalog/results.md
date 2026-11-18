# Full-catalog routing and end-to-end handoffs — results

Issue #96; design in `prereg.md` beside this file, scored as preregistered.
Ran 2026-11-17 on `feat/96-full-catalog-routing`: Claude Code arms and Codex canaries at `1f13345`, scored Codex arms at `7e18ddb` (the harness fix); no plugin file differs between the two.
Hosts and models, from each `arms/*.manifest.json`: Claude Code with `claude-sonnet-5-5`; Codex CLI with `gpt-6.2-sol` (its default, read from the session rollout).
48 scored arms, all exit 0; 8 canaries in `canaries/`, excluded from scoring.
Primary scores: `scores-primary.md` (unblinded). Blind scores: `scores-blind.md` (`openrouter/google/gemini-3.1-pro-preview`, from `blind-bundle.md`, unblinded with `blind-key.json`).

## Route (R)

Counts are plugin arms taking the designed route, of 3; no-plugin arms loaded no skill in any cell, on either host.

| Cell | Designed route | Claude Code | Codex |
|---|---|---|---|
| I1 | none | 3/3 (none loaded) | 3/3 (none loaded) |
| I2 | EDA → HDA | 0/3 (EDA only, 3/3) | 2/3 with both records; 1/3 read both, wrote the exploration log only |
| I3 | HDA → CIR | 0/3 (HDA only, 3/3; no ledger) | 3/3, ledger and identification review each |
| I4 | HDA → (CIR) → DA | 0/3 (none 2/3, HDA only 1/3) | 1/3 with ledger, review, and memo; 2/3 read all three skills, wrote a memo only |

Claude Code made no multi-skill handoff in 12 plugin arms.
Codex read every skill of the designed route in 9 of 9 I2–I4 plugin arms, usually several `SKILL.md` files in one shell `cat`, and wrote each skill's record in 6.

## Evidence boundary (E) and task (C), counts of 3

| Cell | Host | E plugin | E none | C plugin | C none |
|---|---|---|---|---|---|
| I1 | both | n/a | n/a | 3 | 3 |
| I2 | Claude Code | 3 | 0 | 3 | 3 |
| I2 | Codex | 3 | 0 | 3 | 3 |
| I3 | Claude Code | 0 (+1 borderline) | 0 | 1 | 0 |
| I3 | Codex | 3 | 3 | 0 | 0 |
| I4 | Claude Code | 3 | 3 | 3 | 3 |
| I4 | Codex | 3 | 3 | 3 | 3 |

Primary scores shown; the blind scorer agreed on every E cell except I3-claude-plugin-3, which it scored fail (primary: borderline), and differed on C for I3-claude-plugin-1 and -2 (blind pass, primary fail: both give a number range as the answer, which the preregistered C excludes, while also naming what a cleaner design needs).
U, scored only on Codex (the only host that handed off), passed on every handoff: 9 of 9 arms.

What drove each I2 result: every no-plugin arm, on both hosts, called T confirmed from the same rows it was found in, and every Codex no-plugin arm also called D "held up"; every plugin arm, on both hosts, reserved a late window before checking T and reported D as not persisting.
On I3 every Claude Code arm, with or without the plugin, offered a trend-adjusted number (31–43 s) for the review, and four of the six set the same-day promotion aside as unlikely to affect completion time; no Codex arm gave the flow an effect size.
No arm on either host stated what data would identify the effect without also offering a number, so I3's C fails almost everywhere as preregistered.

## Reachable outcome

Outcome 7, mixed by host; no claim pools them.

- **Codex:** outcome 1 on I2 (designed route; E 3/3 against 0/3), outcome 2 on I3 and I4 (designed or partial route; E matches no-plugin, which already held), and no task regression on any cell, I1 included.
- **Claude Code:** outcome 3 on I2 (handoff skipped; E 3/3 against 0/3 from exploration alone), outcome 6 on I3 (handoff skipped and E broken; no-plugin breaks it too), outcome 3 on I4 (no skill or one; E holds in both conditions), no task regression on any cell.

The integration evidence #96 asks for — an agent choosing the route, keeping the boundary across the handoff, and finishing the task — exists for Codex on I2 and I3 at n=3.
For Claude Code the handoff remains unmeasured in practice: the one gain observed (I2) came from a single skill, and on I3 the investigation skill loaded without the identification review that would have stopped the number.

## Limits

- Fixed in advance: one model per host; Codex plugin arms ran without the record-checking hook, which needs `/hooks` trust; primary scoring is unblinded and the blind scorer is blind to condition only as far as redaction holds (host style is visible).
- Codex's route is read from file reads; a batched `cat` of several `SKILL.md` files shows the skill text entered context, not that each skill was followed, so the records each arm wrote are reported beside it.
- Three harness defects found by the Codex canaries were fixed before any scored Codex arm (`prereg.md` § Notes after writing); Claude Code routes were recomputed with the fixed extractor and did not change.
- n=3 per cell per condition: counts, not rates.
