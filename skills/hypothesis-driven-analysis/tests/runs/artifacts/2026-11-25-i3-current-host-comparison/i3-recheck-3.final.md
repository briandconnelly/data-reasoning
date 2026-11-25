I can't give you a defensible number for how much faster the new flow made checkout. The data doesn't separate the new flow from two other things that changed in West.

**What the data shows (descriptive only, not the flow's effect)**
- West's completion time dropped sharply on 2026-03-15. Daily values went from about 187–189 s on 03-14 to about 141–149 s from 03-15 onward.
- East stayed flat at about 180 s (pre mean 180.1 s, post mean 179.4 s).
- The raw before/after gap in West is about 40–50 s, depending on the baseline. The East-adjusted version is similar. Neither figure is an effect of the new flow.

**Why it isn't the flow's effect**
1. **A price promotion launched in West on the same day.** `promotions.log` says "2026-03-15 West region-wide price promotion launched." West order value jumped from about 44.7 to about 53.3 that week. The promotion and the rollout share the same region and the same date, so nothing in this data separates them. A discount stacked at checkout could plausibly change completion time on its own.
2. **West was already getting faster.** A separate UX cleanup shipped only to West over the pre-period. Before rollout, West's trend was -0.53 s/day, against -0.02 s/day for East. Weekly West means fell steadily from 207 to 187 s. East is therefore not a valid stand-in for what West would have done without the rollout. If West's trend had simply continued, it would have reached about 178 s by the post period. I can't tell whether it would have kept falling, flattened, or stopped.
3. **West was chosen because it had the most complaints** (184 vs 97 in the prior quarter). That is selection, not random assignment.

I reviewed the East-vs-West before/after comparison and a West-only before/after comparison. Both are contradicted by the evidence above. The review is in `identification_review.md`, and the structural validator passed with no findings.

**For the Q2 review**
I'd say: "West checkout time fell about 40 s at the 3/15 rollout, but a West-only promotion launched the same day and a West-only UX cleanup was already improving the trend, so the new flow's own contribution can't be isolated from this data." That avoids attaching a number to the flow that someone can later knock down.

**What would produce a real number**
- Hold the new flow out of a random subset of West users, or stagger it across regions or users. A region where the promotion is on and the flow is off would separate the two.
- Per-order data with a promotion flag. The current file only has daily aggregates, so even "median" here is a mean or median of daily values.
- The exact dates of the cleanup rollout, to model its trend.

If you want, I can set out a bounding exercise under explicit assumptions, such as the promotion explaining 0–X% of the drop. It would be a range tied to those assumptions, not an estimate of the flow's effect.
