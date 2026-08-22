"""check-skill-frontmatter.py must reject the malformed cases it names and
accept a well-formed SKILL.md — run with
uv run --with pytest --with pyyaml python -m pytest -q scripts/test_check_skill_frontmatter.py"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent / "check-skill-frontmatter.py"

GOOD = (
    "---\nname: good-skill\ndescription: Use when testing the frontmatter checker.\n---\n\n# Good\n"
)


def run(tmp_path: Path, dirname: str, text: str) -> subprocess.CompletedProcess:
    d = tmp_path / dirname
    d.mkdir()
    f = d / "SKILL.md"
    f.write_text(text, encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(f)], capture_output=True, text=True, check=False
    )


def test_good_skill_passes(tmp_path):
    assert run(tmp_path, "good-skill", GOOD).returncode == 0


@pytest.mark.parametrize(
    ("dirname", "text"),
    [
        ("good-skill", GOOD.replace("name: good-skill", "name: Bad Name!")),
        ("good-skill", GOOD.replace("name: good-skill", "name: " + "x" * 70)),
        ("good-skill", GOOD.replace("Use when testing the frontmatter checker.", "d" * 1030)),
        (
            "good-skill",
            GOOD.replace("description: Use when testing the frontmatter checker.\n", ""),
        ),
        ("other-dir", GOOD),
        ("good-skill", "# no frontmatter\n"),
    ],
    ids=[
        "bad-chars",
        "long-name",
        "long-description",
        "no-description",
        "name-ne-dir",
        "no-frontmatter",
    ],
)
def test_malformed_skill_fails(tmp_path, dirname, text):
    r = run(tmp_path, dirname, text)
    assert r.returncode == 1, r.stdout + r.stderr
