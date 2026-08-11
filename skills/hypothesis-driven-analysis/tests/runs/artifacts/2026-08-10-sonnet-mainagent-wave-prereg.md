# Preregistration: Sonnet-as-main-agent wave — 2026-08-10

Written before any arm ran.
This wave holds the skill wording fixed and varies the model: each arm is a fresh Sonnet subagent acting as the *main* agent, with `SKILL.md` loaded, scored against the committed assertions in `tests/scenarios.md`.
It is not a wording change and ships no edit; the rerun-obligation rules in `PROTOCOL.md` do not apply.
What applies is the Iron Law's preregistration half: the cells, the expected outcomes, and every reachable verdict are written down here first.

## Question under measurement

Does skill quality degrade when a less-capable model (Sonnet) is the main agent that loads and applies `hypothesis-driven-analysis`?
Prior arms (2026-07 waves) ran on stronger models; the sole Sonnet arms on record (`2026-07-20-scenario18-trigger-sonnet-weak.md`) tested triggering, not rule application.
A textual assessment (this session, 2026-08-10) predicted three capability-sensitive axes: (1) rules written as dense literary prose, (2) assumed statistical competence in the interval-sensitivity block, (3) multi-step routing judgment on causal design.

## Cells

One arm per cell this wave (canary-sized; reps only if a cell comes back interesting).
All arms: fresh Sonnet general-purpose subagent, no conversation context, given the committed scenario prompt with absolute paths, told the skill file it may read, forbidden from reading `tests/scenarios.md` and `tests/runs/`, told to write any working files to a per-arm scratch directory outside the repo.

| Cell | Scenario | Axis probed | Scored assertions |
| --- | --- | --- | --- |
| S2-sonnet | S2 non-trigger, bounded descriptive | Over-ceremony pressure | S2's 2 |
| S9-sonnet | S9 estimation routing (randomized A/B) | Routing: identified design → estimation, not full | S9's 3 |
| S11-sonnet | S11 mini route (stated claim) | Routing: claim vs question; score the *reasoning* | S11's 3 |
| S12-sonnet | S12 causal "how much" | Routing: unidentified causal → full, no causal number | S12's 5 |
| S6-sonnet | S6 underpowered null, distributional trap | Statistical competence: median-appropriate sensitivity | S6's 5 |

## Expected outcomes (predictions, per the textual assessment)

- S2-sonnet: pass both. Failure mode if wrong: ceremony on a direct question.
- S9-sonnet: pass. Failure mode if wrong: over-routing to full despite stated randomization (the opposite of the classic failure).
- S11-sonnet: route correct; the at-risk part is the *reason* (routing on effort rather than on "someone asserted something").
- S12-sonnet: the highest-risk routing cell. Failure modes: routes estimation on phrasing; or routes full but still reports a causal effect number; or marks the causal hypothesis `REFUTED` from the observational contrast.
- S6-sonnet: the highest-risk cell overall. Failure modes: sd/√n or mean-based power argument on a median claim; null read as refutation; slow cluster blended into pooled statistics or attributed to the rebuild.

## Reachable verdicts (all rows written before any arm ran)

1. **All five cells GREEN.** Evidence of parity on these cells at n=1; per the suite's own rule this is non-discriminating for the degradation claim, not proof of safety. Action: report parity, recommend nothing; optionally rerun S6/S12 with reps before relying on Sonnet-as-main.
2. **S6 and/or S12 drop assertions; routing-lite cells (S2, S9, S11) hold.** Confirms the capability-sensitivity prediction where predicted. Action: record which axis; recommendation stands that Sonnet runs only as briefed worker, not main agent. No skill edit follows from this wave — a model-sensitivity finding is not a wording defect.
3. **Broad failures including S2/S9/S11.** Stronger than predicted; same action as row 2 plus a note that even routing-lite cells are unsafe.
4. **A cell fails for a fixture or harness reason, not a rule reason** (wrong file path, budget exhaustion, tool denial). That cell is void, not RED; rerun it once fixed. Scored per PROTOCOL step 4's rationale rule: a wrong label reached without traversing the rule under test is entanglement, not evidence.
5. **The wave turns out unnecessary** — e.g. the user redirects, or an arm cannot be dispatched with a Sonnet override. Record what ran and stop; partial waves are reported as partial.

Rows 1–3 all end with "no wording change ships from this wave"; this measurement decides deployment advice (which model may run as main agent), never prose.

## Scoring notes

- Scorer: the dispatching session (Fable), against the committed assertion lists, with one-line evidence pointers into each arm's output and written files.
- S11 and S12 are route-selection runs: no baseline arm exists by design.
- S2 pass requires the *absence* of ceremony; the arm's full return is preserved in the run file so that absence is checkable.
- Full-transcript machine checks (`check_prereg.py`) are out of scope this wave: these arms are dispatched in-session and the harness manifest is not extracted. The S6/S12 assertions scored here do not require it; S1-class preregistration-ordering assertions are deliberately not scored this wave for that reason.
- Tool-call and token counts recorded where the harness reports them; approximate otherwise, and labelled so.

## Contamination controls

- Fresh subagents, not forks (a fork inherits this conversation, which contains the assertions).
- Each prompt names only: the scenario prompt, the skill path, the fixture path, the scratch dir, and the two forbidden paths.
- Nothing in any prompt names the expected route, the assertions, or this file.

## Results (appended after all five arms ran and were scored)

Run files: `2026-08-10-scenario{2,6,9,11,12}-sonnet-mainagent.md`; arm ledgers archived beside this file.

| Cell | Score | Notes |
| --- | --- | --- |
| S2-sonnet | 2/2 | Direct answer, empty scratch, value scorer-verified |
| S9-sonnet | 3/3 | Estimation for the stated-randomization reason; predicted over-routing did not occur |
| S11-sonnet | 3/3 | Mini for the claim-not-effort reason; found an undocumented real coverage gap |
| S12-sonnet | 5/5 | Refused the causal number; form note: no explicit status table, statuses correct in prose |
| S6-sonnet | 5/5, one marginal half | Order-statistic + bootstrap interval, `NON_DISCRIMINATING`; detection limit implied by interval, not named |

**Verdict: row 1** — all cells effectively GREEN at n=1.
The two blemishes are form-level (a missing status table in S12, an unnamed detection limit in S6); no substantive rule was dropped, no status invented, no causal number manufactured, no wrong-reason route taken.
Per row 1 as preregistered: this is evidence of parity on these cells, non-discriminating for the degradation claim by the suite's own too-easy rule, and not proof of safety; no wording change ships; reps on S6/S12 are the next spend if Sonnet-as-main-agent is to be relied on.
Scope limits, as preregistered: n=1 per cell; in-session dispatch, so no transcript manifest and no `check_prereg.py` ordering check (S1-class ordering assertions deliberately unscored); token counts are harness-reported subagent totals.
One unpreregistered observation, recorded as such: all five arms self-reported their route with a correct paraphrase of the governing rule, which the prereg did not ask for and the assertions do not score.
