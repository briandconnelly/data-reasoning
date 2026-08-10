# Measurement wave 1 evidence — causal-identification-review, 2026-08-09

Scope: the 18 scoreable arms of Phase 4's first scored wave (trigger cells CS1/CS2/CS6a; pairs CS3/CS5/CS6b; amended-cell re-runs CS4/CS7; HDA seam cells S9/S12/S1/S15).
Transcripts live in `.superpowers/sdd/2026-08-08-causal-identification-review-skill/task-4.3/` (`sc-*` first-wave scored arms, `sc2-*` amended-cell re-runs); `canary-*` and the superseded `sc-cs4-*`/`sc-cs7-*` arms are archived context, excluded from scoring per the catalog's amendment notes.
Extraction instrument: `skills/hypothesis-driven-analysis/tests/extract_evidence.py` with `--normalize-root <worktree>` (subcommands `identity`, `manifest`, `events`, `text`); with-skill record files were read directly from the per-arm staging dirs.
Every quote in the run records and this artifact was grepped against the archived transcript extraction or the archived record file it is attributed to, per `PROTOCOL.md` step 6.

**Durability note (2026-08-09, post-wave review).**
`.superpowers/` is gitignored, so the transcripts and per-arm record files this artifact's greps ran against do not ship with the repository.
The sha256 digests below are the durable integrity anchors: a checkout without the archived workspace cannot re-run the quote verification, only confirm that a later-produced copy of a transcript matches its recorded digest.
The per-arm identification-review records exist inside the transcripts' Write tool calls and are recoverable from them where the archive is present.

## Transcript digests and identity totals

sha256 recomputed with `shasum -a 256` equivalent (`hashlib.sha256` over raw bytes); the `identity` subcommand independently reports the same digest for every file (verified per arm — a mismatch would have been a snapshot-integrity failure).

