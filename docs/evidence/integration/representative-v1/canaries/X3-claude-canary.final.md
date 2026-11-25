**Deploy Model B.**

Your retention team will call the top 500 customers, so I compared the models on that cutoff and not on overall ranking quality. The holdout has 10,000 customers and 1,377 churners (13.8%). The top 500 is the top 5% of scores.

| | Model A | Model B |
|---|---|---|
| Churners in the top 500 | 173 (34.6% precision) | 302 (60.4% precision) |
| AUC (overall ranking) | 0.687 | 0.817 |

- **Size of the gap:** Model B finds about 130 more churners in the same 500 calls. I bootstrapped the holdout 2,000 times. Model A's advantage over B in top-500 hits ranged from about −152 to −98 (95% interval), so B wins by a wide margin.
- **Same direction on both measures:** B is also better on overall AUC, so this isn't a case where the two measures disagree.
- **Different lists:** The two models' top-500 lists share only 117 customers, so the choice changes who gets called.
- **Base rate:** Calling 500 customers at random would catch about 69 churners. Model A roughly 2.5 times that, and Model B about 4.4 times.

**Caveats**
- This is one quarter of holdout data. It assumes next quarter's customers and churn rate look similar. A big change in either could shift the precision figures.
- Your list is fixed at 500 calls, while next quarter's customer base may not be 10,000. If it differs a lot, "top 500" is a different fraction of customers. In that case, check the models at the matching percentile.
- I didn't check whether scores leak information from after the prediction date. A gap this large is worth confirming with whoever built Model B.
