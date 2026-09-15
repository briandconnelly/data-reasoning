# Decision Record Template

This template records a decision analysis's content.
`../SKILL.md` governs what that content means.
Every closed-vocabulary slot below — route, verdict, provenance — names only the slot: which value applies, what values exist, and what each value means are `../SKILL.md`'s to state, not this template's.
Fill one record per decision; use the Decide blocks for the decide route and the VoI block alone for the voi route.
The skeletons show the exact label and the bare shape of each value; everything else a slot needs to know is in § Slot notes below, outside the record, so that none of it is copied into one.

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

- Loss ratio: <multiple> — provenance: <class>
- Decision threshold (posterior odds): <odds> — provenance: <class>

## Decision-state model

- Proposition: <the binary proposition the decision turns on>
- Residual reading: <what "false" includes, covering explanations nobody named>
- Claim class: <value>
- Identification basis: <design or review licensing a causal posterior, or NONE>
- Identification conditions: <identifying assumptions as explicit conditions, or none>
- Ledger mapping: <which UNRESOLVED rows fold into which state and what the residual absorbs, or none>

## Evidence and update

- Prior odds: <odds or range> — provenance: <class>
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | <evidence item> | <ratio or range> | <class> | <where the ratio comes from> |

- Independence: <single item, or why the items are conditionally independent given each state>
- Posterior odds: <odds or range>

## Robustness

- Prior class swept: <low>–<high> — provenance: <class>
- Loss range swept: <low>–<high> — provenance: <class>
- Crossover: <the prior odds or loss ratio at which the preferred action flips, or none within swept class>

## Verdict

- Verdict: <value>
- Recommended action: <action A or action B exactly as written in Actions, or returned to owner>
- Conditions: <the prior class, loss provenance, and assumptions the verdict is conditional on>

## Handoff

- Open factual disputes: <what would change the verdict and needs adjudication, or none>
- Identification gaps: <causal propositions lacking a licensing design or review, or none>
- VoI question: <the collect-more option worth pricing, or none>

This block states facts, crossovers, and open questions only.
It does not recommend or prescribe which route a receiving skill takes.
```

```markdown
# VoI Record: <one-line pull question>

## VoI

- Route: voi
- Pending decision: <value>
- Signal model: <value>
- Value basis: <value>
- Value calculation: <value>
- Upper bound: <value>
- Cost: <value>
- Verdict: <value>
```

## Slot notes

These notes are read once and never copied into a record; a record carries the label, the value, and — where the skeleton shows one — a single ` — provenance: <class>` suffix, and nothing else on the line.

Labels are copied exactly as the skeleton spells them, colon included.
A relabelled slot (`Proposition (H1):`, `Consequences (units: …):`) is a missing slot to every checker.

A value stands bare.
Explanation goes in the Conditions slot, the Handoff block, or the report, not after the value; a value followed by a parenthesis, a dash, or a clause is a different value.

Numeric slots — Loss ratio, Decision threshold, Prior odds, Posterior odds, Prior class swept, Loss range swept, and the LR cell — take a single number or a `<low>–<high>` range with low ≤ high, written as decimals: `0.02–0.2`, not `1:49 to 1:4`; `4.5`, not `4.5 (= 0.9/0.2)`.
Odds and likelihood ratios are positive.

Provenance is exactly one class from `../SKILL.md` § Numeric Policy, on the slots the skeleton marks and in the evidence table's provenance cell.
`derived` is not a class; a threshold derived from an elicited loss ratio carries the loss ratio's class.

Sentinels replace the whole value and appear bare, with no suffix and no provenance.
They are `none stated` (Decision threshold); `none needed` (Prior odds, Posterior odds, Prior class swept, Crossover, under a `dominated` verdict); `none supported — see Robustness` (Prior odds and Posterior odds, under `../SKILL.md` § Degraded Modes); `none within swept class` (Crossover); `single item` (Independence); `returned to owner` (Recommended action, under a sensitive verdict); `NONE` (Identification basis); and `none` (Identification conditions, Ledger mapping, the three Handoff slots).

The evidence table has exactly four cells per row, and a pipe inside a cell is written `\|`.
An item with no defensible ratio reads `none supported` in both its LR and provenance cells with the reason in its source cell (`../SKILL.md` § Degraded Modes).

Value sets: Route per `../SKILL.md` § Routing; Claim class, Verdict, and Recommended action per `../SKILL.md` § The Decide Route; the VoI slots per `../SKILL.md` § The VoI Route.
A Recommended action names one of the two actions in the Actions slot's own words under `robust` and `dominated`.
