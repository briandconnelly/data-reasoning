**Deploy Model B.**

Your retention team will call the top 500 customers on one list, so I compared the models on that cutoff. I took the 500 highest scores from each model on the 10,000 holdout customers (13.8% churned overall).

| | Model A | Model B |
|---|---|---|
| Churners in top 500 | 173 (34.6%) | 302 (60.4%) |
| Overall AUC | 0.687 | 0.817 |

- **Size of the gap:** Model B reaches about 129 more churners with the same 500 calls. The two top-500 lists share only 117 customers.
- **Reliability:** I resampled the holdout 500 times to test this. Model B came out ahead in every resample, by roughly 98 to 153 churners (95% interval).
- **Data quality:** The file has 10,000 unique customers with no missing values.

- **Single quarter:** This is one quarter of holdout data. If customer behavior shifts, the gap could narrow, so track the top-500 hit rate after deployment.
- **Past churn only:** The holdout shows who churned. It doesn't show who would have stayed because of a call, so it can't tell you which model's list is better for retention.
