# Decision Record: Supplier for next year's 100,000 units

## Decision frame

- Route: decide
- Actions: Stay with Acme vs Move to Brightline
- Decision owner: The purchasing team
- Reversibility: The supplier is fixed for the year under either action.
- Deadline or forcing event: Signing the annual supply contract
- Consequences:

  | | Brightline stays at or below 3% | Brightline exceeds 3% |
  | --- | --- | --- |
  | Stay with Acme | Acme's historical rate as a planning baseline, with Acme's own penalty exposure | Same Acme baseline and exposure |
  | Move to Brightline | Pay returns on Brightline defects, modeled at the trial rate in this state | Pay returns on Brightline defects and the $1 million penalty |

- Favored if true: Move to Brightline
- Loss ratio: 0.019417475728155338 — provenance: sensitivity-only
- Decision threshold (posterior odds): 51.5 — provenance: sensitivity-only

## Decision-state model

- Proposition: Brightline's realized annual defect rate is at most 3%.
- Residual reading: Brightline's realized annual rate exceeds 3%, including any production, batch, or sampling differences the trial cannot show.
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: none

## Evidence and update

- Prior odds: none supported — see Robustness
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | Brightline trial | none supported | none supported | data/brightline_trial.csv records 1 defect in 150 units from one trial batch. Neither representativeness at scale nor the trial-count distribution conditional on either annual state is established. Under independent representative sampling with a fixed defect probability, the probability of at most one defect at 3% is 5.85% and the exact one-sided 95% upper limit is 3.12%. These are sampling calculations. |
  | Acme history | none supported | none supported | data/acme_history.csv records 1,000 defects in 50,000 units. Monthly rates span 1.85%–2.09% over 12 months. The history provides a cost baseline for Acme and supplies no calibrated likelihood for Brightline's annual state. |
  | Contract | none supported | none supported | data/contract_terms.md supplies the identical unit prices, annual volume, $15 per defect, and $1 million penalty for more than 3,000 annual defects. These determine costs given outcomes. |

- Independence: No likelihood ratios are combined.
- Posterior odds: none supported — see Robustness

## Robustness

- Prior class swept: 19–99 — provenance: sensitivity-only
- Loss range swept: 0.008097165991902834–0.019704142303315714 — provenance: sensitivity-only
- Crossover: flips at loss ratio 0.010101010101010102–0.05263157894736842

There is no quantitative update supported for the annual state. For the decision, independently sweep hypothetical post-trial odds from 19 to 99 of staying at or below 3%, equivalent to 5% to 1% exceedance risk. These odds are scenarios. They cannot be inferred from the trial or mapped back to prior odds.

For expected dollar cost, use Acme’s observed 2% as its expected rate and omit its penalty risk for the baseline. In Brightline’s below-threshold state use its trial rate of 1/150 as the conditional mean. In the other state sweep its conditional mean annual defect rate from 3.001% (3,001 defects) to 100% (the mathematical maximum). Both conditional rates are sensitivity assumptions. The favorable-state gain is $30,000 − $10,000 = $20,000. The unfavorable-state loss relative to Acme runs from $1,015,015 to $2,470,000. The gain divided by the loss yields the swept loss range. At a 4% conditional mean in the penalty state, the loss is $1,030,000 and the odds crossover is 51.5, equivalent to a 1.90% chance of triggering the penalty. The crossover runs from 0.80% to 1.93% exceedance risk over the full loss sweep. At each hypothetical post-trial odds value, the loss ratio must exceed the reciprocal of those odds for Brightline to be cheaper.

At 4% in the penalty state, a 1% exceedance chance gives $20,500 in expected Brightline costs and a 2% chance gives $31,000. Acme costs $30,000 at its historical rate before its own penalty risk. Allowing a nonzero Acme penalty chance increases its expected cost by $1 million times that chance. If Brightline's mean in the favorable state reaches 2%, the modeled savings vanish even without a penalty.

## Verdict

- Verdict: loss-sensitive
- Recommended action: returned to owner
- Conditions: The modeled cost difference depends on unknown annual tail probabilities and conditional defect rates. As a risk judgment for a locked annual commitment, favor staying with Acme given the observed monthly stability and the unquantified exposure from scaling a single Brightline batch. The modeled $20,000 routine savings assume that Brightline can reproduce the trial rate in the favorable state. Acme's history supports its planning baseline and leaves its own future penalty risk uncertain.

## Handoff

- Open factual disputes: Brightline's full-volume annual rate distribution and Acme's future probability of exceeding 3% are unknown.
- Identification gaps: none
- VoI question: none
