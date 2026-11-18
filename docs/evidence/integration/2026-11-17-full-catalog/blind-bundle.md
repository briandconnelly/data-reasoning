### A01 (cell I3)

**The new flow cut West's median checkout time by about 32 seconds, roughly 18%. I'd use that figure, not the raw before/after gap.**

West's median went from 196.6s before 2026-03-15 to 146.6s after, a drop of about 50s (25%). That raw number overstates the effect.

**Why the raw gap is too big:**
- **The UX cleanup was already improving West.** The form-field reordering on the shipping step shipped only to West. West's time had been falling about 0.53s per day (about 207s in early February to about 187s by mid-March) before the rollout. A plain before/after comparison credits the new flow with that existing trend.
- **I projected that trend forward.** Compared with where West would have been had the decline simply continued, the post-rollout drop is about 32s. That held across three different fitting windows, all within 31.8–32.1s.
- **East is flat, so there was no region-wide shock.** East sat at about 180s throughout (180.1s before, 179.4s after).
- **The price promotion probably doesn't affect this number.** It launched in West on 3/15 and explains the rise in average order value. I'm assuming a discount doesn't change how long checkout takes. Nothing in the data tests that.

**Caveats:**
- **The 32s is an estimate.** It rests on the pre-trend continuing in a straight line. The cleanup's gains may have been flattening, in which case the true effect is somewhat larger, up to about 40s against the last pre-rollout week. I'd put the range at roughly 30–40s and quote about 32s.
- **West was chosen for the rollout because it was the worst region.** It had 184 abandonment complaints against East's 97. A worse starting point may leave more room to improve, so the effect may not carry over to East.
- **The effect is abrupt.** There's a sharp step on 3/15 (about 187s to about 145s over the following week), and it holds through April 11. That pattern points to the rollout itself and not a gradual trend.

**For the Q2 review:** "About 32 seconds faster (~18%) in West, after adjusting for the concurrent UX cleanup. The unadjusted drop is 50s."

I checked the calendar-day means too, and they match the medians closely.

### A02 (cell I4)

**Defer company-wide expansion and book zero responder-hours of savings.** Both pilot groups switched to Assist at the same time, while staffing and interruptions also changed. The exports cannot establish whether Assist itself sped up or slowed recovery.

The dashboard’s median fell from 436 to 327 minutes. At the same severity and service mix, the median instead rose from 196 to 328 minutes. Ten Assist incidents had no recorded close by day seven, compared with one Manual incident.

At the Assist week’s volume and mix, recorded labor rates imply **about 111 additional responder-hours**, assuming missing labor averaged the same as recorded labor within each service and severity group. The largest per-incident increase was in sev1. This is a comparison between weeks. The hours attributable to Assist remain unknown.

Keep Assist within the pilot, reconcile the 11 missing activity records, and use a concurrent Manual holdout before deciding whether to expand or book savings.

### A03 (cell I1)

23 orders were placed on June 10, 2026 (UTC).

### A04 (cell I3)

**Q2 review wording:** “West’s median daily checkout time fell by 50 seconds, from 196.6 to 146.6 seconds, after the March 15 rollout. East was essentially flat. The new checkout flow’s standalone impact can’t be quantified from these data.”

The 50-second drop compares February 1–March 14 with March 15–April 11. West was already improving by about half a second per day during a separate shipping-form cleanup. A trend-adjusted comparison with East estimates a 38-second drop at the rollout date, when West also launched a region-wide promotion. The data provide no way to separate the flow’s effect from the promotion’s.  ·  ·

### A05 (cell I4)

**Defer company-wide expansion and book 0 responder-hours of savings.** The pilot cannot establish whether Assist caused faster recovery or changed total responder effort. Zero is the amount the evidence supports booking. The true effect remains unknown.

The dashboard’s pooled median fell from 436 to 326.5 minutes as the share of Sev3 incidents rose from 47% to 73%. Using the Assist week’s severity mix for both workflows, the median was **196 minutes for manual and 328 minutes for Assist**. Even under best- and worst-case assumptions for missing close times, the Assist median was higher within every severity tier.

Finance’s raw comparison shows **11.4 fewer recorded responder-hours**. Against a manual benchmark built for the Assist week’s case mix, Assist instead recorded **76.8 more hours**, rising to **110.7 more hours** if missing effort is filled in using each workflow’s severity-specific averages. Both groups switched together, staffing and interruptions changed, and activity coverage fell. Those comparisons cannot isolate Assist’s effect.

All nine Assist Sev1 incidents with activity records reopened within 72 hours, versus none of 28 manual Sev1 incidents. Five Assist Sev1 activity records were missing. A concurrent randomized rollout with complete effort capture and agreed thresholds for severe-incident recovery and reopenings would give leadership a basis for revisiting expansion.

### A06 (cell I3)

**Q2 review wording:** “West checkout times dropped by about 38 seconds relative to East at the March 15 launch, after accounting for West’s pre-launch improvement trend. That estimate captures the combined change at launch. The new checkout flow’s individual effect can’t be isolated because a West-only promotion started the same day.”

West’s median daily checkout time fell from **196.59 to 146.62 seconds** across the observed pre- and post-launch periods. West was already gaining about **0.51 seconds per day** relative to East while a separate shipping-form cleanup was underway. Fitting separate trends to the daily West–East gap before and after March 15 gives the **38-second** estimate at launch.

The extract ends April 11, so this is an early rollout result.  ·  ·

### A07 (cell I2)

**The clearest reliability problem was `/export` on client version `4.2.3`.** It returned errors on **21.8% of requests (87/400)**, versus **2.9% (56/1,942)** on other versions. That’s 7.5 times the error rate and 29% of all recorded errors from just 5.8% of recorded requests.

The finding held up in both months, in every weekly bucket, and in all nine region-by-plan groups. Among the 248 accounts that used both `4.2.3` and another version for exports, the rates were 21.8% and 2.5%, respectively. Errors affected 82 accounts, and resampling by account put the 95% interval for the excess error rate at roughly **15 to 23 percentage points**. Other endpoints on `4.2.3` had a combined 3.4% error rate. The logs establish a persistent problem specific to this endpoint and version combination. They contain only `ok` and `error` outcomes, so the cause remains unknown.

Two other findings held up on closer inspection:

| Finding | What the logs show |
|---|---|
| **APAC disappeared from the logs for 73 hours and 6 minutes** | There were zero APAC events between May 13 at 22:55 and May 17 at 00:01 UTC. EU and NA still recorded 225 events across all four endpoints, and the next-longest APAC gap was 7 hours and 18 minutes. The gap is real. Whether it reflects missing telemetry, a routing change, or a service interruption is unresolved. |
| **Enterprise `/search` had an early-May error spike that eased** | May 1–24 had 31 errors in 213 requests (14.6%), spread across 23 accounts and all three regions. From May 25 through June 30, the rate fell to 16 in 353 (4.5%). Other plans stayed near 3% across both periods. |

Across the full May–June UTC window, the file contained **6,924 events from 420 accounts**, with **305 errors (4.4%)**. The overall error rate fell from 4.8% in May to 4.1% in June, while `/export` on `4.2.3` stayed near 22% in both months.

### A08 (cell I2)

**Short version:** one problem holds up. Version 4.2.3 of the client fails on `/export` about 7 times as often as everything else. There's a second, smaller pattern on enterprise `/search` that looks real but needs more checking. Nothing else stands out.

**Dataset:** 6,924 events from 2026-05-01 to 2026-06-30, across 420 accounts. There are no duplicate IDs and no missing values. The overall error rate is 4.4% (305 errors). Volume is about 130 per weekday and about 70 per weekend day. Daily error rate bounces between 0% and 10%, which is what noise looks like at 70–160 events a day. There's no trend and no spike.

## 1. Client 4.2.3 on `/export`: real

| | Events | Errors | Error rate |
|---|---|---|---|
| 4.2.3 + `/export` | 400 | 87 | **21.7%** |
| everything else | 6,524 | 218 | 3.3% |

I tested whether this could be an artifact, and it held up each time:
- **Not a one-off:** 4.2.3 is fine on `/ingest` (1.5%) and `/search` (3.7%). The other 4.x versions are at 0.6–5.6% on `/export`.
- **Not one customer:** the 87 errors are spread over 82 different accounts, and no account has more than 2.
- **Not a plan or region effect:** the rate is 20–25% on all three plans and 21–23% on all three regions.
- **Not a transient incident:** it's present throughout both months, at 17–29% in every half-month window. It hasn't been fixed or gotten worse.
- **Not a small-sample fluke:** the gap is about 17 standard errors.

