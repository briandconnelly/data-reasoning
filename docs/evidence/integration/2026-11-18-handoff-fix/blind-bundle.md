# Blind bundle — 2026-11-18 handoff-fix reruns

### B01 (cell I3)

I can't give you a defensible number for how much faster the new flow made checkout. The West-vs-East comparison doesn't isolate the new flow's effect, so any figure would mostly measure other things.

**What the data shows (descriptive only, not an effect):**
- West median completion time was 187 s in the last pre-rollout week and about 146–147 s in each of the four weeks after 2026-03-15. That is a drop of about 41 s, which looks like a step at the rollout date.
- East was flat at about 180 s throughout.

**Why that drop can't be credited to the new flow:**
1. **The pre-trends aren't parallel.** West's gap to East shrank steadily before rollout, from 27.6 s to 7.0 s over six weeks, about 4.5 s per week. East didn't move. `ux_cleanup_note.md` says a separate shipping-step cleanup reached West gradually through the pre-period, and East never got it. A difference-in-differences comparison against East would credit that existing improvement to the new flow.
2. **A West-only promotion launched the same day.** `promotions.log` shows a price promotion starting 2026-03-15 in West. Average order value rose from 44.94 to 54.13 in West and stayed flat in East. I can't separate the promotion's effect on completion time from the new flow's.
3. **West was chosen for its high complaint volume** (184 complaints vs East's 97). That raises the possibility of regression to the mean, and nothing in the data lets me test it.

**For the Q2 review:** the safe wording is "West median completion time fell from about 187 s to about 147 s after the 3/15 rollout, coinciding with a West-only promotion and continuing UX improvements. The new flow's own contribution is not isolated." I'd avoid presenting 41 s, or a percentage, as the flow's effect.

**What would identify it:** a staggered or randomized rollout, for example by user or by a second region. A holdout within West would also work. Another option is a donor region with the same UX cleanup and no new flow. I can set up one of these designs if you'd like.

I saved the full review at `records/checkout_review.md`, and the structural validator passed with no findings.

### B02 (cell I2)

The data has one real problem: **client 4.2.3 calling `/export` fails far more often than anything else.** It holds up on data it was not found in.

## The problem
- **Error rate:** 4.2.3 on `/export` errors on about 21% of calls (72 of 345) in 05-01 to 06-23. Other versions on `/export` error on 2.9%.
- **It's specific to `/export`:** 4.2.3 on `/ingest`, `/report` and `/search` looks normal.
- **Held-out check:** I set aside 06-24 to 06-30 before looking, and only checked the candidate patterns against it afterwards. 4.2.3 on `/export` errored 27% there (15 of 55), against 2.7% for other versions.
- **Not one bad account:** it appears in every week (13–28%), in all three plans and regions, and across 70 different accounts, none with more than 2 errors.
- **Why it matters:** 4.2.3 alone is the top-line "version 4.2.3 is bad" signal, with a 9.4% overall error rate against about 3.5% for other versions. That signal is almost entirely this one endpoint.

The file has no error codes, so I can't say why it fails. The next step is a per-error-code breakdown for 4.2.3 on `/export`, plus the 4.2.3 release notes and server logs.

## What didn't hold up
- **Enterprise looks worse (6.5% errors vs about 3.8%).** Part of that came from enterprise on `/search` (8.7%), but that dropped to 4.1% (3 of 73) in the held-out week, so I wouldn't act on it. Enterprise was still higher on other endpoints in the held-out week (8.1%). The cause is unattributed and needs more data. The magnitude is probably overstated, because I picked it out of 12 plan-by-endpoint cells.
- **Week-to-week errors** are flat (3.4–5.3%), with no trend.

## Data caveats
- The file is clean: no nulls, duplicate IDs or odd values.
- I can't tell whether it's complete. It averages about 115 events a day for 420 accounts, so it may be a sample.
- 05-16 (a Saturday) has 43 events against 64–74 on other Saturdays. I can't tell a real quiet day from dropped rows, so it's worth asking whoever runs the export.

The held-out week is now used up, so any further confirmation needs newer or independent data.

The exploration log is `exploration-log.md` in the working directory. The plugin's record validator ran on it and printed nothing; I'm reading that as a pass, but it only checks structure.

### B03 (cell I4)

**Recommendation: don't expand yet, and book no responder-hour savings.** I wrote the full memo to `assist_decision_memo.md` in the working directory.

**Why the dashboard headline is misleading**
- **Mix shift:** The median closing time fell from 7.3h to 5.4h only because the incident mix changed on June 8. A typical day went from 4/12/14 sev1/sev2/sev3 incidents to 2/6/22. Sev3s are the quickest and cheapest, so the pooled median drops even if every tier gets worse.
- **Within tiers, Assist is slower and costlier.**
  - Sev1: +10h to close and +72 responder minutes per incident, and the closing-time ranges don't overlap (manual 14–21h, Assist 26–32h).
  - Sev2: +3.7h to close and +38 responder minutes.
  - Sev3: +2.2h to close and +26 responder minutes.
  - This supports the responders' complaint about extra work on the hard incidents.
- **Mean cost is flat:** Pooled mean responder minutes per incident are 90.2 before and 90.9 after. The median drop is the artifact.

**Other fields point the same way**
- **Unclosed:** 10 Assist incidents never closed, 5 of them sev1, against 1 in the manual week. My Assist figures count only closed incidents, so they are flattering.
- **Sev1 quality:** Handoffs fell from 5–7 to 0–1, and all 9 closed Assist sev1s were reopened within 72h (28 manual sev1s: none). That looks like early closure, not better recovery.
- **Staffing:** Responders rose from 12 to 14 (identity) and from 11 to 13 (storage) at the same cutover. Extra capacity should have helped, which makes Assist look worse still.

**Responder hours**
- **Finance's number:** About 63 hours saved comes from comparing medians across different mixes. It isn't credible.
- **My estimate:** Credible attributable savings are **0 hours**.
  - Pooled, with a floor for the unclosed incidents: about 22 hours more than manual.
  - Holding the mix as given and comparing within tiers: about 111 hours more.

**What the data can't establish**
- **Causation:** A single cutover with no holdout, one week per arm, and staffing changed at the same moment fully confounds Assist with the week. I can't prove Assist caused the slowdown, only that there is no evidence it helped.
- **Why the mix changed:** If Assist changed how incidents get classified, the tiers aren't comparable and the stratified numbers are biased. The pooled result still shows no savings.
- **The unclosed incidents:** I can't tell whether the 10 are truly open or a logging gap.
- **Scope:** Two service groups over 14 days says nothing about the rest of the company.
- **Data quality:** Daily counts and the severity mix are exactly constant within each week. That's unusual for real traffic, so ask the data owners whether the export is templated.

Before any rollout decision, find out what else changed on June 8, resolve the unclosed incidents and sev1 reopens, and rerun with a concurrent control compared within severity tier.

### B04 (cell I2)

The one real problem in this log is that client version 4.2.3 fails on `/export` at roughly 10 times the rate of every other version. It held up when I checked it on data I hadn't used to find it.

## What's going on

- **Overall:** the log has 6,924 events, 61 days, 420 accounts, and 4.4% errors. It is structurally clean, with no duplicate IDs, no empty fields and no missing days. Volume follows a normal weekday/weekend rhythm, and the weekly error rate is flat at about 3.4–5.3%.
- **4.2.3 on `/export`:**
  - The first six weeks showed a 20.9% error rate for 4.2.3 on `/export`, against 2.9% for other versions on the same endpoint.
  - 4.2.3 isn't elevated on `/ingest` or `/search`, so the problem is specific to `/export`.
  - It shows up on every plan, region and week, and it's spread over 87 different accounts, with no account having more than 3 errors.
  - The higher error rate on `/export` overall comes entirely from 4.2.3.

## How I checked it

I held back the last 7 days (06-24 to 06-30) and wrote down what would count as a pass or fail before looking at them. In that window, 4.2.3 on `/export` failed 15 of 55 times (27.3%), against 6 of 222 (2.7%) for other versions. 4.2.3 off `/export` was normal (2.0% against 2.4%). It passed my pre-set bar of at least 3 times the other versions' rate and at least 10% absolute.

- **What this rules out:** the pattern being an artifact of the earlier weeks I searched.
- **What it doesn't rule out:** that 4.2.3 logs errors differently, or that the export itself is incomplete. The last week comes from the same file, not an independent source.
- **Not tested:** why it happens. The data shows the association only.

## Leads that didn't hold up

- **Enterprise errors on `/search`:** enterprise runs at 8.7% there, against about 3.5% for other plans. On the held-back week it was 4.8% against 2.2%, but that's only 3 errors. It missed my 6% bar without being contradicted, so I'd call it unresolved. It came from sifting about 24 small cells, so it could easily be noise.
- **Volume dip on 05-14 to 05-16:** daily counts were 95, 83 and 43, below the usual pattern. The shortfall is spread across hours and endpoints, with no clean outage gap. This file can't tell low traffic from dropped records. Checking it needs an independent traffic count (gateway or billing) for those days.

## Caveats

- The file looks like a sample or extract, and there's no independent count to check its completeness against.
- Magnitudes like "21%" were picked because they were the biggest gaps, so they're probably somewhat overstated. The 27% on the held-back week is the better estimate.
- The record validator ran and printed no findings. I didn't capture an exit code, so treat that as a likely clean pass, not a confirmed one.

## What to do next

The cheapest next step is to look at what 4.2.3 changed in its export path, and to check whether `/export` errors from that version share an error code or message. If you want that cause settled formally, I can hand the 4.2.3 finding to a proper investigation.

The full record is in `exploration-log.md`, with the scripts in `scripts/`, both in the working directory.

### B05 (cell I4)

# Decision memo: expanding Assist beyond the two pilot groups

## Recommendation
**Do not expand Assist yet, and do not book responder-hour savings in the rollout plan.** The data don't show that Assist caused faster recovery, and they point the other way. The credibly attributable saving is **0 responder-hours**. If the severity labels are taken at face value, the point estimate is a **cost of roughly 110 responder-hours** in the Assist week.

## Why the headline is misleading
The dashboard is arithmetically right. Median time to close fell from 436 to 326.5 minutes (−110), and the drop is stable under resampling. It comes from case mix, not from faster work.

| | Manual (Jun 1–7) | Assist (Jun 8–14) |
|---|---|---|
| Incidents | 210 | 210 |
| sev1 / sev2 / sev3 | 13% / 40% / 47% | 7% / 20% / 73% |

The mix is exactly 4/12/14 incidents per day in the manual week and exactly 2/6/22 per day in the Assist week, on all 14 days. Natural variation wouldn't be that regular. It looks like a rule-driven change at cutover, such as triage or severity labelling, not a shift in what arrived.

Sev3 incidents close fast, so a mix with more of them lowers the median regardless of the workflow. Within each severity, Assist is slower and costs more responder time:

| Severity | Median time to close (manual → Assist) | Mean responder minutes (manual → Assist) |
|---|---|---|
| sev1 | 1,100 → 1,659 min (+51%) | 240 → 312 |
| sev2 | 513 → 740 min (+44%) | 99 → 137 |
| sev3 | 167 → 302 min (+81%) | 39 → 65 |

This holds in both service groups and all three intake channels. The two weeks are flat internally, so there is no learning curve or pre-trend that would explain it.

## Responder-hours
- **Per incident, with no adjustment:** mean responder minutes are 90.2 under manual and 90.9 under Assist. That is no saving even before adjusting for mix. If Assist did relabel work as lower severity, the headline gain is only a labelling artefact.
- **Holding severity fixed:** at the manual mix, Assist costs +37 responder-minutes per incident (95% CI +35 to +39) and +233 minutes to close. At the Assist mix the figures are +32 and +182.
- **In hours:** applying the within-severity gaps to the 210 Assist incidents gives about **+111 responder-hours** in the week. That is 17 h on sev1, 27 h on sev2 and 67 h on sev3.
- **Undercount:** that figure leaves out the 10 Assist incidents that never closed and have no activity row. Priced at their severity averages they add at least ~34 hours.
- **Responders' complaint:** the data support it, but it isn't limited to difficult incidents. Sev3 got proportionally worse too.

I can't see Finance's calculation, so I can't say which step failed. Any conversion of the −110 minute headline into hours inherits the mix problem.

## Other fields, which agree with this
- **Unresolved incidents.** 10 of 210 Assist incidents have no close record 8.5 to 15 days after opening, against 1 of 210 under manual. Five are sev1, which is 5 of 14 Assist sev1 incidents. That means the Assist sev1 close times above are understated.
- **Reopens.** All 9 closed Assist sev1 incidents reopened within 72 hours, against 0 of 28 manual sev1. Across all severities it is 9 of 200 against 0 of 209.
- **Handoffs.** Sev1 handoffs fell from 5.9 to 0.4 while minutes rose and every incident reopened. Either handoffs aren't being logged or escalation isn't happening. That is a hypothesis to check, not something the data establish.
- **Staffing changed on the same day.**
  - Active responders rose from 12 to 14 in identity and from 11 to 13 in storage.
  - Scheduled hours rose about 18–20%.
  - Interruption minutes per day rose from 12 to 74 in identity and from 29 to 59 in storage.
  - Recorded incident hours as a share of scheduled hours fell from 24.5% to 19.9%.
  - Capacity went up, so no hours were released. Extra staff should have made close times faster, and they got slower.

## What the data can and cannot establish
**Can establish:**
- The headline median improvement is a composition effect.
- Within every severity, the Assist week was slower and used more responder time.
- Nothing in the data supports booking savings.
- The sev1 outcomes (unresolved incidents and reopens) are a concern.

**Cannot establish:**
- **Causation in either direction.** Assist, the staffing increase, the interruption increase and the severity shift all began at the same midnight. Without a holdout I can't separate them. The within-severity slowdown is large and uniform, but it is still a before/after comparison with one cutover, one week per arm and two groups. The service owners' "clean" claim only covers which workflow applied to each incident. It doesn't cover everything else that changed at cutover.
- **What produced the severity shift.** If Assist changed how incidents are classified, severity is itself an outcome. In that case the per-incident comparison (no saving) is the fairer one, and the stratified one is a sensitivity check.
- **Final outcomes for the unresolved incidents.** Responder minutes are only recorded for incidents with an activity row.
- **Whether the data are complete.** Responder minutes are as recorded in the export, and I haven't checked them against another source.

## Suggested next steps
1. **Today:** triage the 5 open Assist sev1 incidents (INC0211, INC0236, INC0273, INC0311, INC0404) and review the 9 reopened sev1 incidents. That is an operational risk whatever happens with the rollout.
2. **Before Monday:** ask what changed on June 8 in triage and severity rules, headcount and interruption sources. Ask Finance for their hours formula.
3. **If the pilot continues:** run a real comparison, such as a holdout or alternating assignment within each group. Fix severity at intake before assigning the workflow. Track close time and responder minutes by severity, plus reopens, unresolved incidents and handoff logging. Set the expansion criteria in advance.

I ran the analysis with Python's standard library, since pandas wasn't installed. The scripts are in `/private/var/folders/4_/s6fbcjyn4b13xdxkd3lv0kw00000gn/T/an.uoli/`, and I can turn them into a tidy appendix if you want one.

### B06 (cell I4)

# Decision memo: Should Assist expand company-wide?

**Recommendation: no. Don't book any savings, and don't expand yet.** The data doesn't show that Assist made recovery faster. On a like-for-like basis it points the other way.

## 1. The headline is a mix effect

Median time to close did fall, from 436 to 326 minutes. But the incident mix changed at the cutover.

| | Manual (Jun 1–7) | Assist (Jun 8–14) |
|---|---|---|
| sev1 / sev2 / sev3 incidents | 28 / 84 / 98 | 14 / 42 / 154 |
| Share that is sev3 | 47% | 73% |

The change is exact. Both groups went from 4 / 12 / 14 per day to 2 / 6 / 22 per day on June 8. Total volume stayed at 15 per group per day. Sev3 incidents close fastest, so a shift toward sev3 lowers the overall median regardless of the workflow.

Within each severity, Assist is slower. These are medians for incidents with a close record:

| Severity | Manual TTC (min) | Assist TTC (min) | Assist − Manual (95% CI) | Responder min, manual → Assist |
|---|---|---|---|---|
| sev1 | 1,100 | 1,659 | +559 (464 to 715) | 240 → 312 |
| sev2 | 513 | 740 | +228 (182 to 256) | 99 → 137 |
| sev3 | 167 | 302 | +135 (116 to 150) | 39 → 65 |

- **No overlap:** In every severity, every closed Assist incident took longer than every manual one.
- **Adjusted effect:** After adjusting for severity, service group and intake channel, Assist closes about 1.66× slower. It also uses about 33 more responder-minutes per incident (CI 31 to 35).
- **Responder minutes overall:** Unadjusted, they are flat (90.2 vs 90.9 per incident). So even the raw data gives no responder-time saving.

The "extra work on hard incidents" claim from responders is borne out. The worst gap is on sev1.

## 2. Other fields point the same way

- **Missing closures:** 10 of 210 Assist incidents have no close record, against 1 of 210 manual. Seven are sev1 or sev2, and five are sev1 (5 of 14 Assist sev1). Each has been open at least 8.5 days at the extract. Every number above uses closed incidents only, so it flatters Assist.
- **Reopens:** All 9 closed Assist sev1 incidents were reopened within 72 hours. None of the 28 manual sev1 incidents were. Reopens elsewhere were zero in both arms.
- **Handoffs:** Assist sev1 incidents show about 0.4 handoffs against 5.9 under manual. Together with the reopens, that suggests sev1s are being closed without proper escalation. Sev2 and sev3 handoffs are higher under Assist (4.0 vs 3.0 and 1.5 vs 0.5).
- **Staffing changed at the same moment.** Active responders rose from 12 to 14 (identity) and from 11 to 13 (storage). Scheduled hours rose about 18%. Interruption minutes also rose sharply (identity 12 → 74 a day, storage 29 → 59). Assist is therefore not the only change at the cutover.

## 3. Responder-hours I can credibly attribute

**Zero saved.** The Finance figure is the median drop of about 110 minutes × 210 incidents, or roughly 383 hours (my reconstruction, since I haven't seen their number). It has three problems:

- It is built on the mix artifact.
- Elapsed time to close is not responder time.
- Raw responder minutes show no change.

My estimate of the opposite effect, holding severity mix at the Assist-week level:

- **+6,640 responder-minutes, about +110 hours,** over the Assist week (sampling CI roughly 105 to 116 hours).
- **A further 25–34 hours** if the 10 unclosed Assist incidents cost anything like their peers. They have no minutes recorded, so the true cost is probably higher still.
- **Net:** about 135–145 more hours.

Treat this as an upper bound on Assist's own effect, because staffing and interruptions moved at the same time.

## 4. What the data can and cannot establish

**It can establish:**
- The headline improvement is a composition artifact.
- At the same severity, closed Assist incidents were slower and cost more responder time.
- Sev1 handling under Assist looks worse on closure, reopens and handoffs.

**It cannot establish:**
- **Causation, in either direction.** There is one cutover, no holdout and no concurrent control. Staffing, interruptions and the severity mix all changed on June 8. A before-and-after comparison can't separate them from Assist. "Every incident followed the workflow active when it opened" fixes the assignment rule, not the confounding.
- **Why the severity mix shifted.** If the real incident mix changed, adjusting for severity is correct. If Assist's triage re-labels incidents, so that sev1s and sev2s are being downgraded to sev3, then severity is itself an Assist outcome. That would make Assist's slower sev3s even harder to explain. Whichever it is, the headline doesn't hold. This is the first thing to ask the service owners.
- **Whether the 11 missing records are open incidents or an extract gap.** Closure times in the file stop on June 15, which suggests they may be extract gaps. Either way, the missingness is lopsided toward Assist and high severity.
- **Generalization.** The sample is two service groups and one week each.

## 5. Next steps

1. Don't book the Finance savings.
2. Find out why the severity mix and the staffing changed on June 8, and why the 10 Assist incidents have no close record.
3. Audit the 9 reopened Assist sev1 incidents.
4. Before expanding, run a staggered or randomized rollout with a concurrent control. Randomize at the incident or group level, and leave staffing unchanged. Pre-specify severity-adjusted time to close, responder minutes and reopen rate as the outcomes.

Analysis scripts are in `/tmp/an/` (`a.py`, `b.py`, `c.py`). The analysis used pandas and statsmodels, run via `uv`.

### B07 (cell I2)

One real problem showed up, and it held up on data I had set aside before looking. The structural validator on my exploration log came back clean, and that only checks structure, not whether the analysis is right.

**Real problem: `/export` calls from client version 4.2.3 fail far more often than anything else.**
- **Exploration window (May 1 to June 16):** 66 of 290 calls errored (22.8%). Everything else ran at 3.5%.
- **Held-out check (June 17 to 30, 1,664 rows I had not looked at):** 21 of 110 errored (19.1%) against 3.0% for the rest. The 95% bootstrap interval for the difference is 9 to 24 points, so it doesn't include zero.
- **It needs both factors.** `/export` on other versions fails 2.8% of the time, and 4.2.3 on other endpoints fails 3.7%.
- **It isn't one bad account.** It shows up in every plan, region and week, across 64 different accounts.
- **Size:** I'd put the true rate nearer 19% than 23%, since the first number came from searching many combinations. It's about 1 in 5 export calls on a version that makes up roughly 17% of traffic.
- **Cause unknown:** the file has no error codes, latency or request details. I can tell you where the failures are, not why.

**Not confirmed: enterprise accounts may have more errors outside that cell.**
- In the first window, enterprise ran at 5.7% against about 2.7% for other plans.
- On the held-out rows it was 4.0% vs 2.6%, but the interval (−0.7 to +3.6 points) includes zero. That doesn't rule it out, but I wouldn't report it as real.

**Unexplained: May 16 has only 43 events, against a typical 124 a day.**
- The shortfall is spread across most hours, so it isn't a clean outage window.
- The file can't tell a real traffic dip from missing records or an incomplete export. Checking gateway counts for that day would settle it.

**Otherwise the data is clean:** all 61 days are present, with no duplicates or empty fields. Error rates are flat week to week, with no trend.

The log with the full looks, leads and held-out outcomes is at `exploration-log.md` in your working directory. The next step I'd take is pulling error codes for `/export` on 4.2.3 and checking what changed in that client version.

### B08 (cell I3)

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

### B09 (cell I3)

I can't give you a number for the Q2 review that says how much faster the new flow made checkout. The data doesn't isolate the flow's effect.

**What the data shows (descriptive only)**
- West's weekly mean completion time fell from about 187 s (week of 03-08) to about 145–147 s after 03-15.
- East stayed flat at about 179–180 s.
- The West–East gap went from about +7 s to about −34 s.
- I'd treat that ~40 s swing as a raw before/after contrast. It is not the effect of the flow.

**Why it isn't the flow's effect**
1. **West was already improving before rollout.** The West–East gap shrank from 27.5 s to 7 s over the pre-period, about 3.6 s per week (slope −0.51 s/day, SE 0.05). A shipping-step UX cleanup reached only West in those weeks. East-as-control assumes West would have tracked East, and the pre-period shows it didn't.
2. **A West price promotion launched on the same day.** It started 2026-03-15, in West only (average order value jumps from about 45 to about 54). I can't separate its effect on completion time from the flow's. The data has no variation that would let me.
3. **West was chosen because it was the worst region on cart-abandonment complaints** (184 vs 97 in East). Regions picked for being worst tend to improve anyway, and I can't tell how much of West's drop is that.

The review ends in `assumption-contradicted`: parallel trends fails on the pre-period data, and the promotion confound is untestable here. I'm not giving an adjusted or "trend-corrected" figure either, because any such figure would rest on assumptions the data contradicts.

**What would identify it**
- Re-run the flow in a randomized A/B test inside West, or in a region with no concurrent promotion.
- Or get the cleanup's end date and a promotion-free West-like control, to bound what's left.

**For the review, I'd write:** "West completion time fell ~40 s relative to East after the March rollout; the new flow's share is not separable from a concurrent promotion and a prior UX cleanup."

The record is in `identification_review.md`, one level above the data folder. The structural validator ran with no findings.
