**Deploy Model B.** With a budget of 500 calls, Model B’s top-ranked list contained 302 actual churners on last quarter’s holdout. Model A’s contained 173. That’s **129 more churners reached with the same number of calls**. [Holdout scores](/var/folders/4_/s6fbcjyn4b13xdxkd3lv0kw00000gn/T/int-arm-4z2a88mh/data/holdout_scores.csv)

| Model | Churners in top 500 | Precision at 500 | Accuracy at 0.5 cutoff |
|---|---:|---:|---:|
| A | 173 | 34.6% | 84.6% |
| B | 302 | 60.4% | 79.5% |

Model A wins on the currently reported 0.5-cutoff accuracy. Precision at 500 matches how the retention team will actually select customers.

A paired bootstrap that rebuilt both top-500 lists on each resample gave a 95% interval of **100 to 153 additional churners** for Model B. The recommendation assumes next quarter’s customer mix and model performance are comparable to the holdout. The scores and churn outcomes measure how well each model targets likely churners. Estimating how many customers the calls would retain requires evidence on the effect of outreach.
