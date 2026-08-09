# Scenario 3 — Debugging-discrimination guard under the 2026-07-20 description, Rerun

Date: 2026-08-08.
Run: rerun of the owed S3 trigger-discrimination arm, paying Owed-measurements debt 1.
Supersedes `2026-07-18-scenario3-trigger-postdesc.md`, which scored the `aa1470e` wording, and predates the 2026-07-20 ungated description edit that the S18 section of `tests/scenarios.md` says supersedes the recorded S2, S3, S17, and S18 runs.
Model: Sonnet.
Catalog (stated, skill not named): hypothesis-driven-analysis + exploratory-data-analysis + systematic-debugging, per `dispatch-facts.md`.
Prompt: Scenario 3's failing test (`test_parse_dates` fails with `ValueError: unconverted data remains: Z` since commit abc123; "Fix it.").
Fixture: staged copy of `tests/fixtures/s3-bug/{dateutils.py,test_dateutils.py}`; `test_dateutils.py` sha256 `47279ba7b5d49cc6523c692a77d90bbdbe9e8881d08cdb51216050fe7a9b28b9` (matches the recorded value in the 2026-07-18 S17 evidence artifact).

| # | Assertion | Result | Evidence |
| --- | --- | --- | --- |
| 1 | The debugging skill (or plain debugging) handles it; hypothesis-driven-analysis does not activate. | PASS | Text block 1 (before any tool call): "I'll use the **systematic-debugging** skill since this is a reproducible test failure that needs root-cause diagnosis before a fix." Manifest ordinal 1 reads `systematic-debugging/SKILL.md`; no read of `hypothesis-driven-analysis/SKILL.md` anywhere in the manifest. |
| 2 | No investigation ledger is created for a reproducible software failure. | PASS | Write-tool scan of the manifest (machine-checked, planted positive validated — see evidence artifact) finds exactly one `Edit` (ordinal 7, the arm's own fixture copy `dateutils.py` — the fix), no `Write` of any ledger file; no hypothesis-driven-analysis ceremony anywhere in the text stream. |

Total: 2/2.

Fidelity note: this arm actually applied its fix (one `Edit`, ordinal 7, followed by re-running the reproduction case and `test_parse_dates` to verify), rather than only describing candidate fixes as the 2026-07-18 postdesc run did — permitted here because the dispatch confined writes to per-arm scratch directories and the edited file is the arm's own staged fixture copy, not the repository (confirmed clean by `git status --porcelain skills/`, see evidence artifact).
This is a substantive difference in *how* the arm worked, not a deviation from either scored assertion: no ledger was written either way.
One arm is consistency, not proof, that the carve-out held under the 2026-07-20 wording.
Cost: 9 tool calls; no token figure reached the scoring session (`dispatch-facts.md`), so none is recorded rather than reconstructed.
Evidence: `tests/runs/artifacts/2026-08-08-trigger-rerun-evidence.md`.
