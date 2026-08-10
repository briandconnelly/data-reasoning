# Decision Record Template

This template records a decision analysis's content.
`../SKILL.md` governs what that content means.
Every closed-vocabulary slot below — route, verdict, provenance — names only the slot: which value applies, what values exist, and what each value means are `../SKILL.md`'s to state, not this template's.
Fill one record per decision; use the Decide blocks for the decide route and the VoI block alone for the voi route.
Numeric slots take a single number or a `<low>–<high>` range with low ≤ high; odds and likelihood ratios are positive.

```markdown
# Decision Record: <one-line decision>

## Decision frame

- Route: decide — value set per `../SKILL.md` § Routing (authority)
- Actions: <action A> vs <action B>
- Decision owner: <who decides and acts>
- Reversibility: <what undoing each action costs>
- Deadline or forcing event: <when the decision happens by default, or `none`>
- Consequences:

  | | <proposition> true | <proposition> false |
  | --- | --- | --- |
  | <action A> | <outcome> | <outcome> |
  | <action B> | <outcome> | <outcome> |

- Loss ratio: <cost of wrongly choosing A over B, as a multiple> — provenance: <class>
- Decision threshold (posterior odds): <odds at which the preferred action flips> — provenance: <class> — or `none stated`

## Decision-state model

- Proposition: <the binary proposition the decision turns on>
- Residual reading: <what "false" includes — explicitly covering explanations nobody named>
- Claim class: <value> — value set per `../SKILL.md` § The Decide Route (authority)
- Identification basis: <pointer to the design or review licensing a causal posterior, or `NONE`>
- Ledger mapping: <which UNRESOLVED rows fold into which state and what the residual absorbs, or `none`>

## Evidence and update

- Prior odds: <odds or range> — provenance: <class> — or `none needed` under a dominated verdict
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | <evidence item> | <ratio or range> | <class> | <where the ratio comes from> |

- Independence: <why the items above are conditionally independent given each state, or `single item`>
- Posterior odds: <odds or range, recomputable from the lines above> — or `none needed` under a dominated verdict

## Robustness

- Prior class swept: <the range of prior odds considered> — provenance: <class> — or `none needed` under a dominated verdict
- Loss range swept: <the range of loss ratios considered> — provenance: <class>
- Crossover: <the prior or loss ratio at which the preferred action flips, or `none within swept class`> — or `none needed` under a dominated verdict

## Verdict

- Verdict: <value> — value set and semantics per `../SKILL.md` § The Decide Route (authority)
- Conditions: <the prior class, loss provenance, and assumptions the verdict is conditional on>

## Handoff

- Open factual disputes: <what would change the verdict and needs adjudication, or `none`>
- Identification gaps: <causal propositions lacking a licensing design or review, or `none`>
- VoI question: <the collect-more option worth pricing, or `none`>

This block states facts, crossovers, and open questions only.
It does not recommend or prescribe which route a receiving skill takes.
```

```markdown
# VoI Record: <one-line pull question>

## VoI

- Route: voi — value set per `../SKILL.md` § Routing (authority)
- Pending decision: <the two actions and current leaning, or a pointer to the decide record or collection plan>
- Signal model: <what the pull could return and what each return does to the posterior> — provenance: <class>
- Value calculation: <expected improvement from deciding after the signal, net of full cost, compared with zero — or the break-even price in break-even mode>
- Cost: <stated or measured cost of the pull, or `none stated`>
- Verdict: <value> — value set and semantics per `../SKILL.md` § The VoI Route (authority)
```
