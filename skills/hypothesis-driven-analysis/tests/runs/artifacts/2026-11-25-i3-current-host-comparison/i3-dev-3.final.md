I can't give you a causal number for the new flow from this data. The comparison fails the checks it would need to pass, so any "X seconds faster" figure would be a guess that other changes also feed into.

**What the data shows (descriptive only):**
- West's median checkout time dropped from about 187 s in the last pre-rollout week to about 145 s in the first week after. It stayed near 146 s through Apr 11.
- East stayed flat at about 180 s the whole time.
- A naive West-vs-East before/after contrast gives about 42–46 s, roughly 22–25%. That is the contrast, not the effect of the flow.

**Why it can't be read as the flow's effect:**
1. **West was already getting faster.** A separate UX cleanup (shipping-step form reordering) shipped to West only, and it was lowering completion time before the rollout. West's pre-period slope was about -0.53 s/day, against about -0.02 s/day in East. Placebo contrasts inside the pre-period were already -6 to -7 s. So West and East were not on parallel paths.
2. **A West-only promotion launched the same day.** The price promotion started 2026-03-15, and average order value in West rose from about $45 to $54. Its effect on checkout time can't be separated from the flow's in this data.
3. **West was chosen because it was worst.** It had the highest cart-abandonment complaints (184 vs 97 in East). With one treated region and one comparison region, that selection can't be tested.

If you extrapolate West's pre-trend instead, the gap is about -33 s. So the contrast moves by roughly 10 s depending on the assumption, which shows how sensitive it is. I'm not offering that as the effect either.

**What I'd put in the Q2 review:** "After the West rollout, median checkout time fell from about 187 s to about 145 s (East flat), but a concurrent West-only UX cleanup and price promotion mean we can't attribute the drop to the new flow."

**What would give a real number:**
- Roll the flow out to East, or to a randomly chosen subset of West users or sessions, with a holdout group.
- Failing that, use session-level data with the promotion and cleanup exposure flagged, or more regions with staggered rollout dates.

The full review is in `identification_review.md` (one level above `data/`). Its structural validator ran clean, which checks format only, not whether the analysis is right.
