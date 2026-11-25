**Sign with Acme.**

**Acme.** The 12 months of history show 1,000 defects in 50,000 units, a 2.0% rate. Monthly rates stay between 1.8% and 2.1%, so the annual rate is very unlikely to reach the 3% penalty line.
- Expected cost: 100,000 × 2% × $15 ≈ **$30,000**.
- Penalty risk is effectively zero.

**Brightline.** The trial found 1 defect in 150 units, or 0.67%. That looks better than Acme, but 150 units can't pin the rate down.
- If Brightline's true rate were 2%, a trial this clean would still happen about 20% of the time. At 3% it would happen about 6% of the time. The trial can't rule out a rate as bad as Acme's, or worse.
- I put a Beta prior on Brightline's rate and updated it with the trial. Three different priors give the results below:

| Prior on Brightline's rate | Expected defect rate | Chance rate is over 3% | Expected total cost (returns plus penalty risk) |
|---|---|---|---|
| Uniform (know nothing) | 1.3% | 5.7% | ~$77k |
| Jeffreys | 1.0% | 2.8% | ~$43k |
| Skeptical (centred on Acme's 2%) | 1.0% | 1.7% | ~$32k |

- Even under the most skeptical prior, Brightline is no cheaper in expectation than Acme's $30k.
- It carries a 2–6% chance of a $1M penalty that Acme essentially doesn't.

**Why the gap is smaller than it looks.** The best Brightline could save is about $30k a year, and only if its true rate were near zero. The downside is $1M. The trial is also a single batch, inspected over five days. It may not represent a full year of production, and suppliers often put their best work into trial batches. That makes the 0.67% an optimistic estimate.

**Caveats.**
- The prior is a judgment call, but the answer holds under all three I tried.
- If you can negotiate a larger or longer trial with Brightline, such as 1,000 or more units spread over several production runs, the choice could flip. A clean result at that size would make Brightline's rate credibly lower than Acme's. A contract with Brightline that covers the penalty would also change the math.
- Neither supplier's price differs, so only defect costs and penalty risk matter here.
