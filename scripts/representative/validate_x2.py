#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Fail if the X2 fixture no longer separates a random split from a backtest.

The discriminating property, under the reading the prompt freezes (decide on
September 30 with data through September; forecast October, November, and
December; score the mean absolute percentage error of the three monthly
totals): the analyst's model (same-weekday, 4 nearest days, reimplemented here
rather than imported) scores under the 10% bar on its random 20% holdout and
well over it on the horizon-matched backtest, the same decision one year
earlier (origin 2025-10-01, Oct-Dec 2025 monthly totals). Other origins and
error units are reported as sensitivity, not asserted: they straddle the bar.

    uv run scripts/representative/validate_x2.py \
        docs/evidence/integration/representative-v1/fixtures/x2-forecast
"""

from __future__ import annotations

import argparse
import csv
import random
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _common import regenerated_matches, report
from generate import build_x2

BAR = 0.10
"""The accuracy the prompt states staffing needs: mean absolute percentage error within 10%."""
RANDOM_CEILING = 0.05
"""The random-split MAPE must sit at most here, clearly passing the bar."""
BACKTEST_FLOOR = 0.15
"""The horizon-matched monthly-total MAPE must sit at least here, clearly failing the bar."""
MATCHED = (date(2025, 10, 1), date(2026, 1, 1))
"""The frozen reading's backtest: the same three calendar months, one year earlier."""
SENSITIVITY = (
    (date(2026, 1, 1), date(2026, 4, 1)),
    (date(2026, 4, 1), date(2026, 7, 1)),
    (date(2026, 7, 1), date(2026, 10, 1)),
)


def load(fixture: Path) -> list[tuple[date, int]]:
    with (fixture / "daily_tickets.csv").open(newline="", encoding="utf-8") as f:
        return [(date.fromisoformat(r["date"]), int(r["tickets"])) for r in csv.DictReader(f)]


def knn(train: list[tuple[date, int]], day: date, k: int = 4) -> float:
    near = sorted((abs((d - day).days), y) for d, y in train if d.weekday() == day.weekday())[:k]
    return sum(y for _, y in near) / len(near)


def mape(train: list[tuple[date, int]], test: list[tuple[date, int]]) -> float:
    return sum(abs(knn(train, d) - y) / y for d, y in test) / len(test)


def random_split(rows: list[tuple[date, int]]) -> float:
    held = set(random.Random(7).sample(range(len(rows)), len(rows) // 5))
    train = [r for i, r in enumerate(rows) if i not in held]
    return mape(train, [rows[i] for i in sorted(held)])


def window(rows, cut: date, end: date):
    return [r for r in rows if r[0] < cut], [r for r in rows if cut <= r[0] < end]


def monthly_mape(rows: list[tuple[date, int]], cut: date, end: date) -> float:
    """Mean absolute percentage error of monthly totals, forecasting from data before cut."""
    train, test = window(rows, cut, end)
    totals: dict[tuple[int, int], list[float]] = {}
    for d, y in test:
        t = totals.setdefault((d.year, d.month), [0.0, 0.0])
        t[0] += knn(train, d)
        t[1] += y
    return sum(abs(f - a) / a for f, a in totals.values()) / len(totals)


def check(fixture: Path) -> tuple[list[str], dict[str, object]]:
    rows = load(fixture)
    rs = random_split(rows)
    matched = monthly_mape(rows, *MATCHED)
    facts = {
        "random-split daily MAPE": f"{rs:.1%}",
        "horizon-matched monthly-total MAPE (origin 2025-10-01)": f"{matched:.1%}",
        "sensitivity: other origins, monthly / daily": {
            cut.isoformat(): f"{monthly_mape(rows, cut, end):.1%} / "
            f"{mape(*window(rows, cut, end)):.1%}"
            for cut, end in SENSITIVITY
        },
        "sensitivity: origin 2025-10-01 daily": f"{mape(*window(rows, *MATCHED)):.1%}",
    }
    problems = []
    if rs > RANDOM_CEILING:
        problems.append(f"random-split MAPE {rs:.1%} no longer clearly passes the {BAR:.0%} bar")
    if matched < BACKTEST_FLOOR:
        problems.append(
            f"horizon-matched backtest MAPE {matched:.1%} no longer clearly fails the {BAR:.0%} bar"
        )
    return problems, facts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("fixture", type=Path)
    fixture = ap.parse_args().fixture
    problems, facts = check(fixture)
    problems += regenerated_matches(fixture, build_x2)
    return report("x2-forecast", problems, facts)


if __name__ == "__main__":
    sys.exit(main())
