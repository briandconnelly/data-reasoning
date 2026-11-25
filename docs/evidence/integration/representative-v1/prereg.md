# Representative suite v1 — preregistration

Issue #115.
Written 2026-11-24, before any arm, canary included, ran.
Everything below is fixed before the canaries; any change after them is a dated note at the end, never an edit above it.

## Question

On routine requests and on challenge tasks, does a clean plugin install change the user's answer compared with the same host and model given no plugin, by enough to justify the plugin's procedure and its context cost?
The adversarial catalogs cannot answer this: by their own rule a scenario a baseline passes is too easy for them.
This suite keeps tasks a baseline may pass, because "the plugin makes no difference" is one of the results it exists to detect.

## Cells

Prompts are frozen by the SHA-256 of the prompt text with `{DATA}` left unexpanded, as `scripts/run_integration.py` `prompt_sha256` computes it; `scripts/test_run_integration.py` fails if a prompt and its hash here disagree.
`{DATA}` is replaced with the staged fixture path.
No prompt names a skill, a route, a method, or the trap its cell sets.
Routine prompts avoid the skills' own vocabulary (explore, investigate, hypothesis, decision, evidence, causal, uncertainty).

Fixtures are built by `scripts/representative/generate.py` (seed 20261124) into `fixtures/` beside this file.
Each has a validator under `scripts/representative/` that recomputes its discriminating property from the files, byte-compares a fresh build, and runs as a prek hook; `scripts/representative/test_validators.py` proves each validator fails on a degenerate copy.

| Fixture file | SHA-256 |
| --- | --- |
| `r-sales/orders.csv` | `8828d775e7566bd80f44da81acfbfd205b9f75aa78a1556e3037503fcbf9e648` |
| `x1-supplier/acme_history.csv` | `191979a86e7aac3b2dfced353f3c4e0182fbcc24ab73861d456fd8531b049a3c` |
| `x1-supplier/brightline_trial.csv` | `5fecbcae033bc3660824b255eb483b7a5f54c527b9abf600326ba886a0d71164` |
| `x1-supplier/contract_terms.md` | `9f75453aada6ef191b7a3c26679594858d17952269026e08c216f99588dcc6f8` |
| `x2-forecast/analyst_model.py` | `e2a1dde3f836d59fbde611aa369f47be00c93fa9f142a7ea863fc273892ada34` |
| `x2-forecast/analyst_notes.md` | `e4fd4e40fe56ac4ecadfe7ea5ae6ed849febf92d0a63e2062c70e8690793db52` |
| `x2-forecast/daily_tickets.csv` | `bc7a603a1eb8f797aa4e7ffc7f82b82b2049489f2ef0f2738db3a31cbd1369bd` |
| `x3-churn/holdout_scores.csv` | `139bb2c7f5a531be624bbd213f77dce571c1d9d9b70f01cdc23603473371ebce` |
| `x3-churn/models.md` | `a66c4f6d04fdbc94ae396d90325f84144e10911a1959f3768d1659a0f0f5df40` |

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

Fixture: `fixtures/x1-supplier/`: Brightline's trial (1 defective of 150), Acme's history (1,000 of 50,000), and contract terms (100,000 units, $15 per defective unit, a $1,000,000 penalty if the annual defect rate exceeds 3%).
Prompt: "We have to pick one supplier for all 100,000 units next year: stay with Acme or move to Brightline. Brightline's trial batch, our Acme history, and the contract terms are in `{DATA}`. Brightline's trial had fewer defects than Acme usually has. Which supplier should we sign with?"
Prompt SHA-256: `937402c9bfdda5b78cc3d919319d5824969424b519107ad2fdd60bcfba3ec18e`.
Ground truth: treating the trial rate (0.67%) as known costs Brightline $10,000 against Acme's $30,000, so a point estimate picks Brightline.
Carrying the trial's uncertainty, a beta posterior gives Brightline a 5.7% (uniform prior) or 2.8% (Jeffreys prior) chance of exceeding 3%, so expected cost is $76,769 or $42,607 against Acme's $30,029 or $30,014: Acme.
Designed route: `decision-analysis`.

### X2 — a random split passes and a backtest fails (challenge)

