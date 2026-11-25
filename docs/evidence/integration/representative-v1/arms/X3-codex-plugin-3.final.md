**Deploy Model B for the 500-call list.** On last quarter’s 10,000-customer holdout, Model B put **129 more actual churners** in the top 500 than Model A did.

| Model | Actual churners in top 500 | Precision at 500 | Accuracy at 0.5 |
|---|---:|---:|---:|
| A | 173 | 34.6% | 84.60% |
| B | 302 | 60.4% | 79.45% |

Model A had higher accuracy at the team’s usual 0.5 cutoff. Model B had higher precision at 500, which matches how the retention team will select customers.

A paired bootstrap that reranked both models on each resampled list gave a 95% interval of **100 to 153 additional churners in Model B’s top 500**, assuming next quarter’s list is drawn from a similar customer population. The holdout measures who churned. Estimating how many customers the calls would retain requires evidence on the effect of outreach.
