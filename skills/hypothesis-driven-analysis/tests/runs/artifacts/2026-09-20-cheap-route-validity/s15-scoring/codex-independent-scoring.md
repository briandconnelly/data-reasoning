# Codex's independent scoring of the S15 arms — verbatim return

amicus job `bc5aa000fbcb49269235ccc6f009699e` (`amicus_consult`, backend `codex`, reasoning effort `high`), started 2026-09-20T21:56Z, `ok: true`, not truncated, no findings or list diagnostics.
The text below is the backend's return unedited; it is a scorer's claim, adjudicated in `scoring.md`, and its line breaks are the backend's own.

## Summary

Overall verdict: preregistration row 10, “No regression,” with assertion 9 separately recorded under row 9 as a shared catalog failure. Post passes every assertion pre passes and additionally passes assertions 6, 8, and 10. No assertion is a post-only regression.

Scores: pre 6/10; post 9/10.

| Assertion | Pre | Post |
|---|---|---|
| 1 | **PASS.** “Route: full… single cutover… no holdout… nothing identifies the effect” — `s15-pre.scratch/ledger.md:3`. This takes the full route and states the identifying failure. | **PASS.** “Route: full… no holdout, no randomization: nothing identifies the causal contrast” — `s15-post.scratch/ledger.md:3`. This directly satisfies the assertion. |
| 2 | **PASS.** “H1 \| causal \| UNRESOLVED” — `s15-pre.scratch/ledger.md:67`. `score_ledger.py` reported “C1 checked and passed… 0 REFUTED.” | **PASS.** “H1 \| causal \| UNRESOLVED” — `s15-post.scratch/ledger.md:78`. `score_ledger.py` reported “C1 checked and passed… 2 REFUTED, none of them causal.” |
| 3 | **PASS.** “H3 \| descriptive \| UNRESOLVED” — `s15-pre.scratch/ledger.md:69`. There is no descriptive REFUTED row, so the assertion is vacuously satisfied; C2 reported “nothing to check,” not an earned positive check. | **PASS.** “H3 \| descriptive (estimand: severity-standardized difference in median time to close)” — `s15-post.scratch/ledger.md:80`, matching the Plan-time estimand at `s15-post.plan-ledger.md:27`; the observed +3.42h was larger rather than smaller in magnitude. C2 structurally passed for H3 and H4. The semantic adequacy of H3’s refutation is separately questionable under C4, but the catalog’s assertion 3 only asks whether the descriptive row existed, named its estimand, and failed at that estimand. |
| 4 | **PASS.** “Pooled closed-only median 7.27->5.44” and “standardized +3.42h” — `s15-pre.scratch/ledger.md:51,53`. It preserves the raw estimand and distinguishes the standardized reversal. | **PASS.** “dashboard’s median drop (7.27h -> 5.44h, -1.83h) is a real descriptive fact” — `s15-post.scratch/ledger.md:72`; “standardized diff +3.42h” — line 60. It does not call the dashboard arithmetic false. |
| 5 | **PASS, with a mild judgment call.** “staffing +2 per group… severity may itself be affected… 11 incidents have no activity record” — `s15-pre.scratch/ledger.md:71`. The memo also limits the evidence to one week per arm. Although it calls composition “best supported,” it does not select a causal winner and keeps staffing, calendar-time, severity, and recording threats live. | **PASS, with the same judgment call.** “single cutover… staffing +2… severity… may itself be affected… meaning of absence is UNKNOWN” — `s15-post.scratch/ledger.md:84`. “Other changes that week” remain an unresolved possibility in the memo; no causal winner is selected. |
| 6 | **FAIL.** “They were all at least 205 hours old at extract, so ‘not yet matured’ doesn’t explain them” and “Missing rows erase it” — `s15-pre.manifest.json`, `result_text`. These infer event/missingness implications without evidence separating still open, unrecorded, and incomplete export. The same memo later admits “Whether they are still open, unrecorded or a truncated export can’t be told,” so the direction claims are internally inconsistent. C3 passed only because it reads the ledger, not the memo—an explicit instrument limitation. | **PASS.** “S2… UNKNOWN — the 11 missing rows could be still-open incidents, unrecorded closures, or an incomplete export” — `s15-post.scratch/ledger.md:50`. For the one licensed direction claim, the memo gives the estimand-specific all-placement bound: “headline median barely moves under any placement… drop of 1.77 to 1.89h” — `s15-post.manifest.json`, `result_text`. The C3 exit-1 was only canonical-format drift (`S2 (activity.csv): UNKNOWN` rather than `S2: UNKNOWN`), not a semantic failure under assertion 6. |
| 7 | **PASS.** “none of the responder-hour saving Finance wants to book can be credibly attributed” — `s15-pre.manifest.json`, `result_text`. Conditional +120h and imputation figures are explicitly not identified effects; “credible attributable saving is zero” means no defensible bookable saving, not an identified zero effect. This phrasing is slightly risky but the surrounding causal disclaimer resolves it. | **PASS.** “This is not a finding that Assist ‘does harm’: the design can’t establish that either” — `s15-post.manifest.json`, `result_text`. It clearly distinguishes no bookable saving from a zero-effect estimate. |
| 8 | **FAIL.** Plan-time T5 promised “sev1 contrast, bounds for missing, top-decile share” — `s15-pre.plan-ledger.md:53`; final T5 became “sev1 contrast, missing rows as bound” — `s15-pre.scratch/ledger.md:55`. Neither `a1.py`, `a2.py`, nor `a3.py` computes the promised top-decile test, and no amendment records that deviation. | **PASS.** T1 promised all three severity strata and T5 promised sev1/2 — `s15-post.plan-ledger.md:58,62`; `analysis_out.txt:8-10` contains sev1, sev2, and sev3, while `analysis2_out.txt:1-3` covers overall handoffs and `analysis_out.txt:27-41` covers the daily series. All promised strata were executed before stopping. |
| 9 | **FAIL.** Actual output shows the reversal: marginal handoffs 2.25->1.96, while sev2 3.01->3.95 and sev3 0.54->1.52 — `extract_evidence.py events s15-pre.jsonl --ordinal 9 --with-result-text`. The memo interprets only sev1 (“Handoffs fell from about 6 to 0”) and never interprets the marginal-versus-stratum reversal. | **FAIL.** `analysis2_out.txt:2-3` gives marginal 2.25->1.96, while `analysis_out.txt:8-10` gives sev1 5.93->0.44, sev2 3.01->3.95, and sev3 0.54->1.52. The memo discusses only sev1’s lower handoffs and does not interpret the aggregation reversal. This is the shared row-9 debt. |
| 10 | **FAIL under the assertion’s strict machine-established letter; substantive preregistration itself is visible.** `check_prereg.py` returned exit 2: “UNVERIFIABLE: no executed Write/Edit matches… possible Bash-mediated ledger write(s) at ordinal(s) 8,13,14,15.” Ordinal 8 is in fact `cat > ledger.md`, and its recovered content equals `s15-pre.plan-ledger.md` including the shell-added final newline; it contains five hypotheses and five `NOT_TESTED` rows. All ordinals 1–7 are orientation. This is a Bash-write/checker format incompatibility, not evidence of retrospective planning, but the catalog says ordering must be machine-established and an unverifiable result fails the assertion. A reasonable scorer could instead manually pass it; that would depart from the stated instrument contract. | **PASS.** `check_prereg.py` found “PREREG_WRITE: ordinal 8,” with exit 1 only because manual classification was required. Ordinal 8’s Write content is byte-identical to `s15-post.plan-ledger.md` (SHA-256 `653c56ae…c342348`) and contains five hypotheses plus five `NOT_TESTED` rows. All ordinals 1–7 are orientation, so the manual classification clears it. |

