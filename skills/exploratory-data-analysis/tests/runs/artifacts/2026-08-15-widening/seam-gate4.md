# Gate 4 — seam holds under C3

Verdict is scored per `2026-08-15-widening-prereg.md` § "Confirmatory wave", quoted verbatim, attributed:
> Gate 4 — seam (under C applied to the skill): `run_trigger.py` T13 5/5 to `exploratory-data-analysis` and T14 5/5 to `hypothesis-driven-analysis`.
> Fail → STOP; do not ship; commit the evidence.

No separate threshold is stated here; the rule above is the sole authority (per `AGENTS.md`'s single-authority rule for normative statements).

## 2026-08-18 correction — first attempt was invalid

The first attempt at this gate (commit `0732e44`) is invalid and is archived, not deleted, at `skills/exploratory-data-analysis/tests/runs/artifacts/2026-08-15-widening/seam-invalid-wrong-checkout/`.
`run_trigger.py` hardcodes `REPO = Path("/Users/bdc/projects/data-reasoning")` at line 26 and derives `EDA_SKILL = REPO / "skills/exploratory-data-analysis/SKILL.md"` from that constant, so the instrument always reads the SKILL.md in the main repo checkout, never the worktree's copy, regardless of the harness's own cwd.
The first attempt applied C3 to the worktree's SKILL.md and verified the round trip against that same worktree path, which passed — but the instrument itself, when invoked, read the main repo's unmodified SKILL.md, which still carried the shipped description.
The archived manifests `manifest-t13-20260818T021753Z.json` and `manifest-t14-20260818T023334Z.json` record `eda_description_sha256` `a80b97340c2c3b8bd412ac595f8b2d2f51f8c5ec20e709c7c49160d5562a0a38`, length 1019 — the shipped text, not C3.
That first attempt's 5/5 + 5/5 routing result was therefore measured under the shipped description, not under C3, and Gate 4 was never actually exercised by it.
The corrected procedure below applies C3 to the main repo checkout (the file the instrument actually reads), and verifies the binding two ways: before the runs, via the instrument's own `parse_description(EDA_SKILL)`, and after the runs, by reading `eda_description_sha256`/`eda_description_len` back out of each run's own manifest — so the check reads exactly what the instrument read, not a copy of it.

## Manifest binding evidence (corrected run)

All three manifests written by the corrected run record `eda_description_sha256` `9a4e874b8af2220d1faa26d4a958a6e687439f44f49195b9abb64daef426e80d`, length 1021 — the sha256 of the rstripped C3 text, matching the pre-run `parse_description(EDA_SKILL)` check exactly:
- `manifest-t13-20260818T032548Z.json`: sha `9a4e874b...`, len 1021.
- `manifest-t14-20260818T035248Z.json`: sha `9a4e874b...`, len 1021.
- `manifest-t14-20260818T132836Z.json` (rep 6 retry): sha `9a4e874b...`, len 1021.

This confirms the corrected run genuinely exercised C3 in the checkout the instrument reads.

## SKILL.md carried C3 in the main repo checkout during the runs

The main repo's `skills/exploratory-data-analysis/SKILL.md` (at `/Users/bdc/projects/data-reasoning/skills/exploratory-data-analysis/SKILL.md`, outside this worktree) was overwritten in place with the text of `skills/exploratory-data-analysis/tests/eval/frozen-2026-08-15-C3.txt` before the corrected runs.
The round trip was verified with the instrument's own `run_trigger.parse_description(EDA_SKILL)`, which reported 1021 chars and sha256 `9a4e874b8af2220d1faa26d4a958a6e687439f44f49195b9abb64daef426e80d`, matching the frozen file's rstripped text exactly.
After all corrected runs (including the rep 6 retry) completed, `git checkout -- skills/exploratory-data-analysis/SKILL.md` reverted the main repo checkout to the shipped description; `git status --porcelain -- skills/exploratory-data-analysis/SKILL.md` in the main repo was confirmed clean afterward.
This task's commit contains only artifacts under `tests/runs/artifacts/2026-08-15-widening/`; the real SKILL.md edit lands as its own clean commit in Tasks 9-10.

## Per-rep routing (corrected run)

| scenario | rep | catalog_order | route | valid | invalid_reason | expected | match |
|---|---|---|---|---|---|---|---|
| t13 | 1 | eda-first | eda | True | - | exploratory-data-analysis | yes |
| t13 | 2 | hda-first | eda | True | - | exploratory-data-analysis | yes |
| t13 | 3 | eda-first | eda | True | - | exploratory-data-analysis | yes |
| t13 | 4 | hda-first | eda | True | - | exploratory-data-analysis | yes |
| t13 | 5 | eda-first | eda | True | - | exploratory-data-analysis | yes |
| t14 | 1 | eda-first | hda | True | - | hypothesis-driven-analysis | yes |
| t14 | 2 | hda-first | hda | True | - | hypothesis-driven-analysis | yes |
| t14 | 3 | eda-first | hda | True | - | hypothesis-driven-analysis | yes |
| t14 | 4 | hda-first | hda | True | - | hypothesis-driven-analysis | yes |
| t14 | 5 | eda-first | hda | **False** | exit code 1 | hypothesis-driven-analysis | **VOID — not scored** |
| t14 | 6 (retry of void rep 5) | hda-first | hda | True | - | hypothesis-driven-analysis | yes |

t14 rep 5 exited with code 1 and its transcript is invalid (`invalid_reason: "exit code 1"`); per the prereg's void discipline a void is never scored as a negative, so it is excluded and replaced by the rep 6 retry, which is valid and routed correctly on the first retry attempt.
T13: 5/5 valid reps routed to `exploratory-data-analysis`.
T14: 5/5 valid reps (reps 1-4 and the rep 6 retry) routed to `hypothesis-driven-analysis`; rep 5 was a void, retried once.

Source data: `skills/exploratory-data-analysis/tests/runs/artifacts/2026-08-15-widening/seam/summary.tsv` and the per-rep `.detect.json`/`.jsonl`/`.stderr` files in the same directory, plus manifests `manifest-t13-20260818T032548Z.json`, `manifest-t14-20260818T035248Z.json`, and `manifest-t14-20260818T132836Z.json`.
The invalid first attempt's evidence is preserved at `skills/exploratory-data-analysis/tests/runs/artifacts/2026-08-15-widening/seam-invalid-wrong-checkout/`.

## Verdict

T13 5/5 valid reps to `exploratory-data-analysis`: **True**.
T14 5/5 valid reps to `hypothesis-driven-analysis` (reps 1-4 plus the rep 6 retry, rep 5 void excluded): **True**.

**VERDICT: PASS.**

Gates 1-4 all pass; per the prereg this ships as two commits (B, then C), with Tasks 9-10 landing the real SKILL.md edit and citing this gate's evidence.
