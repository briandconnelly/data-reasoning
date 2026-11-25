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
It specifies what that change will put where and is not a home for any rule.
Revised 2026-11-25, before any implementation, after a cross-model design review; the first draft (every existing slot kept and filled with a sentinel) was never committed to any checker and is not kept.

- `../SKILL.md` § Numeric Policy: the elimination condition (answer 4 above), the zero-count guard, the both-impossible disposition, the surviving-state comparison (answer 2), the precedence of `resolved` over the ordered rule's statewise clauses, and what qualifies a structural exclusion to license causal wording (§ Causal basis below), each once.
- `../SKILL.md` § The Decide Route: `resolved` in the closed verdict list, the resolved record's blocks, the Recommended action reading under `resolved`, and the model-review handoff (§ Model review below), each pointing at § Numeric Policy for meaning.
- `../SKILL.md` § Routing: only what answer 3's adjudication-first ruling needs.
- `../references/decision-record-template.md`: the resolved skeleton, and § Slot notes for its labels and value grammar.
- `tests/check_decision.py` and `instruments/check_record.py`: enforcement, split as § Who enforces what says.

### Instruction to the implementing change

In the same change that puts these rules in `../SKILL.md`, the template, and the tests, reduce this record to the selected option, its rationale, the choices below, and pointers to each rule's home.
`decisions/` ships in the installed tree, so a contract left here after that change is a second statement of every rule (HDA decision 004).

### Shape

A `resolved` record is a complete record of its own, with its own skeleton in the template, a third fenced block after the decide and VoI skeletons:

```markdown
# Decision Record: <one-line decision>

## Decision frame

- Route: decide
- Actions: <action A> vs <action B>
- Decision owner: <who decides and acts>
- Reversibility: <what undoing each action costs>
- Deadline or forcing event: <date or event, or none>
- Consequences:

  | | <proposition> true | <proposition> false |
  | --- | --- | --- |
  | <action A> | <outcome> | <outcome> |
  | <action B> | <outcome> | <outcome> |

## Decision-state model

- Proposition: <the binary proposition the decision turns on>
- Residual reading: <what "false" includes, covering explanations nobody named>
- Claim class: <value>
- Identification basis: <design or review licensing the causal conclusion, structural exclusion — see Resolution, or NONE>
- Identification conditions: <identifying assumptions as explicit conditions, or none>
- Ledger mapping: <which UNRESOLVED rows fold into which state and what the residual absorbs, or none>

## Resolution

- Excluded state: <proposition true or proposition false>
- Surviving state: <the other one, or none>
- Observations:

  | observation | source |
  | --- | --- |
  | <one verified part of the accepted evidence> | <file or source it comes from> |

- Accepted evidence: <the whole observation, as the conjunction of the rows above>
- Structural exclusion: <the logical or mechanical reason the accepted evidence is impossible under the excluded state>
- Exclusion assumptions: <the assumptions of the stated model the exclusion rests on>
- Surviving-state possibility: <why the accepted evidence is possible under the surviving state>
- Surviving-state losses:

  | action | loss | provenance |
  | --- | --- | --- |
  | <action A> | <loss or range> | <class> |
  | <action B> | <loss or range> | <class> |

- Surviving-state loss difference: <signed number or range> — provenance: <class>

## Verdict

- Verdict: resolved
- Recommended action: <action A or action B exactly as written in Actions, or returned to owner, or no preference>
- Conditions: <the exclusion assumptions and loss provenance the verdict is conditional on>

## Handoff

- Open factual disputes: <what would change the verdict and needs adjudication, or none>
- Identification gaps: <causal propositions lacking a licensing design or review, or none>
- VoI question: <the collect-more option worth pricing, or none>
```

The required sections and slots are verdict-dependent; under every verdict other than `resolved` nothing changes.
Under `resolved`:

- Required sections: `## Decision frame`, `## Decision-state model`, `## Resolution`, `## Verdict`, `## Handoff`.
- Absent, and a finding when present: the sections `## Evidence and update` and `## Robustness`, and the Decision frame slots `Favored if true:`, `Loss ratio:`, and `Decision threshold (posterior odds):`.
  That is every odds-only field: prior odds, the evidence table and its ratios, independence, posterior odds, threshold, loss ratio, favored-if-true, both sweeps, and the crossover.
