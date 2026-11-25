# Decision Record: Supplier for next year's 100,000 units

## Decision frame

- Route: decide
- Actions: Stay with Acme vs Move to Brightline
- Decision owner: The contracting team
- Reversibility: The contract commits all units to one supplier for the year, with no mid-year switch.
- Deadline or forcing event: Next year's supplier signing
- Consequences:

  | | Brightline costs less than Acme | Brightline costs at least as much as Acme |
  | --- | --- | --- |
  | Stay with Acme | Forego Brightline's savings | Avoid any incremental Brightline costs |
  | Move to Brightline | Capture the savings | Pay any incremental cost, potentially including a $1 million penalty |

- Favored if true: Move to Brightline
- Loss ratio: 0.0196753566 — provenance: sensitivity-only
- Decision threshold (posterior odds): 50.825 — provenance: sensitivity-only

## Decision-state model

- Proposition: Brightline's annual cost from returns and penalties is lower than Acme's would be for next year's 100,000 units.
- Residual reading: Brightline ties or costs more for any reason, including more returns below the penalty threshold, a penalty, or differences in future production across suppliers.
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: none

## Evidence and update

- Prior odds: none supported — see Robustness
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | Brightline trial | none supported | none supported | data/brightline_trial.csv records 1 defect in 150 units from a single trial batch. The trial supplies neither production representativeness nor the distribution of annual quality within each decision state. |
  | Acme history | none supported | none supported | data/acme_history.csv records 1,000 defects in 50,000 units across 12 months. This benchmarks Acme's returns and supplies no Brightline production reference class. |

- Independence: No likelihood ratios were combined.
- Posterior odds: none supported — see Robustness

## Robustness

- Prior class swept: 1–20 — provenance: sensitivity-only
- Loss range swept: 0.0073782587–0.0295130349 — provenance: sensitivity-only
- Crossover: flips at loss ratio 0.0057744332–0.1154886645

For the illustrative cost model, hold Acme at its observed pooled rate of 2%, or $30,000. Put Brightline at the trial rate of 1/150 in the favorable state ($10,000) and at 3.1% in the adverse state ($1,046,500). These future rates are sensitivity-only. The contract supplies the $15 per return and the $1 million penalty above 3%, with equal unit prices. The loss ratio is $20,000 / $1,016,500. Brightline breaks even at a 1.9296% probability of the adverse state, or favorable odds of 50.825. Holding the adverse case fixed and moving the favorable rate from 0% to 1.5% gives the stated loss ratio range.

For illustration only, if trial units are independent and reflect production and the two state rates are the two point values above, the likelihood ratio for exactly 1 defect is (1/150)/0.031 × ((1−1/150)/(1−0.031))^149 = 8.65886. Prior odds of 1 to 20 give conditional posterior odds of 8.65886 to 173.17718, which flip the central cost case at prior odds of 5.86971 (85.44% prior probability of the favorable state). The reciprocal posterior odds give the stated loss-ratio crossovers in ascending order. The loss sweep varies favorable-state costs with each of these hypothetical posterior odds held fixed, as a separate sensitivity calculation.

More generally, with Acme at $30,000, Brightline's expected cost is $1.5 million times its expected defect rate plus $1 million times its probability of exceeding 3%. Brightline needs a penalty probability below 3% even with zero expected return costs. At $10,000 in expected returns the break-even penalty probability is 2%. At exactly 3% annual defects the contract charges $45,000 in returns and no penalty.

## Verdict

- Verdict: loss-sensitive
- Recommended action: returned to owner
- Conditions: Staying with Acme is the practical choice if the owner prioritizes avoiding the seven-figure penalty exposure and uses Acme's year of shipments as the more reliable planning baseline. The trial does not support the small Brightline penalty probability needed to justify a switch on expected cost. The hypothetical binary losses and prior sweep do not establish expected-cost superiority.

## Handoff

- Open factual disputes: Brightline's trial-to-production comparability and both suppliers' annual penalty probabilities are unmeasured in the supplied records.
- Identification gaps: none
- VoI question: none
