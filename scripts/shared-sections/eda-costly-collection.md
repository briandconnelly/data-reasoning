### Costly collection (modifier, not a route)

Collection is costly when the user, the tool, or the configuration states a cost — a price, a quota, a rate limit, a latency, a size — when you observe the cost directly, or when the pull exceeds a budget they set.
A suspected cost is not a trigger; a stated or measured one is, and a number you cannot classify is treated as costly.
Cost never changes the route: a metered warehouse makes profiling more expensive, not more inferential.
Before any costly pull, on any route, write down: what the pull serves, the exact source and action, why this is the cheapest adequate collection, a budget in the metered unit, the authorization covering it (or `BLOCKED`), and the condition under which you stop or pull again.
Data already paid for is reused, not re-pulled, when it matches the grain and snapshot the exploration needs; a probe that sampled, truncated, or reshaped the data legitimizes a re-pull — take it and say why.
A reused probe's spend counts against the pull's budget rather than going uncounted.
The invariants this section must preserve in common with `hypothesis-driven-analysis`'s costly-collection rule are listed in [decisions/001-shared-gate-authority.md](decisions/001-shared-gate-authority.md); rewording either statement requires re-checking that list.
