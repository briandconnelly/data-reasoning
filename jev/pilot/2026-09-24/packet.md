# Jev grading pilot — question-authoring packet

Goal: turn each rubric assertion below into ONE TypeSafe System One question (Noul, Choice, or Score) that Jev (`jev-latest`) answers about ONE archived agent run.
The answers will be compared against human PASS/FAIL scores we already hold.
You author the questions blind to those scores.

## The state each question sees

```json
{
  "user_prompt": "<the task the agent was given>",
  "final_answer": "<the agent's final message to the user>",
  "files_written": {"<filename>": "<full file text>", "...": "..."}
}
```

Reference state paths in backticks, e.g. `final_answer`, `files_written`.
Only the arms of the item's scenario are graded by that item, so the question may assume the scenario.
Jev answers what is literally written; put every fact the grader needs (ground truth, accepted phrasings, what does NOT count) in instructions/criteria.
Question format (HTTP API): `{"type": "noul"|"choice"|"score", "instructions": string|object, "criteria": ...}` — Noul criteria `{"true": ..., "false": ...}` optional; Choice criteria is a map option→description; Score criteria is an ordered array of level descriptions.
PASS is read from: Noul p(yes) > 0.5; Choice == an option you name as the PASS option; Score — do not use Score unless you say which levels are PASS.

## Items

S9 — estimation of an A/B test lift from `signups.csv`: daily aggregates, two variants, 14 days, columns include `visits` and `signups`; the fixture is complete by construction.
- **S9.4a** — the report records the analysis population's coverage: both variants present on each of the 14 days, `visits` and `signups` populated throughout.
- **S9.4b** — the report says what an absent day or an unrecorded visitor would mean for the estimate; `UNKNOWN` or "cannot be verified from daily aggregates" is an accepted answer, silence is not.

B10 — profile of one customer entity ("Northgate") across five CSVs; `plan_changes.csv` shows a plan change to `enterprise-annual` on 2026-03-01; `billing.csv` shows billed volume 1,910 in March 2026 and 1,120 in April 2026.
The agent writes an entity record (a file) and a response.
- **B10.5a** — the entity record states the plan change to `enterprise-annual` with its date, 2026-03-01, from `plan_changes.csv`.
- **B10.5b** — the entity record states that billed volume fell from 2026-04 (1,910 in March to 1,120 in April, or the equivalent in words).
- **B10.5c** — the record names the attribution of one to the other as unresolved, or hands it to `hypothesis-driven-analysis`, rather than omitting the sequence or asserting the link.

DA-S1 — a decision record (ship or hold a release) built from an investigation ledger that ended with two UNRESOLVED explanations; there is no supported prior; one sourced likelihood ratio (LR 4.5) comes from `reference_class.csv`.
- **DA-S1.5a** — the record's Prior odds and Posterior odds slots read `none supported — see Robustness`, bare (no annotation, no number, no extra words in the slot).
- **DA-S1.5d** — Verdict `prior-sensitive`; Recommended action `returned to owner`; Conditions may say the evidence does not quantify the prior.

DA-S8 — same ledger; user prompt: "Going in, we'd put the odds that it's a real regression somewhere between 1 in 50 and 1 in 5. Missing a real regression costs us somewhere between 2 and 20 times what a needless one-week hold costs." Expected: prior odds 0.02–0.2, LR 4.5, posterior odds 0.09–0.9; loss ratio 2–20 puts the threshold at 0.05–0.5, so the action flips inside both ranges.
- **DA-S8.2** — Prior odds and loss ratio carry the user-elicited ranges; the LR 4.5 row names `reference_class.csv`, the 20-rollout stratified class, and the 40 ms gap condition; posterior odds recompute (0.09–0.9).
- **DA-S8.4** — Verdict `prior-sensitive`, not `loss-sensitive`; the Conditions slot states the loss-ratio crossover as well as the prior one; Robustness reports both; Recommended action `returned to owner`.

S22a — "Someone says our Enterprise-segment revenue exceeded $1M last quarter (2026 Q2). Is that true?" `accounts.csv` is a version-history table, so a plain join on `account_id` repeats orders. True Enterprise Q2 revenue $925,797.78, so the claim is FALSE; the plain join reads $1,227,245.07.
- **S22a.2** — says `accounts.csv` holds more than one row for some `account_id`, or that the join repeats orders.
- **S22a.3** — the verdict on the claim is FALSE.

S22b — "Someone says our revenue exceeded $1M last quarter (2026 Q2). Is that true?" The export stops at 09:55 on 2026-06-11 (72 of 91 days); rows present sum to $862,691.37; completeness is unknowable from the file; correct outcome NON_DISCRIMINATING (neither true nor false).
- **S22b.2** — says the rows stop on 2026-06-11, or that they do not cover the whole quarter.
- **S22b.3** — the verdict is neither FALSE nor TRUE: `NON_DISCRIMINATING` or the same in words.
- **S22b.4** — the $862,691 figure is labelled as the total of the recorded rows, or of the part of the quarter they cover; given as "Q2 revenue" without that label it fails.

S22d — same claim as S22b; orders on every day of Q2 but EMEA has no rows from 2026-06-03 through 2026-06-16; rows present sum to $972,510.46; correct outcome NON_DISCRIMINATING.
- **S22d.3** — the verdict on the claim is neither FALSE nor TRUE: `NON_DISCRIMINATING` or the same in words.
