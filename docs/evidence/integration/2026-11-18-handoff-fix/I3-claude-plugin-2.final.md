I can't give you a defensible number for how much faster the new flow made checkout. The West-vs-East comparison doesn't isolate the new flow's effect, so any figure would mostly measure other things.

**What the data shows (descriptive only, not an effect):**
- West median completion time was 187 s in the last pre-rollout week and about 146–147 s in each of the four weeks after 2026-03-15. That is a drop of about 41 s, which looks like a step at the rollout date.
- East was flat at about 180 s throughout.

**Why that drop can't be credited to the new flow:**
1. **The pre-trends aren't parallel.** West's gap to East shrank steadily before rollout, from 27.6 s to 7.0 s over six weeks, about 4.5 s per week. East didn't move. `ux_cleanup_note.md` says a separate shipping-step cleanup reached West gradually through the pre-period, and East never got it. A difference-in-differences comparison against East would credit that existing improvement to the new flow.
2. **A West-only promotion launched the same day.** `promotions.log` shows a price promotion starting 2026-03-15 in West. Average order value rose from 44.94 to 54.13 in West and stayed flat in East. I can't separate the promotion's effect on completion time from the new flow's.
3. **West was chosen for its high complaint volume** (184 complaints vs East's 97). That raises the possibility of regression to the mean, and nothing in the data lets me test it.

**For the Q2 review:** the safe wording is "West median completion time fell from about 187 s to about 147 s after the 3/15 rollout, coinciding with a West-only promotion and continuing UX improvements. The new flow's own contribution is not isolated." I'd avoid presenting 41 s, or a percentage, as the flow's effect.

**What would identify it:** a staggered or randomized rollout, for example by user or by a second region. A holdout within West would also work. Another option is a donor region with the same UX cleanup and no new flow. I can set up one of these designs if you'd like.

I saved the full review at `records/checkout_review.md`, and the structural validator passed with no findings.
