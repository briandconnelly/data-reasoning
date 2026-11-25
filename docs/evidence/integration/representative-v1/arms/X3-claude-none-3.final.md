**Deploy Model B.**

I scored both models on the 10,000 holdout customers (13.8% churned). I measured them the way you'll use them, as the 500 highest-scored customers on one list.

| | Model A | Model B |
|---|---|---|
| Churners in the top 500 | 173 (34.6%) | 302 (60.4%) |
| Overall AUC | 0.687 | 0.817 |

- **Size of the gap:** B finds about 129 more churners than A in a 500-call list. A bootstrap over customers puts that gap at roughly 100 to 150, so B is better in essentially every resample.
- **Agreement:** The two top-500 lists share only 117 customers, so the choice changes who gets called.
- **Baseline:** Calling 500 customers at random would reach about 69 churners, so A is better than random but B is much better.
- **Data checks:** There were no duplicate customer IDs. No scores were tied at the top-500 cutoff, so the list is well defined.

This is one quarter of holdout data, so I can't say how stable B's lead is over time. With a gap this large, I wouldn't expect the ranking of the two models to flip.
