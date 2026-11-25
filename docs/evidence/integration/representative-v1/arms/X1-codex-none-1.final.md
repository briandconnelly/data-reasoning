**Sign with Acme for all 100,000 units.** Brightline’s trial had 1 defect in 150 units (0.67%), versus Acme’s 1,000 in 50,000 (2.00%). Acme stayed below 3% in every recorded month. Brightline’s single batch leaves enough uncertainty about full-year quality that the $1 million penalty outweighs the expected savings on returns. [Brightline trial](data/brightline_trial.csv) · [Acme history](data/acme_history.csv) · [Contract terms](data/contract_terms.md)

Using a uniform prior for each supplier’s defect rate and assuming each has a stable rate across shipments, I estimate the following costs. Purchase prices are identical.

| Supplier | Expected returns cost | Chance of exceeding 3% | Expected returns and penalty cost |
|---|---:|---:|---:|
| Acme | $30,000 | Negligible under the model | $30,000 |
| Brightline | $19,700 | 5.7% | $76,800 |

At those returns estimates, Brightline’s penalty risk would need to be about **1% or less** to break even. A Jeffreys prior lowers its estimated risk to 2.8% and its expected cost to about $42,600, still above Acme’s. Both estimates assume the trial represents Brightline’s production. With only one batch, the data can’t establish how much its quality varies across batches.