| Arm | sha256 | tool_use (identity) | Dispatch-facts claim |
| --- | --- | --- | --- |
| sc-cs1 | 631b969d64ca0ca61b56652860226174bdbe9f1805cafefda406254ff717122c | 7 (Bash 5, Read 1, Skill 1) | 7 ✓ |
| sc-cs2 | e537ada89422c86aa6acc798384ac8bd4c9a9000d69511b2a3cda50e1e1a3bbd | 5 (Bash 2, Read 2, Write 1) | 5 ✓ |
| sc-cs6a | ec352ed61c840cc17b3b1c7b31cddfc427a00beca7ce50d7833fc1959c9b4dc6 | 0 | 0 ✓ |
| sc-cs3-base | 3bd5bfe8afcca57f25f6ceaf00d688e49b9109454f35547b7eea5a855e33e542 | 3 (Bash 3) | 3 ✓ |
| sc-cs3-ws | 16a454f5d12c2a149f6e685ebc381a16ab4607ff8b996bc6feb23060ccb66c95 | 13 (Bash 6, Read 6, Write 1) | 13 ✓ |
| sc-cs5-base | 434326baa401e706b597977e8f78900169e9085bd6620e666f3942b4f96364ce | 5 (Bash 4, Read 1) | 5 ✓ |
| sc-cs5-ws | 315c3e4c8d79ca6357ff4d5602d979d52273976ff14f0ade6d7dd5066e720151 | 10 (Bash 5, Read 4, Write 1) | 10 ✓ |
| sc-cs6b-base | 5bb2ffeae96718edf950c8359b63f6bcef821dd00ef9633483546cac345907c1 | 15 (Bash 10, Read 4, Write 1) | 15 ✓ |
| sc-cs6b-ws | ace36477cb00c37608ffc228bce45ea981c74602508b02fbbdd701536e9fa2ad | 13 (Bash 6, Read 6, Write 1) | 13 ✓ |
| sc2-cs4-base | d7f6f74c13afd76fab08a0815cc322b24432004eafe5c704337ab47828e8dd9e | 1 (Read 1) | 1 ✓ |
| sc2-cs4-ws | 36df5de006baf3994cc00ac6fd64fbd11bdc3173763d89c35389cce9f732cc09 | 6 (Bash 2, Read 3, Write 1) | 6 ✓ |
| sc2-cs7-base | 9c2e0a61e301275b2079b9a40a8eaa418bd4e226e1126f95b57b59fc59eb9640 | 9 (Bash 6, Read 1, Write 2) | 9 ✓ |
| sc2-cs7-ws | a87e93d6e5d7d71102d572963ee50b53eef336e533e95b040aa7634aba126af3 | 17 (Bash 9, Read 3, Write 5) | 17 ✓ |
| sc2-cs7s2 | 553187a04ba9c91f6a72a612d344cc26574d9d06a7ab958e37474eb5d8209dbd | 11 (Bash 5, Read 4, Write 2) | 12 ✗ (identity's 11 is authoritative; controller figure not reproduced) |
| sc-s9 | ad3cbd912e37d32a8c8b11c93d317251994fadb2a1665f08b8bea1566279605c | 9 (Bash 5, Read 2, Write 2) | 9 ✓ |
| sc-s12 | 04d1339d872d7190dc7bc0c7bdd66c09477637907694af9f835cb4963b5735c0 | 23 (Bash 17, Edit 1, Read 2, Write 3) | 23 ✓ |
| sc-s1 | 93f934d0043dd038dea50cb402760e0804884892dc378b484e00255db365c907 | 20 (Bash 11, Read 3, Write 6) | 20 ✓ |
| sc-s15 | afdff45727fe6eaab16aa179b89584a29c9bb07ee58cc796a7d6bac27e6bb355 | 37 (Artifact 1, Bash 15, Edit 3, Read 7, Skill 2, Write 9) | n/a (tokens and count "not captured") |

## Machine scans over all 18 scoreable manifests

Each pattern was validated against a planted positive in the same script run before its zero was trusted; the script printed "planted positives: all fired" (scan script: `scan_manifests.py`, session scratchpad).

1. Git commands: regex `(?<![\w./-])git\b` over Bash rows; planted positive `cd /tmp && git status && ls` fired; **0 hits across 18 manifests** — no arm ran a git command.
2. Write-tool rows outside arm dirs: `Write`/`Edit`/`NotebookEdit` rows whose target does not start with `<SCRATCH>/phase4-arms/<own-arm>/`; planted positive (a Write targeting another arm's dir) fired; **0 hits** — every write-tool row landed in the arm's own dir.
3. Repo references: regex `<REPO_ROOT>|/Users/bdc/projects/data-reasoning` over every row's target; planted positives (literal repo path, and a `<REPO_ROOT>`-normalized path) both fired; **0 hits** — no arm read or referenced the repository or any `tests/` directory, satisfying the contamination rule.

Scan-scope caveat: scan 2 covers write-tool rows; Bash-mediated writes were covered by reading every Bash target during manifest review (all `mkdir`/redirect targets observed are inside own arm dirs), and scan 3 would have caught any repo-directed one.
The one out-of-sandbox side effect in the wave is sc-s15's `Artifact` tool call (manifest ordinal 37, publishing its own `memo.html`) — a tool-surface effect outside all three scan classes, recorded as a fidelity finding in the S15 run record.

## Machine gate: `check_review.py` per with-skill identification-review record

Command form: `uv run python skills/causal-identification-review/tests/check_review.py <record>`.

| Record | Exit | Findings summary |
| --- | --- | --- |
| sc-cs2/price-increase-churn-identification-review.md | 1 | Genuine closed-set violation: synthetic-control disposition is the conditional compound "not-constructible if fewer than a handful of untreated comparable markets/products exist; otherwise unresolved pending the fit and placebo-in-space probes." (one token required), which also fails Handoff reuse ("disposition(s) ['not-constructible'] appear nowhere above"). |
| sc-cs3-ws/identification-review-cs3-rollout.md | 1 | One parse finding: "Handoff block: Facts is missing or empty" — Facts written as an indented sub-list, checker requires an inline slot value; content present. |
| sc-cs5-ws/identification-review-cs5-bounds.md | 1 | Three parse findings (Assumption ledger and Facts as sub-lists; "Dispositions: none — <rationale>" not accepted as bare `none`) plus advisory "possible point estimate '+9.58 percentage points' outside the Bound endpoints slot" — that number is the pre-disclaimed naive difference ("**not an effect estimate**"). |
| sc-cs6b-ws/identification-review-cs3-rollout.md | 0 | "PASS: schema-scope contract satisfied, no advisory findings" — the wave's one clean gate. |
| sc2-cs4-ws/identification-review-merchant-verification.md | 1 | Eleven shape findings: RD and DiD blocks omit the `- Design:` bullet and render assumptions/probes as inline prose on short-circuited designs; named-only prospective block has no probe/threat tables; no closed-set or reuse violation on manual read. |
| sc2-cs7-ws/identification-review-cs7-seam.md | 1 | Nine findings, all formatting-class: backtick-wrapped Route/Disposition tokens (`` `construct` ``, `` `identified-if` ``, `` `not-constructible` ``) fail the string match; named-only prospective block; Facts/Dispositions as sub-lists. |
| sc-s15/identification-review.md | 1 | Same formatting classes (backticked tokens, prose-form blocks, Handoff-reuse parse); run in-arm as the S15 investigation's A1 side record. |

Pattern finding: 5 of 7 gate failures are checker-format/record-format mismatches (backticked tokens, nested-list slot values, `none` with a rationale, named-only design blocks) against semantically compliant content; the two content-bearing findings are CS2's compound disposition (a real record-discipline deviation, outside CS2's scored scope) and the CS5 advisory (pre-disclaimed).
Disposition of the pattern: recorded for the verdict resolution; the checker and template are unmodified by this task.

**Instrument-revision note (2026-08-09, post-review).**
The exits and findings in the table above are the wave-time checker's output, recorded before the formatting-tolerance fixes the verdict resolution's defect scoping licensed as checker-side (backtick-wrapped tokens, sub-list and paragraph slot values, `none` with a rationale, named-only design blocks, dash-rationale and sublist-indentation tolerance — each pinned in `test_check_review.py`).
The table is deliberately not rewritten: it is the record of what the gate said when the wave was scored, and a reader running the shipped checker today should expect different output.
Re-run 2026-08-09 against records recovered from the archived transcripts' Write calls, the shipped checker passes sc-cs3-ws, sc2-cs7-ws, and sc-s15 clean and passes sc-cs5-ws with only the pre-disclaimed advisory; sc2-cs4-ws retains six genuine slot omissions (absent `- Design:` bullets and identifying assumptions on its short-circuited blocks), and sc-cs2 still fails on its compound disposition and the Handoff-reuse consequence.
The parse-artifact findings dissolved under the tolerant checker; the content-bearing findings stand unchanged.

## Verbatim skill-selection sentences (trigger arms)

- sc-cs1 (text block 1, before any tool result; ordinal 1 is `Skill {"skill": "hypothesis-driven-analysis"}`): "Using hypothesis-driven-analysis: this is a diagnostic \"why did metric X change\" question with a named effect and plausible competing explanations, which is exactly what that skill's PPDAC process covers — not causal-identification-review (which reviews measurement designs, not adjudicates causes) or exploratory-data-analysis (no open-ended profiling ask here)."
- sc-cs2 (text block 1, before any tool result): "This is a \"how could we ever measure this causal effect without randomization\" question — exactly what causal-identification-review is for (candidate designs, their identifying assumptions, and probes to test them). Loading that skill now."
- sc-cs6a (text block 1, the arm's entire preamble, zero tool uses): "No skill fits here — this is a general conceptual teaching request, not a specific causal question to design for, an investigation to adjudicate, or a dataset to explore. I'll just teach it directly."

## CS5 bounds ground-truth match

`tests/fixtures/cs5-bounds-ground-truth.md`: "lower: -0.019370", "upper: 0.273608".
sc-cs5-ws record: "Computed endpoints: **-0.0194, 0.2736**" with the arithmetic lines "lower endpoint = 0.49153 − 0.51090 = **-0.01937**" and "upper endpoint = 0.78450 − 0.51090 = **+0.27361**" — exact to the record's reported precision.
sc-cs5-base (inline answer): "sharp bounds on the effect = [-1.9 pp, +27.4 pp]" — the same pair at two decimal places of percentage points.
Both arms therefore reproduce the generator-documented Lee bounds; the with-skill delta on this cell is record/route ceremony, not numeric correctness (dispatch-facts observation confirmed).

## CS7 stage-2 estimand reuse

Stage 2 estimand line (sc2-cs7s2/estimation-ledger.md line 2, quoted): "Estimand: sharp-RDD local average effect of instant-checkout eligibility on `default_90d`, for accounts at the credit_score = 680 margin — the jump in the local-linear default-rate fit at the cutoff. Carried verbatim from the identification review's Handoff block (`identification-review-cs7-seam-sc2.md`) …".
Stage 1 estimand line (sc2-cs7-ws/identification-review-cs7-seam.md line 6, quoted): "- Estimand: the local average effect of instant-checkout eligibility on 90-day default rate for accounts at the credit-score margin of 680 (a sharp-RDD local estimand) — not an average effect over the full account population, which the design below cannot reach."
Grep: the distinctive phrase `local average effect of instant-checkout eligibility on` resolves in both files (stage 1 line 6, stage 2 line 2); the full strings are not byte-identical (outcome named `default_90d` vs "90-day default rate", population phrase reordered), so stage 2's "Carried verbatim" claim is a matching-terms reuse rather than a byte copy — scored PASS-borderline in the stage-2 run record with this exact evidence.
Corroborating consumption evidence: stage 2 reuses stage 1's bandwidth set (20/30/50/80), its "z ~ -2.1" moderate-support caveat, its three `identified-if` conditions, and its `not-constructible` full-sample finding.

## Preregistration-ordering evidence (seam cells)

- sc-s12: `check_prereg.py` exit 1, `PREREG_WRITE: ordinal 16` of 23; all 12 pre-write touches are orientation (file listing, `head`/`wc`, distinct-value censuses, date ranges, per-day and day×page counts — none crosses `checkout_reached` with an exposure); content check confirmed from the ordinal-16 event (hypothesis table and predictions present at write time; outcomes filled by the ordinal-23 Edit).
- sc-s1: `check_prereg.py` exit 1, `PREREG_WRITE: ordinal 20` of 20; pre-write touches classified: ordinals 3–6 orientation (listing, heads/tails, counts, date ranges); ordinal 7 analysis (week-over-week conversion contrast); ordinal 8 analysis (attempted conversion-by-page/device, errored — intent counts); ordinals 11/13/15/17/19 analysis (`explore1–5.py`, archived in the arm dir, compute per-page conversion and mix reweighting); ordinal 9 orientation (mkdir); the ordering assertion fails. |
- sc-s15: `check_prereg.py` exit 1, `PREREG_WRITE: ordinal 23` of 37; pre-write touches classified: ordinals 3–4, 7–11, 13–14, 21 orientation (schema, counts, coverage, join integrity — `orient.py` is missing-record/censoring accounting); ordinals 16 (`analysis.py`: "Closed-incident (available-case) outcome summary by workflow"), 18 (`daily.py`: daily TTC by workflow), 20 (`deep.py`: stratified bootstrap contrasts) analysis; the ordering assertion fails.
- sc-s15 `score_ledger.py --final investigation-ledger.md --c3-unknown-source S2`: exit 1; no C1 failure (H1 causal `UNRESOLVED`, zero `REFUTED` rows); "C2 (status laundering) not checked" (no archived Plan-time ledger); C3b FAIL: "S2 has no `S2: <reading>` declaration in the completeness bullet; the documented form is `S2: UNKNOWN — <why no evidence discriminates>`".
- sc-s15 `compare_prereg.py`: not runnable — the run archived no Plan-time ledger and made no pre-analysis ledger write to recover one from.

## Token premiums (harness-reported, single arm per cell, n=1 — noise floor unknown)

| Cell | Baseline | With-skill | Premium |
| --- | --- | --- | --- |
| CS3 | 34,924 | 50,162 | +43.6% |
| CS5 | 38,609 | 53,580 | +38.8% |
| CS6b | 53,641 | 51,895 | -3.3% |
| CS4 (sc2) | 31,511 | 56,364 | +78.9% |
| CS7 stage 1 (sc2) | 41,272 | 68,732 | +66.5% |
| CS7 stage 2 (sc2) | — | 74,399 | no baseline by design |

Trigger/seam arms (no pair): sc-cs1 69,446; sc-cs2 47,165; sc-cs6a 26,935; sc-s9 58,167; sc-s12 88,546; sc-s1 91,772; sc-s15 not captured.
All figures are the controller's harness numbers; tool-use counts were re-derived from identities (one discrepancy, sc2-cs7s2, noted in the digest table).

## Measured-wording digests

Frozen reference: `.superpowers/sdd/2026-08-08-causal-identification-review-skill/frozen-digests-c5f4755.txt`.

| File | Frozen (c5f4755) | Re-hashed now | Match |
| --- | --- | --- | --- |
| skills/causal-identification-review/SKILL.md | 8a35546673cb2aefb243a2ce3e04e8e7e22f7a9e457991ad42988666783e06d2 | same | ✓ byte-identical |
| skills/hypothesis-driven-analysis/SKILL.md | 273c396294d0812ddbc7c44fb07484cb364a1496e259a0dc20be6fdd3c169bcd | same | ✓ byte-identical |
| skills/causal-identification-review/tests/scenarios.md | b468d800d0d29222b573fce26957052f67a89afca68987473742e5c50413a0d6 | bd50e0cfdff4c5486e4efd1ee272a2bf53869d413dd22d2e628d64fd1fad922a | ✗ expected — the 2026-08-09 CS4/CS7 amendments (c28b8af) edited the catalog before the `sc2-*` arms ran |

`git show --stat c28b8af` lists only `cs7-seam/data_notes.md`, `generate.py`, `validate_cs4.py`, `validate_cs7.py`, and `tests/scenarios.md` — no SKILL.md, reference, or template file — so the measured skill prose for every scored arm is exactly the c5f4755 wording, confirmed by re-hash, and the `sc2-*` arms additionally saw the amended `data_notes.md` fixture fact as the amendment intends.

## Scoping judgements recorded (verdict-table row 2 requirement)

1. `check_review.py` formatting-class findings (5 records): the fix is checker-side (accept backticked tokens, sub-list slot values, `none — rationale`, and a named-only design shape) or template-side; a checker/test change is not agent-read prose and owes no arm under `PROTOCOL.md` § "What owes a rerun"; a template change would owe arms and is deliberately not made here.
2. CS2 compound-disposition finding: no wording change adopted (the gate exists to catch exactly this and did); owes nothing now; watch item for the next trigger-depth wave.
3. CS4 fixture-wording ambiguity (below-cutoff outcome window): no assertion keys on RD's disposition, so nothing failed; a clarifying fixture edit is agent-read fixture prose and would owe fresh CS4 arms per the catalog's own amendment precedent — deferred and recorded, not assumed.
4. S1/S15 failed assertions: decision points (preregistration ordering, plan discipline, completeness-establishment evidence, secondary-field coverage) all traverse HDA sentences the seam amendment did not edit; the S15 failure profile is identical to the documented pre-amendment before-state (HDA Tenth wave / Re-adjudication / Post-strengthening: prereg reconstructions 4/6, handoffs 0/6, assertion-6 0/6 under the rewritten letter), so no regression attributable to the amendment is measurable; S1's ordering assertion has no pre-amendment measurement to regress from (first live S1 outing of the instrument) and is filed to HDA's suite as a standing-cell finding.