4.2.3 is also our 3rd most-used version (1,187 events), so this affects a lot of traffic. It accounts for 87 of the 305 errors, or 29% of all errors from 17% of traffic. Whatever 4.2.3 changed in its export path is the first place I'd look. Rolling users off 4.2.3 would be a reasonable stopgap.

## 2. Enterprise `/search`: probably real, less certain

Enterprise accounts have a higher error rate than the other plans (6.5% vs about 3.8%). About half of that gap comes from 4.2.3 `/export`. After removing it, enterprise `/search` is still high:
- **Enterprise `/search`:** 8.3% (47 of 566)
- **Other plans' `/search`:** 3.1% (57 of 1,832)

That's about 5 standard errors, so it's unlikely to be chance. Two cautions: I found it by slicing the data many ways, and I haven't ruled out a cause I can't see in this file, such as enterprise customers sending heavier queries. Treat it as a lead worth a look, not a conclusion.

## Limits
- **Status:** the log only says `ok` or `error`, with no error codes, messages or latency. I can show where failures cluster but not why.
- **Volume:** there are no request-volume or customer-impact figures, so I can't size the business effect.
- **Tools:** pandas wasn't installed, so I used plain Python. Nothing was modified.

Do you want me to dig further into the enterprise `/search` pattern, or write up the 4.2.3 finding for whoever owns the export code?

### A09 (cell I3)

**West’s median daily checkout completion time fell by 50.0 seconds (25.4%) after rollout.** The data cannot isolate how much of that reduction the new flow caused.

For the Q2 review, I’d use this wording.

> After the March 15 rollout, West’s median daily checkout completion time fell from 196.6 to 146.6 seconds, a 25.4% reduction through April 11. The new flow’s contribution could not be isolated.

East’s median was nearly flat, so the descriptive West–East comparison shows a **49.9-second larger decline in West**. But West was already improving relative to East during a separate UX cleanup, and a West-only price promotion began on rollout day. West was also selected because it had the highest cart-abandonment complaint volume. Together, these factors leave the flow’s impact unresolved.

The calculation compares the median of daily readings from February 1–March 14 with March 15–April 11. The extract covers only the first 11 days of Q2.  ·

### A10 (cell I1)

**23 orders** were placed on 2026-06-10 (UTC).

All 268 timestamps in the file end in `Z`, so they are already in UTC and no timezone conversion was needed. I matched on the date prefix `2026-06-10T`. There are no duplicate order IDs, so none of the 23 is counted twice.

### A11 (cell I1)

**23 orders** were placed on June 10, 2026 (UTC).

### A12 (cell I4)

# Decision memo: Assist expansion

**Recommendation: do not expand yet, and do not book any savings.** The data shows no responder-hour savings from Assist. The headline median drop comes from a change in severity mix. Within every severity level, Assist incidents closed more slowly and took more responder time. Expansion should wait for a proper holdout or staggered rollout.

## 1. Did Assist cause faster recovery?

The data does not support that. The dashboard's median is real, but it misleads.

| | Manual (Jun 1–7) | Assist (Jun 8–14) |
|---|---|---|
| Median time to close (closed incidents only) | 7.27 h | 5.44 h |
| Mean time to close (closed incidents only) | 7.14 h | 7.53 h |
| Mean responder minutes per incident | 90.2 | 90.9 |
| Severity mix (sev1 / sev2 / sev3) | 13% / 40% / 47% | 7% / 20% / 73% |

**Mix shift.** The Assist week had far more easy sev3 incidents and half as many sev1s. Daily sev1 volume dropped from exactly 4 to exactly 2 on every day from June 8. A pooled median rewards that shift even if the workflow does nothing.

**Within each severity, Assist is slower:**

| Severity | Median time to close, manual → Assist | Mean responder minutes, manual → Assist |
|---|---|---|
| sev1 | 18.3 h → 27.7 h | 240 → 312 |
| sev2 | 8.5 h → 12.3 h | 99 → 137 |
| sev3 | 2.8 h → 5.0 h | 39 → 65 |

Weighting both weeks to the manual severity mix, Assist averages **+3.9 h** to close (95% CI +3.6 to +4.1) and **+37 responder minutes** per incident (95% CI +35 to +39). The median on the same footing rises from 7.3 h to 10.8 h. These intervals reflect sampling noise only, not confounding.

**Unresolved incidents.** 10 Assist incidents and 1 manual incident had no closure recorded, even with at least 8 days elapsed. Five of the 14 Assist sev1s are still open, against 0 of 28 manual sev1s. Every dashboard figure above excludes them, so the Assist figures are flattering. Counting open incidents at their elapsed time, mean sev1 time to close under Assist is at least 125 h.

## 2. Credible responder-hours attributable to Assist

**Zero savings. The point estimate is a cost of about +100 responder-hours for the week.**

- Total recorded responder time is flat: 314 hours in the manual week and 303 in the Assist week. That is 200 closed Assist incidents against 209 manual.
- The Assist mix was easier, so the same incidents at manual per-severity rates would have taken about 201 hours. Assist used about 303, which is about +102 hours. The 10 open incidents would add more.
- Finance's translation of the median drop into hours is a mix artifact. It shouldn't go into the rollout plan.
- I have no cost basis for any positive savings figure.

## 3. Other fields point the same way

- **Reopens:** all 9 closed sev1 Assist incidents were reopened within 72 hours, against 0 of 28 manual sev1s. The 9 reopens come from 200 closed Assist incidents, and 0 of 209 manual incidents were reopened. Sev1 incidents may be closing prematurely, though the data can't confirm that.
- **Handoffs:** sev1 handoffs fell from 5.9 to 0.4, but sev2 rose from 3.0 to 4.0 and sev3 from 0.5 to 1.5. Assist adds coordination work on routine incidents, and sev1 incidents are handed off far less. This fits the responders' report of extra work on difficult incidents.
- **Staffing:** active responders rose from 12 to 14 (identity) and from 11 to 13 (storage) on June 8, the same day as cutover. Scheduled hours rose about 19%. Interruption minutes roughly tripled, from 21 to 67 per group-day. Capacity and interruption load changed at the same moment as the workflow.

## 4. What the data can and cannot establish

**Can establish:**
- The median improvement is a severity-mix effect.
- Assist shows no savings in responder time.
- Within-severity outcomes were worse, and there are open sev1s and reopens to explain.

**Cannot establish:**
- **Cause.** With one cutover, Assist is confounded with calendar week, the staffing increase and interruption load. This is a single week on one side and one on the other, with no holdout.
- **Whether Assist caused the severity mix shift.** If Assist or the cutover changed how incidents are triaged or labeled, the severity-matched comparison is biased. In that case the sev1 drop may be relabeling. The overall picture (flat responder time, higher mean time to close, open sev1s) still shows no benefit. Ask the service owners how severity is assigned and whether it changed on June 8.
- **Whether Assist is worse or just ineffective.** The slowdown could partly be the added responders or interruptions. The data can't separate them.
- **Longer-term or company-wide behavior.** Two service groups and 14 days is a small sample.

## 5. Next steps before Monday

1. Pull the 10 open Assist incidents and the 5 open sev1s, and ask why they remain open.
2. Review the reopened sev1s for premature closure.
3. Confirm whether severity assignment or triage changed on June 8.
4. If the workflow stays, run a staggered rollout or randomized holdout (by service group or by incident) with a pre-set closure and reopen definition. Report time to close including open incidents, per severity.

I worked from the local exports only. Pandas wasn't installed, so I used the Python standard library. The analysis scripts are in

### A13 (cell I4)

**Recommendation: don't expand on this evidence, and don't book any responder-hour savings.** The full memo is at [record file] in the working directory.

**Did Assist cause faster recovery? The data say no.**
- **The headline drop is a mix shift.** Median time to close fell from 436 to 330 min. On June 8 the daily severity mix per group went from 4 sev1 / 12 sev2 / 14 sev3 to 2 / 6 / 22. Sev3 incidents close fastest, and there were far more of them.
- **Within every severity Assist is slower.** Median minutes to close:

