I can't give you a number for how much faster the new flow made checkout. This data doesn't isolate the flow's effect, so any figure I gave you for the Q2 review would be a guess.

**What the data shows**

| | Before 3/15 | After 3/15 |
|---|---|---|
| West median checkout time | 196.6 s | 146.6 s |
| East median checkout time | 180.0 s | 179.9 s |

West is about 50 s faster after rollout and East didn't move. Read that as a description of what happened, not as the flow's effect.

**Why it isn't the flow's effect**

- **West was already getting faster.** A separate shipping-step cleanup went out to West only, before rollout. West's weekly median fell from 206 s to 187 s over the six weeks before 3/15. East stayed flat at about 180 s. The pre-rollout slope was −0.53 s/day in West and −0.02 s/day in East. So East isn't a valid stand-in for what West would have done without the flow.
- **A West price promotion started on 3/15.** It launched the same day as the rollout and East had none. I can't separate its effect from the flow's with this data.
- **West was picked for having the most abandonment complaints** (184 vs 97 in East). That choice could be tied to where West was headed anyway, and nothing here lets me test it.

A before/after comparison in West alone fails for the same two reasons. The pre-trend and the promotion both break it.

I wrote this up in `identification_review.md` and ran the structural validator, which returned no findings. The validator only checks the record's structure, not whether the analysis is right.

**What you can say in the Q2 review**

- West checkout time dropped about 50 s at the 3/15 rollout, with East flat.
- Only part of that can be credited to the flow, because other West-only changes overlapped it. The data can't say how much.

You can also point out that West fell from 187 s to about 147 s between the last pre-week and the first post-week (week of 3/8 to week of 3/15). That 40 s step lines up with the rollout date. Even so, the promotion landed the same day, so it still isn't clean evidence of the flow's effect.

**What would give you a real number**

- Roll the flow out to East, or to a randomly chosen part of each region, and compare.
- Or find a region that got neither the cleanup nor a promotion, with enough pre-rollout history to test its trend against West's.

If you want, I can sketch either design.
