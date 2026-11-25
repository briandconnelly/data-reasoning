#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Build the representative-v1 fixtures (issue #115) deterministically.

The preregistration (`docs/evidence/integration/representative-v1/prereg.md`)
owns what each fixture is for and its ground truth; this script only writes
bytes. Every builder owns a local `random.Random` seeded from SEED plus its
own offset, so editing one builder cannot move another fixture's bytes.
Builders take their discriminating parameters as keyword arguments so the
validators' tests can build a deliberately degenerate copy.

    uv run scripts/representative/generate.py docs/evidence/integration/representative-v1/fixtures
"""

from __future__ import annotations

import argparse
import csv
import math
import random
from datetime import date, timedelta
from pathlib import Path

SEED = 20261124

FIXTURES = ("r-sales", "x1-supplier", "x2-forecast", "x3-churn")


def _write_csv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)


# --- R1, R2: an order table a direct answer settles -------------------------

STORES = ("Riverside", "Hillcrest", "Old Town", "Harbor")
PRODUCTS = {
    "kettle": 34.0,
    "toaster": 29.5,
    "blender": 64.0,
    "coffee grinder": 42.0,
    "mixing bowl set": 18.75,
    "chef knife": 55.0,
    "cutting board": 22.0,
    "dutch oven": 89.0,
}


def build_r_sales(out: Path) -> None:
    rng = random.Random(SEED + 1)
    out.mkdir(parents=True, exist_ok=True)
    rows: list[list[object]] = []
    day = date(2026, 1, 1)
    oid = 10001
    while day <= date(2026, 4, 30):
        for _ in range(rng.randint(6, 14)):
            store = rng.choices(STORES, weights=(4, 3, 2, 3))[0]
            product = rng.choice(sorted(PRODUCTS))
            rows.append(
                [oid, day.isoformat(), store, product, PRODUCTS[product], rng.randint(1, 4)]
            )
            oid += 1
        day += timedelta(days=1)
    _write_csv(
        out / "orders.csv",
        ["order_id", "order_date", "store", "product", "unit_price", "quantity"],
        rows,
    )


# --- X1: a supplier switch whose payoff has a penalty cliff ------------------

X1_VOLUME = 100_000
X1_DEFECT_COST = 15.0
X1_PENALTY = 1_000_000
X1_PENALTY_RATE = 0.03
X1_INCUMBENT_UNITS = 50_000
X1_INCUMBENT_DEFECTS = 1_000
X1_FIRST_YEAR_MONTHS = 3  # Oct-Dec 2025


def build_x1(out: Path, *, trial_units: int = 150, trial_defects: int = 1) -> None:
    rng = random.Random(SEED + 2)
    out.mkdir(parents=True, exist_ok=True)
    bad = set(rng.sample(range(trial_units), trial_defects))
    start = date(2026, 9, 14)
    _write_csv(
        out / "brightline_trial.csv",
        ["unit_id", "inspected_on", "defective"],
        [
            [
                f"BL-{i + 1:04d}",
                (start + timedelta(days=i * 5 // trial_units)).isoformat(),
                int(i in bad),
            ]
            for i in range(trial_units)
        ],
    )
    months = 12
    per_month = X1_INCUMBENT_UNITS // months
    remainder = X1_INCUMBENT_UNITS - per_month * months
    units = [per_month + (1 if m < remainder else 0) for m in range(months)]
    # Spread the incumbent's defects so each month sits near 2.0% but the total is exact.
    defects = [
        round(u * X1_INCUMBENT_DEFECTS / X1_INCUMBENT_UNITS) + rng.randint(-6, 6) for u in units
    ]
    defects[-1] += X1_INCUMBENT_DEFECTS - sum(defects)
    _write_csv(
        out / "acme_history.csv",
        ["month", "units_received", "defective_units"],
        [
            [
                f"2025-{m + 10:02d}" if m < X1_FIRST_YEAR_MONTHS else f"2026-{m - 2:02d}",
                units[m],
                defects[m],
            ]
            for m in range(months)
        ],
    )
    (out / "contract_terms.md").write_text(
        "# Supply contract terms for next year\n"
        "\n"
        f"- Volume: {X1_VOLUME:,} units over the year, all from one supplier.\n"
        "- Unit price: identical for both suppliers.\n"
        f"- Each defective unit that reaches us costs ${X1_DEFECT_COST:.0f}"
        " in rework and returns.\n"
        f"- Our retail partner's quality clause: if the annual defect rate"
        " of the units we ship exceeds"
        f" {X1_PENALTY_RATE:.0%}, we owe a one-time penalty of ${X1_PENALTY:,}.\n"
        "- The supplier is chosen once for the year; there is no mid-year switch.\n",
        encoding="utf-8",
    )


# --- X2: a forecast that interpolates well and extrapolates badly ------------

X2_START = date(2024, 10, 1)
X2_DAYS = 730
X2_WEEKDAY = (1.12, 1.08, 1.04, 1.0, 0.96, 0.82, 0.74)


def build_x2(out: Path, *, annual_amplitude: float = 0.30, noise: float = 0.03) -> None:
    rng = random.Random(SEED + 3)
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for t in range(X2_DAYS):
        d = X2_START + timedelta(days=t)
        season = 1 + annual_amplitude * math.cos(
            2 * math.pi * (d.timetuple().tm_yday - 15) / 365.25
        )
        level = 1200 * (1 + 0.10 * t / 365) * season * X2_WEEKDAY[d.weekday()]
        rows.append([d.isoformat(), max(0, round(level * (1 + rng.gauss(0, noise))))])
    _write_csv(out / "daily_tickets.csv", ["date", "tickets"], rows)
    (out / "analyst_model.py").write_text(ANALYST_MODEL, encoding="utf-8")
    (out / "analyst_notes.md").write_text(
        "# Ticket volume model\n"
        "\n"
        "Model: for each day, average the ticket counts of the 4 nearest days"
        " in the training data that fall on the same weekday.\n"
        "Evaluation: 20% of days held out at random (seed 7), model fit on the other 80%.\n"
        "Result: mean absolute percentage error on the held-out days is 3.6%.\n"
        "Code: `analyst_model.py` in this folder reproduces the number.\n",
        encoding="utf-8",
    )


ANALYST_MODEL = '''"""Analyst's ticket model: same-weekday nearest-neighbour average."""

