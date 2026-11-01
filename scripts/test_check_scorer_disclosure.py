"""The scorer-disclosure checker must flag new run records lacking a Scorer line."""

import importlib.util
import subprocess
import sys
from datetime import date
from pathlib import Path

SCRIPTS = Path(__file__).resolve().parent
SCRIPT = SCRIPTS / "check-scorer-disclosure.py"
spec = importlib.util.spec_from_file_location("check_scorer_disclosure", SCRIPT)
csd = importlib.util.module_from_spec(spec)
spec.loader.exec_module(csd)


def test_record_date_parses_the_filename():
    assert csd.record_date(Path("2026-11-02-s1.md")) == date(2026, 11, 2)
    assert csd.record_date(Path("notes.md")) is None


def test_new_record_without_scorer_line_is_flagged(tmp_path):
    p = tmp_path / "2026-11-02-s1.md"
    p.write_text("# S1\n\nDate: 2026-11-02\n\n| a |\n")
    assert csd.missing_scorer([p]) == [p]


def test_new_record_with_scorer_line_passes(tmp_path):
    p = tmp_path / "2026-11-02-s1.md"
    p.write_text("# S1\n\nDate: 2026-11-02\nScorer: the dispatching session (Fable)\n")
    assert csd.missing_scorer([p]) == []


def test_old_record_without_scorer_line_is_exempt(tmp_path):
    p = tmp_path / "2026-07-16-s1.md"
    p.write_text("# S1\n")
    assert csd.missing_scorer([p]) == []


def test_the_real_tree_passes():
    result = subprocess.run([sys.executable, str(SCRIPT)], check=False, capture_output=True)
    assert result.returncode == 0
