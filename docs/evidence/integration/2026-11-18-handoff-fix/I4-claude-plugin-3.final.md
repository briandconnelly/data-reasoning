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
