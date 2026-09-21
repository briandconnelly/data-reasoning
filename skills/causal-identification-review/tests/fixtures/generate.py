#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Generate every committed fixture directory for causal-identification-review.

Ground truth for each fixture is preregistered in
`skills/causal-identification-review/tests/scenarios.md`; this module plants
exactly the properties that catalog states, and nothing else.

Each fixture's builder owns a *local* `random.Random` instance, seeded
independently of every other builder. Nothing here reads from a shared
module-level RNG in call order -- that is the legacy
`hypothesis-driven-analysis/tests/fixtures/generate.py` pattern, where an edit
to one fixture silently reshuffles the draws of every fixture built after it.
Editing CS5's builder cannot change a single byte of CS3's or CS7's output.

Two fixtures (CS3, CS5) plant a numeric property the catalog says the
"generator computes and records": the pre-trend slope (CS3) and the Lee bounds
endpoints (CS5). For those, this module computes the value from the data it
just generated and writes it into a ground-truth file *outside* the fixture
directory the scenario prompt names, so a compliant agent reading only the
named fixture directory never sees it. `validate_cs3.py` / `validate_cs5.py`
each reimplement the computation independently and check it against the
recorded value, rather than trusting this module's arithmetic.

Run from the repo root:

    uv run skills/causal-identification-review/tests/fixtures/generate.py
