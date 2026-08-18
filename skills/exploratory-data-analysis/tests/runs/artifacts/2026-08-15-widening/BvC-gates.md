# Gates 2 and 3 — gain and cost (B vs C3)

Task 7 of the 2026-08-15 generic speech-act widening wave (issue #17).
Verdicts are drawn strictly from `2026-08-15-widening-prereg.md` § "Confirmatory wave", Gate 2 and Gate 3.

## Label -> file mapping

Every invocation in this task used `run_desc_eval.py --label-a baseline --label-b treatment`, per `instrument-check.md`'s binding note.
In this pair, `baseline` (desc-a) is `frozen-2026-08-15-B-compressed.txt` — this is arm B, the compressed description.
`baseline` here is **not** the shipped 2026-08-11 description used as arm A elsewhere in this wave.
`treatment` (desc-b) is `frozen-2026-08-15-C3.txt` — this is arm C, the winner from screening (Task 5's `screening-decision.md`, pooled generic rate 0.5417, highest among C1/C2/C3).
Both the fresh-fixture manifest (`BvC-fresh/manifest-20260818T013508Z.json`) and the cost-arm manifest (`BvC-cost/manifest-20260818T015902Z.json`) record this mapping under their `descriptions` field, and both agree.
Every rate and interval below that is printed under the labels `baseline`/`treatment` should be read as B/C3 respectively per this mapping.

## Fresh fixture (crossed-pairs-2026-08-15.json, 40 queries, 3 runs/query/arm)

Run: resumed from a prior interrupted invocation (64/240 rows on disk at task start, no process running).
Resumed with `--resume` on the same `results.jsonl`; the resumed run completed to 240 valid rows, 241 total rows, 1 void.
Void: arm `baseline`, query_index 16, run 1, attempt 1, reason `usage_limit`; the retried attempt (attempt 2) came back valid, so the void is not counted as a negative and does not reduce the completed run count, per the prereg's "voids are never negatives" rule.
Per-arm valid completion: baseline 120/120 valid invocations (post-retry); treatment 120/120 valid invocations.

Per-speech-act rates (from `analyze_phasec.py`, n=60 invocations per act per arm):
- profile: baseline 0.8333, treatment 1.0000.
- overview: baseline 0.2000, treatment 0.7000.
- rundown: baseline 0.0000, treatment 0.7667.
- tell-me-about: baseline 0.0000, treatment 0.2667.

Pooled generic rate (overview + rundown + tell-me-about pooled by invocation, excluding profile, per the prereg's definition of "pooled generic rate"; n=90 invocations per arm across the 30 queries carrying those three acts):
- baseline: 6/90 = 0.0667.
- **treatment (C3): 52/90 = 0.5778.**

Pooled generic lift (treatment − baseline, paired by the 30 generic queries, exact paired sign-flip permutation, two-sided 95%, computed with `analyze_ab.py`'s own `paired_differences`/`permutation_interval` machinery applied to the fresh fixture's generic-act query indices, since neither `analyze_phasec.py` nor `analyze_ab.py` emits this interval directly):
- mean lift +0.5111, interval **[+0.2889, +0.7333]**, excludes zero: **True**.

`analyze_phasec.py`'s own preregistered Phase C estimand (theta_bar, the profile-vs-generic gap-of-gaps) is disclosed here for completeness, but it is not the Gate 2 rule and is not used to decide this gate: theta_bar = 0.3444, exact 31/90, interval [+0.0667, +0.6222], p=0.0117, VERDICT CONFIRMED (excludes zero).

Order diagnostic (fresh fixture, from `analyze_phasec.py`):
- by_run: run 1 baseline=0.2750 (n=40) treatment=0.7750 (n=40); run 2 baseline=0.2500 (n=40) treatment=0.7250 (n=40); run 3 baseline=0.2500 (n=40) treatment=0.5500 (n=40).
- by_which_first: when baseline went first, baseline=0.2000 (n=60) treatment=0.6000 (n=60); when treatment went first, baseline=0.3167 (n=60) treatment=0.7667 (n=60).
- Treatment triggers substantially more regardless of order, and the effect does not depend on which arm ran first; this is consistent with a genuine treatment effect rather than an order artifact.

## Cost arms (N1 + N2, 16 queries, 3 runs/query/arm)

Per the correction adjudicated in Task 6 (`AvB-gate1.md`, "Deviation from the controller's correction 2"), `analyze_ab.py` was invoked with `--fixture cost-arms-2026-08-15.json` — the run's own 16-query fixture — not the full `entity-profiling-eval.json`.
The full fixture fails `analyze_ab.py`'s `check_completeness` against a genuinely 16-query-scoped run, because that check requires `expected_runs` valid rows for every one of the full fixture's 50 indices unconditionally.
`instrument-check.md`'s original note is corrected below, dated 2026-08-17.

Run: `BvC-cost/results.jsonl`, 96 rows, 96 valid, 0 void.
Per-arm valid completion: baseline 48/48 valid invocations (N1 30 + N2 18); treatment 48/48 valid invocations (N1 30 + N2 18).
`gate_result.gates[0]` ("Instrument", requiring baseline P0) fails/VOIDs because the P0 arm was never run in a cost-arm-only fixture, which is expected and is one of the veto-fix gate verdicts this task ignores, consistent with `AvB-gate1.md`.

N1 and N2 means (from `analyze_ab.py --fixture cost-arms-2026-08-15.json`):
- N1 baseline mean 0.0000 (0/30 invocations, 10 queries); N1 treatment mean 0.0667 (2/30 invocations, 10 queries).
- N2 baseline mean 0.0000 (0/18 invocations, 6 queries); N2 treatment mean 0.0000 (0/18 invocations, 6 queries).

N1 and N2 change intervals (treatment − baseline, paired by query, exact paired sign-flip permutation, two-sided 95%, computed with `analyze_ab.py`'s own `paired_differences`/`permutation_interval` applied to the N1 and N2 arm's own query indices, since the script's named `paired_p1` interval is scoped to the P1 arm only, which this fixture does not contain):
- **N1 change: mean +0.0667, interval [0.0000, +0.1333], excludes zero: False (includes zero).**
- **N2 change: mean 0.0000, interval [0.0000, 0.0000] (degenerate — every paired difference was exactly 0), excludes zero: False (includes zero).**

Order diagnostic (cost arms, from `analyze_ab.py`):
- by_run: run 1 baseline=0.0000 (n=16) treatment=0.0000 (n=16); run 2 baseline=0.0000 (n=16) treatment=0.0625 (n=16); run 3 baseline=0.0000 (n=16) treatment=0.0625 (n=16).
- by_which_first: when baseline went first, baseline=0.0000 (n=24) treatment=0.0417 (n=24); when treatment went first, baseline=0.0000 (n=24) treatment=0.0417 (n=24).
- The tiny treatment-arm bump (2/96 invocations) is order-independent; no order artifact is evident.

## Gate 2 verdict

Per `2026-08-15-widening-prereg.md` § "Confirmatory wave", Gate 2 — gain (B vs C, fresh fixture): "pooled generic rate under C is at least 0.5 and the interval for the pooled generic lift excludes zero."
Pooled generic rate under C3 = 0.5778 >= 0.5: **True**.
Pooled generic lift interval [+0.2889, +0.7333] excludes zero: **True**.

**VERDICT: PASS.**

## Gate 3 verdict

Per `2026-08-15-widening-prereg.md` § "Confirmatory wave", Gate 3 — cost (B vs C, cost arms): "the N1 change interval and the N2 change interval both include zero."
N1 change interval [0.0000, +0.1333] includes zero: **True**.
N2 change interval [0.0000, 0.0000] includes zero: **True**.

**VERDICT: PASS.**

## Overall

Both Gate 2 and Gate 3 pass.
Per the prereg, the wave proceeds to Gate 4 (seam) in a later task; this task's evidence does not itself ship anything.
