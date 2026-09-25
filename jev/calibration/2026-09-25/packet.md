# Calibration packet, 2026-09-25

This file is the rubric for both scorers in this calibration: the person scoring by hand, and the Jev question set Codex writes from it.
Both see the same evidence per run (below) and score each item PASS or FAIL against the text here and nothing else.
It is an archived test input, not a normative statement: the route definitions are copied from `skills/hypothesis-driven-analysis/SKILL.md` § Routing at commit `5ea04d8` so a scorer can apply them, and that section stays their authority.

## The evidence each item is scored on

```json
{
  "user_prompt": "<the task the agent was given, including its harness frame>",
  "final_answer": "<the agent's final message to the user>",
  "files_written": {"<filename>": "<full file text>"}
}
```

Score only what this evidence shows.
The order of the agent's tool calls is not in it, so no item below depends on that order.

## Routes, as SKILL.md defines them (verbatim at `5ea04d8`)

| Route | Observable condition | Ceremony |
| --- | --- | --- |
| **direct** | No claim is being adjudicated, and the answer is a fact the records themselves settle — no explanatory or causal inference, no generalization past what they directly measure — computing a bounded statistic counts | None; answer and stop |
| **estimation** | The answer is a magnitude or a comparison that generalizes past what the records directly measure, no prior claim is being adjudicated, nothing causal is asked that the design does not already identify, and no rival explanations have to be told apart | Estimand, population, uncertainty statement, practical threshold; no competing hypotheses |
| **mini** | Exactly one stated claim is being adjudicated with no rival explanation competing for it — non-causal, or causal with an identifying design behind it | One-paragraph ledger: claim, prediction, probes, outcome |
| **full** | A causal claim or question is requested that no identifying design settles, or two or more live explanations have to be told apart | Full PPDAC loop with investigation ledger |

When collection is costly (the prompt states a price or a metered source), SKILL.md adds a collection plan on any route without changing the route: "The direct route records nothing, unless collection is costly, in which case it records the collection plan and nothing else."

## Items

S2 — prompt: "Here's `orders.csv`. What was the median order value in June?"
- **S2.1** — Routes direct: computes the median and answers.
- **S2.2** — No ledger, no hypothesis language, no PPDAC ceremony.
  Clarification used when this wave was first scored: raw calculation output an agent saves (a results file, a notes file of numbers) is a working artifact and does not fail this item; a structured analysis note that names its route or carries completeness-semantics vocabulary is a record, and fails it.

S9 — prompt: "We ran variants A and B of the signup page for two weeks, randomly assigning each visitor to one of them; `signups.csv` has variant, visits, and signups per day. Is B better than A, and by how much?"
- **S9.1** — Routes estimation: states the estimand, population, an uncertainty statement, and a practical threshold.
- **S9.2** — Does not invent causal "why" hypotheses or a full PPDAC ledger.
- **S9.3** — Reports the estimate with uncertainty rather than a bare point difference.

S11 — prompt: "Someone claims our checkout p95 latency exceeded 500ms yesterday (2026-07-15). Is that claim true?" Ground truth: the file's realized p95 is about 392ms, so the claim is false.
- **S11.1** — Routes mini: a one-paragraph ledger (claim, prediction, probe, outcome), not the full loop.
- **S11.2** — No hypothesis table, no Sources/Tests/Amendments sections.
- **S11.3** — Answers correctly that the claim is false, reporting the measured p95.

S13 — prompt: "Someone claims our checkout p95 latency exceeded 500ms yesterday (2026-07-15) — but only on mobile, only during the evening peak, and only for returning users."
Ground truth: the full conjunction (mobile, evening peak, returning users) has p95 about 439ms, so the claim as stated is FALSE; mobile in the evening peak without the user-type condition reads about 601ms, and new users in that window about 804ms.
- **S13.1** — Routes mini despite needing three or more probes; does not build a hypothesis table.
- **S13.2** — Does not route full on the grounds that the probe count exceeds two.
- **S13.3** — Settles each conjunct of the claim (device, evening window, and returning-vs-new) and answers correctly that the claim as stated is FALSE (returning-user slice p95 about 439ms).

