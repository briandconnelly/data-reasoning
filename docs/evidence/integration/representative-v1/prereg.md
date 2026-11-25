# Representative suite v1 — preregistration

Issue #115.
Written 2026-11-24, before any arm, canary included, ran.
Everything below is fixed before the canaries; any change after them is a dated note at the end, never an edit above it.

## Question

On routine requests and on challenge tasks, does a clean plugin install change the user's answer compared with the same host and model given no plugin, by enough to justify the plugin's procedure and its context cost?
Answer quality is judged by the verdicts below; cost is reported descriptively beside them (§ Scoring).
The adversarial catalogs cannot answer this: by their own rule a scenario a baseline passes is too easy for them.
This suite keeps tasks a baseline may pass, because "the plugin makes no difference" is one of the results it exists to detect.

## Cells

Prompts are frozen by the SHA-256 of the prompt text with `{DATA}` left unexpanded, as `scripts/run_integration.py` `prompt_sha256` computes it; `scripts/test_run_integration.py` fails if a prompt and its hash here disagree.
`{DATA}` renders as `data`, the staged fixture's path relative to the arm's workspace.
No prompt names a skill, a route, a method, or the trap its cell sets.
Routine prompts avoid the skills' own vocabulary (explore, investigate, hypothesis, decision, evidence, causal, uncertainty).

Fixtures are built by `scripts/representative/generate.py` (seed 20261124) into `fixtures/` beside this file.
Each has a validator under `scripts/representative/` that recomputes its discriminating property from the files, byte-compares a fresh build, and runs as a prek hook; `scripts/representative/test_validators.py` proves each validator fails on a degenerate copy.

| Fixture file | SHA-256 |
| --- | --- |
| `r-sales/orders.csv` | `8828d775e7566bd80f44da81acfbfd205b9f75aa78a1556e3037503fcbf9e648` |
| `x1-supplier/acme_history.csv` | `191979a86e7aac3b2dfced353f3c4e0182fbcc24ab73861d456fd8531b049a3c` |
| `x1-supplier/brightline_trial.csv` | `5fecbcae033bc3660824b255eb483b7a5f54c527b9abf600326ba886a0d71164` |
| `x1-supplier/contract_terms.md` | `5052ba4cc56c9b103b341b7ca6538c13325281b15385a24d053b32ee7160c524` |
| `x2-forecast/analyst_model.py` | `e2a1dde3f836d59fbde611aa369f47be00c93fa9f142a7ea863fc273892ada34` |
| `x2-forecast/analyst_notes.md` | `e4fd4e40fe56ac4ecadfe7ea5ae6ed849febf92d0a63e2062c70e8690793db52` |
| `x2-forecast/daily_tickets.csv` | `bc7a603a1eb8f797aa4e7ffc7f82b82b2049489f2ef0f2738db3a31cbd1369bd` |
| `x3-churn/holdout_scores.csv` | `139bb2c7f5a531be624bbd213f77dce571c1d9d9b70f01cdc23603473371ebce` |
| `x3-churn/models.md` | `183710c26a152baccbc6069e23065261aca3eca0d6eb77ee6478bef57ede01eb` |

### R1 — routine lookup

Fixture: `fixtures/r-sales/` (1,176 orders, four stores, 2026-01-01 to 2026-04-30).
Prompt: "How many orders did the Riverside store take in March 2026? Our order export is `{DATA}/orders.csv`."
Prompt SHA-256: `7acbe2b4590cc4e2f4e7503b3190942777a49964421e2fa6f97be90f9c3a2c03`.
Ground truth: 99 orders (242 units, the misreading `validate_r.py` keeps distinct).
Designed route: none.

### R2 — routine aggregate

Fixture: `fixtures/r-sales/`.
Prompt: "Using `{DATA}/orders.csv`, what was the average order total at each store in February 2026? An order's total is unit_price times quantity."
Prompt SHA-256: `13d3c762b6c8dda4d8fd403e1f92befb456f9071d02f260c0c6a1fff0ac8d238`.
Ground truth: Harbor 117.15, Hillcrest 101.80, Old Town 113.85, Riverside 111.25.
Designed route: none.

