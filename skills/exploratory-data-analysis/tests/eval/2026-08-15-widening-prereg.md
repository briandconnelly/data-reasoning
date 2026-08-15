# Preregistration — generic speech-act widening wave (issue #17)

Written and committed before any invocation of this wave ran.
Design rationale is in the spec this wave implements; this file is the authority for the decision rules only.

## Common to every run

Instrument: `run_desc_eval.py`, matched-pair, counterbalanced, validity-aware; model `claude-opus-5`; timeout 390.
Voids are never negatives.
Every run's transcripts and manifest are archived under `tests/runs/artifacts/` before any number from it is cited.
The order diagnostic is reported for every comparison.
"Pooled generic rate" always means the trigger rate pooled over `overview`, `rundown`, and `tell-me-about`, excluding `profile`.
Intervals are the exact permutation intervals the analyzers report at 95%.

## Screening (Task 5)

Fixture: the 16-query subset in `runs/artifacts/2026-08-12-ceiling-probe/probe-fixture.json`, already burned by the ceiling probe.
Arms: each of C1, C2, C3 against `frozen-2026-08-11-treatment.txt` (shipped), 2 runs per query per arm.
Winner: highest pooled generic rate; ties break toward the fewest edits against B (C1 or C2 over C3).
Proceed to the confirmatory wave only if the winner's pooled generic rate exceeds the shipped arm's pooled generic rate in its own pair by at least 0.25.
Screening numbers carry no ship consequence and are never cited as effect sizes.

## Confirmatory wave (Tasks 6–8)

Arms: A = `frozen-2026-08-11-treatment.txt`, B = `frozen-2026-08-15-B-compressed.txt`, C = the frozen winner.
Fixtures: `crossed-pairs-2026-08-15.json` (fresh, 40 queries) and `cost-arms-2026-08-15.json` (N1 + N2, 16 queries); 3 runs per query per arm.

Gate 1 — compression is a null (A vs B): on the fresh fixture, every per-speech-act contrast interval and the pooled generic contrast interval include zero; on the cost arms, the N1 and N2 change intervals include zero.
Fail → STOP; the compression is redesigned and the wave restarts from candidate freezing.

Gate 2 — gain (B vs C, fresh fixture): pooled generic rate under C is at least 0.5 and the interval for the pooled generic lift excludes zero.
Fail → STOP; do not ship; commit the wave as evidence.

Gate 3 — cost (B vs C, cost arms): the N1 change interval and the N2 change interval both include zero.
Fail → STOP; do not ship; commit the wave as evidence.

Gate 4 — seam (under C applied to the skill): `run_trigger.py` T13 5/5 to `exploratory-data-analysis` and T14 5/5 to `hypothesis-driven-analysis`.
Fail → STOP; do not ship; commit the evidence.

Ship only if gates 1–4 all pass, as two commits: B first (with the gate 1 evidence), then C (with the gate 2–4 evidence).

## Not measured by this wave

Behaviour after triggering (decision 004's recorded limitation stands), domain generality beyond one invented domain per fixture, and — if C3 ships — the attribution between its two mechanisms.
