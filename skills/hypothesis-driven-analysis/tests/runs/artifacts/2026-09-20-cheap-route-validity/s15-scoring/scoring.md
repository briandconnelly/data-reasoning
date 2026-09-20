# S15 regression cell — full scoring of `s15-pre` and `s15-post` (issue #43)

Scored 2026-09-20, after the wave's run record shipped with this cell machine-checked on C1 only.
Two scorers worked separately against the catalog's S15 assertions (`../../../../scenarios.md` § Scenario 15, numbered 1–10 in the order listed): the dispatching session (Fable) and Codex through amicus (job `bc5aa000fbcb49269235ccc6f009699e`, `high` reasoning effort, read-only).
Codex's job was started before the Fable scoring was drafted, the Fable scoring was held in context and not written to disk until the job was terminal, and the framing sent to Codex carried no verdicts; Codex's return disagrees with Fable's on three pre-arm assertions, which is recorded below rather than averaged.
Paths in citations are relative to the archive directory one level up, so `../verify_quotes.py` resolves them.

## Recovered Plan-time ledgers

Both arms first wrote `ledger.md` at ordinal 8 of 15 (pre) and 8 of 12 (post).

- `s15-pre.plan-ledger.md`: the body of the `cat > ledger.md <<'E'` heredoc in the pre arm's ordinal-8 Bash command, plus the newline the heredoc supplies.
- `s15-post.plan-ledger.md`: the `content` of the post arm's ordinal-8 Write, byte for byte.

Each carries the full Hypotheses table, five Tests rows all `NOT_TESTED`, and "(pending)" under Conclusion, so neither first write is a stub.
Reproduce with `uv run python extract_evidence.py events --ordinal 8 runs/artifacts/2026-09-20-cheap-route-validity/<arm>.jsonl` from `tests/`.

## Instruments

Run from `tests/`, with `A=runs/artifacts/2026-09-20-cheap-route-validity`.
Known positive before trusting the C2 pass: the post plan with H4 relabelled `causal` makes `score_ledger.py` exit 1 with "H4 carries a data-artifact REFUTED but was causal at Plan time"; the three instruments' own suites pass (268 tests).

| Instrument | pre | post |
| --- | --- | --- |
| `score_ledger.py --final $A/<arm>.scratch/ledger.md --plan $A/s15-scoring/<arm>.plan-ledger.md` C1 | passed: 5 rows, 0 `REFUTED` | passed: 5 rows, 2 `REFUTED`, none causal |
| C2 | nothing to check (no `REFUTED` descriptive or data-artifact row) | checked and passed: H3 and H4 each traced to a Plan-time id and class, H3 naming its estimand there |
| C3, `--c3-unknown-source S2` | C3a and C3b passed, exit 0 | exit 1 at parse: the bullet reads "S2 (activity.csv): UNKNOWN" (s15-post.scratch/ledger.md) where the scorer requires `S2: UNKNOWN`; C3a is not reported on a parse failure, so C3 yields nothing for this arm |
| C4 | no `REFUTED` row, nothing to flag | `--c4-positive-contradiction H3`: passed, the row carries an `adequacy:` atom. With H4 flagged as well it fails for a missing atom; both scorers read H4 as a deterministic bound (every placement of the absent rows enumerated, s15-post.scratch/analysis3_out.txt) and therefore exempt |
| `check_prereg.py --ledger-pattern 'ledger\.md' --data-pattern 's15-assist-rollout\|\.csv'` on `extract_evidence.py manifest` output | exit 2, UNVERIFIABLE: no Write/Edit matches; Bash candidates named at ordinals 8, 13, 14, 15 | exit 1: `PREREG_WRITE: ordinal 8`, five earlier touches listed for classification |
| `compare_prereg.py --plan … --final …` | exit 1: 9 reworded Tests cells, none covered by a dated amendment | exit 1: 3 reworded Tests cells |

Two instrument limits showed, and neither is patched here.
C3a passed the pre ledger although its Conclusion says "H2 makes Assist look better than it should on means, not on the median." (s15-pre.scratch/ledger.md) with S2 declared `UNKNOWN` — an unconditional direction claim the syntactic check does not recognise.
C4 passed H3 on the presence of the atom alone; Codex reads "adequacy: 0 (deterministic prediction under this estimand)" (s15-post.scratch/ledger.md) as not earned, since a true composition mechanism can produce a larger reversed standardized difference, which is exactly what the arm's own Amendment 2 concedes.

