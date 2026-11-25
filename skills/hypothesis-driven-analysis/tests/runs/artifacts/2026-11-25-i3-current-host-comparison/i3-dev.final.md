I can't give you a number for how much faster the new flow made checkout, because this data doesn't isolate the flow's effect. A figure I'd put in a Q2 review as "the effect" would be one I can't defend.

**What the data shows (descriptive only, not the effect):**
- West median completion time fell from about 187 s in the last pre-rollout week to about 146–147 s in every week after 2026-03-15. That is roughly 40 s lower.
- East stayed flat at about 178–182 s the whole time.
- The West drop is real. What it can't tell you is how much of it the flow caused.

**Why the East comparison doesn't isolate the effect:**
1. **West was already getting faster before rollout.** Its pre-period trend was about −0.53 s/day, from 206 s in early February to 187 s, while East's was about −0.02 s/day. The notes attribute this to a shipping-step UX cleanup that reached West only. The two regions weren't moving in parallel, so East isn't a valid stand-in for what West would have done anyway.
2. **A West-wide price promotion launched on 2026-03-15, the same day as the rollout.** West's average order value jumped from about 45 to about 54 that week. I can't tell from this data whether the promotion changes completion time, and nothing separates it from the flow.
3. **West was chosen because it had more cart-abandonment complaints** (184 vs 97 in the prior quarter). It wasn't picked at random, so it likely differed from East in ways that affect its trajectory.

I wrote this up as an identification review with the verdict `assumption-contradicted`: `records/checkout_review.md`. The validator ran with no output, which I'm reading as a clean pass. I didn't confirm that with an exit code.

**What I'd say in the review:** "West checkout time dropped about 40 s after the rollout. A same-day West promotion and an earlier West-only UX cleanup mean we can't attribute that to the new flow from this data. A clean estimate needs a holdout."

**What would give you a real number:**
- A randomized holdout, either a share of West traffic kept on the old flow or a staggered rollout across regions or stores.
- Session-level data that separates promo-exposed from non-exposed checkouts.

If a decision depends on this, I can lay out how the call changes across the plausible range of effect sizes.
