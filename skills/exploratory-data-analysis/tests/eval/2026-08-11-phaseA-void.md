# Phase A, attempt 1 — VOID on the instrument gate

Governed by `2026-08-11-veto-fix-prereg.md` § Phase A.
This attempt produced no result about the description. It is recorded because a void that goes unrecorded becomes a silently-repeated experiment.

## Verdict

`analyze_ab.py` on the full 300-row result set:

| Gate | Value | Threshold | Outcome |
| --- | --- | --- | --- |
| 1, instrument | baseline P0 = 0.3333 | ≥ 0.8 | **FAIL** |
| 2, no harm | — | — | not evaluated |
| 3, ship | — | — | not evaluated |

**VERDICT: VOID.** Per the preregistration, the description is untouched, no later gate is read, and no number below is a finding about the wording.

## Why the instrument failed

The account hit its usage limit partway through the run.
From ordinal 122 of 300 onward, `claude -p` stopped doing work and returned a refusal — its assistant text reads `You've hit your session limit · resets 4pm (America/Los_Angeles)` — while still exiting 0 with a well-formed, parseable stream carrying a result event and a session id.

**179 of 300 invocations were these non-executions, and the harness scored every one of them as a legitimate `triggered = false`.**

The decay is unmistakable once the run is sliced by time:

| | run 1 | run 2 | run 3 |
| --- | --- | --- | --- |
| P0 trigger rate | 14/16 = 0.875 | 2/16 = 0.125 | 0/16 = 0.000 |

No P0 invocation after ordinal ~139 triggered at all.

## The instrument defect this exposes

Every validity check the harness performs — exit code 0, parseable stream, result event present, non-empty session id — **passes** for a usage-limit refusal.
The harness was built specifically to stop invalid executions from being scored as negatives, and this is an invalid execution that its validity model could not see.
Detection of usage-limit refusals, with no retries burned on them and an immediate run abort, is being added before any re-run; a stranded `usage_limit` cell must resume as incomplete rather than persist as a false negative.

## What must not be salvaged from this run

The first 121 invocations preceded the contamination, and it is tempting to analyse them.
They must not be used as a result: coverage is partial and unbalanced across queries and arms, and *which* invocations survived was determined by when the quota ran out, which is a selection rule correlated with execution order.
`analyze_ab.py` refuses the subset on its completeness gate, which is the correct behaviour.
Recorded only to show why the subset was not analysed: within it, P0 ran 8/9 in both arms and P1 ran 8/27 baseline against 9/26 treatment. These are not estimates of anything.

## What this says about the historical numbers

`skill-creator`'s `run_eval.py` — the instrument behind every number in `decisions/003` and PR #4 — has the same blind spot and no transcript archive to detect it after the fact.
A usage-limit refusal there is indistinguishable from a genuine non-trigger, and `decisions/003`'s "0 harness warnings on every run" would not have flagged one, because no warning exists for this case.
That does not show the historical numbers are contaminated. It shows contamination could not have been noticed, which is an additional reason the preregistration treats them as reference only.
The historical baseline P1 of 0.167 is exactly the shape a partially quota-starved run would also produce, and nothing in the committed record can separate the two.

## Bookkeeping

- Archive: `runs/artifacts/2026-08-11-phaseA-void/` — the full 300-row `results.jsonl`, the manifest, the run log, and the canary and positive-control results.
  All 600 transcript files (7.5 MB) are **not** committed for a void run; `evidence-transcripts/` carries the eight that establish the claims made here: query 24 across all three runs (triggering at ordinals 1, 2, 117, 118 and refusing at 237, 238 with identical wording and an identically registered command), and the ordinal 121/122 boundary where contamination begins.
  The refusal text is greppable in the archived transcripts as `hit your session limit`.
- The wave's frozen texts, fixture, instruments, gates, and canary evidence are unchanged and remain valid; only the arms are void.
- The re-run repeats Phase A in full under the preregistered design once quota headroom exists. Nothing about the design changes as a result of this void, except that the instrument now detects the failure that caused it.
