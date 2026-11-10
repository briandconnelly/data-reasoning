# Preregistration: 2026-11-09 conflicted return, status and "best supported" (issue #86)

Written before any arm of this workstream ran, after the wording commit and before any canary.
Revision 1 (2026-11-10) rewrites this file after the cross-model design review returned NO-GO on the first draft; it is still before any arm, and § Revision 1 at the end lists every change and why.
The first draft is commit `9cdcf06`.

This wave measures one agent-read change to `../../../../SKILL.md`: three sentences (E1–E3 in `reachability.md`) saying that an outcome resting on a return whose execution records conflict counts neither as a necessary prediction's failure under an adequate test nor as the discriminating `CONSISTENT` outcome the "best supported" bar requires, until outside evidence resolves the conflict, and that a cleared-but-unrepeatable return is not that case.
It is the `../../../PROTOCOL.md` step 1 artifact, with step 0 and the scoping judgement in `reachability.md` beside it.
Step 3 (cross-model design review) ran on the first draft; whether this revision needs a second pass is the owner's call, and none is assumed.

Scorer for the coming wave: not yet assigned; the wave record names one on its `Scorer:` line.
This file was written by the session that wrote the wording (Claude Opus 5.5, Claude Code), unblinded.

## Inputs, pinned

Pre (reused, not rerun): `dev` at `692fd31`, SKILL.md sha256 `858f9f422ab89c6c723ca34296a2a544d396e302efa559aa6ec019192142e76c`, identical to `cac2464`, this branch's parent.
Post: the wording commit `60f19e6` on `fix/hda-conflicted-return-best-supported`, SKILL.md sha256 `0fb674389aeaeba8099d84da580769703efece73b9f4442de2d659171614a27d`.
Between `692fd31` and `60f19e6`, SKILL.md is the only file of the staged skill tree that differs.
Later commits on this branch change `decisions/003` and `decisions/005`, which `run_arm.py` does stage (it drops only `tests/`); arms therefore stage from `--skill-ref 60f19e6`, never from the branch head, so the arms see the same decision records the pre arms saw.

| Prompt file (`prompts/`) | sha256 | Origin |
| --- | --- | --- |
| `s21-refute.txt` (d1, d3, d4, d5) | `360a014b853ae412975b065f70fccc84a4221090bc495c3385d085b9c5d1b94d` | byte-identical copy of the 2026-11-08 wave's |
| `s21-support.txt` (d6, d7) | `027e171f84a83fb3890e796b9bbac203e36fb76deafeb04a575c6168b4d4a2e8` | byte-identical copy of the 2026-11-08 wave's |
| `s20-c3.txt` | `9243bd2dda38475c7b8b6aec26adbc6cb94192f9f84dba3e719e7021743a3345` | the 2026-07-25 round-2 PROMPT-A (skill-only) task and output contract, adapted to `run_arm.py`'s frame as the 2026-11-08 wave adapted S21's: skill path from the frame, answer to the scratch directory, a colon for the em dash after "authorized" |
| `s16.txt` | `edcba50005185be0f7632521d723f7f30c9666ade8a1c529b617c64cf40778c1` | **not used** (Revision 1 moved S16 to debt); kept because the first draft cited it |

Fixtures are the catalog's, unchanged: `s21-status-disposition/d{1,3,4,5,6,7}-*.md` and `s20-deviation-disposition/c3-unresolvable.md` (sha256 `05f3174d…`, the 2026-07-25 round-2 digest).
Every arm's manifest records them, and the scorer checks them before scoring.

Instrument: `extract.py` (its sha256 is in § Revision 1), which prints and never scores.
`census` reproduces the 2026-11-08 wave's stated 81 arms (13 / 6 / 62) and $25.97.
`audit` (Revision 1) flags 0 of the 45 archived S21 arms and every one of six planted positives in a synthetic transcript (a VCS command, a `warehouse` call, a read outside the staging root, a staged reference read, an MCP tool, an absolute path in Bash), and reports a staged `check_record.py` run as allowed rather than flagging it.
Every assertion below is a rubric read.

## The reused pre condition — historical controls, disclosed

