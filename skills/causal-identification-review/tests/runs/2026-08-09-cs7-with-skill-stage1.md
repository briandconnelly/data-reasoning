# CS7 with-skill, stage 1 — 2026-08-09 (amended-cell re-run)

Arm transcript: `sc2-cs7-ws.jsonl` (sha256 `a87e93d6…`, full digest in `artifacts/2026-08-09-measurement-wave-1-evidence.md`).
Skill loaded from the staged copy (SKILL.md byte-identical to c5f4755); fixture includes the amended `data_notes.md` no-bundled-policy fact.
Record archived at `sc2-cs7-ws/identification-review-cs7-seam.md` (Write at manifest ordinal 17, the final tool call).
This arm re-measures the cell after the 2026-08-09 CS7 amendments; the first-wave `sc-cs7-ws` arm is archived-unscored.
Scored against `tests/scenarios.md` § CS7 stage-1 assertions (amended).

| Assertion (verbatim, first clause) | Result | Evidence |
| --- | --- | --- |
| Produces a template-shaped record … naming the causal question as a counterfactual contrast, the estimand, the design (regression discontinuity), its identifying assumptions, and the probes run against them. | PASS | Record carries the full Question block ("would an account's 90-day default outcome differ had it been offered instant-checkout versus not"), the estimand, "Design: Regression discontinuity, sharp, running variable = `credit_score`, cutoff = 680", three identifying assumptions, and a five-row probe table with run results. |
| Both probes (no manipulation, covariate balance) are reported as run and passing, not merely proposed. | PASS | Probe rows: manipulation — "windowed ratios (1.12, 1.08, 0.93, 0.79) show no spike or discontinuity in density right at the cutoff — no evidence of bunching/sorting"; covariate balance — "income jump at 680 = −147 vs. placebo mean −69 (sd 335): z ≈ −0.23; tenure … z ≈ −0.49. Both well inside placebo noise". |
| Disposition recorded is `identified-if` per SKILL.md … — the one scenario in this catalog where that disposition is the documented ground truth. | PASS | Record: "Disposition: \`identified-if\` — conditional on (a) no manipulation …, (b) no other confound or policy discontinuity …, (c) the local-linear trend adequately captures …"; the arm cites the amended `data_notes.md` fact and probes the `eligible` field at placebo cutoffs to check it as far as the extract allows. |
| No causal point estimate appears in stage 1's own output — effect estimation is explicitly out of this skill's scope (D5) and is left for stage 2. | PASS | No effect estimate is presented as the effect; the record closes "This record does not estimate the effect … Producing the point estimate … is estimator mechanics and is out of this skill's scope; that work routes to `hypothesis-driven-analysis`'s estimation route." Local-linear outcome-jump magnitudes (−0.093 to −0.069) do appear, but as the non-flatness/noise-floor probe's own statistics with an explicit refusal to read them as the estimate — see the fidelity note. |
| Route recorded is `construct` — the prompt states assignment facts … but claims no design as evidence … | PASS | Record: "Route: \`construct\` — a causal question with no design proposed by the requester, plus a stated fact about how the exposure was assigned … `review` does not apply because no design was presented for vetting — the user asked what the cutoff gives us, not to bless a claimed comparison" — the amended (canary-corrected) expectation, reasoned from the routing conditions. |

Total: 5/5.

Machine gate: `check_review.py` exits 1 with nine findings — the Route and all three Disposition tokens are backtick-wrapped (`` `construct` ``, `` `identified-if` ``, `` `not-constructible` ``) and fail the closed-set string match; the named-only prospective-experiment block lacks the assumptions sub-list and probe/threat tables; Handoff Facts and Dispositions are indented sub-lists where the checker requires inline values.
Every finding is a formatting/parse mismatch (the semantic tokens and reuse are correct on manual read); adjudicated in the verdict resolution.

Fidelity notes (not scored):

- The probe table reports the outcome discontinuity's local-linear gaps and their placebo-sweep z-scores; a stricter reading could call these magnitudes a point estimate in stage 1's output, but the fixture's own entanglement note requires the discontinuity to be verified non-flat, that verification is impossible without computing the gap, and the record explicitly refuses to promote it — the doubt is recorded here and in the verdict resolution rather than silently resolved.
- `check_review.py`'s advisory numeric scan did not flag these gaps (raw proportions carry no %/pp unit), a documented heuristic limitation worth remembering when reading gate output.
- The record honestly bounds what the extract can confirm about the amended no-bundled-policy fact: "a source assertion beyond what this extract's fields can independently confirm for pricing/underwriting rules not present in the data".

Cost: 68,732 tokens (harness-reported, n=1; +66.5% over the 41,272-token baseline); 17 tool uses (identity).
