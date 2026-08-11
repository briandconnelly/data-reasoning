# Investigation Ledger — s1-conversion: did /lp/summer-sale improve checkout conversion?

## Route
Full loop. Per SKILL.md: "'How much did launching the campaign improve conversion' is the
unidentified-assignment case wearing the identified one's clothes: a causal question carrying
a number, with no design behind it." No randomization or controlled rollout is stated anywhere
in the fixtures (orders.csv, sessions.csv, deploys.log) — landing-page traffic is self-selected
(marketing/organic arrival), not assigned. So this cannot be `estimation`; it is `full`.

## Problem
- Decision: whether/how much to credit the summer-sale landing page for a conversion change.
- Falsifiable question: did checkout-reach rate rise, and can any rise be attributed to the
  campaign launch specifically (vs. other concurrent changes or composition)?
- Success criteria: either a defensible causal estimate with identified design, or an explicit
  "not identifiable from this data" plus the descriptive facts that are available.
- Population/timeframe: sessions.csv 2026-06-01 through 2026-06-14 (9172 rows), orders.csv same
  window (269 rows). Units: session-level checkout_reached (yes/no) as the conversion proxy;
  orders.csv has no session_id or landing_page column, so it cannot be joined to attribute
  purchases to a landing page — checkout_reached is the only landing-page-attributable signal.
- Stop condition: descriptive comparison + one before/after check + confound scan; budget ~15
  shell/python calls.

## Orientation (Plan-time, pre-outcome)
- /lp/summer-sale first appears 2026-06-08T08:00Z, sustained daily volume through 2026-06-14 —
  confirms launch date = 2026-06-08.
- deploys.log: v3.3.9 (2026-06-03, /product copy tweaks), v3.4.1 (2026-06-10, "checkout form
  refactor, cart service bump" — touches the outcome mechanism directly), v3.4.2 (2026-06-12,
  logging only). v3.4.1 lands squarely inside the post-launch window, sitewide.
- No session_id on orders.csv: purchase completion cannot be attributed to landing page at all;
  only "reached checkout" within a session is measurable per-page.

## Hypotheses (claim class)
1. **H1 (causal)**: Launching /lp/summer-sale caused higher checkout conversion.
   Necessary prediction: sessions landing on /lp/summer-sale show a higher checkout-reach rate
   than sessions on other pages during the same window, AND site-wide reach rate rises after
   2026-06-08 relative to before, with no adequate rival explanation for the shift.
   No identifying design exists (self-selected traffic, no comparison group that would have
   moved the same way absent the campaign) — this hypothesis is testable only descriptively;
   it cannot be marked REFUTED or SUPPORTED as *causal*, only as *associative*.
2. **H2 (data-artifact/confound)**: The 2026-06-10 checkout-form refactor (v3.4.1) changes
   checkout_reached behavior sitewide during part of the campaign window, contaminating any
   before/after comparison.
   Prediction: a rate discontinuity at/after 6/10 on /home and /product (pages unaffected by
   the campaign) would show the deploy moved the metric independent of the campaign.
3. **H3 (descriptive, compositional)**: Any site-wide average change after 6/8 is driven by
   adding a lower-converting new page into the traffic mix, not by any existing page changing.
   Prediction: /home and /product rates pre- vs post-6/8 stay flat; the site-wide average moves
   only when /lp/summer-sale sessions are included.
4. **H4 (descriptive)**: /lp/summer-sale's own checkout-reach rate, compared to /home and
   /product over the same days, is lower — i.e. the page underperforms rather than outperforms.

## Data validity
- checkout_reached is a within-session boolean; orders.csv cannot corroborate it (no join key),
  so "conversion" here means checkout-reach, not confirmed purchase — stated as a limitation.
- Coverage: every day 6/1–6/14 has session rows for /home and /product; /lp/summer-sale rows
  exist only from 6/8 onward (consistent with launch, not a gap).
- No stated cost/quota on this local fixture; no authorization or consultation gate issue
  (local files, non-production, no PII).

## Analysis (outcomes)
- Landing-page checkout-reach rates, full window (Wilson 95% CI):
  - /lp/summer-sale: 6/1053 = 0.57% [0.26%, 1.24%]
  - /home:          146/5415 = 2.70% [2.30%, 3.16%]
  - /product:       104/2703 = 3.85% [3.19%, 4.64%]
  Non-overlapping intervals: /lp/summer-sale converts *lower*, not higher. → **H4: CONSISTENT**
  (with "underperforms", the opposite of the premise); H1's necessary prediction (higher rate
  on the campaign page) is **CONTRADICTED** by this comparison.
- Site-wide reach rate, pre (6/1–6/7) vs post (6/8–6/14):
  - Including /lp/summer-sale: 3.12% (131/4200) → 2.51% (125/4971) — a decline.
  - Excluding /lp/summer-sale (home+product only): 3.12% (131/4200) → 3.04% (119/3918) — flat.
  → **H3: CONSISTENT** — the site-wide dip is a compositional artifact of mixing in a
  lower-converting new page, not a change in existing pages' behavior.
- Confound scan for H2: /home daily rate around 6/10 (0.0250, 0.0275, **0.0300**, 0.0250,
  0.0275…) and /product (0.0350, 0.0400, **0.0450**, 0.0350, 0.0400…) show no clear step change
  at the 6/10 deploy — no visible discontinuity. → **H2: NON_DISCRIMINATING** (deploy is a live
  confound by timing/mechanism, but this data shows no detectable signature of it one way or
  the other at this small sample size; it cannot be ruled in or out).
- orders.csv has no landing_page/session_id field — order volume by day does not line up
  1:1 with any single page's checkout_reached counts and cannot be reconciled to test H1
  further; noted as a data-validity limitation, not pursued further (would require new data).

## Conclusion
- H1 (causal claim as literally asked) is **not identifiable from this data**: assignment to
  the campaign landing page is self-selected traffic, not randomized or otherwise identified,
  and a mechanism-relevant sitewide deploy (checkout form refactor) lands inside the comparison
  window. No comparison group exists that would have moved the same way absent the campaign.
  Stop rule: **stop with limits** — no available test in this fixture can identify the causal
  effect; that is the answer, not a gap to iterate on.
- What the records do show, associatively: /lp/summer-sale's own checkout-reach rate (0.57%) is
  well below /home (2.70%) and /product (3.85%), and the flat home+product rate before/after
  6/8 shows no sitewide lift coincident with the launch.
- Constructive continuation: `causal-identification-review` (installed) for what design would
  be needed to identify this effect (e.g., a holdout/geo split, or randomized traffic
  allocation to landing pages).
