**Roughly 32 to 43 seconds faster, about 20–23% of West's pre-rollout time. I'd put "about 40 seconds" in the Q2 review with that range attached.** This is a bounded estimate. The data can't give a single clean causal number.

**What the data shows**
- West's completion time dropped sharply on 2026-03-15. The gap between West and East went from about +8s on 3/11–3/14 to about −34s from 3/15 on.
- East stayed flat the whole window, at 180.1s before and 179.4s after.
- West's average order value rose from $44.9 to $54.1. `promotions.log` ties that to a West-only price promotion launched the same day. I found nothing suggesting the promotion changes completion time, so I'm not treating it as a confound for this metric. I can't rule it out either.

**Why the headline number isn't the obvious one**
- A plain before/after comparison of West against East gives −50s. That is too high. A separate UX cleanup (`ux_cleanup_note.md`) was already shortening West's checkout before the rollout. West fell from about 207s to 187s over the five pre-rollout weeks while East didn't move.
- Part of the drop would have happened anyway, so I adjusted for it. I did that two ways:
  - **If the cleanup's gains kept growing after 3/15:** −32s (95% bootstrap interval −36 to −28). This extrapolates the pre-rollout trend.
  - **If the cleanup's gains stopped by 3/15:** about −41 to −43s. This compares the last 7–14 pre days to the first 7–14 post days.
- The trend flattens after 3/15 (slope about −0.03s/day in the West–East gap). That fits the second reading better, so I lean toward the 41–43s end. The data can't confirm it.

**What I can't establish**
- West wasn't picked at random. It was chosen for having the most abandonment complaints (`targeting_note.md`: 184 vs 97 in East). A region like that may have been on a different trajectory from East, and I can't test for that with this data.
- The rollout and the promotion started on the same day, so a promotion effect on completion time can't be separated out. It looks unlikely, not impossible.
- The interval above reflects day-to-day noise only. It doesn't include the uncertainty about which counterfactual is right, which is the bigger one here.

**Not done:** I didn't write a formal ledger or run a formal identification review, because you asked for a number rather than an audit. A cleaner confirmation would be a staggered rollout, or holding back a slice of West. If this number will drive a decision, I can run `causal-identification-review` on the design.