- Required in `## Resolution`, each label exactly once, in the skeleton's order: `Excluded state:`, `Surviving state:`, `Observations:`, `Accepted evidence:`, `Structural exclusion:`, `Exclusion assumptions:`, `Surviving-state possibility:`, `Surviving-state losses:`, `Surviving-state loss difference:`.
- `## Resolution` under any verdict other than `resolved` is a finding.

No sentinel is added.

Slot values:

- `Excluded state:` reads exactly `proposition true` or `proposition false`, naming a state of the Proposition slot.
  `Surviving state:` reads exactly the other of the two, or exactly `none` (§ Model review).
- `Observations:` heads a table with exactly the columns `observation` and `source` and at least one row, every cell filled.
- `Accepted evidence:`, `Structural exclusion:`, `Exclusion assumptions:`, and `Surviving-state possibility:` are prose, non-empty, and never `none`.
- `Surviving-state losses:` heads a table with exactly the columns `action`, `loss`, `provenance`, in that order, and exactly one row per framed action: two rows, each action cell one of the two actions exactly as the Actions slot writes them, neither repeated, every row three cells wide.
  A `loss` cell is a nonnegative decimal or a `<low>–<high>` range with low ≤ high, in the template's numeric grammar; a `provenance` cell is one class from § Numeric Policy; a loss nobody supplied writes `none supported` in both its `loss` and `provenance` cells, together.
- `Surviving-state loss difference:` is L(first action in Actions) − L(second action in Actions) in the surviving state, written as a signed decimal (`-1`, `0`, `2.5`) or `<low> to <high>` with low ≤ high (`-5 to 3`), using ASCII `-` for the sign, followed by ` — provenance: <class>`; or exactly `none supported`, bare.
  It reads `none supported` exactly when a losses row does.

The Verdict section carries exactly one visible `- Verdict:` line, and under `resolved` it reads `resolved` bare: `resolved — <anything>` or `resolved (…)` is a finding.

### The surviving-state comparison

The ruling is about the sign of the loss difference throughout its supported range, so the record states the difference, not only the two marginal losses.
When the losses share a parameter (each is a function of the same uncertain quantity), the difference is computed jointly and can be narrower than the marginals allow.
When only unpaired bounds are supplied, the difference is the marginal endpoint interval: [low(A) − high(B), high(A) − low(B)].
Either way the stated difference must lie inside that endpoint interval, since a joint difference can only be tighter.

Recommended action under `resolved`:

- the first action in Actions when the difference's provenance is belief-grade (`user-elicited` or `externally-sourced`) and its high endpoint is below zero; the second action when its low endpoint is above zero;
- `no preference` when the provenance is belief-grade and the difference is exactly the point `0`;
- `returned to owner` otherwise: provenance not belief-grade, `none supported`, or a range that reaches or spans zero without being the point `0`.

Comparisons are exact, each decimal read as a fraction.
Only surviving-state losses enter; the Consequences table's eliminated-state column plays no part, which is how `dominated` is kept from firing on eliminated-state losses.

Worked cases, with marginal losses A = 1–5 and B = 2–6, all `user-elicited`, A listed first:

- Shared parameter, A = t and B = t + 1 for the same t in [1, 5]: the difference is `-1` throughout; it lies in the endpoint interval [−5, 3]; its high endpoint is below zero, so the record names A.
- Shared parameter, A = B = t for t in [1, 5] (marginals A = 1–5, B = 1–5): the difference is `0`; it lies in [−4, 4]; the record reads `no preference`.
- Unpaired, the same marginals as the first case with no stated relation: the difference is `-5 to 3`; it spans zero; the record reads `returned to owner`.

### Causal basis

