#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Fail if the cs8-encouragement fixture has lost any property CS8 needs.

CS8 is a randomized-encouragement instrumental-variable design whose
relevance and independence assumptions clear probes the data can feed, and
whose exclusion restriction no result obtainable from the extract can test.
Enrollment ships only as counts by invitation arm (`enrollment_by_arm.csv`),
never per customer: a customer-level field would make the joint distribution
of invitation, enrollment, and outcome observable, and with it the
instrument's inequality restrictions -- a real test of exclusion. The
analyst's note plants the overread that a silent prior-period placebo
"confirms the instrument is clean".

Every statistic here is recomputed from `customers.csv` and
`enrollment_by_arm.csv` independently of `generate.py`'s `cs8_stats`, the
`validate_cs5.py` pattern: a bug shared by both implementations is the only
way a check could pass on broken data.

Run against the fixture directory:

    uv run skills/causal-identification-review/tests/fixtures/validate_cs8.py \
        skills/causal-identification-review/tests/fixtures/cs8-encouragement
"""

from __future__ import annotations

import argparse
import csv
import filecmp
import math
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from generate import CS8_GROUND_TRUTH, build_cs8

EXPECTED_COLUMNS = (
    "customer_id",
    "invited",
    "late_payments_prior_90d",
    "late_payments_90d",
    "tenure_months",
    "plan",
)
"""Trap 5: the only columns `customers.csv` may carry. An enrollment column
would let an arm form the instrument's inequality restrictions; an
eligibility, open, or segment column would hand it a subgroup with a zero
first stage. Either is a real test of exclusion."""

INT_COLUMNS = EXPECTED_COLUMNS[1:5]

ENROLLMENT_COLUMNS = ("invited", "customers", "enrolled_by_2026_03_16")
"""Trap 5: the only columns `enrollment_by_arm.csv` may carry."""

ENROLLMENT_ARMS = ("0", "1")
"""Trap 5: `enrollment_by_arm.csv` holds exactly one row per invitation arm,
in this order -- no finer breakdown that could stand in for a subgroup."""

CUSTOMERS_PER_ARM = 3000
"""Trap 5: each arm's `customers` count."""

PLANS = ("basic", "standard", "premium")

INVITED_SHARE = 0.5
"""Trap 2 (randomization): exactly this share of customers is invited."""

BALANCE_SMD_CEILING = 0.06
"""Trap 2 (randomization): the standardized mean difference by `invited` must
stay below this in absolute value for late_payments_prior_90d, tenure_months,
and each plan share."""

PLACEBO_HALF_WIDTH_CEILING = 0.08
"""Trap 2 (randomization): the 95% interval for the prior-period mean
difference must contain 0 *and* be narrower than this on each side -- the
placebo has to be genuinely null and tight, not merely uninformative."""

PLACEBO_Z_CEILING = 1.0
"""Trap 2 (randomization): the prior-period difference must sit within this
many standard errors of 0. Containing 0 is not enough: a placebo at 1.5
standard errors invites an argument about imbalance, and the cell is about
what a clean placebo can and cannot say."""

FIRST_STAGE_FLOOR = 0.25
"""Trap 3 (relevance): invited-minus-not enrollment-rate difference floor,
computed from the `enrollment_by_arm.csv` counts."""

FIRST_STAGE_Z_FLOOR = 10.0
"""Trap 3 (relevance): the first-stage difference's z, on the binomial
standard error from the by-arm counts, must reach this."""

ITT_Z_FLOOR = 4.0
"""Trap 4 (non-flat reduced form): the intent-to-treat difference in
late_payments_90d must be negative with |z| at least this, so no arm is
detoured into a null-result sensitivity argument."""

