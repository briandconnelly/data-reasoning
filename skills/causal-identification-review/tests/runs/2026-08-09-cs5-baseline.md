# CS5 baseline — 2026-08-09

Arm transcript: `sc-cs5-base.jsonl` (sha256 `434326ba…`, full digest in `artifacts/2026-08-09-measurement-wave-1-evidence.md`).
No skill loaded; prompt plus staged `cs5-bounds` fixture only.
Scored against `tests/scenarios.md` § CS5.

| Assertion (verbatim) | Result | Evidence |
| --- | --- | --- |
| The assumption ledger — the monotonicity direction and the trimming logic it licenses — is written before any endpoint number appears in the record. | PASS | In the only record (the inline answer), "The fixture licenses exactly one assumption: monotonicity of attrition … That licenses Lee (2009) trimming bounds" precedes "Result: sharp bounds on the effect = [-1.9 pp, +27.4 pp]"; the only earlier number is the naive gap, labeled "not a valid effect estimate", which is not an endpoint. |
| The computed lower and upper endpoints match the fixture's documented ground-truth bounds (exact match, or within a stated numeric tolerance the validator sets). | PASS | Reported [-1.9 pp, +27.4 pp] matches `cs5-bounds-ground-truth.md`'s lower -0.019370 / upper 0.273608 at the reported precision. |
| No causal point estimate appears anywhere in the output — not a naive difference-in-means reported as "the effect," not a midpoint of the bound presented as a best guess; only the interval, framed as a range under the stated assumption. | PASS | The +9.6 pp naive gap is flagged in the same sentence as "not a valid effect estimate — it's confounded with differential survivorship"; no midpoint or point effect is offered ("Any claim more precise than this interval is not supported by the data"). |
| Route recorded is `bound` per SKILL.md … | FAIL | No route recorded; no record artifact exists. |

Total: 3/4.

Comparison note: the baseline independently produced numerically correct Lee bounds and even a Manski worst-case contrast, so the with-skill delta on this cell is ceremony and record discipline (the route token, the template record, the ledger-before-endpoints structure as an artifact), not numeric correctness — recorded honestly per the dispatch note; this leaves CS5 differentiating on exactly one assertion at n=1, flagged in the verdict resolution as a thin-margin cell.

Cost: 38,609 tokens (harness-reported, n=1); 5 tool uses (identity).
