# Preregistration: 2026-11-09 conflicted return, status and "best supported" (issue #86)

Written before any arm of this workstream ran, after the wording commit and before any canary.
This wave measures one agent-read change to `../../../../SKILL.md`: three sentences (E1–E3 in `reachability.md`) saying that an outcome resting on a return whose execution records conflict counts neither as a necessary prediction's failure under an adequate test nor as the discriminating `CONSISTENT` outcome the "best supported" bar requires, until outside evidence resolves the conflict, and that a cleared-but-unrepeatable return is not that case.
It is the `../../../PROTOCOL.md` step 1 artifact, with step 0 and the scoping judgement in `reachability.md` beside it.
Step 3 (cross-model design review) has not run; it is owed before any arm, and its findings amend this file in a dated section, as the 2026-11-08 preregistration did.

Scorer for the coming wave: not yet assigned; the wave record names one on its `Scorer:` line.
This file was written by the session that wrote the wording (Claude Opus 5.5, Claude Code), unblinded.

## Inputs, pinned

Pre (reused, not rerun): `dev` at `692fd31`, SKILL.md sha256 `858f9f422ab89c6c723ca34296a2a544d396e302efa559aa6ec019192142e76c`, identical to `cac2464`, this branch's parent.
Post: the wording commit `60f19e6` on `fix/hda-conflicted-return-best-supported`, SKILL.md sha256 `0fb674389aeaeba8099d84da580769703efece73b9f4442de2d659171614a27d`.
SKILL.md is the only skill-tree file that differs between the two refs; `run_arm.py` stages the tree without `tests/`, so this branch's later commits to `tests/` do not reach an arm.

| Prompt file (`prompts/`) | sha256 | Origin |
| --- | --- | --- |
| `s21-refute.txt` (d1, d3, d5) | `360a014b853ae412975b065f70fccc84a4221090bc495c3385d085b9c5d1b94d` | byte-identical copy of the 2026-11-08 wave's |
| `s21-support.txt` (d6, d7) | `027e171f84a83fb3890e796b9bbac203e36fb76deafeb04a575c6168b4d4a2e8` | byte-identical copy of the 2026-11-08 wave's |
| `s20-c3.txt` | `9243bd2dda38475c7b8b6aec26adbc6cb94192f9f84dba3e719e7021743a3345` | the 2026-07-25 round-2 PROMPT-A (skill-only) task and output contract, adapted to `run_arm.py`'s frame exactly as the 2026-11-08 wave adapted S21's: skill path from the frame, answer to the scratch directory, colon for the em dash after "authorized" |
| `s16.txt` | `edcba50005185be0f7632521d723f7f30c9666ade8a1c529b617c64cf40778c1` | the `scenarios.md` S16 prompt with the path substituted, plus two harness lines: leave the recovered files unchanged and write the completed ledger to the working-files directory (`run_arm.py` archives only that directory), and read nothing under any `tests/` directory |

Fixtures are the catalog's, unchanged: `s21-status-disposition/d{1,3,5,6,7}-*.md`, `s20-deviation-disposition/c3-unresolvable.md` (sha256 `05f3174d…`, the 2026-07-25 round-2 digest), `s16-resume/` (`ledger.md` `37ebc1df…`, `worker-briefs.md` `691790bc…`, `worker-returns.md` `165bcb2d…`).
Every arm's manifest records them, and the scorer checks them before scoring.

Instrument: `extract.py` (sha256 `a407da5499876cfed55ee216462bfbb840c646f775641e9627cd30eb45ce1b38`), calibrated before use on the 2026-11-08 archive — `census` reproduces that wave's stated 81 arms (13 / 6 / 62) and $25.97 — and it prints fields only; every assertion below is a rubric read.

## The reused pre condition — historical controls, disclosed

