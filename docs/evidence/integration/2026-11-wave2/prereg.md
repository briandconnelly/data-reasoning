# Wave 2: the `resolved` verdict (#114) and the record pointer (#119) — preregistration

Issues #114 and #119.
Written 2026-11-25, before any arm of this wave, canary included, ran.
Everything below is fixed before the canaries; any change after them is a dated note at the end, never an edit above it.
The measurement law, the order of work, and what a changed sentence owes are `skills/hypothesis-driven-analysis/tests/PROTOCOL.md`'s; this file applies them and does not restate them.

## Question

Two candidate changes to agent-read prose sit on draft branches, and neither merges before its gate here passes.

- **#114**: does adding a seventh decide verdict, `resolved`, make a `decision-analysis` arm record a structurally excluded state as a resolved proposition and recommend from the surviving state's losses, where the current text does not, without making an arm treat zero events in a finite sample as elimination?
- **#119**: does adding two sentences to the shared Record Delivery text make an arm whose records sit in scratch name a path to each record that the user can open after the turn, where the current text does not, without costing records, their timing, or the answer?

"The change is unnecessary" and "no change" are reachable outcomes for both, and are rows in § B.

## Pinned inputs

| Name | Full SHA | What it is |
| --- | --- | --- |
| `BASE` | `b5724c18408b0be2c3103ae76c512d82dc2e7fe3` | `dev` when both candidates branched; the current text for both comparisons |
| `C114` | `ae90b4003336c451b3d8797ff53362e14c9a7d31` | `origin/feat/114-resolved-verdict` (draft PR #137), the #114 candidate |
| `C119` | `0b137643e04435cf2db72c90481686529ec08a26` | `origin/feat/119-record-pointer` (draft PR #134), the #119 candidate |
| `M` | named in the dated note before stage A | the measurement commit: `dev` containing #128's neutral I-cell staging, this file, and the capture change of § G |

`git merge-base BASE C114` and `git merge-base BASE C119` are both `BASE`, so each candidate differs from `BASE` only by its own commits.

Rebase rule: after a rebase of either candidate onto `dev`, its pinned SHA moves only by a dated note at the end of this file.
The note records the new base and candidate SHAs and shows that the measured treatment is byte-identical, by comparing `git diff --no-ext-diff -U0 <old base> <old candidate> -- <treatment paths> | grep -v -e '^index ' -e '^@@'` with the same command on the new pair; any difference voids the measurement for the sentences that changed.
The #114 treatment paths are `skills/decision-analysis/SKILL.md`, `skills/decision-analysis/references/`, `skills/decision-analysis/decisions/`, and `instruments/check_record.py`, with the scorer's `skills/decision-analysis/tests/check_decision.py` compared the same way.
The #119 treatment paths are `scripts/shared-sections/record-delivery.md` and the four `skills/*/SKILL.md`.

Fixtures and prompts, pinned by git object at the named commit:

| Cell | Prompt | Prompt SHA-256 | Fixture | Fixture tree |
| --- | --- | --- | --- | --- |
| DA-S12 | `skills/decision-analysis/tests/fixtures/da-ruled-out-prompts/da-s12.txt` at `C114` | `75aa19faa903071135ca8db3ca6792dd506b6c3495f9bcbd2ff5c5f76de8b774` | `skills/decision-analysis/tests/fixtures/da-ruled-out/s12-partition-loss` at `C114` | `da-ruled-out` tree `d1922e2c555fe3d81614b96e75fde979ef6252bc` |
| DA-S13 | `skills/decision-analysis/tests/fixtures/da-ruled-out-prompts/da-s13.txt` at `C114` | `b2aeac0a01167397a5b64c9c4eb94704658aa488baed2daeebd7d7891dc50cba` | `skills/decision-analysis/tests/fixtures/da-ruled-out/s13-zero-events` at `C114` | same tree |
| DA-S10 | `skills/decision-analysis/tests/runs/artifacts/2026-11-09-evidence-sweep/prompts/da-s10.txt` | `7b34f89d49e10386fb3af7a35180eafb3caef866d1e3a32066b08eb5407663fb` | `skills/decision-analysis/tests/fixtures/da-sweep/s10v2-loss-matrix` | `7b91494af7ebc04a1ef637057f63ff9e0c984f72` |
| I2 | `scripts/run_integration.py` `CELLS["I2"]` | `fe76b3fb8040a8f46965f00f87038e2e64d2250e5e261cc5a34442d78c55c9d8` (`prompt_sha256`) | `skills/hypothesis-driven-analysis/tests/fixtures/s5b-seam` | `d54d1f65be1800ed70cb321123b285f4b9bbca92` |
| I4 | `scripts/run_integration.py` `CELLS["I4"]` (Scenario 15's `PROBLEM.md`) | `fa5edea127117f1bd1b9ead7edd1f6e9e038be756012f99b8a289656a3d740e7` (`prompt_sha256`) | `skills/hypothesis-driven-analysis/tests/fixtures/s15-assist-rollout` | `f265161f732f5f280c152f2c1d0664b5e7a6d238` |

The DA-S12 and DA-S13 fixtures exist only on the #114 branch until it merges; they are read from a detached worktree at `C114` (§ D), never from `dev`.
Each fixture is held to its properties by its validator before stage A: `uv run skills/decision-analysis/tests/fixtures/validate_da_ruled_out.py skills/decision-analysis/tests/fixtures/da-ruled-out` in the `C114` worktree, and the `validate-da-sweep-fixture`, `validate-s5b-seam-fixture`, and `validate-s15-fixture` prek hooks at `M`.

Models: Claude Code `--model claude-sonnet-5-5` and Codex `-m gpt-6.2-sol`, as `docs/evidence/integration/representative-v1/prereg.md` pinned them.
Host versions are recorded in the dated note before stage A; an arm on another version is an invalid execution (§ H).

## A. Reachability, sentence by sentence

Per PROTOCOL § What owes a rerun, a cell owes arms when its decision point traverses an edited sentence.
"Traverses" below is judged from the scenario text and the fixture, read with the prose; each cell's anchor was checked against its catalog heading on 2026-11-25 (the reviewers' line anchors in the #114 and #119 reachability notes all resolve to the scenarios they name).
The reviewers' lists were claims; where this section differs from them it says so.

### #114: edited sentences and the cells that traverse them

Ordinary decide cells, for this section: DA-S1, DA-S1x, DA-S2, DA-S3, DA-S8, DA-S9, DA-S10, DA-S4 only if it writes a reframed record, and the representative suite's X1 (Codex).
DA-S5, DA-S7, and DA-S11 take the VoI route; DA-S6 exits before decide.

| # | Where | Edited sentence (short form) | Cells whose decision point traverses it | Fresh arms in this wave |
| --- | --- | --- | --- | --- |
| 1 | § Routing | an exclusion keeps an ask on `decide` only once verified and in hand; a disputed one routes `out: adjudicate` | DA-S12 (verified side: its README states every fact verified and none in dispute) | DA-S12 |
| 2 | § Numeric Policy | `sensitivity-only` may also appear in a resolved record's surviving-state losses and difference | a resolved record with an unsupported loss: no cell (DA-S12's losses are owner-supplied); VoI cells read the sentence but the inserted clause grants a permission only to a resolved record, so their decision is unchanged | none |
| 3 | § Numeric Policy | a state is eliminated only by a structural exclusion making the whole accepted evidence impossible under it and possible under the other; the record is then `resolved`; ratios stay strictly positive | DA-S12 (exclusion side); DA-S13 (no exclusion, zero count); every ordinary decide cell (no exclusion: every packet's evidence has a positive ratio) | DA-S12, DA-S13, DA-S10 control |
| 4 | § Numeric Policy | doubt about an exclusion assumption that leaves the evidence possible under both states is not elimination | no cell: DA-S12 states no doubt, DA-S13 has no exclusion assumption | none (uncovered) |
| 5 | § Numeric Policy | zero events eliminates only when the stated model makes the complete observation impossible | DA-S13 | DA-S13 |
| 6 | § Numeric Policy | an upper confidence bound is not a likelihood | DA-S13 (its third assertion) | DA-S13 |
| 7 | § Numeric Policy | evidence impossible under both states reaches no verdict: model review | no cell | none (uncovered) |
| 8 | § Numeric Policy | `resolved` is decided before the ordered rule; `dominated` never fires on eliminated-state losses | DA-S12 (bypass; its losses (0, 4) and (6, 1) are not dominated across both states, so the precedence is never contested); DA-S13 and the ordinary cells (pass through) | DA-S12, DA-S13, DA-S10 control |
| 9 | § Numeric Policy | the surviving-state comparison: the loss difference, jointly or as the endpoint interval | DA-S12 (point difference 4 − 1 = 3) | DA-S12 |
| 10 | § Numeric Policy | belief-grade difference below 0 → first row, above 0 → second row, exactly 0 → `no preference`, otherwise returned to owner | DA-S12 (above-0 branch only) | DA-S12 |
| 11 | § Numeric Policy | a structural exclusion licenses causal wording only for the negation of the excluded proposition | DA-S12 (the device log's disk fault invites a cause claim); DA-S4's neighbouring prohibition is not edited | DA-S12 |
| 12 | § The Decide Route | "Six blocks, in order, except under `resolved` (below)" | every decide cell (six-block side); DA-S12 (exception) | DA-S12, DA-S13, DA-S10 control |
| 13 | § The Decide Route, Verdict | the closed set gains `resolved`; selection is the elimination condition, then the ordered rule | every decide cell | DA-S12, DA-S13, DA-S10 control |
| 14 | § The Decide Route, Verdict | under `resolved`, Recommended action reads what the comparison gives | DA-S12 | DA-S12 |
| 15 | § The Decide Route, Resolution | the resolved skeleton and the Resolution block's contents | DA-S12 | DA-S12 |
| 16 | § The Decide Route, Resolution | the model-review draft (`Surviving state: none`), its response, and its handoff (two sentences) | no cell | none (uncovered) |
| 17 | template, opening | use the Resolved blocks instead when the verdict is `resolved` | every decide cell (choosing a skeleton) | as row 12 |
| 18 | template | the resolved skeleton and its slot notes | DA-S12 | DA-S12 |
| 19 | `instruments/check_record.py` feedback | findings on a resolved record; on an ordinary record, only a finding that prints the closed verdict set now lists `resolved` (`test_ordinary_records_are_unchanged` on the branch holds every other finding on 57 archived records byte-identical) | DA-S12 (resolved findings); any decide arm whose record draws a verdict-set finding | carried by every #114 arm (§ D) |
| 20 | `skills/decision-analysis/decisions/008-ruled-out-state.md`, `decisions/README.md` | the dated disposition and contract | none: no SKILL.md or template sentence links either file, so no route reads them; they owe nothing, and a read of a staged `decisions/` file voids the arm (§ H), because 008 names DA-S12 and its expected record | none |

Deviation from PROTOCOL, stated rather than hidden: rows 3, 8, 12, 13, and 17 are traversed by every ordinary decide cell, so PROTOCOL owes arms on DA-S1, DA-S1x, DA-S2, DA-S3, DA-S8, DA-S9, DA-S10, and X1.
This wave pays one matched control, DA-S10 at one arm per condition, and leaves the others as named debt (§ B row 11), for three reasons.
At those cells the new sentences ask one question, whether any state is structurally excluded, and every packet's evidence carries a positive sourced ratio (DA-S1 and DA-S8 4.5, DA-S9 0.5–4, DA-S10 3, X1 one defective in 150), so a correct arm answers no and proceeds as before.
The failure that answer can take, a false elimination, is the one DA-S13 is built to provoke, with a zero count, and DA-S13 is paid in full.
What else changes for an ordinary record, the validator's feedback, is held identical by the candidate's golden test except for the closed-set listing (row 19).
DA-S10 is chosen as the control because it shares DA-S13's path through the ordered rule (point inputs, a `robust` verdict, a named action) and has an archived scored run at n=3 (`skills/decision-analysis/tests/runs/2026-11-10-evidence-sweep.md`: post arms 3/3 on verdict and action), which scopes it without a fresh n=3 pair.
DA-S2 and DA-S4 have no generated fixture; DA-S1x, DA-S3, DA-S8, and DA-S9 reuse their archived counts for scoping and are not rerun.

### #119: edited sentences and the cells that traverse them

| # | Where | Edited sentence | Cells whose decision point traverses it | Fresh arms in this wave |
| --- | --- | --- | --- | --- |
| 1 | shared Record Delivery, rendered into all four SKILL.md | "For each record you wrote or updated as a file for this request, the final message names a path the user can open after the turn; a summary in the answer does not replace it." | every cell where an arm writes a record as a file, listed below | I2, I4 on Codex |
| 2 | shared Record Delivery | "When nothing you can write to stays open to the user after the turn, say so as a delivery limitation rather than presenting a path as delivered; the owning route's record and its timing still apply." | traversed by every file-writing cell as a check; its limitation branch is taken only where storage does not persist after the turn, which no cell sets up | I2, I4 (check side only) |
| 3 | HDA § Conclusion | "… then any ledger pointer § Record Delivery requires" (was "a pointer to the ledger when a durable artifact exists") | every HDA full-route cell that reaches Conclusion: HDA Scenarios 1, 4, 6, 7, 8, 10, 12, 15, 16, 19 (and 18 if its composition run completes the route); EDA E1 arms A2 (full branch) and A3; I2, I3, I4 when HDA completes a full ledger | I2, I4 |

This is a semantic change, not a cross-reference: under the current text a scratch ledger is arguably not a durable artifact, so no pointer is owed; under the candidate one is.
The cells traversing rows 1 and 2, verified against each catalog: HDA Scenarios 1, 4, 6, 7, 8, 10, 12, 15, 16, 19 (full ledger), 9/9a/9b (estimation record when filed), 11, 13, and S22a/b/d (mini ledger when filed), 14 (collection plan); EDA B1–B10 and E1 A1 (exploration log; B9 also a collection plan); CIR CS3, CS4, CS5, CS6b, CS7 stage 1, CS8; DA-S1, S2, S3, S4 (if a record), S8, S9, S10, S12, S13, and the VoI cells S5, S7, S11 when the VoI block is filed; integration I2, I3, I4, and the representative X1 (X2 and X3 only if an arm files a record, which no archived Codex arm did).
HDA Scenarios 20 and 21 stop before any record and do not traverse them.

Nothing else on the #119 branch is agent-read on any route.
`skills/hypothesis-driven-analysis/decisions/010-owed-records-on-a-multi-skill-decision-request.md` and `CHANGELOG.md` ship in the release tree but no SKILL.md sentence links them; both arms carry them at `M`'s text (§ D), so they owe nothing and are not part of the treatment.

Why I2 and I4, and not a catalog cell: the failure #119 targets is a record that sits in scratch and is never pointed to, and those are the cells where it happened.
Re-derived from the 2026-11-17 Codex plugin transcripts (`docs/evidence/integration/2026-11-17-full-catalog/arms/`), by a script that lists each file a command writes and each `.md` path the final message names:

- I2: 3 of 3 arms wrote an exploration log under `/tmp` (plugin-1 and plugin-3 also a ledger there); only plugin-2's final message named its scratch files; no record was in the workspace.
- I4: plugin-2 and plugin-3 wrote a ledger and an identification review under `/tmp`; all three final messages named only the memo in the workspace.
- The same counts appear in decision 010's transcript table, so its premise holds (PROTOCOL step 0).
- I3, checked as a positive control on the instrument: plugin-1's final message already named both `/tmp` records and plugin-3's both workspace records, so I3 is near the ceiling under the current text and would not discriminate.

I2 and I4 together exercise the four validator-signature forms as files: the exploration log (I2), the full ledger (I2, I4), the identification review (I4), and a decision record when I4's arm writes one in template form (0 of 3 archived arms did; the memo is not one).
They cannot reliably exercise a file-backed record without a validator signature (mini ledger, estimation record, collection plan), the inline mini-route form, or a no-file-tools form.
No focused single-skill cell is added for those: the only harness with a single-skill cell is `run_arm.py`, Claude Code only, whose frame tells the arm where to write its working files, which is itself a delivery instruction, so it cannot measure a delivery rule cleanly.
X1 is not included: its archived Codex plugin arms already retained and named their record in 3 of 3, so it is a ceiling, and no row in § B needs a ceiling control to decide shipping.

### Branches no cell in this wave exercises

Each is unmeasured in this wave and is named as such wherever the shipped text is described.

| Branch | Candidate | Cost to cover, in arms | What ships unmeasured if the owner declines |
| --- | --- | --- | --- |
| A disputed exclusion (`out: adjudicate`) | #114 | a new DA cell with a generated packet: 1 canary + 3 + 3 = 7 | the routing sentence's disputed side (row 1) |
| Doubt about an exclusion assumption leaving both states possible | #114 | new cell: 7 | row 4 |
| Evidence impossible under both states (model review, draft, handoff) | #114 | new cell: 7, plus checker evidence of the draft's findings | rows 7 and 16 |
| Precedence over real two-state dominance | #114 | new cell whose eliminated-state losses would make `dominated` fire: 7 | the `dominated` half of row 8 |
| A joint loss difference narrower than the endpoint interval | #114 | new cell: 7 | row 9's joint branch; the catalog notes no checker reads the Conditions statement it needs |
| An exact surviving-state tie (`no preference`) | #114 | new cell: 7 | row 10's 0 branch |
| An unsupported surviving-state loss (`none supported`, returned to owner) | #114 | new cell: 7 | rows 2 and 10's owner-return branch |
| A negative difference, or one reaching or spanning 0 | #114 | new cell: 7 (could share a packet family with the two above at 3 cells, 21 arms) | row 10's other branches |
| Runner-only scratch (a workspace torn down after the turn) | #119 | a harness mode that deletes the workspace and temp writes before the post-turn check, plus a host environment that tells the arm its storage is ephemeral: harness work and 1 + 3 + 3 = 7 arms per cell | row 2's limitation branch, and the rule that a path on a torn-down runner is not delivered |
| A file-backed record without a validator signature | #119 | a new integration cell whose ask routes HDA `mini` or `estimation` with file tools, on Codex: 7 | row 1 for those forms |
| The inline mini-route form and the no-file-tools forms (owe no path) | #119 | a no-file-tools variant of one cell: 7 | that the new sentences do not push an inline form into a file |
| Claude Code for #119, Codex for #114 | both | #119 on Claude Code: I2 and I4 at 1 + 3 + 3 each = 14, though no archived Claude Code plugin arm made a handoff; #114 on Codex has no single-skill harness | each change on the host not measured |

The #114 rows are also exercised by the candidate's checker unit suites; those show the checkers decide each branch as the contract says, not that an agent reaches it.

## B. Every verdict the measurement can reach

Rows are evaluated per candidate after its stage, in order; the first row that matches governs, except row 11 of each table, which applies beside any other.
"Reachable without the change" means the row can fire even if the candidate text had no effect on any arm.

### #114 (cells DA-S12, DA-S13, DA-S10; columns in § F)

| # | Outcome | Disposition and shipping consequence | Reachable without the change |
| --- | --- | --- | --- |
| 1 | A checker defect surfaces while scoring | interpretation paused; the defect is fixed with a test on the candidate branch, every archived record rescored transparently, then resume at row 2; nothing ships meanwhile | yes |
| 2 | DA-S12 or DA-S13 ends with fewer than 3 valid arms in a condition after replacements | that cell is **not measured**; #114 does not ship, since its gate is unmet; the owner chooses a dated rerun note or closure | yes |
| 3 | A candidate arm on DA-S13 or DA-S10 fails FE (false elimination) and the current arms fail FE on fewer | **regression on the false-positive side**: rows 3–6 of § A are withdrawn or revised and remeasured; #114 does not ship | no |
| 4 | The DA-S10 candidate arm fails a catalog assertion its current arm passes | **regression on a control**: the sentences it reaches are withdrawn or revised and remeasured; #114 does not ship | no |
| 5 | On DA-S13, candidate arms pass the arm-level criterion on at least 2 fewer arms than current | **regression on DA-S13**: does not ship | no |
| 6 | At least 2 of 3 candidate DA-S12 arms take `out: adjudicate` (O1) | **routes around the rule**: `resolved` is unmeasured on this model; #114 does not ship as measured; the owner decides between a new draft of the routing sentence or the packet (own arms) and closure | yes |
| 7 | At least 2 of 3 current DA-S12 arms pass O2 | **change unnecessary for behaviour**: the one-state recommendation already happens; the owner decides between closing #114 with no change (decision 008 gets a dated note) and shipping the record form as a clarification with no measured behavioural claim, the latter only if at least 2 of 3 candidate arms pass O3 | yes |
| 8 | At least 2 of 3 candidate DA-S12 arms pass both O2 and O3, at most 1 of 3 current arms pass O2, at least 2 of 3 candidate DA-S13 arms pass, and rows 3–5 did not fire | **successful correction**: #114 ships as measured (Claude Code, `claude-sonnet-5-5`, n=3 on DA-S12 and DA-S13, n=1 control on DA-S10) | no |
| 9 | At most 1 of 3 candidate DA-S12 arms pass O3, and row 6 did not fire | **form not adopted**: the text does not produce the record it defines; #114 does not ship; revise as a new draft with its own arms, or close (no change) | yes |
| 10 | Anything between rows 7 and 9 (a one-arm difference, O2 without O3, or O3 without O2) | **observed, not established**: reported with counts; the owner decides between closing and shipping as a clarification with no measured claim | yes |
| 11 | Beside any row: cells § A shows are reached and this wave does not run, and every branch in § A's uncovered table | **unmeasured debt**, named in `docs/evidence-status.md`; the shipped text is never described as measured on them | yes |
| 12 | Anything not matched above | owner decides, with the counts; no claim of lift | yes |

The current text has no `resolved` verdict, so a current arm cannot pass O3 or DA-S12's second assertion by construction; the attribution question between conditions is O2, and O3 measures whether the candidate's form is adopted.
The one baseline (no-skill) arm per new cell that the DA catalog's convention describes is not run: no row above needs it to decide shipping (§ E).

### #119 (cells I2 and I4 on Codex; columns in § F)

An arm is **informative** for a cell when it created at least one record as a file (column R1 of § F).
An informative arm **delivers** when every record it created as a file passes both R4 (pointer) and R3 (openable at the named path).
k is the number of delivering arms among a condition's valid informative arms on a cell.

| # | Outcome | Disposition and shipping consequence | Reachable without the change |
| --- | --- | --- | --- |
| 1 | A capture defect: a record the transcript shows written is missing from the capture, or a named-path check is wrong against the archive | interpretation paused; fixed with a test; rescored from the archive where the bytes exist, otherwise the affected arms are reported not measured | yes |
| 2 | A cell has fewer than 2 valid informative arms in either condition | that cell is **not measured** on the rule; if neither cell is measured, #119 does not ship as measured and the owner decides | yes |
| 3 | On a measured cell, candidate arms pass the answer columns (E and C, both) on at least 2 fewer arms than current | **answer regression**: the sentences are withdrawn or revised and remeasured; #119 does not ship | no |
| 4 | On a measured cell, candidate arms pass R1 or R2 on at least 2 fewer arms than current, for any owed record | **record regression** (the pointer rule displaced creation or timing): does not ship | no |
| 5 | Candidate arms make at least 2 more false deliveries (R4 pass with R3 fail and no R6 statement) than current arms, across both cells | **false delivery**: does not ship; any single false delivery is reported in either condition | no |
| 6 | Current k ≥ 2 on every measured cell | **change unnecessary for behaviour**: the owner decides between closing #119 with no change (decision 010 gets a dated note) and shipping as a clarification with no measured behavioural claim | yes |
| 7 | Candidate k ≥ 2 and current k ≤ 1 on every measured cell, at least one cell measured, and rows 3–5 did not fire | **successful correction**: #119 ships as measured (Codex, `gpt-6.2-sol`, I2 and I4, n=3 per condition) | no |
| 8 | Candidate k ≤ 1 and current k ≤ 1 on every measured cell | **no lift**: the sentences do not produce the behaviour; does not ship; revise as a new draft with its own arms, or close (no change) | yes |
| 9 | Anything else between rows 6 and 8 (a lift on one cell only, a one-arm difference) | **observed, not established**: reported with counts; the owner decides between closing and shipping as a clarification with no measured claim | yes |
| 10 | Beside any row: every reached cell § A lists that this wave does not run (the HDA, EDA, CIR, and DA catalog cells, I3, X1, and Claude Code), and every uncovered branch | **unmeasured debt**, named in `docs/evidence-status.md` | yes |
| 11 | Anything not matched above | owner decides, with the counts; no claim of lift | yes |

At n=3 nothing is a rate; every row is reported with its exact counts, and a 3/3 against 3/3 tie is "no observed lift", never "no effect".

## C. Other rules each fixture triggers (PROTOCOL § Procedure 2)

### DA-S12

| Rule | How it is neutralized or scored |
| --- | --- |
| `out: adjudicate` (the loss's cause is a factual question) | not neutralized, by design: the README states every fact verified and none in dispute, which keeps the candidate's routing sentence on `decide`, but an arm may still hand off defensibly, so a correct handoff (O1), a correct one-state recommendation (O2), and adoption of the `resolved` form (O3) are three separately scored outcomes, and § B rows 6–10 read them separately |
| Authorization gate (rolling back is a production action) | nothing in the packet is executable and the ask is a recommendation; a verdict authorizes nothing (§ Numeric Policy); an arm that claims to have acted is reported |
| Missing losses | the owner's four losses are in `evidence/owner-losses.md`, `user-elicited` |
| `dominated` | not dominated across both states: roll back (0, 4) and hotfix (6, 1) |
| No supported prior (a current arm's likely path) | scored, not neutralized: a current arm writing the missing-support form passes O2 only if its answer still recommends from the surviving state's losses without an invented ratio |
| Causal wording (the device log shows a disk fault) | scored as column CW; the job's non-involvement may be asserted, the disk fault as the cause may not |
| Evidence untrusted | the packet carries no instructions; verified by reading all seven files on 2026-11-25 |
| Record Delivery and the validator | the arm runs the validator it was staged (§ D); its runs are recorded, not scored |
| Decision records 008 and README (staged with the skill) | an arm that reads any staged `decisions/` file is voided (§ H) |

### DA-S13

| Rule | How it is neutralized or scored |
| --- | --- |
| Robustness-first priors (widening the owner's prior) | the owner's prior odds 1 are "settled and not to be revisited"; S13.4 scores Prior class swept `1` |
| Independence of the 100 host-weeks | stated, with reasons, in the README; S13.2 requires the record to name it |
| Upper bound as likelihood | scored by S13.3 |
| VoI (keep piloting is also more information) | the ask names two actions with owner losses, so `decide` is the designed route; an arm that routes `voi` fails S13's route and is reported; identical across conditions |
| `dominated`, missing losses | not dominated (roll out (10, 0), keep piloting (1, 1)); losses supplied |
| Authorization, costly collection | nothing to execute or pull |

### DA-S10 (control)

As `skills/decision-analysis/tests/runs/artifacts/2026-11-09-evidence-sweep/prereg.md` § Other rules each packet reaches neutralized them; nothing in that packet approaches elimination (ratio 3 from 20,000 canaries per stratum).

### I2 and I4

| Rule | How it is neutralized or scored |
| --- | --- |
| Multi-skill route (EDA → HDA on I2; HDA → (CIR) → DA on I4) | record columns are scored on the observed route, and records missed because the designed route was skipped are reported separately (decision 010's ruling) |
| Timing across a handoff (an upstream skill's results precede a downstream record legitimately) | R2 uses each owning route's own precommitment boundary (§ F) |
| Scratch default in the ledger and exploration-log templates | unchanged in both conditions; R1 does not fail a record for sitting in scratch |
| The record-checking hook | absent on Codex in both conditions, as in every earlier Codex arm |
| Evidence boundary and task | E and C as `docs/evidence/integration/2026-11-17-full-catalog/prereg.md` § Scoring defines them for I2 and I4, as answer controls |
| Cross-arm scratch (one arm's `/tmp` file read or appended by a later arm) | `--clear-scratch` removes each arm's archived scratch originals after its post-turn check; a captured file flagged `top_entry_preexisted` is inspected, and an arm that read or appended to an earlier arm's file is voided (§ H) |
| Condition leak through the workspace name | #128 stages I1–I4 in a neutral `int-arm-*` workspace with a relative `data/` path; `M` must contain it (§ D checks it) |

## D. Matched arms

Each comparison is the current text against the candidate text, run by one harness revision, on the same fixtures, prompts, model, and host version, in one interleaved order, with arm names that carry no condition; the conditions differ only in the treatment.

**#114 validator feedback is part of the treatment.**
`run_arm.py` stages `instruments/check_record.py` from the arm's `--skill-ref` (its default `--instruments-from skill-ref`), so current arms get `BASE`'s validator and candidate arms `C114`'s.
The shipped unit is the SKILL.md, the template, and the validator together; the `BASE` validator rejects every `resolved` record, so a candidate arm given it would be told to change a correct record, which § Record Delivery forbids; and the candidate validator in a current arm would supply guidance the current text does not.
On an ordinary record the two validators differ only in the closed-set listing (§ A row 19), so DA-S13 and DA-S10 see the same feedback in both conditions apart from that word.
This matches the estimand of the 2026-11-09 wave.
`tests/check_decision.py` is never staged; it is the scorer's instrument, run at `C114` on every record.

**#119 has no validator change.**
Its two plugin builds differ only in the five treatment files; the validator, hook, decision records, and `CHANGELOG.md` are `M`'s in both.

### Setup (once, before stage A)

Run from the main checkout, with the repo `.env` moved to `~/.cache/data-reasoning-env-hold/` first and restored after the batch, size and mtime confirmed, per the plan's standing procedure.

```sh
git fetch origin
R=$(git rev-parse --show-toplevel)
BASE=b5724c18408b0be2c3103ae76c512d82dc2e7fe3
C114=ae90b4003336c451b3d8797ff53362e14c9a7d31
C119=0b137643e04435cf2db72c90481686529ec08a26
M=<full SHA of origin/dev, as named in the dated note before stage A>
W="$R/../w2-measure"      # current text for #119; harness and archive for both
K="$R/../w2-c114"         # read-only source of the DA-S12 and DA-S13 fixtures and prompts
N="$R/../w2-c119"         # candidate text for #119
git worktree add --detach "$W" "$M"
git worktree add --detach "$K" "$C114"
git worktree add -b wave2-119-treatment "$N" "$M"
T119="scripts/shared-sections/record-delivery.md skills/exploratory-data-analysis/SKILL.md skills/hypothesis-driven-analysis/SKILL.md skills/causal-identification-review/SKILL.md skills/decision-analysis/SKILL.md"
git -C "$N" diff --no-ext-diff --binary "$BASE" "$C119" -- $T119 > "$R/../w2-119.patch"
git -C "$N" apply --index "$R/../w2-119.patch"
git -C "$N" commit -m "test(integration): wave-2 #119 treatment, for measurement only"
```

Checks, each of which must pass before any arm; a failure stops the batch:

```sh
# #128 is in M: I-cell prompts carry a relative data path
(cd "$W" && uv run scripts/run_integration.py --cell I2 --host codex --condition plugin --name probe --out /tmp/w2-probe --dry-run | grep -F '(`data/events.csv`)')
# the #119 treatment is exactly the candidate's five-file diff
git -C "$N" diff --no-ext-diff --stat "$M" HEAD          # lists exactly the five T119 files
diff <(git diff --no-ext-diff -U0 "$BASE" "$C119" -- $T119 | grep -v -e '^index ' -e '^@@') \
     <(git -C "$N" diff --no-ext-diff -U0 "$M" HEAD | grep -v -e '^index ' -e '^@@')
(cd "$N" && uv run scripts/check-shared-sections.py)
# the #114 staged treatment differs from BASE only in the five files § A names
git diff --no-ext-diff --stat "$BASE" "$C114" -- skills/decision-analysis/SKILL.md skills/decision-analysis/references skills/decision-analysis/decisions skills/decision-analysis/agents instruments/check_record.py
# fixtures hold their properties
(cd "$K" && uv run skills/decision-analysis/tests/fixtures/validate_da_ruled_out.py skills/decision-analysis/tests/fixtures/da-ruled-out)
(cd "$W" && prek run validate-da-sweep-fixture --all-files && prek run validate-s5b-seam-fixture --all-files && prek run validate-s15-fixture --all-files)
# host versions, recorded in the dated note
claude --version; codex --version
```

If `M`'s copies of the five #119 files differ from `BASE`'s, the `diff` above fails and the batch stops for a dated note; the treatment is never hand-merged.

### Commands

Common variables, from any directory:

```sh
RUN="$W/skills/hypothesis-driven-analysis/tests/run_arm.py"
FX="$K/skills/decision-analysis/tests/fixtures"
DAO="$W/skills/decision-analysis/tests/runs/artifacts/2026-11-wave2-resolved"
P10="$W/skills/decision-analysis/tests/runs/artifacts/2026-11-09-evidence-sweep/prompts/da-s10.txt"
F10="$W/skills/decision-analysis/tests/fixtures/da-sweep/s10v2-loss-matrix"
IO="$W/docs/evidence/integration/2026-11-wave2"
da() {  # da <name> <ref> <prompt> <fixture>
  uv run "$RUN" --name "$1" --prompt-file "$3" --skill decision-analysis --skill-ref "$2" \
    --fixture "$4" --out "$DAO" --model claude-sonnet-5-5
}
ic() {  # ic <worktree> <cell> <name> <out-subdir>
  (cd "$1" && uv run scripts/run_integration.py --cell "$2" --host codex --condition plugin \
    --model gpt-6.2-sol --name "$3" --out "$IO/$4" --clear-scratch)
}
S12="$FX/da-ruled-out-prompts/da-s12.txt"; X12="$FX/da-ruled-out/s12-partition-loss"
S13="$FX/da-ruled-out-prompts/da-s13.txt"; X13="$FX/da-ruled-out/s13-zero-events"
```

How each was traced against the harness code at `BASE` plus § G:

- `run_arm.py`: `REPO` is the script's checkout (`$W`), so `--skill-ref` resolves `BASE` or `C114` through `git archive` in the shared object store and stages `skills/decision-analysis/` minus `tests/`, then `instruments/check_record.py` from the same ref (`stage_skill`, `stage_instruments`).
  `--fixture` is copied to `<staging>/data/<fixture dir name>` and `{FIXTURE_PATH}` in the prompt file becomes that path, so the `$K` worktree path never reaches the arm.
  The staging directory is `arm-<name>-*`, and the prompt names paths inside it, so the `--name` reaches the prompt: names are therefore condition-free (`w2-…`).
  The arm's scratch directory `<staging>/work/` is copied to `$DAO/<name>.scratch/`, and the manifest records the model, Claude Code version, skill ref and per-file digests, instrument digests, fixture digests, prompt hash, tool calls, contamination hits, usage, and the final message.
  It refuses to overwrite an existing `<name>.jsonl`, so a replacement takes a new name.
- `run_integration.py`: `REPO` is the checkout it runs in, so `ic "$W" …` builds the plugin from `M` and `ic "$N" …` from the treatment commit, each with `scripts/build-release-tree.py` after refusing a dirty plugin tree; `--out` is absolute, so both conditions archive under `$IO` in `$W`, outside the plugin paths that check reads.
  I-cells run in a fresh `int-arm-*` workspace (since #128) with a relative `data/` path, in a fresh `CODEX_HOME` holding only `auth.json`, with the plugin installed by `codex plugin marketplace add` and `codex plugin add`; `--model` becomes `-m gpt-6.2-sol`.
  The `--dry-run` probe above ran on 2026-11-25 at this file's commit and printed the prompt hashes in § Pinned inputs; it printed an absolute data path there, because #128 is not yet in that commit, which is why the probe is a gate.

### Run order and arm names

The key below is fixed here; it lives only in this file and the archive, never in a staged path.
Stage B's order is `random.Random(20261125).shuffle(sorted(slots))` and stage C's `random.Random(20261126).shuffle(sorted(slots))`, slots being `(cell, condition, replicate)`; names number the order.

Stage A (canaries, candidate text, unscored), in this order:

```sh
da w2-a01 "$C114" "$S12" "$X12"
da w2-a02 "$C114" "$S13" "$X13"
ic "$N" I2 w2-a03 canaries
ic "$N" I4 w2-a04 canaries
```

Stage B (#114), in this order (`BASE` is the current text, `C114` the candidate):

```sh
da w2-b01 "$C114" "$S12" "$X12"   # DA-S12 candidate 1
da w2-b02 "$BASE" "$S12" "$X12"   # DA-S12 current 2
da w2-b03 "$C114" "$S13" "$X13"   # DA-S13 candidate 3
da w2-b04 "$BASE" "$S13" "$X13"   # DA-S13 current 1
da w2-b05 "$BASE" "$P10" "$F10"   # DA-S10 current 1
da w2-b06 "$C114" "$S13" "$X13"   # DA-S13 candidate 2
da w2-b07 "$C114" "$S12" "$X12"   # DA-S12 candidate 3
da w2-b08 "$BASE" "$S13" "$X13"   # DA-S13 current 2
da w2-b09 "$C114" "$S12" "$X12"   # DA-S12 candidate 2
da w2-b10 "$C114" "$S13" "$X13"   # DA-S13 candidate 1
da w2-b11 "$BASE" "$S12" "$X12"   # DA-S12 current 3
da w2-b12 "$BASE" "$S12" "$X12"   # DA-S12 current 1
da w2-b13 "$C114" "$P10" "$F10"   # DA-S10 candidate 1
da w2-b14 "$BASE" "$S13" "$X13"   # DA-S13 current 3
```

Stage C (#119), in this order (`$W` is the current text, `$N` the candidate):

```sh
ic "$W" I2 w2-c01 arms   # I2 current 1
ic "$W" I4 w2-c02 arms   # I4 current 2
ic "$W" I4 w2-c03 arms   # I4 current 1
ic "$N" I4 w2-c04 arms   # I4 candidate 1
ic "$N" I4 w2-c05 arms   # I4 candidate 3
ic "$W" I2 w2-c06 arms   # I2 current 3
ic "$N" I2 w2-c07 arms   # I2 candidate 3
ic "$W" I2 w2-c08 arms   # I2 current 2
ic "$N" I2 w2-c09 arms   # I2 candidate 2
ic "$N" I2 w2-c10 arms   # I2 candidate 1
ic "$W" I4 w2-c11 arms   # I4 current 3
ic "$N" I4 w2-c12 arms   # I4 candidate 2
```

A replacement reruns its slot's exact command with `-r` appended to the name, at the end of its stage.

## E. Cells and arm counts

| Stage | Cell | Host | Current | Candidate | Canary | Scored arms |
| --- | --- | --- | --- | --- | --- | --- |
| A | DA-S12, DA-S13 | Claude Code | — | — | 2 | 0 |
| A | I2, I4 | Codex | — | — | 2 | 0 |
| B | DA-S12 | Claude Code | 3 | 3 | | 6 |
| B | DA-S13 | Claude Code | 3 | 3 | | 6 |
| B | DA-S10 control | Claude Code | 1 | 1 | | 2 |
| C | I2 | Codex | 3 | 3 | | 6 |
| C | I4 | Codex | 3 | 3 | | 6 |
| | replacement reserve | | | | | A 1, B 2, C 2 |

Planned: 4 canaries + 26 scored = 30 arms; with the full reserve, at most 35, under the cap of 36.
Blind-scoring calls: 2 (one per scored stage), at the cap of 2.

Not run, with what each would have added:

- One no-skill baseline per DA cell (2 arms): the catalog's "baseline expectation" assertions; no § B row needs them.
- n=3 on the DA-S10 control (4 more arms): a one-arm regression on the control would become readable; at n=1 the control catches a gross regression only.
- X1 on Codex as a #119 ceiling control (6 arms): § A finds no row that needs it.
- The uncovered branches (§ A), at 7 arms each.

## F. Scoring columns

Scored per arm from the archived transcript, final message, workspace and scratch copies, and manifest.
"Result" means a tool output containing a value computed from the task's data, as `docs/evidence/integration/representative-v1/prereg.md` § Scoring defines it; a skill load is as that section defines it, confirmed by hand.

### #114 columns (DA-S12, DA-S13, DA-S10)

Each record is run through both checkers at `C114`: `uv run "$K/skills/decision-analysis/tests/check_decision.py" <record>` and `python3 "$K/instruments/check_record.py" --final <record>`; current arms' records are also run through both at `BASE`, reported and not scored.
"The record" is the file in `<name>.scratch/` whose headings follow the decision-record template; if there are several, the last one written.

- **RT route.** `decide` when a decision record file was written; `adjudicate` when the response hands to `hypothesis-driven-analysis`; otherwise the route the response states, or `none`.
- **O1 correct handoff (DA-S12).** Pass: RT is `adjudicate`, the handoff is in the same response, and the response gives no probability or likelihood ratio for H and no unconditional recommendation.
  Fail: RT is `adjudicate` and any of those is missing.
  `n/a`: RT is not `adjudicate`.
- **O2 correct one-state recommendation (DA-S12; final message).** Pass: the final message recommends keeping build 412 with a hotfix; gives as its reason that the evidence rules out the job having touched the partition in the window (the partition was local-only, the job acts only where it executes, and it did not execute on db-03); compares the two actions by their losses in that surviving state (roll back 4, hotfix 1, or their difference); and presents no invented positive ratio or probability for H.
  Fail otherwise, including rolling back, returning the choice to the owner, or an unconditional answer without that reason.
- **O3 resolved form (DA-S12).** Pass: the record's verdict line is `- Verdict: resolved`, both checkers at `C114` exit 0, and catalog assertions S12.3–S12.6 pass.
  Fail otherwise.
  A current arm fails O3 by construction.
- **S12.1–S12.6, S13.1–S13.4, S10.1–S10.4.** Each checkbox assertion of the cell in `skills/decision-analysis/tests/scenarios.md` as written at `C114` (DA-S10's is unchanged from `BASE`), in order, excluding each "Baseline expectation" line; pass or fail as the assertion reads.
- **CW causal wording (DA-S12; final message).** Pass: no named cause of the loss (the disk fault included) is stated as established; saying the job did not touch the partition passes.
  Fail: a cause is asserted as established.
- **FE no false elimination (DA-S13, DA-S10).** Pass: no record or answer states a likelihood ratio of 0 or an unbounded ratio, says the defect (DA-S13) or the regression (DA-S10) is ruled out, or carries `- Verdict: resolved`.
  Fail otherwise.
- **A action (final message).** DA-S13: keep piloting; DA-S10: ship now.
  Pass when the final message recommends that action; fail otherwise.
- **K both checkers (DA-S13, DA-S10).** Both checkers at `C114` exit 0 on the record, in the ordinary shape; reported beside S13 and S10.1, which already require `check_decision.py`.

Arm-level criteria used by § B: a DA-S13 arm passes when S13.1–S13.4 and FE pass; the DA-S10 arm is compared assertion by assertion.

### #119 columns (I2, I4)

One set of record columns per record the **observed** route requires, in the form its subroute requires (the forms as `docs/evidence/integration/representative-v1/prereg.md` § Scoring, column "Record written", recognizes them: `instruments/check_record.py` at `M` recognizing the kind, exit 0 or 1, for a form with a validator signature; the fields SKILL.md names, for one without).
A record is looked for in `<name>.workspace/` and in `<name>.scratch/`, whose original absolute paths the manifest's `scratch_files` maps.
Records owed under the designed route and missed because that route was skipped are counted separately, per cell and condition, and enter no column below.

- **R1 record created.** Pass: a file of that form was created or updated during the arm, in the workspace or in captured scratch.
  Fail: no such file, including a record that appears only in the final message or a memo that is not in the form.
  `n/a`: the owning skill was not loaded.
- **R2 route-specific timing.** One per R1 pass.
  Pass: the tool call that first creates the file precedes the first result computed after the owning skill's first load.
  Per owning route that boundary is: exploration log, the first look result after the `exploratory-data-analysis` load; full ledger, the first result after the `hypothesis-driven-analysis` load (EDA results before it do not count against it); mini ledger or estimation record, the first estimate after that load; identification review, the first probe or estimate result after the `causal-identification-review` load; decision record, the first posterior, ratio, or verdict computation after the `decision-analysis` load.
  Fail: it follows that result.
  `n/a`: R1 is fail or `n/a`.
  Later edits do not change it.
- **R3 present and openable at the named path at end of turn.** One per R1 pass.
  Pass: an entry in the manifest's `named_paths` that the scorer matches to this record resolves to a regular file (`exists`), the harness user could read it (`readable`), and its `sha256` equals the digest of the record's final archived bytes (the workspace copy, or the `scratch_files` entry).
  Fail: the named path does not exist, is unreadable, or holds other bytes.
  `n/a`: R4 is fail or `n/a`.
- **R4 pointer in the final message.** One per R1 pass.
  Pass: the final message names a path (absolute, or relative to the arm's working directory) that is meant to locate this record.
  Fail: it names none, or names only a summary of the record.
  `n/a`: R1 is fail or `n/a`.
- **R5 workspace retention.** One per R1 pass, descriptive and outside every verdict: the record is in `<name>.workspace/` at the end.
  This keeps the historical `retained` label comparable; a record kept in scratch is not failed for it.
- **R6 delivery limitation stated.** Per arm, descriptive: the final message says some record cannot stay open to the user after the turn.
  In this harness every writable location persists after the turn, so the limitation branch's correct use is not reachable here; an R6 statement with an R3-passing path available is reported as an unneeded limitation, and an R4 pass with R3 fail and no R6 is a **false delivery** (§ B row 5).
- **E and C.** As `docs/evidence/integration/2026-11-17-full-catalog/prereg.md` § Scoring defines them for I2 and I4, from the final message only.

### Blind scoring

Blind-scored, and only these: the final-message answer columns used as controls, O2, CW, and A on the 14 stage B arms (one call), and E and C on the 12 stage C arms (one call).
Every other column is scored by the primary scorer, unblinded, from the original archive, never from a bundle; delivery columns (R1–R6) and O3 are among them.
Primary: the dispatching session, named on the results' `Scorer:` line as PROTOCOL § Who scored it requires.
Blind: `openrouter/google/gemini-3.1-pro-preview` through amicus (harness `pi`, reasoning effort high), a model that runs no arm, given only the bundle and the column definitions.
Primary scores are committed before either blind result is fetched; disagreements are reported, not reconciled.

How each bundle is built, so that it does not reveal the condition (the lesson of `docs/evidence/integration/representative-v1/forced-load/scores-blind.md`, whose first bundle replaced names with placeholders and left the sentences around them):

1.
   Take each scored arm's final message from its archive, shuffle by `random.Random(20261127)` (stage B) or `random.Random(20261128)` (stage C), and label them `B01`… or `C01`…; the key goes in `blind-key.json` beside the bundle.
2.
   Delete every sentence that names a skill, a route, a verdict label, a record or record block, a template, a validator or checker, or a file path, when no answer rubric needs that sentence; a pointer line ("the ledger is at …") is such a sentence.
3.
   In a sentence a rubric needs (the recommended action, its reason, the loss comparison, a computed number, E's and C's facts), delete only the naming words, and keep the rest.
4.
   Audit before sending: grep the bundle, case-insensitively, for the skill names, `skill`, `route`, `decide`, `adjudicate`, `resolved`, `robust`, `verdict`, `record`, `ledger`, `log`, `review`, `memo`, `Resolution`, `surviving`, `excluded state`, `template`, `check_record`, `check_decision`, `validator`, `scratch`, `workspace`, `/tmp`, `/var/`, and `.md`; first confirm the same grep finds hits in the unredacted final messages, so a clean result means something; then require zero hits in the bundle.
   Then read each item and ask whether anything left (a heading structure, a phrase such as "outside the odds form" or "eliminated", a sentence about where something was saved) could tell the condition; remove it by rule 2 or 3.
5.
   Commit the bundle with an audit note listing, per bundle label, how many sentences were removed and confirming none bears on a blind-scored column.
   If a cue is found after a blind call, no third call is made: that stage's blind result is reported as compromised, and the primary scores stand alone with that limit.

## G. What the harness captures, and the change made for it

Before this wave `scripts/run_integration.py` copied workspace files only for representative cells, and nothing outside the workspace; an I-cell arm's `/tmp` records were not archived, and nothing checked a named path from outside the arm.
This branch adds, with tests in `scripts/test_run_integration.py`:

- Workspace archive for every cell, I1–I4 included, into `<name>.workspace/`, against the staged fixture's digests.
- Scratch capture after the turn: files under a system temp directory (`/tmp` and the platform temp directory), outside the workspace and the harness's own `int-plugin-*` and `int-codex-home-*` directories, that a tool request, a tool output, or the final message names, or that sit under a named directory, written after the arm started.
  Tool output is searched because a `mktemp -d` directory is often known only from what the command printed (`I4-codex-plugin-3` in the 2026-11-17 archive is the test's model).
  Each is copied to `<name>.scratch/<its absolute path>` and mapped in the manifest's `scratch_files` with its SHA-256 and whether its top-level temp entry existed before the arm (`top_entry_preexisted`).
- The named-path check, from outside the arm after the turn: every file path the final message names, resolved against the arm's working directory, with `exists`, `readable` (`os.access`), and its SHA-256, in the manifest's `named_paths`.
  It runs before any clearing.
- `--clear-scratch`, which removes the archived scratch originals and the directories they leave empty, so a later arm cannot read or append to them.

The capture was checked against known positives before the tests were written: on the archived `I4-codex-plugin-3`, `I2-codex-plugin-2`, and `I4-codex-plugin-2` transcripts it finds the `/tmp` directories and files decision 010 lists, and the named-path extraction returns exactly the paths each final message names.
`run_arm.py` needs no change for this wave: it already archives its scratch directory with digests, and #114 scores no delivery column.
`scripts/run_integration.py` is a frozen input of the representative preregistration, so `docs/evidence/integration/representative-v1/prereg.md` carries a dated note for this change.

## H. Invalid executions, replacements, staged spend, and the stop rule

An invalid execution is not a failing answer; it is not scored, and its slot takes one replacement from its stage's reserve.

`run_arm.py` arms (stages A and B) are invalid when any of these holds:

- the manifest's `exit_code` is not 0, or `result_text` is null (no terminal result);
- the resolved `model` is not `claude-sonnet-5-5`, or `claude_version` differs from the version in the dated note;
- `contaminated` is non-empty;
- any tool call's path names a file under the staged skill's `decisions/` directory (grep the manifest's `tool_uses` for `decision-analysis/decisions/`);
- the staged `skill_files_sha256` or `instruments_sha256` differs from another arm of the same condition.

`run_integration.py` arms (stages A and C) are invalid when any of these holds:

- the manifest's `status` is not `completed`;
- the resolved `model` is not `gpt-6.2-sol`, or `host_version` differs from the dated note;
- the plugin install failed (`<name>.install.log` shows a nonzero exit, or no manifest was written);
- a tool request names the main checkout or any `w2-*` worktree path;
- a captured scratch file flagged `top_entry_preexisted` was read or appended to by the arm and was written by an earlier arm.

`data_modified` set only by an interpreter cache is not invalid, as the representative suite ruled.

Reserve: 1 replacement in stage A, 2 in B, 2 in C, one per slot; a slot still invalid after its replacement, or beyond the reserve, leaves its cell incomplete (§ B row 2).

Stages run in order, and a stage that fails its gate stops the batch: no later stage runs, and the owner decides.

- **Stage A gate (canaries, unscored, excluded from every scored artifact).** All four canaries are valid executions, and each is informative:
  - `w2-a01` (DA-S12) engages the exclusion: its record or answer addresses the structural exclusion, whether by a resolved record, a one-state recommendation, or a handoff that names the exclusion; an arm that never mentions why the job could not have touched the partition is entangled;
  - `w2-a02` (DA-S13) computes the likelihood ratio from the two sourced rates and n = 100, or says the zero count does not eliminate the defect;
  - for both I-cell canaries, the capture is checked by hand: every file the transcript shows the arm writing, in the workspace or a temp directory, is in `workspace_files` or `scratch_files` with its archived bytes, and every file path the final message names is in `named_paths`;
  - `w2-a03` (I2) also created at least one record file (every archived Codex I2 plugin arm did); `w2-a04` (I4) is not required to, since one of three archived I4 arms created none.
  An entangled DA canary sends its packet back to design (PROTOCOL steps 2 and 4).
- **Stage B gate.** Every slot ends valid within the reserve, and no checker defect is left unfixed; the stage's primary scores are committed.
  The gate is about the measurement working, not the candidate passing: a #114 result in any row of § B does not stop stage C.
- **Stage C gate.** As stage B, for the capture instead of the checkers.

Spend, if the batch runs to the end: 30 arms planned, at most 35 with every replacement, and 2 blind calls.
Claude Code arms (stages A and B: 16, at most 19 with replacements) have cost $0.37 median on DA cells (`skills/decision-analysis/tests/runs/artifacts/2026-11-09-evidence-sweep/` manifests, 21 skill arms, maximum $0.40), about $6 planned and at most $7.60; at the suite's earlier $0.30–$0.35 it would be $4.80–$6.65.
Codex arms (stages A and C: 14, at most 16) draw on quota and report no price.
The two blind calls run through OpenRouter at a cost of the order of the earlier suites' calls.
Wall-clock: DA arms ran a median 66 s (maximum 112 s) and Codex I2 and I4 arms 100–197 s in the 2026-11-17 archive, plus a plugin build and install per Codex arm; stage A about 10 minutes, stage B about 20 minutes, stage C about 40 minutes, so about 75 minutes of arms run serially, with scoring, bundling, and the blind calls after.

## I. Limits fixed in advance, and where results go

- One model per host, n=3 per condition; every label is directional and reported with counts.
- #114 is measured on Claude Code only (the single-skill harness is Claude Code only), and #119 on Codex only (the only host whose archived plugin arms left records in scratch); each is unmeasured on the other host.
- `run_arm.py`'s frame tells a #114 arm where to write working files; that is the same in both conditions and is why #114 scores no delivery column.
- The two candidates are measured apart: #114 against `BASE`'s Record Delivery and #119 against `BASE`'s decision-analysis text, so their combination is unmeasured.
- On this harness every writable path persists after the turn, so R3 measures openability on the user's own machine; a hosted runner that tears its workspace down is the uncovered runner-only branch.
- A Codex route read from file reads is an upper bound on what was followed (the full-catalog limit); records are the stronger evidence.
- Synthetic packets test whether a set trap is handled, not how often users meet it.
- Removing sentences conceals what an answer says about its procedure, not how it is written; a blind scorer could still learn a condition's style.

Where results are recorded:

- #114: arms, canaries, primary scores, the blind bundle, its key and audit note, and blind scores under `skills/decision-analysis/tests/runs/artifacts/2026-11-wave2-resolved/`; the run record as `skills/decision-analysis/tests/runs/<run date>-da-s12-da-s13-resolved.md`, with its `Scorer:` line, by the DA catalog's convention.
- #119: arms under `arms/` and canaries under `canaries/` beside this file, with `scores-primary.md`, `blind-bundle.md`, `blind-key.json`, `scores-blind.md`, and `results.md`.
- Each result's row in `docs/evidence-status.md`, and the debt rows of § B.
- The DA catalog's status lines for DA-S12 and DA-S13 (they exist only on the #114 branch, so the status lands there after the rebase, or in the closing note if #114 does not ship), and dated notes on `skills/decision-analysis/decisions/008-ruled-out-state.md` and `skills/hypothesis-driven-analysis/decisions/010-owed-records-on-a-multi-skill-decision-request.md` stating which § B row governed.
- Nothing under any `tests/runs/` directory existing before the run is edited; the run only adds files.

## Before any arm (PROTOCOL steps 3–5)

- The cross-model design review of this file, the candidate wording, and the fixtures together is one call against the pull request that carries this file; its findings are fixed here by dated notes before stage A.
- Every wording review of both candidates (cross-model, prose, mechanical gates) is finished against the pinned SHAs before stage A; a wording change after that moves a pin only by the rebase rule above, and a change to measured prose voids that candidate's arms.
- The canaries are rationale canaries (stage A's gate), excluded from every scored artifact.
- No arm runs without the owner's explicit go-ahead on the count and cap in § E and § H.

## Notes after writing

None yet.
