# Codex's step-7 review of commit 1ee5c28 — verbatim return

amicus job `37acbc1c24ce44608a529a9d1e2bc1fa` (`amicus_review_changes`, scope `commit`, backend `codex`), 2026-09-20T22:15Z.
The text below is the backend's return unedited; dispositions are in `scoring.md` § Step-7 review.

Verdict: `concerns`, confidence `high`, coverage `complete`.

## Summary

The evidence supports closing the wave, but the recorded S15 verdict and one scorer total are incorrect. S15 should be row 9, not row 10; row 9 is terminal, so the wave still closes and the preregistered S22a–c row-5 rule still yields “nothing ships as measured.” No security issues found.

## Findings

- **S15 is row 9 under the preregistered first-applicable-row rule** (medium; `skills/hypothesis-driven-analysis/tests/runs/artifacts/2026-09-20-cheap-route-validity/s15-scoring/scoring.md`:63)
  Evidence: The preregistration says “The first row that applies governs” and defines row 9 when pre and post fail the same catalog assertion. Scoring lines 55 and 64 establish that both arms fail assertion 9, so row 9 applies before row 10. The row-10 label is then copied into the run record and scenarios.md.
  Suggestion: Record S15 as “9 — shared catalog failure.” Update the run record and scenario catalog accordingly. State that the wave still closes because row 9 is terminal and S15 has no row 3.
- **Assertion 10 is a mandatory failure for the pre arm, not a scorer-dependent PASS** (medium; `skills/hypothesis-driven-analysis/tests/runs/artifacts/2026-09-20-cheap-route-validity/s15-scoring/scoring.md`:56)
  Evidence: The catalog says assertion 10 is machine-established by check_prereg.py. The reproduced command exits 2 with “UNVERIFIABLE,” and the checker’s documented contract says exit 2 means the preregistration assertion fails. Scoring line 32 acknowledges that result, but line 56 nevertheless gives Fable a manual PASS. Consequently, line 58’s claim that both scorers give pre 6/10 is wrong: with Fable’s assertion-7 failure, Fable scores pre 5/10; Codex scores it 6/10.
  Suggestion: Mark assertion 10 FAIL for both readings, retain only the assertion-7 disagreement, and update the pre totals wherever copied. This does not alter the row-9 verdict.
- **The S15 result is copied into several homes** (low; `skills/hypothesis-driven-analysis/tests/scenarios.md`:1457)
  Evidence: The detailed result originates in s15-scoring/scoring.md but the exact totals, row number, and shared assertion failure are restated in the run record and scenarios.md, while decision 008 separately restates the no-regression conclusion. The incorrect row-10 classification demonstrates the maintenance risk because every copy now requires coordinated correction.
  Suggestion: Make scoring.md the result authority. Have the run record, scenario catalog, and decision record point to it and state only the local consequence needed by each document.

## Questions

- Is the raw Codex/amicus review for job bc5aa000fbcb49269235ccc6f009699e durably retrievable? Only the synthesized account appears in the repository, so the claimed independent scoring cannot be reconstructed solely from this archive.

## Assumptions

- The recovered Plan-time ledgers were treated as immutable evidence; their hashes match the ordinal-8 transcript content exactly.
- The preregistered S22a–c row-5 rule and the S2 row-3 component blocker are cumulative, not conflicting.

## Next steps

- Correct S15 to row 9 in the scoring authority.
- Correct assertion 10 and the pre-arm totals.
- Replace copied result details with pointers to the scoring authority.