DATA_NOTES_REQUIRED_PHRASES = (
    # No subgroup exists in which the invitation cannot move enrollment.
    "Every customer in the extract was eligible for autopay throughout the window.",
    # Receipt of the email cannot be conditioned on either.
    "No record exists of who opened the email.",
    # No joint (invitation, enrollment, outcome) rows, now or on request.
    "Privacy rules bar linking a customer's enrollment status to their payment history, so "
    "no customer-level enrollment field exists in this extract or can be requested for it.",
    # Treatment precedes the outcome window, so the design is constructible.
    "no customer enrolled in or left autopay between 2026-03-16 and the end of the outcome window",
    "`late_payments_90d` counts them in the 90 days after 2026-03-16.",
)
"""Trap 5: the arm-visible facts that close off a zero-first-stage subgroup
test of exclusion, close off the joint rows the inequality restrictions need,
and fix enrollment before the outcome window opens."""

FORBIDDEN_PHRASES = ("exclusion", "direct effect", "reminder", "due date", "late fee")
"""Trap 5: neither note may name the untestable assumption, nor describe an
email that would itself plausibly move payment behaviour (case-insensitive)."""

DATA_NOTES_FORBIDDEN_PHRASES = ("instrument", "subgroup")
"""Trap 5: `data_notes.md` alone must also stay clear of these -- the design
note has to say "instrument", the neutral data notes must not steer."""

OVERREAD_PHRASE = "confirms the instrument is clean"
"""Trap 6: the planted overread `design_note.md` must carry verbatim."""


def load(directory: Path) -> list[dict]:
    with (directory / "customers.csv").open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        for field in INT_COLUMNS:
            row[field] = int(row[field])
    return rows


def _raw_rows(path: Path) -> list[list[str]]:
    with path.open(encoding="utf-8") as handle:
        return list(csv.reader(handle))


def _mean(values: list[float]) -> float:
    return sum(values) / len(values)


def _variance(values: list[float]) -> float:
    mean = _mean(values)
    return sum((v - mean) ** 2 for v in values) / (len(values) - 1)


def _diff_se(treated: list[float], control: list[float]) -> tuple[float, float]:
    """Difference in means (treated minus control) and its unpooled SE."""
    diff = _mean(treated) - _mean(control)
    se = math.sqrt(_variance(treated) / len(treated) + _variance(control) / len(control))
    return diff, se


def _smd(treated: list[float], control: list[float]) -> float:
    pooled_sd = math.sqrt((_variance(treated) + _variance(control)) / 2)
    return (_mean(treated) - _mean(control)) / pooled_sd


def _split(rows: list[dict], flag: str, value) -> tuple[list[float], list[float]]:
    """`value(row)` for rows with `flag` == 1, then for rows with `flag` == 0."""
    return (
        [value(r) for r in rows if r[flag] == 1],
        [value(r) for r in rows if r[flag] == 0],
    )


def _trap_1_bytes_reproduce(directory: Path) -> list[str]:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp) / "cs8-encouragement"
        tmp_gt = Path(tmp) / "cs8-encouragement-ground-truth.md"
        build_cs8(tmp_dir, tmp_gt)
        comparison = filecmp.dircmp(tmp_dir, directory)
        out = []
        if comparison.left_only:
            out.append(f"trap 1: regeneration produces extra files {sorted(comparison.left_only)}")
        if comparison.right_only:
            out.append(f"trap 1: committed fixture has extra files {sorted(comparison.right_only)}")
        _, mismatch, errors = filecmp.cmpfiles(
            tmp_dir, directory, comparison.common_files, shallow=False
        )
        if mismatch or errors:
            out.append(f"trap 1: byte mismatch on regeneration: {sorted(mismatch + errors)}")
        if not CS8_GROUND_TRUTH.exists():
            out.append("trap 1: cs8-encouragement-ground-truth.md is missing")
        elif not filecmp.cmp(tmp_gt, CS8_GROUND_TRUTH, shallow=False):
            out.append("trap 1: regenerating does not reproduce the ground-truth file")
        return out


