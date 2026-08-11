# Phase A canary gate — outcome

Governed by `2026-08-11-veto-fix-prereg.md` § Phase A; nothing here restates its rules.
Canaries are excluded from every arm mean and from every gate computation.

## What ran

Six queries × two descriptions = 12 invocations, `claude-opus-5`, one run each, via `run_desc_eval.py` on the committed canary fixture.
The four 0.33-tier queries plus the two preregistered probes of the clause under test.

## Gate outcome: PASS

**Instrument surfaces live positives.** Before trusting any canary negative, three known-P0 queries were run through the same harness under both descriptions: **6/6 triggered = true**. A negative from this instrument therefore means something.

**Detector agrees with manual reading, 12/12.** Every canary's archived transcript was read directly. In each, the model either answered from context without invoking anything ("I don't have any context on an 'Eastside branch' — that's not something in this repo") or reached for `Bash` first to look for the data. The first tool use decides, and in no transcript was it the synthetic skill command, so `triggered = false` is correct in all twelve. No detector/manual disagreement, so the phase is not voided.

**Synthetic command registered in all 12**: the session's `slash_commands` list contains `exploratory-data-analysis-skill-<uuid>` in every transcript.

## Observations, recorded and not gating

**The dataset probe did not trigger under either description**, reversing the preregistered expectation. The cause is visible in the transcript and is a defect in the probe's wording, not evidence about the veto clause: "Summarize what's in the circulation export." names no file, so the model opened `Bash` to hunt for one, which decides the verdict before any skill is considered. The fixture's own dataset-summary query names a path (`Summarize the dataset in ./circulation.csv.`) and sits in P0, where it has always triggered. The probe pair therefore did not discriminate the clause, and the preregistration's expectation for it is withdrawn as unmeasurable by this instrument rather than treated as a result.

**The prose probe did not trigger under either description**, matching expectation — but for the same uninformative reason, since it too names no document the model can reach. Neither probe should be reused as authored.

**The four 0.33-tier queries returned false under both descriptions at n = 1 each.** This is uninformative by design at one run per cell and is consistent with their historical 0.33 rate; the scored batch, not the canaries, measures them.

**Why entity queries under-trigger here, mechanically.** These queries name entities for which no data exists in the working directory, and the model's first move is either a direct "I don't have that" answer or a `Bash` look-around. Either way the first tool use is not the skill, which is what the detector scores. The historical instrument scored the same way, so the effect is present in the 0.167 / 0.517 numbers too; it is a property of the eval design, identical across both arms, not a bias between them.

## Instrument defect found and fixed during the canary gate

The first canary attempt produced twelve clean, plausible-looking `false` results that were **not measuring the intended configuration**. The harness derives the synthetic skill's name from the fixture's path and silently fell back to the literal `skill` when the fixture was staged outside the repository, so the model was shown a command named `skill-skill-<uuid>` rather than `exploratory-data-analysis-skill-<uuid>` — and the command's name is part of what a model routes on.

Nothing in the run's output signalled this; it was found by reading a transcript's registered command list after the positive control forced the question of why every canary was negative.
The canary fixture was moved into `tests/eval/` (committed) and the canaries were re-run under the correct name; those re-runs are the results reported above.
The silent fallback is now a hard abort, the resolved skill name and how it was resolved are recorded in the manifest and in every result row, and a resume across a skill-name change aborts like a digest change.