"""

from __future__ import annotations

import csv
import math
import random
from datetime import date, timedelta
from pathlib import Path

HERE = Path(__file__).parent

# ---------------------------------------------------------------------------
# CS3 -- review route: confounded rollout comparison
# ---------------------------------------------------------------------------

CS3_OUTDIR = HERE / "cs3-rollout"
CS3_GROUND_TRUTH = HERE / "cs3-rollout-ground-truth.md"
CS3_SEED = 20260301

CS3_PRE_START = date(2026, 2, 1)
CS3_CUTOVER = date(2026, 3, 15)
CS3_POST_END = date(2026, 4, 11)
"""Pre-period: 2026-02-01..2026-03-14 (42 days, 6 weeks) >= the catalog's 4-week
floor. Post-period: 2026-03-15..2026-04-11 (28 days, 4 weeks) >= the catalog's
2-week floor."""

CS3_EAST_BASE = 180.0
CS3_WEST_PRE_START = 208.0
CS3_WEST_PRE_END = 186.0
"""West's pre-period completion time falls linearly from 208s to 186s across
the 42 pre-period days -- the planted differential pre-trend, attributed in
`ux_cleanup_note.md` to a concurrent UX cleanup unrelated to the checkout
flow. West stays distinctly above East throughout the pre-period (208..186
vs a flat 180), consistent with the stated targeting criterion (West had the
worst checkout experience); `validate_cs3.py`'s baseline-level trap checks
the pre-period mean margin directly."""

CS3_WEST_POST_LEVEL = 145.0
"""West's post-cutover completion time -- the real (if confounded) drop the
team wants credited to the flow."""

CS3_NOISE_SIGMA = 3.0

CS3_WEST_AOV_PRE = 45.0
CS3_WEST_AOV_POST = 54.0
CS3_EAST_AOV = 45.0
CS3_AOV_NOISE_SIGMA = 1.5
"""avg_order_value: flat at $45 everywhere except West after the cutover,
where the concurrent promotion lifts it to ~$54. East never moves."""

CS3_WEST_VOLUME = 600
CS3_EAST_VOLUME = 550
CS3_VOLUME_NOISE = 40

CS3_WEST_COMPLAINTS = 184
CS3_EAST_COMPLAINTS = 97
"""Cart-abandonment complaint counts, quarter before rollout -- the stated
selection-into-exposure criterion. West is highest by construction (it is the
only region with a rollout)."""


def _cs3_daily_rows(rng: random.Random) -> list[dict]:
    rows: list[dict] = []
    day_count = (CS3_POST_END - CS3_PRE_START).days + 1
    for offset in range(day_count):
        day = CS3_PRE_START + timedelta(days=offset)
        is_post = day >= CS3_CUTOVER
        pre_index = (day - CS3_PRE_START).days
        pre_days = (CS3_CUTOVER - CS3_PRE_START).days

        # East: flat throughout, no rollout, no promotion.
        east_completion = CS3_EAST_BASE + rng.gauss(0.0, CS3_NOISE_SIGMA)
        east_aov = CS3_EAST_AOV + rng.gauss(0.0, CS3_AOV_NOISE_SIGMA)
        east_volume = max(1, round(CS3_EAST_VOLUME + rng.gauss(0.0, CS3_VOLUME_NOISE)))

        # West: falling pre-trend, then a level shift at cutover.
        if is_post:
            west_completion = CS3_WEST_POST_LEVEL + rng.gauss(0.0, CS3_NOISE_SIGMA)
            west_aov = CS3_WEST_AOV_POST + rng.gauss(0.0, CS3_AOV_NOISE_SIGMA)
        else:
            frac = pre_index / (pre_days - 1)
            trend_level = CS3_WEST_PRE_START + (CS3_WEST_PRE_END - CS3_WEST_PRE_START) * frac
            west_completion = trend_level + rng.gauss(0.0, CS3_NOISE_SIGMA)
            west_aov = CS3_WEST_AOV_PRE + rng.gauss(0.0, CS3_AOV_NOISE_SIGMA)
        west_volume = max(1, round(CS3_WEST_VOLUME + rng.gauss(0.0, CS3_VOLUME_NOISE)))

        rows.append(
            {
                "date": day.isoformat(),
                "region": "East",
                "completion_time_seconds": round(east_completion, 2),
                "avg_order_value": round(east_aov, 2),
                "volume": east_volume,
            }
        )
        rows.append(
            {
                "date": day.isoformat(),
                "region": "West",
                "completion_time_seconds": round(west_completion, 2),
                "avg_order_value": round(west_aov, 2),
                "volume": west_volume,
            }
        )
    return rows


def _ols_slope(xs: list[float], ys: list[float]) -> float:
    """Ordinary least-squares slope of y on x. No numpy -- deps stay empty."""
    n = len(xs)
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    cov = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys, strict=True))
    var = sum((x - mean_x) ** 2 for x in xs)
    return cov / var


def cs3_pre_means(rows: list[dict]) -> tuple[float, float]:
    """West and East pre-period completion-time means (seconds)."""
    west_pre = [
        r["completion_time_seconds"]
        for r in rows
        if r["region"] == "West" and r["date"] < CS3_CUTOVER.isoformat()
    ]
    east_pre = [
        r["completion_time_seconds"]
        for r in rows
        if r["region"] == "East" and r["date"] < CS3_CUTOVER.isoformat()
    ]
    return sum(west_pre) / len(west_pre), sum(east_pre) / len(east_pre)


def cs3_pre_slopes(rows: list[dict]) -> tuple[float, float]:
    """West and East pre-period completion-time slopes (seconds/day)."""
    west_pre = [r for r in rows if r["region"] == "West" and r["date"] < CS3_CUTOVER.isoformat()]
    east_pre = [r for r in rows if r["region"] == "East" and r["date"] < CS3_CUTOVER.isoformat()]
    west_pre.sort(key=lambda r: r["date"])
    east_pre.sort(key=lambda r: r["date"])
    west_slope = _ols_slope(
        list(range(len(west_pre))), [r["completion_time_seconds"] for r in west_pre]
    )
    east_slope = _ols_slope(
        list(range(len(east_pre))), [r["completion_time_seconds"] for r in east_pre]
    )
    return west_slope, east_slope


def build_cs3(outdir: Path, ground_truth_path: Path) -> None:
    rng = random.Random(CS3_SEED)
    rows = _cs3_daily_rows(rng)

    outdir.mkdir(parents=True, exist_ok=True)
    fields = ("date", "region", "completion_time_seconds", "avg_order_value", "volume")
    with (outdir / "daily.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    (outdir / "promotions.log").write_text(
        "2026-03-15 West region-wide price promotion launched.\n"
        "The promotion stacks a checkout discount on top of the existing "
        "loyalty discount, which is why average order value rises in West "
        "starting the same week as the checkout-flow rollout.\n"
        "No promotion activity is recorded in East during this period.\n",
        encoding="utf-8",
    )

    (outdir / "targeting_note.md").write_text(
        "# Rollout targeting note\n"
        "\n"
        "West was selected for the checkout-flow rollout because it had the "
        "highest cart-abandonment complaint volume of any region in the "
        "quarter before rollout.\n"
        "\n"
        "Cart-abandonment complaint counts, quarter before rollout "
        "(2025-11-01 through 2026-01-31):\n"
        "\n"
        f"- West: {CS3_WEST_COMPLAINTS}\n"
        f"- East: {CS3_EAST_COMPLAINTS}\n",
        encoding="utf-8",
    )

    (outdir / "ux_cleanup_note.md").write_text(
        "# Concurrent UX cleanup\n"
        "\n"
        "A separate, unrelated UX cleanup (form-field reordering on the "
        "shipping step) shipped to West gradually across the pre-rollout "
        "weeks and continued improving completion time in West through the "
        "whole pre-period, ahead of and independent of the checkout-flow "
        "rollout.\n"
        "East did not receive this cleanup.\n",
        encoding="utf-8",
    )

    (outdir / "data_notes.md").write_text(
        "# Data notes\n"
        "\n"
        "This extract is complete for both regions across the full window "
        "(2026-02-01 through 2026-04-11): every region has exactly one row "
        "per calendar day, with no missing daily records.\n",
        encoding="utf-8",
    )

    west_slope, east_slope = cs3_pre_slopes(rows)
    west_pre_mean, east_pre_mean = cs3_pre_means(rows)
    ground_truth_path.write_text(
        "# cs3-rollout ground truth\n"
        "\n"
        "Not part of the fixture directory handed to arms -- generated here "
        "so `validate_cs3.py` can check its own independent recomputation "
        "against a value fixed at generation time, per "
        "`skills/causal-identification-review/tests/scenarios.md` CS3.\n"
        "\n"
        "## Planted pre-trend (computed from the generated data)\n"
        "\n"
        f"- West pre-period completion-time slope: {west_slope:.6f} s/day "
        "(falling).\n"
        f"- East pre-period completion-time slope: {east_slope:.6f} s/day "
        "(flat).\n"
        "\n"
        "## Planted baseline level (computed from the generated data)\n"
        "\n"
        f"- West pre-period completion-time mean: {west_pre_mean:.6f} s.\n"
        f"- East pre-period completion-time mean: {east_pre_mean:.6f} s.\n"
        f"- West-minus-East pre-period level margin: "
        f"{west_pre_mean - east_pre_mean:.6f} s (West slower, consistent "
        "with the stated targeting criterion).\n"
        "\n"
        "## Documented ground-truth disposition\n"
        "\n"
        "Both designs the review can construct from this fixture end on "
        "`assumption-contradicted`:\n"
        "\n"
        "- The West-only before/after design's implicit no-confounding-events "
        "assumption is falsified by the concurrent price promotion "
        "(`promotions.log`, and the `avg_order_value` shift in West with no "
        "matching shift in East).\n"
        "- The West-vs-East difference-in-differences design's parallel-"
        "trends assumption is falsified by the planted differential "
        "pre-trend above.\n"
        "\n"
        "No design in this fixture reaches `identified-if` or `unresolved`. "
        "Synthetic control is infeasible by construction: the fixture holds "
        "exactly two regions, so there is no donor pool.\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# CS4 -- construct route: admissible-design matrix over a facts sheet
# ---------------------------------------------------------------------------

CS4_OUTDIR = HERE / "cs4-facts"

CS4_FACTS_MD = (
    "# Merchant-verification rollout: facts sheet\n"
    "\n"
    "There is no transaction-level dataset for this rollout -- only the facts below.\n"
    "Nothing here should be read as a hint toward the right design; it is the complete "
    "set of facts a review has to work with.\n"
    "\n"
    "## Eligibility cutoff\n"
    "\n"
    "Merchants with lifetime transaction volume of $50,000 or more are auto-enrolled "
    "in the new merchant-verification step.\n"
    "Merchants below $50,000 lifetime volume are not enrolled.\n"
    "The cutoff is a hard, enforced rule applied uniformly at enrollment time, not a "
    "guideline analysts can override.\n"
    "\n"
    "## Onboarding batch\n"
    "\n"
    "Enrollment is staged by which processor onboarding batch a merchant was assigned to.\n"
    "Batch order follows the processor's onboarding capacity and logistics schedule, "
    "which was fixed before the verification step existed and is stated to be "
    "independent of any merchant's chargeback history or risk profile.\n"
    "Merchants in an earlier batch reach their enrollment decision (and, if eligible, "
    "their verification start date) earlier than merchants in a later batch.\n"
    "\n"
    "## Pre-rollout chargeback history\n"
    "\n"
    "Pre-rollout chargeback history was not retained in this export.\n"
    "Only the 90 days following each merchant's own enrollment date exist in the data "
    "the fraud team can pull.\n"
    "There is no pre-period chargeback series for any merchant, enrolled or not.\n"
    "\n"
    "## Analyst discretion\n"
    "\n"
    'Risk analysts had discretion to fast-track "high-touch" merchants into '
    "verification early, within their assigned batch, on unrecorded judgment calls.\n"
    "Which merchants were fast-tracked, and why, was not logged anywhere the fraud "
    "team can retrieve.\n"
    "\n"
    "## Prospective option\n"
    "\n"
    "A prospective randomized experiment -- enrolling future new merchants into "
    "verification vs. not, going forward -- has not been ruled out and could be "
    "proposed.\n"
    "No design work of any kind has been done for it, and none is included here.\n"
)


def build_cs4(outdir: Path) -> None:
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "facts.md").write_text(CS4_FACTS_MD, encoding="utf-8")


# ---------------------------------------------------------------------------
# CS5 -- bound route: attrition bounds under stated monotonicity
# ---------------------------------------------------------------------------

CS5_OUTDIR = HERE / "cs5-bounds"
CS5_GROUND_TRUTH = HERE / "cs5-bounds-ground-truth.md"
CS5_SEED = 20260501

CS5_N_INVITED = 600
CS5_N_NONINVITED = 600
CS5_INVITED_ATTRITION = 0.12
CS5_NONINVITED_ATTRITION = 0.30
"""Invited customers churn (and so go unobserved) less often than
non-invited customers -- the direction the stated monotonicity assumption
licenses (invitation can only keep a customer observed longer)."""

CS5_P_RETAIN_INVITED_OBS = 0.62
CS5_P_RETAIN_NONINVITED_OBS = 0.55
"""Retention probability conditional on being observed. Deliberately
different by cohort -- the fixture's whole point is that this raw contrast
cannot be read as the program's effect."""


