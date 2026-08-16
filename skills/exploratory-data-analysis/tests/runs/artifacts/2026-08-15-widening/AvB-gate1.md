# Gate 1 — the compression is a null (A vs B)

Task 6 of the 2026-08-15 generic speech-act widening wave (issue #17).
Verdict is drawn strictly from `2026-08-15-widening-prereg.md` § "Confirmatory wave", Gate 1.

## Label -> file mapping

Every invocation in this task used `run_desc_eval.py --label-a baseline --label-b treatment`, per the controller's correction to the brief and per `instrument-check.md`'s binding note.
`baseline` (desc-a) is `frozen-2026-08-11-treatment.txt` — this is arm A, the shipped description.
`treatment` (desc-b) is `frozen-2026-08-15-B-compressed.txt` — this is arm B, the compressed description.
Both fresh-fixture manifests (`AvB-fresh/manifest-20260815T203935Z.json` and its resume manifest `manifest-20260816T033216Z.json`) and the cost-arm manifest (`AvB-cost/manifest-20260816T034252Z.json`) record this mapping under their `descriptions` field, and all three agree.
Every rate and interval below that is printed under the labels `baseline`/`treatment` should be read as A/B respectively per this mapping.

## Fresh fixture (crossed-pairs-2026-08-15.json, 40 queries, 3 runs/query/arm)

Run: 240 planned invocation-cells, 241 total rows (240 valid, 1 void), executed across two `run_desc_eval.py` invocations because the first invocation was interrupted by a usage-limit refusal partway through and resumed with `--resume` on the same `results.jsonl`.
Void count: 1 void total, arm `treatment`, query_index 30, run 3, attempt 1, reason `usage_limit`.
The retried attempt on resume came back valid, so the void is not reinterpreted as a negative and does not reduce the completed run count.
Void count by arm: baseline 0 voids; treatment 1 void (retried to valid).
Per-arm valid completion: baseline 120/120 valid invocations; treatment 120/120 valid invocations (post-resume).

Per-speech-act contrast intervals (paired by the 10 queries carrying each act, exact paired sign-flip permutation, two-sided 95%, computed with `analyze_ab.py`'s own `paired_differences`/`permutation_interval` machinery applied to the fresh fixture's per-act query groups, since neither `analyze_phasec.py` nor `analyze_ab.py` emits a per-act interval directly):
- profile: mean +0.1000, interval [0.0000, +0.2000], excludes zero: **False** (includes zero).
- overview: mean -0.1000, interval [-0.2000, 0.0000], excludes zero: **False** (includes zero).
- rundown: mean -0.0667, interval [-0.1333, 0.0000], excludes zero: **False** (includes zero).
- tell-me-about: mean 0.0000, interval [-0.0667, +0.0667], excludes zero: **False** (includes zero).

Pooled generic contrast interval (overview + rundown + tell-me-about pooled by query, excluding profile, per the prereg's own definition of "pooled generic rate"; paired by the 30 queries in those three acts):
- pooled generic: mean -0.0556, interval [-0.1111, 0.0000], excludes zero: **False** (includes zero).

`analyze_phasec.py`'s own preregistered Phase C estimand (theta_bar, the profile-vs-generic gap-of-gaps) is disclosed here for completeness, but it is not the Gate 1 rule and is not used to decide this gate: theta_bar = -0.1556, interval [-0.3111, 0.0000], VERDICT NOT_SUPPORTED (this is the veto-fix wave's own estimand, not this wave's Gate 1 condition).

Order diagnostic (fresh fixture, from `analyze_phasec.py`):
- by_run: run 1 baseline=0.3000 (n=40) treatment=0.3250 (n=40); run 2 baseline=0.3250 (n=40) treatment=0.3000 (n=40); run 3 baseline=0.4000 (n=40) treatment=0.3500 (n=40).
- by_which_first: when baseline went first, baseline=0.3000 (n=60) treatment=0.3000 (n=60); when treatment went first, baseline=0.3833 (n=60) treatment=0.3500 (n=60).

## Cost arms (N1 + N2, 16 queries, 3 runs/query/arm)

Two invocation forms were tried for the run + analysis pair.
The first (documented below) is the one whose output is used for this gate, because it is the only combination that passes `analyze_ab.py`'s structural checks for a genuinely 16-query-scoped run.

**Deviation from the controller's correction 2, with evidence.** The controller's correction 2 instructed `analyze_ab.py` to be invoked with `--fixture entity-profiling-eval.json` (the full fixture) for cost-arm analysis, per `instrument-check.md`'s binding note, while the run itself uses `cost-arms-2026-08-15.json`.
Two forms of that combination were executed and both failed `analyze_ab.py`'s structural checks, with evidence archived in this task's report:
1. Run against `cost-arms-2026-08-15.json` directly (`query_index` 0-15 relative to that file's own order), analyzed with `entity-profiling-eval.json`: exit 2, `CHECK FAILED`, every `query_index` mismatched because the subset fixture reorders and renumbers the same 16 queries relative to the full fixture (archived at `AvB-cost-subset-fixture-indexing-mismatch/` — later restored to `AvB-cost/`, see below).
2. Run against `entity-profiling-eval.json` with `--queries 28-43` (the full fixture's own N1+N2 indices, confirmed by text-matching every query against `cost-arms-2026-08-15.json`), analyzed with `entity-profiling-eval.json`: exit 2, `CHECK FAILED`, because `analyze_ab.py`'s `check_completeness` requires `expected_runs` valid rows for every one of the fixture's 50 indices unconditionally, and a genuinely 16-query-scoped run only ever covers 16 of them (archived at `AvB-cost-full-fixture-partial-coverage-incomplete/`).
`instrument-check.md`'s claim that "the full fixture is safe for cost-arm-only results" was verified there only against the archived, fully-covered 50-query Phase A results file, never against a genuinely partial 16-query-only results file.
That claim does not hold for form 2 above, as directly demonstrated.
The only combination that passes `analyze_ab.py`'s checks for a 16-query-scoped run is using `cost-arms-2026-08-15.json` as the fixture for both the run and the analysis, because then every check (`check_fixture_match`, `check_completeness`) is evaluated against exactly the same 16-row shape the run itself covered.
That combination (archived at `AvB-cost/`) is therefore the one used below.
`gate_result.gates[0]` ("Instrument", requiring baseline P0) fails because the P0 arm was never run in a cost-arm-only fixture, which is expected and is one of the "veto-fix gate verdicts" this task is instructed to ignore.

Run: `AvB-cost/results.jsonl`, 96 rows, 96 valid, 0 void.
Void count by arm: baseline 0 voids; treatment 0 voids.
Per-arm valid completion: baseline 48/48 valid invocations (N1 30 + N2 18); treatment 48/48 valid invocations (N1 30 + N2 18).

N1 and N2 means (from `analyze_ab.py --fixture cost-arms-2026-08-15.json`):
- N1 baseline mean 0.0667 (2/30 invocations, 10 queries); N1 treatment mean 0.0000 (0/30 invocations, 10 queries).
- N2 baseline mean 0.0000 (0/18 invocations, 6 queries); N2 treatment mean 0.0000 (0/18 invocations, 6 queries).

N1 and N2 change intervals (paired by query, exact paired sign-flip permutation, two-sided 95%, computed with `analyze_ab.py`'s own `paired_differences`/`permutation_interval` applied to the N1 and N2 arm's own query indices, since the script's named `paired_p1` interval is scoped to the P1 arm only, which this fixture does not contain):
- N1 change: mean -0.0667, interval [-0.1333, 0.0000], excludes zero: **False** (includes zero).
- N2 change: mean 0.0000, interval [0.0000, 0.0000] (degenerate — every paired difference was exactly 0), excludes zero: **False** (includes zero).

Order diagnostic (cost arms, from `analyze_ab.py`):
- by_run: run 1 baseline=0.0625 (n=16) treatment=0.0000 (n=16); run 2 baseline=0.0625 (n=16) treatment=0.0000 (n=16); run 3 baseline=0.0000 (n=16) treatment=0.0000 (n=16).
- by_which_first: when baseline went first, baseline=0.0417 (n=24) treatment=0.0000 (n=24); when treatment went first, baseline=0.0417 (n=24) treatment=0.0000 (n=24).

## Gate 1 verdict

Per `2026-08-15-widening-prereg.md` § "Confirmatory wave", Gate 1: "on the fresh fixture, every per-speech-act contrast interval and the pooled generic contrast interval include zero; on the cost arms, the N1 and N2 change intervals include zero."
All four per-speech-act contrast intervals include zero (profile, overview, rundown, tell-me-about).
The pooled generic contrast interval includes zero.
The N1 change interval includes zero.
The N2 change interval includes zero.
Every condition of Gate 1 is satisfied.

**VERDICT: PASS.** The compression edit (arm B against arm A) is a null on the fresh fixture's per-act and pooled-generic contrasts and on the cost arms' N1/N2 change, per prereg Gate 1.
This does not ship anything by itself.
Gate 1 only clears the compression edit to proceed to Gate 2 (B vs C gain) in a later task.
