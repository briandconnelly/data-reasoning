# Investigation: How much did launching /lp/summer-sale improve checkout conversion?

## Problem

- Decision informed: whether to credit the summer-sale landing page with a conversion lift (e.g. continue/scale the campaign) or treat it as neutral/negative.
- Falsifiable question: what happened to checkout conversion (session-level `checkout_reached`) associated with the launch of `/lp/summer-sale`, for sessions 2026-06-01 through 2026-06-14, and can any of that change be attributed to the campaign?
- Success criteria: answered means either (a) a defensible magnitude of improvement is produced with its uncertainty, or (b) the investigation establishes that the causal magnitude is not available from this data and reports the best descriptive account of what did happen.
- Stop condition: conclude when no named unresolved alternative could reverse the answer, within budget.
- Effort budget: ~20 shell/python queries against the local fixtures.

## Assignment check (before routing)

No field or document states how sessions were assigned to `/lp/summer-sale` vs. `/home` vs. `/product` (no randomization, no A/B flag, no referrer/channel field).
`/lp/summer-sale` sessions only start appearing 2026-06-08; before that, only `/home` and `/product` exist.
This is a landing page that was launched to the whole subsequent traffic stream, not a randomized or plausibly-independent split — the unidentified-assignment case the skill names explicitly for this exact question.
Route: **full** (causal question, no identifying design; can't ask the user headless, so proceeding under that assumption per the skill's routing rule, and naming it here).

## Hypotheses

| id | claim | Candidate explanation | Prediction if true | Prediction if false | Necessary prediction (failure refutes) | Cheapest adequate test | Data needed |
| --- | --- | --- | --- | --- | --- | --- | --- |
| H1 | causal | Launching `/lp/summer-sale` improved checkout conversion | site-wide checkout-reached rate rises after 06-08 vs before | rate flat or falls after 06-08 | blended rate must not fall after 06-08 (a true improvement cannot be net negative) | T1 | sessions.csv |
| H2 | descriptive (estimand: `checkout_reached` rate on `/home` and `/product`, pre- vs post-06-08) | The blended rate change is a composition/mix effect: a new, lower-converting landing page was added while existing pages' own conversion stayed flat | `/home` and `/product` rates unchanged pre/post; blended change explained by the new segment's weight and rate | `/home`/`/product` rates also shift materially pre/post | `/home` and `/product` rates must not show a discriminating pre/post change | T2 | sessions.csv |
| H3 | data-artifact | The 2026-06-10 `v3.4.1` deploy ("checkout form refactor") confounds any post-06-08 window, producing a step at 06-10 rather than 06-08 | `/home`/`/product` conversion shows a discontinuity specifically at 06-10 | no discontinuity at 06-10 beyond noise | `/home`/`/product` conversion must show a step at 06-10 for this to explain anything | T3 | sessions.csv, deploys.log |
| H4 | descriptive (estimand: device mix by landing page) | `/lp/summer-sale`'s low conversion is explained by a heavier mobile mix rather than by the page/traffic itself | device mix on summer-sale is materially more mobile-heavy than `/home`/`/product` | device mix is comparable across landing pages | device mix must differ materially between summer-sale and the other pages | T4 | sessions.csv |

H1 has no design that assigns exposure independently of the outcome, so under the skill's Conclusion rule, no test of it alone (an exposure–outcome contrast from an unidentified design) can mark it `REFUTED` — only independent evidence falsifying a necessary prediction without relying on that contrast could, and none exists here. It can be reported as `UNRESOLVED` associatively at most.

## Sources

| id | Origin (file, query, system) | Acquired | Coverage notes |
| --- | --- | --- | --- |
| S1 | `sessions.csv` (9171 data rows) | read in full | 2026-06-01 to 2026-06-14, all 3 landing pages, `checkout_reached` populated for every row |
| S2 | `orders.csv` (268 data rows) | read in full | no session/landing-page linkage; used only for validity cross-check |
| S3 | `deploys.log` | read in full | 3 entries; used to date the refactor confound |

## Data Validity

