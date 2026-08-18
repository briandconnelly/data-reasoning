# Scoping and preregistration — restructuring the worker-return rules into labeled lists (2026-08-18)

Branch: `hda-analysis-restructure`.
Change under scope: `SKILL.md` § Analysis, the passage from `Spot-verify the evidence…` through `Validate assumptions shared across workers…`, reorganized into a `#### Verifying worker returns` subsection with bold labels and bullet lists.
Every sentence keeps its bytes and its order; the only new text is the heading and the labels.
The ordering this document obeys, the rerun obligation it applies, and the rules the passage states all live elsewhere and are not restated here — see `PROTOCOL.md` (order, and what owes a rerun) and `SKILL.md` § Analysis (the rules themselves).

This document is written before the wording edit, per `PROTOCOL.md`'s order.
It is a scoping and preregistration record, not a measurement: no arm was run for it.

Notation: **P1–P24** are the passage's sentences, **S7/S16/S19/S20/S21** are scenarios, and c1–c4 / d1–d7 are those scenarios' cells.

## Sentence identifiers

P1–P24 number the passage's sentences in current file order.
The fragments below are handles, not the rules; read the rule in `SKILL.md`.

| ID | Handle | New group |
| --- | --- | --- |
| P1 | Spot-verify the evidence… | lead sentence |
| P2 | Verifying does not mean paying twice… | Free check first |
| P3 | Start with the free check… | Free check first |
| P4 | Does the command implement the method… | Free check first |
| P5 | That costs nothing and catches… | Free check first |
| P6 | Re-run the collection when it is cheap… | Free check first |
| P7 | When neither is available… | Free check first |
| P8 | That is a limitation to state… | Free check first |
| P9 | …classify each fault… | When the free check faults a return |
| P10 | …a fixed severity order… | When the free check faults a return |
| P11 | Rank the return's execution record… | When the free check faults a return |
| P12 | An error in a derived value… | Derived-value error |
| P13 | Record the outcome the corrected figure implies… | Derived-value error |
| P14 | A deviation is established when… | Established deviation |
| P15 | An established deviation makes the reconciled outcome… | Established deviation |
| P16 | A narrative field contradicting… | Established deviation |
| P17 | That downgrade records the inadequacy… | Established deviation |
| P18 | An established deviation that leaves the prediction adequately tested… | Established deviation |
| P19 | When the execution records themselves conflict… | Conflicting execution records |
| P20 | Nor is anything verified… | Conflicting execution records |
| P21 | Record the fault as a limitation… | Conflicting execution records |
| P22 | "Unverified" is that limitation, not a fourth outcome… | Conflicting execution records |
| P23 | Do not reach for `NON_DISCRIMINATING` here either… | Conflicting execution records |
| P24 | Validate assumptions shared across workers… | Shared assumptions |

## Method, and what the instrument can and cannot show

Reachability was re-derived from the run archive under `tests/runs/`, not taken from the scenario catalog.
The extractor walks the two disposition evidence artifacts heading by heading at every heading depth, collects each arm's archived answer, and reports which arms' `GOVERNING SKILL TEXT` contains each sentence.
Depth-agnostic walking is deliberate: `PROTOCOL.md`'s third documented loss was an extraction that matched one heading level and silently dropped a third of the arms.

Quotation is a **lower bound** on reachability, not a measure of it: an arm reaches a sentence whenever its decision point traverses it, and arms quote only the text they cite as governing.
Where quotation is silent, the reachability call below is made from the fixture description and the run notes, and the evidence for it is named.

Two independent checks that the instrument is not returning a clean result because it is broken:

- It reproduces three totals the archive states independently (S20 rounds 1–2 = 60 arms; c2 = 12 arms; c3 = 15 arms, 14 `UNRESOLVED` and one `REFUTED`).
- Its per-sentence scan returns hits for sentences the archive quotes and zero for P9 and P10 — and `scenarios.md` independently records the co-occurring-fault case as unmeasured, so that zero is corroborated rather than trusted.

## Reconciliation against totals the archive already states

