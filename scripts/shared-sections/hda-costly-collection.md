### Costly collection is a modifier, not a route

Collection is costly when the user, the tool, or the configuration states a cost — a price, a quota, a rate limit, a latency, a size — when you observe the cost directly, or when the pull exceeds a budget they set.
What triggers this is a cost someone stated or you measured, not one you suspect; a guess is not an observable condition, and the first slow query is.
If you have a number and cannot tell whether it is big enough to matter, treat it as costly: the plan is six lines and the pull is not.
Cost does not select the route, because cost says nothing about whether there is anything to explain.
A metered warehouse does not turn "what was the median order value in June" into a question with competing explanations; it is the same descriptive answer, bought at a worse price.

What costly collection buys is the plan, not the hypothesis table.
It binds any costly pull you make, on every route and on work that took no route at all — a metered dump you are only reformatting is still metered.
Before collecting, write down: the decision or output the pull serves, the exact source and action, why this is the cheapest adequate collection, a budget in the relevant unit, the authorization covering it (or `BLOCKED`), and the condition under which you stop or re-pull.
That record is the thing the expense is meant to buy: the fishing expedition you do not pay for twice.
A datum you have already pulled — including one an orientation probe returned to show the data's shape — is already paid for: when the probe returned the same rows, at the same grain and snapshot, that the systematic pull would, reuse them rather than paying twice.
Count a reused probe's spend against the plan's budget rather than leaving it uncounted, and record it in the plan's `Already paid for` field.
When the probe only sampled, truncated, or reshaped the data, a re-pull is legitimate — take it and say why, rather than stitching an inconsistent dataset together to dodge one.
It is worth writing whether the answer is one median or five rival explanations.

The direct route records nothing, unless collection is costly, in which case it records the collection plan and nothing else.
The estimation route records estimand, population, uncertainty method, and threshold.
The mini route records a one-paragraph ledger.
Templates for all record forms are in [references/ledger-template.md](references/ledger-template.md).
The gates and the data rules below bind every evidence-bearing route; only the ledger ceremony varies by route.