Pre-write chronology and content check:

- Pre ordinals 1–2: orientation/setup reads of `SKILL.md` and `ledger-template.md`.
- Pre ordinal 3: orientation; failed file inventory command, exposing no outcome contrast.
- Pre ordinal 4: orientation; CSV headers, row counts, and staffing coverage. Staffing values show a co-exposure step but no exposure–outcome relationship.
- Pre ordinal 5: orientation; intended uniqueness, coverage, missingness, and composition checks, but failed before reading data because pandas was unavailable.
- Pre ordinal 6: orientation; interpreter/dependency probe.
- Pre ordinal 7: orientation; row counts, key/orphan checks, coverage and missingness by workflow/group/severity, date coverage, and negative-duration checks. It inspected no workflow–TTC, workflow–minutes, workflow–handoffs, or workflow–reopen relationship.
- Pre ordinal 8: first actual ledger write through Bash. The recovered plan matches the archived plan ledger modulo the final newline supplied by the heredoc.
- Post ordinals 1–2: orientation/setup reads of the skill and template.
- Post ordinal 3: orientation; failed inventory command.
- Post ordinal 4: orientation; headers, row counts, and staffing coverage, with no outcome relationship.
- Post ordinal 5: orientation; intended uniqueness/coverage/missingness checks, but pandas import failed before results.
- Post ordinal 6: orientation; dependency probe.
- Post ordinal 7: orientation; key counts, orphan/missing rows, date coverage, composition, and field population only.
- Post ordinal 8: first ledger Write, containing the full Plan-time tables and `NOT_TESTED` outcomes.

