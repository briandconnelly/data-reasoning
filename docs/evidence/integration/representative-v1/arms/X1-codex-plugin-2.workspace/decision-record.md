# Decision Record: Supplier for next year's 100,000 units

## Decision frame

- Route: decide
- Actions: Stay with Acme vs Sign with Brightline
- Decision owner: The buyer responsible for the annual supply contract
- Reversibility: One supplier for the entire year with no mid-year switch
- Deadline or forcing event: Award of next year's contract
- Consequences:

  | | Brightline costs less | Brightline costs at least as much |
  | --- | --- | --- |
  | Stay with Acme | Forgo $20,000 at the Brightline trial rate and Acme historical rate | Avoid $1,015,015 to $1,030,000 in incremental costs in the illustrated Brightline penalty scenarios |
  | Sign with Brightline | Save $20,000 at those rates | Tie at equal rates and penalty status, or incur higher returns and potentially the $1 million penalty |

- Favored if true: Sign with Brightline
- Loss ratio: 0.0194174757281553–0.0197041423033157 — provenance: sensitivity-only
- Decision threshold (posterior odds): 50.75075–51.5 — provenance: sensitivity-only

## Decision-state model

- Proposition: Brightline's realized annual returns and penalty cost is lower than Acme's would be for next year's volume.
- Residual reading: Brightline ties or costs more, including higher returns below the penalty threshold and previously unseen production differences.
- Claim class: descriptive
- Identification basis: NONE
- Identification conditions: none
- Ledger mapping: none

## Evidence and update

- Prior odds: none supported — see Robustness
- Evidence:

  | item | LR | provenance | source, reference class, conditioning |
  | --- | --- | --- | --- |
  | Supplier defect records | none supported | none supported | data/acme_history.csv has 1,000 defects in 50,000 units over 12 months. data/brightline_trial.csv has 1 in 150 from one batch. The aggregate states lack a supported distribution of annual outcomes and a model connecting the trial to production across batches. |

- Independence: single item
- Posterior odds: none supported — see Robustness

## Robustness

- Prior class swept: 1–100 — provenance: sensitivity-only
- Loss range swept: 0.0194174757281553–0.0197041423033157 — provenance: sensitivity-only
- Crossover: flips at loss ratio 0.01–1

For hypothetical odds O from 1 to 100, Brightline wins when the savings-to-downside ratio exceeds 1/O. At the illustrated loss ratios the decision flips at odds of 50.75075–51.5 in favor of Brightline being cheaper. No quantitative update is supported. These odds are scenario inputs, with no claim about their actual probability.

At Acme's historical rate, its annual returns cost projects to $30,000. Brightline's trial rate projects to $10,000 in returns. A year with 3,001 to 4,000 Brightline defects costs $1,045,015 to $1,060,000 including penalty, using data/contract_terms.md. In this two-outcome illustration, Brightline breaks even at a 1.90%–1.93% penalty probability. More generally, with Acme fixed at its historical rate, Brightline breaks even when its expected returns cost plus $1 million times its penalty probability equals $30,000. Even with expected returns of zero, a penalty probability above 3% makes Brightline more expensive under that Acme benchmark.

Under independent binomial sampling with a stable trial defect probability of 3%, the chance of seeing at most one defect in 150 units is 5.85%. The exact one-sided 95% upper confidence limit solves that binomial tail equation at 5% and is 3.12%. This calculation describes what the trial can resolve under the sampling model. It supplies neither a probability of incurring the annual penalty nor a likelihood ratio for the composite decision states.

## Verdict

- Verdict: loss-sensitive
- Recommended action: returned to owner
- Conditions: Acme is the conservative choice if limiting exposure to the penalty is the owner's priority. The scenario loss ratios depend on extrapolating the observed rates and positing the Brightline penalty outcomes. Expected-dollar ranking depends on both suppliers' production distributions and annual penalty probabilities, which the records do not establish.

## Handoff

- Open factual disputes: Brightline's year-scale production risk and the stability of Acme's historical performance at the contracted volume.
- Identification gaps: none
- VoI question: none