### R3, R4 — representative requests (placeholders)

These cells are placeholders.
They have no prompt, fixture, or ground truth, and `scripts/run_integration.py` refuses to run them.
They await real user requests supplied by the owner, anonymized and used with permission.
A real prompt must satisfy all of the following before it is frozen here by a dated note:

- R3 is an investigation ask and R4 an exploration ask, in the user's own words, not rewritten by anyone who wrote the skills.
- Identifying details are replaced, and nothing else about the wording changes.
- It is paired with a fixture that answers it, generated and validated like the others, with ground truth stated before any arm.
- It names no skill, route, or method.
- Its designed route and its C and E criteria are written in the same note, before any arm of it.

Until then the suite runs as five cells and every count says so.

### X1 — carrying the uncertainty flips the action (challenge)

Fixture: `fixtures/x1-supplier/`: Brightline's trial (1 defective of 150), Acme's history (1,000 of 50,000), and contract terms.
The terms state 100,000 units, no inspection on receipt (every defective unit received is shipped, so the shipped defect rate equals the supplier's rate), $15 in returns per defective unit, and a $1,000,000 penalty if the annual shipped defect rate exceeds 3%.
Prompt: "We have to pick one supplier for all 100,000 units next year: stay with Acme or move to Brightline. Brightline's trial batch, our Acme history, and the contract terms are in `{DATA}`. Brightline's trial had fewer defects than Acme usually has, and it is all we know about Brightline. Which supplier should we sign with?"
Prompt SHA-256: `b6533ba6367afa8747308af958ccdfb722cf81b46dff4784abdd6e38b931dfe5`.
Prior information: the user has none about Brightline beyond the trial, so no supported prior exists in the decision skill's sense.
Ground truth: treating the trial rate (0.67%) as known costs Brightline $10,000 against Acme's $30,000, so a point estimate picks Brightline.
Carrying the trial's uncertainty under the symmetric prior family Beta(a, a), a from 0.5 (Jeffreys) to 1 (uniform), Brightline's chance of exceeding 3% runs from 2.8% to 5.7% and its expected cost from $42,607 to $76,769, against Acme's $30,014 to $30,029: Acme across the whole family.
Acme's posterior cost differs from $30,000 because its posterior mean rate (1,001/50,002 under the uniform prior) is slightly above 2%, not because of the penalty, whose probability for Acme is effectively zero.
Sensitivity, outside the stated family: Brightline wins for a at or below 0.2 and Acme from 0.25 up, so the answer depends on the prior only for priors that put more weight near zero defects than Jeffreys does.
The break-even is a penalty probability for Brightline of about 1% to 2% (where $1,000,000 × P equals Acme's cost minus Brightline's expected per-unit cost).
`validate_x1.py` asserts the point-estimate choice, Acme across the stated family, and the shipped-equals-received statement, and reports the sensitivity.
Designed route: `decision-analysis`.

### X2 — a random split passes and a backtest fails (challenge)

Fixture: `fixtures/x2-forecast/`: daily ticket counts from 2024-10-01 to 2026-09-30 with weekly and annual seasonality, the analyst's same-weekday nearest-neighbour model, and notes reporting its random-split error.
Prompt: "Our analyst built a model for daily support ticket volume; the notes, code, and two years of data (through September 30, 2026) are in `{DATA}`. They report under 4% error on held-out days. Today, with data through September, we set staffing for October, November, and December from each month's forecast total, and that works if the three monthly totals are within 10% of actual on average. Can we use it?"
Prompt SHA-256: `af193ef90ea11d5a3e3f95a5610e329ba6107de30889742a4ee92ea46d890319`.
Frozen reading, from the prompt: decision date 2026-09-30, horizon October to December, error unit the mean absolute percentage error of the three monthly totals, bar 10%.
The horizon-matched backtest is the same decision one year earlier: forecast October to December 2025 from data before 2025-10-01.
Ground truth: random 20% holdout daily MAPE 3.6%; horizon-matched monthly-total MAPE 23.8%, failing the bar.
The model cannot be used as evaluated.
Sensitivity, reported and not asserted: from origin 2026-01-01 the three-month monthly-total MAPE is 3.6% (daily 5.1%), from 2026-04-01 33.3% (33.7%), from 2026-07-01 7.1% (7.6%), and from 2025-10-01 daily 23.6%.
An origin outside the matching season can therefore pass the bar, which is why the reading is frozen.
Designed route: `hypothesis-driven-analysis`.

### X3 — two metrics pick different winners (challenge)

Fixture: `fixtures/x3-churn/`: 10,000 holdout customers (13.8% churned) with each model's churn probability, and `models.md`, which states that the team currently reports accuracy at a 0.5 cutoff.
Prompt: "We have two candidate churn models scored on last quarter's holdout customers, with who actually churned: `{DATA}/holdout_scores.csv`. Next quarter our retention team will call the 500 customers the deployed model scores highest on one list like this one. Which model should we deploy?"
Prompt SHA-256: `bb80c360a92e3f7677a27c8af75cbac772ef93c93c9b601e86e5e9e2c3dae13b`.
Frozen reading, from the prompt: one pooled list, the top 500 by each model's score.
Ground truth: accuracy at the 0.5 reporting cutoff picks A (84.6% against 79.5%); the top 500 picks B, 302 churners (60.4%) against A's 173 (34.6%).
B also wins at 1,000 (505 against 305) and 1,500 (660 against 427), so no reading of the list size moves the winner; `validate_x3.py` asserts all three.
Sensitivity, reported and not asserted: accuracy reverses at other cutoffs (A 86.23% against B 87.26% at 0.9, where the all-negative baseline is 86.23%), which is why the reporting cutoff is stated in the fixture.
Designed route: `hypothesis-driven-analysis` (its estimation route: a purely predictive comparison); a first load of `decision-analysis` is also on route, and then its handoff to `hypothesis-driven-analysis` is scored.

## Conditions

Seven cells × two conditions (plugin, no plugin) × two hosts (Claude Code, Codex) × n=3 = 84 scored arms.
One canary per cell per host is run and excluded from scoring: 7 in B3 Step 4 on one host and 7 in C1 on the other.
Until R3 and R4 have prompts, the runnable count is 60 scored arms and 5 canaries per host.

Each condition is set up as `docs/evidence/integration/2026-11-17-full-catalog/prereg.md` § Conditions sets it up, through `scripts/run_integration.py`, with these differences for this suite's cells:

- The workspace is named `int-arm-*`, and `{DATA}` renders as the relative path `data`, so neither the arm's name nor its condition reaches the prompt.
- Before any host call the harness refuses to run unless the fixtures, prompts, this file, and the harness match HEAD, and the staged fixture bytes and the prompt match the hashes above.
  Arm outputs under `arms/` beside this file are outside that check, so a replicate block runs without a commit after each arm.
- Each manifest records the prompt hash, per-file fixture digests, the requested and resolved model, the host version, and an execution status; every file the arm created or changed in its workspace is copied into `<name>.workspace/`.

### Models and host versions

Each host's model id is pinned with `--model` (Claude Code `--model`, Codex `-m`) and named in a dated note below before the first canary; the harness refuses a representative arm without it.
A comparison between plugin and no-plugin arms of one cell on one host is paired only when every arm in it has the same resolved model (the manifest's `model`) and the same `host_version`; otherwise it is reported as unpaired, with its counts and no verdict.
No comparison crosses host versions or models silently.

### Run order

Arms run in three replicate blocks per host; each block holds every runnable cell × condition once, in the order `random.Random(20261124 + replicate).shuffle(sorted(slots))` gives, the same on both hosts:

1. R2-none, X3-none, X2-none, R2-plugin, X3-plugin, R1-plugin, X1-none, X2-plugin, X1-plugin, R1-none
2. R2-plugin, X2-none, R1-plugin, R2-none, X3-none, X1-plugin, X1-none, R1-none, X3-plugin, X2-plugin
3. R2-plugin, X3-plugin, X2-none, R2-none, X1-plugin, R1-plugin, X2-plugin, X3-none, X1-none, R1-none

R3 and R4 slots are added to every block, by the same rule, in the dated note that freezes them.

### Invalid executions

An invalid execution is not a failing answer; it is not scored.
It is any arm whose manifest status starts `invalid-execution` (a timeout, a nonzero host exit, a transcript line that does not parse, or a transcript without the host's own terminal success event), whose resolved model or host version differs from the pinned one, or whose plugin install failed.
An invalid arm is rerun once, in a new slot at the end of its block; at most three replacements are made per host.
A slot still invalid after its replacement, or beyond the cap, leaves its cell's comparison on that host incomplete: it is reported with the counts of valid arms and gets no verdict.

## Scoring

Scored per arm from the archived transcript, final message, and the workspace files the harness copied.
"Results" means a tool output containing a value computed from the task's data (a count, mean, estimate, or model output); reading a schema, header, or file listing is not a result.
A skill load is a `Skill` tool call or a read of that skill's `SKILL.md` (Claude Code), or a read of that skill's `SKILL.md` from the installed plugin cache (Codex), as `observed_route` in `scripts/run_integration.py` extracts them, confirmed by hand.

This section is the single home of the column definitions below; other files point here by column name.

- **First activation.**
  Pass: the first data-reasoning skill load is a skill on the cell's designed route.
  Fail: the first load is off the designed route, or there is no skill load at all, recorded as `none`.
  Not applicable: the cell's designed route is none (R1, R2), where loads are scored under unnecessary ceremony instead.
- **Handoff taken.**
  Scored once per handoff in the observed route that the designed route allows.
  The only one in this version is X3's optional `decision-analysis` → `hypothesis-driven-analysis`: scored when `decision-analysis` is the first load, `n/a` when `hypothesis-driven-analysis` is.
  Pass: the downstream skill is loaded after the upstream skill; a single tool call that loads both passes and is annotated `batched`.
  Fail: the downstream skill is never loaded.
  Not applicable: no such handoff, or the upstream skill never loaded; R3 and R4 state theirs when frozen.
- **Record written: `<record>`.**
  One column per record the observed route requires, in the form its subroute requires.
  The forms are a decision record (`decision-analysis`), a full ledger, mini ledger, or estimation record (`hypothesis-driven-analysis`, by the route its `SKILL.md` § Routing assigns), an exploration log (`exploratory-data-analysis`), and an identification review (`causal-identification-review`).
  A form with a validator signature passes when `instruments/check_record.py` recognizes the file as that kind (exit 0 or 1, not 2); its structural findings are reported, not scored.
  A form with none (mini ledger, estimation record; `scripts/shared-sections/record-delivery.md`) passes when the file carries the fields that `SKILL.md` names for it (§ Estimation Route for an estimation record, § Routing for a mini ledger).
  Each record is labelled with one of three states, and only the last two pass:
  - `scratch`: created during the arm but absent from the workspace at the end;
  - `retained`: present in the workspace at the end;
  - `delivered`: retained, and the final message names or links its path.
  The results record reports retained and delivered counts separately, so a scratch-only arm is never read as a memo-only one.
  Fail: no such file, including a record that appears only in the final message.
  Not applicable: the requiring skill was not loaded.
- **Record written before results: `<record>`.**
  One column per record scored pass on record written.
  Pass: the tool call that first creates the record's file precedes the first result computed after the owning skill's load (that route's precommitment boundary), so results computed earlier under an upstream skill do not count against a downstream record.
  Fail: it follows that result.
  Not applicable: record written is fail or not applicable.
  Later edits do not change this column.
  A separate descriptive column, **record before any result (whole arm)**, records whether the file preceded the arm's first result of all; it enters no verdict.
- **Evidence boundary (E).**
  Read from the final message only, for every arm, plugin or not.
  R1, R2: `n/a`.
  X1: Brightline's trial rate is not treated as its known rate; the answer says the trial is too small to rule out a rate above the 3% clause, and that this risk drives the choice.
  X2 has two columns, both required for E:
  - **E(a) leakage recognized**: the answer says the random-split figure does not measure forecasting months ahead and names why: the held-out days were drawn at random, so the model was scored on days with training days on both sides of them (interpolation, leakage across time, or ignoring time order all qualify).
    Generic caution ("validate further", "forecasts are uncertain", "monitor in production") without naming the time-order problem fails.
  - **E(b) horizon-matched backtest reported and interpreted**: the final message reports a backtest whose training data all precede October 2025 and whose test window is October to December 2025, scored on monthly totals, gives its error within 3 points of 23.8%, and concludes the model fails the 10% bar for this staffing use.
    A backtest reported only at another origin fails E(b), whatever it concludes.
    Like every E and C column, E(b) is read from the final message alone, so both scorers apply it to the same evidence.
  X3: the answer says accuracy at a threshold is not the measure for a 500-call list and compares the models by a measure taken at that depth of each model's ranking.
  Qualifying measures: precision (hit rate) in the top 500, churners caught in the top 500, lift or gains at 500, or a precision-at-k curve read at 500.
  Not qualifying on their own: AUC, accuracy, F1, precision, or recall at a probability threshold, log loss, or calibration.
- **Task (C).**
  Read from the final message only.
  R1: 99.
  R2: every one of the four store means within 0.01 of the ground truth, inclusive (|reported − truth| ≤ 0.01).
  An answer that rounds to one decimal passes when each value is within 0.05 of the truth, inclusive, so Harbor's exact 117.15 passes as 117.1 or 117.2.
  X1: either Acme, or a conditional recommendation that the decision skill's missing-support form produces: it states a break-even penalty probability (or an equivalent crossover in rate or prior terms) between 1% and 2.5%, says the trial cannot establish which side Brightline is on, and names what would change the action (a larger trial or other evidence on Brightline).
  An unconditional Brightline fails.
  X2: no, not for October to December staffing as evaluated.
  X3: B, with the top-500 churner counts reported for both models within 3 of the ground truth (B 302, A 173), or the equivalent precision within 0.6 points (60.4%, 34.6%).

One orchestrator-only column, not blind-scored and outside every verdict:

- **X2 backtest computed (transcript).**
  Pass: the transcript shows a tool call that computes the October to December 2025 backtest E(b) describes, from training data that all precede October 2025.
  Fail: no such computation appears.
  Not applicable: every cell but X2.
  The X2 verdict and the X2 D1 signal use E(b), which both scorers score; this column is reported beside E(b), and an arm that passes E(b) and fails this column is listed as an unsupported report in the results record.
  It is the only answer-related column read from the transcript; X1's and X3's E and C columns have no transcript component, since each is settled by what the final message states.

The routing, record, and ceremony columns are read from the transcript and workspace too, and are likewise scored by the orchestrator only.

Three further measures, per arm, all descriptive:

- **Unnecessary ceremony.**
  Scored on R1 and R2 only, `n/a` elsewhere.
  Fail when any of these occurs before or instead of the direct answer: a data-reasoning skill load, a record file written, a preregistration or plan the user did not ask for, or a stop for authorization or clarification.
  A plan is a set of steps, hypotheses, or criteria written out before the answer, in a file or in more than two sentences of the reply; one or two sentences saying what will be computed are not a plan.
  Pass otherwise.
  Each fail is tagged with its causes, naming the skill when a load is among them.
  A skill load that routes straight out to a direct answer still fails; this column counts the load as the cost.
- **Wall-clock latency.** `duration_s` from the arm's manifest.
- **Loaded context tokens.**
  Claude Code: from the final `result` event's `usage`, `input_tokens + cache_creation_input_tokens + cache_read_input_tokens`.
  Codex: the sum over `turn.completed` events of `usage.input_tokens`, cached tokens included.
  Extracted by the scorer from the archived `.jsonl`.

Record columns, answer columns, and the three measures are reported side by side and never combined into one score.
Cost is descriptive in this version: latency and loaded context are reported per cell, condition, and host as medians with each arm's value, and no rule here trades them against answer quality.
The question's cost half is answered by that report, not by a verdict.

### Scorers

Primary: the dispatching Claude Code session (the orchestrator), unblinded, scores every arm.
Blind: `openrouter/google/gemini-3.1-pro-preview` through amicus, a model that runs no arm, scores E and C on every arm from final messages with skill names, record headings, and condition redacted; it scores no transcript-based column.
Disagreements are reported, not reconciled.
The results record carries its `Scorer:` line as `skills/hypothesis-driven-analysis/tests/PROTOCOL.md` § Who scored it requires.

## Verdicts

Reported per host and per cell; no verdict pools Claude Code and Codex, and challenge cells are reported apart from the routine and representative cells.
At n=3 nothing is a rate, and every verdict is reported with its exact counts.

An arm passes when it passes every answer column its cell has: C, and E where E applies (both E(a) and E(b) on X2); on R1 and R2 an arm passes on C alone.
An arm that passes some of those columns and fails another is a split arm: it counts as a failing arm, and the results record reports how many arms split and which column each failed.
So every valid arm is passing or failing, and a condition (plugin or no plugin, for one cell on one host) has k passing arms, k from 0 to 3.

| Plugin k | No-plugin k | Label for that cell and host |
| --- | --- | --- |
| 2 or 3 | 0 or 1 | directional lift |
| 0 or 1 | 2 or 3 | directional regression |
| 2 or 3 | 2 or 3 | not distinguished at n=3, both majorities pass |
| 0 or 1 | 0 or 1 | not distinguished at n=3, both majorities fail |

Each label is a majority comparison at n=3 and is reported as directional, never as an effect or as "no difference"; 3/3 against 2/3, or 0/3 against 1/3, is a one-arm difference reported in the counts and not read either way.
An unpaired or incomplete comparison gets no label.
Across the suite, on a host, the summary lists how many cells carry each label; no single suite-level verdict is drawn.

## What would change a maintenance decision

Stated before any arm; each signal acts only on a labelled, paired, complete comparison.

- **X2 → D1 (#116).**
  If the plugin condition on X2 has at most 1 of 3 arms passing E(b) on either host, D1 writes the on-demand reference for horizon-matched backtesting.
  If it has at least 2 of 3 on both hosts, #116's forecasting row closes as "no change, measured".
- **X3 → D1 (#116).**
  If the plugin condition on X3 has at most 1 of 3 passing arms on either host, D1 writes the on-demand reference for evaluating a model at its operating point.
  If it has at least 2 of 3 on both hosts, #116's model-evaluation row closes as "no change, measured".
- **R1, R2 → descriptions.**
  Counted per host and per skill: L is the number of the 6 plugin arms on R1 and R2 whose ceremony fail includes a load of that skill.
  L of at least 3 justifies narrowing that skill's description, through the unfreeze procedure of `skills/exploratory-data-analysis/decisions/006-description-freeze-until-measured.md`.
  L of exactly 2 is inconclusive: the description stays unchanged, recorded as a watch item that a later measured arm on that skill must cite before any change.
  L of at most 1 leaves it unchanged.
  Ceremony fails with no skill load (a plan, a record, or a stop without one) justify no description change; when the no-plugin arms on the same cells fail ceremony on the same grounds at least as often, the behaviour is recorded as the host's, and no plugin change follows.
- **Activation (#104, #108, #111).**
  Descriptive only.
  Within a cell's plugin condition on a host, arms that passed first activation are compared with arms that did not on E and C, and only when both groups have at least one arm; otherwise the comparison is "not assessable".
  The comparison is reported with its counts and justifies no activation work by itself; any proposal for activation work cites it beside its own evidence.
- **Conflicting signals.**
  When two signals point at the same skill in opposite directions (a D1 reference to add and a description to narrow), neither change is made from this suite; the conflict is reported and the owner decides.
  Signals on different skills or files are acted on independently.

## Limits fixed in advance

- One Claude model and one Codex model.
- Codex plugin arms run without the record-checking hook, as in the full-catalog suite.
- Synthetic challenge fixtures test whether a known trap is caught, not how often real users meet it; R3 and R4 are the representative sample and are not yet frozen.
- The routine prompts were written by the plugin's maintainers' agent, outside the skills' vocabulary, which reduces but does not remove the risk that they route better than a user's words would.
- X1's keyed answer rests on the stated prior family; a prior concentrated near zero defects (Beta(a, a) with a at or below 0.2) reverses it, and an arm that says so and conditions its recommendation passes C.
- The full-catalog cells I1–I4 keep that suite's behaviour, including a workspace named after the arm (`int-<name>-*`, where the name carries the condition) inside the absolute data path their prompts show; that condition leak is not fixed here, so the full-catalog comparisons are not changed after the fact.

## Notes after writing

2026-11-25, before the first canary:

- Models pinned: Claude Code `--model claude-sonnet-5-5`; Codex `-m gpt-6.2-sol`.
  Host versions at this note: Claude Code 2.1.332, codex-cli 0.172.0.
- The owner confirmed the four calls this file makes on their behalf: X1's prior family Beta(a, a) for a from 0.5 to 1, X3's one pooled list, the ±3 tolerances on X2's backtest error and X3's hit counts, and the cap of three replacements per host.
- Canaries run in the plugin condition, one per runnable cell per host, into `canaries/` beside this file, named `<cell>-<host>-canary`.
  A canary passes when its manifest status is `completed`, its resolved model and host version match this note, its prompt hash and fixture digests match this file, the plugin install succeeded, and its workspace files were archived.
  Canary answers are not scored.
- Scored arms wait for the owner's go-ahead after the canaries are reported.

2026-11-25, after the canaries and before any scored arm:

- All ten canaries passed the criteria above; they are archived under `canaries/`.
- Observed in the canaries, unscored: Claude Code loaded no skill on any of the five cells; Codex loaded skills on X1, X2, and X3.
- Deviation, decided by the owner on budget grounds before any scored arm: Codex runs all three replicate blocks (30 arms).
  Claude Code runs block 1 only (10 arms).
  If any Claude Code plugin arm in block 1 loads a skill, blocks 2 and 3 run as written.
  If none does, Claude Code stops at block 1: its comparisons are reported with their counts as incomplete, with no verdict, and no maintenance signal is drawn from that host.
- Scored arms are named `<cell>-<host>-<condition>-<replicate>`; a replacement adds `-r`.
- The `data_modified` flag is set by any new file under `data/`, including an interpreter cache (`__pycache__`) written when an arm imports the fixture's code; the results record reports the flag with what changed, and such a cache alone is not a modified fixture.

2026-11-25, after the first run's results:

- Four further Claude Code no-plugin arms run out of block order for the forced-load diagnostic in `forced-load/prereg.md`: `X2-claude-none-2`, `X2-claude-none-3`, `X3-claude-none-2`, `X3-claude-none-3`.
  They are this file's own slots and are scored as written; Claude Code's plugin slots for blocks 2 and 3 stay unrun, so its suite comparisons stay incomplete.

2026-11-25, harness change after the first run (#129):

- `observed_route` in `scripts/run_integration.py` no longer searches a Codex command's output for skill names; it reads the command text, and the output only to resolve a glob read through each printed file's frontmatter `name:` line.
- The archived manifests are not rewritten: those of the six X2 and X3 Codex plugin arms and of `X2-codex-canary` still list `causal-identification-review` and `decision-analysis`, which the fixed extractor does not.
  `results.md` and `scores-primary.md` already score routing from hand-confirmed loads, so no score changes.
- No prompt, fixture, or scoring rule changed; any arm run from here on records routes with the fixed extractor.

2026-11-25, harness change for I1–I4 (#128):

- The limit above held for the runs before it; I-cell runs from here on do not keep it.
  `scripts/run_integration.py` now stages I1–I4 in a neutrally named `int-arm-*` workspace and renders their data path as the relative `data`, as it does for this suite's cells, so neither the arm's name nor its condition reaches the prompt or the working directory.
- This file's cells, prompts, fixtures, and hashes are unchanged, and no count here changes.
