**Sign with Acme.**

Brightline's trial looks better, but it is too small to tell you whether Brightline stays under the 3% penalty line. The penalty is large enough that the comparison turns on that line.

**The numbers**
- **Acme:** 1,000 defects in 50,000 units over 12 months, so 2.0%. Monthly rates stay between 1.85% and 2.09%. A full-year rate above 3% is effectively impossible. Expected cost is about 2,000 defects × $15 = **$30k**, with no penalty.
- **Brightline:** 1 defect in 150 units, so 0.67%. That is only 150 units over 5 days (30 a day). A trial this size is consistent with true rates anywhere from about 0.02% to 3.7% (95% interval).

**Cost at 100,000 units**
Defect cost is about $1.5M × the defect rate, plus a $1M penalty if the rate goes above 3%. The $15 return cost per defect is small next to the penalty. Brightline would save at most about $30k in returns if it were perfect. A 3% breach costs $1M. So Brightline only wins if the chance it exceeds 3% is below roughly 1.5–2%.

I put a few different priors on Brightline's true rate and updated on the trial:

| Prior on Brightline | Mean rate | P(>3%) | Expected cost |
|---|---|---|---|
| Uniform | 1.3% | 5.7% | ~$77k |
| Jeffreys | 1.0% | 2.8% | ~$43k |
| Skeptical (centered near Acme, 50 units' weight) | 1.0% | 1.7% | ~$32k |
| Skeptical (centered near Acme, 200 units' weight) | 1.4% | 2.0% | ~$42k |

Acme's expected cost is about $30k under every prior. The most optimistic prior I tried only roughly ties with it. The rest make Brightline $10–45k worse in expectation, and every one carries a real chance of a $1M hit that Acme doesn't.

**Caveats**
- A trial batch is often a supplier's best effort. A sample of 150 that happens to beat Acme's average is weak evidence, and the "fewer defects than usual" comparison makes it look stronger than it is.
- Acme's 2.0% comes from 50,000 units over a full year. Brightline's 0.67% comes from 150 units over 5 days, so the two estimates are not comparably reliable.
- The choice is also one-way for the year (no mid-year switch), so there's no chance to correct if Brightline disappoints.

**What would change my answer:** a larger Brightline trial. If they ship about 1,000–2,000 units across several weeks and the rate stays under ~1.5%, the chance of breaching 3% drops enough that Brightline would be worth considering. The most it can save is about $30k a year. Another route is to negotiate a contract with Brightline that covers the penalty or caps its defect rate. Neither is in the current terms.
