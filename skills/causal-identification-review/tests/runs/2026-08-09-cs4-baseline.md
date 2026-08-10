# CS4 baseline — 2026-08-09 (amended-cell re-run)

Arm transcript: `sc2-cs4-base.jsonl` (sha256 `d7f6f74c…`, full digest in `artifacts/2026-08-09-measurement-wave-1-evidence.md`).
No skill loaded; prompt plus staged `cs4-facts/facts.md` only.
This arm re-measures the cell after the 2026-08-09 CS4 amendment; the first-wave `sc-cs4-*` arms are archived-unscored per the amendment note in the catalog.
Scored against `tests/scenarios.md` § CS4 (amended assertions).

| Assertion (verbatim, first clause) | Result | Evidence |
| --- | --- | --- |
| Names ≥2 candidate designs including regression discontinuity, each carrying identifying assumptions and data requirements, with every disposition drawn from the closed set …; a timing-based design …, if named, must confront the discretion fact rather than treat realized timing as clean … | FAIL | Two designs named with assumptions and requirements (RDD "primary", batch-cohort "secondary"), and the discretion fact is confronted ("fast-tracking … analyst discretion on unlogged 'high-touch' judgment. That's selection on unobserved risk, baked directly into the timing variable"); but no disposition from the closed set is assigned to anything. |
| Regression discontinuity's block states its identifying assumptions (no manipulation/sorting …; continuity …) and its data requirements (the running variable, the enrollment flag, the outcome, and enough merchant density near the cutoff to run a manipulation and covariate-balance check). | PASS | Final text: "A manipulation check (density/McCrary-style) — can merchants influence which side of $50k they land on?"; "A check that nothing else changes at $50k"; "The running variable (lifetime volume) … with enough resolution to identify a bandwidth around $50k"; "Chargeback outcomes for merchants on both sides of the cutoff"; "Covariate balance just above/below the cutoff". |
| If an instrumental-variable design is named (at whatever disposition), its block states … relevance … exclusion … and independence/exogeneity … — all three, not a subset — … | PASS (vacuous) | No instrumental-variable design is named; the batch-cohort comparison is an intent-to-treat-style calendar-time contrast, not an IV block. |
| When the instrumental-variable block's estimand is a local average treatment effect, the block also states monotonicity … | PASS (vacuous) | No IV block exists. |
| Does not propose difference-in-differences or a matching/selection-on-observables design as admissible … | PASS | DiD is explicitly rejected ("Diff-in-diff … impossible for the same reason"), matching never proposed; "early- vs. late-verified within a batch" is rejected on the discretion fact. |
| If a prospective randomized experiment is mentioned, it is named only — no power calculation, minimum-detectable-effect figure, sample-ratio-mismatch check, or other prospective-design mechanics appear (D3's exclusion). | PASS | "scope the prospective randomized rollout mentioned in the facts" — named as the only population-level route, no mechanics anywhere. |
| Route recorded is `construct` per SKILL.md … | FAIL | No route recorded; no record artifact (answer inline, 1 tool use total). |

Total: 5/7.

Comparison note: the baseline reads the same facts sheet to nearly the same design matrix as the with-skill arm — including independently reading the 90-day-post-enrollment outcome window as unavailable for below-cutoff merchants ("not '90 days after enrollment,' since ineligible merchants have no enrollment date") — but recommends RDD as "the primary retrospective analysis" contingent on a new data pull rather than recording an evidence-bounded disposition, and produces no record, route, or closed-set vocabulary.

Cost: 31,511 tokens (harness-reported, n=1); 1 tool use (identity).
