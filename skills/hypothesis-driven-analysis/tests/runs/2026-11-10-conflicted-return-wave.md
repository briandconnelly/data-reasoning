# Conflicted return, status and "best supported" (issue #86) — measured wave, 2026-11-10

Date: 2026-11-10.
Scorer: an Opus subagent of the dispatching session (Claude Opus 5.5, Claude Code), unblinded — the same agent wrote the wording, the preregistration, and its Revision 1; no reviewer changed a score.
Preregistration: `artifacts/2026-11-09-conflicted-return/prereg.md` as of Revision 1 (commit `1f3ea54`), with `reachability.md` beside it; committed before any arm, after a cross-model design review of the first draft (`9cdcf06`) returned NO-GO and was answered by that revision.
The rules were not edited after any arm ran.
Harness: `../run_arm.py`, unchanged since `c733f80`; every arm's prompt, command, transcript, manifest, and written files are under `artifacts/2026-11-09-conflicted-return/` as `<cell>-post-<i>.*`, canaries as `canary-*`.
Model: `claude-sonnet-5-5` on all 28 arms (requested `sonnet`); Claude Code 2.1.322 on all 28. The reused pre arms ran Claude Code 2.1.319; that difference is not pinned by any digest and is disclosed here.
Extraction: `artifacts/2026-11-09-conflicted-return/extract.py` (`census`, `digests`, `audit`, `fields`), calibrated before use as the preregistration records.
Cost: $9.27 across 28 arms ($2.20 for the 7 canaries, $7.07 for the 21 scored arms), from the manifests' `total_cost_usd`.

**Verdict: SHIP (preregistered row R8).** No reserve arm was spent.

## What was measured

Post: SKILL.md at `60f19e6` (sha256 `0fb674389aeaeba8099d84da580769703efece73b9f4442de2d659171614a27d`), staged with `--skill-ref 60f19e6`; all 28 manifests carry that digest and the same 14 skill-tree files.
Pre: not run. The 15 archived arms `s21d{1,3,5,6,7}-pre-*` of `2026-11-08-binding-rules-hoist-wave.md` are reused as historical controls, selected after the failure was observed, with prompts, frame, tools, model, skill tree and packets preserved (`artifacts/2026-11-09-conflicted-return/reachability.md`, Step 0).
Every arm's fixture digest equals the committed packet (28 of 28 files checked).

`extract.py census` on the artifact directory: `manifests=28 {'canary': 7, 'scored': 21}`, `cost=$9.27`, no contamination flagged by `run_arm.py`'s scan, no nonzero exit.
`extract.py audit`: 0 hits on all 28 arms; every arm made three tool calls (read SKILL.md, read the packet, write `answer.md`).

## Canaries (fixture validation, excluded from the scored tables)

All seven reached their decision point for the reason under test, so row R3 did not fire.
d6 and d3 decided on the conflicting execution records and quoted the new § Conclusion sentence; d5 and d7 on the cleared-but-unrepeatable carve-out, which both quoted; d4 on the adequately tested deviation; d1 on the recorded `NON_DISCRIMINATING`; S20 c3 reconciled T2 as `CONTRADICTED` with the conflict limitation.

| Canary | H2 status | Best supported | T2 token | Ground |
| --- | --- | --- | --- | --- |
| `canary-s21d6-post` | `UNRESOLVED` | No | `CONSISTENT` kept | conflict, new sentence quoted |
| `canary-s21d3-post` | `UNRESOLVED` | — | `CONTRADICTED` kept | conflict, new sentence quoted |
| `canary-s21d5-post` | `REFUTED` | — | kept | cleared return, carve-out quoted |
| `canary-s21d7-post` | `UNRESOLVED` | Yes | kept | cleared return, carve-out quoted |
| `canary-s21d4-post` | `REFUTED` | — | kept | adequately tested deviation |
| `canary-s21d1-post` | `UNRESOLVED` | — | `NON_DISCRIMINATING` kept | recorded outcome |
| `canary-s20c3-post` | `UNRESOLVED` (unscored) | — | `CONTRADICTED` + conflict limitation | conflict disposition |

## Scored results

A cell entry is the number of arms passing every applicable assertion (A.status, A.token, A.best, A.rationale, A.scope).
Pre is the reused 2026-11-08 count under the same rubric, fixed in the preregistration before any post arm.