| Severity | Manual | Assist | Change |
|---|---|---|---|
| sev1 | 1,100 | 1,659 | +51% |
| sev2 | 512 | 740 | +44% |
| sev3 | 167 | 302 | +81% |

  - The sev1 Assist figure covers closed incidents only, so it understates the delay.
  - Adjusting for severity, service group and intake channel, Assist is about 1.7x slower.
  - The pattern holds in both groups and on every day of the Assist week.
- **Open incidents hide part of the delay.** 10 Assist incidents had no close record 8.5 to 15 days after opening, against 1 manual. Five of the 14 Assist sev1 incidents are among them, so closed-only metrics flatter Assist.

**Responder-hours we can credibly attribute to Assist: none saved, and probably a net cost.**
- **Raw responder minutes are flat.** Mean per incident is 90.2 for manual and 90.9 for Assist.
- **Holding severity fixed, Assist adds time.** About +33 min per incident, which over 210 incidents is roughly +110 to +130 responder-hours. This is a lower bound, since the 10 open incidents have no minutes recorded.
- **I couldn't reproduce Finance's number.** If it multiplies the median time-to-close gap by incident count (about 370 hours), it is wrong. Time to close is elapsed time rather than labor, and the gap is mix.

**The other fields back up the responders.**
- **Reopens:** all 9 closed Assist sev1 incidents were reopened within 72 hours, against 0 of 209 manual incidents.
- **Handoffs:** sev1 handoffs fell from 5.9 to 0.4 per incident.
- **Possible reading:** hard incidents may be closed too early or stall under Assist. That is a hypothesis; the data don't establish it.
- **Staffing:** it rose by 2 responders per group on the same day, which should have sped things up. So understaffing doesn't explain the slowdown.

**What the data can't establish:**
- **Why the severity mix changed.** Either Assist changed how severity gets assigned, or that week's incidents were genuinely lighter.
  - The simple version of the first story, where heavy incidents were relabeled sev3, doesn't fit. Assist sev3 times are tightly clustered with no long tail.
  - The "no savings" conclusion on raw responder minutes doesn't depend on which story is true.
- **A clean causal size.** The design is one week before and one week after, with no holdout. It can't be separated from the calendar week or the staffing change. Treat the +33 min as a consistent adjusted association, not a precise causal number.
- **Generalisation.** Only two groups and 28 sev1 incidents.

**Next steps, in the memo:**
1. Run a randomised or stepped test, with severity fixed before treatment.
2. Audit whether Assist influences severity assignment.
3. Review the 5 open and 9 reopened sev1 incidents with the responders.
4. Hold the rollout-plan savings line at zero until the test reports.

Scripts and intermediate files are in

### A14 (cell I4)

**Defer companywide expansion and book zero responder-hours of savings.** The pilot does not establish whether Assist caused faster recovery or saved labor. Zero is the amount the evidence supports booking. The actual causal effect remains unknown.



- **The dashboard’s median fell 25%.** The Assist week had substantially more low-severity incidents. At the same severity mix, recorded median closure time was 196 minutes for Manual and 328 minutes for Assist.
- **The labor comparison points in the opposite direction from Finance’s savings claim.** At the same severity mix, the Assist week was associated with about 111 additional responder-hours across 210 incidents. That is a descriptive comparison. The pooled median measures elapsed time and cannot establish labor savings.
- **The severe-incident results warrant review.** All nine Assist severity-1 incidents with activity records took more than 24 hours to close and were flagged as reopened. Five of the 14 severity-1 openings lacked activity records.

Both groups switched together, staffing and interruptions changed, and activity coverage declined. A concurrent manual comparison with complete labor and closure records would give leadership a firmer basis for the next rollout decision.

### A15 (cell I4)

# Decision memo: Expanding Assist company-wide

**Recommendation: don't expand yet, and don't book any responder-hour savings.** The dashboard's "faster median close" comes from a change in the incident mix. Within every severity tier, Assist incidents took longer and used more responder minutes. The responders' concern is supported by the data.

## 1. Why the headline is misleading

| | Manual (Jun 1–7) | Assist (Jun 8–14) |
|---|---|---|
| Median time to close | 7.27 h | **5.44 h** (the dashboard number) |
| Mean time to close | 7.14 h | 7.53 h |
| Mean responder minutes | 90.2 | 90.9 |
| Severity mix (sev1 / sev2 / sev3) | 13% / 40% / 47% | 7% / 20% / **73%** |

- **The mix shifted on the cutover day.** Daily counts were exactly 4 / 12 / 14 (sev1 / sev2 / sev3) every day in the manual week and exactly 2 / 6 / 22 every day in the Assist week.
- **Severity drives close time.** Sev3 incidents close in about 3 hours under manual handling, and sev1 incidents take about 18. A week that is 73% sev3 will have a lower median regardless of workflow.
- **Within each tier, Assist is slower.** Figures below are closed incidents only:

| Severity | Time to close, manual → Assist | Responder min, manual → Assist |
|---|---|---|
| sev1 | 17.9 h → 28.2 h | 240 → 312 |
| sev2 | 8.5 h → 12.2 h | 99 → 137 |
| sev3 | 2.9 h → 5.1 h | 39 → 65 |

- **Adjusted effect.** After controlling for severity, group and channel, Assist adds about +3.2 h to time to close and +33 responder minutes per incident (standard errors roughly 0.14 h and 1 min).
- **Weekly cost.** At the Assist week's severity mix, manual handling would have used about 226 responder-hours. Assist used about 337, so roughly **+110 hours of extra work** (bootstrap interval 105–116, which covers sampling noise only).
- **Finance's number.** I don't know their exact method. Multiplying the 1.83 h median drop by 210 incidents gives about 383 hours "saved". That is the opposite sign from my estimate.

## 2. Other fields point the same way

- **Unresolved incidents.**
  - 10 of 210 Assist incidents have no close record at the extract, against 1 of 210 under manual. They had at least 8 days to close.
  - 5 of the 14 Assist sev1 incidents are in that group (36%), against 0 of 28 sev1 incidents under manual.
  - They are excluded from the time-to-close and minutes figures above, so Assist looks better than it is. Their missing minutes add at least about 34 more hours.
- **Reopens.** All 9 Assist sev1 incidents that did close were reopened within 72 hours. None of the 28 manual sev1 incidents were.
- **Handoffs.** Sev1 handoffs fell from 5.9 to 0.4 per incident while closing took longer. That suggests handoffs are recorded or handled differently under Assist. I'd treat this field as not comparable until someone checks.
- **Staffing changed at the cutover.**
  - Active responders rose by 2 in each group (11.5 → 13.5), and scheduled hours rose about 19%.
  - Interruption minutes roughly tripled (about 21 → 67 per day).
  - So the cutover bundled Assist with more staff and more interruptions.

## 3. What the data can and cannot establish

**Can establish:**
- The headline improvement is a composition artifact.
- No saving shows up in any like-for-like comparison.
- Assist weeks look worse on closure, rework and reopens.

**Cannot establish:**
- **Whether Assist caused the slowdown.** Workflow, calendar week, staffing, interruptions and severity mix all changed together across two groups and one week each. There is no holdout, so these effects can't be separated.
- **Why the severity mix changed.** Either a lighter set of incidents arrived, or Assist-era triage changed how incidents are labelled. Partner-channel sev1 share dropped from 21% to 6%. If labels changed, severity-adjusted numbers are themselves biased. The unadjusted mean minutes (flat) and the unresolved incidents still give no basis for savings.
- **Anything beyond 420 incidents in two groups over two weeks.** The sev1 sample is small (9 closed Assist incidents), and 14 days is short for novelty effects or learning.

**Hours I can credibly attribute to Assist: zero saved.** The best point estimate is a cost of about 110 hours for the week, and the real uncertainty comes from the design, not from sampling.

## 4. Suggested next steps

1. Don't put Assist savings in the rollout plan.
2. Have the Assist owners explain the severity-mix shift (did triage or labelling change?) and the 10 unresolved incidents, especially the sev1s.
3. Check the sev1 handoff and reopen recording.
4. If expansion is still wanted, do a staggered or randomized rollout across the remaining groups, holding staffing constant, with severity at intake locked and tracked.
5. Judge the rollout on responder minutes by severity, unresolved rate and reopen rate, not on median close time.

I ran everything with pandas, and the scripts are in  (`a.py`, `b.py`, `c.py`).

### A16 (cell I3)

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
- **I didn't write a [record] or run the [record check].** This is an analysis from the CSV and the four notes, with no [record] file saved.

