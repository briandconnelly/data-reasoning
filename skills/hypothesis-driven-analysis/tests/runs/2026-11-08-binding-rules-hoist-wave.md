# Binding-rules hoist (issue #66, step 1) — measured wave, 2026-11-08

Date: 2026-11-08.
Scorer: the dispatching session (Claude Opus 5.5, Claude Code), unblinded — it wrote the preregistration and the edit; no reviewer changed a score.
Preregistration: `artifacts/2026-11-08-binding-rules-hoist-prereg.md` (committed at `c733f80`, before any edit or arm; Amendment 1 at `b6a14de`, after the canaries and before any scored pre/post arm).
Harness: `../run_arm.py` (with the `--skill-md` option this branch adds); every arm's prompt, command, transcript, manifest, and written files are under `artifacts/2026-11-08-binding-rules-hoist/` as `<cell>-<arm>-<i>.*`, canaries as `canary-*`.
Model: `claude-sonnet-5-5` on every arm (requested `sonnet`); Claude Code 2.1.319.
Contamination: none on any of the 81 arms after adjudication — the scanner flagged `s21d6-pretrunc-2` and `s1-pretrunc-2`, and in both the hit is the string `SKILL.md` inside prose the arm wrote through a Bash heredoc (its own note that the file it was given was cut off), not a path it read; every read in both transcripts is inside the staged tree.
Extraction: `artifacts/2026-11-08-binding-rules-hoist/extract.py` (S21 status and best-supported fields, the S21.Q quote check, and cost); its quote check was calibrated on a known positive (the exact status-set sentence, found) and a known negative (the same sentence with its condition altered, not found) before use.
Cost: $25.97 across 81 arms (6 pre-trunc, 13 canaries, 62 scored), from the manifests' `total_cost_usd`.

**Verdict: withdrawn (preregistered row 5, regression).** The edit was reverted on this branch at `d5c0b4a`; nothing in SKILL.md ships.

## What was measured

Pre: SKILL.md at `dev` `692fd31` (sha256 `858f9f42…`).
Post: the edit at `99135bc`, made by the preregistered `hoist.py` and checked by its `check` mode (32 of 32 moved lines and pointers in place).

| Post-edit file at `99135bc` | sha256 |
| --- | --- |
| `skills/hypothesis-driven-analysis/SKILL.md` | `f07cd775383bf3ee065a8bbd89bb4bed333174e3bc4bc333edd018e6b6c026ae` |
| `skills/hypothesis-driven-analysis/references/ledger-template.md` | `eb34ddb850b63cf95e1fc91142d003ea902ef33475552e90b6e57b41c2910913` |
| `skills/causal-identification-review/SKILL.md` | `bf2956b7fa3633e2dec8bf1f641e106c177d9af4ed7cee3d00a5d017e02bc069` |
| `skills/decision-analysis/SKILL.md` | `29d44a724c0d2d02374bb99a14a4d5da82c9aa2421c3d8d81a35bf0cf9416b05` |
| post SKILL.md cut to 5,000 o200k_base tokens (`post-SKILL.prefix5000.md`, 24,353 bytes, ends in § Data) | `9bcdf0a4af6c088918533c9b1850aab22a01519ac2b77efdb258f3e3854c6e43` |

`scripts/check-shared-sections.py`, `scripts/check-description-freeze.py`, and `scripts/check-citations.py` all passed on the edit.

Retained prefix, measured on the committed post file with `prefix_tokens.py` (tiktoken 0.14.0, `o200k_base`; bytes/4 beside it):

| Point in the post file | o200k_base | bytes/4 |
| --- | --- | --- |
| end of `## Binding rules` (its last sentence) | 1,350 | 1,651 |
| end of the rendered authorization gate | 3,764 | 4,566 |
| whole file | 8,590 | 10,608 |

Both were under 5,000, so row 0 did not fire.
Neither number is Claude's tokenizer or Claude Code's re-attachment measure.

## Pre-trunc gate (row 4), before the edit