Fixture: `fixtures/x2-forecast/`: two years of daily ticket counts with weekly and annual seasonality, the analyst's same-weekday nearest-neighbour model, and notes reporting its random-split error.
Prompt: "Our analyst built a model for daily support ticket volume; the notes, code, and two years of data are in `{DATA}`. They report under 4% error on held-out days. We want to use it to set staffing for each of the next three months, and staffing works if forecasts are within 10% on average. Can we use it?"
Prompt SHA-256: `ce4b24272b603538ce9253a4de506e6a0c06fc291bf0b1800efe3ec15fcfc48e`.
Ground truth: random 20% holdout MAPE 3.6%; a rolling-origin backtest forecasting each of the last four 91-day quarters from the data before it gives 23.4%, 5.2%, 33.9%, 7.8%, mean 17.6%.
The model cannot be used as evaluated: the random split measures interpolation between neighbouring days, not forecasting three months ahead.
Designed route: `hypothesis-driven-analysis`.

### X3 — two metrics pick different winners (challenge)

Fixture: `fixtures/x3-churn/`: 10,000 holdout customers (13.8% churned) with each model's churn probability.
Prompt: "We have two candidate churn models scored on last quarter's holdout customers, with who actually churned: `{DATA}/holdout_scores.csv`. Our retention team can call 500 customers a month. Which model should we deploy?"
Prompt SHA-256: `4e1cf77f40205682bbd002246e2566d2d24ac40010db11da3fbff7a2f662fcbe`.
Ground truth: accuracy at a 0.5 threshold picks A (84.6% against 79.5%); precision among each model's top 500 picks B (60.4% against 34.6%).
For a team that can call 500 customers, B.
Designed route: `hypothesis-driven-analysis`; a first load of `decision-analysis` that hands the comparison to it is also on route.

## Conditions

Seven cells × two conditions (plugin, no plugin) × two hosts (Claude Code, Codex) × n=3 = 84 scored arms.
One canary per cell per host is run and excluded from scoring: 7 in B3 Step 4 on one host and 7 in C1 on the other.
Until R3 and R4 have prompts, the runnable count is 60 scored arms and 5 canaries per host.

Each condition is set up exactly as `docs/evidence/integration/2026-11-17-full-catalog/prereg.md` § Conditions sets it up, through `scripts/run_integration.py`, which this suite extends and does not change for I1–I4.

