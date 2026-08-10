# CS3 with-skill — 2026-08-09

Arm transcript: `sc-cs3-ws.jsonl` (sha256 `16a454f5…`, full digest in `artifacts/2026-08-09-measurement-wave-1-evidence.md`).
Skill loaded from the staged copy at c5f4755; record archived at `sc-cs3-ws/identification-review-cs3-rollout.md` (written at manifest ordinal 13, the final tool call).
Scored against `tests/scenarios.md` § CS3.

| Assertion (verbatim) | Result | Evidence |
| --- | --- | --- |
| Names {concurrent change, pre-existing trend, selection into exposure} as identifying threats — all three, not a subset. | PASS | Record threat registers name the concurrent UX cleanup and same-day promotion, the non-flat pre-trend (assumption-probe row: "West's weekly median fell steadily through the pre-period (206.3s -> 204.1s -> …)"), and "Selection into treatment via complaint volume". |
| Proposes ≥1 probe per named threat: a placebo/falsification check on `avg_order_value` … a pre-period slope comparison … a check of whether West's baseline … was already an outlier … | PASS | Record probes, all run: "Cross-referenced `promotions.log` against West vs. East median `avg_order_value` pre/post 2026-03-15" (West 44.80 -> 53.99, East flat); weekly median completion time for both regions across the pre-period; `targeting_note.md` complaint counts (West 184 vs East 97) with the pre-period West-vs-East level gap recorded in Facts. |
| Every design considered ends on a disposition from the closed set … — no unconditional "valid" or "identified" language anywhere. | PASS | Both Design blocks end "Disposition: assumption-contradicted — …"; `check_review.py` confirms both disposition tokens parse from the closed set and finds no forbidden certification vocabulary. |
| Both the before/after and the East-comparison designs are assigned `assumption-contradicted`, matching the fixture's documented ground truth. | PASS | Record: "Disposition: assumption-contradicted" for "Design: Before/after in West" and for "Design: Difference-in-differences, West vs. East". |
| Does not propose synthetic control; proposing it fails this assertion … | PASS | Synthetic control appears once, only to rule it out: "Only two regions exist, so synthetic control isn't feasible either (no donor pool)" (final text); the record never names it. |
| Route recorded is `review` per SKILL.md … | PASS | Record Question block: "Route: review — a before/after comparison in West is being offered as causal evidence of the flow's effect, per `../SKILL.md` § Routing." |

Total: 6/6.

Machine gate: `uv run python skills/causal-identification-review/tests/check_review.py <record>` exits 1 with one finding — "Handoff block: Facts is missing or empty" — because the record wrote `- Facts:` followed by an indented sub-list where the checker requires an inline slot value.
The Facts content is present and substantive; this is a record-shape/checker-parse mismatch, adjudicated in the verdict resolution, not an assertion row.

Fidelity notes (not scored):

- All probes were executed against `daily.csv` before the record was written (manifest ordinals 9–11), and the single record write is the last tool call.
- The final text closes with "no design here supports a causal point estimate" and the record carries the Non-Goals disclaimer verbatim.

Cost: 50,162 tokens (harness-reported, n=1; +43.6% over the 34,924-token baseline); 13 tool uses (identity).

## Instrument note (2026-08-09, post-review)

The machine-gate paragraph above describes the checker as it stood when this arm was scored; it is kept as written because this file records what the gate said at scoring time.
The checker was subsequently given the formatting tolerance the verdict resolution's defect scoping licensed, and on re-run against this record (recovered from the archived transcript) the shipped checker passes it clean.
See the instrument-revision note in `artifacts/2026-08-09-measurement-wave-1-evidence.md` for the full re-run results.
