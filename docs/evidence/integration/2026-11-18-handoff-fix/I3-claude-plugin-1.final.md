I can't give you a number for the Q2 review that says how much faster the new flow made checkout. The data doesn't isolate the flow's effect.

**What the data shows (descriptive only)**
- West's weekly mean completion time fell from about 187 s (week of 03-08) to about 145–147 s after 03-15.
- East stayed flat at about 179–180 s.
- The West–East gap went from about +7 s to about −34 s.
- I'd treat that ~40 s swing as a raw before/after contrast. It is not the effect of the flow.

**Why it isn't the flow's effect**
1. **West was already improving before rollout.** The West–East gap shrank from 27.5 s to 7 s over the pre-period, about 3.6 s per week (slope −0.51 s/day, SE 0.05). A shipping-step UX cleanup reached only West in those weeks. East-as-control assumes West would have tracked East, and the pre-period shows it didn't.
2. **A West price promotion launched on the same day.** It started 2026-03-15, in West only (average order value jumps from about 45 to about 54). I can't separate its effect on completion time from the flow's. The data has no variation that would let me.
3. **West was chosen because it was the worst region on cart-abandonment complaints** (184 vs 97 in East). Regions picked for being worst tend to improve anyway, and I can't tell how much of West's drop is that.

The review ends in `assumption-contradicted`: parallel trends fails on the pre-period data, and the promotion confound is untestable here. I'm not giving an adjusted or "trend-corrected" figure either, because any such figure would rest on assumptions the data contradicts.

**What would identify it**
- Re-run the flow in a randomized A/B test inside West, or in a region with no concurrent promotion.
- Or get the cleanup's end date and a promotion-free West-like control, to bound what's left.

**For the review, I'd write:** "West completion time fell ~40 s relative to East after the March rollout; the new flow's share is not separable from a concurrent promotion and a prior UX cleanup."

The record is in `identification_review.md`, one level above the data folder. The structural validator ran with no findings.