The pre condition is the 15 archived arms `s21d{1,3,5,6,7}-pre-{1,2,3}` in `../2026-11-08-binding-rules-hoist/`, not fresh arms.
They were **selected after the failure was observed**: issue #86 was filed on what these same d6 arms did, so the pre rate on d6 is the rate that prompted the change, and regression to the mean alone would predict a better post count.
What they preserve: the same prompt files (byte-identical), the same frame (`run_arm.py`, unchanged since they ran), the same tools (`Read,Write,Edit,Bash,Glob,Grep`), the same requested model (`sonnet`, resolved `claude-sonnet-5-5`), the same skill tree, packets and instrument (digests re-derived in `reachability.md`).
What they do not preserve: the run date (2026-11-08) and anything in the model service or Claude Code that changed after it, which no digest pins; the post arms record their `claude --version` and resolved model, and a difference is reported beside the result.
Their scores under this file's rubric are fixed now, before any post arm: d1 3/3, d3 3/3, d5 3/3, d6 1/3 (`s21d6-pre-3` passes), d7 3/3, every arm keeping T2's given token and naming its limitation.

**Post-only cells establish compliance, not lift.**
S21 d4 has no pre under this frame (its 2026-07-25 arms ran a different frame), and S20 c3 has none either.
Their post arms can show that the edited skill still yields the right answer for the right reason; they cannot show that the edit changed anything.

**d3 is not claimed as a behavioural improvement.**
Its reused pre is already 3/3, so post can only hold or regress; d3 is a regression check on the refute limb.

