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
        "the non-invited cohort's survival rate, from the bottom "
        "(lower endpoint) and from the top (upper endpoint), then "
        "subtracting the non-invited cohort's observed mean.\n",
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
    "default rate at the credit-score-680 discontinuity, for accounts "
    "within the fixture's bandwidth of the cutoff"
)
"""`accounts.csv` carries `eligible` only -- no treatment-receipt column --
so the estimand is eligibility's effect (a sharp-RD claim), not use's, which
would need receipt data and fuzzy-RD assumptions."""


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
        "This extract is complete: every account in the export has a "
        "credit score, an eligibility flag, tenure, income, and a 90-day "
        "default outcome, with no missing account records.\n",
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


def main() -> None:
    build_cs3(CS3_OUTDIR, CS3_GROUND_TRUTH)
    build_cs4(CS4_OUTDIR)
    build_cs5(CS5_OUTDIR, CS5_GROUND_TRUTH)
    build_cs7(CS7_OUTDIR, CS7_GROUND_TRUTH)


if __name__ == "__main__":
    main()
