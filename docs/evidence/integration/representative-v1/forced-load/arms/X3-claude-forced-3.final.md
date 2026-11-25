**Deploy Model B.** Its top-500 list catches far more of the customers who actually churn.

Estimation on the 10,000 holdout customers, base churn rate 13.8%. Precision means the share of the called customers who actually churned.

| | Model A | Model B |
|---|---|---|
| Precision in top 500 (your call list) | 34.6% (173 churners) | 60.4% (302 churners) |
| Precision in top 100 | 48% | 81% |
| Precision in top 1,000 | 30.5% | 50.5% |
| AUC (ranking quality overall) | 0.687 | 0.817 |

- **Size of the gap:** B beats A by 25.8 points of precision at 500, about 129 more churners reached per list. A bootstrap over customers (2,000 resamples, 95% interval) puts the paired difference at +20 to +31 points. The whole interval is far above any plausible practical threshold.
- **Not a tie-breaking artifact:** Both models have clear score gaps at the 500 cutoff. B also wins at every list size I checked (100, 250, 500, 1,000) and on AUC, so the result doesn't depend on the exact 500 cutoff.
- **Different customers:** The two top-500 lists share only 117 customers, so the choice changes who gets called, not just the order.

**Limits:**
- The estimate assumes next quarter's customers and churn behavior look like last quarter's. Drift would move both models' absolute precision, but a 20+ point paired gap across all list sizes is unlikely to reverse.
- Precision at 500 is a prediction-quality measure, not a causal one. It says B finds likelier churners. It doesn't say calls will save them. If the team wants to call people they can actually persuade, that needs a separate test with a randomized holdout of the call list.
- I did not check how the holdout relates to the training data, or whether scores were calibrated or tuned against this holdout. If B's hyperparameters were selected on this same data, its numbers are somewhat optimistic. That is worth confirming, though the margin is large.

I wrote no ledger file. The estimation route doesn't require one.