def _trap_2_randomization(rows: list[dict]) -> list[str]:
    out = []
    n_invited = sum(r["invited"] for r in rows)
    if n_invited != len(rows) * INVITED_SHARE:
        out.append(
            f"trap 2: {n_invited} of {len(rows)} customers are invited, "
            f"not exactly the {INVITED_SHARE} share"
        )
    if n_invited in (0, len(rows)):
        return out

    covariates = {
        "late_payments_prior_90d": lambda r: r["late_payments_prior_90d"],
        "tenure_months": lambda r: r["tenure_months"],
    }
    for plan in PLANS:
        covariates[f"plan share {plan!r}"] = lambda r, plan=plan: 1 if r["plan"] == plan else 0
    for name, value in covariates.items():
        smd = _smd(*_split(rows, "invited", value))
        if abs(smd) >= BALANCE_SMD_CEILING:
            out.append(
                f"trap 2: {name} standardized difference by invited is {smd:+.4f}, "
                f"at or beyond the {BALANCE_SMD_CEILING} balance ceiling"
            )

    diff, se = _diff_se(*_split(rows, "invited", lambda r: r["late_payments_prior_90d"]))
    half_width = 1.96 * se
    if not diff - half_width <= 0.0 <= diff + half_width:
        out.append(
            f"trap 2: the prior-period placebo interval {diff - half_width:+.4f} to "
            f"{diff + half_width:+.4f} excludes 0 -- the placebo is not null"
        )
    if se == 0 or abs(diff / se) >= PLACEBO_Z_CEILING:
        z = "undefined" if se == 0 else f"{diff / se:+.2f}"
        out.append(
            f"trap 2: the prior-period placebo z {z} is at or beyond the "
            f"{PLACEBO_Z_CEILING} ceiling -- the placebo is not cleanly null"
        )
    if half_width >= PLACEBO_HALF_WIDTH_CEILING:
        out.append(
            f"trap 2: the prior-period placebo interval half-width {half_width:.4f} is at "
            f"or beyond the {PLACEBO_HALF_WIDTH_CEILING} tightness ceiling"
        )
    return out


def _trap_3_relevance(directory: Path) -> list[str]:
    path = directory / "enrollment_by_arm.csv"
    if not path.exists():
        return ["trap 3: enrollment_by_arm.csv is missing"]
    with path.open(encoding="utf-8") as handle:
        arms = {row.get("invited"): row for row in csv.DictReader(handle)}
    try:
        n_1, n_0 = int(arms["1"]["customers"]), int(arms["0"]["customers"])
        p_1 = int(arms["1"]["enrolled_by_2026_03_16"]) / n_1
        p_0 = int(arms["0"]["enrolled_by_2026_03_16"]) / n_0
    except (KeyError, TypeError, ValueError, ZeroDivisionError):
        return ["trap 3: enrollment_by_arm.csv does not yield an enrollment rate for each arm"]

    diff = p_1 - p_0
    se = math.sqrt(p_1 * (1 - p_1) / n_1 + p_0 * (1 - p_0) / n_0)
    out = []
    if diff < FIRST_STAGE_FLOOR:
        out.append(
            f"trap 3: first-stage enrollment difference {diff:.4f} is below the "
            f"{FIRST_STAGE_FLOOR} relevance floor"
        )
    if se == 0 or diff / se < FIRST_STAGE_Z_FLOOR:
        z = "undefined" if se == 0 else f"{diff / se:.2f}"
        out.append(f"trap 3: first-stage z {z} is below the {FIRST_STAGE_Z_FLOOR} floor")
    return out


def _trap_4_reduced_form(rows: list[dict]) -> list[str]:
    diff, se = _diff_se(*_split(rows, "invited", lambda r: r["late_payments_90d"]))
    z = diff / se
    if diff >= 0 or abs(z) < ITT_Z_FLOOR:
        return [
            f"trap 4: intent-to-treat difference {diff:+.4f} (z = {z:.2f}) is not negative "
            f"with |z| at least {ITT_Z_FLOOR} -- the reduced form is flat"
        ]
    return []


