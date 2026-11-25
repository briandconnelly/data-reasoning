**Deploy Model B** if the goal is to reach as many likely churners as possible with 500 calls. On last quarter’s holdout, Model B’s top 500 included **302 customers who churned**, compared with **173** for Model A. That’s **129 more observed churners** for the same call budget.

| Holdout metric | Model A | Model B |
|---|---:|---:|
| Observed churners in the top 500 | 173 | 302 |
| Precision at 500 | 34.6% | 60.4% |
| Overall accuracy at a 0.5 cutoff | 84.6% | 79.5% |

Model A leads on overall accuracy at 0.5, but the call list is built by rank. Precision at 500 measures how many of those calls go to customers who churned.

I resampled the 10,000 holdout customers 5,000 times, rebuilding both top-500 lists on each draw. The middle 95% of Model B’s leads ranged from **100 to 153 additional churners**. That range reflects customer sampling within last quarter. The recommendation assumes next quarter’s list is drawn from a similar population. If the goal is to maximize **churn prevented**, the holdout leaves that question open because it doesn’t measure who would stay as a result of a call.
