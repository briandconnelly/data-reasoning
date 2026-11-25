**Deploy Model B.** It finds far more actual churners in the top 500 than Model A, and the gap is much larger than sampling noise.

I ranked all 10,000 holdout customers by each model's score and counted how many of the top 500 actually churned. The overall churn rate is 13.8% (1,377 churners), so a random list of 500 would catch about 69.

| | Churners in top 500 | Precision@500 | AUC |
|---|---|---|---|
| Model A | 173 | 34.6% | 0.687 |
| Model B | 302 | 60.4% | 0.817 |

- **The gap is large:** B finds 129 more churners than A in the top 500. Bootstrapping the holdout customers 1,000 times gives a 95% interval of +99 to +153 churners for B over A. The interval is nowhere near zero.
- **It holds across list sizes:** B also leads at the top 100 (81 vs 48), 250 (179 vs 99), 1,000 (505 vs 305) and 2,000 (783 vs 533).
- **AUC agrees:** B leads by 0.115 to 0.144 at 95%, so the ranking is better overall and not only at the top.

Data checks: there are no missing values or duplicate customer IDs. Scores are nearly all distinct (9,747 unique values for A, 9,485 for B), so ties at the cutoff of 500 don't affect the result.

**Limits**
- **Single holdout:** This is one quarter's holdout. The bootstrap covers sampling noise but not drift between this quarter and next, such as seasonality or a change in who the customers are. The size of the gap makes a reversal unlikely, but I can't test it from this file. Re-check precision@500 after the first quarter in production.
- **Scope of the comparison:** B is better at finding customers who would churn. Whether calling them reduces churn, or whether A's list would respond better to a call, is a causal question this data can't answer. It only supports the choice of model, not an estimate of the retention team's impact.
- **Scoring pipeline:** I assumed next quarter's scores are produced the same way as these. If B depends on features that are only available in some cases, check that first.

I did not write a ledger file. The estimation route only needs the estimand, population, uncertainty method and threshold, and those are all covered above. The scripts are in `/tmp/an/a.py`.
