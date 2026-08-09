#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Fail if the cs3-rollout fixture has lost any property CS3 needs.

Ground truth and floors are preregistered in scenario CS3
(`skills/causal-identification-review/tests/scenarios.md`). Every threshold
is a floor or ceiling the committed seed clears with margin, so a failure
here means the fixture changed rather than that a bound was tight.

Run against the fixture directory:

    uv run skills/causal-identification-review/tests/fixtures/validate_cs3.py \
        skills/causal-identification-review/tests/fixtures/cs3-rollout
"""

from __future__ import annotations

import argparse
import csv
import filecmp
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from generate import CS3_CUTOVER, CS3_GROUND_TRUTH, build_cs3

CUTOVER_ISO = CS3_CUTOVER.isoformat()

SLOPE_TOLERANCE = 1e-6
"""Trap 1: recomputed slope vs. the generator's recorded value, floating-point
arithmetic only -- both sides run the identical sum-of-squares math on the
same frozen data, so any gap beyond FP noise means one side changed."""

WEST_SLOPE_FLOOR = 0.30
"""Trap 1: West's pre-period completion-time slope must fall at least this
many seconds/day -- the planted differential pre-trend must be loud enough
that a pre-period slope comparison flags it as non-parallel."""

EAST_SLOPE_CEILING = 0.20
"""Trap 1: East's pre-period slope must stay this close to flat."""

AOV_PROMO_FLOOR = 5.0
"""Trap 2: West's avg_order_value must rise at least this much from pre to
post cutover -- the planted concurrent promotion, visible on the named
placebo channel."""

AOV_EAST_CEILING = 2.0
"""Trap 2: East's avg_order_value must stay this close to flat across the
same cutover -- East gets no promotion, so the placebo probe finds nothing
there."""

COMPLETION_DIFF_FLOOR = 15.0
"""Trap 3: West's naive before/after completion-time drop must be at least
this large -- a real, non-flat primary contrast, not a fluke of noise."""

EXPECTED_FILES = {
    "daily.csv",
    "promotions.log",
    "targeting_note.md",
    "ux_cleanup_note.md",
    "data_notes.md",
}
"""Trap 4: the handed-to-arms directory holds exactly these files -- no
donor-pool region file that would make synthetic control constructible, and
no stray ground-truth leak."""


def load(directory: Path) -> list[dict]:
    with (directory / "daily.csv").open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        row["completion_time_seconds"] = float(row["completion_time_seconds"])
        row["avg_order_value"] = float(row["avg_order_value"])
        row["volume"] = int(row["volume"])
    return rows


def _slope(xs: list[float], ys: list[float]) -> float:
    """Independent OLS-slope reimplementation.

    Deliberately not imported from `generate.py`: this validator checks the
    generator's own recorded pre-trend value against a second, separately
    written computation, so a bug shared by both is the only way a mismatch
    could hide.
    """
    n = len(xs)
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(xs, ys, strict=True))
    denominator = sum((x - mean_x) ** 2 for x in xs)
    return numerator / denominator


def _pre_series(rows: list[dict], region: str) -> list[float]:
    pre = [r for r in rows if r["region"] == region and r["date"] < CUTOVER_ISO]
    pre.sort(key=lambda r: r["date"])
    return [r["completion_time_seconds"] for r in pre]


def _mean(values: list[float]) -> float:
    return sum(values) / len(values)


def _trap_1_pretrend(rows: list[dict]) -> list[str]:
    out = []
    west_series = _pre_series(rows, "West")
    east_series = _pre_series(rows, "East")
    west_slope = _slope(list(range(len(west_series))), west_series)
    east_slope = _slope(list(range(len(east_series))), east_series)

    if west_slope > -WEST_SLOPE_FLOOR:
        out.append(
            f"trap 1: West pre-period slope {west_slope:.4f} s/day is not steeper than "
            f"-{WEST_SLOPE_FLOOR} s/day"
        )
    if abs(east_slope) > EAST_SLOPE_CEILING:
        out.append(
            f"trap 1: East pre-period slope {east_slope:.4f} s/day exceeds the "
            f"{EAST_SLOPE_CEILING} s/day flat ceiling"
        )

    recorded = _parse_ground_truth_slopes()
    if recorded is None:
        out.append("trap 1: cs3-rollout-ground-truth.md is missing or unparseable")
    else:
        recorded_west, recorded_east = recorded
        if abs(recorded_west - west_slope) > SLOPE_TOLERANCE:
            out.append(
                f"trap 1: recorded West slope {recorded_west:.6f} does not match "
                f"recomputed slope {west_slope:.6f}"
            )
        if abs(recorded_east - east_slope) > SLOPE_TOLERANCE:
            out.append(
                f"trap 1: recorded East slope {recorded_east:.6f} does not match "
                f"recomputed slope {east_slope:.6f}"
            )
    return out


def _parse_ground_truth_slopes() -> tuple[float, float] | None:
    if not CS3_GROUND_TRUTH.exists():
        return None
    text = CS3_GROUND_TRUTH.read_text(encoding="utf-8")
    west = east = None
    for line in text.splitlines():
        if "West pre-period completion-time slope" in line:
            west = float(line.split(":")[1].strip().split(" ")[0])
        if "East pre-period completion-time slope" in line:
            east = float(line.split(":")[1].strip().split(" ")[0])
    if west is None or east is None:
        return None
    return west, east


