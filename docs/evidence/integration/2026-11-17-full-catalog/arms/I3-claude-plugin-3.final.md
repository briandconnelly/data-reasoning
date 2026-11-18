Status: I've checked the data and have a number. Here is the answer.

**Short answer for Q2:** West checkout completion time was about **37 seconds faster (roughly 20%)** in the step at the 2026-03-15 rollout. The plausible range is **32–43 seconds (about 18–23%)**, depending on how you treat West's earlier improvement. I'd call it an associated improvement, not a clean causal effect of the new flow. This is a quick analysis, not a full preregistered investigation, and I wrote no ledger file.

**What the data shows**
- East is flat at about 180 s throughout.
- West was already improving before the rollout, falling about 3.7 s per week. That is the separate shipping-step UX cleanup (`ux_cleanup_note.md`), and East never got it. West went from about 206 s in early February to about 189 s in the two weeks before launch.
- West then dropped to about 144.5 s in the first post-launch week and stayed near 146 s. The post-launch slope is about +0.4 s per week, so the earlier steady decline has stopped. The pre-trend residual noise is about 2.6 s, so the drop is far larger than noise.

**How the estimate moves with the counterfactual**

| Assumption about West without the new flow | Effect |
|---|---|
| Flat at the last 2 pre-weeks (about 189 s) | about −43 s (−23%). This is the same as a difference-in-differences against East. |
| Pre-trend continues to the launch day | about −37 s |
| Pre-trend continues through the whole post-period | about −32 s average |

**Why this isn't a clean causal number**
- **East can't serve as the comparison.** Because of the UX cleanup, West and East were not moving in parallel before launch. A plain West-versus-East difference-in-differences would credit some of the cleanup's gains to the new flow.
- **A price promotion launched in West the same day.** `promotions.log` shows it started 2026-03-15. West's average order value rose from $44.9 to $54.1 while East stayed flat. I can't rule out that it affected completion time, for example by changing who checks out or how long they take. Volume barely moved, which makes a large composition shift less likely but doesn't settle it.
- **West was chosen because it had the most cart-abandonment complaints.** It had 184 complaints in the prior quarter, against 97 for East. A region picked for being the worst may have more room to improve, so the effect may not carry to other regions.

**For the review slide:** "West median checkout time fell about 37 s (about 20%) at the new-flow launch; estimates range 32–43 s depending on how much of West's pre-existing UX-cleanup trend is netted out. A same-day West promotion and non-random region selection mean this is not a clean causal estimate." The figures above are means of daily values. The data is already daily medians, and I did not recompute from raw orders.

To get a defensible causal number, you would need a clean comparison. A staggered rollout, or a holdout of West traffic on the old flow, would give one. I can run an identification review on what that design would need if you want it.