| Claim in the archive | This extraction | Verdict |
| --- | --- | --- |
| S20: "60 arms run and scored 2026-07-25 across two rounds" | rounds 1–2 = 30 + 30 = 60 arm sections | agrees |
| S20 whole archive (rounds 1–5) | 75 arm sections = 30 + 30 + 6 + 6 + 3 | consistent; rounds 3–5 add 15 validation arms |
| S20 c2 = 12 arms, all `REFUTED` | 12 arms, 12 `REFUTED` | agrees |
| S20 c3 = 15 arms, 14 `UNRESOLVED`, the exception `round1-preC3-2` | 15 arms, 14 `UNRESOLVED`, `round1-preC3-2` `REFUTED` | agrees |
| S20 c1 = 27 arms, all `UNRESOLVED` | **33 arms**, all 33 `UNRESOLVED` | **disagrees on the count** |
| S20 c4: status tracks the recorded outcome, in every arm | 15 arms, 7 `UNRESOLVED` / 8 `REFUTED` | consistent |
| S21: 18 arms run and scored | 24 arm sections = 6 canary (`pre`) + 18 `scored-pre` | agrees; canaries are excluded from the scored set |

**Finding (archive discrepancy, recorded here, not fixed here).**
The c1 count of 27 omits six round-1 arms — `round1-preA1`, `-preA2`, `-preA3`, `-preB1`, `-preB2`, `-preB3` — which ran against the round-1 `c1-established.md` packet under the skill-only (A) and both-files (B) prompts, before the arm-naming convention gained a cell prefix.
Their archived answers identify the packet unambiguously: each faults a coherent 2026-06-09/2026-06-11 execution record against a brief and a Method line naming 2026-06-10, which is the c1 packet's planted fault.
The correct whole-archive c1 count is 33.
The substantive claim is unaffected — all 33 c1 arms derive `UNRESOLVED` — so the count is low by six and the finding it supports still holds.
This is the same class of miss the archive already corrected once for c3 (twelve counted where fifteen ran), reached here through a name pattern rather than a heading pattern.
The text carrying it is `scenarios.md`, which this branch does not edit; it is left as a recorded discrepancy for a separate change.

## Amendments

- 2026-08-18, post-edit (commit b5143b8): corrected the Cells-per-group table's Free-check row arm count from 12 to 6 (S21 d5 + d7 at 3 arms each); no reachability, expectation, or owed-arms claim changed.
  That commit's message named only the digest pin; this note discloses the arithmetic correction it also carried.

**Second finding: no archived arm read the current file.**
Every S21 arm and every S20 round-3 to round-5 arm read `SKILL.md` at digest `da9cefbc…`; the file this scoping was written against, before the restructure, is `c88a49c9…`, and the restructured file the owed arms will read is `9191a552…` (added after the edit, which is the only time it can be known).
S16's arms (2026-07-17) and S19's arms (2026-07-21) predate the 2026-07-25 disposition edit entirely.
The archive is therefore evidence about which cells reach which sentences, and about what those cells produced under earlier text — it is not a current-wording baseline for any cell.

## Sentence-by-sentence reachability

"Quoted by" lists cells whose archived arms quote the sentence as governing text.
"Reached by" is the scoping call, and it is what the owed-arms list consumes.

