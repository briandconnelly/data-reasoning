**Deploy Model B.** On last quarter’s holdout, it put 302 actual churners in the top 500, compared with 173 for Model A. That’s **129 more churners reached** for the same 500 calls.

| Holdout metric | Model A | Model B |
|---|---:|---:|
| Actual churners in top 500 | 173 | **302** |
| Precision at 500 | 34.6% | **60.4%** |
| Accuracy at the 0.5 cutoff | **84.6%** | 79.45% |

Precision at 500 matches the team’s calling policy because the team ranks customers and fills a fixed list. The holdout measures how many churners each model identifies. It doesn’t measure how many calls would prevent churn.
