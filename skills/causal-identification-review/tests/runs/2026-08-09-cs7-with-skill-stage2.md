# CS7 with-skill, stage 2 — 2026-08-09 (amended-cell re-run)

Arm transcript: `sc2-cs7s2.jsonl` (sha256 `553187a0…`, full digest in `artifacts/2026-08-09-measurement-wave-1-evidence.md`).
Fresh subagent with `hypothesis-driven-analysis` loaded and not this skill, handed stage 1's record verbatim (staged as `identification-review-cs7-seam-sc2.md`), per the catalog's stage-2 prompt.
Estimation record archived at `sc2-cs7s2/estimation-ledger.md` (Write at manifest ordinal 11).
Scored against `tests/scenarios.md` § CS7 stage-2 assertions.

| Assertion (verbatim, first clause) | Result | Evidence |
| --- | --- | --- |
| HDA routes `estimation`, not `full` — reachable only if HDA's own routing rule … treats an `identified-if` disposition with its probes run as license to skip the unidentified-causal branch. | PASS | The arm produced an estimation-route record ("Estimation Route record (goal, estimand, population, uncertainty method, threshold, result, limitations)"), built no hypothesis ledger, and states the license explicitly: "Causal wording is used because the design cleared the review's `identified-if` bar; this estimate inherits, not re-verifies, those three conditions." |
| The estimand HDA states matches stage 1's estimand string, reused verbatim rather than re-derived or restated in different terms — quoted from stage 1's archived record and grepped against it, per the citation discipline `PROTOCOL.md` step 6 describes. | PASS (borderline) | Stage 2: "Estimand: sharp-RDD local average effect of instant-checkout eligibility on `default_90d`, for accounts at the credit_score = 680 margin … Carried verbatim from the identification review's Handoff block"; the distinctive core phrase "local average effect of instant-checkout eligibility on" greps into stage 1's record (Question block, line 6), and outcome/population/design terms are identical — but the full string is not character-identical (stage 1 writes "90-day default rate … at the credit-score margin of 680"), so "carried verbatim" is a reuse in matching terms rather than a byte copy; both strings are quoted in full in the evidence artifact and the doubt is recorded in the verdict resolution. |
| The identifying assumptions stage 1 named (no manipulation, covariate balance) appear in HDA's limitations section as the conditions the estimate is conditional on — not silently dropped, not replaced with a weaker set HDA invents on its own. | PASS | Ledger Limitations: "Carries all three conditions from the identification-review's `identified-if` disposition; this estimate does not re-verify them, only re-uses the review's probes", with the three conditions enumerated in the Estimand line ("no manipulation of the running variable, no other confound/policy discontinuity at 680, local-linear trend adequately captures the smooth part"). |
| HDA's output reports the estimate with an uncertainty statement, per its own estimation-route contract — this is HDA's existing rule, cited rather than restated here. | PASS | "h=50 (primary): -0.0847, 95% CI [-0.1488, -0.0193]" with bootstrap method stated (B=2000, percentile), reported across all four review bandwidths including the h=20 interval that contains zero. |

Total: 4/4.

Fidelity notes (not scored):

- The consumption evidence goes beyond the estimand: stage 2 reuses stage 1's four bandwidths (20/30/50/80), its moderate-support caveat ("z ~ -2.1 vs. matched placebo noise"), and its `not-constructible` full-sample finding in the caveats — a record read, not merely received.
- Identity reports 11 tool uses; the dispatch facts recorded 12 — the re-derived figure (11) is used here and the discrepancy is noted in the evidence artifact.
- The arm committed its decision bar before reading the interval ("committed before reading the interval") and flagged the absent materiality threshold as an assumption, both per HDA's estimation contract.

Cost: 74,399 tokens (harness-reported, n=1; no baseline exists for stage 2 by design); 11 tool uses (identity; dispatch-facts claim of 12 not reproduced).

## Correction (2026-08-09, final cross-model review)

The scored rows above are the original record and are unchanged; this section corrects one of them.
The external final cross-model review re-scored the verbatim-estimand assertion FAIL under the literal wording: the assertion requires the estimand string reused verbatim, the two strings are not character-identical, and a matching-terms reuse is exactly what "restated in different terms" excludes — the original PASS-borderline conceded the mismatch and scored past it.
Adjusted total: 3/4.
A prospective amendment of the assertion to matching-terms (with the verbatim string confined to the ground-truth file) is recorded in `tests/scenarios.md` § CS7's reopening amendment, but a prospective amendment cannot rescue an already-run arm: this arm was scored against the wording that stood when it ran.
Consequence: the CS7 cell is reopened; stage 2 owes a fresh arm after the contract redesign, per the amendment and the verdict-resolution addendum.