Instrument adjudication:

- `score_ledger.py`: pre exits 0 for C1/C3 and reports C2 “nothing to check.” Post exits 0 for C1/C2 when C3 is omitted. With `--c3-unknown-source S2`, post exits 1 because its declaration is `S2 (activity.csv): UNKNOWN` instead of the exact canonical `S2: UNKNOWN`; this is an arm formatting defect caught by an intentionally strict parser, not a failure of assertion 6’s semantic letter.
- C4: pre has no REFUTED row. Post H3 is best classified as a positive/distributional contradiction: an observed relation between marginal and standardized estimates is offered as refuting the composition explanation, and a true composition explanation could still yield a larger sign reversal. The claimed “adequacy: 0 (deterministic prediction…)” is therefore not semantically earned. C4 nevertheless reports PASS because it is syntactic and sees a rate plus variant range. This classification is a genuine judgment call; a scorer treating the finite-export estimand as wholly deterministic could exempt it, but SKILL.md says a complete census is one realization rather than an exemption for an observed distributional pattern. Post H4 is a legitimate deterministic refutation: `analysis3_out.txt:2-4` exhausts all placements of the ten absent Assist values and proves the median can only be 5.375–5.50. H4 should be exempt and unflagged; deliberately flagging it makes C4 fail for the missing atom, illustrating why the caller must classify rows first.
- `compare_prereg.py`, pre: T1 method is substantive (5000 preregistered resamples became an unspecified method and the script actually used 4000); T1 prediction is substantive because the 95%-contrast requirement was deleted; T2 method is a cosmetic implementation elaboration within the preregistered exact/permutation alternative; T2 prediction is substantive because the median promise was deleted; T3 method is substantive because stratified resampling was introduced at conclusion time; T4 method is substantive because it adds residualization; T4 prediction is substantive because “daily” was dropped and the condition was reframed; T5 method and prediction are substantive because the top-decile/long-tail work and handoffs were removed and TTC substituted. No dated amendment covers these cells.
- `compare_prereg.py`, post: T1’s added “95%” is cosmetic because 95% was already committed in Plan prose; T3’s pooled-mix/bootstrap additions are cosmetic consolidation of details already in the H3 row and Plan prose, and its dated amendment does not actually authorize editing the method cell; T4’s “11” to “11 absent” is cosmetic. All remain immutable-cell violations under the comparator even when cosmetic.
- The Tenth-wave statement remains true: none of the current ten assertions directly scores exact plan-versus-final cell immutability. Pre’s T5 drift independently exposes omitted promised work and therefore fails assertion 8, but the comparator difference itself is not a separate catalog failure.

Cell verdict:

- Row 10 applies overall: post passes every assertion pre passes.
- Post-only improvements: assertions 6, 8, and 10.
- Shared row-9 catalog failure: assertion 9.
- Post-only regressions: none; row 3 does not apply.

Draft join sentence:

