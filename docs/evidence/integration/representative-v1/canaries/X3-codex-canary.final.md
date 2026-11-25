**Deploy Model B** if the goal is to reach as many would-be churners as possible with 500 calls. On last quarter’s holdout, Model B put **302 actual churners** in its top 500, compared with **173** for Model A. That’s **129 more churners reached** for the same call volume.

| Model | Actual churners in top 500 | Precision at 500 | Accuracy at 0.5 cutoff |
|---|---:|---:|---:|
| A | 173 | 34.6% | 84.60% |
| B | 302 | 60.4% | 79.45% |

Model A’s higher accuracy describes its performance when classifying all 10,000 customers at a fixed cutoff. The call campaign uses a fixed list size, so precision at 500 matches the deployment rule.

The recommendation assumes last quarter’s holdout is reasonably representative of next quarter. The holdout measures how well each model finds churners. How many calls would actually prevent churn remains unknown.