Six pre-trunc arms ran on `c733f80` before the edit existed.
Row 4 needed every pre-trunc arm to pass every scored assertion; `s21d1-pretrunc-2` reported H2 as "Open / untested" rather than `UNRESOLVED`, and `s1-pretrunc-1` put "UNRESOLVED-best supported" in a status cell, so row 4 did not fire and the edit proceeded.
Both S21 d1 pre-trunc arms noticed the file ended mid-sentence and said the status vocabulary was not in their input: "The SKILL.md I could read does not define a status label for this state, so "unresolved" is my wording, not the skill's" (`s21d1-pretrunc-1.scratch/answer.md`).

## Canaries (fixture validation, excluded from the scored tables)

All thirteen reached their decision point for the reason under test: each S21 canary derived the status citing the status set (and the best-supported bar on d6/d7); S1, S12, and S15 wrote ledgers with outcome-derived statuses and a stop outcome; S11 routed `mini` on an asserted claim; S9 routed `estimation` on stated randomization.
`canary-s1-posttrunc` concluded in prose with no per-hypothesis status, which led to Amendment 1 (BR.status fails when no status is assigned).
`canary-s21d6-post` answered best supported "Only in conditional, basis-cell language", an early sign of the d6 result below.

## Scored results — pre against post (full SKILL.md)

n=3 per arm on the paid cells, n=2 on the controls.
A cell entry is the number of arms passing the cell's catalog assertion.

| Cell | Assertion | pre | post | Post-only failures |
| --- | --- | --- | --- | --- |
| S21 d1 | `UNRESOLVED`, rationale the recorded `NON_DISCRIMINATING` | 3/3 | 3/3 | 0 |
| S21 d3 | `UNRESOLVED`, rationale the unverified return | 3/3 | **1/3** | **2** |
| S21 d5 | `REFUTED` | 3/3 | 3/3 | 0 |
| S21 d6 | `UNRESOLVED` and **not** best supported | 1/3 | 1/3 | 0 |
| S21 d7 | `UNRESOLVED`, best supported stands | 3/3 | 3/3 | 0 |
| S1 | BR.status, BR.best, BR.causal, BR.conf, BR.order, BR.stop; catalog properties | 3/3 | 3/3 | 0 |
| S12 | BR.*; full route, premise caught, causal hypothesis `UNRESOLVED`, no identified estimate | 3/3 | 3/3 | 0 |
| S15 | BR.*; `score_ledger.py` C1 | 2/3 (C1) | 3/3 | 0 |
| S11 (control) | `mini`, no hypothesis table, false at ≈392ms; no bleed | 2/2 | 2/2 | 0 |
| S9 (control) | `estimation`; no full ledger; no bleed | 2/2 | 2/2 | 0 |

**S21 d3, the cell that decided the verdict.**
`s21d3-post-1` and `s21d3-post-2` both derived "REFUTED (with the limitation that it rests on an unverified worker return…)"; `s21d3-post-3` and all three pre arms derived `UNRESOLVED`.
This is the reading issue #113 described and `decisions/005` records as rare: a `CONTRADICTED` outcome on a conflicting-record return counted as an adequate test.
Both failing arms quote the status set (G1) as governing; `s21d3-post-2` also reasons from the precedence list (G2): "UNRESOLVED would require two adequate tests of the same necessary prediction that disagree, and there is only one."
Both also cite the Analysis section's worker-return sentences and the packet's Data Validity section — but every pre arm cites those too and reaches `UNRESOLVED`, so the rule that decides the difference is the moved status set, not a rule outside the moved text.
Row 6 (divergence citing a rule outside the moved text) was considered and not applied for that reason; it is the closest alternative reading, and under it the cell would have been rerun rather than the change withdrawn.
Post failed on two more arms than pre, which is row 5 as preregistered.
Neither failing arm cites § Binding rules, its placement, its scope sentence, or a pointer; the regression is in outcome, not in a cited reason.
At n=3, 0/3 against 2/3 is not strong evidence of a causal effect of the move (a one-sided Fisher exact test on that table gives p = 0.2); the preregistration chose a rule, not a significance test, and the rule fired.

