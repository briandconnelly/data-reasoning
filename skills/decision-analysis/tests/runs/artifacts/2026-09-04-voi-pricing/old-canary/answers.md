# Answers and calculations

## uninformative

The maximum justified fee is $0.
The report is uninformative: both likelihood ratios equal 1, so expected decision loss stays $50 and gross information value is $0.

Record: [uninformative.md](uninformative.md).

## missing-price

The maximum justified fee is $25.
The report reduces expected decision loss from $50 to $20, worth $30 gross; subtract the $5 delay cost to get a $25 fee ceiling.
A $25 fee leaves you indifferent.

Record: [missing-price.md](missing-price.md).

## missing-model

There is insufficient information to justify the $10 purchase.
Perfect information would be worth $50, so $50 is an upper bound on a potentially justified fee, not an estimate of this report’s value.
At a $10 fee, net value could range from −$10 to +$40.

Record: [missing-model.md](missing-model.md).

## missing-prior

Only an upper bound is available: no report can be worth more than $50 under these losses.
For an unspecified p=P(H), perfect-information value is 100×min(p,1−p), whose maximum is $50.
This does not assign a probability or justify any positive fee for the actual report; its value could be zero.

Record: [missing-prior.md](missing-prior.md).

## priced

Do not buy at $40 on these inputs.
The report provides $30 of expected decision improvement, so its net value is $30−$40=−$10.

Record: [priced.md](priced.md).

## equality

You are indifferent at $30.
The report provides $30 of expected decision improvement and costs $30, leaving net value $0.
There is no strict expected-loss preference to purchase or decline.

Record: [equality.md](equality.md).

No report was purchased.
