"""The scorer-disclosure checker must flag new run records lacking a Scorer line."""

import importlib.util
import re
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


def test_undated_record_is_flagged(tmp_path):
    p = tmp_path / "t15-trigger.md"
    p.write_text("# T15\n")
    assert csd.missing_scorer([p]) == [p]


def test_record_dated_exactly_on_the_cutoff_is_checked(tmp_path):
    p = tmp_path / "2026-11-01-x.md"
    p.write_text("# X\n")
    assert csd.missing_scorer([p]) == [p]


def test_fenced_scorer_line_does_not_count(tmp_path):
    p = tmp_path / "2026-11-02-s1.md"
    p.write_text("# S1\n\nDate: 2026-11-02\n```\nScorer: example\n```\n\n| a |\n")
    assert csd.missing_scorer([p]) == [p]


def test_commented_scorer_line_does_not_count(tmp_path):
    p = tmp_path / "2026-11-02-s1.md"
    p.write_text("# S1\n\nDate: 2026-11-02\n<!-- Scorer: x -->\n\n| a |\n")
    q = tmp_path / "2026-11-03-s1.md"
    q.write_text("# S1\n\nDate: 2026-11-03\n<!--\nScorer: x\n-->\n\n| a |\n")
    assert csd.missing_scorer([p, q]) == [p, q]


def test_scorer_line_after_the_first_table_does_not_count(tmp_path):
    p = tmp_path / "2026-11-02-s1.md"
    p.write_text("# S1\n\nDate: 2026-11-02\n\n| a |\n| - |\n\nScorer: late\n")
    assert csd.missing_scorer([p]) == [p]


def test_the_real_tree_passes():
    result = subprocess.run([sys.executable, str(SCRIPT)], check=False, capture_output=True)
    assert result.returncode == 0


def test_default_record_paths_include_agents_skills():
    paths = [p.relative_to(csd.REPO).as_posix() for p in csd.default_record_paths()]
    assert any(p.startswith(".agents/skills/") for p in paths)
    assert any(p.startswith("skills/") for p in paths)


def test_hook_regex_matches_both_trees():
    text = (csd.REPO / "prek.toml").read_text()
    line = next(ln for ln in text.splitlines() if 'id = "check-scorer-disclosure"' in ln)
    raw = re.search(r'files = "((?:[^"\\]|\\.)*)"', line).group(1)
    pattern = re.compile(raw.replace("\\\\", "\\"))
    assert pattern.search(".agents/skills/x/tests/runs/2026-11-02-r.md")
    assert pattern.search("skills/x/tests/runs/2026-11-02-r.md")
    assert not pattern.search("skills/x/tests/runs/artifacts/2026-11-02-r.md")
