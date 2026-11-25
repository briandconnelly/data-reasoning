**Deploy Model B.** Its top 500 holds about 74% more actual churners than Model A's.

I treated this as a predictive comparison, so I used the estimation route and no causal claims are involved. The metric is the number of real churners among each model's 500 highest-scored customers. That matches how the retention team will use it.

On last quarter's 10,000 holdout customers (1,377 churned, a 13.8% base rate):

| | Model A | Model B |
|---|---|---|
| Churners in top 500 (precision 34.6% vs 60.4%) | 173 | 302 |
| Churners in top 100 | 48 | 81 |
| Churners in top 1,000 | 305 | 505 |
| AUC | 0.687 | 0.817 |
| Accuracy at 0.5 cutoff | 84.6% | 79.5% |

- **Size of the gap:** B finds 129 more churners than A in the top 500. A paired bootstrap over customers (1,000 resamples, 95% interval) puts that gap at +99 to +153. The whole interval is far above zero, so this is not sampling noise. The same ordering holds at every list size I checked, from 100 to 2,000.
- **Why the accuracy numbers point the wrong way:** the team's current report ranks A higher, at 84.6% against 79.5% accuracy. That metric doesn't fit this decision, for two reasons:
  - The 0.5 cutoff doesn't match the 500-call list. A flags only 533 customers at 0.5, while B flags 2,394.
  - With 86% non-churners, accuracy mostly rewards a model for staying quiet.
  - The 500-call list depends only on ranking, and B ranks better.
- **Data checks:** there are no missing values or duplicate customers. Neither model has tied scores at the 500th-place cutoff, so the top-500 lists are unambiguous.

**Limits:**
- The 302 and 173 figures come from last quarter's customers. Next quarter's absolute numbers will shift if churn rates or the customer mix change. The size of B's lead is the reliable part. I can't test whether it holds under drift with this file.
- I didn't test whether the 129 extra churners are saveable. Calling a customer who would have churned anyway, or who can't be retained, wouldn't help. That needs a retention-outcome measurement, and it applies equally to either model.
- `models.md` says both models were trained on the same data. I couldn't check that, and I assumed the holdout customers weren't in the training data.

I didn't write a ledger file. The estimation route only calls for recording the estimand, population, uncertainty method and threshold, and those are all stated above.