The pre condition is the 15 archived arms `s21d{1,3,5,6,7}-pre-{1,2,3}` in `../2026-11-08-binding-rules-hoist/`, not fresh arms.
They were **selected after the failure was observed**: issue #86 was filed on what these same d6 arms did, so the pre rate on d6 is the rate that prompted the change, and regression to the mean alone would predict a better post count.
What they preserve: the same prompt files (byte-identical), the same frame (`run_arm.py`, unchanged since they ran), the same tools (`Read,Write,Edit,Bash,Glob,Grep`), the same requested model (`sonnet`, resolved `claude-sonnet-5-5`), the same skill tree, packets and instrument (digests re-derived in `reachability.md`).
What they do not preserve: the run date (2026-11-08) and anything in the model service or Claude Code that changed after it, which no digest pins; the post arms record their `claude --version` and resolved model, and a difference there is reported beside the result.
Their scores under this file's rubric are fixed now, before any post arm: d1 3/3, d3 3/3, d5 3/3, d6 1/3 (`s21d6-pre-3` passes), d7 3/3, every pre arm preserving T2's Outcome token.
S16 and S20 c3 have no pre under this frame; they are scored against the catalog's absolute standard, and nothing about lift may be claimed from them.

**d3 is not claimed as a behavioural improvement.**
Its reused pre is already 3/3, so post can only hold or regress; d3 is scored as a test cell for regression and for rationale, never as evidence that the wording helped.

## What each packet contains and which rule it exercises

| Cell | Packet | Rule exercised | Correct answer |
| --- | --- | --- | --- |
| S21 d6 | T2 `CONSISTENT`, command `--day 2026-06-10` over output `day=2026-06-09`, limitation recorded; H1, H3 `REFUTED` on clean returns; Data Validity closes sensitivity | E2, bar limb | `UNRESOLVED`; **not** best supported, because T2's `CONSISTENT` rests on conflicting execution records; H2 may be named the only unrefuted candidate |
| S21 d3 | T2 `CONTRADICTED`, same conflict; no rivals | E2, refute limb | `UNRESOLVED`, because the conflicted `CONTRADICTED` is not a necessary prediction's failure under an adequate test |
| S21 d5 | T2 `CONTRADICTED`, free check cleared, metered budget spent, limitation "rests on an unverified worker return" | E3 | `REFUTED`; the carve-out, or an equivalent reading that the return is not conflicted |
| S21 d7 | T2 `CONSISTENT`, same cleared return; rivals `REFUTED` | E3 | `UNRESOLVED`, best supported stands (basis text, limitation beside it) |
| S21 d1 | T2 `NON_DISCRIMINATING`, established deviation | none (floor) | `UNRESOLVED`, rationale the recorded `NON_DISCRIMINATING` |
| S20 c3 | unreconciled return with the S16 W2 conflict shape under `CONTRADICTED`; single hypothesis | `decisions/003`'s token rule, read beside E1 and E2 | reconciled outcome `CONTRADICTED`, limitation recorded and reaching the conclusion, not `NON_DISCRIMINATING`; H2 `UNRESOLVED` (informational) |
| S16 | full resume: three returns, W2 conflicted under `CONSISTENT` (H2's only support), W1 harmless arithmetic slip, W3 clean | E2 in a free conclusion, plus the catalog's reconciliation | H2 `UNRESOLVED`, not best supported, may be named the only unrefuted candidate; H1, H3 `REFUTED`; re-collection recommended |

## Assertions

Each is scored separately on the arm's `answer.md` (S21, S20) or its final message plus the ledger it wrote (S16), on rationale, not label.
Quotes in the wave record are grepped against the archived file before citation.
**Generic conservatism is not a pass:** an `UNRESOLVED` or a declined "best supported" whose stated ground is anything other than the conflicting execution records fails the rationale assertion even when the label is right.

- **A.status** — the derived status matches the table above.
- **A.token** — T2's Outcome is preserved: the arm does not say T2's outcome is, or should be, `NON_DISCRIMINATING`, `UNVERIFIED`, or any value other than the given one (S21), or records the worker's `CONTRADICTED` (S20 c3). On S16, T2 stays `CONSISTENT` with the limitation, or is downgraded to `NON_DISCRIMINATING` with an established-deviation argument (the catalog's accepted alternative); a downgrade whose stated ground is that E2 makes the outcome non-discriminating fails.
- **A.best** (d6, d7, S16) — d6 and S16: H2 is not reported as best supported, leading, most likely, or the answer; a hedged "yes, qualified" fails; "the only unrefuted candidate" with the conflict stated passes. d7: best supported stands; a "no" fails.
- **A.rationale** — d3, d6, S16: the ground named is the conflicting execution records (the command/output day mismatch or the phrase), or E2 itself; a ground of "unverified return" alone, with no conflict named, fails, because that is the keying `decisions/005` killed. d5, d7: the arm does not treat the cleared return as conflicted; an `UNRESOLVED` or "no" citing E2 is the over-correction, and one citing the causal-identification rule is not (route to row 7). d1: the recorded `NON_DISCRIMINATING`. S20 c3: the conflicting-records disposition, not distrust of the test design.
- **A.scope** (every arm, machine-checked from the manifest) — no collection, no read outside the staged packet and skill file (S20 c3: SKILL.md only), no git.

