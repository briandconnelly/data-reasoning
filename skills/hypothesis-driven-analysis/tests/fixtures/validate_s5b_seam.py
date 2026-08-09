#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Fail if the s5b-seam fixture has lost any trap it exists to set.

The E1 seam scenario and the S5 replacement are only live while the fixture
keeps every trap below. Run against the fixture directory:

    uv run skills/hypothesis-driven-analysis/tests/fixtures/validate_s5b_seam.py \
        skills/hypothesis-driven-analysis/tests/fixtures/s5b-seam

Traps and their floors are preregistered in scenario E1
(`skills/exploratory-data-analysis/tests/scenarios.md`). Every threshold is a
floor the committed seed clears with margin, so a failure here means the
fixture changed rather than that a bound was tight.
"""

from __future__ import annotations

import argparse
import csv
import filecmp
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from generate_s5b_seam import (
    D_ENDPOINT,
    D_PLAN,
    DISCOVERY_DAYS,
    HOLE_DAYS,
    HOLE_REGION,
    RESERVE_MAX,
    RESERVE_MIN,
    START,
    T_ENDPOINT,
    T_VERSION,
    VERSIONS,
    build,
)

T_FLOOR_PP = 12.0
"""Trap 1: T's lift, in the discovery window and in EVERY admissible reserve."""

D_EARLY_FLOOR_PP = 8.0
"""Trap 2: the decoy must be loud enough in-sample to be a top-ranked lead."""

D_RESERVE_CEILING_PP = 1.5
"""Trap 2: and must be gone in EVERY admissible reserve."""

REGION_DELTA_FRACTION = 0.10
"""Trap 5: neither effect may ride on the region the coverage hole removes.

Stated as a fraction of the effect's own lift rather than in absolute points.
The T cell holds a few hundred rows, and dropping a 23% region resamples it --
a shift of about a point is ordinary noise at that n, not region dependence.
An absolute 0.5pp ceiling failed on the committed seed for exactly that reason,
which is a bound too tight to be evidence rather than a fixture defect."""

D_EARLY_DAYS = 20

# Semantic hints only. The raw categorical values under test -- 4.2.3, /export,
# enterprise -- are exempt by construction: the fixture cannot work without
# them, and forbidding them would make this check impossible rather than strict.
TELEGRAPH_TOKENS = (
    "affected",
    "bad",
    "broken",
    "bug",
    "regression",
    "outage",
    "known_issue",
    "error_reason",
    "root_cause",
    "faulty",
    "planted",
    "decoy",
)


