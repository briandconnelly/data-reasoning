import importlib.util
import subprocess
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "check-shipped-urls.py"
BASE = "https://github.com/briandconnelly/data-reasoning/blob"
# The dev commit the four scenario-catalog links are pinned to (issue #67).
# It still carries the pre-fix `blob/main/.../tests/scenarios.md` links.
PIN = "5fc87dca1358ef41173924ad0ce1ecb9ef35a4f3"
SKILLS = (
    "hypothesis-driven-analysis",
    "causal-identification-review",
    "exploratory-data-analysis",
    "decision-analysis",
)

spec = importlib.util.spec_from_file_location("check_shipped_urls", SCRIPT)
assert spec is not None
assert spec.loader is not None
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


@pytest.fixture
def tree(tmp_path):
    """A real release tree, built by the release builder itself."""
    out = tmp_path / "release"
    mod.load_builder().build(out)
    return out


def scan_with(tree: Path, text: str) -> list[str]:
    (tree / "docs" / "probe.md").write_text(text, encoding="utf-8")
    return mod.scan(tree, REPO)


def test_valid_pin_passes(tree):
    url = f"{BASE}/{PIN}/skills/hypothesis-driven-analysis/tests/scenarios.md"
    assert scan_with(tree, f"See {url}, which an install does not carry.\n") == []


def test_pinned_path_missing_at_that_sha_fails(tree):
    url = f"{BASE}/{PIN}/skills/hypothesis-driven-analysis/tests/no-such-file.md"
    failures = scan_with(tree, f"See {url}.\n")
    assert len(failures) == 1
    assert "does not exist at" in failures[0]


def test_unknown_sha_fails(tree):
    url = f"{BASE}/{'0' * 40}/README.md"
    failures = scan_with(tree, f"See {url}.\n")
    assert len(failures) == 1
    assert "does not exist at" in failures[0]


def test_main_link_to_an_unshipped_tests_path_fails(tree):
    url = f"{BASE}/main/skills/hypothesis-driven-analysis/tests/scenarios.md"
    failures = scan_with(tree, f"See {url}.\n")
    assert len(failures) == 1
    assert "not in the release tree" in failures[0]


def test_main_link_to_a_shipped_path_passes(tree):
    url = f"{BASE}/main/skills/hypothesis-driven-analysis/SKILL.md"
    assert scan_with(tree, f"See {url}.\n") == []


def test_dev_link_fails(tree):
    url = f"{BASE}/dev/skills/hypothesis-driven-analysis/tests/scenarios.md"
    failures = scan_with(tree, f"See {url}.\n")
    assert len(failures) == 1
    assert "ref `dev`" in failures[0]


def test_short_sha_fails(tree):
    url = f"{BASE}/{PIN[:7]}/skills/hypothesis-driven-analysis/tests/scenarios.md"
    failures = scan_with(tree, f"See {url}.\n")
    assert len(failures) == 1
    assert "40-hex" in failures[0]


def test_the_four_pre_fix_links_fail(tree):
    """Known positive: the SKILL.md intros as they stood at PIN, before #67's fix."""
    for skill in SKILLS:
        old = subprocess.run(
            ["git", "-C", str(REPO), "show", f"{PIN}:skills/{skill}/SKILL.md"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        (tree / "skills" / skill / "SKILL.md").write_text(old, encoding="utf-8")
    failures = mod.scan(tree, REPO)
    assert len(failures) == len(SKILLS)
    for skill, failure in zip(sorted(SKILLS), failures, strict=True):
        assert failure.startswith(f"skills/{skill}/SKILL.md:")
        assert f"blob/main/skills/{skill}/tests/scenarios.md" in failure


def test_the_shipped_tree_passes():
    assert mod.main() == 0
