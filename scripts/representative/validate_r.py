#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Fail if the R1/R2 order table no longer yields the preregistered answers.

R1 and R2 are routine: one right answer a direct query settles. The property
that keeps them routine is that the answer is unique and unambiguous: R1's
order count differs from the unit count a misreading would give, and R2's
per-store means are distinct and do not sit on a rounding boundary at cents.
The expected values are the prereg's ground truth
(`docs/evidence/integration/representative-v1/prereg.md` § R1, § R2), copied
here so a regenerated table that moves them fails.

    uv run scripts/representative/validate_r.py \
        docs/evidence/integration/representative-v1/fixtures/r-sales
"""

from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _common import regenerated_matches, report
from generate import build_r_sales

R1_EXPECTED = 99
ROUNDING_GUARD = 0.01
"""An R2 mean within this many cents of a half cent is ambiguous to round."""
R2_EXPECTED = {"Harbor": 117.15, "Hillcrest": 101.80, "Old Town": 113.85, "Riverside": 111.25}


def load(fixture: Path) -> list[dict[str, str]]:
    with (fixture / "orders.csv").open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check(fixture: Path) -> tuple[list[str], dict[str, object]]:
    rows = load(fixture)
    march = [r for r in rows if r["store"] == "Riverside" and r["order_date"].startswith("2026-03")]
    r1 = len(march)
    units = sum(int(r["quantity"]) for r in march)
    totals: dict[str, list[float]] = defaultdict(list)
    for r in rows:
        if r["order_date"].startswith("2026-02"):
            totals[r["store"]].append(float(r["unit_price"]) * int(r["quantity"]))
    means = {k: sum(v) / len(v) for k, v in sorted(totals.items())}
    facts = {
        "R1 orders": r1,
        "R1 units (a misreading)": units,
        "R2 means": {k: f"{v:.4f}" for k, v in means.items()},
    }
    problems = []
    if r1 != R1_EXPECTED:
        problems.append(f"R1 is {r1}, not the preregistered {R1_EXPECTED}")
    if units == r1:
        problems.append(
            "R1's order count equals its unit count, so a misreading cannot be told apart"
        )
    if {k: round(v, 2) for k, v in means.items()} != R2_EXPECTED:
        problems.append("R2's per-store means differ from the preregistered values")
    if len({round(v, 2) for v in means.values()}) != len(means):
        problems.append("two stores share an R2 mean at cents")
    for k, v in means.items():
        if abs((v * 100) % 1 - 0.5) < ROUNDING_GUARD:
            problems.append(f"R2's {k} mean sits on a rounding boundary at cents")
    return problems, facts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("fixture", type=Path)
    fixture = ap.parse_args().fixture
    problems, facts = check(fixture)
    problems += regenerated_matches(fixture, build_r_sales)
    return report("r-sales", problems, facts)


if __name__ == "__main__":
    sys.exit(main())
