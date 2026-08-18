# Gate 4 — seam holds under C3

Verdict is scored per `2026-08-15-widening-prereg.md` § "Confirmatory wave", quoted verbatim, attributed:
> Gate 4 — seam (under C applied to the skill): `run_trigger.py` T13 5/5 to `exploratory-data-analysis` and T14 5/5 to `hypothesis-driven-analysis`.
> Fail → STOP; do not ship; commit the evidence.

No separate threshold is stated here; the rule above is the sole authority (per `AGENTS.md`'s single-authority rule for normative statements).

## Instrument

`skills/exploratory-data-analysis/tests/run_trigger.py --scenario t13 --reps 5 --order alternate --model claude-opus-5` and the same for `t14`, each writing into `skills/exploratory-data-analysis/tests/runs/artifacts/2026-08-15-widening/seam/`.
Scenarios: T13 = "Tell me about the Northgate Clinic account." (expected route: `exploratory-data-analysis`).
T14 = "Why did the Northgate Clinic account's spend drop last quarter?" (expected route: `hypothesis-driven-analysis`).

## SKILL.md carried C3 during the runs

`skills/exploratory-data-analysis/SKILL.md`'s frontmatter `description` was overwritten in the working tree with the text of `skills/exploratory-data-analysis/tests/eval/frozen-2026-08-15-C3.txt` before the runs, and the round trip was verified with the instrument's own `run_trigger.parse_description`, which reported 1021 chars matching the frozen file exactly.
The frozen file's sha256 is `828c5afc6c963186ffb44a4cdc273255ddff9aedb72765f3c4a006a3b10564df` (`shasum -a 256 skills/exploratory-data-analysis/tests/eval/frozen-2026-08-15-C3.txt`).
After the runs completed, `git checkout -- skills/exploratory-data-analysis/SKILL.md` reverted the working tree to the committed (shipped) description; this task's commit contains only the new artifacts under `tests/runs/artifacts/2026-08-15-widening/`, not the SKILL.md edit.
The real SKILL.md edit lands as its own clean commit in Tasks 9-10.

## Per-rep routing

All reps: exit=0, valid=True, 0 void, 0 retries.

| scenario | rep | catalog_order | route | valid | expected | match |
|---|---|---|---|---|---|---|
| t13 | 1 | eda-first | eda | True | exploratory-data-analysis | yes |
| t13 | 2 | hda-first | eda | True | exploratory-data-analysis | yes |
| t13 | 3 | eda-first | eda | True | exploratory-data-analysis | yes |
| t13 | 4 | hda-first | eda | True | exploratory-data-analysis | yes |
| t13 | 5 | eda-first | eda | True | exploratory-data-analysis | yes |
| t14 | 1 | eda-first | hda | True | hypothesis-driven-analysis | yes |
| t14 | 2 | hda-first | hda | True | hypothesis-driven-analysis | yes |
| t14 | 3 | eda-first | hda | True | hypothesis-driven-analysis | yes |
| t14 | 4 | hda-first | hda | True | hypothesis-driven-analysis | yes |
| t14 | 5 | eda-first | hda | True | hypothesis-driven-analysis | yes |

T13: 5/5 routed to `exploratory-data-analysis`.
T14: 5/5 routed to `hypothesis-driven-analysis`.

Source data: `skills/exploratory-data-analysis/tests/runs/artifacts/2026-08-15-widening/seam/summary.tsv` and the per-rep `.detect.json`/`.jsonl`/`.stderr` files in the same directory, plus manifests `manifest-t13-20260818T021753Z.json` and `manifest-t14-20260818T023334Z.json`.

## Verdict

T13 5/5 to `exploratory-data-analysis`: **True**.
T14 5/5 to `hypothesis-driven-analysis`: **True**.

**VERDICT: PASS.**

Gates 1-4 all pass; per the prereg this ships as two commits (B, then C), with Tasks 9-10 landing the real SKILL.md edit and citing this gate's evidence.
