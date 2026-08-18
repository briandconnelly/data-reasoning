# Instrument check — positive-control the analyzers before the widening wave

Written before any Tasks 5-7 invocation runs.
This records that `analyze_phasec.py` and `analyze_ab.py` reproduce published numbers from committed archives, and pins the exact invocation forms later tasks must use.

## Step 1 — analyze_phasec.py against the Phase C archive

Command:

```
python3 skills/exploratory-data-analysis/tests/eval/analyze_phasec.py \
  --results skills/exploratory-data-analysis/tests/runs/artifacts/2026-08-11-phaseC/results.jsonl \
  --fixture skills/exploratory-data-analysis/tests/eval/crossed-pairs-2026-08-11.json \
  --expected-runs 3
```

Reproduced exactly, matching decision 004 and `2026-08-11-phaseC-results.md`.
Baseline arm: profile 0.8333, overview 0.1000, rundown 0.0333, tell-me-about 0.1333.
Treatment arm: profile 0.8000, overview 0.0667, rundown 0.0000, tell-me-about 0.0000.
theta_bar = -0.0333, exact interval [-0.1333, +0.0667], VERDICT: NOT_SUPPORTED — all matching the published record exactly.
`analyze_phasec.py` is confirmed to reproduce a published number from a committed archive; the instrument is trustworthy for baseline/treatment-labeled data.

## Additional control — ceiling-probe table by direct tally

`analyze_phasec.py` cannot ingest the 2026-08-12 ceiling-probe archive, because that archive's `arm_label` values are `shipped`/`ceiling`, not the `baseline`/`treatment` pair the script hardcodes.
The published ceiling-probe table is nonetheless reproducible directly from the archive by an ad hoc tally of `results.jsonl`, joined to `probe-fixture.json` on `query_index` for `speech_act`, restricted to `status == "valid"` rows.
Run with `python3 <script>` from the worktree root, the script below reproduces the table exactly, so the archive itself is sound even though `analyze_phasec.py` cannot read its labels.

```python
import json
from collections import defaultdict

fixture = json.load(open("skills/exploratory-data-analysis/tests/runs/artifacts/2026-08-12-ceiling-probe/probe-fixture.json"))
speech_act_by_index = {i: item["speech_act"] for i, item in enumerate(fixture)}

rows = []
with open("skills/exploratory-data-analysis/tests/runs/artifacts/2026-08-12-ceiling-probe/results.jsonl") as f:
    for line in f:
        line = line.strip()
        if line:
            rows.append(json.loads(line))

counts = defaultdict(lambda: [0, 0])  # (arm, act) -> [triggers, n]
for row in rows:
    if row.get("status") != "valid":
        continue
    act = speech_act_by_index[row["query_index"]]
    arm = row["arm_label"]
    counts[(arm, act)][1] += 1
    if row["triggered"]:
        counts[(arm, act)][0] += 1

order = ["profile", "overview", "rundown", "tell-me-about"]
for arm in ("shipped", "ceiling"):
    parts = []
    for act in order:
        trig, n = counts[(arm, act)]
        rate = trig / n if n else None
        parts.append(f"{act}={rate:.3f} (n={n})")
    print(arm, " ".join(parts))

total_valid = sum(1 for r in rows if r.get("status") == "valid")
total_void = sum(1 for r in rows if r.get("status") == "void")
print(f"rows={len(rows)} valid={total_valid} void={total_void}")
```

Output:

```
shipped profile=0.500 (n=8) overview=0.125 (n=8) rundown=0.125 (n=8) tell-me-about=0.125 (n=8)
ceiling profile=0.875 (n=8) overview=1.000 (n=8) rundown=1.000 (n=8) tell-me-about=0.750 (n=8)
rows=64 valid=64 void=0
```

That matches the published table exactly: shipped 0.500/0.125/0.125/0.125 and ceiling 0.875/1.000/1.000/0.750 for profile/overview/rundown/tell-me-about, with all 64 rows valid and 0 void.

## Step 2 — analyze_ab.py invocation form for cost-arm analysis

Working command, validated against the archived Phase A results:

```
python3 skills/exploratory-data-analysis/tests/eval/analyze_ab.py \
  --results skills/exploratory-data-analysis/tests/runs/artifacts/2026-08-11-phaseA/results.jsonl \
  --fixture skills/exploratory-data-analysis/tests/eval/entity-profiling-eval.json \
  --expected-runs 3 --json
```

This exits 0 and its JSON carries per-arm means (including N1 and N2) and the P1 permutation interval.
The 16-query subset fixture (`cost-arms-2026-08-15.json`) fails against the same results file with `CHECK FAILED` (query-index and query-text mismatches), because `analyze_ab.py` matches results to the fixture positionally by `query_index` and the subset reorders and shortens the query list relative to any results file built against the full fixture's indices.
**Tasks 6-7 must pass `--fixture skills/exploratory-data-analysis/tests/eval/entity-profiling-eval.json` (the full fixture) for cost-arm analysis, never `cost-arms-2026-08-15.json`.**
The results file for a cost-arm run only contains cost-arm queries, so arm means for arms other than N1/N2 are simply absent from the output, not incorrect.

## Binding notes for Tasks 5-7

`analyze_phasec.py` hardcodes `DESC_ARMS = ("baseline", "treatment")` and will reject any `results.jsonl` whose `arm_label` values are anything else.
Every future wave run that needs `analyze_phasec.py`-style per-speech-act analysis must invoke `run_desc_eval.py` with `--label-a baseline --label-b treatment`, where `baseline` is always the reference arm (desc-a) and `treatment` is always the candidate arm (desc-b).
The run manifest records which frozen description file each label maps to for that run, so the generic `baseline`/`treatment` labels stay unambiguous.
Any gate note, report, or disclosure table that cites `baseline` or `treatment` from an `analyze_phasec.py` run must translate those labels back to the actual description files via that run's manifest before drawing conclusions about a specific candidate.

## Correction, 2026-08-17 — the "always full fixture" rule for `analyze_ab.py` was measured wrong

Task 6's `AvB-gate1.md` demonstrated, with archived evidence, that the "Tasks 6-7 must pass `--fixture entity-profiling-eval.json` (the full fixture) for cost-arm analysis" instruction above does not hold for a genuinely cost-arm-only results file.
Two forms were tried and both failed:
1. Run against the 16-query subset fixture, analyzed with the full fixture: `CHECK FAILED` on `query_index`, because the subset fixture reorders and renumbers the same 16 queries relative to the full fixture's own indices.
2. Run against the full fixture with `--queries` restricted to the cost arms' own indices, analyzed with the full fixture: `CHECK FAILED` in `check_completeness`, because that check requires `expected_runs` valid rows for every one of the full fixture's 50 indices unconditionally, and a genuinely 16-query-scoped run only ever covers 16 of them.
The original claim above only worked because the archive it was validated against (`2026-08-11-phaseA/results.jsonl`) happened to cover all 50 queries of the full fixture — a fully-covered special case, not the general rule.

**Corrected rule:** `analyze_ab.py`'s `--fixture` argument must match the fixture the run itself was executed against, not "the full fixture" unconditionally.
For a 16-query cost-arm run, that is `cost-arms-2026-08-15.json`, because then `check_fixture_match` and `check_completeness` are both evaluated against exactly the same 16-row shape the run covered.
Task 7 applied this corrected rule for the B-vs-C3 cost-arm analysis; see `BvC-gates.md` and the `AvB-cost` evidence in `AvB-gate1.md` for the two failing forms and the passing form.