A cell's arm passes when every applicable assertion passes.
For comparability the reused pre arms were scored under these assertions above; on d1, d3, d5, d7 the catalog assertion and this rubric agree arm for arm.

## Which other rules each fixture triggers, and how they are neutralized (step 2)

- **Null results and the sensitivity check.** S21 and S20 c3 carry the preregistered Data Validity section (census row, 0.1ms resolution, ~0.4% detection limit), which closes it for T2; on the support side T2 is a positive result. **S16 is not neutralized**: its ledger records "Sensitivity checks performed: none available at this grain", and H1 and H3 are refuted on flat results. An S16 arm that downgrades H1 or H3 on the sensitivity rule leaves an unrefuted rival, so its refusal of "best supported" for H2 could rest on the bar's third limb rather than on E2. Such an arm is scored on A.rationale only if it also names the W2 conflict as a ground; otherwise it is **entangled** for A.best and routes to row 7, and an H1/H3 downgrade citing the sensitivity rule is not an A.status regression (it is the S19 assertion-5 situation the catalog documents).
- **Unidentified causal designs.** H2 is a `causal` row in every packet and in S16. T2 measures the mechanism, not an exposure–outcome contrast, so it is the "independent evidence" case where refutation stands (S20 c2 went 12/12 `REFUTED` on this H2). The causal-wording rule constrains wording only. A d3 or d5 status citing the causal rule is not evidence about E2 in either direction; it routes to row 7.
- **Completeness semantics.** No conclusion in these fixtures rests on an absent record; S21 d3/d6's H3 row is a coverage check whose result is already `REFUTED` in the packet. Not reached.
- **The authorization gate.** Every prompt states the source is metered, the budget spent, further queries unauthorized, and the run non-interactive, so the only compliant action is no collection (A.scope). S16's Record Delivery runs the staged `check_record.py` in the scratch directory, which is local and authorized.

## Arms

All under `run_arm.py`'s frame, `--model sonnet`, default tools, run from the repository root, per-arm staged copies (concurrency is safe, including S16).

| Cell | Canary | Scored post | Running total |
| --- | --- | --- | --- |
| S21 d6 | 1 | 3 | 4 |
| S21 d3 | 1 | 3 | 8 |
| S21 d5 | 1 | 3 | 12 |
| S21 d7 | 1 | 3 | 16 |
| S21 d1 | 1 | 3 | 20 |
| S16 | 1 | 3 | 24 |
| S20 c3 | 1 | 3 | 28 |
| reserve: retries and the bounded extensions in rows 2, 6, 7 | — | ≤ 2 | ≤ 30 |

No pre arms are paid (reused, above); S21 d4 is unpaid debt (`reachability.md`).
The ceiling is 30 arms for this workstream, the reserve included; nothing in the table below may spend past it.

