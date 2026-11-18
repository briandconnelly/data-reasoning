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

I ran everything with pandas, and the scripts are in `/tmp/an/` (`a.py`, `b.py`, `c.py`).
