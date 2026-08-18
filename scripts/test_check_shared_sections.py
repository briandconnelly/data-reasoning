"""The shared-section checker must catch drift and must be able to fail.

decisions/001-shared-gate-authority.md (EDA) enumerates the invariants the
costly-collection and data-rules copies must preserve; this checker freezes
bytes and routes any editor to that list.
"""

import importlib.util
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

MIN_SECTION_SIZE = 150
EXPECTED_ERROR_CODE = 2

SCRIPTS = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "check_shared_sections", SCRIPTS / "check-shared-sections.py"
)
css = importlib.util.module_from_spec(spec)
spec.loader.exec_module(css)

REPO = SCRIPTS.parent


def make_fake_repo(tmp_path: Path) -> Path:
    fake = tmp_path / "repo"
    shutil.copytree(REPO / "skills", fake / "skills")
    shutil.copytree(REPO / "scripts" / "shared-sections", fake / "scripts" / "shared-sections")
    return fake


def test_every_target_extracts_real_content():
    """Known positive: each configured section extracts non-trivially."""
    for skill, heading, _slug in css.TARGETS:
        text = (REPO / "skills" / skill / "SKILL.md").read_text(encoding="utf-8")
        block = css.extract_section(text, heading)
        assert block.startswith(heading + "\n")
        assert len(block) > MIN_SECTION_SIZE, (skill, heading)


def test_missing_heading_is_an_error_not_a_pass():
    with pytest.raises(ValueError, match="heading not found"):
        css.extract_section("# nothing here\n", "### Costly collection (modifier, not a route)")


def test_extraction_stops_at_next_same_or_higher_heading():
    text = "## Data Rules\n\nline one\n\n## Next Section\n\nnope\n"
    block = css.extract_section(text, "## Data Rules")
    assert "line one" in block
    assert "nope" not in block


def test_extraction_ignores_headings_inside_code_fences():
    text = "## Data Rules\n\n```\n## Not A Heading\n```\nline two\n\n## Next\n"
    block = css.extract_section(text, "## Data Rules")
    assert "line two" in block
    assert "## Not A Heading" in block


def test_boundary_blank_line_changes_are_detected():
    """The frozen slice is exact bytes, including boundary blank lines."""
    a = css.extract_section("## Data Rules\n\nbody\n\n## Next\n", "## Data Rules")
    b = css.extract_section("## Data Rules\n\nbody\n\n\n## Next\n", "## Data Rules")
    assert a != b


def test_drift_is_detected(tmp_path, capsys):
    """Mutation check: a one-character edit to any copy must fail the run."""
    fake = make_fake_repo(tmp_path)
    victim = fake / "skills" / "exploratory-data-analysis" / "SKILL.md"
    victim.write_text(
        victim.read_text(encoding="utf-8").replace(
            "Cost never changes the route", "Cost rarely changes the route"
        ),
        encoding="utf-8",
    )
    assert css.run(fake, update=frozenset()) == 1
    assert "001-shared-gate-authority.md" in capsys.readouterr().err


def test_update_is_targeted(tmp_path, capsys):
    """--update refreshes only the named golden, so a drift elsewhere still fails."""
    fake = make_fake_repo(tmp_path)
    victim = fake / "skills" / "exploratory-data-analysis" / "SKILL.md"
    old_cost = (
        "Cost never changes the route: a metered warehouse makes profiling more expensive, "
        "not more inferential."
    )
    new_cost = (
        "Cost never changes the route: a metered warehouse makes profiling costlier, "
        "not more inferential."
    )
    old_provenance = (
        "Minimize collection, redact secrets and personal data, and record provenance "
        "for every source."
    )
    new_provenance = (
        "Minimize collection, redact secrets and personal data, and record provenance "
        "for each source."
    )
    victim.write_text(
        victim.read_text(encoding="utf-8")
        .replace(old_cost, new_cost)
        .replace(old_provenance, new_provenance),
        encoding="utf-8",
    )
    css.run(fake, update=frozenset({"eda-costly-collection"}))  # refreshes only that golden
    assert css.run(fake, update=frozenset()) == 1  # the un-updated data-rules drift still fails
    capsys.readouterr()  # drain
    css.run(fake, update=frozenset())
    err = capsys.readouterr().err
    assert "eda-data-rules" in err
    assert "eda-costly-collection" not in err


def test_unknown_update_target_is_an_error():
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "check-shared-sections.py"), "--update", "no-such-slug"],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == EXPECTED_ERROR_CODE


def test_boundary_blank_line_drift_fails_run(tmp_path):
    """A boundary blank-line edit must fail the production comparison path."""
    fake = make_fake_repo(tmp_path)
    victim = fake / "skills" / "exploratory-data-analysis" / "SKILL.md"
    victim.write_text(
        victim.read_text(encoding="utf-8").replace(
            "\n\n## The Lifecycle (explore route)", "\n\n\n## The Lifecycle (explore route)"
        ),
        encoding="utf-8",
    )
    assert css.run(fake, update=frozenset()) == 1


def test_clean_repo_passes():
    assert css.run(REPO, update=frozenset()) == 0
