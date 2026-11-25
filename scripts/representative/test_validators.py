"""Each representative-v1 validator passes its committed fixture and fails a degenerate one.

A validator that cannot fail is not evidence, so every check below builds a
copy that has lost exactly the property the validator guards and asserts the
validator reports it.
"""

from __future__ import annotations

import csv
import shutil
import sys
from pathlib import Path

import pytest

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import generate  # noqa: E402
import validate_r  # noqa: E402
import validate_x1  # noqa: E402
import validate_x2  # noqa: E402
import validate_x3  # noqa: E402
from _common import regenerated_matches  # noqa: E402

FIXTURES = HERE.parents[1] / "docs/evidence/integration/representative-v1/fixtures"

CASES = [
    ("r-sales", validate_r, generate.build_r_sales),
    ("x1-supplier", validate_x1, generate.build_x1),
    ("x2-forecast", validate_x2, generate.build_x2),
    ("x3-churn", validate_x3, generate.build_x3),
]


@pytest.mark.parametrize(("name", "validator", "builder"), CASES, ids=[c[0] for c in CASES])
def test_committed_fixture_passes(name, validator, builder):
    problems, _ = validator.check(FIXTURES / name)
    assert problems == []
    assert regenerated_matches(FIXTURES / name, builder) == []


def test_x1_fails_when_the_trial_is_large_enough_to_settle_the_rate(tmp_path):
    generate.build_x1(tmp_path / "x1", trial_units=3000, trial_defects=20)
    problems, _ = validate_x1.check(tmp_path / "x1")
    assert any("no longer picks Acme" in p for p in problems)


def test_x2_fails_when_the_series_has_no_annual_cycle(tmp_path):
    generate.build_x2(tmp_path / "x2", annual_amplitude=0.0)
    problems, _ = validate_x2.check(tmp_path / "x2")
    assert any("rolling-origin" in p for p in problems)


def test_x3_fails_when_model_b_is_calibrated(tmp_path):
    generate.build_x3(tmp_path / "x3", b_inflation=0.0)
    problems, _ = validate_x3.check(tmp_path / "x3")
    assert any("accuracy no longer picks A" in p for p in problems)


def test_x3_fails_when_model_b_ranks_no_better(tmp_path):
    generate.build_x3(tmp_path / "x3", b_noise=3.0)
    problems, _ = validate_x3.check(tmp_path / "x3")
    assert any("precision in the top 500" in p for p in problems)


def test_r_fails_when_a_row_moves_the_answer(tmp_path):
    fixture = tmp_path / "r-sales"
    shutil.copytree(FIXTURES / "r-sales", fixture)
    path = fixture / "orders.csv"
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    drop = next(i for i, r in enumerate(rows) if r[2] == "Riverside" and r[1].startswith("2026-03"))
    del rows[drop]
    with path.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f, lineterminator="\n").writerows(rows)
    problems, _ = validate_r.check(fixture)
    assert any("R1 is 98" in p for p in problems)


def test_r_fails_when_units_equal_orders(tmp_path):
    fixture = tmp_path / "r-sales"
    shutil.copytree(FIXTURES / "r-sales", fixture)
    path = fixture / "orders.csv"
    with path.open(newline="", encoding="utf-8") as f:
        rows = list(csv.reader(f))
    for r in rows[1:]:
        r[5] = "1"
    with path.open("w", newline="", encoding="utf-8") as f:
        csv.writer(f, lineterminator="\n").writerows(rows)
    problems, _ = validate_r.check(fixture)
    assert any("equals its unit count" in p for p in problems)


def test_byte_compare_catches_an_edited_fixture(tmp_path):
    fixture = tmp_path / "x3-churn"
    shutil.copytree(FIXTURES / "x3-churn", fixture)
    (fixture / "models.md").write_text("edited\n", encoding="utf-8")
    assert any("models.md" in p for p in regenerated_matches(fixture, generate.build_x3))
