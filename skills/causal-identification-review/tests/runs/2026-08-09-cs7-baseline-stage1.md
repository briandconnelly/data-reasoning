# CS7 baseline, stage 1 — 2026-08-09 (amended-cell re-run)

Arm transcript: `sc2-cs7-base.jsonl` (sha256 `9c2e0a61…`, full digest in `artifacts/2026-08-09-measurement-wave-1-evidence.md`).
No skill loaded; prompt plus staged `cs7-seam` fixture (with the amended `data_notes.md`) only.
This arm re-measures the cell after the 2026-08-09 CS7 amendments; the first-wave `sc-cs7-*` arms are archived-unscored.
Scored against `tests/scenarios.md` § CS7 stage-1 assertions.

| Assertion (verbatim) | Result | Evidence |
| --- | --- | --- |
| Produces a template-shaped record (once the template exists) naming the causal question as a counterfactual contrast, the estimand, the design (regression discontinuity), its identifying assumptions, and the probes run against them. | FAIL | No record artifact; the arm wrote only analysis scripts (`rdd_analysis.py`, `rdd_local_linear.py`) and answered inline with no counterfactual-contrast or estimand statement. |
| Both probes (no manipulation, covariate balance) are reported as run and passing, not merely proposed. | PASS | "No manipulation/bunching: density … essentially identical just below vs. above 680 (~31.2 vs ~31.3 accounts/point)"; "Covariate smoothness: `account_tenure_months` and `income` show no significant jump at 680 (t = -1.12 and -0.08)". |
| Disposition recorded is `identified-if` per SKILL.md … | FAIL | No disposition; instead the certification vocabulary the disposition contract exists to forbid: "the identification here looks sound" and "a valid regression-discontinuity design for this outcome". |
| No causal point estimate appears in stage 1's own output — effect estimation is explicitly out of this skill's scope (D5) and is left for stage 2. | FAIL | The arm estimated the effect in stage 1: "τ = -0.086 (se 0.033, t = -2.60)" and "≈ 7-9 percentage points lower 90-day default among eligible … accounts". |
| Route recorded is `construct` — … | FAIL | No route recorded. |

Total: 1/5.

Comparison note: the baseline collapses the two-stage separation into one shot — it runs the right probes, then immediately estimates and certifies ("valid", "sound") with no record, no disposition, and nothing a downstream consumer could inherit conditions from; the with-skill stage-1 arm produced the record, the `identified-if` conditions, and left the estimate to stage 2 — which is the expected baseline failure the catalog preregistered ("expected to fail to produce a template-shaped record with a run disposition").

Cost: 41,272 tokens (harness-reported, n=1); 9 tool uses (identity).
