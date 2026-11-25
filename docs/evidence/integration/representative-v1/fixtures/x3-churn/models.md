# Candidate churn models

Both models were trained on the same data and scored on last quarter's holdout customers.
Each score is the model's churn probability for that customer; `churned` is what actually happened.
The team currently reports each model's accuracy at a 0.5 cutoff: a customer scoring 0.5 or more counts as a predicted churner.