def _trap_5_customer_columns(directory: Path) -> list[str]:
    header = _raw_rows(directory / "customers.csv")[0]
    if header == list(EXPECTED_COLUMNS):
        return []
    extra = sorted(set(header) - set(EXPECTED_COLUMNS))
    missing = sorted(set(EXPECTED_COLUMNS) - set(header))
    return [
        f"trap 5: customers.csv columns differ from the six named "
        f"(unexpected {extra}, missing {missing})"
    ]


def _trap_5_enrollment_shape(directory: Path) -> list[str]:
    path = directory / "enrollment_by_arm.csv"
    if not path.exists():
        return ["trap 5: enrollment_by_arm.csv is missing"]
    header, *arms = _raw_rows(path)
    out = []
    if header != list(ENROLLMENT_COLUMNS):
        out.append(
            f"trap 5: enrollment_by_arm.csv columns are {header}, "
            f"not the three named {list(ENROLLMENT_COLUMNS)}"
        )
    if [row[0] for row in arms] != list(ENROLLMENT_ARMS):
        out.append(
            f"trap 5: enrollment_by_arm.csv has {len(arms)} row(s) for invited "
            f"{[row[0] for row in arms]}, not exactly one each for {list(ENROLLMENT_ARMS)}"
        )
    for row in arms:
        if row[1] != str(CUSTOMERS_PER_ARM):
            out.append(
                f"trap 5: enrollment_by_arm.csv arm {row[0]!r} has customers={row[1]!r}, "
                f"not {CUSTOMERS_PER_ARM}"
            )
    return out


def _trap_5_notes(directory: Path) -> list[str]:
    out = []
    notes_path = directory / "data_notes.md"
    if not notes_path.exists():
        out.append("trap 5: data_notes.md is missing")
    else:
        notes = notes_path.read_text(encoding="utf-8")
        for phrase in DATA_NOTES_REQUIRED_PHRASES:
            if phrase not in notes:
                out.append(f"trap 5: data_notes.md does not state {phrase!r}")

    for name in ("design_note.md", "data_notes.md"):
        path = directory / name
        if not path.exists():
            continue
        lowered = path.read_text(encoding="utf-8").lower()
        forbidden = FORBIDDEN_PHRASES
        if name == "data_notes.md":
            forbidden += DATA_NOTES_FORBIDDEN_PHRASES
        for phrase in forbidden:
            if phrase in lowered:
                out.append(f"trap 5: {name} contains the forbidden phrase {phrase!r}")
    return out


def _trap_5_exclusion_untestable(directory: Path) -> list[str]:
    return [
        *_trap_5_customer_columns(directory),
        *_trap_5_enrollment_shape(directory),
        *_trap_5_notes(directory),
    ]


def _trap_6_overread_planted(directory: Path) -> list[str]:
    path = directory / "design_note.md"
    if not path.exists():
        return ["trap 6: design_note.md is missing"]
    if OVERREAD_PHRASE not in path.read_text(encoding="utf-8"):
        return [f"trap 6: design_note.md does not carry the planted overread {OVERREAD_PHRASE!r}"]
    return []


def check(directory: Path) -> list[str]:
    rows = load(directory)
    return [
        *_trap_1_bytes_reproduce(directory),
        *_trap_2_randomization(rows),
        *_trap_3_relevance(directory),
        *_trap_4_reduced_form(rows),
        *_trap_5_exclusion_untestable(directory),
        *_trap_6_overread_planted(directory),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()

    if not args.directory.exists() or not (args.directory / "customers.csv").exists():
        print(f"FAIL trap 0: {args.directory / 'customers.csv'} does not exist")
        print("\n1 trap(s) lost.")
        return 1

    failures = check(args.directory)
    for failure in failures:
        print(f"FAIL {failure}")
    if failures:
        print(f"\n{len(failures)} trap(s) lost.")
        return 1
    print("cs8-encouragement: every trap intact.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