- It appears in post’s Plan as “expected 1:1… test uniqueness on both sides; reconcile 420 = 409 matched + 11 unmatched” — `s15-post.plan-ledger.md:51`.
- Execution was partial. Ordinal 7 prints `420 409 420 set()` and lists 11 unmatched incidents; combined with the raw 409-row activity count, this supports one-to-one cardinality, no activity orphans, 409 matches, and 11 unmatched incidents. However, the script constructs activity as a dictionary before its uniqueness check, and it never reconciles the additive `responder_minutes` total before versus after the join, as the draft rule requires.
- The behavior was not materially new relative to pre: pre ordinal 7 already checked 420 incidents, 409 activity IDs, zero orphans, and the matched/unmatched coverage matrix. The draft chiefly made the check explicit in post’s ledger. There is no observable displacement of promised analysis in post; both arms still missed assertion 9, while only pre omitted a promised top-decile check. Causal attribution of any difference to one sentence remains uncertain at n=1.

## Findings

- **Pre fails strict preregistration certification despite a real ordinal-8 plan write** (medium; `tests/runs/artifacts/2026-09-20-cheap-route-validity/s15-pre.jsonl`)
  Evidence: `check_prereg.py` exits 2 because the first ledger write is Bash-mediated rather than a Write/Edit event; ordinal 8 nevertheless contains the complete Plan-time ledger.
  Suggestion: Record assertion 10 as FAIL under the catalog’s machine-established contract, while noting this is format incompatibility rather than retrospective planning.
- **Pre makes unsupported missingness-direction claims** (high; `tests/runs/artifacts/2026-09-20-cheap-route-validity/s15-pre.manifest.json`)
  Evidence: The memo says “not yet matured doesn’t explain them” and “Missing rows erase it,” while also admitting the files cannot distinguish still open, unrecorded, and incomplete export.
  Suggestion: Score pre assertion 6 FAIL; keep direction unknown except where an estimand-specific all-placement bound is stated adjacent to the claim.
- **Both arms omit the handoffs aggregation reversal from their interpretation** (medium; `tests/runs/artifacts/2026-09-20-cheap-route-validity/s15-post.scratch/analysis_out.txt`:8)
  Evidence: Marginal handoffs improve from 2.25 to 1.96, while sev2 and sev3 worsen; neither memo interprets that reversal.
  Suggestion: Record assertion 9 as a shared catalog failure under preregistration row 9.
- **Post H3’s C4 atom is syntactically valid but semantically doubtful** (medium; `tests/runs/artifacts/2026-09-20-cheap-route-validity/s15-post.scratch/ledger.md`:60)
  Evidence: The row calls an observed marginal-versus-standardized relationship “deterministic” and records `adequacy: 0`, although a true composition mechanism can produce a larger sign reversal.
  Suggestion: Classify H3 as a positive/distributional contradiction; report that C4 passes only syntactically and does not validate the zero-rate claim.
- **Post’s drafted join reconciliation is incomplete** (low; `tests/runs/artifacts/2026-09-20-cheap-route-validity/s15-post.scratch/analysis.py`:5)
  Evidence: The run supports row cardinality and unmatched-row reconciliation, but activity is dictionary-collapsed and no additive responder-minutes total is reconciled across the join.
  Suggestion: Treat the draft sentence as only partially executed and do not claim a complete join-validity check.
- **Pre silently narrows promised T5 work** (medium; `tests/runs/artifacts/2026-09-20-cheap-route-validity/s15-scoring/s15-pre.plan-ledger.md`:53)
  Evidence: The Plan promises `top-decile share`; the final row and all three scripts omit it without an explicit deviation.
  Suggestion: Score pre assertion 8 FAIL independently of the comparator’s immutability finding.

## Questions


## Assumptions

- `result_text` in each harness manifest is the arm’s final user-facing memo, as stated in the task.
- C3’s implicated activity source is S2 in both ledgers.
- Workflow-by-severity composition and staffing-step inspection before ordinal 8 count as orientation because neither relates exposure to a requested outcome.
- Assertion 10 is scored according to the catalog’s strict requirement that ordering be established by `check_prereg.py`, even though pre’s Bash heredoc can be manually reconstructed.

## Next steps

- Record the cell as row 10 overall, with assertion 9 separately recorded as row-9 shared debt.
- Retain the post join wording only with the qualification that this arm did not execute the required additive-total reconciliation.
- If the harness intends Bash-mediated plan writes to qualify, revise the catalog or instrument contract before rescoring rather than overriding it ad hoc.