| ID | Quoted by (archived arms) | Reached by | Basis |
| --- | --- | --- | --- |
| P1 | S20 c1, c2, c3, c4 | S20 all cells; S16; S19 | quotation; S16 and S19 are free-investigation resumes whose first act on the packet is this duty |
| P2 | S20 c2 | S20 all cells; S16; S19 | quotation; an S19 arm restates the paying-twice comparison in its own reasoning |
| P3 | S20 c1, c2, c3, c4 | S20 all cells; S16; S19 | quotation |
| P4 | S20 c1, c2, c3, c4 | S20 all cells; S16; S19 | quotation |
| P5 | S20 c1, c2, c4 | S20 all cells; S16; S19 | quotation |
| P6 | S20 c2 | S20 all cells; S16; S19 | quotation; each of these cells has a metered source with the budget spent, so the sentence is traversed and its condition fails |
| P7 | S20 c4; S21 d5, d7 | S20 all cells; S21 d5, d7; S16; S19 | quotation; S19 arms record outcomes resting on unverified worker attestations |
| P8 | S20 c4; S21 d5, d7 | as P7 | quotation |
| P9 | none | no archived cell | no packet carries faults of two classes at once |
| P10 | none | no archived cell | `scenarios.md` records the co-occurring-fault case as unmeasured, and no fixture builds it |
| P11 | S20 c1 | S20 c1, c3, c4 | quotation for c1; c3 and c4 turn on whether command and output agree, which is this ranking applied |
| P12 | S20 c2 | S20 c2; S16 (W1) | quotation; S16's W1 plant is the derived-value case |
| P13 | S20 c2 | S20 c2; S16 (W1) | quotation |
| P14 | S20 c1 | S20 c1, c4; S16 (alternate branch) | quotation; c4 is the disclosed-deviation packet, and S16 accepts an established-deviation reading of W2 |
| P15 | S20 c1 | S20 c1; S16 (alternate branch) | quotation |
| P16 | S20 c1 | S20 c1 | quotation |
| P17 | S20 c1 | S20 c1 | quotation |
| P18 | S20 c4; S21 d4 | S20 c4; S21 d4 | quotation |
| P19 | S20 c3; S21 d3, d6 | S20 c3; S21 d3, d6; S16 (W2) | quotation; S16's W2 plant is the conflicting-record case |
| P20 | S20 c3 | S20 c3; S21 d3, d6; S16 (W2) | quotation |
| P21 | S20 c3; S21 d3, d6 | S20 c3; S21 d3, d6; S16 (W2) | quotation |
| P22 | S20 c3, c4; S21 d3, d5, d6, d7 | same | quotation; this sentence exists because a c3 arm invented an out-of-set label |
| P23 | S20 c3, c4; S21 d5 | S20 c3, c4; S21 d5 | quotation |
| P24 | none | no archived cell | see the P24 resolution below |

### Cells per group

| Group | Cells that reach it | Archived arms in those cells |
| --- | --- | --- |
| lead sentence (P1) | S20 c1–c4; S16; S19 | 75 + 3 + 3 |
| Free check first (P2–P8) | S20 c1–c4; S21 d5, d7; S16; S19 | 75 + 6 + 3 + 3 |
| When the free check faults a return (P9–P11) | S20 c1, c3, c4 reach P11; no cell reaches P9 or P10 | 63 for P11 |
| Derived-value error (P12–P13) | S20 c2; S16 | 12 + 3 |
| Established deviation (P14–P18) | S20 c1; S20 c4; S21 d4; S16 | 33 + 15 + 3 + 3 |
| Conflicting execution records (P19–P23) | S20 c3; S20 c4; S21 d3, d5, d6, d7; S16 | 15 + 15 + 12 + 3 |
| Shared assumptions (P24) | none | 0 |

## Explicit resolutions

**S7, assertion 4 — reaches no restructured sentence.**
`tests/runs/2026-07-16-scenario7-fanout.md` records assertion 4 as `NOT TESTED`, with the evidence "No workers to reconcile": the fan-out-capable arm judged the fan-out criterion unmet and stayed inline, so no worker return ever existed to verify.
The two serial arms score assertion 5 only, and say so in their own totals.
No archived S7 arm traverses the passage, there is no archived outcome for the restructure to reproduce, and S7 owes nothing.
What this does not say: S7's assertion 4 is the duty P1 states, so the cell would reach the passage if a future arm ever fanned out — the reason it does not is a property of the archived runs, not of the fixture.

**S19 — reaches the lead sentence and the Free-check group, and nothing below them.**
The three with-skill arms performed the free check on the two returns that did arrive: `2026-07-21-scenario19-with-skill-a.md` scores assertion 5 on "Both `REFUTED` on the clean returns after free-check verification", and arm c's note records "a free-check pass that found both returns clean".
The evidence artifact carries the arms' own words — "the free check found no fault", "Nothing in that free check faulted either return", and outcomes resting "on unverified worker attestations" — which places them in P1–P8 and specifically in P7/P8.
Because no fault was found, no arm entered P9–P23: the classification and disposition groups are not reached by this cell.
S19 owes arms for the lead sentence and the Free-check group only.

**P24 (shared assumptions) — reached by no archived cell.**
No arm anywhere in the archive quotes it, and no scenario asserts on it: S20 and S21 hand the agent a single test's return, so there is nothing shared to validate, and neither S16 nor S19 is scored on cross-worker assumptions.
P24 moves with the rest and is unmeasured before and after; that is a standing gap in the fixture family, not a debt this change creates.