The dev checker's causal-basis gate is unchanged: a `causal` Claim class needs an Identification basis other than `NONE`, and then Identification conditions other than `none`; it checks presence, not adequacy.
`structural exclusion — see Resolution` is an accepted Identification basis only under `resolved` and only when `Excluded state:` reads `proposition true`; elsewhere it is a finding in the dev checker.
The rule § Numeric Policy states: a structural exclusion licenses causal wording only for the negation of the excluded causal proposition, and only when every causal path the proposition names requires a condition the accepted evidence shows absent; it licenses no causal claim about what did cause the outcome, which stays an identification gap for the Handoff.
Asserting a cause (excluding `proposition false`) needs an ordinary licensing basis, because it would require excluding every path in the residual, including ones nobody named.
Whether the stated paths really all require the absent condition is a reviewer's judgement, not a checker's.

### Model review

When the accepted evidence is impossible under both states, no verdict is reached.
The disposition's home is § Numeric Policy; the handoff's is § The Decide Route, which will say:

- the draft record keeps `Surviving state: none` and its Verdict slot unfilled, is not completed, and is not rewritten to clear a finding;
- the response delivers no recommendation; it states the accepted evidence, the reason it is impossible under each state, and the exclusion assumptions or binary framing that must be wrong for both to hold, with the draft's path;
- the response reports the record as not validated, naming the validator's model-review finding as the expected limitation, per § Record Delivery;
- the conflict is handed to `hypothesis-driven-analysis` as a factual dispute about the observation or the model, in the same response.

Both checkers keep rejecting `Surviving state: none` under every verdict, with a finding that says the disposition is model review, never a verdict.
Agent behaviour in this case, in the routing of a disputed exclusion to `out: adjudicate`, and in a surviving-state tie despite apparent two-state dominance is tested by measured arms, not by the checkers.

### Plan stage and `--final`

The dev checker has no plan-stage mode: it reads every record as complete, as it does today.
The shipped validator keeps its two modes.
In its default mode a record still carrying template placeholders or `pending` is in progress and completeness findings are suspended, as today, so the resolved skeleton validates clean and a half-filled record is not a finding.
Otherwise, and always under `--final`, the shipped validator chooses the required set from the single visible Verdict slot: `resolved` selects the resolved set, any other filled verdict the ordinary set, and an unfilled Verdict slot under `--final` is a finding, as today.

### Who enforces what

Both checkers, on visible Markdown only (each strips fenced code and HTML comments before locating sections; the shipped validator already does, the dev checker must start to, so a `## Resolution` inside a fence or comment counts as absent):

1. `resolved` is in the closed verdict set; exactly one visible `- Verdict:` line; under `resolved` the token is bare.
2. The verdict-dependent section and slot sets above, including the absence of every odds-only field under `resolved` and the absence of `## Resolution` under every other verdict.
3. `Excluded state:` and `Surviving state:` read the closed tokens and differ; `Surviving state: none` is a model-review finding under every verdict.
4. The four prose slots are non-empty and not `none`; `Observations:` has its two columns and at least one filled row.
5. The losses table: exact headers in order, exactly one row per framed action, every row three cells wide, each provenance a class or the paired `none supported`.
6. The loss difference carries exactly one provenance class, or reads `none supported` bare exactly when a losses row does.
7. Recommended action under `resolved` is one of the two framed actions, `no preference`, or `returned to owner`, and is `returned to owner` when the difference's provenance is not belief-grade or reads `none supported`; `no preference` stays a finding outside `indifferent` and `resolved`.

The dev checker alone, which parses numbers:

8. Each loss parses as a nonnegative number or ordered range, and the difference as a signed number or ordered `<low> to <high>` range.
9. The difference lies within the marginal endpoint interval.
10. The recommendation matches the difference per § The surviving-state comparison: a named action must be the one the sign gives, `no preference` needs the belief-grade point `0`, and `returned to owner` is required, not merely allowed, otherwise.
11. Under `resolved`, the ordered rule, the posterior recomputation, and the statewise sentinel checks do not run: `resolved` is dispatched first.
12. The causal-basis rule of § Causal basis.
13. `- Surviving-state losses:` and `- Observations:` are table headings, exempt from the empty-value check beside Consequences and Evidence.