import csv
import random
import sys
from datetime import date


def load(path):
    with open(path, newline="") as f:
        return [(date.fromisoformat(r["date"]), int(r["tickets"])) for r in csv.DictReader(f)]


def predict(train, day, k=4):
    same = [(abs((d - day).days), y) for d, y in train if d.weekday() == day.weekday()]
    same.sort()
    return sum(y for _, y in same[:k]) / k


def main(path):
    rows = load(path)
    rng = random.Random(7)
    test = set(rng.sample(range(len(rows)), len(rows) // 5))
    train = [r for i, r in enumerate(rows) if i not in test]
    errs = [abs(predict(train, rows[i][0]) - rows[i][1]) / rows[i][1] for i in sorted(test)]
    print(f"held-out MAPE: {100 * sum(errs) / len(errs):.1f}%")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "daily_tickets.csv")
'''


# --- X3: two churn models whose winner depends on the metric -----------------

X3_N = 10_000


def build_x3(out: Path, *, b_noise: float = 0.25, b_inflation: float = 0.25) -> None:
    rng = random.Random(SEED + 4)
    out.mkdir(parents=True, exist_ok=True)
    rows = []
    for i in range(X3_N):
        risk = rng.gauss(0, 1)
        p = 1 / (1 + math.exp(-(-2.6 + 1.6 * risk)))
        churned = int(rng.random() < p)
        # A: calibrated but sees the risk through heavy noise.
        a_logit = -2.6 + 1.6 * (0.55 * risk + 0.835 * rng.gauss(0, 1))
        # B: sees the risk sharply, but its scores are shifted up across the board.
        b_logit = -2.6 + 2.6 * (risk + b_noise * rng.gauss(0, 1))
        a = 1 / (1 + math.exp(-a_logit))
        b = b_inflation + (1 - b_inflation) / (1 + math.exp(-b_logit))
        rows.append([f"C{i + 1:05d}", f"{a:.6f}", f"{b:.6f}", churned])
    _write_csv(
        out / "holdout_scores.csv",
        ["customer_id", "model_a_score", "model_b_score", "churned"],
        rows,
    )
    (out / "models.md").write_text(
        "# Candidate churn models\n"
        "\n"
        "Both models were trained on the same data and scored on"
        " last quarter's holdout customers.\n"
        "Each score is the model's churn probability for that customer;"
        " `churned` is what actually happened.\n",
        encoding="utf-8",
    )


BUILDERS = {
    "r-sales": build_r_sales,
    "x1-supplier": build_x1,
    "x2-forecast": build_x2,
    "x3-churn": build_x3,
}


def build_all(root: Path) -> None:
    for name, builder in BUILDERS.items():
        builder(root / name)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("root", type=Path)
    build_all(ap.parse_args().root)


if __name__ == "__main__":
    main()
