"""Exercise install diagnostics against release and contaminated packages."""

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_release_install_check_and_fixture_detection(tmp_path):
    root = tmp_path / "release"
    subprocess.run(
        [sys.executable, str(REPO / "scripts/build-release-tree.py"), str(root)], check=True
    )
    command = [sys.executable, str(root / "instruments/check_install.py")]
    clean = subprocess.run(command, capture_output=True, text=True, check=False)
    assert clean.returncode == 0, clean.stdout + clean.stderr
    assert "Host activation/trust was NOT tested" in clean.stdout
    fixture = root / "skills/hypothesis-driven-analysis/tests/fixtures/rogue/SKILL.md"
    fixture.parent.mkdir(parents=True)
    fixture.write_text("---\nname: rogue\n---\n")
    dirty = subprocess.run(command, capture_output=True, text=True, check=False)
    assert dirty.returncode == 1
    assert "Unexpected discoverable skill:" in dirty.stdout
    assert "rogue/SKILL.md" in dirty.stdout
    fixture.unlink()
    (root / "skills/decision-analysis/SKILL.md").unlink()
    missing = subprocess.run(command, capture_output=True, text=True, check=False)
    assert missing.returncode == 1
    assert "Missing shipped skill: skills/decision-analysis/SKILL.md" in missing.stdout


def test_missing_validator_is_not_a_pass(tmp_path):
    root = tmp_path / "release"
    subprocess.run(
        [sys.executable, str(REPO / "scripts/build-release-tree.py"), str(root)], check=True
    )
    (root / "instruments/check_record.py").unlink()
    result = subprocess.run(
        [sys.executable, str(root / "instruments/check_install.py")],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert "validator missing" in result.stdout


def test_missing_manifest_hook_config_is_not_a_pass(tmp_path):
    root = tmp_path / "release"
    subprocess.run(
        [sys.executable, str(REPO / "scripts/build-release-tree.py"), str(root)], check=True
    )
    manifest = root / ".codex-plugin/plugin.json"
    manifest.write_text(manifest.read_text().replace("./hooks/hooks.json", "./hooks/missing.json"))
    result = subprocess.run(
        [sys.executable, str(root / "instruments/check_install.py")],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 1
    assert "missing.json" in result.stdout