def load(directory: Path) -> list[dict]:
    with (directory / "events.csv").open(encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        row["day"] = (int(row["ts"][8:10]) - START.day) + (30 if row["ts"][5:7] == "06" else 0)
    return rows


def lift_pp(rows: list[dict], cell, window) -> tuple[float, int]:
    inside = [r for r in rows if cell(r) and window(r)]
    outside = [r for r in rows if not cell(r) and window(r)]
    if not inside or not outside:
        return 0.0, 0
    rate_in = sum(r["status"] == "error" for r in inside) / len(inside)
    rate_out = sum(r["status"] == "error" for r in outside) / len(outside)
    return 100 * (rate_in - rate_out), len(inside)


def is_t(row: dict) -> bool:
    return row["endpoint"] == T_ENDPOINT and row["client_version"] == T_VERSION


def is_d(row: dict) -> bool:
    return row["plan"] == D_PLAN and row["endpoint"] == D_ENDPOINT


def reserve_windows(last_day: int):
    for length in range(RESERVE_MIN, RESERVE_MAX + 1):
        cutoff = last_day - length + 1
        yield length, (lambda r, c=cutoff: r["day"] >= c)


def _trap_1_true_lead_reproduces(rows: list[dict], last_day: int) -> list[str]:
    """T must be visible in discovery AND in every window an arm might reserve."""
    out = []
    value, _ = lift_pp(rows, is_t, lambda r: r["day"] < DISCOVERY_DAYS)
    if value < T_FLOOR_PP:
        out.append(f"trap 1: T lift in discovery window {value:.1f}pp < {T_FLOOR_PP}pp")
    for length, window in reserve_windows(last_day):
        value, count = lift_pp(rows, is_t, window)
        if value < T_FLOOR_PP:
            out.append(
                f"trap 1: T lift in {length}-day reserve {value:.1f}pp < {T_FLOOR_PP}pp (n={count})"
            )
    return out


def _trap_2_decoy_vanishes(rows: list[dict], last_day: int) -> list[str]:
    """D must be loud enough in-sample to be chased, and gone in every reserve."""
    out = []
    value, _ = lift_pp(rows, is_d, lambda r: r["day"] < D_EARLY_DAYS)
    if value < D_EARLY_FLOOR_PP:
        out.append(f"trap 2: D lift in first {D_EARLY_DAYS}d {value:.1f}pp < {D_EARLY_FLOOR_PP}pp")
    for length, window in reserve_windows(last_day):
        value, _ = lift_pp(rows, is_d, window)
        if value > D_RESERVE_CEILING_PP:
            out.append(
                f"trap 2: D lift in {length}-day reserve {value:.1f}pp > {D_RESERVE_CEILING_PP}pp"
            )
    return out


def _trap_4_hole_and_denominator(rows: list[dict], last_day: int, directory: Path) -> list[str]:
    """The hole sits exactly where it claims, and nothing can measure around it."""
    out = []
    for day in range(last_day + 1):
        present = any(r["day"] == day and r["region"] == HOLE_REGION for r in rows)
        if day in HOLE_DAYS and present:
            out.append(f"trap 4: {HOLE_REGION} present on hole day {day}")
        if day not in HOLE_DAYS and not present:
            out.append(f"trap 4: {HOLE_REGION} absent on non-hole day {day}")
    # Only the data file. An earlier revision whitelisted a README here and put
    # the planted ground truth in it -- inside the very directory the arms are
    # handed. That is the defect that invalidated the original S5 (a compliant
    # agent lists the directory and legitimately uses what it finds), so the
    # ground truth lives at ../s5b-seam-ground-truth.md and this is now strict.
    extra = [p.name for p in directory.iterdir() if p.name != "events.csv"]
    if extra:
        out.append(f"trap 4: the fixture directory must hold events.csv alone; found {extra}")
    return out


def _trap_5_region_not_load_bearing(rows: list[dict]) -> list[str]:
    """Neither effect may ride on the region the coverage hole removes."""
    out = []
    for name, cell, window in (
        ("T", is_t, lambda _r: True),
        ("D", is_d, lambda r: r["day"] < D_EARLY_DAYS),
    ):
        with_apac, _ = lift_pp(rows, cell, window)
        without_apac, _ = lift_pp([r for r in rows if r["region"] != HOLE_REGION], cell, window)
        delta = abs(with_apac - without_apac)
        ceiling = REGION_DELTA_FRACTION * abs(with_apac)
        if delta > ceiling:
            out.append(
                f"trap 5: excluding {HOLE_REGION} moves {name}'s lift {delta:.2f}pp "
                f"> {ceiling:.2f}pp ({REGION_DELTA_FRACTION:.0%} of its {with_apac:.1f}pp lift)"
            )
    return out


def _trap_6_7_version_and_tokens(rows: list[dict], directory: Path) -> list[str]:
    """Nothing may distinguish the affected version, or name the mechanism."""
    out = []
    names = [row[0] for row in VERSIONS]
    counts = {v: sum(r["client_version"] == v for r in rows) for v in names}
    order = sorted(counts, key=lambda v: -counts[v])
    if T_VERSION in (order[0], order[-1]):
        out.append(f"trap 6: {T_VERSION} is the most or least frequent version")
    if T_VERSION in (names[0], names[-1]):
        out.append(f"trap 6: {T_VERSION} is the oldest or newest version")

    text = (directory / "events.csv").read_text(encoding="utf-8").lower()
    for token in TELEGRAPH_TOKENS:
        if token in text or token in directory.name.lower():
            out.append(f"trap 7: telegraph token {token!r} appears in the fixture")
    return out


def _trap_8_bytes_reproduce(directory: Path) -> list[str]:
    """The committed bytes must be what the generator produces, today."""
    with tempfile.TemporaryDirectory() as tmp:
        build(Path(tmp))
        if filecmp.cmp(Path(tmp) / "events.csv", directory / "events.csv", shallow=False):
            return []
    return ["trap 8: regenerating from the committed seed does not reproduce events.csv"]


def check(directory: Path) -> list[str]:
    rows = load(directory)
    last_day = max(r["day"] for r in rows)
    failures = [
        *_trap_1_true_lead_reproduces(rows, last_day),
        *_trap_2_decoy_vanishes(rows, last_day),
        *(
            ["trap 3: a row carries both the T cell and the D cell"]
            if any(is_t(r) and is_d(r) for r in rows)
            else []
        ),
        *_trap_4_hole_and_denominator(rows, last_day, directory),
        *_trap_5_region_not_load_bearing(rows),
        *_trap_6_7_version_and_tokens(rows, directory),
        *_trap_8_bytes_reproduce(directory),
    ]
    return failures


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--report", action="store_true", help="print measured margins and exit 0")
    args = parser.parse_args()

    if args.report:
        rows = load(args.directory)
        last_day = max(r["day"] for r in rows)
        worst_t = min(lift_pp(rows, is_t, w)[0] for _, w in reserve_windows(last_day))
        best_d = max(lift_pp(rows, is_d, w)[0] for _, w in reserve_windows(last_day))
        disc, _ = lift_pp(rows, is_t, lambda r: r["day"] < DISCOVERY_DAYS)
        early, _ = lift_pp(rows, is_d, lambda r: r["day"] < D_EARLY_DAYS)
        print(f"rows={len(rows)}")
        print(f"T discovery={disc:.1f}pp  T worst reserve={worst_t:.1f}pp (floor {T_FLOOR_PP})")
        print(
            f"D early={early:.1f}pp (floor {D_EARLY_FLOOR_PP})  "
            f"D best reserve={best_d:.1f}pp (ceiling {D_RESERVE_CEILING_PP})"
        )
        return 0

    failures = check(args.directory)
    for failure in failures:
        print(f"FAIL {failure}")
    if failures:
        print(f"\n{len(failures)} trap(s) lost.")
        return 1
    print("s5b-seam: every trap intact.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
