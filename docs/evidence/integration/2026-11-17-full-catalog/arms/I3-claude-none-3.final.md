**Best estimate: the new flow cut median checkout completion time by about 40 seconds, roughly 21%.** For the Q2 review I'd say "about 40 s (~20%) faster".

Here is how I got that, and why I didn't use the simple West before/after number.

**What the data shows**
- West's median was 196.6 s before 2026-03-15 and 146.6 s after. That is a 50 s drop, about 25%.
- East's median didn't move: 180.0 s before and 179.9 s after.
- West has a clear step on rollout day. It went from 189.0 s on 3/14 to 148.6 s on 3/15, and it has stayed around 146 s since.

**Why 50 s overstates it**
- The shipping-step UX cleanup was already improving West before the rollout. East didn't get it.
- West's median fell from 205 s to 197 s to 189 s over the three two-week blocks before 3/15. Part of the 50 s gap is that earlier improvement.
- Comparing the last pre-rollout week (median 187.4 s) with the post period (146.6 s) strips most of it out. That gives the ~41 s figure, or about 22%.

**Caveats**
- **Not a clean A/B test.** West was picked because it had the most cart-abandonment complaints (184 vs 97 in East). A difference-in-differences against East would therefore be shaky, and I didn't lean on it.
- **The cleanup may not have finished.** If it was still improving West at the time of rollout, some of the 40 s may belong to it, so treat 40 s as an upper-end estimate. The step on 3/15 is sharp, though, and a gradual cleanup doesn't usually produce that.
- **The price promotion shouldn't affect the time estimate.** It launched in West the same day and explains the higher average order value there. It plausibly affects order value and volume, not how long checkout takes. I didn't verify that, and I didn't check whether the promotion changed who checks out.

My uncertainty is about ±5–10 s, and I didn't compute a formal confidence interval.
