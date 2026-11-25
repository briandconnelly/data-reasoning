#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Fail if the X3 fixture's two metrics stop picking different winners.

The discriminating property: at the conventional 0.5 threshold model A has
the higher overall accuracy, while among each model's highest-scored
customers model B's precision is higher, each by a stated margin. The prompt
freezes one pooled list and 500 calls, so the cut that decides is the top
500; B must also win at 1,000 and 1,500 so no reading of the list size moves
the winner. The accuracy contrast is taken at the 0.5 cutoff that models.md
states is the team's reporting cutoff; other cutoffs are sensitivity only
(at 0.9 B's accuracy is higher, and the all-negative baseline ties A).

    uv run scripts/representative/validate_x3.py \
        docs/evidence/integration/representative-v1/fixtures/x3-churn
"""

from __future__ import annotations

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _common import regenerated_matches, report
from generate import build_x3

CUTS = (500, 1000, 1500)
"""Readings of "500 calls a month" against a quarter's holdout."""
THRESHOLD = 0.5
CUTOFF_STATEMENT = "currently reports each model's accuracy at a 0.5 cutoff"
SENSITIVITY_CUTOFFS = (0.3, 0.7, 0.9)
ACCURACY_MARGIN = 0.02
"""A's accuracy must beat B's by at least two points."""
PRECISION_MARGIN = 0.10
"""At every cut, B's precision in its top k must beat A's by at least ten points."""


def load(fixture: Path) -> list[tuple[float, float, int]]:
    with (fixture / "holdout_scores.csv").open(newline="", encoding="utf-8") as f:
        return [
            (float(r["model_a_score"]), float(r["model_b_score"]), int(r["churned"]))
            for r in csv.DictReader(f)
        ]


def accuracy(rows: list[tuple[float, float, int]], col: int, cut: float = THRESHOLD) -> float:
    return sum((r[col] >= cut) == bool(r[2]) for r in rows) / len(rows)


def precision_at(rows: list[tuple[float, float, int]], col: int, k: int) -> tuple[float, bool]:
    """Precision among the top k by score, and whether a tie straddles the cut."""
    ranked = sorted(rows, key=lambda r: r[col], reverse=True)
    tie = ranked[k - 1][col] == ranked[k][col]
    return sum(r[2] for r in ranked[:k]) / k, tie


def check(fixture: Path) -> tuple[list[str], dict[str, object]]:
    rows = load(fixture)
    acc = {"A": accuracy(rows, 0), "B": accuracy(rows, 1)}
    facts: dict[str, object] = {
        "rows": len(rows),
        "churn rate": f"{sum(r[2] for r in rows) / len(rows):.1%}",
        "accuracy at 0.5": {k: f"{v:.1%}" for k, v in acc.items()},
    }
    facts["sensitivity: accuracy A / B at other cutoffs"] = {
        c: f"{accuracy(rows, 0, c):.2%} / {accuracy(rows, 1, c):.2%}" for c in SENSITIVITY_CUTOFFS
    }
    facts["all-negative baseline accuracy"] = f"{1 - sum(r[2] for r in rows) / len(rows):.2%}"
    problems = []
    if CUTOFF_STATEMENT not in (fixture / "models.md").read_text(encoding="utf-8"):
        problems.append("models.md no longer states the team's 0.5 reporting cutoff")
    if not acc["A"] - acc["B"] >= ACCURACY_MARGIN:
        problems.append("overall accuracy no longer picks A by the margin")
    for k in CUTS:
        pa, tie_a = precision_at(rows, 0, k)
        pb, tie_b = precision_at(rows, 1, k)
        facts[f"precision (hits) in top {k}"] = {
            "A": f"{pa:.1%} ({round(pa * k)})",
            "B": f"{pb:.1%} ({round(pb * k)})",
        }
        if not pb - pa >= PRECISION_MARGIN:
            problems.append(f"precision in the top {k} no longer picks B by the margin")
        if tie_a or tie_b:
            problems.append(f"a score tie straddles rank {k}, so the top {k} is ambiguous")
    return problems, facts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("fixture", type=Path)
    fixture = ap.parse_args().fixture
    problems, facts = check(fixture)
    problems += regenerated_matches(fixture, build_x3)
    return report("x3-churn", problems, facts)


if __name__ == "__main__":
    sys.exit(main())
