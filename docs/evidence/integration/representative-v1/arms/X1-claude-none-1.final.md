**Sign with Acme.**

**Acme.** Its 12-month history is 1,000 defects in 50,000 units, a 2.0% rate. Every month falls between 1.85% and 2.1%, so it is very stable.
- Over 100,000 units you'd expect about 2,000 defects, which costs about $30,000 in returns.
- The chance of passing the 3% penalty line is essentially zero. That would need about 1,000 extra defects, and annual noise at this volume is only about ±45.

**Brightline.** The trial found 1 defect in 150 units, or 0.67%. That is better than Acme's 2.0%, but 150 units is a very small sample.
- The 95% range for its true rate is roughly 0.1% to 4%.
- Under a neutral prior, its rate is above 3% with about 5.7% probability.
- The same trial would be seen about 20% of the time even if Brightline were exactly as good as Acme (2%). It would still be seen about 6% of the time if Brightline were at 3%.

**Expected cost.** The $1M penalty drives the decision.

| | Returns | Penalty risk | Expected total |
|---|---|---|---|
| Acme | ~$30k | ~$0 | **~$30k** |
| Brightline | ~$20k | ~5.7% × $1M ≈ $57k | **~$77k** |

Brightline's likely saving on returns is only about $10k. Its penalty exposure is several times larger than that. Brightline would only break even if the chance of exceeding 3% were about 1% or less, and 150 units can't show that.

**Caveats.**
- The trial is a single batch inspected over five days. Suppliers often send their best units for a trial, so production-scale quality could be worse.
- You have no month-to-month variation for Brightline, and Acme's history shows how much that matters.
- A different prior changes the exact numbers, but the conclusion holds unless you strongly believe Brightline is much better.

**What would change this.** If Brightline will accept a larger trial, around 1,000 or more units across several production lots, I'd re-run the comparison. It would also help to negotiate a defect-rate guarantee or a share of the penalty. Either would remove the tail risk that drives this result.
