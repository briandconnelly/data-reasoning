**I can't give you a defensible number for the new flow's effect on checkout time, and I'd advise against putting one in the Q2 review.** The data shows West got faster, but it can't separate the new flow from other things that changed in West.

**What the data shows (descriptive only)**

| Median completion time (s) | East | West |
|---|---|---|
| Feb 1–14 | 180.5 | 205.4 |
| Mar 1–14 | 179.9 | 189.1 |
| Mar 15–Apr 11 (post) | 179.9 | 146.6 |

- West dropped about 42s (22%) from the two weeks before rollout to the post period.
- East didn't move.
- West also fell overnight on Mar 15, from 189.0s to 148.6s. That step lines up with the rollout date.

**Why that gap isn't the effect of the flow**

1. **Concurrent price promotion.** A West-only promotion launched on 2026-03-15, the same day as the rollout (`promotions.log`). Average order value in West jumped from about 44 to 54 that day. The data can't separate the promotion's effect on completion time from the flow's.
2. **Pre-existing West trend.** A shipping-step UX cleanup in West was already improving completion time before rollout (`ux_cleanup_note.md`). West fell from about 205s to 189s over the six pre-rollout weeks, while East stayed flat. East therefore isn't a valid stand-in for what West would have done without the new flow, so a West-minus-East comparison would credit the flow with the cleanup's gains.
3. **Non-random selection.** West was chosen because it had the most cart-abandonment complaints (184 vs 97 in East). A region picked for being the worst may be improving for its own reasons.

I haven't tried to correct for any of this. Any adjusted figure would depend on assumptions this data can't check, so it wouldn't be a measured effect.

**What you can say in the Q2 review**
- "West median checkout time fell from about 189s to about 147s after the 3/15 launch. East was flat. The launch coincided with a West-only promotion and followed an ongoing UX cleanup, so the new flow's separate contribution isn't established."

**How to get a real number**
- Run a holdout or randomized rollout: send a random share of West traffic, or of both regions, to the old flow.
- If the flow is only partly rolled out, compare users on the old and new flow within West over the same days.
- If neither is possible, find a region or segment that got the flow without the promotion. A design review (`data-reasoning:causal-identification-review`) could say whether anything in the existing data qualifies.

I didn't write up a formal ledger file for this. The conclusion rests on the notes in the data folder plus the medians above.
