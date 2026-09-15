# Scenario 9 — Estimation route data-validity inheritance, 2026-09-15 remediation wave

Preregistration: `artifacts/2026-09-15-remediation-wave-prereg.md` (cells, added assertions S9.4a–b, verdict table, amendment 1).
Design review: `artifacts/2026-09-15-remediation-wave/design-review.md`.
Harness: `../run_arm.py`; every arm's prompt, command, transcript, manifest, and written files are under `artifacts/2026-09-15-remediation-wave/` as `s9-baseline.*`, `s9-pre.*`, `s9-post.*`.
Model: `claude-sonnet-5` on every arm (manifest `model`); Claude Code 2.1.272; no contamination hits on any arm.
Fixture: `tests/fixtures/s9-ab/signups.csv`, sha256 in each manifest under `fixture_files_sha256`.
Skill under test: pre = `skills/hypothesis-driven-analysis/SKILL.md` at `main` (284ca3d); post = this branch's working tree at the time of the run (sha256 of every staged skill file in the manifests' `skill_files_sha256`).
Scorer: the dispatching session (Fable); every quote below was grepped against the named archive file with `artifacts/2026-09-15-remediation-wave/verify_quotes.py`.

## Scored table

| # | Assertion | baseline | pre | post |
| --- | --- | --- | --- | --- |
| S9.1 | Routes estimation: estimand, population, uncertainty statement, practical threshold | FAIL — rates, a CI, and a z-test, but no estimand or population statement, and significance stands in for a threshold: "significant at the standard 0.05 threshold" (s9-baseline.manifest.json) | PASS — "Estimand: difference in signup conversion rate (signups/visits), B minus A" and "Practical threshold: not stated by user" (s9-pre.scratch/estimation-record.md) | PASS — "Estimand: the per-visitor signup-rate difference (B − A) and relative lift" and "Practical threshold: not stated by the user." (s9-post.scratch/estimation_ledger.md) |
| S9.2 | No causal "why" hypotheses, no full PPDAC ledger | PASS — three tool calls, an analysis script and its output, no hypotheses | PASS — "this was a straightforward estimation problem, not a multi-hypothesis investigation" (s9-pre.manifest.json); one estimation record written, no hypothesis table | PASS — "this is a magnitude/comparison question, not a multi-hypothesis diagnosis" (s9-post.scratch/estimation_ledger.md); one estimation record, no hypothesis table |
| S9.3 | Estimate with uncertainty, not a bare point | PASS — "95% CI on the absolute difference:** [0.15, 1.12] percentage points" (s9-baseline.manifest.json) | PASS — "95% CI: +0.14pp to +1.13pp" (s9-pre.manifest.json) | PASS — "95% CI on the absolute difference: approximately **+0.1 to +1.1 percentage points**" (s9-post.scratch/estimation_ledger.md) |
| S9.4a | Coverage of the analysis population recorded | FAIL — balance of visits between arms is noted, cell coverage is not | PASS — "28 rows = 14 days x 2 variants (2026-07-01 .. 2026-07-14), no missing variant-days (checked)." (s9-pre.scratch/estimation-record.md); field population not stated | PASS — "Coverage matrix (date × variant, the grain the estimate uses): 14 dates × 2 variants = 28 cells expected; 28 present." and "`visits` and `signups` are populated (non-null, positive integers) in all 28 rows." (s9-post.scratch/estimation_ledger.md) |
| S9.4b | What an absent day or unrecorded visitor would mean is stated (UNKNOWN accepted) | FAIL — not addressed | FAIL — the record notes that no SRM check is possible without visitor-level logs, which is about randomization, not completeness; nothing says what an absent record would mean | PASS — "Source completeness semantics: `data/signups.csv` — UNKNOWN. No export contract, sentinel row, or independent denominator was available" (s9-post.scratch/estimation_ledger.md) |

Totals: baseline 2/5, pre 4/5, post 5/5.

## Verdict for the cell

Row 4 of the preregistered table, **reaches behavior**: post passes both added assertions and pre fails S9.4b.
No regression: post passes every catalog assertion pre passes.
Skill needed on this cell: yes on S9.1 (baseline fails, both skill arms pass), unchanged from 2026-07-16.

The changed sentence — the estimation route inheriting § Plan's coverage matrix and § Analysis's completeness semantics — is measured as reaching behavior at n=1 on one model.
The pre arm shows the pre-edit route already produced a coverage count when the fixture is tidy; what the sentence added is the completeness-semantics statement, which pre did not make and post made as `UNKNOWN`, the honest reading for a daily aggregate.

## Correctness and cost

All three arms report B − A = +0.63pp (4.77% vs 4.14%) with a 95% interval of roughly [+0.15, +1.12]pp, matching the fixture's ground truth and the 2026-07-16 and 2026-08-10 runs.

| arm | tool calls | output tokens | wall clock |
| --- | --- | --- | --- |
| baseline | 3 | 3,595 | 40 s |
| pre | 8 | 5,439 | 71 s |
| post | 8 | 11,112 | 134 s |

The post arm's record is longer: it carries the Data Validity block the sentence now requires.
That is the sentence's context cost on this cell, and it is measured here, not assumed.

## What this does not show

n=1 per arm, one model, one day.
The S9 fixture is complete by construction, so S9.4a tests whether coverage is recorded, not whether a hole is found; the sentence's value on a fixture with a hole is unmeasured.
The 2026-08-10 Sonnet run scored the pre-edit wording 3/3 on S9.1–S9.3; this wave's pre arm agrees, so that result stands for the catalog assertions and this record supersedes nothing.
