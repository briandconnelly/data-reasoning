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


def test_x1_fails_when_the_point_estimate_no_longer_picks_brightline(tmp_path):
    generate.build_x1(tmp_path / "x1", trial_units=150, trial_defects=5)
    problems, _ = validate_x1.check(tmp_path / "x1")
    assert any("point estimate no longer picks Brightline" in p for p in problems)


def test_x2_fails_when_the_random_split_no_longer_passes(tmp_path):
    generate.build_x2(tmp_path / "x2", noise=0.15)
    problems, _ = validate_x2.check(tmp_path / "x2")
    assert any("random-split" in p for p in problems)


def _write_scores(fixture, rows):
    fixture.mkdir()
    shutil.copy2(FIXTURES / "x3-churn" / "models.md", fixture / "models.md")
    with (fixture / "holdout_scores.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["customer_id", "model_a_score", "model_b_score", "churned"])
        for i, (a, b, y) in enumerate(rows):
            w.writerow([f"C{i:05d}", f"{a:.6f}", f"{b:.6f}", y])


def test_x3_fails_when_a_tie_straddles_the_cut(tmp_path):
    rows = [(r[0], 0.5, r[2]) for r in validate_x3.load(FIXTURES / "x3-churn")]
    _write_scores(tmp_path / "x3", rows)
    problems, _ = validate_x3.check(tmp_path / "x3")
    assert any("tie straddles rank 500" in p for p in problems)


def test_x3_fails_when_b_loses_at_a_deeper_cut(tmp_path):
    # B's top 500 all churn, its next 1,000 none; A ranks the other 500 churners first.
    n, top, deep = 2000, 500, 1500
    rows = []
    for i in range(n):
        churned = int(i < top or i >= deep)
        b = 1 - i / n
        a = 0.4 + (i - deep) / n if i >= deep else (0.3 - i / n / 10 if i < top else 0.01)
        rows.append((a, b, churned))
    _write_scores(tmp_path / "x3", rows)
    problems, _ = validate_x3.check(tmp_path / "x3")
    assert any("top 1000 no longer picks B" in p for p in problems)


def test_x2_fails_when_the_series_has_no_annual_cycle(tmp_path):
    generate.build_x2(tmp_path / "x2", annual_amplitude=0.0)
    problems, _ = validate_x2.check(tmp_path / "x2")
    assert any("horizon-matched" in p for p in problems)


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
    assert any("unit count is" in p for p in problems)


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


def test_x1_fails_when_the_shipped_rate_is_not_tied_to_the_received_rate(tmp_path):
    fixture = tmp_path / "x1-supplier"
    shutil.copytree(FIXTURES / "x1-supplier", fixture)
    terms = fixture / "contract_terms.md"
    text = terms.read_text(encoding="utf-8").replace(
        validate_x1.PASS_THROUGH, "and half are reworked"
    )
    terms.write_text(text, encoding="utf-8")
    problems, _ = validate_x1.check(fixture)
    assert any("shipped rate" in p for p in problems)


def test_x3_fails_when_the_reporting_cutoff_is_unstated(tmp_path):
    fixture = tmp_path / "x3-churn"
    shutil.copytree(FIXTURES / "x3-churn", fixture)
    (fixture / "models.md").write_text("# Candidate churn models\n", encoding="utf-8")
    problems, _ = validate_x3.check(fixture)
    assert any("0.5 reporting cutoff" in p for p in problems)