def _cs5_cohort(
    rng: random.Random, n: int, attrition: float, p_retain_obs: float, prefix: str
) -> list[dict]:
    rows = []
    for i in range(n):
        customer_id = f"{prefix}{i:04d}"
        missing = rng.random() < attrition
        if missing:
            rows.append({"customer_id": customer_id, "retained_30d": ""})
        else:
            retained = 1 if rng.random() < p_retain_obs else 0
            rows.append({"customer_id": customer_id, "retained_30d": str(retained)})
    return rows


CS5_ASSIGNMENT_NOTE = (
    "# Assignment and outcome-missingness notes\n"
    "\n"
    "## Assignment\n"
    "\n"
    "Invitations to the concierge onboarding call were randomized: within each monthly "
    "enrollment wave, invited customers were drawn by lottery from that wave's at-risk "
    "cohort.\n"
    "The randomization was implemented and logged by the platform team; nothing about a "
    "customer's history entered the draw.\n"
    "Randomization settles who was invited, but it does not identify the program's "
    "effect as a point here, because the 30-day outcome is differentially missing "
    "across the two cohorts (see below).\n"
    "\n"
    "## Monotonicity assumption\n"
    "\n"
    "The only licensed assumption about the missing 30-day outcomes is monotonicity of "
    "attrition: invitation can only keep a customer observed longer, never shorten the "
    "observation window.\n"
    "This direction is stated here as a fact of the fixture, not inferred from the data.\n"
    "\n"
    "## Why some outcomes are missing\n"
    "\n"
    "Some invited and some non-invited customers churned before their 30-day retention "
    "outcome could be observed.\n"
    "A blank `retained_30d` value means the customer churned before the 30-day window "
    "closed, not that the event was unrecorded or the export is incomplete.\n"
    "The missing-outcome rate differs between the two cohorts, so the observed "
    "difference in retention rates cannot be read as the program's effect.\n"
)


