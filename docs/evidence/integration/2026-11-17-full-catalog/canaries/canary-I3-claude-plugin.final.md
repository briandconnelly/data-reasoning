Status: I've read all the files and run the numbers.

**Headline: West's median checkout time dropped about 40 seconds (about 21%) right after the 2026-03-15 rollout. That figure is not cleanly attributable to the new flow, so I'd present it as a range with caveats.**

| Measure | Result |
|---|---|
| West, week before rollout | about 187 s |
| West, after rollout (flat through 4/11) | about 146 s |
| Raw drop | about 41 s (about 22%) |
| East, before and after | about 180 s, flat (180.1 vs 179.4) |
| Naive before/after difference vs. East | about 50 s (about 43–50 s depending on baseline window) |
| West step at launch, after removing its pre-existing trend | about 39 s at launch, about 26 s by the end of the window |

**Why not just quote 50 s:**
- **The UX cleanup:** West was already improving by about 0.5 s per day before launch, from 207 s to 187 s over six weeks. The cleanup in `ux_cleanup_note.md` explains that, and East did not get it. Comparing West's pre-period average to its post-period average credits that earlier gain to the new flow.
- **The step at launch:** the drop is a sharp step. West went from about 187–189 s on the days before launch to about 141–149 s on the days after, and has been flat since. That jump is the most defensible measure of the new flow's effect, about 40 s. If the cleanup's trend had kept going, the effect shrinks to about 26 s by April, but a trend that long is unlikely, so I'd lean on about 40 s.

**What I can't rule out:**
- **Price promotion:** it launched in West on the same day (`promotions.log`). It plausibly changes checkout behavior, and I can't separate it from the new flow with this data. The log notes its effect on order value, not completion time.
- **How West was chosen:** West got the rollout because it had the most abandonment complaints (184 vs. 97 in East). That makes it a different kind of region from East, so East is an imperfect stand-in for what West would have done anyway.
- **What the column measures:** I treated `completion_time_seconds` as the daily median, as your question implies, but the file doesn't say so.

**For the Q2 review**, I'd write: "Median checkout time in West fell roughly 40 s (about 21%) at the 3/15 launch and stayed there, while East was unchanged. This is an upper-end estimate, because a West-only price promotion launched the same day." The defensible range is about 26–43 s.

To tighten it, I'd need a promo-free comparison, such as a West sub-segment unaffected by the promotion. A staggered rollout would also work. `causal-identification-review` is the skill I'd use to design either.
