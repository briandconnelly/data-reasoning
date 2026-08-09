#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Fail if the cs7-seam fixture has lost any property CS7 needs.

Ground truth and floors are preregistered in scenario CS7
(`skills/causal-identification-review/tests/scenarios.md`): a sharp
credit-score-680 cutoff whose identifying assumptions actually clear their
probes, unlike CS3/CS4 which are built to defeat their designs.

Run against the fixture directory:

    uv run skills/causal-identification-review/tests/fixtures/validate_cs7.py \
        skills/causal-identification-review/tests/fixtures/cs7-seam
"""

from __future__ import annotations

import argparse
import csv
import filecmp
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from generate import CS7_CUTOFF, CS7_ESTIMAND, CS7_GROUND_TRUTH, build_cs7

WIDE_BANDWIDTH = 20
NARROW_BANDWIDTH = 10

DENSITY_RATIO_FLOOR = 0.6
"""Trap 1 (no manipulation): the smaller of the two side counts must be at
least this fraction of the larger -- no bunching at the cutoff."""

TENURE_BALANCE_CEILING = 2.0
"""Trap 2 (covariate balance): account_tenure_months must not jump by more
than this many months right at the cutoff."""

INCOME_BALANCE_CEILING = 3000.0
"""Trap 2 (covariate balance): income must not jump by more than this many
dollars right at the cutoff."""

JUMP_FLOOR = 0.03
"""Trap 3 (real effect): the raw default-rate jump across the wide bandwidth
must exceed this -- a real, non-flat signal, not an accident of the draw."""

EXPECTED_FILES = {"accounts.csv", "data_notes.md"}

DATA_NOTES_REQUIRED_PHRASES = (
    # The no-bundled-policy fact the identified-if ground truth rests on,
    # stated arm-visibly (2026-08-09 amendment): without it a careful arm
    # has no discriminating evidence for the no-coincident-confound
    # assumption and correctly refuses identified-if.
    "gates instant-checkout eligibility only",
    "no other product, pricing, underwriting, or policy rule",
    "at or near 680",
)
"""Trap 8: data_notes.md must state that nothing but instant-checkout
eligibility keys on the 680 threshold -- the validate_cs4 trap 1 pattern."""


def load(directory: Path) -> list[dict]:
    with (directory / "accounts.csv").open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        row["credit_score"] = int(row["credit_score"])
        row["account_tenure_months"] = float(row["account_tenure_months"])
        row["income"] = float(row["income"])
        row["default_90d"] = int(row["default_90d"])
        row["eligible"] = row["eligible"] == "true"
    return rows


def _mean(values: list[float]) -> float:
    return sum(values) / len(values)


def _side(rows: list[dict], lo: int, hi: int) -> list[dict]:
    return [r for r in rows if lo <= r["credit_score"] < hi]


def _trap_1_no_manipulation(rows: list[dict]) -> list[str]:
    below = _side(rows, CS7_CUTOFF - WIDE_BANDWIDTH, CS7_CUTOFF)
    above = _side(rows, CS7_CUTOFF, CS7_CUTOFF + WIDE_BANDWIDTH)
    if not below or not above:
        return ["trap 1: one side of the cutoff has zero accounts in the wide bandwidth"]
    ratio = min(len(below), len(above)) / max(len(below), len(above))
    if ratio < DENSITY_RATIO_FLOOR:
        return [
            f"trap 1: density ratio {ratio:.3f} (n_below={len(below)}, n_above={len(above)}) "
            f"is below the {DENSITY_RATIO_FLOOR} no-manipulation floor"
        ]
    return []


def _trap_2_covariate_balance(rows: list[dict]) -> list[str]:
    below = _side(rows, CS7_CUTOFF - NARROW_BANDWIDTH, CS7_CUTOFF)
    above = _side(rows, CS7_CUTOFF, CS7_CUTOFF + NARROW_BANDWIDTH)
    out = []
    if not below or not above:
        return ["trap 2: one side of the cutoff has zero accounts in the narrow bandwidth"]

    tenure_diff = abs(
        _mean([r["account_tenure_months"] for r in below])
        - _mean([r["account_tenure_months"] for r in above])
    )
    income_diff = abs(_mean([r["income"] for r in below]) - _mean([r["income"] for r in above]))
    if tenure_diff > TENURE_BALANCE_CEILING:
        out.append(
            f"trap 2: account_tenure_months jumps {tenure_diff:.3f} months at the cutoff, "
            f"exceeding the {TENURE_BALANCE_CEILING}-month balance ceiling"
        )
    if income_diff > INCOME_BALANCE_CEILING:
        out.append(
            f"trap 2: income jumps ${income_diff:.2f} at the cutoff, exceeding the "
            f"${INCOME_BALANCE_CEILING} balance ceiling"
        )
    return out


def _trap_3_real_effect(rows: list[dict]) -> list[str]:
    below = _side(rows, CS7_CUTOFF - WIDE_BANDWIDTH, CS7_CUTOFF)
    above = _side(rows, CS7_CUTOFF, CS7_CUTOFF + WIDE_BANDWIDTH)
    jump = _mean([r["default_90d"] for r in below]) - _mean([r["default_90d"] for r in above])
    if jump < JUMP_FLOOR:
        return [
            f"trap 3: raw default-rate jump {jump:.4f} is below the {JUMP_FLOOR} "
            "non-flat-effect floor"
        ]
    return []


def _trap_4_sharp_assignment(rows: list[dict]) -> list[str]:
    out = []
    for row in rows:
        expected = row["credit_score"] >= CS7_CUTOFF
        if row["eligible"] != expected:
            out.append(
                f"trap 4: account {row['account_id']} has eligible={row['eligible']} but "
                f"credit_score={row['credit_score']} (expected {expected})"
            )
    return out


def _trap_5_estimand() -> list[str]:
    if not CS7_GROUND_TRUTH.exists():
        return ["trap 5: cs7-seam-ground-truth.md is missing"]
    text = CS7_GROUND_TRUTH.read_text(encoding="utf-8")
    if CS7_ESTIMAND not in text:
        return [
            "trap 5: cs7-seam-ground-truth.md does not carry the precommitted estimand verbatim"
        ]
    return []


def _trap_6_directory(directory: Path) -> list[str]:
    found = {p.name for p in directory.iterdir()}
    missing = EXPECTED_FILES - found
    extra = found - EXPECTED_FILES
    out = []
    if missing:
        out.append(f"trap 6: fixture directory is missing {sorted(missing)}")
    if extra:
        out.append(f"trap 6: fixture directory has unexpected entries {sorted(extra)}")
    return out


def _trap_7_bytes_reproduce(directory: Path) -> list[str]:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp) / "cs7-seam"
        tmp_gt = Path(tmp) / "cs7-seam-ground-truth.md"
        build_cs7(tmp_dir, tmp_gt)
        comparison = filecmp.dircmp(tmp_dir, directory)
        out = []
        if comparison.left_only:
            out.append(f"trap 7: regeneration produces extra files {sorted(comparison.left_only)}")
        if comparison.right_only:
            out.append(f"trap 7: committed fixture has extra files {sorted(comparison.right_only)}")
        _, mismatch, errors = filecmp.cmpfiles(
            tmp_dir, directory, comparison.common_files, shallow=False
        )
        if mismatch or errors:
            out.append(f"trap 7: byte mismatch on regeneration: {sorted(mismatch + errors)}")
        if not filecmp.cmp(tmp_gt, CS7_GROUND_TRUTH, shallow=False):
            out.append("trap 7: regenerating does not reproduce the ground-truth file")
        return out


def _trap_8_no_bundled_policy(directory: Path) -> list[str]:
    notes_path = directory / "data_notes.md"
    if not notes_path.exists():
        return ["trap 8: data_notes.md is missing"]
    lowered = notes_path.read_text(encoding="utf-8").lower()
    out = []
    for phrase in DATA_NOTES_REQUIRED_PHRASES:
        if phrase.lower() not in lowered:
            out.append(f"trap 8: data_notes.md does not state {phrase!r}")
    return out


def check(directory: Path) -> list[str]:
    rows = load(directory)
    return [
        *_trap_1_no_manipulation(rows),
        *_trap_2_covariate_balance(rows),
        *_trap_3_real_effect(rows),
        *_trap_4_sharp_assignment(rows),
        *_trap_5_estimand(),
        *_trap_6_directory(directory),
        *_trap_7_bytes_reproduce(directory),
        *_trap_8_no_bundled_policy(directory),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()

    if not args.directory.exists() or not (args.directory / "accounts.csv").exists():
        print(f"FAIL trap 0: {args.directory / 'accounts.csv'} does not exist")
        print("\n1 trap(s) lost.")
        return 1

    failures = check(args.directory)
    for failure in failures:
        print(f"FAIL {failure}")
    if failures:
        print(f"\n{len(failures)} trap(s) lost.")
        return 1
    print("cs7-seam: every trap intact.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
