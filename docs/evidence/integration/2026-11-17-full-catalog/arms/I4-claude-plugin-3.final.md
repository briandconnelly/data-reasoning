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

The structural validator reported no findings on the ledger.

Files are in `/private/var/folders/4_/s6fbcjyn4b13xdxkd3lv0kw00000gn/T/int-I4-claude-plugin-3-e3jzbf2e/`:
- `assist_decision_memo.md`
- `assist_ledger.md`
