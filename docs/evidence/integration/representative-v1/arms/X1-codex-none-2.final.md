**Sign with Acme for all 100,000 units.** Brightline’s trial had a lower defect rate, but the expected savings on returns are too small to justify the modeled risk of a $1 million penalty.

| Supplier | Observed defects | Expected returns cost | Chance of exceeding 3% | Expected total quality cost |
|---|---:|---:|---:|---:|
| Acme | 1,000 / 50,000 (2.00%) | $30,029 | Near zero | $30,029 |
| Brightline | 1 / 150 (0.67%) | $19,737 | 5.71% | $76,826 |

With identical unit prices, Brightline saves about **$10,300** in expected returns costs. That saving can absorb only about a **1.03%** chance of the penalty. The model puts Brightline’s chance at **5.71%**, adding roughly **$57,100** in expected penalty cost.

The estimates use a beta-binomial model with a uniform prior for each supplier’s defect rate. It assumes each supplier’s underlying rate is stable and that the observed units represent next year’s production. Using a Jeffreys prior instead lowers Brightline’s estimated penalty chance to **2.77%** and its expected quality cost to about **$42,600**, still above Acme’s. Brightline’s single batch leaves batch-to-batch variation unmeasured.