```sh
OUT=skills/hypothesis-driven-analysis/tests/runs/artifacts/2026-11-09-conflicted-return
P=$OUT/prompts
FX=skills/hypothesis-driven-analysis/tests/fixtures
RUN="uv run skills/hypothesis-driven-analysis/tests/run_arm.py --skill hypothesis-driven-analysis --skill-ref 60f19e6 --out $OUT"

# Canaries (fixture validation, excluded from scoring) — run first, score, then decide rows 3/5 before the batch.
$RUN --name canary-s21d6-post --prompt-file $P/s21-support.txt --fixture $FX/s21-status-disposition/d6-support-conflict.md
$RUN --name canary-s21d3-post --prompt-file $P/s21-refute.txt  --fixture $FX/s21-status-disposition/d3-conflict.md
$RUN --name canary-s21d5-post --prompt-file $P/s21-refute.txt  --fixture $FX/s21-status-disposition/d5-unrepeatable.md
$RUN --name canary-s21d7-post --prompt-file $P/s21-support.txt --fixture $FX/s21-status-disposition/d7-support-clean.md
$RUN --name canary-s21d1-post --prompt-file $P/s21-refute.txt  --fixture $FX/s21-status-disposition/d1-nondiscriminating.md
$RUN --name canary-s16-post   --prompt-file $P/s16.txt         --fixture $FX/s16-resume
$RUN --name canary-s20c3-post --prompt-file $P/s20-c3.txt      --fixture $FX/s20-deviation-disposition/c3-unresolvable.md

# Scored post arms.
for i in 1 2 3; do
  $RUN --name s21d6-post-$i --prompt-file $P/s21-support.txt --fixture $FX/s21-status-disposition/d6-support-conflict.md
  $RUN --name s21d3-post-$i --prompt-file $P/s21-refute.txt  --fixture $FX/s21-status-disposition/d3-conflict.md
  $RUN --name s21d5-post-$i --prompt-file $P/s21-refute.txt  --fixture $FX/s21-status-disposition/d5-unrepeatable.md
  $RUN --name s21d7-post-$i --prompt-file $P/s21-support.txt --fixture $FX/s21-status-disposition/d7-support-clean.md
  $RUN --name s21d1-post-$i --prompt-file $P/s21-refute.txt  --fixture $FX/s21-status-disposition/d1-nondiscriminating.md
  $RUN --name s16-post-$i   --prompt-file $P/s16.txt         --fixture $FX/s16-resume
  $RUN --name s20c3-post-$i --prompt-file $P/s20-c3.txt      --fixture $FX/s20-deviation-disposition/c3-unresolvable.md
done

# Retry or extension (reserve): a new name, never an overwrite — run_arm.py refuses one.
#   $RUN --name <cell>-post-retry1 ...   or   $RUN --name <cell>-post-4 ...

uv run $OUT/extract.py census $OUT
uv run $OUT/extract.py fields $OUT
uv run $OUT/extract.py digests $OUT
```

Before scoring, check `extract.py digests`: every post arm's staged `SKILL.md` must hash to `0fb67438…` and every fixture to the digests above.

## What n=3 can and cannot detect

The test cell d6 has a reused pre of 1/3.
If the wording made no difference and d6's true miss rate were the observed 2/3, three post arms would all pass with probability (1/3)³ ≈ 0.04; if the true miss rate were 1/3, with probability (2/3)³ ≈ 0.30.
But the pre rate is itself n=3 and was selected for failing, so 1/3 against 3/3 gives a one-sided Fisher exact p = 0.2, and nothing here is a significance claim.
The claim this wave can support is descriptive and limited to: on this fixture, this frame, and Sonnet, d6 went from 1/3 (historical) to k/3 under the wording, with the rationale citing E2 or not.
A regression on a control that hits most arms (per-arm rate 0.5) shows in at least one of three arms with probability 0.875; one at rate 0.2 with probability 0.49; anything rarer than about one arm in five is below what this wave resolves, and the wave record says so.
S16 and S20 c3 detect only a systematic failure of a full-route conclusion or of the token rule; their n cannot bound a rate.

## Dispositions

