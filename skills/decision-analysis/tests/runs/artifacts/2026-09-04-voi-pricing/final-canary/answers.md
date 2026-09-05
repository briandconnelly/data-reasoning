# Diagnostic report answers

All dollar values use only the supplied decision losses, probabilities, and costs.

| Case | Result | Verdict |
| --- | --- | --- |
| [uninformative](uninformative.md) | Gross value $0; fee break-even $0, so no positive fee is justified. | `break-even-only` |
| [missing-price](missing-price.md) | Gross value $30; after $5 delay, fee break-even is $25, with positive net value below $25. | `break-even-only` |
| [missing-model](missing-model.md) | Perfect-information upper bound $50; actual report value unknown, so the $10 price is not established as worthwhile. | `upper-bound-only` |
| [missing-prior](missing-prior.md) | Loose loss-range upper bound $100; actual value and justifiable fee cannot be established. | `upper-bound-only` |
| [priced](priced.md) | Gross value $30 minus $40 fee gives −$10 net; decline at this price. | `not-worth-it` |
| [equality](equality.md) | Gross value $30 minus $30 fee gives $0 net; buying and declining tie. | `not-worth-it` |
| [missing-delay](missing-delay.md) | Gross value $30; fee break-even is $25−d, where d is unknown dollar delay cost. | `break-even-only` |

The records contain provenance, arithmetic, conditions, and references to the supplied skill's governing rules.
No report was purchased.
