import json
import re
import subprocess
import sys
from fnmatch import fnmatch
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "scripts" / "build-release-tree.py"
EXPECTED_SKILL_COUNT = 4


def build(out: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(out)], capture_output=True, text=True, check=False
    )


def test_release_tree_contains_runtime_and_excludes_evidence(tmp_path):
    out = tmp_path / "release"
    assert build(out).returncode == 0
    assert (out / ".claude-plugin" / "plugin.json").is_file()
    assert (out / ".claude-plugin" / "marketplace.json").is_file()
    assert (out / "hooks" / "check_record_hook.py").is_file()
    assert (out / "hooks" / "check_record_hook.sh").is_file()
    assert (out / "instruments" / "check_record.py").is_file()
    assert (out / "skills" / "hypothesis-driven-analysis" / "SKILL.md").is_file()
    assert not (out / "skills" / "hypothesis-driven-analysis" / "tests").exists()
    assert not (out / "instruments" / "test_check_record.py").exists()
    assert not list(out.rglob("s18-analytics"))


def test_release_tree_has_exactly_one_skill_per_skill_dir(tmp_path):
    out = tmp_path / "release"
    assert build(out).returncode == 0
    skill_files = list((out / "skills").rglob("SKILL.md"))
    assert len(skill_files) == EXPECTED_SKILL_COUNT
    assert all(p.parent.parent == out / "skills" for p in skill_files)


def test_release_marketplace_points_at_itself(tmp_path):
    out = tmp_path / "release"
    assert build(out).returncode == 0
    mp = json.loads((out / ".claude-plugin" / "marketplace.json").read_text())
    assert mp["plugins"][0]["source"] == "./"


def test_builder_refuses_an_existing_directory_it_did_not_make(tmp_path):
    out = tmp_path / "precious"
    out.mkdir()
    (out / "keep.txt").write_text("do not delete")
    r = build(out)
    assert r.returncode != 0
    assert (out / "keep.txt").exists()
    assert "refusing" in r.stderr


def test_builder_rebuilds_its_own_output(tmp_path):
    out = tmp_path / "release"
    assert build(out).returncode == 0
    assert build(out).returncode == 0
    assert (out / ".data-reasoning-release").is_file()


# --- Completeness: the tree must carry every tracked runtime file ----------
#
# The presence assertions above name a fixed list, so they cannot notice a
# runtime file added later that never reaches the tree. The helpers below
# instead enumerate the runtime directories from the git index -- tracked
# files only, so untracked scratch cannot break them -- and require every
# file under them to be in the built tree unless it is denylisted here.

_RUNTIME_PREFIXES = (
    "hooks/",
    "output-styles/",
    "instruments/",
    ".claude-plugin/",
    ".codex-plugin/",
    ".agents/",
)
_RUNTIME_TOP_LEVEL = ("LICENSE", "README.md")

# Tracked files under a runtime directory that the release tree omits on
# purpose. Glob-matched against the repo-relative path; keep this list short
# and say why each entry is out.
RELEASE_DENYLIST = (
    # The validator's own pytest suite is development evidence, not runtime:
    # an install runs instruments/check_record.py, it does not test it.
    "instruments/test_*.py",
    # A repo-local authoring skill for agents working on this repository
    # (added in bb73b29), not one of the plugin's four shipped skills. Both
    # plugin manifests point their `skills` key at ./skills/, and only the
    # four skills under it ship.
    ".agents/skills/*",
    # Scenario catalogs, fixtures, and archived runs: ~43 MB of evaluation
    # evidence that stays on `main` by the release tree's design.
    "skills/*/tests/*",
)


def is_runtime_path(rel: str) -> bool:
    """Does this repo-relative tracked path belong in an install?"""
    if rel in _RUNTIME_TOP_LEVEL or rel.startswith(_RUNTIME_PREFIXES):
        return True
    # Everything under a skill directory is runtime unless denylisted, so a
    # subtree added later fails here instead of being silently dropped.
    parts = rel.split("/")
    return len(parts) >= 3 and parts[0] == "skills"  # noqa: PLR2004