## Pre-write touches (assertion 10)

Both scorers classify every call before ordinal 8 as orientation, in both arms.
Ordinals 1–2 read `SKILL.md` and the ledger template; 3 is a failed listing; 4 prints headers, row counts, and `staffing.csv`; 5 fails on `import pandas` before reading anything; 6 probes the interpreter; 7 counts rows, keys, orphans, and absent activity rows by workflow × group × severity, and date ranges.
No call before ordinal 8 relates workflow to time to close, responder minutes, handoffs, or reopens.
`staffing.csv` printed whole at ordinal 4 shows the capacity step, a co-exposure and not an outcome.

## Scored table

| # | Assertion | pre | post |
| --- | --- | --- | --- |
| 1 | Routes full; cutover does not identify the effect | PASS — "nothing identifies the effect; every co-occurring change is a live rival." (s15-pre.scratch/ledger.md) | PASS — "nothing identifies the causal contrast, and >=2 live explanations exist." (s15-post.scratch/ledger.md) |
| 2 | Causal Assist hypothesis stays `UNRESOLVED` (C1) | PASS | PASS |
| 3 | Every `REFUTED` descriptive row was a Plan-time row with an estimand (C2) | PASS, vacuously: no such row | PASS — H3 and H4; H3 "necessary prediction refuted as preregistered (magnitude wording, T3)" (s15-post.scratch/ledger.md) |
| 4 | Raw median decline correct for its estimand | PASS — "**The headline is real but comes from mix.**" (s15-pre.manifest.json) | PASS — "**The dashboard number is real.**" (s15-post.manifest.json) |
| 5 | Threats stay live; no causal winner | PASS | PASS |
| 6 | No direction from absent records without established semantics | **FAIL** (both scorers) — "**Missing rows erase it.**" (s15-pre.manifest.json), and the ledger line quoted under Instruments, beside the same memo's "can't be told from these files" | PASS — "I can't tell whether those incidents are still open, were never recorded, or were dropped from the export." (s15-post.manifest.json), with the all-placements bound beside the one robustness claim |
| 7 | No attributable hours as an identified effect | **scorers differ** — Fable FAIL, borderline: "**The credible attributable saving is zero, and the point estimate is negative.**" (s15-pre.manifest.json) under a headline reading "Assist did not cause faster recovery in this data" (s15-pre.manifest.json); Codex PASS, reading "zero" as "nothing bookable" given the memo's causal disclaimer | PASS — the memo says its recommendation is not a finding of harm: "the design can't establish that either." (s15-post.manifest.json) |
| 8 | Stop rule after every promised stratum, or a recorded deviation | **FAIL**, on Codex's finding, verified — the plan's T5 promises "sev1 contrast, bounds for missing, top-decile share" (s15-scoring/s15-pre.plan-ledger.md); no script computes a top-decile share, the final T5 cell drops it, and Amendments records nothing about it | PASS — all three severities, both groups, the daily series, and overall handoffs are in the outputs |
| 9 | Interprets the `handoffs` aggregation reversal | **FAIL** — the ordinal-9 output holds marginal 2.25 → 1.96 with sev2 3.01 → 3.95 and sev3 0.54 → 1.52; the memo reads sev1 only | **FAIL** — "handoffs mean 2.25" (s15-post.scratch/analysis2_out.txt) against 1.96, strata in `analysis_out.txt`; the ledger says "CONSISTENT (minutes); handoffs mixed" (s15-post.scratch/ledger.md) and the memo reads sev1 only |
| 10 | Plan-time ledger written before the first analysis query | **scorers differ**, because the instrument's contract says two things — its fail-closed note sends a Bash-written ledger to be "verified from the events stream and scored manually", and its exit-code list says of exit 2 "the preregistration assertion fails". Fable PASS on the first: the manual check finds a complete plan at ordinal 8 and only orientation before it. Codex FAIL on the second, in both its scoring and its step-7 review, while agreeing the preregistration is real. The assertion's own failing case, "a run with no mid-run ledger write", is not this arm | PASS |

