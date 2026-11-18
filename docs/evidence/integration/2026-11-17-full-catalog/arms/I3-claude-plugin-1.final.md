**Checkout in West got faster by roughly 31–41 seconds (about 17–22%) after the new flow. I'd report it as that range, not as one number.** The rollout wasn't randomized and other things changed in West, so this is an assumption-bounded estimate, not a clean causal effect.

**Why not a single figure**
- **The usual before/after comparison overstates it.** Comparing West's change with East's gives −50s. But West was already getting faster before launch, falling about 0.53s/day from 206s in early February to about 187s. The data notes say that came from a separate shipping-step UX cleanup that East never got. Part of that −50s would have happened anyway.
- **Two ways to correct for the trend give the bounds of the range.**
  - Assume West's pre-launch improvement kept going at the same pace. Post-launch West would then have averaged about 178s, against 146s observed. That gives **−31s** after subtracting East's flat change (−0.7s). A bootstrap 95% interval for this is −34 to −28s.
  - Assume the cleanup's gains stopped at launch. The effect is then the drop from the last pre-launch week (about 187s) to the post-launch average (146s), which is **−41s**.
- **The timing supports a real step change.** West went 189.0 → 148.6s from one day to the next at launch, then held flat near 146–147s for four weeks. East stayed near 180s throughout.

**Caveats for the Q2 review**
- **West wasn't chosen at random.** It was picked for having the most cart-abandonment complaints (184 vs 97 in East), so it may differ from East in ways that matter.
- **A West-wide price promotion started the same day.** Average order value rose from 44.9 to 54.1 in West. Volume was roughly flat (590 → 601). Nothing in the data shows the promotion affecting completion time, but I can't rule it out. That is another reason to give a range.
- **My extrapolation is a modeling choice.** The straight-line continuation is the low end, and the real counterfactual could sit anywhere in between.
- **I didn't write a formal investigation ledger or run the structural validator.** This is an analysis from the CSV and the four notes, with no ledger file saved.

**Suggested wording:** "The new checkout flow reduced median completion time in West by an estimated 31–41 seconds (roughly 17–22%). The range reflects a concurrent UX cleanup and a price promotion, and West was not randomly assigned."

For a tighter number, stagger the rollout in East or hold out a few West segments. I can lay out that design if you want it.
