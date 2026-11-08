# Preregistration: 2026-11-08 binding-rules hoist (issue #66, step 1)

Written before the SKILL.md edit and before any arm ran.
This wave measures one agent-read change to `../../../SKILL.md`: the binding sentences of `### Conclusion` move verbatim into a new `## Binding rules` section placed after the intro paragraph and before `## Routing`, and § Conclusion keeps one pointer sentence per moved group.
The purpose is that the rules sit inside the first 5,000 tokens of the file, which is what Claude Code re-attaches of an invoked skill after compaction.
It is the `../../PROTOCOL.md` step 1 artifact; steps 2 (entanglement), 3 (design review), and 4 (canaries) are recorded here too.
Step 0: the premise is arithmetic, not an archive claim, and it holds on the pre-edit file — `### Conclusion` begins at o200k_base token 6,393 of 8,460, so none of the moved sentences is in a 5,000-token prefix (measured with `2026-11-08-binding-rules-hoist/prefix_tokens.py`, below).

Scorer: the dispatching session (Claude Opus 5.5, Claude Code), unblinded: it wrote this preregistration and the edit.

## Inputs, pinned

Pre-edit tree: `dev` at `692fd31` (`git rev-parse` of `origin/dev` when this branch was cut).

| File | sha256 (pre) |
| --- | --- |
| `skills/hypothesis-driven-analysis/SKILL.md` | `858f9f422ab89c6c723ca34296a2a544d396e302efa559aa6ec019192142e76c` |
| `skills/hypothesis-driven-analysis/references/ledger-template.md` | `3ceda09c912b5636bf63f4104a6048abb7b3a22c2a5b4423cfe53a8c7fdb71b5` |
| `skills/hypothesis-driven-analysis/references/subagent-briefs.md` | `3cda9ff7e28fe11cfd41c230b5f1d938393cbb4d5b6ce48e611cbf27159ce3cb` |
| `skills/causal-identification-review/SKILL.md` | `1da57d11946eee084818abb16a04d76d9b24836acbe12cc58e909bfc355cb55c` |
| `skills/decision-analysis/SKILL.md` | `38ccdaf3e82726a97d08bcbb168829942a67994ecb1afc9bbb8b000153596054` |
| pre SKILL.md cut to its first 5,000 o200k_base tokens (`2026-11-08-binding-rules-hoist/pre-SKILL.prefix5000.md`, 24,470 bytes, ends mid-sentence in § Analysis) | `f1fd98190302d1102a6fa09192afe987b3812cac3b2a70cb656009128a91a8be` |

