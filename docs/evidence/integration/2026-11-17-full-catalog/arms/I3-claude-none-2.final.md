**The new checkout flow made checkout about 37–40 seconds faster in West, roughly 20%. Use about 38 s (~20%) for the Q2 review.** The naive before/after figure is about 50 s, and that overstates the effect.

| Method | West change |
|---|---|
| Raw mean, pre vs post (196.7 → 146.1 s) | −50.5 s (−26%) |
| Same vs East (East: 180.1 → 179.4 s) | about −50 s |
| Last 14 pre-days vs first 14 post-days (189.2 → 145.8 s) | −43 s |
| Pre-trend extrapolated to the rollout date | about −37 s |
| Day-of-rollout step (189.0 → 148.6 s) | −40 s |

- **Why the raw number is inflated:** West was already getting faster before rollout. The shipping-step form cleanup shipped to West only, and completion time fell from about 205 s to 189 s over February and early March, roughly 0.53 s/day (`ux_cleanup_note.md`). A raw pre/post average credits that earlier improvement to the new flow.
- **Why East doesn't fix it:** East is flat, so it controls for seasonality but not for the West-only cleanup. A difference-in-differences against East would still show about −50 s.
- **The step at 3/15 is clean:** West drops about 40 s in a single day and then stays flat at about 146 s. Slope after rollout is about 0.05 s/day, versus −0.53 s/day before. That sharp break is why I trust the 37–40 s figure.
- **Range:** I'd quote 37–43 s, depending on how much of the cleanup's continued gains you assume would have kept going. Extrapolating the old trend gives −37 s at rollout. Linear extrapolation is a modelling assumption, and the true no-rollout path is unknowable. The −43 s window comparison counts a little cleanup benefit as flow benefit.
- **Caveat on the promotion:** The 3/15 West price promotion (`promotions.log`) raises average order value and overlaps the rollout exactly. It shouldn't directly speed up checkout, but I can't rule out some change in West's mix of orders. I'd flag it.
- **Caveat on selection:** West was picked because it had the most abandonment complaints (184 vs 97 in East). It may differ from East in ways that matter, so don't assume the same gain in East. It's an observational comparison, not a randomized one.

Suggested wording: *"The new checkout flow reduced median checkout time in West by ~38 s (~20%), after accounting for a concurrent UX cleanup that had already been improving West; unadjusted, the drop looks like ~50 s."*

One more note: the data is daily averages (`completion_time_seconds`), not medians. I treated it as the median series you described. If you have order-level data, I can compute the real median effect and confidence intervals.