Pre: 6/10 on either scorer's reading (Fable fails 6, 7, 8, 9; Codex fails 6, 8, 9, 10).
Post: 9/10 on both.

## Verdict

**Row 9 — shared catalog failure**, on assertion 9: the first row that applies governs, and both arms fail the same catalog assertion.
It is the debt the Tenth wave measured at 0/6 — the `handoffs` reversal is held in both arms' outputs and surfaced by neither — recorded in the catalog, not attributed to the change, and not blocking it.
Row 3 does not apply under either scorer's reading of 7 and 10: post fails no assertion that pre passes.
Post-only passes on 6 and 8 (and 7 or 10, by scorer) are unattributed differences at n=1 and are claimed as nothing.
Row 9 is terminal, so with this cell scored every cell of the wave ends on a terminal row.

This file is the home of the S15 result; the run record, the catalog's Seventeenth-wave entry, and decision 008 point here and carry only the row.

## What the join sentence did on this cell

The post plan's Data Validity carries "reconcile 420 = 409 matched + 11 unmatched." (s15-scoring/s15-post.plan-ledger.md), the draft § Plan sentence applied.
The reconciliation it names ran at ordinal 7, before the plan was written: 420 incidents, 409 activity ids, no orphans, 11 unmatched listed.
It is partial against the draft's own letter: activity rows are loaded into a dict keyed on `incident_id` before anything tests that key for uniqueness (uniqueness follows only from 409 dict entries equalling the 409 data rows counted at ordinal 4), and no total of `responder_minutes` is reconciled across the join.
It is also not new: the pre arm's ordinal 7 ran the same counts, orphan check, and matched/unmatched matrix with no sentence asking for them.
No promised work was displaced in post; the one dropped promise on this cell is pre's.
So on S15, as on S22a and S22c, the sentence changed what the ledger says and not what the arm did.

## `compare_prereg.py` differences, adjudicated

No current assertion's letter scores plan-versus-final immutability, as the Tenth wave recorded for arm e; the differences are recorded, not scored, except where one exposes dropped work (pre T5, scored under assertion 8).

- pre, substantive: T1 method ("incident bootstrap 5000" preregistered, `a1.py` runs 4000 and `a3.py` 1000) and prediction (the 95%-interval commitment removed from the cell); T2 prediction ("median/mean" became "mean" after the median turned out insensitive); T3 method; T4 method and prediction; T5 method and prediction (top-decile and handoffs removed, TTC substituted).
  T2 method is an elaboration inside the preregistered alternative.
  The pre arm also met the same T3 wording trap as post — a sign reversal its "smaller in magnitude" prediction did not anticipate — and recorded `CONSISTENT` with an undated post-hoc note, where post recorded `CONTRADICTED`, kept the prediction, and dated the amendment.
- post, cosmetic: T1 "95%" (already committed in the plan's prose), T3 "pooled mix, bootstrap" (already in the H3 row), T4 "absent".

## Step-7 review

Codex reviewed commit `1ee5c28` (`codex-step7-review.md`); its independent scoring is archived verbatim as `codex-independent-scoring.md`, since the amicus job record expires.

| Finding | Disposition |
| --- | --- |
| S15 is row 9, not row 10: "The first row that applies governs", and both arms fail assertion 9 | **Accepted.** The first version of this file, and Codex's own independent scoring, called the cell row 10 with assertion 9 set aside as row 9; the table has no per-assertion rows. Corrected here and in the three files that carry the row. Nothing downstream moves: row 9 is terminal and is not row 3. |
| Pre assertion 10 must fail for both scorers, making Fable's pre total 5/10 | **Declined, disagreement kept.** The contract is ambiguous in the way the table row now quotes, and a manual score is what one of its two sentences asks for. The totals stand at 6/10 for each scorer: the review's 5/10 presumes its own reading of 10. The ambiguity is filed as an instrument issue, not settled here. |
| The S15 result was restated in four files | **Accepted.** This file is the home; the others now carry the row and a pointer. |
| Is Codex's raw scoring durably retrievable? | **Accepted.** Archived beside this file. |