**S21 d6 fails in both conditions.**
Two of three pre arms and two of three post arms said H2 may be reported as best supported with a limitation attached, e.g. "Yes, but only as a qualified report" (`s21d6-pre-2.scratch/answer.md`).
The 2026-07-25 wave scored d6 correctly in every arm under a different prompt frame; this wave's frame is `run_arm.py`'s, shared by pre and post.
`decisions/005`'s reopening condition is an arm reaching the disposition d3 or d6 scores as a miss "under any wording"; the shipped wording's d6 misses here meet it.
That is outside this change's scope and is filed as issue #86 rather than fixed here.

**S15 pre-3** marked the causal Assist hypothesis `REFUTED` on a stratified contrast (`score_ledger.py` C1 fails); this is a pre-arm miss, not a regression.

**BR.cont (informational).** S12 named `causal-identification-review` in 1/3 pre and 2/3 post final messages; S15 named both `causal-identification-review` and `decision-analysis` in 3/3 pre and 3/3 post.

**Controls.** No control arm built a hypothesis-status table, assigned per-hypothesis statuses, or cited the new section; the only `Binding rules` mentions in any arm's written files are in two S21 d6 post-trunc answers (`canary-s21d6-posttrunc`, `s21d6-posttrunc-1`), each noting that the section was present in the truncated file.

## Approximation arms — prefix-only robustness, not Claude Code compaction

Each arm was given only the first 5,000 o200k_base tokens of SKILL.md (pre or post), with no conversation summary, no shared re-attachment budget, Claude Code's measure not used, and no way to reopen the full file.
This exercised whether the rules are followed when only the prefix is present; Claude Code's compaction was not exercised, and nothing here says how it behaves.

| Cell | Assertion | pre-trunc | post-trunc |
| --- | --- | --- | --- |
| S21 d1 | `UNRESOLVED`, rationale the `NON_DISCRIMINATING` outcome | 1/2 | 2/2 |
| S1 | BR.status (Amendment 1 applied) | 1/2 | 2/2 |
| S1 | BR.best, BR.causal, BR.order | 2/2 | 2/2 |
| S21 d6 (informational) | `UNRESOLVED`, not best supported | 2/2 | 2/2 |

Post-trunc never failed where pre-trunc passed, and improved on two assertions by one arm each — short of the preregistered *beat* (2/2 against 0/2), which is row 8a; that row requires no regression, so it never governed.
Every post-trunc S21 arm quoted the moved status set verbatim from its truncated file; no pre-trunc arm could, because none of the moved sentences is in the pre prefix.
The truncated d6 arms answered d6 correctly in all four arms, more often than the full-file arms of either condition, which is worth knowing and is not evidence for or against the hoist.

## Verdict

Row 5 fired on S21 d3: post failed the catalog assertion on two more arms than pre.
Per the preregistration, the change is **withdrawn**, with no rewording after the fact; the edit is reverted on this branch (`d5c0b4a`), and the cross-reference updates went with it.
Any revision is a new pre/post pair under an amendment to the preregistration.
What the wave did show, for whoever takes #66 up next: the move kept every other paid cell and both controls level; the prefix arithmetic works (gate at 3,764 o200k_base tokens); prefix-only arms did somewhat better with the rules in the prefix, short of the preregistered bar; and S21 d3/d6 are less settled under this harness than `decisions/005` records, in the shipped wording as well as the moved one.

## Debt and limits

- Reached but unpaid cells, as listed in the preregistration (S4, S6, S7, S8, S10, S16, S18, S19, S20, S21 d4, and the position-only cheap-route cells) remain unmeasured for this change; with the change withdrawn, they owe nothing.
- Every arm ran on one Claude model; Codex is unmeasured.
- The scorer is the agent that wrote the change, unblinded; S21 outcomes are machine-extracted from the arms' answer files, and the full-route BR assertions are rubric reads of the arms' ledgers and final messages.
- The six pre-trunc arms ran before Amendment 1 and are scored under it; the S1 pre-trunc scratch files were first read after the amendment was written.