Scenario prompt files (the text `run_arm.py` substitutes into its frame; `{FIXTURE_PATH}` becomes the staged path, so each arm's full-prompt hash differs and is recorded in its manifest):

| Prompt file (`2026-11-08-binding-rules-hoist/prompts/`) | sha256 |
| --- | --- |
| `s1.txt` (byte-identical to the record-delivery wave's) | `969f5f3d429badea4506fd61ed73446dad258d9d1f5049529d9d0cd29bf12a64` |
| `s11.txt` (byte-identical to the record-delivery wave's) | `a4d383ae097436f3be3ac00f8da6c93f6aa545d2ab8940a390cc96e0d69409f9` |
| `s9.txt` (byte-identical to the 2026-09-15 remediation wave's) | `df027af372dfb009d42c684f136d6f337abdba31b72d8b49f446e743fea728d0` |
| `s12.txt` (catalog prompt, path substituted) | `0a33f736a2531d7b1fb087ed7bf310637a8ff88122e00231ef9f18ac334087b3` |
| `s15.txt` (catalog prompt, one sentence per line, path substituted) | `1b03aade79a220e8e5f73a39260c7552b281f1c1bad63fb381a93b2aa4c2ae9e` |
| `s21-refute.txt` (d1, d3, d5) | `360a014b853ae412975b065f70fccc84a4221090bc495c3385d085b9c5d1b94d` |
| `s21-support.txt` (d6, d7) | `027e171f84a83fb3890e796b9bbac203e36fb76deafeb04a575c6168b4d4a2e8` |

The S21 prompts carry the 2026-07-25 templates' task and output contract with two changes forced by the harness: the skill path comes from `run_arm.py`'s frame rather than a `{SKILL_MD}` slot, and the answer goes to the arm's scratch directory.
The 2026-07-25 S21 arms therefore are not a baseline for these; pre and post here share one frame.

Fixtures are the catalog's own, unchanged (`s1-conversion`, `s9-ab/signups.csv`, `s11-mini`, `s15-assist-rollout`, `s21-status-disposition/d*.md`); every arm's manifest records their sha256s, and the scorer checks them against the committed bytes.

Instruments archived beside this file: `prefix_tokens.py` (sha256 `39b912c51bc9c8bcea4ac1a8b7bc2b72a809d60bb917df57331932c95b7c7a31`; tiktoken 0.14.0, `o200k_base`) and `hoist.py` (sha256 `1393881e9ef98b60d111076b31e22928cc6832af68cfe8ee046f76197a44d1a0`), the edit as a program: it moves lines by exact match, so the moved sentences are byte-identical by construction, and its `check` mode re-verifies that every moved line occurs exactly once, inside § Binding rules, and that each pointer occurs once in § Conclusion.
`../../run_arm.py` gains `--skill-md`, which swaps the staged SKILL.md for another file and records that file's path and sha256 in the manifest; it is used only by the approximation arms.

## The change, exactly

What moves (in this order, byte-identical, into § Binding rules), and the pointer each group leaves in § Conclusion:

| Group | Sentences moved (handles; the bytes are the pre file's) | Pointer left in § Conclusion |
| --- | --- | --- |
| G1 status set and derivation | B1 "Derive hypothesis status from the latest effective outcome…"; B2 "The status set is closed…"; B3 "\"Necessary\" is not decided at conclusion time…" | `Status derivation and the closed status set are stated in § Binding rules.` |
| G2 precedence | B4 "Precedence when tests disagree:" and its three bullets B5–B7 | `Precedence when tests disagree is stated in § Binding rules.` |
| G3 data-artifact rule | B8 "A data-artifact hypothesis is never `REFUTED` on a validity check…" | ``The rule for refuting a `data-artifact` hypothesis is stated in § Binding rules.`` |
| G4 `SUPPORTED` bar and summary table | B9 "`SUPPORTED` is not a status…"; B10 "The per-hypothesis summary table repeats…" | `The "best supported" bar and the summary-table rule are stated in § Binding rules.` |
| G5 stop rule | B11 "Apply the precommitted stop rule:"; bullets B12 Conclude, B13 Iterate, B14 Stop with limits; continuations B15 (`causal-identification-review`) and B16 (`decision-analysis`) | `Apply the precommitted stop rule stated in § Binding rules.` |
| G6 causal wording | B17 "Use causal wording only when…" through B21 "…associative language is mandatory and the limitations name which of those threats remain open." | `Causal wording is governed by the bar stated in § Binding rules.` |
| G7 numeric confidence | B22 "Do not invent numeric confidence values."; B23 "A `decision-analysis` record's provenance-classed numbers…" | `The numeric-confidence rule is stated in § Binding rules.` |
| G8 report order | B24 "Report the answer first, then the per-hypothesis evidence summary…" | `Report in the order § Binding rules states.` |

Everything else in § Conclusion stays where it is: "A prediction that merely *would be nice*…", the unidentified-contrast and independent-evidence sentences, the descriptive-row sentence, the falsifiability and variant-scope paragraphs, the retrospective-evidence sentences, "If two explanations both clear the bar…", the residual sentence, and "Multiple contributing explanations are allowed…".
The retrospective sentence's "that bar" now resolves to the G4 pointer, which names the bar.

New prose, all of it: the heading `## Binding rules`, one scope sentence under it — `These rules bind every full-route conclusion; § Conclusion applies them.` — and the eight pointers above.
The scope sentence exists because position used to scope these rules to the full route (they sat under `## The Loop (full route)`); placed ahead of `## Routing`, they would otherwise read as binding the `direct`, `mini`, and `estimation` routes, which they did not before.

Cross-references updated in the same change (PROTOCOL § What owes a rerun: a cross-reference owes nothing):

- SKILL.md § Plan, "(see Conclusion)" after the `associative` claim-class sentence becomes "(see § Binding rules)"; the causal-wording bar it points at moves.
- `references/ledger-template.md`, the sentence placing the status rules "in SKILL.md's Conclusion section" names § Binding rules and § Conclusion, since the status set moves and the class-specific refutation rules (causal, descriptive) stay.
- `skills/causal-identification-review/SKILL.md` and `skills/decision-analysis/SKILL.md` point at HDA's causal-wording bar as "§ Conclusion"; both become "§ Binding rules".
- `decisions/005-status-under-an-unverified-return.md` § Where the rule lives names "the Conclusion section's closed status set"; it gets a dated note, not a rewrite.

Post-edit digests are recorded in the wave record after the edit, which is the only time they can be known.

## Retained prefix (measured on a scratch copy of the edit before this commit)

Tokenizer: tiktoken `o200k_base`; bytes/4 printed beside it as a second proxy.
Claude's own tokenizer is not available offline, and Claude Code's re-attachment measure is not documented to be either of these; both numbers are estimates, and the offsets are reported with their margin rather than as a pass.

| Point in the file | pre o200k_base | pre bytes/4 | post (scratch) o200k_base | post (scratch) bytes/4 |
| --- | --- | --- | --- | --- |
| end of the last moved sentence (end of § Binding rules in post; end of § Conclusion in pre) | 7,903 | 9,757 | 1,350 | 1,651 |
| end of the rendered authorization gate | 2,924 | 3,533 | 3,764 | 4,566 |
| whole file | 8,460 | 10,449 | 8,588 | 10,607 |

Both post offsets are under 5,000 on both proxies; the gate's margin is 1,236 o200k_base tokens and 434 bytes/4 units.
The edit pushes the gate 840 o200k_base tokens later; that is the cost of the hoist and the reason the budget is the whole retained prefix.

## Which cells reach the change

Reachability is read from the fixtures, the catalog prompts, and the prose, per PROTOCOL § What owes a rerun.
"Reaches G*n*" means the cell's scored decision point traverses a sentence of that group.
"Position" means the cell's route never reached § Conclusion before, but every activating arm now reads the moved sentences and the scope sentence before it routes, so the risk is scope bleed rather than a changed rule.
No cell's prompt contract requires quoting from a named section: S20 and S21 require verbatim quotation from SKILL.md, which a verbatim move preserves; archived S20/S21 arms label quotes "(Conclusion)" of their own accord, which is not scored.

| Cell | Reaches | Basis | Paid here |
| --- | --- | --- | --- |
| S1 | G1–G8 | full route; assertion 5 is G4 + G6; the 2026-07-16 arm marked the mobile-undercount row `REFUTED` on a schema-only check, which is G3 | yes, n=3 |
| S2 | position | routes `direct` | no — debt (S11, S9 stand in) |
| S3 | none | the skill does not activate | no |
| S4 | G1, G4, G5, G6, G8 | full route; production unauthorized forces Stop with limits; assertions are about authorization, whose rendered gate moves 840 tokens later | no — debt |
| S5 | G4 (with the retrospective sentence, which stays) | scenario invalid as written | no — unpayable |
| S6 | G1, G5 (B14), G6, G8 | "can't tell from this data"; cluster attribution is causal wording | no — debt |
| S7 | as S1 | S1's investigation, fan-out | no — debt |
| S8 | G1, G4, G6, G8 | assertion 3 "best-supported, not proven" | no — debt |
| S9 | position; G6 as read by an estimation arm on a randomized design | routes `estimation`; the counterfactual bar is met by randomization, so a correct arm may use causal wording | yes, control, n=2 |
| S10 | G1, G4, G8 | `REFUTED` on necessary predictions | no — debt (metered CLI; prompt path under `tests/`) |
| S11 | position | routes `mini` | yes, control, n=2 |
| S12 | G1, G4, G5 (B15), G6, G8 | causal question with no identifying design | yes, n=3 |
| S13, S14, S17, S22a–d | position | `mini` / `direct` | no — debt |
| S15 | G1, G4, G5 (B14–B16; assertion 8 is the stop rule), G6, G7, G8 | decision memo on an unidentified rollout | yes, n=3 |
| S16 | G1, G4, G5, G8 | H2 `UNRESOLVED`, H1/H3 `REFUTED`, re-collection recommended | no — debt |
| S18 | as S1 | composition | no — debt |
| S19 | G1, G4 (B9 is assertion 2's "stated bar"), G5 | crash leaves T2 untested | no — debt |
| S20 c1–c4 | G1, at an unscored output | the prompt asks for H2's status, which the catalog deliberately does not assert | no — debt |
| S21 d1, d3, d5 | G1 (B1, B2), G2 (B5) | refute side: the arm derives status | yes, n=3 each |
| S21 d6, d7 | G1, G4 (B9) | support side: best-supported bar is live | yes, n=3 each |
| S21 d4 | G1, G2 | refute side, immaterial deviation | no — debt |
| CIR, DA, EDA cells | none | each stages its own skill only; their SKILL.md edits are cross-references | no |

The debt rows keep this change from being called measured across the catalog.

## Arms

- **pre** — `--skill-ref 692fd31`.
- **post** — `--skill-ref <the edit commit>`, named in the wave record.
- **pre-trunc** — `--skill-ref 692fd31 --skill-md pre-SKILL.prefix5000.md`.
- **post-trunc** — `--skill-ref <the edit commit> --skill-md post-SKILL.prefix5000.md`, cut by `prefix_tokens.py cut` from the committed post file; its sha256 goes in the wave record.

No baseline arm: the question is whether moving the text changes behavior, which is pre against post; every cell here has run against a no-skill baseline before.
Model `sonnet` (resolved model recorded per arm), Claude Code 2.1.319, default tools, one validator staged in every arm by `run_arm.py`.
Arms run concurrently on per-arm staged copies.

### The approximation arms — prefix-only robustness, not Claude Code compaction

Pre-trunc and post-trunc arms run on S21 d1, S21 d6, and S1, n=2 each; d6 is informational (see Assertions).
They hand the agent only the first 5,000 o200k_base tokens of SKILL.md, with nothing else from the session and no way to reopen the full file.
Claude Code's compaction differs in every one of those respects: it also carries a conversation summary, shares a 25,000-token budget across re-attached skills, uses its own token measure, and leaves the agent free to reopen the file.
These arms test whether the rules are present and followed when only the prefix is present; they do not test compaction, and nothing in the wave record may say they do.

## Order of work

1. Commit this preregistration (with `prompts/`, the instruments, and the pre prefix) before any edit or arm.
2. Run the **pre-trunc** arms (6), which need only the pre file, and score them — the "unnecessary" gate below can fire here, before the change exists.
3. Make the edit with `hoist.py` plus the cross-references; run `hoist.py check`, `scripts/check-shared-sections.py`, the description freeze, and the citation checker; measure the offsets on the committed file; commit.
4. Canaries: one post arm per paid cell (10) and one post-trunc arm per approximation cell (3), excluded from the scored artifact.
5. Scored batch: pre and post on every paid cell at the n above; post-trunc on the approximation cells.
6. Score, archive under `2026-11-08-binding-rules-hoist/`, write the wave record.

## Entanglement (step 2)

The fixtures are the catalog's own, and each has run under this skill before, so the standing gates they reach are known and are the same in pre and post: S1's mobile undercount and deploy red herring, S12's and S15's missing identifying design, S15's selection-sensitive missing activity, S21's preregistered Data Validity section closing the null-result sensitivity rule.
None of those gates is in the moved text except the causal-wording bar (G6), which is under test, and the unidentified-contrast rule, which stays in § Conclusion and is read by the same arms in both conditions.
The new entanglement is position: arms that previously never read § Conclusion now read the binding rules before routing, which is what the S11 and S9 controls score.
The truncated arms entangle with everything after the cut: both prefixes lose § Analysis's worker-return rules, so S21 d6's unverified-return rationale is missing in both; d6 is scored on status and best-supported, not on that rationale.

## Assertions

Every assertion is scored on the arm's delivered output (final message, plus the ledger or `answer.md` it wrote), and on rationale, not label alone.
Quotes in the wave record are grepped against the archived transcript or written file before citation.

**S21 (all cells), catalog:** d1 `UNRESOLVED`, rationale the recorded `NON_DISCRIMINATING` outcome; d3 `UNRESOLVED`, rationale the unverified return, not the causal-identification rule; d5 `REFUTED`; d6 `UNRESOLVED` and not best supported, on the unverified-return rationale; d7 `UNRESOLVED` with best supported standing.
**S21.Q (informational, every arm):** each fragment of `GOVERNING SKILL TEXT` of 20 or more characters, after removing backticks and asterisks, splitting on ellipses, and collapsing whitespace, is a substring of the SKILL.md that arm was staged with; and which group (G1–G8, or a sentence outside them) it quotes.

**Full-route cells (S1, S12, S15), binding-rule assertions:**

- **BR.status** (B2, B9, B10): every hypothesis status the ledger's summary and the report assign is `REFUTED` or `UNRESOLVED`; no `SUPPORTED`, `CONFIRMED`, or "best supported" in a status cell; and the summary table's `claim` column repeats each row's Hypotheses-table claim class unchanged (from the Plan-time ledger when the arm archived one, else from the final ledger's Hypotheses table).
- **BR.best** (B9): every "best supported" (or equivalent "leading", "most likely cause") claim names a hypothesis that is not `REFUTED`, has a `CONSISTENT` outcome from a test that discriminates it from the named rivals, and has no unrefuted rival the report itself leaves explaining the same observations equally well.
- **BR.causal** (B17–B21): no unqualified causal claim for an effect no identifying design supports; S12 and S15 state that the design does not identify the effect.
- **BR.conf** (B22): no invented numeric confidence ("85% confident", "probability 0.7 that H2…").
- **BR.order** (B24): the final message gives the answer before the per-hypothesis evidence summary, and the limitations after it.
- **BR.stop** (B11–B14): the report states where the stop rule left the investigation (concluded, or stopped with stated limits), consistent with the ledger.
- **BR.cont (informational):** S12 and S15 name `causal-identification-review` (B15); S15 names `decision-analysis` (B16). Neither skill is installed in the arm, and both sentences say "when installed", so absence is not a failure; the count is compared pre against post.

**Catalog regression properties:**
S1 — names the `/lp/summer-sale` composition shift as best supported, dismisses the deploy on timing, surfaces the mobile undercount or states it as a limitation, and does not mark a `data-artifact` row `REFUTED` on a check that did not probe coverage (G3).
S12 — routes `full`; the campaign is associated with lower blended conversion; the causal campaign hypothesis is `UNRESOLVED`; no effect estimate is reported as identified.
S15 — routes `full`; states the cutover does not identify Assist's effect; `score_ledger.py` C1 passes on the final ledger; attributable responder-hours are not reported as an identified effect.

**Controls (S11, S9):**
S11 — routes `mini`; no hypothesis table and no Sources/Tests/Amendments sections; answers that the claim is false with the measured p95 (≈392ms).
S9 — routes `estimation`; states estimand, population, an uncertainty statement, and a practical threshold; no full ledger.
**BR.bleed:** no hypothesis-status table, no per-hypothesis `REFUTED`/`UNRESOLVED` statuses beyond the mini route's own claim outcome, and no full-route conclusion ceremony; a control arm that adds any of these and cites § Binding rules, its scope sentence, or "binding" rules as the reason is scope bleed.

**Approximation cells:** S21 d1, the catalog assertion (status `UNRESOLVED`, rationale the recorded `NON_DISCRIMINATING` outcome); S1, all of BR.status, BR.best, BR.causal, BR.order, each scored on every arm whether or not another assertion already separates the arms.
S21 d6 is run and reported but is **informational and excluded from rows 4, 8, 8a, and 9**: both prefixes lose the unverified-return rules its correct rationale needs, so a generic conservative `UNRESOLVED` / not-best-supported answer cannot be told apart from application of G4 (design review, finding 3).
S21.Q is reported, not scored, here: a pre-trunc arm cannot quote a G1 sentence because none is in its file, so a quote-based comparison could not fail in the post arm's favor and is not evidence.

## Canaries (step 4)

One post arm per paid cell and one post-trunc arm per approximation cell, named `canary-*`, excluded from the scored tables.
A canary passes as fixture validation when its arm reaches the decision point under test *for the reason under test*, per PROTOCOL step 4: an S21 arm derives the status and its rationale names the status rule or the recorded outcome it reads (for d6/d7, the best-supported bar); a full-route arm writes a ledger whose statuses are derived from recorded outcomes and whose report applies a stop-rule outcome; a control routes for the catalog's reason (S11: a stated claim is adjudicated; S9: randomized assignment, magnitude asked).
A canary that never reaches its decision point, or reaches the right label for a reason outside the moved text, means the cell is entangled or not exercising the text: return to step 2 for that cell, drop or replace it before paying scored arms, and record it.

## Why these n, for this claim

The claim is narrow: a verbatim move does not regress the reached cells, and in a prefix-only file the moved rules are present and followed where the pre prefix's arms fail them.
Non-regression cannot be proven by a small batch; what n=3 per arm can do is catch a regression that hits most arms.
If the move raises a cell's per-arm failure rate from zero to p, the chance that at least one of three post arms fails is 1−(1−p)³ — 0.875 at p=0.5, 0.49 at p=0.2 — and row 7 below turns any single post-only failure into three more pairs before a verdict.
A regression rarer than about one arm in five is below what this batch resolves, and the wave record says so.
The controls are scope-bleed screens at n=2: bleed, if the scope sentence fails, is expected to be systematic rather than rare, since every activating arm reads the section.
The scored approximation cells (S21 d1, S1) are at n=2, with one bounded extension to n=4 under row 8a, because their question is presence, not rate: a pre prefix contains none of the moved sentences, so a difference, if the rules matter, should show on both arms.
No n here is inherited from an earlier wave; the S21 cadence of n=3 is a coincidence of the arithmetic above.

Planned arms: 6 pre-trunc, 13 canaries, 48 pre/post on the six paid full-skill cells' eight cell-conditions (S21 ×5, S1, S12, S15), 8 on the controls, 6 post-trunc: 81, plus any row-7 extensions or row-2 retries.

## Verdicts

| Outcome | Disposition |
| --- | --- |
| 0. A post offset (end of § Binding rules, or end of the rendered gate) is at or over 5,000 on either proxy, measured on the committed file | decline before any post arm: the edit fails its own purpose |
| 1. The owner declines the arm spend | decline; nothing ships (reachable without the change) |
| 2. Infrastructure failure or contamination on an arm | arm void; one fresh retry, recorded |
| 3. A canary never reaches its decision point | cell dropped or replaced before scored arms, recorded |
| 4. **Unnecessary, early:** every pre-trunc arm passes every scored assertion on both scored approximation cells (S21 d1, S1) | the rules' absence from the prefix changed nothing on these cells: decline the hoist without editing (reachable without the change) |
| 5. **Regression:** on any paid cell, post fails a scored assertion on at least two more arms than pre (pooled with any row-7 extension), or any post arm fails one citing § Binding rules, its placement, its scope sentence, or a pointer; or any control arm shows bleed citing them | withdraw; no rewording after the fact — any revision is a new pre/post pair under an amendment to this file |
| 6. A post-only divergence whose rationale cites a rule outside the moved text (the sensitivity rule, the worker-return dispositions, the unidentified-contrast rule) | not attributable to the move; re-scope per PROTOCOL step 2 and rerun that cell before any verdict |
| 7. Exactly one post-only failure on a cell, not citing the new text | three more pre/post pairs on that cell, then apply row 5 to the pooled arms |
| 8. **Unnecessary, late:** no regression, and on every scored approximation cell (S21 d1, S1) each assertion's post-trunc pass count is at most its pre-trunc pass count | the hoist buys no prefix-only robustness on these cells: decline as unnecessary |
| 8a. **Short of a beat:** no regression, row 8 does not fire, row 9 does not fire (post-trunc passes some assertion more often than pre-trunc, but never 2/2 against 0/2) | two more pre-trunc and post-trunc arms on each scored approximation cell, once; then post-trunc *beats* if, pooled at n=4, it passes an assertion on at least three more arms than pre-trunc with no assertion worse by two; a beat ships under row 9, anything else declines as not shown |
| 9. No regression, controls hold, and post-trunc *beats* pre-trunc on at least one scored approximation cell — passes a scored assertion on both arms where pre-trunc fails it on both — with post-trunc no worse by two arms on any assertion of any scored approximation cell | **ship**, claimed as prefix-only robustness on the named cells at n=2 and no regression detected at n=3 on the paid cells; Claude Code's compaction was not exercised, and the CHANGELOG line says so |

Owner decision 3 (2026-11-08) fixes that a ship verdict rests on prefix-only evidence; no native-compaction arm is in this wave.

## Step 3 — cross-model design review

Codex (amicus consult, read-only, job `e71c591b54404adea16a6eef4037d700`, 2026-11-08) reviewed this file, the draft SKILL.md, `hoist.py`, `prefix_tokens.py`, the prompts, and the `run_arm.py` change before any arm ran.
It confirmed the draft matches `hoist.py`'s output, the check passes for every moved line and pointer, and found no meaning change in the scope sentence or pointers and no further instrument defect.
Three findings, all upheld and applied above before this file was first committed:

1. *A mixed prefix improvement had no verdict* (one pre-trunc arm passing, both post-trunc passing: rows 4, 8, and 9 all silent). Fixed by defining *beat* in row 9, restating row 8 on pass counts, and adding row 8a, a single bounded extension that ends in ship or decline.
2. *BR.best and BR.status omitted parts of B9 and B10* (the "no unrefuted rival explains … equally well" limb; the unchanged claim column). Both are now scored, and every approximation assertion is scored on every arm.
3. *Canaries validated output shape, not rationale; truncated d6 could credit generic conservatism.* Canaries now pass only for the reason under test, and d6's approximation arms are informational, excluded from the ship and decline rows.
