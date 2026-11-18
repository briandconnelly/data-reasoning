# Decision memo: Assist expansion (Monday operations review)

## Recommendation
**Do not expand Assist yet, and do not book any responder-hour savings.** The data does not show Assist speeding up recovery. Within each severity tier, Assist incidents were slower and needed more responder time, and they were reopened more often.

## Why the headline is misleading
The dashboard reports that median time to close fell from 436 to 326 minutes. That drop comes from a change in the incident mix, not from faster work.

| | Manual week | Assist week |
|---|---|---|
| Incidents opened | 210 | 210 |
| Sev1 / Sev2 / Sev3 | 28 / 84 / 98 | 14 / 42 / **154** |
| Median time to close (all closed, min) | 436 | 326.5 |
| Sev1 median (min) | 1,100 | 1,659 |
| Sev2 median (min) | 512 | 740 |
| Sev3 median (min) | 167 | 302 |

- **Mix shift:** Sev3 went from 47% to 73% of incidents, and sev1 halved. The daily mix is identical every day within each week and steps at the cutover (14/12/4 per day before, 22/6/2 after).
- **Composition effect:** Re-weighting the manual week's per-severity averages to the Assist-week mix gives a mean of 300 minutes, down from 427. That is the whole dashboard improvement, with no change in how fast any incident type closes.
- **Within-tier results:** Holding severity fixed, Assist is slower on time to close by about 182 minutes per incident on average. The bootstrap 95% interval is 173–192.
- **Responder minutes by tier:** Assist took more in every tier. The differences are sev1 +72, sev2 +38 and sev3 +26 minutes per incident, and each interval excludes zero.
- **The responders' complaint holds:** The penalty is largest on the hardest incidents (sev1 +72 min, sev3 +26 min). That matches what they reported.

## Responder-hours we can credibly attribute
**Zero saved. If anything, the data points toward extra effort.**

- **Severity-adjusted:** Assist cost about +32 responder-minutes per incident. Across the 200 closed Assist incidents, that is about **+100 responder-hours** versus the manual workflow, with a bootstrap interval of roughly +96 to +106 hours.
- **Without adjusting for severity at all:** Mean responder minutes per closed incident are flat (90.2 manual vs 90.9 Assist). Total closed-incident hours were 314 manual and 303 Assist, so the lighter mix produced only a small apparent saving.
- **Unclosed incidents hide extra cost:** Ten Assist incidents are still unclosed after 8.5–15 days, and 5 of them are sev1. One manual incident is also unclosed. Their minutes are missing, so costing the Assist ones at tier averages adds roughly 34 hours, which more than erases the unadjusted 11-hour apparent saving. Dropping them flatters Assist on every measure.
- **Finance's figure:** Any savings number built from the median drop is an artifact of the mix and should come out of the rollout plan.

## Other fields: consistent, and concerning
- **Reopens within 72 hours:** 9 of 200 Assist incidents were reopened, against 0 of 209 manual. All 9 were sev1, and one-sided Fisher p≈0.001. The rate was zero in every manual tier.
- **Sev1 handoffs:** Average handoffs fell from 5.9 to 0.4 on sev1, while sev2 and sev3 rose. This could be a recording change or real loss of escalation, and it needs checking either way.
- **Staffing and interruptions:** The cutover coincided with two more active responders per group. Scheduled hours rose from about 96 to 114 per day for identity and from 87 to 104 for storage. Interruption minutes also rose, from 12 to 74 per day for identity and from 29 to 59 for storage.

## What the data can and cannot establish
**It can establish:**
- The dashboard median drop is a composition effect.
- Assist-week incidents were slower and more costly within each severity tier.
- Savings cannot be booked.

**It cannot establish:**
- **That Assist caused the slowdown.** There is no holdout, and the "clean" before/after claim only guarantees each incident ran under one workflow. Everything else changed at the same moment, including staffing, interruptions and the severity mix, so one week is confounded with the cutover. The slowdown is a strong warning signal, not a proven effect.
- **Why the severity mix changed.** If Assist or its intake changes how incidents are labelled, the tier comparison is biased: harder incidents downgraded into sev3 would make sev3 look slower. The unadjusted comparison, which shows no savings, does not depend on this, so the recommendation holds either way.
- **Anything about the rest of the company.** Only two service groups and one week of Assist data are covered, and staffing and incident volume were constant at 15 per day.

## Suggested next steps
1. Remove the savings line from the rollout plan.
2. Find out whether severity assignment changed at cutover, and why.
3. Audit the 10 stuck incidents and the 9 sev1 reopens, and check how sev1 handoffs are recorded.
4. If the pilot continues, run a staggered or randomized rollout, for example Assist on alternating incidents or on one group at a time. Pre-register time to close and responder minutes within each severity tier, with unclosed incidents counted as censored.
5. Treat the extra responders and interruptions as a separate question.

The analysis scripts are in `/tmp` (`lib.py`, `b.py`, `c.py`, `d.py`) and use only the three local exports. Intervals are from a 2,000-draw bootstrap with seed 1.
