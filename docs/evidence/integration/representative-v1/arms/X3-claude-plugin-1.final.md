**Deploy Model B.**

I scored both models on the 10,000 holdout customers. 1,377 of them churned, a base rate of 13.8%. Your use case is a call list of the 500 highest-scored customers, so I compared the models on that list.

| Metric | Model A | Model B |
|---|---|---|
| Precision in the top 500 (churners per 500 called) | 34.6% (173) | 60.4% (302) |
| Precision in the top 100 | 48% | 81% |
| Precision in the top 1,000 | 30.5% | 50.5% |
| AUC (overall ranking quality) | 0.687 | 0.817 |

- **Size of the gap:** B's list would reach about 129 more churners than A's. A bootstrap over customers gives a 95% interval of roughly 98 to 152 more, so the gap is not noise.
- **Consistency:** B is ahead at every list size I checked, and on AUC too. The result doesn't depend on exactly where the cutoff falls.
- **Different lists:** the two models' top-500 lists share only 117 customers, so the choice changes who gets called.

Two caveats:
- This assumes next quarter's scoring pool is about the same size as this holdout (about 10,000 customers). If the pool is much larger or smaller, 500 is a different fraction of it. B's lead held at every top-k I checked, so I'd expect the ranking to hold, but the exact precision would shift.
- Precision measures who churned, not who the calls would save. If the retention team's offer works better on some kinds of customers, such as those about to churn anyway, the best list could differ. The data here can't tell us that.
