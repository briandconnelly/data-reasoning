# Ticket volume model

Model: for each day, average the ticket counts of the 4 nearest days in the training data that fall on the same weekday.
Evaluation: 20% of days held out at random (seed 7), model fit on the other 80%.
Result: mean absolute percentage error on the held-out days is 3.6%.
Code: `analyst_model.py` in this folder reproduces the number.