Unchanged and stated exactly: in a `robust`, `prior-sensitive`, `loss-sensitive`, or `evidence-sensitive` record, every Evidence row is either a strictly positive ratio or range or the paired `none supported` form.
`dominated` and `indifferent` records return before any LR cell is read, so an LR of `0` in one passes the dev checker today; that is a known gap, out of scope here, to be filed separately.

The shipped validator's template parity (`test_required_slots_exist_in_shipped_templates`) gains a resolved required-slot set checked against the template's resolved block, which `detect()` classifies as a decision record by its title; the dev checker's parity test compares the template's bullets with the union of its ordinary and resolved label sets.

A human reviewer checks what neither checker can: that the exclusion is structural (logical or mechanical) and not a frequency, a zero count included; that the observations are the whole accepted evidence; that the exclusion is not itself in dispute, which would route `out: adjudicate`; that a causal exclusion meets § Causal basis; and that a jointly computed difference really rests on a shared parameter.

### Worked example (DA-S12)

The proposition is narrowed to direct modification by the job, because "the job caused the loss" is not excluded by the job's absence from db-03: a remote run could trigger a local process.
The narrowing does not make the decision trivial: the residual now includes build 412 acting on db-03 by some other path, so the owner's surviving-state losses must price that, and rolling back keeps a positive value there.
The packet facts align: storage topology (local-only partition), the job's design document (it modifies data only where it runs), process accounting and the deploy log (it never ran on db-03), and the device log (a named alternative).
The losses are illustrative until the fixture fixes them.

```markdown
# Decision Record: roll back to build 411 or keep build 412 with a hotfix after the db-03 partition loss

## Decision frame

- Route: decide
- Actions: roll back to build 411 vs keep build 412 with a hotfix
- Decision owner: the storage on-call lead
- Reversibility: either action is undone by one redeploy, about an hour
- Deadline or forcing event: noon today
- Consequences:

  | | the job directly modified the partition true | the job directly modified the partition false |
  | --- | --- | --- |
  | roll back to build 411 | the faulty job is removed | a build is withdrawn; any indirect build-412 cause is removed too |
  | keep build 412 with a hotfix | the faulty job runs until the hotfix | the build stays and the hotfix work goes to the found cause |

## Decision-state model

- Proposition: the build-412 compaction job, executing, directly modified or deleted the orders partition on db-03
- Residual reading: the partition was lost by anything other than that job's direct action, including a disk fault, another process, build 412 acting by another path, and causes nobody named
- Claim class: causal
- Identification basis: structural exclusion — see Resolution
- Identification conditions: the partition was held only on db-03's local disk; the job modifies data only on the host where it executes; process accounting and the deploy log are complete for the incident window
- Ledger mapping: none

## Resolution

- Excluded state: proposition true
- Surviving state: proposition false
- Observations:

  | observation | source |
  | --- | --- |
  | the orders partition on db-03 was lost overnight | packet file: incident timeline |
  | the partition lived only on db-03's local disk, with no replica, shared volume, or network storage | packet file: storage topology |
  | the compaction job modifies data only by executing on the host that holds it | packet file: compaction design |
  | the job never executed on db-03, and db-03 never ran build 412 | packet files: process accounting, deploy log |
  | db-03's device log records a disk fault in the window | packet file: db-03 device log |

- Accepted evidence: the partition was lost while the compaction job never executed on db-03, the only host holding it
- Structural exclusion: the job can modify data only where it executes and the partition existed only on db-03, where it never executed, so direct modification by the job is impossible
- Exclusion assumptions: the storage topology, process accounting, and deploy log are complete for the incident window, and the design document's locality claim holds for build 412
- Surviving-state possibility: a loss without the job's direct action is possible under not-H, and the device log names one such cause, a disk fault
- Surviving-state losses:

  | action | loss | provenance |
  | --- | --- | --- |
  | roll back to build 411 | 4 | user-elicited |
  | keep build 412 with a hotfix | 1 | user-elicited |

- Surviving-state loss difference: 3 — provenance: user-elicited

## Verdict

- Verdict: resolved
- Recommended action: keep build 412 with a hotfix
- Conditions: the exclusion assumptions in Resolution, and the owner's surviving-state losses of 4 and 1

## Handoff

- Open factual disputes: none
- Identification gaps: what caused the loss is not identified; the device log's disk fault is a candidate, not an established cause
- VoI question: none
```

