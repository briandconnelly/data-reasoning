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

I used only the local exports and did no modeling beyond severity standardization and bootstrap intervals. Scripts are at `/tmp/a.py` and `/tmp/b.py`.