def tracked_runtime_files() -> list[str]:
    out = subprocess.run(
        ["git", "-C", str(REPO), "ls-files", "-z"], capture_output=True, text=True, check=True
    ).stdout
    tracked = [p for p in out.split("\0") if p]
    assert tracked, "git ls-files returned nothing; the walk below would pass vacuously"
    return [
        p
        for p in tracked
        if is_runtime_path(p) and not any(fnmatch(p, d) for d in RELEASE_DENYLIST)
    ]


def test_the_runtime_walk_sees_more_than_the_fixed_list_names():
    """Guard the instrument: a walk that matched nothing would pass vacuously."""
    found = tracked_runtime_files()
    assert len(found) > len(NAMED_IN_FIXED_LIST)
    assert set(NAMED_IN_FIXED_LIST) <= set(found)
    # Reached only by walking, never by the fixed list -- the class of file
    # this test exists to notice.
    assert "skills/hypothesis-driven-analysis/agents/openai.yaml" in found
    # And the denylist really removes things.
    assert "instruments/test_check_record.py" not in found
    assert not any(p.startswith("skills/hypothesis-driven-analysis/tests/") for p in found)


def test_every_tracked_runtime_file_reaches_the_release_tree(tmp_path):
    out = tmp_path / "release"
    assert build(out).returncode == 0
    missing = [rel for rel in tracked_runtime_files() if not (out / rel).is_file()]
    assert not missing, f"tracked runtime files absent from the release tree: {missing}"


# --- No shipped SKILL.md may cite a path that is not in the tree -----------

# A cited path is a Markdown link target or a backticked token that ends in
# one of these extensions. Anything else backticked is prose.
_CITED_EXTS = ("md", "py", "json", "yaml", "yml", "sh", "toml", "csv", "txt", "log")
_BACKTICKED = re.compile(r"`([^`\n]+)`")
_MD_LINK = re.compile(r"\]\(([^)\s]+)\)")
_PATH_LIKE = re.compile(r"^[\w.@~+-]+(?:/[\w.@~+-]+)*\.(?:" + "|".join(_CITED_EXTS) + r")$")


def cited_relative_paths(text: str) -> set[str]:
    """Relative file paths a reader of this Markdown is pointed at."""
    found = {m.group(1) for m in _MD_LINK.finditer(text)}
    found |= {m.group(1).strip() for m in _BACKTICKED.finditer(text)}
    return {
        p
        for p in found
        if _PATH_LIKE.match(p) and not p.startswith(("/", "#", "http://", "https://"))
    }


def test_the_citation_scan_finds_the_citations_that_are_there():
    """Guard the instrument: an empty scan would make the next test vacuous."""
    cited = cited_relative_paths(
        (REPO / "skills" / "hypothesis-driven-analysis" / "SKILL.md").read_text()
    )
    assert "references/ledger-template.md" in cited
    assert "https://github.com/briandconnelly/data-reasoning" not in cited


def test_no_shipped_skill_cites_a_path_missing_from_the_release_tree(tmp_path):
    out = tmp_path / "release"
    assert build(out).returncode == 0
    skills = sorted((out / "skills").glob("*/SKILL.md"))
    assert len(skills) == EXPECTED_SKILL_COUNT
    dangling = []
    for skill in skills:
        for cited in sorted(cited_relative_paths(skill.read_text())):
            # Cited either from the skill's own directory or from the tree root.
            if not (skill.parent / cited).exists() and not (out / cited).exists():
                dangling.append(f"{skill.parent.name}/SKILL.md -> {cited}")
    assert not dangling, f"citations that dangle in a release install: {dangling}"


# Files the fixed-list assertions at the top of this module already name; the
# walk above must reach strictly more than these.
NAMED_IN_FIXED_LIST = (
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    "hooks/check_record_hook.py",
    "hooks/check_record_hook.sh",
    "instruments/check_record.py",
    "skills/hypothesis-driven-analysis/SKILL.md",
)
