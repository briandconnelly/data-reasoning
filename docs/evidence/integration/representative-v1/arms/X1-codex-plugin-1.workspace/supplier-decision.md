# Decision Record: Supplier for next year's 100,000 units

## Decision frame

- Route: decide
- Actions: Stay with Acme vs Move to Brightline
- Decision owner: The buyer responsible for the annual supplier contract
- Reversibility: The contract allows no mid-year switch.
- Deadline or forcing event: One supplier must be selected before next year's orders.
- Consequences:

  | | Brightline exceeds 3% true | Brightline exceeds 3% false |
  | --- | --- | --- |
  | Stay with Acme | $30,000 in returns at Acme's historical 2%, used as a planning baseline | Same planning baseline |
  | Move to Brightline | At least $1,045,015 in returns and penalty | $0 to $45,000 in returns, with $10,000 at the trial rate |

- Favored if true: Stay with Acme
- Loss ratio: 33.8338333333–50.75075 — provenance: sensitivity-only
- Decision threshold (posterior odds): 0.0197041423–0.0295562135 — provenance: sensitivity-only

## Decision-state model

- Proposition: H is that Brightline would deliver more than 3,000 defective units in the 100,000-unit contract year.
- Residual reading: H false includes every Brightline outcome at or below 3%, including outcomes between 2% and 3% that cost more than the Acme baseline without incurring a penalty.
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: none

## Evidence and update

- Prior odds: none supported — see Robustness
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | Brightline trial | none supported | none supported | data/brightline_trial.csv has 1 defect in 150 units from one batch. There is no supported model linking trial and annual production or specifying defect rates within each state. |
  | Acme history | none supported | none supported | data/acme_history.csv has 1,000 defects in 50,000 units, with monthly rates of 1.85% to 2.09%. It informs Acme's planning baseline and provides no calibrated evidence on Brightline's state. |

- Independence: No ratios are combined.
- Posterior odds: none supported — see Robustness

## Robustness

- Prior class swept: 0.001–1 — provenance: sensitivity-only
- Loss range swept: 33.8338333333–50.75075 — provenance: sensitivity-only
- Crossover: flips at loss ratio 1–1000

The illustrative odds grid spans about 0.10% to 50% chance of a penalty. No quantitative update is supported, so there is no derived posterior-odds range. For any assumed decision odds o, Acme is cheaper in expectation when the loss ratio exceeds 1/o. The crossover runs from 1,000 at odds 0.001 to 1 at odds 1. At the stated loss ratios, the odds crossover is approximately 0.01970 to 0.02956, or 1.93% to 2.87% probability. Equality gives equal expected cost.

The sweep holds Brightline's penalty-state count at the first penalty-triggering value, 3,001 defects, and varies its average returns cost conditional on no penalty from $0 to $10,000. These scenario assumptions favor Brightline and are sensitivity-only. Acme's $30,000 baseline minus Brightline's conditional returns cost gives $20,000 to $30,000 in savings. The $1,045,015 minimum penalty-state cost minus Acme's baseline gives $1,015,015 in extra cost. Dividing the latter by the former gives the loss ratio. Higher penalty-state costs or smaller no-penalty savings reduce the probability Brightline can tolerate. When its no-penalty expected returns cost is at least $30,000, Brightline offers no expected cost advantage at any positive penalty probability under this Acme baseline. The $15 per defect, $1 million penalty, strict 3% threshold and equal prices come from data/contract_terms.md.

If the trial consisted of independent draws at a fixed 3% defect rate, the chance of seeing one or fewer defects would be (0.97)^150 + 150 × 0.03 × (0.97)^149 = 5.85%. The corresponding exact one-sided 95% upper limit is 3.12% for the sampled process under that model. This calculation is conditional on the sampling model and supplies no probability that annual production crosses the penalty threshold.

## Verdict

- Verdict: loss-sensitive
- Recommended action: returned to owner
- Conditions: The annual choice depends on the unknown scale-up risk and the buyer's tolerance for the penalty. Acme is the conservative choice for a buyer who prioritizes avoiding that exposure and uses Acme's 2% history as next year's baseline. The data supply no calibrated annual penalty probability for either supplier. The scenario loss ratio uses the stated dollar terms and sensitivity-only conditional defect assumptions.

## Handoff

- Open factual disputes: Brightline's annual defect risk under full-volume production and whether Acme's historical performance will hold next year.
- Identification gaps: none
- VoI question: none