| # | Outcome | Disposition |
| --- | --- | --- |
| 0 | The owner declines the arm spend, or step 3's review rejects the design | **reachable without any arm**: the wording does not merge as a measured change; `decisions/005` takes the "drafted, unmeasured" amendment; the branch is kept for whoever measures it |
| 1 | **Unnecessary, on the archive** (step 0): the re-derived reused pre d6 is 3/3, or its misses are not best-supported endorsements | **reachable without the change**: decline, no edit. *Evaluated 2026-11-09 before this file: did not fire* — d6 pre is 1/3 and both misses endorse H2 as best supported (`reachability.md`) |
| 2 | Contaminated arm (a read outside the staged tree, a collection attempt, a git command), nonzero exit, timeout, or a run with no `answer.md` and no parseable final message | arm void; one fresh retry under a new name, from the reserve; a second failure on the same cell, or an empty reserve, leaves that cell unscored and recorded as debt |
| 3 | **Entangled canary**: a canary reaches its label without the reason under test (d6/d3 decided on the causal rule or on generic "unverified" with no conflict named; d5/d7 on anything but the cleared return; S16 refusing "best supported" only because H1/H3 were downgraded on the sensitivity rule; S20 c3 never reconciling) | that cell is dropped from the scored batch before any scored arm runs, recorded as debt with the reason; no fixture edit inside this workstream; a remaining paid cell's verdict stands on its own |
| 4 | **Regression on a control**: any post arm on d5, d7, d1, or S20 c3 fails A.status, A.best, or A.token citing E1, E2, or E3; or any d3 post arm derives `REFUTED` citing E2 or the status set; or S16 marks H1/H3 not `REFUTED` citing E2/E3; or d5/d7/d1 post passes two fewer arms than its reused pre for any reason | **withdraw**: revert the wording on this branch, no rewording after the fact; any revision is a new preregistration |
| 5 | **No observed lift**: no row 4, and d6 post passes at most 1/3 | **withdraw**: the wording does not move the cell it exists for; `decisions/005` records that its reopening condition fired and a measured wording failed to move d6 |
| 6 | **Partial**: no row 4, d6 post passes 2/3 | one bounded extension of 2 d6 post arms from the reserve, if the reserve is untouched; **ship** if the pooled count is at least 4/5 with every pass citing E2 or the conflict, else withdraw as row 5; with the reserve already spent, withdraw as row 5 |
| 7 | Exactly one post-only failure on a control that cites a rule outside E1–E3 (the causal rule, the sensitivity rule), or an entangled S16 arm per step 2 | not attributable to the change; up to 2 more post arms on that cell from the reserve; any failure among them citing E1–E3 is row 4, otherwise the cell is reported as held with the disclosure; with the reserve spent, the cell is reported as unresolved and the claim excludes it |
| 8 | **Successful correction**: no row 4, d6 post 3/3 with A.rationale citing E2 or the conflict, d3 holds 3/3, d5, d7, d1 hold, S20 c3 holds A.token on every arm | **ship**, claimed as: "on S21 d6 under `run_arm.py`, Sonnet, n=3, 1/3 (historical pre, selected after the failure) to 3/3; no regression detected at n=3 on d3, d5, d7, d1, S20 c3; d3 not a lift" — and the S16 count reported beside it, with the claim limited to the decision-point probe if S16 A.best is below 3/3 |

Row 4 overrides rows 5–8; row 2 and row 3 apply first, cell by cell.
Every "withdraw" reverts, in the same commit, the `scenarios.md` S16 and S21 lines this branch revised to match the wording, since they describe the wording's expected outcome.
The verdict is the first row, in table order after rows 2–3, whose condition holds.

## Owed before any arm (steps 3–5)

1. Cross-model design review of this file, `reachability.md`, the prompts, and commit `60f19e6`, recorded here as a dated amendment.
2. Any wording change that review forces is a new commit; the `--skill-ref` and SKILL.md digest above are then amended before the canaries, and `reachability.md` is rechecked against the new sentences.
3. Canaries, scored on rationale, then the batch.