**P9 and P10 — reached by no archived cell, for a documented reason.**
`scenarios.md` records that a packet carrying an established *and* an unresolvable fault together is unmeasured, and no fixture builds one.
These two sentences move with the rest and owe no arms, because no cell's decision point traverses them.

## Preregistered expectation

The restructure changes no sentence's bytes and no sentence's order.
The expectation is therefore that **every reached cell reproduces its archived outcome and its archived rationale**, and that no cell's rationale starts citing a group label as if the label were the rule.
A divergence is a finding about the restructure — evidence that list structure and labels carry behavior the running prose did not — and it is reported as such rather than smoothed over.

Verdicts enumerated in advance, including the ones where nothing ships:

| Result | Verdict |
| --- | --- |
| Every reached cell reproduces its archived outcome, and rationales still cite sentences rather than labels | merge, claimed as a structure-only change with no behavioral claim |
| Any reached cell diverges, and the divergence's rationale cites the new structure | do not merge as written; the divergence is the finding, and it is written up whether or not the branch is revived |
| Any reached cell diverges citing a rule outside the passage (the null-result sensitivity rule, the causal-identification rule) | not attributable to the restructure; re-scope per `PROTOCOL.md` step 2 and rerun before drawing any conclusion |
| No arms are authorized, or the human judges the legibility gain too small to buy at this arm cost | decline the restructure and keep the current prose |

The last row is reachable without the change existing and is satisfiable without running anything.
It is here because a table written by someone who intends to ship omits the row where nothing ships.

## Owed arms, for the human merge gate

Precedent for the size of this obligation: round 5 of the S20 wave measured a **byte-identical** sentence that had only been promoted from a continuation line to its own list item, with three c1 arms, on the standing rule that a changed agent-read file gets measured rather than reasoned about.
This change is that same class of edit applied to every group of the passage, so the obligation is one batch per reached cell rather than one arm overall.

Minimum defensible batch, n=3 per cell, matching the archived cadence so outcomes are comparable:

| Cell | Arms | Groups it reaches |
| --- | --- | --- |
| S20 c1-established (both files) | 3 | P1, Free check, P11, Established deviation |
| S20 c2-derived (both files) | 3 | P1, Free check, Derived-value |
| S20 c3-unresolvable (both files) | 3 | P1, Free check, P11, Conflicting records |
| S20 c4-immaterial (both files) | 3 | P1, Free check, P11, Established deviation, Conflicting records |
| S21 d3-conflict | 3 | Conflicting records |
| S21 d6-support-conflict | 3 | Conflicting records |
| S21 d5-unrepeatable | 3 | Free check (P7, P8), P22, P23 |
| S21 d7-support-clean | 3 | Free check (P7, P8), P22 |
| S21 d4-deviation | 3 | Established deviation (P18) |
| S19 with-skill | 3 | P1, Free check |
| S16 with-skill | 1 | the whole passage, under free investigation |

Total: **31 arms**.
Not owed, for the reasons recorded above: S7 (no arm reaches the passage), S21 d1 (quotes no restructured sentence and is governed by the Conclusion section), and any cell for P9, P10, or P24 (no cell reaches them).

Two notes for the gate to weigh rather than inherit:

- S21 d1 is cheap and is the floor control the scenario built; adding it back costs 3 arms and buys a check that the restructure did not disturb the one cell expected to be indifferent to it.
- The S16 arm is scoped at n=1 because that is the archived cadence for that cell, and n=1 is stated as measured, never as proven.

A cheaper first pass exists and is **not** preregistered as sufficient: one arm per S20/S21 cell, nine arms, as a divergence screen.
A screen that comes back clean at n=1 does not license the merge, because the expectation here is reproduction across a cell and one arm cannot show it.
If a screen is run, its arms are named as a screen and reported apart from any scored batch.

## Honest limits of this scoping

Reachability is settled from the archive and the fixture descriptions, not measured; that is what `PROTOCOL.md` prescribes, and it is still a judgement.
Quotation evidence is a lower bound, so a cell marked as reaching a group on fixture reasoning could in practice never traverse the sentence, and a cell marked unreached could traverse one silently.
The archived outcomes were produced against earlier wordings of this file, so "reproduces its archived outcome" compares across a text difference this document does not quantify — the comparison is still the right one for a change that alters no sentence, but a divergence would have to rule that difference out before it is attributed to the restructure.
No arm was run for this document, and no claim in it is a measurement.