def build_cs5(outdir: Path, ground_truth_path: Path) -> None:
    rng = random.Random(CS5_SEED)
    invited_rows = _cs5_cohort(
        rng, CS5_N_INVITED, CS5_INVITED_ATTRITION, CS5_P_RETAIN_INVITED_OBS, "inv"
    )
    noninvited_rows = _cs5_cohort(
        rng, CS5_N_NONINVITED, CS5_NONINVITED_ATTRITION, CS5_P_RETAIN_NONINVITED_OBS, "non"
    )

    outdir.mkdir(parents=True, exist_ok=True)
    fields = ("customer_id", "cohort", "retained_30d")
    with (outdir / "outcomes.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        for row in invited_rows:
            writer.writerow({**row, "cohort": "invited"})
        for row in noninvited_rows:
            writer.writerow({**row, "cohort": "non_invited"})

    (outdir / "assignment_note.md").write_text(CS5_ASSIGNMENT_NOTE, encoding="utf-8")

    treated_observed = [int(r["retained_30d"]) for r in invited_rows if r["retained_30d"] != ""]
    control_observed = [int(r["retained_30d"]) for r in noninvited_rows if r["retained_30d"] != ""]
    lower, upper = cs5_lee_bounds(
        treated_observed, control_observed, CS5_N_INVITED, CS5_N_NONINVITED
    )

    ground_truth_path.write_text(
        "# cs5-bounds ground truth\n"
        "\n"
        "Not part of the fixture directory handed to arms -- generated here "
        "so `validate_cs5.py` can check its own independent recomputation "
        "against a value fixed at generation time, per "
        "`skills/causal-identification-review/tests/scenarios.md` CS5.\n"
        "\n"
        "## Lee (2009) trimming bounds (computed from the generated data)\n"
        "\n"
        f"- lower: {lower:.6f}\n"
        f"- upper: {upper:.6f}\n"
        "\n"
        "Computed by trimming the invited cohort's observed "
        "`retained_30d` distribution (the lower-attrition cohort) down to "
        "the non-invited cohort's survival rate -- from the bottom, which "
        "keeps the highest outcomes and gives the upper endpoint, and from "
        "the top, which keeps the lowest outcomes and gives the lower "
        "endpoint -- then subtracting the non-invited cohort's observed "
        "mean.\n",
        encoding="utf-8",
    )


def cs5_lee_bounds(
    treated_observed: list[int], control_observed: list[int], n_treated: int, n_control: int
) -> tuple[float, float]:
    """Lee (2009) trimming bounds, computed at generation time and recorded
    in `cs5-bounds-ground-truth.md`.

    `validate_cs5.py` reimplements this independently rather than importing
    it, so a bug shared by both implementations is the only way this check
    could pass on broken data.
    """
    s1 = len(treated_observed) / n_treated
    s0 = len(control_observed) / n_control
    control_mean = sum(control_observed) / len(control_observed)

    if s1 >= s0:
        trim_frac = (s1 - s0) / s1
        pool = sorted(treated_observed)
        n_trim = round(trim_frac * len(pool))
        kept_for_upper = pool[n_trim:] if n_trim else pool
        kept_for_lower = pool[: len(pool) - n_trim] if n_trim else pool
        upper = (sum(kept_for_upper) / len(kept_for_upper)) - control_mean
        lower = (sum(kept_for_lower) / len(kept_for_lower)) - control_mean
    else:
        # Symmetric case: trim the control (lower-attrition-here) cohort
        # instead. Not exercised by the committed fixture (invited has
        # lower attrition by construction) but kept for completeness.
        trim_frac = (s0 - s1) / s0
        pool = sorted(control_observed)
        n_trim = round(trim_frac * len(pool))
        kept_for_upper = pool[: len(pool) - n_trim] if n_trim else pool
        kept_for_lower = pool[n_trim:] if n_trim else pool
        treated_mean = sum(treated_observed) / len(treated_observed)
        upper = treated_mean - (sum(kept_for_lower) / len(kept_for_lower))
        lower = treated_mean - (sum(kept_for_upper) / len(kept_for_upper))

    return (min(lower, upper), max(lower, upper))


# ---------------------------------------------------------------------------
# CS7 -- handoff seam: a design whose assumptions clear their probes
# ---------------------------------------------------------------------------

CS7_OUTDIR = HERE / "cs7-seam"
CS7_GROUND_TRUTH = HERE / "cs7-seam-ground-truth.md"
CS7_SEED = 20260701

CS7_N_ACCOUNTS = 6000
CS7_CUTOFF = 680
CS7_SCORE_MEAN = 650.0
CS7_SCORE_SD = 70.0
CS7_SCORE_MIN, CS7_SCORE_MAX = 300, 900

CS7_TENURE_INTERCEPT = 12.0
CS7_TENURE_SLOPE = 0.05
CS7_TENURE_NOISE_SD = 6.0

CS7_INCOME_INTERCEPT = 40000.0
CS7_INCOME_SLOPE = 60.0
CS7_INCOME_NOISE_SD = 4000.0

CS7_DEFAULT_BASE = 0.30
CS7_DEFAULT_SCORE_SLOPE = 0.00035
CS7_DEFAULT_FLOOR = 0.03
CS7_DEFAULT_CEILING = 0.50
CS7_TREATMENT_EFFECT = 0.06
"""The true local effect of eligibility on 90-day default rate at the
cutoff: eligible accounts default 6pp less often than the smooth baseline
their score alone would predict."""

CS7_ESTIMAND = (
    "the local average effect of instant-checkout eligibility on 90-day "
    "default rate at the credit-score-680 discontinuity"
)
"""`accounts.csv` carries `eligible` only -- no treatment-receipt column --
so the estimand is eligibility's effect (a sharp-RD claim), not use's, which
would need receipt data and fuzzy-RD assumptions. An earlier wording added
"for accounts within the fixture's bandwidth of the cutoff", but no
arm-visible file defines a bandwidth (the validator's bandwidths are not
arm-readable under the contamination rule), so the clause was dropped
(2026-08-09) -- locality is already carried by "at the discontinuity"."""


def _cs7_default_probability(score: int, eligible: bool) -> float:
    p = CS7_DEFAULT_BASE - CS7_DEFAULT_SCORE_SLOPE * (score - 500)
    if eligible:
        p -= CS7_TREATMENT_EFFECT
    return min(CS7_DEFAULT_CEILING, max(CS7_DEFAULT_FLOOR, p))


def _cs7_rows(rng: random.Random) -> list[dict]:
    rows = []
    for i in range(CS7_N_ACCOUNTS):
        score = round(rng.gauss(CS7_SCORE_MEAN, CS7_SCORE_SD))
        score = min(CS7_SCORE_MAX, max(CS7_SCORE_MIN, score))
        eligible = score >= CS7_CUTOFF

        tenure = (
            CS7_TENURE_INTERCEPT
            + CS7_TENURE_SLOPE * (score - 650)
            + rng.gauss(0.0, CS7_TENURE_NOISE_SD)
        )
        tenure = max(0.0, tenure)

        income = (
            CS7_INCOME_INTERCEPT
            + CS7_INCOME_SLOPE * (score - 650)
            + rng.gauss(0.0, CS7_INCOME_NOISE_SD)
        )
        income = max(0.0, income)

        p_default = _cs7_default_probability(score, eligible)
        default_90d = 1 if rng.random() < p_default else 0

        rows.append(
            {
                "account_id": f"acc{i:05d}",
                "credit_score": score,
                "eligible": "true" if eligible else "false",
                "account_tenure_months": round(tenure, 2),
                "income": round(income, 2),
                "default_90d": default_90d,
            }
        )
    return rows


def build_cs7(outdir: Path, ground_truth_path: Path) -> None:
    rng = random.Random(CS7_SEED)
    rows = _cs7_rows(rng)

    outdir.mkdir(parents=True, exist_ok=True)
    fields = (
        "account_id",
        "credit_score",
        "eligible",
        "account_tenure_months",
        "income",
        "default_90d",
    )
    with (outdir / "accounts.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)

    (outdir / "data_notes.md").write_text(
        "# Data notes\n"
        "\n"
        "Accounts with a credit score of 680 or higher are auto-approved "
        "for instant-checkout; accounts below 680 go through manual review "
        "and are not offered it.\n"
        "The 680 threshold gates instant-checkout eligibility only: no "
        "other product, pricing, underwriting, or policy rule in effect "
        "during the observation window keys on credit score at or near "
        "680.\n"
        "This extract is complete: every account in the export has a "
        "credit score, an eligibility flag, tenure, income, and a 90-day "
        "default outcome, with no missing account records, and the "
        "extract is complete for all accounts within the credit-score "
        "range the export spans.\n",
        encoding="utf-8",
    )

    ground_truth_path.write_text(
        "# cs7-seam ground truth\n"
        "\n"
        "Not part of the fixture directory handed to arms -- kept here so "
        "stage 1's record can be checked against a precommitted estimand, "
        "per `skills/causal-identification-review/tests/scenarios.md` CS7.\n"
        "\n"
        "## Precommitted estimand\n"
        "\n"
        f"> {CS7_ESTIMAND}\n"
        "\n"
        "Stage 1's record must state this estimand in matching terms for "
        "stage 2 to reuse verbatim.\n"
        "\n"
        "## Design ground truth\n"
        "\n"
        "- No manipulation at the cutoff: the running variable's density is "
        "smooth through 680 by construction.\n"
        "- Covariate balance at the cutoff: `account_tenure_months` and "
        "`income` are continuous functions of `credit_score` alone (no "
        "jump at 680), so they are balanced immediately around the "
        "cutoff.\n"
        "- No other stated confound at the cutoff: unlike CS3/CS4, this "
        "fixture plants no concurrent change, no differential pre-trend, "
        "and no selection story.\n"
        f"- Planted local treatment effect: eligible accounts default "
        f"{CS7_TREATMENT_EFFECT * 100:.0f}pp less often than the smooth "
        "score-only baseline predicts, so the discontinuity is a real, "
        "non-flat signal.\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------
# CS8 -- untestable assumption: randomized encouragement, silent placebo
# ---------------------------------------------------------------------------

CS8_OUTDIR = HERE / "cs8-encouragement"
CS8_GROUND_TRUTH = HERE / "cs8-encouragement-ground-truth.md"
CS8_SEED = 20260802

CS8_N_CUSTOMERS = 6000
CS8_N_INVITED = 3000
CS8_INVITE_DATE = date(2026, 3, 2)

CS8_P_ALWAYS_TAKER = 0.15
CS8_P_COMPLIER = 0.30
"""Latent compliance types, drawn independently of `invited`: always-takers
enroll whatever happens, compliers enroll only if invited, and the remaining
55% never enroll. There are no defiers by construction -- a fact no shipped
file can show, which is why monotonicity stays untestable."""

CS8_RATE_MEAN = {"always": 0.5, "complier": 1.0, "never": 1.3}
CS8_RATE_SHAPE = 4.0
"""Each customer's 90-day late-payment rate is gamma-distributed around a
mean that depends on compliance type. Always-takers run well below
never-takers (self-selection into autopay), so enrollment is genuinely
confounded and only the invitation contrast is usable."""

CS8_AUTOPAY_MULTIPLIER = 0.45
"""Enrollment multiplies a customer's post-period rate by this factor. It is
the *only* path from `invited` to `late_payments_90d` in this generator: the
email itself does nothing. Nothing arm-visible says so, which is the point."""

CS8_PLANS = ("basic", "standard", "premium")
CS8_PLAN_WEIGHTS = (0.50, 0.35, 0.15)
CS8_TENURE_MIN, CS8_TENURE_MAX = 1, 120
"""`plan` and `tenure_months` are drawn independently of `invited`, of
compliance type, and of the lateness rate -- pure balance covariates."""

CS8_FIELDS = (
    "customer_id",
    "invited",
    "late_payments_prior_90d",
    "late_payments_90d",
    "tenure_months",
    "plan",
)
"""`customers.csv` carries no enrollment column. The latent types still drive
enrollment and the outcome, but enrollment ships only as counts by arm
(`enrollment_by_arm.csv`): with a customer-level field the joint distribution
of invitation, enrollment, and outcome is observable, and the instrument's
inequality restrictions become a real, if weak, test of exclusion and
monotonicity -- which this fixture exists to withhold."""

CS8_ENROLLMENT_FIELDS = ("invited", "customers", "enrolled_by_2026_03_16")

CS8_ESTIMAND = (
    "the average effect of autopay enrollment on 90-day late-payment count "
    "among customers whose enrollment the invitation changes (compliers)"
)
"""A complier-local estimand: the Wald ratio identifies nothing broader, and
only under exclusion and monotonicity, which the disposition carries by
name."""

CS8_OVERREAD = "confirms the instrument is clean"
"""The planted overread in `design_note.md`: a prior-period placebo is
balanced by randomization alone whatever the email does after it is sent, so
its silence says nothing about exclusion."""

CS8_DESIGN_NOTE = (
    "# Autopay invitation: design note\n"
    "\n"
    "We want the effect of autopay enrollment on late payments in the 90 days after the "
    "enrollment window closed.\n"
    "Invitations were assigned by a seeded random number generator over the full customer "
    "list on 2026-03-02, before any outcome in the 90-day window was observed.\n"
    "3000 of 6000 customers were invited.\n"
    "Every invited customer received the same email, quoted here in full.\n"
    "\n"
    "> Subject: Set up autopay in two minutes\n"
    ">\n"
    "> You can now set up autopay from your online account.\n"
    "> Sign in, open Billing, choose Autopay, and pick the card or bank account you want "
    "to use.\n"
    "> You can turn autopay off again from the same page at any time.\n"
    "\n"
    "Enrollment was voluntary and cannot be linked to payment history at the customer level, "
    "so we use the invitation as an instrument for enrollment: the estimate is the "
    "difference in late payments by invitation divided by the difference in enrollment "
    "rates by invitation.\n"
    "As a placebo check we regressed late payments in the 90 days before the invitation on "
    f"the invitation flag and found no effect, which {CS8_OVERREAD}, so the IV estimate is "
    "the causal effect of autopay.\n"
)

CS8_DATA_NOTES = (
    "# Data notes\n"
    "\n"
    "This extract is complete: it holds every customer on the list as of 2026-03-02, with "
    "no missing rows, and every field is populated.\n"
    "Every customer in the extract was eligible for autopay throughout the window.\n"
    "Customers could enroll in autopay with or without an invitation.\n"
    "Enrollment is held in the billing system.\n"
    "This extract carries it only as counts by invitation arm in `enrollment_by_arm.csv`, "
    "as of 2026-03-16, when the enrollment window closed.\n"
    "Enrollment was fixed on 2026-03-16: no customer enrolled in or left autopay between "
    "2026-03-16 and the end of the outcome window.\n"
    "Privacy rules bar linking a customer's enrollment status to their payment history, so "
    "no customer-level enrollment field exists in this extract or can be requested for it.\n"
    "`late_payments_prior_90d` counts late payments in the 90 days before 2026-03-02, and "
    "`late_payments_90d` counts them in the 90 days after 2026-03-16.\n"
    "No record exists of who opened the email.\n"
)


def _poisson(rng: random.Random, rate: float) -> int:
    """Knuth's multiplication algorithm. Fine at the rates used here (well
    under 10); no numpy -- deps stay empty."""
    threshold = math.exp(-rate)
    count = 0
    product = rng.random()
    while product > threshold:
        count += 1
        product *= rng.random()
    return count


def _cs8_rows(rng: random.Random) -> list[dict]:
    # True randomization: shuffle a list holding exactly CS8_N_INVITED ones
    # before any customer attribute is drawn.
    invited_flags = [1] * CS8_N_INVITED + [0] * (CS8_N_CUSTOMERS - CS8_N_INVITED)
    rng.shuffle(invited_flags)

    rows = []
    for i, invited in enumerate(invited_flags):
        draw = rng.random()
        if draw < CS8_P_ALWAYS_TAKER:
            kind = "always"
        elif draw < CS8_P_ALWAYS_TAKER + CS8_P_COMPLIER:
            kind = "complier"
        else:
            kind = "never"
        enrolled = 1 if kind == "always" or (kind == "complier" and invited) else 0

        rate = rng.gammavariate(CS8_RATE_SHAPE, CS8_RATE_MEAN[kind] / CS8_RATE_SHAPE)
        prior = _poisson(rng, rate)
        # No `invited` term here: the invitation reaches the outcome through
        # enrollment alone. `enrolled_autopay` stays on the in-memory row for
        # the by-arm counts; build_cs8 never writes it per customer.
        post = _poisson(rng, rate * CS8_AUTOPAY_MULTIPLIER if enrolled else rate)

        tenure = rng.randint(CS8_TENURE_MIN, CS8_TENURE_MAX)
        plan = rng.choices(CS8_PLANS, weights=CS8_PLAN_WEIGHTS)[0]

        rows.append(
            {
                "customer_id": f"cust{i:05d}",
                "invited": invited,
                "enrolled_autopay": enrolled,
                "late_payments_prior_90d": prior,
                "late_payments_90d": post,
                "tenure_months": tenure,
                "plan": plan,
            }
        )
    return rows


def _mean_var(values: list[float]) -> tuple[float, float]:
    """Mean and sample (n-1) variance."""
    n = len(values)
    mean = sum(values) / n
    return mean, sum((v - mean) ** 2 for v in values) / (n - 1)


def _two_proportion_contrast(hits_t: int, n_t: int, hits_c: int, n_c: int) -> dict:
    """Difference in proportions (treated minus control) from counts alone,
    with its binomial standard error, z, and 95% interval."""
    p_t, p_c = hits_t / n_t, hits_c / n_c
    diff = p_t - p_c
    se = math.sqrt(p_t * (1 - p_t) / n_t + p_c * (1 - p_c) / n_c)
    return {
        "treated": p_t,
        "control": p_c,
        "diff": diff,
        "se": se,
        "z": diff / se,
        "lo": diff - 1.96 * se,
        "hi": diff + 1.96 * se,
    }


def cs8_enrollment_by_arm(rows: list[dict]) -> list[dict]:
    """The only form in which enrollment ships: one row per invitation arm."""
    return [
        {
            "invited": arm,
            "customers": sum(1 for r in rows if r["invited"] == arm),
            "enrolled_by_2026_03_16": sum(
                r["enrolled_autopay"] for r in rows if r["invited"] == arm
            ),
        }
        for arm in (0, 1)
    ]


def _two_group_contrast(treated: list[float], control: list[float]) -> dict:
    """Difference in means (treated minus control) with its unpooled standard
    error, z, 95% interval, and standardized difference (pooled-SD scale)."""
    mean_t, var_t = _mean_var(treated)
    mean_c, var_c = _mean_var(control)
    diff = mean_t - mean_c
    se = math.sqrt(var_t / len(treated) + var_c / len(control))
    return {
        "treated": mean_t,
        "control": mean_c,
        "diff": diff,
        "se": se,
        "z": diff / se,
        "lo": diff - 1.96 * se,
        "hi": diff + 1.96 * se,
        "smd": diff / math.sqrt((var_t + var_c) / 2),
    }


def cs8_outcome_tv(rows: list[dict]) -> float:
    """Total-variation distance between the two arms' `late_payments_90d`
    distributions -- bounded by the first-stage difference if independence,
    exclusion, and monotonicity all hold, the one observable implication the
    extract leaves, and an implication of the three together."""
    arms = {z: [r["late_payments_90d"] for r in rows if r["invited"] == z] for z in (0, 1)}
    support = set(arms[0]) | set(arms[1])
    return 0.5 * sum(
        abs(arms[1].count(y) / len(arms[1]) - arms[0].count(y) / len(arms[0])) for y in support
    )


def cs8_stats(rows: list[dict]) -> dict[str, dict]:
    """Every realized number `cs8-encouragement-ground-truth.md` records.

    `validate_cs8.py` reimplements these independently rather than importing
    them, following `cs5_lee_bounds`.
    """
    invited = [r for r in rows if r["invited"] == 1]
    control = [r for r in rows if r["invited"] == 0]
    arm_not, arm_invited = cs8_enrollment_by_arm(rows)

    def by_invited(value) -> dict:
        return _two_group_contrast([value(r) for r in invited], [value(r) for r in control])

    stats = {
        # From the by-arm counts, the way an arm has to compute it.
        "first_stage": _two_proportion_contrast(
            arm_invited["enrolled_by_2026_03_16"],
            arm_invited["customers"],
            arm_not["enrolled_by_2026_03_16"],
            arm_not["customers"],
        ),
        "prior": by_invited(lambda r: r["late_payments_prior_90d"]),
        "tenure": by_invited(lambda r: r["tenure_months"]),
        "itt": by_invited(lambda r: r["late_payments_90d"]),
    }
    for plan in CS8_PLANS:
        stats[f"plan_{plan}"] = by_invited(lambda r, plan=plan: 1 if r["plan"] == plan else 0)
    return stats


def build_cs8(outdir: Path, ground_truth_path: Path) -> None:
    rng = random.Random(CS8_SEED)
    rows = _cs8_rows(rng)

    outdir.mkdir(parents=True, exist_ok=True)
    with (outdir / "customers.csv").open("w", newline="", encoding="utf-8") as handle:
        # extrasaction="ignore" drops the in-memory `enrolled_autopay` key.
        writer = csv.DictWriter(
            handle, fieldnames=CS8_FIELDS, lineterminator="\n", extrasaction="ignore"
        )
        writer.writeheader()
        writer.writerows(rows)

    with (outdir / "enrollment_by_arm.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=CS8_ENROLLMENT_FIELDS, lineterminator="\n")
        writer.writeheader()
        writer.writerows(cs8_enrollment_by_arm(rows))

    (outdir / "design_note.md").write_text(CS8_DESIGN_NOTE, encoding="utf-8")
    (outdir / "data_notes.md").write_text(CS8_DATA_NOTES, encoding="utf-8")

    stats = cs8_stats(rows)
    first, prior, tenure = stats["first_stage"], stats["prior"], stats["tenure"]
    itt = stats["itt"]
    wald = itt["diff"] / first["diff"]
    outcome_tv = cs8_outcome_tv(rows)
    plan_lines = "".join(
        f"- `plan` share `{plan}`: invited {stats[f'plan_{plan}']['treated']:.4f}, "
        f"not invited {stats[f'plan_{plan}']['control']:.4f}, "
        f"standardized difference {stats[f'plan_{plan}']['smd']:+.4f}.\n"
        for plan in CS8_PLANS
    )

    ground_truth_path.write_text(
        "# cs8-encouragement ground truth\n"
        "\n"
        "Not part of the fixture directory handed to arms -- generated here so "
        "`validate_cs8.py` can check the realized design against numbers fixed at "
        "generation time.\n"
        "Every number below is computed from the generated data.\n"
        "\n"
        "## Precommitted estimand\n"
        "\n"
        f"> {CS8_ESTIMAND}\n"
        "\n"
        "## Realized first stage (from the by-arm counts)\n"
        "\n"
        f"- Enrollment rate, invited: {first['treated']:.4f}.\n"
        f"- Enrollment rate, not invited: {first['control']:.4f}.\n"
        f"- Difference: {first['diff']:.4f} (z = {first['z']:.2f}, 95% interval "
        f"{first['lo']:.4f} to {first['hi']:.4f}).\n"
        "\n"
        "## Realized balance by `invited`\n"
        "\n"
        f"- `late_payments_prior_90d` mean: invited {prior['treated']:.4f}, not invited "
        f"{prior['control']:.4f}, difference {prior['diff']:+.4f} (95% interval "
        f"{prior['lo']:+.4f} to {prior['hi']:+.4f}), standardized difference "
        f"{prior['smd']:+.4f}.\n"
        f"- `tenure_months` mean: invited {tenure['treated']:.4f}, not invited "
        f"{tenure['control']:.4f}, standardized difference {tenure['smd']:+.4f}.\n"
        f"{plan_lines}"
        "\n"
        "## Realized contrasts in `late_payments_90d`\n"
        "\n"
        f"- Intent-to-treat difference (invited minus not invited): {itt['diff']:+.4f} "
        f"(z = {itt['z']:.2f}, 95% interval {itt['lo']:+.4f} to {itt['hi']:+.4f}).\n"
        f"- Wald ratio (intent-to-treat difference over first-stage difference): {wald:+.4f}.\n"
        "\n"
        "## Ground-truth assessment of each assumption\n"
        "\n"
        "- Relevance: probed by the first stage from `enrollment_by_arm.csv`, not "
        "contradicted.\n"
        "- Independence: randomization is stated and quoted, and balance on prior late "
        "payments, tenure, and plan came back clean: not contradicted.\n"
        "- Exclusion: one weak joint bound, and nothing else.\n"
        "  If the invitation is independent of outcomes, reaches late payments only through "
        "enrollment, and moves no customer's enrollment the wrong way, the two arms' outcome "
        "distributions can differ only among customers whose enrollment it moves, so their "
        "total-variation distance cannot exceed the first-stage difference.\n"
        "  The bound follows from independence, exclusion, and monotonicity together, not from "
        "exclusion alone; a record that uses it says so.\n"
        f"  The distance is {outcome_tv:.4f} against a first-stage difference of "
        f"{first['diff']:.4f}, so the bound holds, and with that much slack it could be "
        "broken only by a large violation of one of the three: a direct effect of the email "
        "on a large share of customers, say, or a large share whose enrollment it moves the "
        "wrong way.\n"
        "  Enrollment exists only as counts by arm, so the joint distribution of invitation, "
        "enrollment, and outcome -- which the instrument's inequality restrictions need -- "
        "cannot be formed.\n"
        "  Every customer was eligible, so no subgroup exists in which the invitation cannot "
        "move enrollment.\n"
        "  Whether a customer opened the email is unrecorded.\n"
        "  The prior-period placebo is balanced by randomization alone whatever the email "
        "does after it is sent, so it is silent on exclusion.\n"
        "  A customer-level enrollment field, or a randomized arm sent an email with no "
        "enrollment content, would make it testable in earnest.\n"
        "  Two records are therefore sound: not contradicted by that bound, with its blind "
        "spot named; or not testable here, with the placebo named as a check considered and "
        "the reason it is silent.\n"
        "  Both are sound because the untestable value is the review's own finding, not a "
        "fact about the extract: a review that names the bound owes it as a probe, and a "
        "review that does not name it records what it did consider, which is what a reader "
        "contests.\n"
        "  This file names the bound so a scorer can recognize it, not so an arm must.\n"
        "  A review is not required to know the bound; it is required not to mistake the "
        "placebo, the balance checks, or the first stage for a probe of exclusion.\n"
        "- Monotonicity: defiers are unobservable, and without customer-level enrollment the "
        "inequality restrictions that could expose a large share of them cannot be formed.\n"
        "  Its only observable implication is the sign of the first stage, which is positive; "
        "the same two records are sound, for the same reason.\n"
        "  A review that writes the sign "
        "down as something monotonicity implies has named the implication and owes the row; "
        "one that reports the first stage for relevance and says defiers are unobservable has "
        "not, and its untestable row stands.\n"
        "\n"
        "## Documented ground-truth disposition\n"
        "\n"
        "`identified-if`, conditional on exclusion and monotonicity, each carried by name.\n"
        f'The design note\'s claim that the silent placebo "{CS8_OVERREAD}" is the planted '
        "overread: a review that repeats it, or that drops either condition, has lost the "
        "scenario.\n",
        encoding="utf-8",
    )


# ---------------------------------------------------------------------------


def main() -> None:
    build_cs3(CS3_OUTDIR, CS3_GROUND_TRUTH)
    build_cs4(CS4_OUTDIR)
    build_cs5(CS5_OUTDIR, CS5_GROUND_TRUTH)
    build_cs7(CS7_OUTDIR, CS7_GROUND_TRUTH)
    build_cs8(CS8_OUTDIR, CS8_GROUND_TRUTH)


if __name__ == "__main__":
    main()
