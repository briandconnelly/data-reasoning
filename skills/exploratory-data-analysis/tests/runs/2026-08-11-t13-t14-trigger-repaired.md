# T13/T14 seam repeat under the repaired description — Phase D

Governed by `../eval/2026-08-11-veto-fix-prereg.md` § Phase D, which requires this repeat because the description changed; the instrument, constructs, gates, and outcome classification are those of `artifacts/2026-08-11-t13-t14-trigger-prereg.md` and are not restated.

This run does **not** supersede `2026-08-11-t13-trigger.md` / `-t14-`.
Those measured the pre-edit wording and remain valid for it; this measures the post-edit wording. Both stand.

- Description under test: `SKILL.md` at `a92120f`, byte-identical to `tests/eval/frozen-2026-08-11-treatment.txt` (verified).
- `hypothesis-driven-analysis`'s description is unchanged from the earlier wave.
- Model `claude-opus-5`, fresh `claude -p` per rep via `tests/run_trigger.py`, catalog order counterbalanced, five scored reps per cell.
- Archive: `artifacts/2026-08-11-phaseD-seam/`.

## Result

| Cell | selected = expected | Outcome row |
| --- | --- | --- |
| T13 "Tell me about the Northgate Clinic account." | **5/5** `exploratory-data-analysis` | 1 |
| T14 "Why did the Northgate Clinic account's spend drop last quarter?" | **5/5** `hypothesis-driven-analysis` | 1 |

**Cross-cell disposition row 1/1: no collision detected at screening precision.** Identical to the pre-edit result.

The repaired wording does not disturb the seam. As before, 5/5 spans roughly 0.48–1.00 (two-sided 95% Clopper–Pearson), so this is screening evidence that nothing broke, not a reliability claim.

## Gates

1. **Harness validity** — one void: `t14-rep2` exited 1 with no result event. Excluded, preserved in the archive, and rerun once as `t14-rep2-r2` (valid, `hda`) per the preregistered rule. All other scored reps valid.
2. **Instrument smoke tests** — `c-eda` → `eda`, `c-hda` → `hda`, `c-none` → `none`, all valid. `c-hda`'s first attempt was killed by an operator-side 2-minute tool timeout mid-flight; the harness's no-overwrite refusal blocked a silent clobber, and it was rerun as `c-hda-rep1-r2` with the partial transcript preserved.
3. **Rationale canaries** — **deviation, disclosed below.**
4. **Wording fixed** — no uncommitted change to either `SKILL.md` across the wave; the EDA description matches the frozen treatment text at `HEAD`.
5. **Ambiguity** — zero `unclear` across all ten scored reps.

## Deviation from the preregistered procedure

Phase D specifies repeating the earlier wave "exactly … (same gates, canaries, and rep counts)".
The scored reps were run **before** the instrument smoke canaries rather than after, and the two hand-scored rationale canaries were **not** run as separate excluded arms.

What replaces them, and why it is adequate here: every one of the ten scored transcripts was read directly by the operator, which is the evidence the rationale-canary gate exists to produce. All ten carry an explicit `ROUTE:` token matching the detector's parse, with rationale that engages the descriptions rather than echoing the prompt — T13 reps reason from "a named entity whose story is wanted, with no effect to explain and no claim to adjudicate"; T14 reps from "a named effect … needs explaining, with multiple plausible causes". Detector and manual reading agree 10/10.

What is nonetheless weaker than the original wave: the canaries there ran *first* and could have stopped the scored arms before they were paid for. Here they could not. The ordering guarantee is lost even though the evidence is present, and a reader should treat this cell's instrument check as confirmatory rather than gating.

## Recorded, not scored

Consultation was sparser than in the pre-edit wave: three of five T13 reps and one of five T14 reps read the chosen skill's `SKILL.md`, versus all reps previously. Consultation is process evidence and never counts toward activation, so this does not affect the result; it is noted because a shift in whether arms open the file at all is the kind of thing worth seeing early if it continues.

Three T13 reps and two T14 reps again emitted their ROUTE token after an initial look-around ("I'll start by checking what data is available"), the same compliance deviation recorded pre-edit, with no effect on classification.

## Scope

Two descriptions, synthetic queries, prompted dispatch with a stated catalog and a forced route declaration — not real installation, and not the four-skill deployment check `decisions/003` still owes.
