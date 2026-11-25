#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Fail if the X1 fixture no longer flips the action when uncertainty is carried.

The discriminating property: plugging the trial's observed defect rate in as
if it were known picks Brightline, while integrating over a posterior for
that rate (under both a uniform and a Jeffreys prior) picks Acme, because the
contract's penalty cliff sits inside the posterior's plausible range.
Everything is recomputed from the CSVs and contract_terms.md; nothing is
imported from the generator except for the byte-compare.

    uv run scripts/representative/validate_x1.py \
        docs/evidence/integration/representative-v1/fixtures/x1-supplier
"""

from __future__ import annotations

import argparse
import csv
import math
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from _common import regenerated_matches, report
from generate import build_x1

MARGIN = 0.25
"""Each decision must win by at least this fraction of the loser's expected
cost, so a flip is not a rounding artefact."""


def beta_sf(x: float, a: float, b: float, steps: int = 20_000) -> float:
    """P(p > x) for p ~ Beta(a, b), by Simpson's rule on the density."""
    lnorm = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)

    def pdf(p: float) -> float:
        if p <= 0 or p >= 1:
            return 0.0
        return math.exp(lnorm + (a - 1) * math.log(p) + (b - 1) * math.log1p(-p))

    h = (1 - x) / steps
    total = pdf(x) + pdf(1.0)
    for i in range(1, steps):
        total += (4 if i % 2 else 2) * pdf(x + i * h)
    return total * h / 3


def terms(fixture: Path) -> dict[str, float]:
    text = (fixture / "contract_terms.md").read_text(encoding="utf-8")

    def num(pattern: str) -> float:
        m = re.search(pattern, text)
        if not m:
            raise SystemExit(f"contract_terms.md: no match for {pattern!r}")
        return float(m.group(1).replace(",", ""))

    return {
        "volume": num(r"Volume: ([\d,]+) units"),
        "defect_cost": num(r"costs \$([\d,.]+) in rework"),
        "penalty_rate": num(r"exceeds ([\d.]+)%") / 100,
        "penalty": num(r"penalty of \$([\d,]+)"),
    }


def counts(fixture: Path) -> tuple[int, int, int, int]:
    with (fixture / "brightline_trial.csv").open(newline="", encoding="utf-8") as f:
        trial = [int(r["defective"]) for r in csv.DictReader(f)]
    with (fixture / "acme_history.csv").open(newline="", encoding="utf-8") as f:
        hist = list(csv.DictReader(f))
    return (
        len(trial),
        sum(trial),
        sum(int(r["units_received"]) for r in hist),
        sum(int(r["defective_units"]) for r in hist),
    )


def expected_cost(t: dict[str, float], rate: float, p_over: float) -> float:
    return t["volume"] * rate * t["defect_cost"] + p_over * t["penalty"]


def check(fixture: Path) -> tuple[list[str], dict[str, object]]:
    t = terms(fixture)
    bn, bd, an, ad = counts(fixture)
    facts: dict[str, object] = {"brightline trial": f"{bd}/{bn}", "acme history": f"{ad}/{an}"}
    problems = []

    # Point estimate: the observed rate treated as known;
    # the cliff binds only if that rate is over it.
    point = {}
    for name, n, d in (("acme", an, ad), ("brightline", bn, bd)):
        r = d / n
        point[name] = expected_cost(t, r, 1.0 if r > t["penalty_rate"] else 0.0)
    facts["point-estimate cost"] = {k: round(v) for k, v in point.items()}
    if not point["brightline"] < (1 - MARGIN) * point["acme"]:
        problems.append("the point estimate no longer picks Brightline by the margin")

    for prior, a0 in (("uniform", 1.0), ("jeffreys", 0.5)):
        post = {}
        for name, n, d in (("acme", an, ad), ("brightline", bn, bd)):
            a, b = d + a0, n - d + a0
            post[name] = expected_cost(t, a / (a + b), beta_sf(t["penalty_rate"], a, b))
        facts[f"posterior cost ({prior})"] = {k: round(v) for k, v in post.items()}
        if not post["acme"] < (1 - MARGIN) * post["brightline"]:
            problems.append(
                f"carrying the uncertainty ({prior} prior) no longer picks Acme by the margin"
            )
    return problems, facts


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("fixture", type=Path)
    fixture = ap.parse_args().fixture
    problems, facts = check(fixture)
    problems += regenerated_matches(fixture, build_x1)
    return report("x1-supplier", problems, facts)


if __name__ == "__main__":
    sys.exit(main())