Every arm records its host version (`host_version` in the manifest) and model.
Host version drift moves activation (#111), so no comparison crosses host versions silently: a comparison between arms whose host versions differ says so beside the comparison, and a condition pair (plugin against no plugin) for one cell on one host is run on one host version or reported as unpaired.

## Scoring

Scored per arm from the archived transcript, final message, and the files left in the arm's workspace.
"Results" means the first tool output containing a value computed from the task's data (a count, mean, estimate, or model output); reading a schema, header, or file listing is not a result.
A skill load is a `Skill` tool call or a read of that skill's `SKILL.md` (Claude Code), or a read of that skill's `SKILL.md` from the installed plugin cache (Codex), as `observed_route` in `scripts/run_integration.py` extracts them, confirmed by hand.

This section is the single home of the six column definitions below; other files point here by column name.

- **First activation.**
  Pass: the first data-reasoning skill load is a skill on the cell's designed route.
  Fail: the first load is off the designed route, or there is no skill load at all, recorded as `none`.
  Not applicable: the cell's designed route is none (R1, R2), where loads are scored under unnecessary ceremony instead.
- **Handoff taken.**
  Scored once per handoff in the designed route; no cell in this version designs one, so it is `n/a` for X1–X3 and R1–R2, and R3 and R4 state theirs when frozen.
  Pass: the downstream skill is loaded after the upstream skill; a single tool call that loads both passes and is annotated `batched`.
  Fail: the downstream skill is never loaded.
  Not applicable: no handoff designed, or the upstream skill never loaded.
- **Record written: `<record>`.**
  One column per record a skill on the observed route requires (`decision-analysis`: decision record; `hypothesis-driven-analysis`: ledger; `exploratory-data-analysis`: exploration log; `causal-identification-review`: identification review).
  Pass: at the end of the arm a workspace file exists that `instruments/check_record.py` recognizes as that record kind (exit 0 or 1, not 2).
  Its structural findings are reported beside the pass, not scored.
  Response text standing in for the file passes only where the owning skill allows it when no file tools exist and the host had none; no arm in this suite lacks file tools.
  Fail: no such file, including a record that appears only in the final message.
  Not applicable: the requiring skill was not loaded.
- **Record written before results: `<record>`.**
  One column per record scored pass on record written.
  Pass: the tool call that first creates the record's file precedes the first result in the transcript.
  Fail: it follows the first result.
  Not applicable: record written is fail or not applicable.
  Later edits do not change this column.
- **Evidence boundary (E).**
  Read from the final message only, for every arm, plugin or not.
  R1, R2: `n/a`.
  X1: Brightline's trial rate is not treated as its known rate; the answer says the trial is too small to rule out a rate above the 3% clause, and that this risk drives the choice.
  X2: the answer says the random-split figure does not measure forecasting months ahead, and either reports a time-ordered evaluation that misses the 10% bar or states that the held-out figure cannot support the claim.
  X3: the answer says accuracy at a threshold is not the measure for a 500-call limit and compares the models at the top 500 or an equivalent ranking measure at that limit.
- **Task (C).**
  Read from the final message only.
  R1: 99.
  R2: all four store means within 0.01 of the ground truth.
  X1: Acme, or "do not switch on this trial" with Acme for the year.
  X2: no, not for three-month staffing as evaluated.
  X3: B.

Three further measures, per arm:

- **Unnecessary ceremony.**
  Scored on R1 and R2 only, `n/a` elsewhere.
  Fail when any of these occurs before or instead of the direct answer: a data-reasoning skill load, a record file written, a preregistration or plan the user did not ask for, or a stop for authorization or clarification.
  Pass otherwise.
  A skill load that routes straight out to a direct answer with none of the rest still fails; this column counts the load as the cost.
- **Wall-clock latency.** `duration_s` from the arm's manifest.
- **Loaded context tokens.**
  Claude Code: from the final `result` event's `usage`, `input_tokens + cache_creation_input_tokens + cache_read_input_tokens`.
  Codex: the sum over `turn.completed` events of `usage.input_tokens`, cached tokens included.
  Extracted by the scorer from the archived `.jsonl`; reported, not thresholded.

Record columns, answer columns, and the three measures are reported side by side and never combined into one score.

### Scorers

Primary: the dispatching Claude Code session (the orchestrator), unblinded, scores every arm.
Blind: `openrouter/google/gemini-3.1-pro-preview` through amicus, a model that runs no arm, scores E and C on every arm from final messages with skill names, record headings, and condition redacted.
Disagreements are reported, not reconciled.
The results record carries its `Scorer:` line as `skills/hypothesis-driven-analysis/tests/PROTOCOL.md` § Who scored it requires.

## Verdicts

Reported per host and per cell; no verdict pools Claude Code and Codex, and challenge cells are reported apart from the routine and representative cells.
At n=3 nothing is a rate; "pass" below means at least 2 of 3 arms and "fail" at most 1 of 3.

| Plugin on E and C | No plugin on E and C | Verdict for that cell and host |
| --- | --- | --- |
| pass | fail | the plugin improves the answer |
| pass | pass | the plugin makes no difference: the baseline already does this |
| fail | fail | the plugin makes no difference: neither condition does this, a gap |
| fail | pass | a regression attributable to the plugin |

Across the suite, "the plugin makes no difference" is the verdict on a host when every scored cell lands in one of the two no-difference rows.
A cell where E and C disagree within a condition is reported as split, with each column's counts.

## What would change a maintenance decision

Stated before any arm:

- **X2, X3 → D1 (#116).**
  If plugin arms fail E or C on X2 (or X3) on either host, D1 writes the on-demand reference for that cell's method.
  If plugin arms pass E and C on both hosts, #116's row for that cell closes as "no change, measured".
- **R1, R2 → descriptions.**
  If at least 3 of the 6 plugin arms on R1 and R2 on a host fail unnecessary ceremony, narrowing the description of each skill they loaded is justified, through the unfreeze procedure of `skills/exploratory-data-analysis/decisions/006-description-freeze-until-measured.md`.
  At most 1 of 6 leaves the descriptions unchanged.
- **Activation (#104, #108, #111).**
  If the suite verdict on a host is "the plugin makes no difference", chasing automatic activation on that host is deprioritized: activating more often would not change answers on these tasks.
  If a challenge cell's plugin arms that passed first activation pass E while those that did not fail it, activation work on that host is justified.

## Limits fixed in advance

- One Claude model and one Codex model.
- Codex plugin arms run without the record-checking hook, as in the full-catalog suite.
- Synthetic challenge fixtures test whether a known trap is caught, not how often real users meet it; R3 and R4 are the representative sample and are not yet frozen.
- The routine prompts were written by the plugin's maintainers' agent, outside the skills' vocabulary, which reduces but does not remove the risk that they route better than a user's words would.

## Notes after writing
