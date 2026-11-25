#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Fail if the X2 fixture no longer separates a random split from a backtest.

The discriminating property: the analyst's model (same-weekday, 4 nearest
days, reimplemented here rather than imported) scores under the 10% bar on a
random 20% holdout and well over it on a rolling-origin backtest that
forecasts each of the last four quarters from the data before it.

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
"""The rolling-origin MAPE must sit at least here, clearly failing the bar."""
HORIZON = 91
ORIGINS = 4


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


def backtest(rows: list[tuple[date, int]]) -> list[float]:
    out = []
    for j in range(ORIGINS, 0, -1):
        cut = len(rows) - j * HORIZON
        out.append(mape(rows[:cut], rows[cut : cut + HORIZON]))
    return out


def check(fixture: Path) -> tuple[list[str], dict[str, object]]:
    rows = load(fixture)
    rs = random_split(rows)
    bt = backtest(rows)
    overall = sum(bt) / len(bt)
    facts = {
        "random-split MAPE": f"{rs:.1%}",
        "rolling-origin MAPE per quarter": [f"{e:.1%}" for e in bt],
        "rolling-origin MAPE mean": f"{overall:.1%}",
    }
    problems = []
    if rs > RANDOM_CEILING:
        problems.append(f"random-split MAPE {rs:.1%} no longer clearly passes the {BAR:.0%} bar")
    if overall < BACKTEST_FLOOR:
        problems.append(
            f"rolling-origin MAPE {overall:.1%} no longer clearly fails the {BAR:.0%} bar"
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
