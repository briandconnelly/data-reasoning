### Costly collection (modifier, not a route)

Collection is costly when the user, the tool, or the configuration states a cost — a price, a quota, a rate limit, a latency, a size — when you observe the cost directly, or when the pull exceeds a budget they set.
A suspected cost is not a trigger; a stated or measured one is, and a number you cannot classify is treated as costly.
Cost never changes the route: a metered warehouse makes a probe more expensive to run, not a design more identified.
Before any costly pull, on any route — a probe against a metered source is one — write down: what the pull serves, the exact source and action, why this is the cheapest adequate collection, a budget in the metered unit, the authorization covering it (or `BLOCKED`), and the condition under which you stop or pull again.
Data already paid for is reused, not re-pulled, when it matches the grain and snapshot the probe needs; a pull that sampled, truncated, or reshaped the data legitimizes a re-pull — take it and say why.
A reused pull's spend counts against the plan's budget rather than going uncounted.
The invariants this statement must preserve in common with the other skills' costly-collection rules are listed in `skills/exploratory-data-analysis/decisions/001-shared-gate-authority.md`; rewording this statement requires re-checking that list by hand.

