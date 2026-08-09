# CS5 with-skill — 2026-08-09

Arm transcript: `sc-cs5-ws.jsonl` (sha256 `315c3e4c…`, full digest in `artifacts/2026-08-09-measurement-wave-1-evidence.md`).
Skill loaded from the staged copy at c5f4755; record archived at `sc-cs5-ws/identification-review-cs5-bounds.md` (Write at manifest ordinal 10, the final tool call).
Scored against `tests/scenarios.md` § CS5.

| Assertion (verbatim) | Result | Evidence |
| --- | --- | --- |
| The assumption ledger — the monotonicity direction and the trimming logic it licenses — is written before any endpoint number appears in the record. | PASS | The record's Bound block orders "Assumption ledger:" (randomization, then "Monotonicity of attrition, stated in the source as a fact of the fixture … invitation can only keep a customer observed longer, never shorten the observation window") before "Bound logic:" before "Computed endpoints: **-0.0194, 0.2736**"; the record was written in a single post-analysis Write, so document order is the record's order. |
| The computed lower and upper endpoints match the fixture's documented ground-truth bounds (exact match, or within a stated numeric tolerance the validator sets). | PASS | Record endpoints -0.01937 / +0.27361 match `cs5-bounds-ground-truth.md` (lower -0.019370, upper 0.273608) to the reported precision; the record's arithmetic (203/413, 324/413, 211/413) reproduces the trimming construction. |
| No causal point estimate appears anywhere in the output — not a naive difference-in-means reported as "the effect," not a midpoint of the bound presented as a best guess; only the interval, framed as a range under the stated assumption. | PASS | The naive difference appears once, in Handoff Facts, pre-disclaimed: "(**not an effect estimate** — confounded by the differential attrition described above) … the naive difference of these two rates is +9.58 percentage points, a number that falls inside the computed bound but is not itself licensed as the effect or as a midpoint." |
| Route recorded is `bound` per SKILL.md (to be written; D3/D5 fix that this route produces real endpoints, not only a plan for endpoints). | PASS | Record Question block: "Route: bound — the assignment note states, and the data confirm, that nothing identifies a point effect and no design is constructible …"; real endpoints are computed, not planned. |

Total: 4/4.

Machine gate: `check_review.py` exits 1 with three findings plus one advisory — "Bound block: Assumption ledger is missing or empty" and "Handoff block: Facts is missing or empty" (both slots written as indented sub-lists where the checker requires inline values), "Dispositions names no closed-set disposition value and is not 'none'" (the record wrote "Dispositions: none — this record carries no Design block …", and the checker accepts only bare `none`), and advisory "possible point estimate '+9.58 percentage points' outside the Bound endpoints slot" (the pre-disclaimed naive difference quoted above).
All three gate findings are shape/parse mismatches against semantically compliant content; adjudicated in the verdict resolution.

Fidelity notes (not scored):

- The record checks the licensed monotonicity direction against the data before trimming ("P(observed | invited) = 534/600 = 0.890 vs … 413/600 = 0.688 — … had it run the other way, the assumption would be contradicted and no bound would be licensed by it"), which is the bound route working as specified.
- The estimand is correctly scoped to the always-observed stratum, matching the fixture's construction.

Cost: 53,580 tokens (harness-reported, n=1; +38.8% over the 38,609-token baseline); 10 tool uses (identity).
