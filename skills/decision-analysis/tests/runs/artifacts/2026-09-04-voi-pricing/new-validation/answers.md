# Diagnostic report answers

| Case | Conclusion | Verdict | Record |
| --- | --- | --- | --- |
| uninformative | Gross value $0; maximum break-even fee $0, and even a free report only ties. | break-even-only | [Record](uninformative.md) |
| missing-price | Gross value $30; with $5 delay, fee below $25 gives positive net value and $25 ties. | break-even-only | [Record](missing-price.md) |
| missing-model | Perfect-information upper bound $50; actual report value and break-even fee are unknown, so the $10 price cannot establish a worthwhile purchase. | upper-bound-only | [Record](missing-model.md) |
| missing-prior | Finite loss-span upper bound $100 over possible priors and signals; actual report value and justified fee remain unknown. | upper-bound-only | [Record](missing-prior.md) |
| priced | Gross value $30 minus $40 cost gives -$10 net value; decline the report at this price. | not-worth-it | [Record](priced.md) |
| equality | Gross value $30 minus $30 cost gives $0 net value; report and acting now tie. | not-worth-it | [Record](equality.md) |
| missing-delay | Gross value $30; with $5 opportunity cost and unknown delay D, the break-even fee is $25-D, conditional on nonnegative fees requiring D≤$25. | break-even-only | [Record](missing-delay.md) |

All calculations use only the corresponding supplied request.
No report was purchased.
