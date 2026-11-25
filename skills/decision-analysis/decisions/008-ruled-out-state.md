# 008 — A state that an observation rules out

Status: accepted, 2026-11-25 (proposed 2026-11-24; issue #114).

## Question

A decide record cannot say that a verified observation rules a state out.
`../references/decision-record-template.md` § Slot notes says "Odds and likelihood ratios are positive", and `tests/check_decision.py` fails any evidence row whose ratio's lower endpoint is at or below zero ("must parse as a positive ratio or range").
The symmetric case, an observation impossible under the other state, has no form at all: the checker's range pattern accepts only finite decimals, so an unbounded ratio cannot be written.
The forms left are a small positive ratio, which invents a magnitude no source supports, or the missing-ratio form, which discards decisive evidence.
No archived run has hit this; it is a gap in the format, and how often real use meets it is unknown.

Two constraints bind any answer.
The provenance rules live in `../SKILL.md` § Data Rules and § Numeric Policy, with their rationale in `003-numeric-provenance-policy.md`.
The binary scope, and the checker's refusal to approximate outside it, are `004-binary-scope.md`'s.

## Two observations that look alike

*Elimination.*
Let D be the accepted evidence, the whole observation as recorded, and H the proposition.
Under a stated model, D's likelihood ratio is P(D | H) / P(D | not-H).
D eliminates a state when its likelihood under that state is exactly zero and its likelihood under the other state is positive: the ratio is then exactly 0 or exactly unbounded.
The zero must come from a structural exclusion in the model (a logical or mechanical reason, such as the observed behaviour requiring a code path the suspected build does not contain), never from a frequency.
Imperfect detection does not by itself make the ratio finite: a process that records a true event with probability 0.8 and never records an event that did not occur gives 0.8 against 0, which is still unbounded.
What makes it finite is a positive probability of D under the eliminated state, which arises through false positives, or through failure of the assumptions behind the exclusion.
If D has zero likelihood under both states, conditioning on it is undefined; the disposition is model review (the binary model or its exclusion assumptions are wrong), never a ratio.

*Zero events in a finite sample.*
Under n independent Bernoulli trials with a common event rate p, zero events has probability (1 − p)^n, positive for every p below 1.
The ratio between two states is therefore finite and positive whenever each state assigns the zero count positive likelihood; that conditional is the whole claim, not "finite sample implies finite ratio".
For example, 100 independent weeks with p = 0.02 under H and p = 0.005 under not-H give, at zero events, (0.98 / 0.995)^100 ≈ 0.219.
A zero count alone supports an upper confidence bound on the rate: for zero of n Bernoulli trials the exact one-sided 95% bound is 1 − 0.05^(1/n) (≈ 0.0295 at n = 100), and under a Poisson model over n exposure units it is −ln(0.05)/n (≈ 0.0300), the "rule of three".
The sampling model must be named, because host-weeks drawn from the same hosts can share host-level failures and are then not independent trials.
A confidence bound is neither a state-conditional predictive probability, so it supplies no likelihood ratio by itself, nor evidence of a structural zero.
A zero count alone does not establish impossibility; it eliminates a state only when the model structurally requires an event on every trial under that state (p = 1) while p < 1 under the other, which is a structural exclusion, not a frequency.
The current positive-ratio rule stops a zero count from being recorded as elimination without such an exclusion, and any change must keep it doing so.

## Positions

The options below are compared at exact structural endpoints only: a ratio of exactly `0` or exactly unbounded.
Ranges that reach an endpoint are a separate choice, listed last.

*A. Exact endpoints inside the decide record.*
Allow an exact `0` or unbounded ratio in the Evidence table and carry it through the existing arithmetic.
What it would cost, through the machinery in `../SKILL.md` § Numeric Policy:

- **Posterior odds.** An exact zero ratio makes posterior odds exactly `0` and an unbounded one makes them unbounded; the template's "Odds and likelihood ratios are positive" excludes both, and slot grammar and checker parsing (`_RANGE`, `parse_range`) would need a token for infinity.
- **Joint evidence.** Two items, one impossible under each state, multiply to 0 × ∞; that is the both-zero case above and takes the model-review disposition, which `004`'s out-of-scope report already resembles.
- **Sweeps and crossovers.** At an exact endpoint every finite positive prior gives the same posterior (0 or unbounded), so no finite positive prior crossover exists and the prior clause can never flip the action; the sweep runs but tests nothing.
  The Crossover slot and the checker require a positive flip point (`_crossover_value`, and the sensitive-verdict check that fails a Crossover at or below zero).
- **Ties.** The threshold is strictly positive in the checker, so odds of exactly `0` never tie it, and unbounded odds need an ordering against it before the exact-comparison rule can apply.
- **Loss gates.** The loss ratio r is built from loss differences in both states (§ Numeric Policy), and one of those states can no longer occur, so r would weigh a difference that cannot affect the decision.
  Loss class follows sourcing, not state probability, so an owner-supplied loss in the eliminated state stays belief-grade and the loss cap does not fire on it; but a `sensitivity-only` loss there would still cap the verdict at `loss-sensitive`.
  The position therefore owes a ruling on whether r and the cap read losses in an eliminated state.
- **Validators.** The positivity check is a numeric guard in the dev checker, `tests/check_decision.py`.
  The shipped validator, `instruments/check_record.py`, parses no numeric ratio: it checks each evidence row's provenance class and the paired missing-ratio sentinels, but it also enforces the closed verdict set and the coupling between a verdict and its slots, so it changes whenever the chosen form adds a sentinel, a slot, a verdict, or a new verdict-to-slot coupling.

*B. Exact endpoints, decided by the one-state comparison.*
Record the exact `0` or unbounded ratio in the Evidence table, so the evidence keeps a numeric form, but take the verdict from the surviving-state comparison in C rather than from the odds arithmetic.
It costs the grammar and parsing work of A and a rule that an exact endpoint switches the verdict path, but spares the sweep, crossover, and tie rulings.

*C. A resolved proposition outside the odds form.* Recommended.
The record states D, the structural reason D is impossible under the eliminated state, and why D's likelihood under the surviving state is positive, and then leaves the odds form.
Resolving the state does not remove the decision: with S the surviving state, the expected loss difference given D is L(A, S) − L(B, S), and the record still has to compare it.
That comparison keeps the provenance rules, the missing-loss gate, and the uncertainty checks of § Numeric Policy, applied to the surviving-state losses.
Strict preference: a supported difference with one sign everywhere in its stated range names that action.
Tie: a difference of exactly zero prefers neither action.
Unsupported or sign-changing: a difference that lacks belief-grade losses, or whose stated range spans zero, returns the choice to the owner.
It cannot reuse the `dominated` clause as written: with losses A = (1, 0) and B = (1, 5) over (S, eliminated), `dominated` prefers A, though in the surviving state both cost 1 and the actions tie.
Likelihood ratios stay strictly positive, so the zero-count guard keeps working unchanged, and the sweeps, crossovers, ties, and loss ratio never meet `0` or infinity.

*D. Ranges that reach an endpoint.*
A range such as `0.5` to unbounded is not elimination, because it admits finite values, so C does not apply.
Whether it carries the posterior across the threshold depends on the prior and losses: at prior odds 1 and a threshold of 0.1 every ratio in it gives posterior odds above the threshold and the action never flips, while at a higher threshold it can; either way it would need its own sweep semantics.
`../SKILL.md` § Numeric Policy already counts a range endpoint that reaches the threshold as a flip there, and that rule would have to say what an endpoint at infinity does.
This is a separate owner choice and not part of the recommendation.

## What argues for the recommendation

Options A and B spend their cost making arithmetic produce an answer D already gave: once a state is impossible, priors, sweeps, and crossovers have nothing left to vary.
C adds no new number, so the provenance rules are untouched, and keeps `004`'s scope, since the both-zero case still lands on model review.
It also puts the burden where a reviewer can check it: the record must justify the structural exclusion in words, rather than writing `0` in a cell where it looks like any other ratio.
What it gives up is uniformity: a ruled-out record has a different shape from every other decide record, and whether an exclusion is structural is a judgement the checker cannot make.

On the voi route, if the state is settled and a signal would reveal only that same state, its gross information value is zero; a signal about the surviving-state losses, or about an exclusion assumption, is a different calculation.

## Contract changes each option owes

`../SKILL.md` § Routing reserves `out: direct` for bounded, unasserted, non-causal facts the records settle, and `decide` for a choice under uncertainty with a full record.
Keeping a resolved proposition on `decide` (A, B, or C) changes § The Decide Route: its blocks and its closed list of six verdicts would need a form for the surviving-state comparison, whether a seventh verdict, a sentinel set on the belief slots, or a ruling inside an existing verdict.
Routing it to `out: direct` would change § Routing, because a resolved causal proposition with a loss comparison is not a bounded non-causal fact, and would drop the record that carries the comparison's provenance.

## Reversing the recommendation

If the owner prefers A, the work is:

1. Decide in § Numeric Policy that an exact `0` or unbounded ratio is admissible only under the elimination condition above, that a zero count alone never establishes impossibility (it qualifies only when a structural exclusion in the model gives it zero likelihood under one state), and that the both-zero case goes to model review.
2. Give the template's slot notes a spelling for an unbounded endpoint and for zero and unbounded posterior odds.
3. Rule, in § Numeric Policy, what each verdict clause and the exact-tie rule do at those endpoints, and whether r and the loss cap read losses in an eliminated state.
4. Change the parse and positivity checks in `tests/check_decision.py` (prior odds, evidence ratio, crossover, threshold) to match, with fixtures for each endpoint, and change `instruments/check_record.py` wherever the form adds a sentinel, a slot, a verdict, or a verdict-to-slot coupling.
5. Measure DA-S12 and DA-S13 and every existing cell the edited sentences reach.

Reversing to B is steps 1, 2, 4, and 5 plus the surviving-state comparison of C, since B also changes the record form and the verdict path; D is a separate change on top of either.

## Open owner questions

- Accept C, or reverse to A or B?
- Under C, which form carries the surviving-state comparison in § The Decide Route: a seventh verdict, a sentinel set on the belief slots, or a ruling inside an existing verdict?
- Does a resolved proposition stay on `decide`, or does § Routing change to send it elsewhere?
- When an exclusion rests on an assumption (the build manifest is complete), is the ratio exact, or does the assumption's failure probability make it finite?
- Is D wanted at all?

## Reopening condition

A measured arm shows agents recording a zero count with no structural exclusion as elimination under whichever form ships, or a real decision arrives where the eliminated state cannot be cleanly separated from a surviving one and the chosen form cannot express it.

## Where the rules live

Nothing here is a rule yet.
Once the owner decides, semantics go in `../SKILL.md` § Numeric Policy, routing in § Routing, the record shape and verdict list in § The Decide Route, the representation in `../references/decision-record-template.md` § Slot notes, and enforcement in `tests/check_decision.py` (and `instruments/check_record.py` if the form adds a sentinel, a slot, a verdict, or a verdict-to-slot coupling), each in its one home; this record will point at them.
The paired scenario cells are DA-S12 and DA-S13 in `../tests/scenarios.md`.

## Decision, 2026-11-25

The owner accepts option C: a resolved proposition outside the odds form, recorded as a seventh decide verdict `resolved`, staying on the `decide` route, with option D deferred.
The sections above stay as the proposal's history; this section and § Record contract below are the disposition.
The owner's reasons, as the recommendation gave them: A and B spend their cost making arithmetic reproduce an answer the observation already gave, and A also creates undefined products (0 × unbounded); a verdict is what both checkers key on, so the coupling is enforceable, while `out: direct` would drop the loss comparison's provenance.

The five open owner questions, in order:

1. *Accept C, or reverse to A or B?*
   C is accepted; A and B are not adopted, and § Reversing the recommendation stays as the record of what either would cost.
2. *Which form carries the surviving-state comparison?*
   A seventh verdict, `resolved`, not a sentinel set on the belief slots and not a ruling inside an existing verdict.
   The surviving-state comparison names an action only when supported losses give it a strict advantage throughout the stated range; it reads `no preference` for an exact tie; it returns the choice to the owner when losses are unsupported or the range reaches zero without being an exact tie.
   Precedence: `resolved` is decided before the statewise clauses, and the existing `dominated` clause must not fire on losses in the eliminated state.
3. *Does a resolved proposition stay on `decide`?*
   It stays on `decide`; § Routing does not send it elsewhere.
   `out: adjudicate` still outranks `decide`: `resolved` applies when the excluding evidence is already verified and in hand, not when the exclusion is itself in dispute.
4. *When an exclusion rests on an assumption, is the ratio exact?*
   An exclusion is exact, conditional on the stated model, only when the whole accepted observation is impossible in one state and possible in the other.
   If doubt about an assumption gives the observation positive likelihood in both states, it is not elimination: use the ordinary positive-ratio form when a ratio is supportable, and the missing-support form otherwise.
   If the observation is impossible in both states, the disposition is model review, never a verdict.
   The draft of this ruling said any stated failure probability on an assumption defeats exactness; the adopted correction is that what matters is whether the failure makes the observation possible under the excluded state.
5. *Is D wanted at all?*
   Not now: D is deferred.
   A range reaching an endpoint stays inexpressible, as it is today, and the positive-ratio rule keeps rejecting it.

The positive-ratio rule is unchanged: likelihood ratios stay strictly positive in every record, so `tests/test_check_decision.py`'s zero-ratio regression keeps failing a zero written as elimination.

## Record contract

This section fixes the record shape `resolved` takes, for the change to the two checkers, the template, and `../SKILL.md` that implements it.
It specifies what that change will put where and is not a home for any rule: once the change lands, each rule lives where the list below says, and this section is history.

- `../SKILL.md` § Numeric Policy: the elimination condition (answer 4 above), the zero-count guard, the both-impossible disposition, the surviving-state comparison (answer 2), and the precedence of `resolved` over the ordered rule's statewise clauses, each once.
- `../SKILL.md` § The Decide Route: `resolved` in the closed verdict list, the Resolution block, and the Recommended action reading under `resolved`, each pointing at § Numeric Policy.
- `../SKILL.md` § Routing: only what answer 3's adjudication-first ruling needs.
- `../references/decision-record-template.md`: the Resolution block skeleton, and § Slot notes for its labels and for the sentinel.
- `tests/check_decision.py` and `instruments/check_record.py`: enforcement, split as § Who enforces what says.

### Shape

A `resolved` record keeps every existing section and every existing slot label, in the template's order.
It adds one section, `## Resolution`, placed between `## Decision-state model` and `## Evidence and update`, carrying these top-level bullets in this order, labels spelled exactly:

```markdown
## Resolution

- Excluded state: <proposition true or proposition false>
- Surviving state: <proposition true or proposition false, the other one>
- Accepted evidence: <the whole observation as recorded, with the file or source of each part>
- Structural exclusion: <the logical or mechanical reason the accepted evidence is impossible under the excluded state>
- Exclusion assumptions: <the assumptions of the stated model the exclusion rests on>
- Surviving-state possibility: <why the accepted evidence is possible under the surviving state>
- Surviving-state losses:

  | action | loss | provenance |
  | --- | --- | --- |
  | <action A> | <loss or range> | <class> |
  | <action B> | <loss or range> | <class> |
```

The template carries this block as its own fenced skeleton after the decide skeleton, introduced as used only under the `resolved` verdict.

Slot values:

- `Excluded state:` and `Surviving state:` each read exactly `proposition true` or `proposition false`, naming a state of the Proposition slot; the two differ.
  `Surviving state:` reads exactly `none` when the accepted evidence is impossible under both states, and such a record is a model-review finding, never a verdict.
- `Accepted evidence:`, `Structural exclusion:`, `Exclusion assumptions:`, and `Surviving-state possibility:` are prose, non-empty, and never `none`.
- `Surviving-state losses:` heads a table with exactly the columns `action`, `loss`, `provenance` and exactly two data rows.
  Each `action` cell is one of the two actions exactly as the Actions slot writes them, each appearing once.
  Each `loss` cell is a nonnegative decimal or a `<low>–<high>` range with low ≤ high, in the grammar of the template's numeric slots; zero is allowed, because a loss is not an odds.
  Each `provenance` cell is one class from § Numeric Policy.
  A loss nobody supplied writes `none supported` in both its `loss` and `provenance` cells, the missing-ratio form's spelling.

The sentinel is `not applicable — resolved`, with an em dash, written bare and replacing the whole value.
Under `resolved` it fills exactly these existing slots, and it is valid nowhere else in any record:

| slot | section |
| --- | --- |
| Favored if true | Decision frame |
| Loss ratio | Decision frame |
| Decision threshold (posterior odds) | Decision frame |
| Prior odds | Evidence and update |
| Independence | Evidence and update |
| Posterior odds | Evidence and update |
| Prior class swept | Robustness |
| Loss range swept | Robustness |
| Crossover | Robustness |
| every Evidence table row's LR cell and provenance cell, together | Evidence and update |

No existing slot is absent under `resolved`.
Every other existing slot keeps its ordinary form: Route `decide`, Actions, Decision owner, Reversibility, Deadline or forcing event, the Consequences table over both states, the Decision-state model's six slots, Conditions, and the three Handoff slots.
The Evidence table keeps at least one row; each row's item and source cells are filled, the source cell naming where the item comes from.

The verdict line is `- Verdict: resolved`, bare.

### Recommended action

The existing `- Recommended action:` slot carries the three outcomes of answer 2, in the spellings it already uses:

- one of the two actions exactly as the Actions slot writes them, when both `provenance` cells of the Surviving-state losses table are belief-grade (`user-elicited` or `externally-sourced`) and that action's loss interval lies strictly below the other's, its high endpoint below the other's low endpoint;
- `no preference`, when both provenance cells are belief-grade and the two losses are equal points;
- `returned to owner` in every other case: a provenance cell that is not belief-grade or reads `none supported`, or loss intervals that overlap or touch without being equal points.

Loss comparisons are exact, each decimal read as an exact fraction, as the dev checker already reads thresholds.
Only the surviving-state losses enter; the Consequences table's eliminated-state column plays no part.

### Causal basis

The causal-basis gate in `tests/check_decision.py` is unchanged: a `causal` Claim class needs an Identification basis other than `NONE`, and then Identification conditions other than `none`.
Under `resolved`, Identification basis may read exactly `structural exclusion — see Resolution`, and Identification conditions then restate the Exclusion assumptions as explicit conditions.
That basis value is valid only under `resolved`; an existing licensing basis (the causal-wording bar or an `identified-if` disposition) is also accepted there.

### Plan stage and `--final`

The dev checker has no plan-stage mode: it reads every record as complete, as it does today.
The shipped validator keeps its two modes.
In its default mode a record still carrying template placeholders or `pending` is in progress and completeness findings are suspended, as today, so a `## Resolution` section written from the skeleton before the verdict is known is not a finding.
Otherwise, and always under `--final`, the shipped validator applies the `resolved` requirements when the Verdict slot is filled with `resolved`, and the outside-`resolved` prohibitions when it is filled with another verdict; a slot still in template state is skipped in default mode and is a finding under `--final`, as in every coupling check today.

### Who enforces what

The shipped validator, `instruments/check_record.py`, checks structure and coupling and parses no number:

1. `resolved` is in `DECIDE_VERDICTS`.
2. Under `resolved`, `## Resolution` is present and non-empty; its six inline slots are present and non-empty (under `--final`, filled); `Surviving-state losses:` heads a table with the columns `action`, `loss`, `provenance` and at least one data row as wide as its header.
3. Under `resolved`, `Excluded state:` and `Surviving state:` read the closed tokens and differ, and none of the four prose slots reads `none`.
4. Under `resolved`, each slot and cell in the sentinel table reads the sentinel exactly; any other value, `none needed` and `none supported — see Robustness` included, is a finding.
5. Under `resolved`, Recommended action is one of the two framed actions, `no preference`, or `returned to owner`, and it is `returned to owner` when any Surviving-state losses `provenance` cell is not belief-grade.
6. Under any verdict, `Surviving state: none` is a finding whose text says the disposition is model review, never a verdict.
7. Under any verdict other than `resolved`, a `## Resolution` section, or the sentinel in any slot or cell, is a finding; `no preference` stays a finding outside `indifferent` and `resolved`.
8. Every other check is unchanged for every other verdict, and the provenance vocabulary check reads the sentinel as a sentinel, not as an unknown class.

The dev checker, `tests/check_decision.py`, enforces the same structure and adds arithmetic and provenance:

1. Everything in the shipped list, with the Resolution labels held in a label constant of their own, required only under `resolved`.
2. The Surviving-state losses table has exactly two data rows, the two framed actions each once, each loss parsing as a nonnegative number or ordered range, and each provenance a class or the paired `none supported`.
3. The recommendation matches the table per § Recommended action: a named action must be the strictly lower one, `no preference` needs equal belief-grade points, and `returned to owner` is required, not merely allowed, in every other case.
4. Under `resolved`, the ordered rule, the posterior recomputation, and the statewise sentinel checks do not run: `resolved` is dispatched before them.
5. The causal-basis gate holds per § Causal basis, and `structural exclusion — see Resolution` outside `resolved` is a finding.
6. Every Evidence LR cell that is not the sentinel still parses as a strictly positive number or range under every verdict, so a `0` or unbounded ratio fails everywhere.

A human reviewer checks what neither checker can: that the exclusion is structural (logical or mechanical) and not a frequency, a zero count included; that the accepted evidence is the whole observation; that the exclusion is not itself in dispute, which would route `out: adjudicate`; and that the Exclusion assumptions are the ones the exclusion actually needs.

### Worked example (DA-S12)

The DA-S12 shape from `../tests/scenarios.md`, with an illustrative owner loss table over (H, not-H) of roll back = (2, 4) and keep with a hotfix = (8, 1), until the fixture fixes real numbers.
Across both states neither action dominates; in the surviving state, not-H, the hotfix costs 1 against 4, so the record names it.

```markdown
# Decision Record: roll back to build 411 or keep build 412 with a hotfix after the db-03 partition loss

## Decision frame

- Route: decide
- Actions: roll back to build 411 vs keep build 412 with a hotfix
- Decision owner: the storage on-call lead
- Reversibility: either action is undone by one redeploy, about an hour
- Deadline or forcing event: noon today
- Consequences:

  | | compaction job caused the loss true | compaction job caused the loss false |
  | --- | --- | --- |
  | roll back to build 411 | the faulty job is removed | a working build is withdrawn and the disk fault stays unaddressed |
  | keep build 412 with a hotfix | the faulty job keeps running until the hotfix | the build stays and the hotfix work goes to the disk fault |

- Favored if true: not applicable — resolved
- Loss ratio: not applicable — resolved
- Decision threshold (posterior odds): not applicable — resolved

## Decision-state model

- Proposition: the build-412 compaction job caused the loss of the orders partition on db-03
- Residual reading: something other than that job caused it, including causes nobody named
- Claim class: causal
- Identification basis: structural exclusion — see Resolution
- Identification conditions: the storage topology, process accounting, and deploy log are complete for the incident window; the compaction job modifies data only on the host where it runs
- Ledger mapping: none

## Resolution

- Excluded state: proposition true
- Surviving state: proposition false
- Accepted evidence: the orders partition on db-03 was lost overnight, and neither db-03's process accounting nor the deploy log shows build 412 or its compaction job running on db-03 (packet files: process accounting, deploy log)
- Structural exclusion: the partition lived only on db-03's local disk (packet file: storage topology), and the compaction job can modify data only by executing on the host that holds it (packet file: compaction design), so it could not have touched a partition on a host where it never ran
- Exclusion assumptions: the storage topology, process accounting, and deploy log are complete for the incident window, and the design document's locality claim holds for build 412
- Surviving-state possibility: a loss without the job is possible under not-H; db-03's device log records a disk fault in the window (packet file: db-03 device log)
- Surviving-state losses:

  | action | loss | provenance |
  | --- | --- | --- |
  | roll back to build 411 | 4 | user-elicited |
  | keep build 412 with a hotfix | 1 | user-elicited |

## Evidence and update

- Prior odds: not applicable — resolved
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | partition lost while build 412 never ran on db-03 | not applicable — resolved | not applicable — resolved | packet files: process accounting, deploy log; see Resolution |

- Independence: not applicable — resolved
- Posterior odds: not applicable — resolved

## Robustness

- Prior class swept: not applicable — resolved
- Loss range swept: not applicable — resolved
- Crossover: not applicable — resolved

## Verdict

- Verdict: resolved
- Recommended action: keep build 412 with a hotfix
- Conditions: the exclusion assumptions in Resolution, and the owner's surviving-state losses of 1 and 4

## Handoff

- Open factual disputes: none
- Identification gaps: none
- VoI question: none
```

Slot by slot, what each checker accepts and rejects on this example:

| slot | both checkers accept | both checkers reject | the dev checker alone also rejects |
| --- | --- | --- | --- |
| the nine sentinel slots | the bare sentinel | any number, `none needed`, `none stated`, `single item`, `none supported — see Robustness`, the sentinel with an annotation | — |
| Evidence row LR and provenance | the sentinel in both cells | the sentinel in one cell only; a class or a number in either | a `0` or other non-positive ratio, as under every verdict |
| Claim class, Identification basis, Identification conditions | `causal`, `structural exclusion — see Resolution`, conditions restated | — | that basis with conditions `none`; `causal` with basis `NONE` |
| Excluded state, Surviving state | `proposition true` and `proposition false`, differing | equal values or any other token; `Surviving state: none`, as model review | — |
| Accepted evidence, Structural exclusion, Exclusion assumptions, Surviving-state possibility | non-empty prose | missing, empty, or `none` | — |
| Surviving-state losses | the two framed actions, decimal losses, belief-grade classes | a missing table or column | a third row, an action not in Actions, an unparseable or negative loss, an unpaired `none supported` |
| Recommended action | `keep build 412 with a hotfix` | a value outside the three forms; anything but `returned to owner` when a class is not belief-grade | `roll back to build 411`, `no preference`, or `returned to owner`, since 1 lies strictly below 4 under belief-grade losses |
| Verdict | `resolved` | — | — |

### Choices made in the contract

1. *Every existing slot stays, filled with a sentinel, rather than going absent.*
   The shipped validator's `REQUIRED_SLOTS` and the dev checker's `DECIDE_LABELS` require every slot in every decide record, and `test_required_slots_exist_in_shipped_templates` and `tests/test_template_parity_da.py` tie both to the template; absent slots would make both required-slot sets verdict-dependent.
   Cost if wrong: nine sentinel lines per record, which an agent may annotate or replace and then fail; the DA-S12 arm measures that.
2. *A new sentinel, `not applicable — resolved`, not `none needed`.*
   The shipped validator reserves `none needed` for `dominated` and `indifferent` and flags it under any other verdict; reusing it would weaken that check, and answer 2 says `dominated` must not fire here.
   Cost if wrong: one more sentinel to learn; because of the em dash, implementers must compare the whole stripped value before the dev checker's `_bare` split, as it already does for `none supported — see Robustness`.
3. *Every Evidence row takes the sentinel in both cells; no row keeps a positive ratio under `resolved`.*
   Mixed rows would leave odds-form numbers in a record that has left the odds form, with nothing consuming them.
   Cost if wrong: corroborating evidence with a supportable ratio is recorded only by name and source, so if the exclusion later fails its ratio has to be reconstructed.
4. *The surviving-state comparison reads a new two-row loss table, not the Consequences table or the Loss ratio slot.*
   The Consequences table holds prose outcomes, and the loss ratio r is built from both states.
   Cost if wrong: the surviving state's outcomes appear twice (Consequences prose and the table), and no checker compares them.
5. *Unsupported losses are spelled with the paired `none supported`, borrowed from the missing-ratio form.*
   One spelling for "no supportable number" across the record.
   Cost if wrong: a reader may take it for the missing-ratio form; the column header disambiguates.
6. *The model-review disposition is encoded as `Surviving state: none`, failing under every verdict.*
   Answer 4 says the both-impossible case is never a verdict, so the record must fail whatever it claims, and a slot value gives both checkers something to key on.
   Cost if wrong: an agent that sees both states excluded may write no Resolution section and an ordinary verdict, which no checker catches; that is a reviewer's call, as whether an exclusion is structural is.
7. *Precedence over `dominated` is enforced structurally: a `## Resolution` section under any verdict other than `resolved` fails.*
   Neither checker computes statewise domination from losses (the dev checker's docstring disclaims it), so there is no arithmetic `dominated` clause to switch off; the enforceable form is that a record stating an exclusion must take `resolved`.
   Cost if wrong: a record that omits the Resolution section and takes `dominated` on eliminated-state losses passes both checkers.
8. *Identification basis may read `structural exclusion — see Resolution`.*
   DA-S12's proposition is causal, and the gate needs a non-`NONE` basis; the exclusion is what licenses the causal conclusion there, and its assumptions become the Identification conditions, so the gate's second clause still bites.
   Cost if wrong: an exclusion becomes a self-licensing identification basis; if the owner wants a causal `resolved` record to need the causal-wording bar or an `identified-if` disposition as well, the value is withdrawn and the gate stays as it is.
9. *The Resolution labels are a label constant of their own in the dev checker, required only under `resolved`, and `tests/test_template_parity_da.py` compares the template with the union of the checker's label sets.*
   The parity test collects every top-level template bullet, so the new labels must be on the checker side, and adding them to `DECIDE_LABELS` would require them in every decide record.
   Cost if wrong: none to behaviour; the parity test unions two checker-side sets.
10. *The shipped validator checks that unsupported losses force `returned to owner`, but not strictness or ties.*
    It parses no number (§ Positions, A), so the strict-advantage and exact-tie readings are the dev checker's alone.
    Cost if wrong: a shipped-validator pass can carry a named action on overlapping ranges, as it can today carry a `robust` verdict whose arithmetic does not hold.
11. *`Exclusion assumptions:` may not read `none`.*
    Answer 4 makes exactness conditional on the stated model, so there is always a model to name.
    Cost if wrong: a purely logical exclusion has to state the binary model as its assumption.

### The implementing change's tests, decided by the contract

- `test_resolved_passes_with_exclusion_and_strict_surviving_preference`: § Shape, § Recommended action's first case, and the worked example.
- `test_resolved_passes_in_the_other_direction`: § Shape, with `Excluded state: proposition false` and `Surviving state: proposition true`.
- `test_resolved_exact_tie_reports_no_preference`: § Recommended action's second case.
- `test_resolved_range_touching_zero_returns_to_owner`: § Recommended action's third case, intervals that touch.
- `test_resolved_with_unsupported_losses_returns_to_owner`: § Recommended action's third case, a provenance cell not belief-grade or `none supported`.
- `test_resolved_without_a_structural_exclusion_fails`: shipped items 2 and 3 (no Resolution section, or `Structural exclusion:` missing, empty, or `none`).
- `test_resolved_carrying_an_odds_slot_fails`: the sentinel table and shipped item 4.
- `test_evidence_impossible_under_both_states_fails_as_model_review`: `Surviving state: none` and shipped item 6.
- `test_dominated_does_not_fire_on_losses_in_the_eliminated_state`: shipped item 7 and choice 7 (a Resolution section under `dominated` fails), with the same record passing as `resolved` with `no preference` on losses A = (1, 0) and B = (1, 5) over (surviving, eliminated), by § Recommended action's second case.
- `test_ordinary_records_are_unchanged`: shipped items 7 and 8, and dev item 6.
- `test_resolved_is_an_accepted_decide_verdict`: shipped item 1.
- `test_resolved_requires_each_contract_statement`: shipped items 2 and 3.
- `test_resolved_rejects_posterior_odds_and_crossover`: shipped item 4.
- `test_resolved_recommendation_coupling`: shipped item 5.
- `test_other_verdicts_keep_their_coupling`: shipped items 7 and 8.
