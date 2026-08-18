"""The description-freeze checker must catch drift and must be able to fail."""

import importlib.util
import shutil
from pathlib import Path

import pytest

SCRIPTS = Path(__file__).resolve().parent
MIN_DESC_LENGTH = 200
spec = importlib.util.spec_from_file_location(
    "check_description_freeze", SCRIPTS / "check-description-freeze.py"
)
cdf = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cdf)

REPO = SCRIPTS.parent


def make_fake_repo(tmp_path: Path) -> Path:
    fake = tmp_path / "repo"
    shutil.copytree(REPO / "skills", fake / "skills")
    shutil.copytree(
        REPO / "scripts" / "frontmatter-descriptions",
        fake / "scripts" / "frontmatter-descriptions",
    )
    return fake


def test_every_description_extracts_real_content():
    for skill in cdf.SKILLS:
        desc = cdf.read_description(REPO / "skills" / skill / "SKILL.md")
        assert len(desc) > MIN_DESC_LENGTH, skill


def test_broken_frontmatter_is_an_error_not_a_pass(tmp_path):
    bad = tmp_path / "SKILL.md"
    bad.write_text("---\ndescription: [unclosed\n---\nbody\n", encoding="utf-8")
    with pytest.raises(ValueError, match="frontmatter"):
        cdf.read_description(bad)


def test_drift_is_detected(tmp_path, capsys):
    fake = make_fake_repo(tmp_path)
    victim = fake / "skills" / "decision-analysis" / "SKILL.md"
    victim.write_text(
        victim.read_text(encoding="utf-8").replace(
            "binary uncertain proposition", "binary or ternary uncertain proposition"
        ),
        encoding="utf-8",
    )
    assert cdf.run(fake, update=frozenset()) == 1
    assert "006-description-freeze-until-measured.md" in capsys.readouterr().err


def test_clean_repo_passes():
    assert cdf.run(REPO, update=frozenset()) == 0