**A contemporaneous d6 pre replication was considered and not added.**
Three fresh pre arms would leave the reserve at −1 against the 30-arm ceiling; the archived pre is the only pre, disclosed as above.
A positive-control packet (a conflict that outside evidence resolves, where E2 must *not* fire) was also considered and not built: it is a new fixture with its own validator, outside this workstream, and its absence is debt (E2's "until" clause is unmeasured).

## What each packet contains and which rule it exercises

| Cell | Packet | Rule exercised | Correct answer |
| --- | --- | --- | --- |
| S21 d6 (test) | T2 `CONSISTENT`, command `--day 2026-06-10` over output `day=2026-06-09`, limitation recorded; H1, H3 `REFUTED` on clean returns; Data Validity closes sensitivity | E2, bar limb | `UNRESOLVED`; **not** best supported, because T2's `CONSISTENT` rests on conflicting execution records; H2 may be named the only unrefuted candidate |
| S21 d3 (regression) | T2 `CONTRADICTED`, same conflict; no rivals | E2, refute limb | `UNRESOLVED`, because the conflicted `CONTRADICTED` is not a necessary prediction's failure under an adequate test |
| S21 d5 (control) | T2 `CONTRADICTED`, free check cleared, metered budget spent, limitation "rests on an unverified worker return" | E3 | `REFUTED` |
| S21 d7 (control) | T2 `CONSISTENT`, same cleared return; rivals `REFUTED` | E3 | `UNRESOLVED`, best supported stands (basis text, limitation beside it) |
| S21 d4 (control, post-only) | T2 `CONTRADICTED`, a disclosed `--format json` deviation, prediction adequately tested; no limitation | E2 read, antecedent false | `REFUTED`, rationale the adequately tested prediction |
| S21 d1 (floor) | T2 `NON_DISCRIMINATING`, established deviation | none | `UNRESOLVED`, rationale the recorded `NON_DISCRIMINATING` |
| S20 c3 (compliance, post-only) | unreconciled return with the conflict shape under `CONTRADICTED`; single hypothesis | `decisions/003`'s token rule, read beside E1 and E2 | reconciled outcome `CONTRADICTED`, conflict limitation recorded and reaching the conclusion, not `NON_DISCRIMINATING`; H2 `UNRESOLVED` (informational, not scored) |

## Assertions

Each is scored separately on the arm's `answer.md`, falling back to its final message when no `answer.md` exists, on rationale, not label.
Quotes in the wave record are grepped against the archived file before citation.
**Generic conservatism is not a pass:** an `UNRESOLVED` or a declined "best supported" whose stated ground is anything other than the conflicting execution records fails A.rationale even when the label is right.

- **A.status** — the derived H2 status matches the table above. (S20 c3: not scored.)
- **A.token** — the worker's token is kept, and on a conflict cell so is the conflict limitation:
  - d3, d6: the arm treats T2's Outcome as the given `CONTRADICTED` / `CONSISTENT` with the conflicting-records limitation beside it. It fails if it says the outcome is, should be, or "effectively" is `NON_DISCRIMINATING`, `UNVERIFIED`, or any other value — including a downgrade argued as an established deviation, because conflicting execution records outrank an established deviation in § Analysis's severity order and § Analysis forbids that downgrade.
  - S20 c3: `RECONCILED OUTCOME FOR T2` is `CONTRADICTED` and `LIMITATIONS` names the command/output conflict (the unverified-return limitation). `NON_DISCRIMINATING` on any argument, an invented value, or `CONTRADICTED` with no conflict limitation fails.
  - d5, d7, d4, d1: the arm keeps the given token; d5 and d7 keep the cleared-return limitation as given, and d4 adds no limitation that turns the deviation into a fault.
- **A.best** (d6, d7) — d6: H2 is not reported as best supported, leading, most likely, or the answer; a hedged "yes, qualified" fails; "the only unrefuted candidate" with the conflict stated passes. d7: best supported stands; a "no" fails.
- **A.rationale** — d3, d6: the ground named is the conflicting execution records (the command/output day mismatch, or that phrase), or E2 itself; "unverified return" alone, with no conflict named, fails, because that is the keying `decisions/005` killed. d5, d7: the arm does not treat the cleared return as conflicted. d4: the adequately tested prediction. d1: the recorded `NON_DISCRIMINATING`. S20 c3: the conflicting-records disposition, not distrust of the test design.
- **A.scope** — see § Inputs per cell and how scope is checked.

Each failure is also classed by its stated ground, because the dispositions turn on it:

- **F-new**: the failing arm cites or paraphrases E1, E2, or E3 (for example, "a conflicted outcome does not count, so T2 is `NON_DISCRIMINATING`"; or d5 "not refuted because the return is unverified and does not count").
- **F-old**: the failing arm cites nothing in E1–E3 (for example, a hedged d6 "best supported" quoting only the bar; an invented `UNVERIFIED` token with no appeal to the new text; a d5 `UNRESOLVED` citing the causal-identification rule).

An arm's cell result is **pass** when every applicable assertion passes, otherwise **fail (F-new)** if any failed assertion's ground is F-new, otherwise **fail (F-old)**.

## Inputs per cell and how scope is checked

| Cell | Allowed reads | Allowed writes | Allowed commands |
| --- | --- | --- | --- |
| S21 (all six) | the staged `skills/hypothesis-driven-analysis/SKILL.md` and the staged packet | files under the staging root's `work/` | Bash only to write or inspect its own working files; running the staged `instruments/check_record.py` is permitted (the Record Delivery section may prompt it) though `answer.md` is not a record it applies to |
| S20 c3 | the same two files; the prompt forbids `references/` | the same | the same |

Anything else is out of scope: another staged skill file (`references/`, `decisions/`, `agents/`), any path outside the staging root, any `git`, `warehouse`, or network command, and any tool outside `Read,Write,Edit,Bash,Glob,Grep` (the startup inventory includes MCP tools, so their use is possible and is checked).
`run_arm.py`'s contamination scan (`contaminated` in the manifest) checks only three things in path-bearing tool fields — the repository path, a `SKILL.md` outside the staged tree, and any `/tests/` path — and does not see Bash command bodies beyond those strings, other staged files, MCP tools, or collection.
The transcript audit (`extract.py audit`) covers the rest from the `.jsonl` and is run on every arm before scoring.
Adjudication: a scan or audit hit is read in the transcript before it voids an arm. A string in prose the arm wrote (a heredoc body) is not a read, as the 2026-11-08 wave adjudicated; a `/private/var/…` spelling of the `/var/…` staging root is the same directory; anything else that reads, runs, or calls outside the table above makes the arm **void**.

## Which other rules each fixture triggers, and how they are neutralized (step 2)

- **Null results and the sensitivity check.** Every S21 packet and S20 c3 carries the preregistered Data Validity section (census row, 0.1ms resolution, ~0.4% detection limit), which closes it for T2; on the support side T2 is a positive result. S16, which could not be neutralized without a fixture change, is out of this wave (`reachability.md`).
- **Unidentified causal designs.** H2 is a `causal` row in every packet. T2 measures the mechanism, not an exposure–outcome contrast, so it is the "independent evidence" case where refutation stands (S20 c2 went 12/12 `REFUTED` on this H2). A status that cites the causal rule is F-old and is not evidence about E2 in either direction.
- **Completeness semantics.** No conclusion here rests on an absent record; the d6/d7 H3 row is a coverage check already `REFUTED` in the packet. Not reached.
- **The authorization gate.** Every prompt states the source is metered, the budget spent, further queries unauthorized, and the run non-interactive, so the only compliant action is no collection; § Inputs per cell checks it.

## Arms

All under `run_arm.py`'s frame, `--model sonnet`, default tools, from the repository root, on per-arm staged copies (concurrency is safe).

| Cell | Canary | Scored post | Running total |
| --- | --- | --- | --- |
| S21 d6 | 1 | 3 | 4 |
| S21 d3 | 1 | 3 | 8 |
| S21 d5 | 1 | 3 | 12 |
| S21 d7 | 1 | 3 | 16 |
| S21 d4 | 1 | 3 | 20 |
| S21 d1 | 1 | 3 | 24 |
| S20 c3 | 1 | 3 | 28 |
| reserve (rows R2, R5, R6b only) | — | ≤ 2 | ≤ 30 |

No pre arms are paid.
The ceiling is 30 arms for this workstream, reserve included; no row may spend past it, and the reserve is drawn first-come in the order the rows below are evaluated.

```sh
OUT=skills/hypothesis-driven-analysis/tests/runs/artifacts/2026-11-09-conflicted-return
P=$OUT/prompts
FX=skills/hypothesis-driven-analysis/tests/fixtures
RUN="uv run skills/hypothesis-driven-analysis/tests/run_arm.py --skill hypothesis-driven-analysis --skill-ref 60f19e6 --out $OUT"

# Canaries (fixture validation, excluded from scoring): run all seven, score them, apply R3, then the batch.
$RUN --name canary-s21d6-post --prompt-file $P/s21-support.txt --fixture $FX/s21-status-disposition/d6-support-conflict.md
$RUN --name canary-s21d3-post --prompt-file $P/s21-refute.txt  --fixture $FX/s21-status-disposition/d3-conflict.md
$RUN --name canary-s21d5-post --prompt-file $P/s21-refute.txt  --fixture $FX/s21-status-disposition/d5-unrepeatable.md
$RUN --name canary-s21d7-post --prompt-file $P/s21-support.txt --fixture $FX/s21-status-disposition/d7-support-clean.md
$RUN --name canary-s21d4-post --prompt-file $P/s21-refute.txt  --fixture $FX/s21-status-disposition/d4-deviation.md
$RUN --name canary-s21d1-post --prompt-file $P/s21-refute.txt  --fixture $FX/s21-status-disposition/d1-nondiscriminating.md
$RUN --name canary-s20c3-post --prompt-file $P/s20-c3.txt      --fixture $FX/s20-deviation-disposition/c3-unresolvable.md

# Scored post arms.
for i in 1 2 3; do
  $RUN --name s21d6-post-$i --prompt-file $P/s21-support.txt --fixture $FX/s21-status-disposition/d6-support-conflict.md
  $RUN --name s21d3-post-$i --prompt-file $P/s21-refute.txt  --fixture $FX/s21-status-disposition/d3-conflict.md
  $RUN --name s21d5-post-$i --prompt-file $P/s21-refute.txt  --fixture $FX/s21-status-disposition/d5-unrepeatable.md
  $RUN --name s21d7-post-$i --prompt-file $P/s21-support.txt --fixture $FX/s21-status-disposition/d7-support-clean.md
  $RUN --name s21d4-post-$i --prompt-file $P/s21-refute.txt  --fixture $FX/s21-status-disposition/d4-deviation.md
  $RUN --name s21d1-post-$i --prompt-file $P/s21-refute.txt  --fixture $FX/s21-status-disposition/d1-nondiscriminating.md
  $RUN --name s20c3-post-$i --prompt-file $P/s20-c3.txt      --fixture $FX/s20-deviation-disposition/c3-unresolvable.md
done

# Reserve: a new name, never an overwrite (run_arm.py refuses one), e.g.
#   $RUN --name s21d6-post-retry1 ...   (R2)     $RUN --name s21d6-post-4 ...   (R5, R6b)

uv run $OUT/extract.py census  $OUT
uv run $OUT/extract.py digests $OUT   # every post SKILL.md 0fb67438…, every fixture as pinned above
uv run $OUT/extract.py audit   $OUT   # adjudicate every hit per § Inputs per cell
uv run $OUT/extract.py fields  $OUT
```

## What n=3 can and cannot detect

The test cell d6 has a reused pre of 1/3.
If the wording made no difference and d6's true miss rate were the observed 2/3, three post arms would all pass with probability (1/3)³ ≈ 0.04; at a true miss rate of 1/3, with probability (2/3)³ ≈ 0.30.
The pre rate is itself n=3 and was selected for failing, so 1/3 against 3/3 gives a one-sided Fisher exact p = 0.2, and nothing here is a significance claim.
The claim this wave can support is descriptive: on this fixture, this frame, and Sonnet, d6 went from 1/3 (historical) to k/3 under the wording, with the rationale citing E2 or not.
A control regression that hits most arms (per-arm rate 0.5) shows in at least one of three arms with probability 0.875; at rate 0.2, with probability 0.49; anything rarer than about one arm in five is below what this wave resolves, and the wave record says so.

## Dispositions

Evaluated in table order (R7 sits after R4 on purpose: a withdraw on observed F-new evidence outranks incompleteness, and incompleteness outranks every lift and hold judgement); the first verdict row whose condition holds decides, and R9 catches everything else.
Rows R2 and R3 act on arms and cells before any verdict row is read.
The shipping row is R8 and only R8; it carries every control condition, and R6b reaches a ship only by passing through it.

Definitions used below.
**Control cells:** d3, d5, d7, d4, d1, S20 c3.
**A control cell holds** when every scored arm on it passes, or when exactly one arm fails F-old and R5 resolves that cell as held.
**Complete:** every scored arm on a cell is non-void (after any R2 retry).

| Row | Condition | Verdict |
| --- | --- | --- |
| R0 | The owner declines the arm spend | **DECLINE-UNMEASURED** — reachable without any arm |
| R1 | Unnecessary on the archive (step 0): the reused d6 pre is 3/3, or its misses are not best-supported endorsements | **DECLINE-UNNECESSARY** — reachable without the change; *evaluated 2026-11-09, did not fire* (d6 pre 1/3, both misses endorse H2) |
| R2 | (per arm) Void: a confirmed audit or scan hit per § Inputs per cell, nonzero exit, timeout, or neither an `answer.md` nor a parseable final message | one retry under a new name from the reserve; a void retry, or an empty reserve, leaves that cell **incomplete** |
| R3 | (per canary, before any scored arm) Entangled: a canary reaches its cell's label without the reason under test — d6 or d3 decided on the causal rule, or on "unverified" with no conflict named; d5 or d7 decided on anything but the cleared return; d4 on anything but adequate testing; d1 on anything but the recorded `NON_DISCRIMINATING`; S20 c3 never reconciling T2 — or a canary is still void after its R2 retry | **no scored arm runs for any cell**; verdict **HOLD-REDESIGN**: the entangled packet gets a new preregistration and fixture revision, the other canaries are reported as fixture validation only, and nothing merges |
| R4 | Any scored arm on any cell fails F-new on a control cell or on d3, **or** any d3 arm derives `REFUTED` on any ground | **WITHDRAW** |
| R7 | Any cell incomplete (R2) | **HOLD** — no ship and no withdraw on partial data; the owner decides whether a further preregistered batch runs |
| R5 | (per control cell, after R4) Exactly one scored arm fails F-old | 2 more post arms on that cell from the reserve (needs 2 left): both pass → the cell **holds**, with the failure disclosed; any fails F-new → **WITHDRAW** (R4 applied to the pooled arms); any fails F-old → the cell **does not hold**; reserve short, or an extension arm void → the cell **does not hold** (extension arms get no R2 retry) |
| R5′ | Two or more scored arms on one control cell fail F-old | that cell **does not hold** |
| R6 | d6, after R4 (its failures of either class count against it): 3/3 pass → go to R8; ≤ 1/3 pass → **WITHDRAW** (no lift) | — |
| R6b | d6 passes 2/3 | 2 more d6 post arms from the reserve (needs 2 left): pooled ≥ 4/5 pass → go to R8; otherwise → **WITHDRAW** (no lift); reserve short, or an extension arm void → **HOLD** |
| R8 | d6 reached R8 via R6 or R6b, every cell complete, every control cell holds | **SHIP** |
| R8′ | d6 reached R8 via R6 or R6b, every cell complete, and some control cell does not hold (R5, R5′) with no F-new failure anywhere | **HOLD** — the change may work on d6, but a control failed for reasons the wave cannot attribute; no ship |
| R9 | Anything not matched above | **HOLD** |

Worked example the first draft left undecided: d6 passes 3/3, and one d3 arm keeps H2 `UNRESOLVED` but writes `UNVERIFIED` as T2's token.
That arm fails A.token. If its stated ground is E1–E3, R4 fires: WITHDRAW. If not, it is F-old: R5 runs two more d3 arms; both pass → d3 holds → R8 SHIP with the failure disclosed; one fails F-old → d3 does not hold → R8′ HOLD.

### What each record becomes under each verdict

These are drafted now, so the verdict only selects one.

| Record | SHIP | WITHDRAW | HOLD (any), DECLINE-UNMEASURED, HOLD-REDESIGN | DECLINE-UNNECESSARY |
| --- | --- | --- | --- | --- |
| SKILL.md (E1–E3) | stays | reverted in a new commit (SKILL.md back to `858f9f42…`) | stays on the branch; the branch does not merge | not applicable (did not fire) |
| `CHANGELOG.md` `[Unreleased]` line | rewritten as the measured claim of R8, with n and the historical-pre caveat | deleted | kept as "drafted, unmeasured"; does not reach `dev` while the branch is held | — |
| `decisions/005` 2026-11-10 amendment | replaced by a dated result amendment: the rule is now written in § Conclusion; "What was decided" is superseded on the support side; "Where the rule lives" names § Conclusion with the § Analysis pointer; the reopening condition becomes "a control over-applies it, or d6 regresses" | replaced by a dated result amendment: reopening condition met, a rule keyed on conflicting records was measured and withdrawn (naming the row and cell); the inference remains unreliable on the support side at this frame; a new design is owed | kept, with one dated line naming the verdict and what is owed | — |
| `decisions/003` 2026-11-10 note | kept, pointing at 005's result amendment | rewritten: the closure stays reopened, and the rule is still unwritten after a measured attempt | kept | — |
| `docs/evidence-status.md` six "no on this branch" cells (S1, S9, S11, S12, S15, S21) | kept as "no — `dev` adds the conflicted-return rule (#86)" once merged; the S21 row's Result gains this wave | reverted to "yes" after verifying the reverted SKILL.md digest equals the archived one; the S21 row's Result gains this wave as withdrawn | kept on the branch, unmerged | — |
| `scenarios.md` S21 status note and the d3/d6 assertion sharpening | status note updated with the wave; assertions stay | status note updated with the withdrawn wave; the d3/d6 sharpening stays, since it corrects the catalog's keying independently of the wording | kept | — |
| `scenarios.md` S16 dated draft note | kept, still marked unmeasured (S16 stays debt) | deleted | kept | — |

## Revision 1 — design review, 2026-11-10 (before any arm)

A cross-model design review of commit `9cdcf06` returned NO-GO for the batch as first preregistered; each finding was checked against the files before acting.

1. **S16 entangled — upheld.** The first draft's own step-2 paragraph conceded that S16's flat H1/H3 refutations carry no sensitivity check, so an arm could decline "best supported" on an unresolved rival without the rule. S16 is now unpaid debt (`reachability.md`), its catalog text is restored with a dated unmeasured note, and its prompt file is kept but unused. d4 is paid with the released budget.
2. **A.token accepted a `NON_DISCRIMINATING` downgrade on S16 — upheld.** That acceptance was copied from S16's catalog text, which itself conflicts with § Analysis's severity order and its "Do not reach for `NON_DISCRIMINATING` here either". A.token now requires the worker's token plus the conflict limitation on every paid conflict cell. S16's catalog acceptance is left as found (out of scope here) and reported.
3. **Disposition table left mixed results undecided — upheld.** Replaced by R0–R9 with an explicit order, an F-new/F-old classification for every assertion failure, a single shipping row carrying every control condition, defined outcomes for incomplete and entangled cells, and a catch-all.
4. **A.scope was undifferentiated — upheld in part.** Every remaining cell's prompt does allow only SKILL.md and the packet; the cells that legitimately read references were S16's, now out. What was missing, and is now added, is the staged-validator allowance and the separation between `run_arm.py`'s three-pattern scan and the transcript audit (`extract.py audit`, new, calibrated as in § Inputs, pinned).
5. **Stale records — upheld.** `CHANGELOG.md`, `decisions/005`, `decisions/003`, and `docs/evidence-status.md` now carry dated draft/unmeasured statements; the S21 d3 catalog rationale no longer keys on the generic limitation; `reachability.md`'s "five canaries" is corrected. § What each record becomes under each verdict is new.
6. **S20 c3 post-only — upheld,** and the same holds for d4 under this frame.
7. Optional items (a contemporaneous d6 pre replication; a positive-control packet) were not added, for the budget and scope reasons in § The reused pre condition.

`extract.py` sha256 after Revision 1: `16c00d47ca921881d11e8ede2ce6660ed9ebd4b9ddb5c851290a9f59c3ec3474` (first draft: `a407da54…`). It changed by the `audit` command only; `census` and `fields` were re-run on the 2026-11-08 archive after the change and reproduce 81 arms (13 / 6 / 62), $25.97, and 45 S21 arms.