| Cell | Role | pre (reused) | post | A.status | A.token | A.best | A.rationale | A.scope |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| S21 d6 | test | 1/3 | **3/3** | 3/3 `UNRESOLVED` | 3/3 | 3/3 not best supported | 3/3 conflict named | 3/3 |
| S21 d3 | regression check | 3/3 | 3/3 | 3/3 `UNRESOLVED` | 3/3 | — | 3/3 conflict named | 3/3 |
| S21 d5 | control | 3/3 | 3/3 | 3/3 `REFUTED` | 3/3 | — | 3/3 cleared return | 3/3 |
| S21 d7 | control | 3/3 | 3/3 | 3/3 `UNRESOLVED` | 3/3 | 3/3 best supported stands | 3/3 cleared return | 3/3 |
| S21 d4 | control, post-only | — | 3/3 | 3/3 `REFUTED` | 3/3 | — | 3/3 adequately tested | 3/3 |
| S21 d1 | floor | 3/3 | 3/3 | 3/3 `UNRESOLVED` | 3/3 | — | 3/3 recorded `NON_DISCRIMINATING` | 3/3 |
| S20 c3 | compliance, post-only | — | 3/3 | (unscored; 3/3 `UNRESOLVED`) | 3/3 `CONTRADICTED` + conflict limitation | — | 3/3 conflict disposition | 3/3 |

No arm failed any assertion, so there is no F-new or F-old failure to class and no quote of a failing arm to give.

**S21 d6.**
All three arms answered "No" to best supported, quoted the new sentence in `GOVERNING SKILL TEXT`, and named the command/output day conflict.
Each also took up the elimination argument the two 2026-11-08 misses had followed and rejected it: "That holds even though H1 and H3 are REFUTED and H2 is the only hypothesis left on the table." (`s21d6-post-2`); "H1 and H3 being REFUTED does not fill that gap." (`s21d6-post-1`).

**Controls.**
d5 and d7 drew the carve-out explicitly: "It is not the conflicting-execution-records kind, which would bar refutation." (`s21d5-post-2`); "Its inability to be re-run is therefore the "merely could not be re-run" case, not the conflicting-execution-records case." (`s21d7-post-2`).
S20 c3 arms quoted the new sentence too and still kept the worker's token: "I did not downgrade it to NON_DISCRIMINATING, because the skill forbids that for this fault." (`s20c3-post-1`).
On d3 the token held the same way: "I did not change it to NON_DISCRIMINATING." (`s21d3-post-3`).

## Disposition, applied in the preregistered order

R0 (owner declined) and R1 (unnecessary on the archive) did not fire; R1 was evaluated before the preregistration.
R2: no void arm. R3: no entangled canary. R4: no F-new failure and no d3 `REFUTED`. R7: every cell complete. R5, R5′: no control failure. R6: d6 3/3, so to R8. R8: d6 reached it via R6, every cell complete, every control cell holds — **SHIP**.

## What this result may be claimed to show

On S21 d6, under `run_arm.py`'s frame, on Sonnet, n=3: 1/3 on the shipped wording (historical, reused, selected after the failure) to 3/3 on the drafted wording, with every passing arm citing the new sentence.
That is a one-sided Fisher exact p = 0.2 against the reused pre, so it is a descriptive result, not a significant one; regression to the mean from a pre selected for failing would also predict some improvement.
No regression was detected at n=3 on d3, d5, d7, d1; a control regression with a per-arm rate under about one in five is below what this wave resolves.
d3 is not a lift: its pre was already 3/3.
d4 and S20 c3 have no pre under this frame, so they show compliance with the edited text, not lift.

## Debt and limits

- Unpaid cells that reach the edited sentences, per `reachability.md`: S16 (entangled by its unchecked null refutations; a versioned packet would make it measurable), S20 c1, c2, c4, S19, S10, S1, S4, S6, S7, S8, S12, S15, S18.
- E2's "until evidence from outside that return resolves the conflict" clause is unmeasured: no packet resolves a conflict from outside.
- One model, one fixture family, one frame; Codex is unmeasured.
- The scorer wrote the wording and the preregistration and scored unblinded; S21 labels are machine-extracted from `answer.md`, rationale and token are rubric reads, and every quote above was grepped against the archived `answer.md`.
- Claude Code 2.1.322 for post against 2.1.319 for the reused pre.