- Collection method: flat session and order logs; no join key between them (orders carry no landing-page or session id), so orders.csv cannot answer a landing-page-level question and was used only as a cross-check.
- Coverage matrix (day × landing page × device, the grain the analysis uses): every day 06-01..06-14 has rows for `/home` and `/product`; `/lp/summer-sale` rows exist only from 06-08 onward (expected — that's the launch date, confirmed against deploys.log having no earlier summer-sale-related entry). Within 06-08..06-14, all three pages × two devices are populated every day with no zero-count cells.
- Field population: `checkout_reached`, `landing_page`, `device`, `timestamp` are 100% populated (0 missing rows checked directly).
- Coverage baseline: daily session counts jump from 600/day (06-01..06-07) to 760/day (06-08..06-12) then drop to ~585/day (06-13..06-14) — consistent with the new landing page adding volume, then an apparent partial-day cutoff at the data's end (14th and 13th short). No independent traffic-source denominator exists to confirm this isn't a collection artifact; recorded as a coverage note, not resolved further since it doesn't bear on the rate comparisons (rates, not counts, are being compared).
- Known instrument failures: none documented.
- Source completeness semantics: S1 — no absent-record contract available (no independent event counter); declared `UNKNOWN` — S1: UNKNOWN — no independent denominator (e.g. server access log or ad-platform click count) exists to confirm every session was captured, so absence of a session cannot be distinguished from non-occurrence.
- Sensitivity checks performed: Wilson/normal-approximation 95% CIs computed on every proportion comparison the conclusion relies on (T1, T2, T4), at the pre-committed 95% level, on the contrast itself (difference of proportions), not on either arm alone.

## Tests

| id | Hypothesis | Preregistered prediction | Method | Outcome | Evidence |
| --- | --- | --- | --- | --- | --- |
| T1 | H1 | blended `checkout_reached` rate does not fall after 06-08 | proportion pre (06-01..06-07) vs post (06-08..06-14), all landing pages, 95% CI on the difference | NON_DISCRIMINATING | pre 131/4200=3.12%, post 125/4971=2.51%; diff = −0.60pp, 95% CI (−1.29pp, +0.08pp) (S1). The point estimate is a decline and the interval sits almost entirely below zero, but it grazes zero at the upper bound — it does not cleanly discriminate "improved" from "flat/declined," though it rules out a material improvement (any rise ≥0.08pp is outside the interval). |
| T2 | H2 | `/home` and `/product` rates unchanged pre vs post 06-08 | proportion pre vs post per landing page, 95% CI on each difference | CONSISTENT | `/home`: 2.71%→2.68%, diff −0.04pp, CI (−0.90pp, +0.83pp) — contains 0. `/product`: 3.93%→3.76%, diff −0.17pp, CI (−1.62pp, +1.28pp) — contains 0. Both existing pages' own conversion is unchanged within noise (S1). |
| T3 | H3 | discontinuity at 06-10 on `/home`/`/product` | daily rate series for `/home` and `/product` inspected around 06-10 | CONTRADICTED | daily conversion on `/home` and `/product` shows no step at 06-10 beyond the day-to-day noise already present before 06-08 (S1); the refactor is not visible in checkout-reach behavior on unaffected pages. |
| T4 | H4 | summer-sale device mix materially more mobile than `/home`/`/product` | device-share comparison by landing page | CONTRADICTED | device mix is nearly identical across pages: summer-sale 52.2% mobile, `/home` 53.4% mobile, `/product` 53.8% mobile (S1) — a ≤1.6pp spread, not a material difference. Device mix does not explain summer-sale's much lower rate. |

Supplementary (not a separate hypothesis, reported as evidence for the answer): `/lp/summer-sale`'s own conversion rate is 6/1053 = 0.57%, vs. `/home` 2.70% and `/product` 3.85% over the same post-launch window — 95% CI on (summer-sale − pre-existing-pages baseline) = (−3.24pp, −1.85pp), entirely negative (S1).

## Amendments

None.

## Conclusion

- Answer: this data does not support a causal "how much did it improve conversion" number, and the observational record does not show an improvement to attribute one to. Site-wide checkout-reach conversion did not rise after 06-08 (T1: point estimate −0.60pp, CI grazing zero, ruling out any material rise). `/home` and `/product` — the traffic the campaign didn't touch — kept flat conversion across the launch (T2), so nothing site-wide moved because of the launch. `/lp/summer-sale` itself converts far below the other two pages (0.57% vs 2.70%/3.85%, CI entirely negative), and that gap is not explained by device mix (T4) or by the concurrent 06-10 deploy (T3).
- Best supported: H2 (composition effect) — the small blended-rate dip is consistent with adding a new, low-converting segment to the traffic mix while the pre-existing pages' own conversion stayed flat; it is not consistent with the campaign lifting conversion anywhere in the funnel that was measured.
- Per-hypothesis summary:

  | id | claim | status | basis |
  | --- | --- | --- | --- |
  | H1 | causal | UNRESOLVED | no identifying design exists for landing-page assignment, so T1 (an unidentified exposure–outcome contrast) cannot by itself refute or confirm it; the descriptive record it produced (flat-to-down, not up) gives no basis to claim an improvement either |
  | H2 | descriptive | UNRESOLVED | best supported — T2 CONSISTENT (existing pages flat), consistent with T1's small net decline being a mix effect rather than a within-page change |
  | H3 | data-artifact | REFUTED | necessary prediction (a step at 06-10) failed under T3 — no discontinuity found |
  | H4 | descriptive | REFUTED | necessary prediction (device-mix difference) failed under T4 — mix is nearly identical across pages |
- Limitations: assignment to `/lp/summer-sale` was not randomized or stated independent of outcome — visitors who click a sale-page ad or link may simply differ in purchase intent from visitors to `/home`/`/product` regardless of page design, and this data has no channel/referrer field to test that; so even the negative finding for `/lp/summer-sale`'s own conversion is associative, not a claim that the page caused low conversion. Orders.csv could not be joined to sessions (no shared key), so "checkout conversion" here is measured as `checkout_reached`, not completed purchase — if the two diverge, that divergence is not observable from this data. Session-count coverage (fewer sessions on the last two days) was noted but not resolved; it doesn't affect the rate comparisons made. The constructive next step — a design that would actually identify the campaign's effect (e.g., a pre-registered geo or user-level holdout) — is `causal-identification-review`'s work, not reproduced here.