Slot by slot on this example (✓ accept, ✗ reject):

| slot or field | both checkers | dev checker alone also rejects |
| --- | --- | --- |
| `## Evidence and update`, `## Robustness`, Favored if true, Loss ratio, Decision threshold | ✗ if any is present | — |
| Verdict | ✓ one bare `resolved`; ✗ a second Verdict line, `resolved — …` | — |
| Claim class, Identification basis, Identification conditions | ✓ `causal`, `structural exclusion — see Resolution`, conditions restated | that basis with conditions `none`, or with `Excluded state: proposition false` |
| Excluded state, Surviving state | ✓ the two tokens, differing; ✗ equal, other tokens, or `Surviving state: none` (model review) | — |
| Observations | ✓ two columns, filled rows; ✗ missing table or column | — |
| the four prose slots | ✓ non-empty prose; ✗ missing, empty, `none` | — |
| Surviving-state losses | ✓ one row per action; ✗ a missing row, a duplicate action, a wrong header, a short row, an unknown class, an unpaired `none supported` | an unparseable or negative loss |
| Surviving-state loss difference | ✓ `3 — provenance: user-elicited`; ✗ no class, two classes | any value but `3`, since both losses are points and the endpoint interval is [3, 3] |
| Recommended action | ✓ `keep build 412 with a hotfix`; ✗ a value outside the three forms | `roll back to build 411`, `no preference`, `returned to owner` |
| `## Resolution` inside a fence or comment | ✗ counts as absent | — |

The difference here is L(roll back) − L(hotfix) = 4 − 1 = 3, a point, so its endpoint interval is exactly [3, 3]; a positive low endpoint names the second action.

### Choices made in the contract

1. *A separate resolved skeleton whose required sections and slots are verdict-dependent, omitting every odds-only field, with no sentinel* (orchestrator ruling A).
   Both checkers need verdict-dependent requirements for `## Resolution` anyway, and the shipped `_required_slots(body, kind)` already varies its set by body for exploration records; the dev checker reads the verdict before `_require_slots` can choose a set.
   Cost if wrong: two record shapes on one route, and an agent that starts from the ordinary skeleton and later reaches `resolved` must delete two sections and three slots, which the measured arm will show.
2. *The loss comparison is a stated signed difference, checked against the marginal endpoint interval*, so that a shared parameter can give a strict preference or an exact tie that overlapping marginals cannot.
   Cost if wrong: the difference's sign convention gives the Actions order a meaning it has nowhere else (§ Numeric Policy says the order carries none), and a difference narrower than the marginals rests on a pairing only a reviewer can check.
3. *The marginal losses table stays beside the difference*, with exactly one row per framed action in both checkers, so a missing or duplicated action cannot pass and the difference has something to be checked against.
   Cost if wrong: two statements of the same losses that the dev checker relates only by containment.
4. *Unsupported losses use the paired `none supported`*, the missing-ratio form's spelling, and the difference then reads `none supported` bare.
   Cost if wrong: a reader may take it for the missing-ratio form; the column header disambiguates.
5. *Source-backed observations are a two-column table in `## Resolution`*, replacing the Evidence table the resolved record omits.
   Cost if wrong: an agent may duplicate the observations in prose and table, which no checker compares.
6. *DA-S12's proposition is narrowed to direct modification by the job*, rather than requiring the packet to show every causal path needs local execution, because the narrowing is exact and keeps the decision non-trivial (the residual includes build 412 acting by another path, so rollback keeps value).
   Cost if wrong: the scenario no longer tests an exclusion of a broad causal claim, which is the harder and commoner case.
7. *`structural exclusion — see Resolution` stays an accepted basis, only with `Excluded state: proposition true` and only with § Numeric Policy's qualification*, because the dev gate checks presence, not adequacy.
   Cost if wrong: an agent writes the basis for an exclusion that does not cover every named path, and only a reviewer catches it.