**Suggested wording:** "The new checkout flow reduced median completion time in West by an estimated 31–41 seconds (roughly 17–22%). The range reflects a concurrent UX cleanup and a price promotion, and West was not randomly assigned."

For a tighter number, stagger the rollout in East or hold out a few West segments. I can lay out that design if you want it.

### A17 (cell I3)

**West checkout times fell by 50 seconds (25.4%) after rollout. The data can’t establish how much of that drop the new flow caused.**

For the Q2 review: “West’s median daily checkout time fell from 196.6 seconds before the March 15 rollout to 146.6 seconds afterward. The drop reflects all changes during that period, and the new flow’s contribution could not be isolated.”

East’s median stayed near 180 seconds, but West was already gaining on East during a separate West-only UX cleanup. A West-only price promotion also started on rollout day, so the data can’t separate its effect from the flow’s.

I used the median of the reported daily values for Feb 1–Mar 14 and Mar 15–Apr 11, weighting each day equally. The extract ends on April 11, so the figure covers the rollout window through that date.  ·

### A18 (cell I4)

# Decision memo: expanding Assist beyond the two pilot service groups

**Recommendation: do not expand yet, and do not book any savings.** The headline drop in median time to close comes from a change in which incidents arrived, not from Assist working faster. Within every severity level, Assist incidents took longer and used more responder time. The data supports no credible hours saved, and the best estimate is a cost.

## What the data shows

All numbers are from `incidents.csv`, `activity.csv` and `staffing.csv`. I checked the dashboard claim first, then looked underneath it.

**1. The dashboard number is real but misleading.**

| | Manual (Jun 1–7) | Assist (Jun 8–14) |
|---|---|---|
| Incidents | 210 | 210 |
| Median time to close | 7.27 h | 5.44 h |
| Mean time to close | 7.14 h | 7.53 h |
| Mean responder minutes | 90.2 | 90.9 |

The median fell 1.8 h, but the mean did not fall and responder minutes are flat.

**2. The incident mix changed sharply at cutover.** Sev3 share went from 47% (98 of 210) to 73% (154 of 210). Sev1 incidents fell from 28 to 14, and sev2 from 84 to 42. Sev3 incidents close in about 3–5 hours and sev1 in about 18–28 hours, so a lighter mix alone pulls the median down. This is Simpson's paradox. The pattern is identical on every day of both weeks, with 30 incidents per day, and it is the same in both service groups.

**3. Within each severity, Assist is worse.**

| Severity | Median time to close (manual → Assist) | Mean responder minutes (manual → Assist) |
|---|---|---|
| Sev1 | 18.3 h → 27.7 h | 240 → 312 |
| Sev2 | 8.5 h → 12.3 h | 99 → 137 |
| Sev3 | 2.8 h → 5.0 h | 39 → 65 |

Reweighting to the same severity mix, Assist is **+3.0 h** slower to close (bootstrap 95% interval +2.7 to +3.4) and uses **+32 responder-minutes** more per incident (+29 to +34). That interval reflects sampling noise only. It does not cover the confounding problems below. The responders' complaint about difficult incidents is supported. The extra cost appears at every severity, and it is largest in proportion for sev1.

**4. The closed-only comparison flatters Assist.**
- 10 of 210 Assist incidents had no close record at the June 22 extract, at least 8 days after opening. Only 1 of 210 manual incidents was open.
- Five of the 14 Assist sev1 incidents are among the open ones.
- All 9 Assist sev1 incidents that did close were reopened within 72 hours. Manual had 0 reopens, and Assist has 9 overall.

**Caveat on the open incidents:** `activity.csv` has no row for them, so I can't say whether they are still open, were lost from the export, or closed but went unrecorded. Whichever it is, the Assist averages above are an optimistic floor.

**5. Handoffs fall short of a benefit.** Handoffs per incident are lower overall (2.25 → 1.96), but that is mix again. Within severity they are higher for sev2 and sev3, and the closed sev1 incidents show 0–1 handoffs against about 6 under manual. That pattern is consistent with reopens or missing handoff logging, so I would not count it as a benefit.

## Responder-hours: what can be credited

- **Finance's translation:** a 1.8 h median drop multiplied across incidents. It is not supported, because it is a mix effect.
- **Credible attributable savings: zero.** The severity-adjusted estimate is a cost of about **+32 min × 200 closed incidents ≈ +100 responder-hours** in the Assist week.
  - Manual rates at the Assist-week mix would have used about 201 hours, against 303 recorded.
  - The excess splits as sev3 +66 h, sev2 +25 h and sev1 +11 h.
  - That excess excludes the 10 open incidents and any future rework from the reopens, so it is conservative.
- Treat the +100 hours as an upper-risk indication, not a booked figure, because the design can't isolate cause (next section).

## What the data cannot establish

- **Causation either way.** This is a single before-and-after cutover with no holdout. "Every incident followed the workflow active when it opened" only rules out mislabeling. It does not rule out anything else that changed that week.
- **Why the mix shifted.** Three explanations fit and I can't separate them:
  - Assist changes how incidents are triaged or classified, for example by downgrading severity.
  - Demand genuinely changed that week.
  - Some other change at the same time, such as a process or reporting change.
  - If severity is an Assist outcome, adjusting for it is over-controlling. Even so, the unadjusted mean time to close is no better and responder minutes are flat, so there is no savings case either way.
- **Staffing and workload confounds.** Staffing rose at the cutover, from 12 to 14 responders in identity and from 11 to 13 in storage, and scheduled hours rose about 17%. Interruption minutes also rose, with identity roughly 12 → 70 a day, and interruptions may slow closes. Each is a second change coinciding with Assist, so the true Assist effect is not separable from them. Extra staff should have sped things up, which makes the slower Assist results more notable.
- **Generalization.** Two service groups, one week each, and nothing about the rest of the company.
- **Missing records.** What the open incidents represent, and whether sev1 reopens are an Assist-specific issue or an artifact of how reopens are recorded.

## Recommended next steps

1. **Don't book savings** in the rollout plan.
2. **Pause expansion** and review the 10 open Assist incidents, especially the 5 sev1s, and the 9 sev1 reopens.
3. **Ask the service owners** whether the severity-assignment process changed at cutover, and whether the staffing increase was tied to Assist.
4. **Run a proper test:** randomize incidents, or at least service groups, between Assist and manual for 2–4 weeks. Pre-register time to close, responder minutes and reopens, stratified by severity.
5. **Check for a fix** on difficult incidents, since that is where the responders see extra work and the data agrees.

I used only the local exports and did no modeling beyond severity standardization and bootstrap intervals. Scripts are at  and

### A19 (cell I3)

Status: I've checked the data and have a number. Here is the answer.

**Short answer for Q2:** West checkout completion time was about **37 seconds faster (roughly 20%)** in the step at the 2026-03-15 rollout. The plausible range is **32–43 seconds (about 18–23%)**, depending on how you treat West's earlier improvement. I'd call it an associated improvement, not a clean causal effect of the new flow. This is a quick analysis, not a full preregistered investigation, and I wrote no [record] file.

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

To get a defensible causal number, you would need a clean comparison. A staggered rollout, or a holdout of West traffic on the old flow, would give one. I can run an [review] on what that design would need if you want it.

### A20 (cell I1)

**23 orders** were placed on June 10, 2026 (UTC).

### A21 (cell I1)

**23 orders** were placed on June 10, 2026 (UTC).

### A22 (cell I4)

# Decision memo: expanding Assist to the rest of the company

**Recommendation: do not expand yet, and do not book any responder-hour savings.** The dashboard's drop in median time to close comes from a change in which incidents were counted, not from faster recovery. Within every severity tier, Assist incidents took longer and used more responder time. The strongest evidence of harm is on the hardest incidents.

## What the data shows

| Measure | Manual (Jun 1–7) | Assist (Jun 8–14) |
|---|---|---|
| Incidents | 210 | 210 |
| Median time to close | 7.27h | 5.44h (the dashboard headline) |
| Mean time to close (closed only) | 7.14h | 7.53h |
| Mean responder minutes per closed incident | 90.2 | 90.9 |
| Incidents with no closure record | 1 | 10 |
| Reopened within 72h | 0% | 4.5% of closed |

