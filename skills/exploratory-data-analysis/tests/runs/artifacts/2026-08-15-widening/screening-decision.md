# Screening decision — issue #17 generic speech-act widening

Written after all three screening pairs (C1, C2, C3) completed and were analyzed with `analyze_phasec.py --expected-runs 2`.
Applies the prereg rule from `2026-08-15-widening-prereg.md` § Screening verbatim; the rule is not re-derived here.

## Label to description mapping

`analyze_phasec.py` hardcodes the arm labels `baseline` and `treatment`.
Per the controller ruling in `instrument-check.md`, every screening run used `--label-a baseline --label-b treatment`.
In every pair, label `baseline` maps to `--desc-a skills/exploratory-data-analysis/tests/eval/frozen-2026-08-11-treatment.txt` (the shipped description) and label `treatment` maps to `--desc-b`, the candidate under test for that pair (C1, C2, or C3 respectively).
Each run's manifest (`manifest-*.json` in the corresponding `screening-C{1,2,3}/` directory) records this mapping by SHA-256 digest of the description file.

## Pooled generic rate per pair

"Pooled generic rate" means the trigger rate pooled over `overview`, `rundown`, and `tell-me-about`, excluding `profile`, per the prereg's common definition.

- Pair C1: shipped (baseline) = 0.2083 (10/48), C1 (treatment) = 0.3750 (18/48); delta = +0.1667.
- Pair C2: shipped (baseline) = 0.1667 (8/48), C2 (treatment) = 0.5000 (24/48); delta = +0.3333.
- Pair C3: shipped (baseline) = 0.1250 (6/48), C3 (treatment) = 0.5417 (26/48); delta = +0.4167.

Validity: C1 64/64 valid, 0 void.
C2 64/64 valid, 1 void (usage_limit refusal at q7, baseline arm, run 1, retried to a valid attempt; recorded as void, not scored as a negative).
C3 64/64 valid, 0 void.
The C2 pair's run was interrupted mid-wave by a harness usage limit at 19/64 rows and resumed with `--resume`, which appended to the existing `results.jsonl` without deleting any row.

## Order diagnostics (recorded, not gating)

- C1 by_run: run 1 baseline=0.2500, treatment=0.3750; run 2 baseline=0.3125, treatment=0.5000.
  C1 by_which_first: baseline-first — baseline=0.2500, treatment=0.5625; treatment-first — baseline=0.3125, treatment=0.3125.
- C2 by_run: run 1 baseline=0.3125, treatment=0.5000; run 2 baseline=0.3125, treatment=0.5000.
  C2 by_which_first: baseline-first — baseline=0.3125, treatment=0.5625; treatment-first — baseline=0.3125, treatment=0.4375.
- C3 by_run: run 1 baseline=0.3125, treatment=0.5625; run 2 baseline=0.1875, treatment=0.6250.
  C3 by_which_first: baseline-first — baseline=0.2500, treatment=0.5625; treatment-first — baseline=0.2500, treatment=0.6250.

## Winner and prereg rule applied

Winner: highest pooled generic rate among C1 (0.3750), C2 (0.5000), and C3 (0.5417) is C3, with no tie to break.
C3's pooled generic rate (0.5417) exceeds the shipped arm's pooled generic rate in its own pair (0.1250) by 0.4167, which is at least the prereg's 0.25 proceed threshold, so the screening wave proceeds to the confirmatory wave (Tasks 6-8) with `frozen-2026-08-15-C3.txt` as arm C.

Screening numbers carry no ship consequence and are not cited as effect sizes, per the prereg.