8. *Exactly one visible Verdict line and a bare `resolved`*, because the shipped validator reads the first Verdict slot and validates the others only against the vocabulary, and both checkers read `resolved — note` as `resolved`.
   Other verdicts keep their current tolerance of annotations in the shipped validator.
   Cost if wrong: an annotation an agent adds out of habit fails the record.
9. *The dev checker strips fenced code and HTML comments before locating sections*, matching the shipped validator, so a Resolution section in a fence or comment is absent.
   Cost if wrong: the dev checker's section parse changes for every record kind it reads, which `test_ordinary_records_are_unchanged` must cover.
10. *`Surviving state: none` stays a rejection under every verdict, and the no-verdict handoff is § The Decide Route's*, because `--final` requires a Verdict and a model-review case has none.
    Cost if wrong: the delivered draft always reports a validator finding, which a reader may take for a defect.
11. *The statewise LR gap is not tightened in this change*: `dominated` and `indifferent` records never read LR cells, so a `0` there passes today; it is filed separately.
    Cost if wrong: a statewise record can carry an elimination-shaped `0` until that issue is fixed.
12. *`Exclusion assumptions:` may not read `none`*, because answer 4 makes exactness conditional on a stated model.
    Cost if wrong: a purely logical exclusion has to name the binary model as its assumption.
13. *The resolved label sets are constants of their own in both checkers*, and both parity tests read the template's resolved block.
    Cost if wrong: none to behaviour; each parity test unions two sets.

### The implementing change's tests, decided by the contract

Dev checker (`tests/test_check_decision.py`):

- `test_resolved_passes_with_exclusion_and_strict_surviving_preference`: § Shape and the worked example.
- `test_resolved_passes_in_the_other_direction`: `Excluded state: proposition false`, with a non-causal claim class or an ordinary basis (§ Causal basis).
- `test_resolved_exact_tie_reports_no_preference`: difference `0`, § The surviving-state comparison.
- `test_resolved_range_touching_zero_returns_to_owner`: a difference range reaching zero.
- `test_resolved_with_unsupported_losses_returns_to_owner`: a difference not belief-grade, or `none supported`.
- `test_resolved_shared_parameter_strict_preference`: marginals 1–5 and 2–6, difference `-1`, names the first action.
- `test_resolved_shared_parameter_exact_tie`: marginals 1–5 and 1–5, difference `0`, `no preference`.
- `test_resolved_without_a_structural_exclusion_fails`: items 2 and 4.
- `test_resolved_carrying_an_odds_slot_fails`: item 2, with an odds-only field present (each of the five sections or slots parametrized).
- `test_resolved_missing_a_loss_row_fails` and `test_resolved_duplicate_loss_rows_fail`: item 5.
- `test_duplicate_verdict_line_fails` and `test_annotated_resolved_fails`: item 1.
- `test_fenced_resolution_counts_as_absent` and `test_commented_resolution_counts_as_absent`: the visible-Markdown rule and choice 9.
- `test_evidence_impossible_under_both_states_fails_as_model_review`: item 3.
- `test_dominated_does_not_fire_on_losses_in_the_eliminated_state`: losses over (surviving, eliminated) of A = (1, 0) and B = (1, 5) pass as `resolved` with difference `0` and `no preference`; the same record with `## Resolution` under `dominated` fails, item 2.
- `test_ordinary_records_are_unchanged`: item 2's "nothing changes" and the unchanged LR invariant; every existing fixture keeps its findings.

Shipped validator (its unit suite, test_check_record.py beside it):

- `test_resolved_is_an_accepted_decide_verdict`: item 1.
- `test_resolved_requires_each_contract_statement`: items 2 to 6.
- `test_resolved_rejects_posterior_odds_and_crossover`: item 2, odds-only fields present.
- `test_resolved_recommendation_coupling`: item 7.
- `test_other_verdicts_keep_their_coupling`: item 2's "nothing changes" and item 7's `no preference` rule.
- The missing-row, duplicate-row, duplicate-Verdict, annotated-`resolved`, odds-field, fenced, and commented cases above, each also against the shipped validator, by the same items.