**1. The headline is a mix shift (Simpson's paradox).** The severity mix changed abruptly at cutover.

| Severity | Manual share | Assist share |
|---|---|---|
| sev1 | 13% | 7% |
| sev2 | 40% | 20% |
| sev3 | 47% | 73% |

The manual week was exactly 4 sev1, 12 sev2 and 14 sev3 incidents every day. In the Assist week it was about 1.3 sev1 and 6 sev2 a day. Total volume stayed at 15 per group per day, so total incident count did not change. A larger share of easy incidents pulls the median down. Within each severity, Assist is slower:

| Severity | Time to close, manual | Time to close, Assist | Responder minutes, manual | Responder minutes, Assist |
|---|---|---|---|---|
| sev1 | 17.9h | 28.2h | 240 | 312 |
| sev2 | 8.5h | 12.2h | 99 | 137 |
| sev3 | 2.9h | 5.1h | 39 | 65 |

The responders' complaint matches this. Holding severity mix fixed, Assist adds about 3.0h per incident (95% interval 2.9–3.2h) and about 32 responder minutes per incident (30–33). These intervals reflect sampling noise only. They do not cover the design problems below.

**2. The worst cases are missing from the Assist numbers.**
- 5 of 14 Assist sev1 incidents (36%) had no closure record after 8.5 to 15 days. No manual sev1 was left open.
- Those unclosed incidents are excluded from every Assist figure above, so the Assist numbers are flattering.
- All 9 sev1 incidents that did close under Assist were reopened within 72h.
- Those 9 also show about 0.4 handoffs, versus 5.9 under manual. That pattern suggests premature closure.

**3. The other fields do not support expansion either.**
- Handoffs are higher under Assist for sev2 (3.95 vs 3.01) and sev3 (1.52 vs 0.54).
- Staffing rose at cutover: 12→14 responders in identity and 11→13 in storage, with scheduled hours up about 20 a day.
- Interruption minutes were also higher in the Assist week. This is a second change made at the same time as the cutover.
- Staffing cannot explain Assist being slower. It does mean no speedup could be credited to Assist alone.

## Responder-hours attributable to Assist

**Credible savings: zero.**
- **Unadjusted:** responder minutes per incident are flat (+0.7 min, about +2.5 hours over 210 incidents), so there is no saving even before adjustment.
- **Severity-adjusted:** about +32 min per incident, roughly **+110 responder-hours of extra work** in the Assist week (closed incidents only).
- **Finance's likely headline:** a median-based saving of about 18 minutes per incident, or roughly 63 hours. That figure comes entirely from the severity-mix shift and should not be booked.
- **Missing records:** the 10 unclosed Assist incidents have no recorded minutes, so the +110 hours is probably an underestimate.

## What this data can and cannot establish

**It can establish:**
- The headline median drop is explained by mix, not speed.
- Assist-week incidents were slower and heavier within each severity.
- Sev1 closures under Assist are suspect.

**It cannot establish:**
- **Causation in either direction.** There is no holdout, only one pre-week, and staffing changed at the same moment as the workflow. "Every incident followed the workflow active when it opened" is true, but it does not make the comparison clean, because everything else also changed on June 8.
- **Why severity shifted.** Either Assist or intake changed how severity is assigned, or the incident mix genuinely changed. If Assist downgrades severity, then comparing within severity is itself biased, and I'd want to see the severity-assignment logic.
  - Even without adjusting for severity, Assist shows no gain in mean time to close, mean responder minutes, or closure completeness.
  - The conclusion "no demonstrated benefit" holds under both readings.
- **Whether the sev1 reopens and unclosed incidents are real recovery failures or recording artifacts.** The 11 missing activity rows need checking against the source system.
- **Anything after one week, or about service groups beyond identity and storage.**

## Before Monday

1. Check the 11 missing activity rows in the source system, especially the 5 sev1 incidents.
2. Find out who sets severity and whether Assist influences it.
3. Re-run any rollout with a holdout. Randomize incidents, or stagger a service group at a time. Compare within severity as assigned before the workflow acts.
4. Hold any savings booking until a rerun confirms a benefit.

I used only the three local exports. The scripts are in  The analysis uses Python's standard library, because pandas was not available here.

### A23 (cell I2)

There is one real problem in the logs, plus a data gap that is probably an ingestion issue.

**Overview:** The file has 6,924 events from 2026-05-01 to 2026-06-30, across 420 accounts. The overall error rate is 4.4%, with 305 errors. The data is clean: no duplicate IDs, no malformed rows, no out-of-order timestamps, and each account stays on one plan and one region. Traffic follows a normal weekday/weekend pattern.

**1. Client 4.2.3 fails on `/export` about 22% of the time**
- Events on `/export` from client 4.2.3 errored in 87 of 400 cases (21.8%). Every other combination of client version and endpoint sits at roughly 0.6–9%, and the rest of the dataset errors at 3.3%.
- Several things suggest the cause is the 4.2.3 client on `/export` rather than something else:
  - **Not a plan effect:** Enterprise has a higher overall error rate (6.5%), but 4.2.3 `/export` is bad on every plan: 25% on enterprise, 21.5% on growth, 19.9% on starter. Other `/export` traffic on enterprise is only 3.9%.
  - **Not a region effect:** It is about 21–23% in all three regions.
  - **Not one bad account:** The 87 errors are spread across 82 accounts, and no account has more than 2.
  - **Not a one-off incident:** It runs at roughly 15–30% every week for the full two months.
  - **Not chance:** I shuffled the error labels 500 times, and no client-version/endpoint cell came close to 21.8%.
- **Where it matters:** 4.2.3 is about 17% of all traffic and the second most used version. It also accounts for about 114 of the 305 errors.
- **Limits:** The logs only have a status of `ok` or `error`, so I can't say why it fails. The next step is a look at the 4.2.3 changelog for `/export` changes, and at server-side error messages for those requests. This is a correlation, not a confirmed root cause. 4.2.3 may also differ in some way I can't see, such as payload size. 4.3.1 and 4.4.0 don't show the problem on `/export`, so upgrading looks like a likely fix.

**2. APAC data is missing from May 13 22:55Z to May 17 00:01Z**
- That is a gap of about 3 days. The next-longest APAC gap is about 7 hours.
- It explains the low daily counts on May 14–16, such as 43 events on Sat May 16. It looks like a collection or ingestion outage rather than real traffic. I can't tell from this file whether APAC was actually down or only unlogged, so check that.
- APAC's slightly higher error rate of 4.9% is not a concern, since it is within what chance would produce.

**Other things I checked that look fine**
- **Client versions:** Old versions (3.9.4, 4.0.x) are declining and 4.3.1 and 4.4.0 are growing, which looks like normal rollout.
- **Time patterns:** Error rates are flat across the two months, and the hourly variation looks like noise.
- **`/ingest`:** It has the lowest error rate, at 1.9%.

### A24 (cell I3)

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

**Not done:** I didn't write a [record] or run a formal [review], because you asked for a number rather than an audit. A cleaner confirmation would be a staggered rollout, or holding back a slice of West. If this number will drive a decision, I can run `[method]` on the design.

### A25 (cell I3)

For the Q2 review, I’d report **a 50-second observed drop in West’s median daily checkout time, from 196.6 to 146.6 seconds, or about 25%**. East’s median held steady at about 180 seconds. **The data can’t isolate how much of West’s improvement came from the new checkout flow.**

West was already gaining on East by about half a second per day before launch, during a separate West-only UX cleanup. After extrapolating that pre-launch trend, West’s daily checkout times averaged **32 seconds below the projected level** over the four weeks after launch. A West-only price promotion began on launch day, so that gap can include effects from both changes. West was also selected because it had the most prior cart-abandonment complaints, which limits East’s usefulness as a comparison.

The post-launch window runs from March 15 through April 11. The extract covers only the first 11 days of Q2.

### A26 (cell I2)

Two things in the logs look real, and I'm less sure of a third.

I used 7 of a planned 20 queries. The full record, with the [record] and the search behind each lead, is in [record file] in the working directory. The log passes the [record check].

## What the data is
There are 6,924 events from 2026-05-01 to 2026-06-30, spread over 420 accounts. The file has no empty fields, no duplicate IDs and no malformed timestamps. Volume follows a normal weekday/weekend rhythm. 4.4% of events are errors. The only status values are `ok` and `error`, with no latency, error codes or reasons.

## Real: client 4.2.3 fails on `/export`
- **Rate:** 4.2.3 on `/export` errors on 72 of 345 events (21%). Every other version on `/export` errors at 2.9%. 4.2.3 on the other endpoints is normal, at 3.6%.
- **Spread:** it appears on all three plans and all three regions. It spans 232 accounts, and the five worst account-level counts make up about 10% of the errors. It's steady week to week rather than an incident burst.
- **Other cells:** the next most unusual version-and-endpoint cell out of 36 is 10% on 69 events.
- **Holdout:** I held back the last week (06-24 to 06-30) while searching. It shows 15 of 55 errors (27%) for 4.2.3 on `/export`, against 2.4% for everything else.
- **Significance:** a shuffle test puts the chance of this by luck below 0.02%.
- **Limit:** the file records only that it happens. The cause would have to come from server logs or a comparison of the 4.2.3 export code with 4.2.0. 4.2.3 is also among the most-used versions, so this affects a lot of traffic.

## Real, but a data gap: no APAC events for 73 hours
- **Gap:** from 05-13 22:55Z to 05-17 00:01Z, APAC logged nothing, while EU and NA kept going. The next-longest APAC gap is 6 hours. This is also why May 14–16 looked like a volume dip.
- **Open question:** this file can't tell a real APAC outage from lost logging. Ask whoever owns the APAC log pipeline about 05-13 to 05-17.
- **Side effect:** any APAC statistic that includes those days is understated.

## Weak, don't act on it: enterprise errors in May
Enterprise accounts show more errors even without 4.2.3 (5.3% against about 2.9%). The excess is mostly on `/search` and `/report` in May and early June, and it disappears from about 06-08. I looked at many slices, the weekly counts are small, and I never checked it on the holdout week. Treat it as probably overstated until someone checks server logs.

## Limits
The file can't show whether it is all traffic or a sample, so absence of events means different things depending on the source. The 4.2.3 result is a pattern in the logs, not a diagnosed cause.

### A27 (cell I2)

**Two error patterns held up.** `/export` requests from client `4.2.3` failed at about 7.5 times the rate of other versions in both months. Enterprise `/search` had a separate spike in May that largely subsided in June.

| Segment | May error rate | June error rate |
|---|---:|---:|
| `/export`, client `4.2.3` | 21.8% (41/188) | 21.7% (46/212) |
| `/export`, other clients | 2.6% (25/964) | 3.2% (31/978) |
| `/search`, enterprise | 12.8% (35/274) | 4.1% (12/292) |
| `/search`, other plans | 3.4% (30/888) | 2.9% (27/944) |

- **`/export` on `4.2.3` was the biggest issue.** Its 400 events accounted for 5.8% of traffic and 28.5% of all errors. The higher rate held across every week represented in the logs, all three regions, and all three plans. Among the 248 accounts that used both `4.2.3` and another version for exports, the rates were still 21.8% versus 2.5%. The other endpoints showed no comparable spike on `4.2.3`.
- **The May enterprise `/search` spike was widespread.** The 35 errors were spread across 27 accounts and 18 days. The gap held after accounting for week, region, and client version. Removing the worst day still left an 11.3% error rate versus 3.5% for other plans. June showed a much smaller gap.

The logs cover **6,924 events across 420 accounts** from May 1 through June 30, 2026. Overall errors fell from 4.8% in May to 4.1% in June, while the export issue persisted. The file records only `ok` or `error`, so it establishes where failures were concentrated. Root cause, latency, and whether the issues continued after June remain unknown.

### A28 (cell I1)

**23 orders** were placed on 2026-06-10 (UTC).

All timestamps in the file end in `Z`, so no timezone conversion was needed. None of the 23 order IDs from that day are duplicated.

### A29 (cell I4)

**Defer company-wide expansion and book 0 responder-hours of savings.** Both pilot groups switched on the same day, so the exports cannot establish how much of the change Assist caused. The comparisons accounting for incident mix point toward slower closure and higher labor.

The dashboard’s median fell from **436 to 326.5 minutes** among recorded closures. During the same week, sev3 incidents grew from **47% to 73%** of openings, and median closure time rose within every severity tier. Recorded closures within seven days fell from **209 to 200** out of 210 openings per week. All nine recorded Assist sev1 closures reopened within 72 hours.

The 200 Assist incidents with recorded closures used **102 more responder-hours** than expected at manual-week rates for the same severity, service group, and intake channel. Sensitivity scenarios for missing activity yielded **78 to 110 excess hours**. These are descriptive comparisons, and the causal labor effect remains unknown.

### A30 (cell I3)

**For the Q2 review, report a 50-second drop (25.4%) in West’s median daily checkout completion time after rollout.** It fell from 196.6 seconds before March 15 to 146.6 seconds from March 15 through April 11. East was essentially flat at 180 seconds. 

The data can’t isolate how much of that drop the new flow caused. West was already getting faster relative to East during a separate UX cleanup, and a West-only price promotion began on rollout day.  · 

The 50 seconds compares the median of the daily values for February 1–March 14 with March 15–April 11. The extract covers Q2 only through April 11.

### A31 (cell I1)

**23 orders** were placed on 2026-06-10 (UTC).

All timestamps in the file are in UTC (`Z` suffix) and well-formed, and there are no duplicate order IDs. That means the count is a plain match on the date prefix.

### A32 (cell I2)

One real problem holds up. The rest of the data looks healthy, and one second lead did not hold up.

## What's going on
- **Data quality:** the file is clean. It has 6,924 events over 61 contiguous days (2026-05-01 to 06-30), with no missing values and no duplicate IDs. Traffic has a normal weekday/weekend rhythm.
- **Error rate:** overall errors run at about 4.4% and are flat week to week. No region or plan has a problem on its own.

## The real problem: `/export` on client version 4.2.3
- **Exploration window (05-01 to 06-23):** `/export` calls from client 4.2.3 errored on 72 of 345 (20.9%). `/export` on every other version errored on 50 of 1,720 (2.9%).
- **Held-out week (06-24 to 06-30):** I kept this week out of the exploration and tested only afterwards. 4.2.3 `/export` errored on 15 of 55 (27.3%), against 6 of 222 (2.7%) for other versions. This is a clear replication, with z of roughly 6.
- **Scope:** the problem is specific to the combination. 4.2.3 on other endpoints errors at the normal rate (2.0% in the held-out week, against 2.4% for other versions).
- **Spread:** it is steady week to week, appears in all regions and plans, and touches 70 distinct accounts in the error set. It isn't one noisy customer.
- **Impact:** 4.2.3 `/export` accounts for about 90 of the roughly 305 errors in the whole file.

The data can't tell you why. A version-specific bug is the obvious suspect, but the file has no HTTP codes or error details to confirm that. Start by checking what changed in `/export` handling in 4.2.3.

## The lead that did not hold up: enterprise on `/search`
- In the exploration window, enterprise `/search` errored at 8.8%, against 3.5% for other plans.
- In the held-out week it was 4.1% (3 of 73) against 1.8% (4 of 221). The direction is the same, but there are only 3 errors, so I can't distinguish it from noise.
- I'd call it unresolved, not a problem. It would need more data to settle.

## Caveats
- I can't verify completeness. There is no independent traffic count, and about 114 events a day is low for an API, so the file may be a sample. The 4.2.3 rate should hold either way, but treat the absolute counts as sample counts.
- `status` is only ok or error, with no error codes or latency.
- The held-out week is now used up. Further confirmation of D1 needs new data, for example next week's events or a 4.2.3 rollback comparison.
- Weekends in the data are quiet (about 65 to 80 events), and 05-16 was the lowest day at 43. I looked at this only as a coverage note, not as a lead.

The log, with the [record] and the predictions written before the held-out test, is at [record file] in the working directory. I ran the [tool] [record check]. That checks the record's structure, not the analysis.

### A33 (cell I2)

**The clearest API problem in the logs is `/export` on client version 4.2.3.** About one in five recorded events in that group was marked `error` in both months. I used May to find the pattern and held June back to check whether it repeated.

| Comparison | May | June holdout |
|---|---:|---:|
| `/export`, client 4.2.3 | 21.8% (41/188) | 21.7% (46/212) |
| `/export`, other versions | 2.6% (25/964) | 3.2% (31/978) |
| `/search`, enterprise | 12.8% (35/274) | 4.1% (12/292) |
| `/search`, other plans | 3.4% (30/888) | 2.9% (27/944) |

The `/export` gap held in every June week. Matching the comparison traffic to the 4.2.3 traffic mix by week, plan, and region left an **18.5 percentage-point gap**. The 46 June errors were spread across 44 accounts. Across the other endpoints combined, June’s recorded error rate for 4.2.3 was 2.4%, compared with 2.9% for the other versions.

**The large May enterprise `/search` gap did not recur in June.** It fell from 9.4 percentage points to 1.2 points. Accounting for week, client version, and region put the June gap at 1.8 points. The May spike remains unexplained.

Overall, the file contains **6,924 events and 305 errors (4.4%)**. The recorded error rate fell from 4.8% in May to 4.1% in June. All 61 UTC dates were represented, with no duplicate event IDs or blank fields. The export lacks independent request totals, error codes, and retry linkage, so coverage and root cause remain unknown. The replicated finding is the elevated **recorded event error rate** for the `/export` and 4.2.3 combination.

 ·

### A34 (cell I4)

The evidence doesn't support expanding Assist or booking any responder-hour savings. The median time to close did fall from 7.27 h to 5.44 h, but that comes from a change in case mix, not from Assist.

**Why the headline is misleading**
- The share of sev3 incidents jumped from 47% to 73% of volume in the Assist week, and sev3 incidents close fast, so the pooled median drops.
- Within every severity, Assist-week incidents closed later, with the gaps below (Assist minus manual; intervals are 95% bootstrap and exclude zero):

| Severity | Time to close | Responder minutes |
|---|---|---|
| sev1 | +10.3 h | +72 min |
| sev2 | +3.7 h | +38 min |
| sev3 | +2.2 h | +26 min |

- At a common severity mix, Assist costs about 3.5 h of clock time and 34 min of responder time per incident. That matches what the responders are saying about difficult incidents.

**Other fields point the same way**
- **Reopens:** all 9 recorded sev1 incidents in the Assist week were reopened within 72 h, against none of 28 in the manual week.
- **Missing records:** 10 of the 11 incidents with no activity record are in the Assist week, including 5 of 14 sev1 incidents. I can't tell from the files whether these are still open or just unrecorded. All figures above use only incidents that have a record.
- **Staffing:** active responders rose by 2 per group on June 8, the same day as the cutover. Interruption minutes per group-day also roughly tripled.

**Responder-hours attributable to Assist: zero.**
- Finance's figure is clock time, not responder effort.
- Recorded responder hours barely moved (314 h to 303 h), and that gap comes from the missing records and the lighter mix.
- If Assist were the only change, the standardized estimate would be a cost of roughly 115–120 responder-hours over the Assist week. Treat that as an upper-bound illustration, not a booked number.

**What the data can't establish**
- It can't prove that Assist caused any of this: there was no holdout, only one week per arm, and staffing changed at the same time.
- It can't explain why the severity mix shifted. If Assist changed how incidents get labeled, even the within-severity comparison is biased.
- Closure records can't be checked for completeness.
- I looked at the Assist-versus-manual comparison before writing down hypotheses. So the findings are retrospective and are not preregistered.

**Before Monday:** ask the dashboard and Finance teams how they handled the 11 missing records. Check whether triage or intake rules changed on June 8. If you expand at all, stagger or randomize the rollout with staffing held constant, and pre-register time to close, responder minutes by severity, and reopen rate. The memo lists these steps.

The [record check].

Files are in 
- [record file]
- [record file]

### A35 (cell I2)

The [record check]. That is a structural check only, not a claim that the analysis is right.

## Summary

The file holds 6,924 events from 2026-05-01 to 2026-06-30, across 420 accounts and 4 endpoints. Overall, 4.4% of events are errors. The data is clean: no duplicates, no empty fields, and every day is present. There's a normal weekday/weekend rhythm. The overall error rate is flat by week. Two things hold up as real, and one looked like a problem but is fading.

### 1. Client version 4.2.3 fails on `/export` (holds up)
- Requests from client 4.2.3 to `/export` error about **21%** of the time. Every other version on `/export` errors about **2.7%**.
- On other endpoints, 4.2.3 looks normal, so this is specific to `/export`.
- I tried to break it three ways, and it survived all three:
  - **Not a few bad accounts:** the errors are spread over 70 accounts, with at most 2 each.
  - **Not a plan, region or week mix effect:** it appears in every plan, region and week.
  - **Same accounts, different version:** among the 231 accounts that used both 4.2.3 and other versions on `/export`, errors were 20.9% on 4.2.3 and 2.4% on other versions.
- I also checked it on a held-out week (2026-06-24 to 06-30) that I didn't look at while searching. It was worse there, at **27% (15 of 55)** against 2.7% for other versions.
- **Not known:** why it fails. The file has no error reason or status code, so I can't tell a client bug from the server mishandling 4.2.3 requests. The next step is to pull error details for 4.2.3 `/export` from the gateway logs.

### 2. APAC has no events for 73 hours (a data problem, cause unknown)
- No APAC events were logged from **2026-05-13 22:55Z to 2026-05-17 00:01Z**, which includes two weekdays. NA and EU were normal. No other gap in any region exceeds 7.3 hours.
- This file can't say whether APAC had an outage, a logging or export gap, or no traffic. To find out, compare it against gateway or load-balancer counts for those dates.
- If it was a real outage, it was invisible in this data. If it was a logging gap, any APAC analysis over that window is incomplete.

### 3. Enterprise `/search` errors were elevated, then faded (probably not a current problem)
- The error rate was 8.8% against about 3.5% for other plans, peaking at 22.6% in week 19 and falling to about 3% by week 25.
- The held-out week had 3 errors in 73 requests, which can't be told apart from baseline. It looks like a transient issue that has mostly cleared. The size of the early spike is probably overstated, because I picked it out by searching. Check whether an incident or deploy was recorded for weeks 19–22.

### Other notes
- The raw enterprise (6.5%) and `/export` (5.9%) error rates looked elevated. Part of that is the 4.2.3 effect and the rest is the enterprise `/search` episode. I found no separate problem there.
- Counts are per logged event, not per user, and I had no independent source to check coverage against.

The log, with looks, leads and the held-out check, is at [record file] in the working directory. I used about 11 of the 25 tool calls I'd budgeted.

### A36 (cell I1)

**23 orders** were placed on 2026-06-10 (UTC).

I counted rows in `orders.csv` whose timestamp starts with `2026-06-10T`. Every timestamp in the file ends in `Z`, so they are all UTC and no conversion was needed. I also checked for duplicate order IDs and found none.

### A37 (cell I4)

**Defer company-wide expansion and book zero responder-hours of savings from this pilot.** The exports cannot establish whether Assist caused faster recovery or how much labor it saved. Zero is the amount Finance can credit today. The actual effect, including its direction, remains unknown.

- **The dashboard’s 25% median improvement reverses at a common incident mix.** The recorded median fell from 436 to 326.5 minutes as the share of Sev3 incidents rose from 47% to 73%. At the Assist week’s mix of severity and service group, median closure rose from 196 to 328 minutes.
- **Recorded labor also rose at a common mix.** Mean responder effort rose from 64.6 to 96.2 minutes per incident, equivalent to about **111 additional responder-hours per 210 incidents**. That compares the two weeks and cannot isolate Assist’s effect.
- **Severe incidents warrant particular attention.** All nine recorded Assist Sev1 closures reopened within 72 hours, compared with zero of 28 manual closures. Five of the 14 Assist Sev1 incidents had no activity row, and the exports cannot distinguish unresolved work from missing records.

Both service groups switched together, while staffing, interruptions, and incident mix also changed. Keep Assist at pilot scope and use a concurrent controlled comparison that tracks responder effort through reopened work before reconsidering expansion or crediting savings.

### A38 (cell I3)

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

### A39 (cell I1)

**23 orders** were placed on June 10, 2026 (UTC).

### A40 (cell I1)

**23** orders were placed on 2026-06-10 (UTC).

All timestamps in the file are in UTC (`Z` suffix) and well-formed. I checked for duplicate order IDs and found none, so the count is 23 distinct orders.

### A41 (cell I1)

**23 orders** were placed on 2026-06-10 (UTC).

All timestamps in the file are in UTC (they end in `Z`), so no timezone conversion was needed. There are no duplicate order IDs.

### A42 (cell I2)

**The clearest problem in the logs is `/export` on client version 4.2.3.** In the June 16–30 events I reserved for verification, 22 of 115 exports on 4.2.3 were marked `error` (**19.1%**), compared with 16 of 498 on other versions (**3.2%**). That’s a **15.9 percentage-point gap**.

| `/export` error rate | Client 4.2.3 | Other versions |
|---|---:|---:|
| May 1–June 15, initial review | 22.8% (65/285) | 2.8% (40/1,444) |
| June 16–30, verification | 19.1% (22/115) | 3.2% (16/498) |

The gap appeared in both halves of the verification window, in every region and plan, and among accounts that used both version groups. The 22 errors on 4.2.3 came from 22 distinct accounts. Outside `/export`, 4.2.3 had a **2.5%** recorded error rate versus **3.2%** for other versions. That makes the export and version combination the priority for investigation.

**Enterprise `/search` had a smaller, earlier spike that didn’t persist.** From May 1–14, enterprise search recorded **16.7%** errors (21/126) versus **3.2%** for other plans (13/405). By June 16–30, the rates were **3.4%** (5/146) and **3.8%** (18/480), respectively.

The export contains **6,924 events across 420 accounts**, with **305 marked `error` (4.4%)**. All 61 days are represented, event IDs are unique, and every field is populated. The CSV has no independent request totals, HTTP codes, or retry identifiers. The repeated `/export` gap is established for the recorded events. Its cause, the true production error rate, and the number of unique failed requests remain unknown.

### A43 (cell I1)

23 orders were placed on June 10, 2026 (UTC).

### A44 (cell I2)

Two things stand out in the logs, and one of them is a real problem. I checked both before writing this up.

**The dataset:** 6,924 events from 2026-05-01 to 2026-06-30, across 420 accounts. There are no duplicate IDs, no missing fields and no malformed timestamps. The overall error rate is 4.4% (305 errors), and it is flat across the two months and across hours of the day. Weekdays run at about 130 events a day and weekends at about 70.

**1. Client 4.2.3 on `/export` fails about 22% of the time. This is a real problem.**
- Those 400 calls had 87 errors (21.8%). Everything else combined had 218 errors in 6,524 calls (3.3%).
- It's specific to that combination. 4.2.3 on other endpoints errors at 3.4%, and `/export` on other versions errors at 2.9%.
- It isn't a mix effect:
  - Every plan shows it: enterprise 25%, growth 22%, starter 20%.
  - Every region shows it: apac 21%, eu 23%, na 22%.
  - It's there in both months (21.8% in May, 21.7% in June), so it isn't a one-off incident.
- It isn't one bad account. 82 of the 249 accounts that used this combination hit errors.
- It also explains why enterprise looks worst overall (6.5%). Without these calls enterprise drops to 5.3%, which is still the highest plan, so I can't fully explain that residual from this data.

My read is that 4.2.3 has an `/export` regression that has been live for the whole period. The logs show where it fails but not why. Check the 4.2.3 release changes to `/export`. If an upgrade path exists, 4.2.3 users are the ones who need it.

**2. There are no APAC events from 2026-05-14 to 2026-05-16. This is real in the data, but I can't tell what caused it.**
- APAC normally logs 30–34 events a day. Then it logs exactly 0 for three full days, and about 14 on the 17th as it recovers. NA and EU are normal throughout, apart from a weekend dip.
- It's complete silence from every APAC account, not a drop, so it looks like an APAC outage or an ingestion/logging gap rather than a change in user behavior. The logs only record that no events arrived, so they can't say whether the API was down or the logging was. Check infra and incident records for those dates.
- It's also why the volume dip on 05-14 to 05-16 looked odd.

**Looked at and not worth acting on:**
- 4.1.2 on `/report` had 7 errors in 74 calls (9.5%), against about 3 expected. That's too few calls to say anything, so I'd just keep an eye on it.
- `/export` is the worst endpoint overall (6.1%), but that's almost entirely the 4.2.3 issue above.
- The hourly error rates (2–7%) are noise at these sample sizes.

I only had the CSV, with no deploy history or incident records, so the causes above are hypotheses. The data itself supports the 4.2.3 `/export` failure rate and the 3-day APAC gap.

### A45 (cell I3)

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

### A46 (cell I4)

**Defer company-wide expansion and book 0 responder-hours of savings.** The pilot cannot establish whether Assist caused faster recovery or how many hours it saved or added. Both service groups switched on the same day, while staffing, interruptions, and incident mix also changed.

The dashboard median fell 25%, from 436 to 326.5 minutes, as Sev3 incidents rose from 47% to 73% of intake. Within every severity tier, recorded closures took longer and required more responder minutes. Seven-day recorded closure fell from 99.5% to 95.2%, and all nine recorded Assist Sev1 closures reopened within 72 hours, versus zero of 28 manual Sev1 closures.

At the Assist week’s severity and service mix, the comparison implies **111 additional responder-hours** across 210 incidents when missing effort is filled in using the observed average for each group. Alternative assumptions gave 78 to 144 additional hours. These are descriptive scenarios, and the causal effect remains unidentified.

The memo recommends auditing the missing resolution records and Sev1 reopenings, then running a controlled extension with a contemporaneous manual holdout before reconsidering expansion.

### A47 (cell I2)

The May–June logs show **persistent `/export` failures on client 4.2.3**, **elevated enterprise `/search` failures in May**, and **three days of missing APAC events**. I rechecked both error patterns after excluding the dates with missing APAC data. Both held up.

The file contains 6,924 events across 420 accounts, with 305 errors (4.4%). The overall error rate fell from 4.76% in May to 4.06% in June, mainly because search errors fell. The export problem persisted through the end of June.

| Finding | What held up |
|---|---|
| **`/export` on client 4.2.3** | **87 of 400 requests failed (21.75%)**, versus **56 of 1,942 (2.88%)** on other versions. The rate was nearly identical in May and June, and the gap appeared in every region and plan. Among the 248 accounts that used both 4.2.3 and other versions for exports, the rates were 21.80% versus 2.47%. The failures reached 82 accounts across 47 days. On the other endpoints combined, 4.2.3 had essentially the same error rate as other versions. |
| **Enterprise `/search` in May** | **35 of 274 requests failed (12.77%)**, versus **30 of 888 (3.38%)** for other plans. The gap held across all three regions and both halves of May. Matching the comparison for region and client version gave a 3.35% baseline. Enterprise search fell to **12 of 292 (4.11%)** in June, and the decline also held among enterprise accounts that used search in both months. |
| **APAC events missing May 14–16 UTC** | APAC recorded **zero events across all endpoints** for three full days, while EU and North America recorded 221. Every other date had APAC traffic. Comparable Thursdays, Fridays, and Saturdays suggest roughly **90 APAC events** would ordinarily appear over those three days. The file establishes the gap. Independent request or logging telemetry would distinguish a traffic interruption from a collection failure. |

I’d investigate the `/export` path for 4.2.3 first. That combination produced **29% of all recorded errors on 6% of traffic**. The logs identify where the failures concentrate. They contain only `ok` or `error` status, so the underlying failure mechanism remains unverified.

### A48 (cell I2)

The clearest recurring problem in the logs is **`/export` on client version `4.2.3`**. About 22% of those events recorded an error in both months, versus about 3% for other versions using the same endpoint. I also verified a three-day gap in APAC records. Whether that gap reflects missing logs or a traffic interruption is unresolved.

| Signal | May | June holdout | What held up |
|---|---:|---:|---|
| `/export` on `4.2.3` vs. other versions | 21.8% (41/188) vs. 2.6% (25/964) | 21.7% (46/212) vs. 3.2% (31/978) | The gap appeared in all three regions and every June week. It stayed at 18.5 percentage points after accounting for region, plan, and half-month. The 46 June errors spanned 44 accounts, and other endpoints showed much smaller version differences. |
| Enterprise `/search` vs. other plans | 12.8% (35/274) vs. 3.4% (30/888) | 4.1% (12/292) vs. 2.9% (27/944) | The May spike was present in the logs. The June gap fell below the 3-point threshold I set before checking June and reversed in the second half. |

**APAC had zero records from May 14 through May 16 UTC.** EU and North America recorded 221 events over those dates, and APAC had records on every other date in the file. A second count reproduced the gap. Independent gateway counts would help distinguish a logging gap from a traffic interruption.

Across both months, the file contains **6,924 events from 420 accounts**, with 305 errors (4.4%). The 400 `/export` events on `4.2.3` account for 87 errors, or **29% of all recorded errors**. The file has unique event IDs and no blank fields. Without independent traffic counts or error details, it establishes the recurring association but leaves production-wide rates and root cause unresolved.