def _trap_2_concurrent_change(rows: list[dict]) -> list[str]:
    out = []
    west_pre = [
        r["avg_order_value"] for r in rows if r["region"] == "West" and r["date"] < CUTOVER_ISO
    ]
    west_post = [
        r["avg_order_value"] for r in rows if r["region"] == "West" and r["date"] >= CUTOVER_ISO
    ]
    east_pre = [
        r["avg_order_value"] for r in rows if r["region"] == "East" and r["date"] < CUTOVER_ISO
    ]
    east_post = [
        r["avg_order_value"] for r in rows if r["region"] == "East" and r["date"] >= CUTOVER_ISO
    ]

    west_diff = _mean(west_post) - _mean(west_pre)
    east_diff = _mean(east_post) - _mean(east_pre)

    if west_diff < AOV_PROMO_FLOOR:
        out.append(
            f"trap 2: West avg_order_value rose only {west_diff:.2f} < {AOV_PROMO_FLOOR} "
            "-- the planted promotion is too weak"
        )
    if abs(east_diff) > AOV_EAST_CEILING:
        out.append(
            f"trap 2: East avg_order_value moved {east_diff:.2f}, exceeding the "
            f"{AOV_EAST_CEILING} flat ceiling -- the placebo channel is not clean"
        )

    return out


def _trap_3_primary_contrast(rows: list[dict]) -> list[str]:
    west_pre = [
        r["completion_time_seconds"]
        for r in rows
        if r["region"] == "West" and r["date"] < CUTOVER_ISO
    ]
    west_post = [
        r["completion_time_seconds"]
        for r in rows
        if r["region"] == "West" and r["date"] >= CUTOVER_ISO
    ]
    diff = _mean(west_post) - _mean(west_pre)
    if diff > -COMPLETION_DIFF_FLOOR:
        return [
            f"trap 3: West's before/after completion-time drop {diff:.2f}s is not steeper than "
            f"-{COMPLETION_DIFF_FLOOR}s -- the primary contrast is too weak or flat"
        ]
    return []


def _trap_4_decoy_and_directory(rows: list[dict], directory: Path) -> list[str]:
    out = []
    regions = {r["region"] for r in rows}
    if regions != {"West", "East"}:
        out.append(f"trap 4: expected exactly {{West, East}}, found {regions}")

    found = {p.name for p in directory.iterdir()}
    missing = EXPECTED_FILES - found
    extra = found - EXPECTED_FILES
    if missing:
        out.append(f"trap 4: fixture directory is missing {sorted(missing)}")
    if extra:
        out.append(f"trap 4: fixture directory has unexpected entries {sorted(extra)}")
    return out


def _trap_5_selection_note(directory: Path) -> list[str]:
    out = []
    note_path = directory / "targeting_note.md"
    if not note_path.exists():
        return ["trap 5: targeting_note.md is missing"]
    text = note_path.read_text(encoding="utf-8")

    west_count = east_count = None
    for line in text.splitlines():
        stripped = line.strip("- ").strip()
        if stripped.startswith("West:"):
            west_count = int(stripped.split(":")[1].strip())
        if stripped.startswith("East:"):
            east_count = int(stripped.split(":")[1].strip())
    if west_count is None or east_count is None:
        out.append("trap 5: targeting_note.md does not carry parseable West/East complaint counts")
    elif west_count <= east_count:
        out.append(
            f"trap 5: West's stated complaint count {west_count} is not higher than "
            f"East's {east_count}"
        )
    if "highest" not in text.lower():
        out.append("trap 5: targeting_note.md does not state West was the highest-complaint region")
    return out


def _trap_6_bytes_reproduce(directory: Path) -> list[str]:
    with tempfile.TemporaryDirectory() as tmp:
        tmp_dir = Path(tmp) / "cs3-rollout"
        tmp_gt = Path(tmp) / "cs3-rollout-ground-truth.md"
        build_cs3(tmp_dir, tmp_gt)
        mismatch = _dircmp(tmp_dir, directory)
        if mismatch:
            return mismatch
        if not filecmp.cmp(tmp_gt, CS3_GROUND_TRUTH, shallow=False):
            return ["trap 6: regenerating does not reproduce the ground-truth file"]
    return []


def _dircmp(built: Path, committed: Path) -> list[str]:
    comparison = filecmp.dircmp(built, committed)
    out = []
    if comparison.left_only:
        out.append(f"trap 6: regeneration produces extra files {sorted(comparison.left_only)}")
    if comparison.right_only:
        out.append(f"trap 6: committed fixture has extra files {sorted(comparison.right_only)}")
    _, mismatch, errors = filecmp.cmpfiles(built, committed, comparison.common_files, shallow=False)
    if mismatch or errors:
        out.append(f"trap 6: byte mismatch on regeneration: {sorted(mismatch + errors)}")
    return out


def check(directory: Path) -> list[str]:
    rows = load(directory)
    return [
        *_trap_1_pretrend(rows),
        *_trap_2_concurrent_change(rows),
        *_trap_3_primary_contrast(rows),
        *_trap_4_decoy_and_directory(rows, directory),
        *_trap_5_selection_note(directory),
        *_trap_6_bytes_reproduce(directory),
    ]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    args = parser.parse_args()

    if not args.directory.exists():
        print(f"FAIL trap 0: fixture directory {args.directory} does not exist")
        print("\n1 trap(s) lost.")
        return 1
    if not (args.directory / "daily.csv").exists():
        print(f"FAIL trap 0: {args.directory / 'daily.csv'} does not exist")
        print("\n1 trap(s) lost.")
        return 1

    failures = check(args.directory)
    for failure in failures:
        print(f"FAIL {failure}")
    if failures:
        print(f"\n{len(failures)} trap(s) lost.")
        return 1
    print("cs3-rollout: every trap intact.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
