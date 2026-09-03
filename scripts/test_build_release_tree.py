import json
import subprocess
import sys
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