S14 — prompt: "What was the median order value in June? Orders live only in the warehouse, queried with `warehouse.py --dataset orders --day <YYYY-MM-DD>`. Each query is metered — it bills per call and takes a few seconds." Ground truth: median order value 46.94 over 349 orders.
- **S14.1** — Routes direct — the metered source does not promote a descriptive question to full.
- **S14.3** — Produces no hypothesis table, no competing explanations, no coverage matrix.

## Items added before freezing: runs without the skill

These three runs had no skill loaded, so they never saw the record templates the items name.
One reading applies to every item in this section: a run passes on content that does the named job, whatever it is headed, unless the item asks for a specific label, value, or form.
The definitions below are copied from `skills/decision-analysis/SKILL.md` and `skills/exploratory-data-analysis/SKILL.md` at commit `5ea04d8`, so a scorer can apply the items; those files stay their authority.

DA-S1 — prompt: "Here's our investigation ledger (`ledger.md`) — it ended with two UNRESOLVED explanations for the p95 regression. Release freeze is Friday. Missing a real regression costs us roughly ten times what a needless one-week hold costs. Should we ship or hold?"
Definitions: the decision turns on one binary proposition "stated with an explicit residual reading — 'H1 as stated' versus 'not-H1, including explanations nobody named'"; a ledger is evidence input: "record which `UNRESOLVED` rows fold into which state and what the residual absorbs, and never derive a likelihood ratio from a status token alone — `UNRESOLVED` carries no likelihood information."
The verdict set is closed: `robust` (one action is preferred across the entire stated prior class and loss range), `prior-sensitive` (the preferred action flips within the prior class), `loss-sensitive` (it flips within the loss range, or the losses are sensitivity-only), and `dominated` (one action wins under every state); "`optimal` is not a verdict".
- **DA-S1.2** — The two UNRESOLVED rows are mapped into a binary state model with an explicit residual reading; no LR is derived from a status token.
- **DA-S1.4** — Verdict is one of the closed set with conditions attached; no "optimal", no execution of the shipping decision.

DA-S8 — prompt: DA-S1's ledger, with "Going in, we'd put the odds that it's a real regression somewhere between 1 in 50 and 1 in 5. Missing a real regression costs us somewhere between 2 and 20 times what a needless one-week hold costs — the team can't agree on the number. Release freeze is Friday. Should we ship or hold?"
Ground truth: prior odds 0.02–0.2 and the ledger's likelihood ratio 4.5 give posterior odds 0.09–0.9; a loss ratio of 2–20 puts the decision threshold at odds 0.05–0.5, so the preferred action flips inside the prior range and inside the loss range.
- **DA-S8.3** — Robustness reports both crossovers: the prior odds at which the action flips for a given loss ratio, and the loss ratio at which it flips for a given prior.

B10 — prompt: "Tell me about the Northgate Clinic account. Everything we have is under `b10-entity/` and covers January through June."
Fixture facts: Northgate Clinic resolves to two account ids after a mid-window rename; it has zero rows in two of the six months; an independent contract-status file covers one of those two months and is silent about the other, so one empty month is resolvable as genuine inactivity and the other is not; a plan change lands one month before a drop in billed volume, which invites a causal story the data does not support.
Definitions: Frame-lite "pins the entity and the identifier that resolves it, the sources that carry it, and the timeframe"; the orientation record is the record of what the data covers and what its absences mean, written before any pattern is interpreted; the entity record is "the descriptive facts the sources settle about the entity across the framed window, in associational wording".
- **B10.1** — Frame-lite pins the entity and the identifier that resolves it, the sources that carry it, and the timeframe; a run that widens to the whole table without recording the scope change, or that silently drops the second id, fails.
- **B10.2** — Orient records absence semantics for both empty months: the covered month is distinguished as no activity on independent evidence, and the uncovered one is recorded as `UNKNOWN` rather than read as inactivity.
- **B10.3** — The deliverable is the orientation record plus the entity record; a leads table, or an orientation record alone, fails.
- **B10.4** — No causal attribution anywhere in the output (scored on assertion status rather than vocabulary): the plan change and the volume drop may both be stated, and their order in time may be stated, but neither may be offered as the reason for the other.
