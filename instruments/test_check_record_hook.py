"""The hook must stay silent on non-records, feed findings back on records,
and surface validator unavailability on records instead of passing silently."""

# ruff: noqa: PLR2004 -- 2 is the hook's documented exit code for "not validated"

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HOOK = REPO / "hooks" / "check_record_hook.py"


def run_hook(payload: dict, plugin_root: str | None = None) -> subprocess.CompletedProcess:
    env = {"CLAUDE_PLUGIN_ROOT": plugin_root if plugin_root is not None else str(REPO)}
    return subprocess.run(
        [sys.executable, str(HOOK)],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def test_non_markdown_is_silent(tmp_path):
    f = tmp_path / "notes.py"
    f.write_text("x = 1\n")
    r = run_hook({"tool_input": {"file_path": str(f)}})
    assert r.returncode == 0
    assert not r.stderr


def test_non_record_markdown_is_silent(tmp_path):
    f = tmp_path / "notes.md"
    f.write_text("# Some Notes\n\nhello\n")
    r = run_hook({"tool_input": {"file_path": str(f)}})
    assert r.returncode == 0
    assert not r.stderr


def test_clean_record_is_silent(tmp_path):
    f = tmp_path / "record.md"
    f.write_text("# VoI Record: is the pull worth it?\n\n## VoI\n\n- Verdict: break-even-only\n")
    r = run_hook({"tool_input": {"file_path": str(f)}})
    assert r.returncode == 0
    assert not r.stderr


def test_record_with_findings_feeds_back(tmp_path):
    f = tmp_path / "record.md"
    f.write_text("# Decision Record: ship or wait?\n\n## Verdict\n\n- Verdict: optimal\n")
    r = run_hook({"tool_input": {"file_path": str(f)}})
    assert r.returncode == 2
    assert "verdict" in r.stderr.lower()
    assert "006-instruments-are-not-a-live-self-check.md" in r.stderr


def test_record_with_unavailable_validator_is_not_a_silent_pass(tmp_path):
    f = tmp_path / "record.md"
    f.write_text("# Decision Record: ship or wait?\n\n## Verdict\n\n- Verdict: optimal\n")
    r = run_hook({"tool_input": {"file_path": str(f)}}, plugin_root=str(tmp_path / "nowhere"))
    assert r.returncode == 2
    assert "not validated" in r.stderr


def test_missing_file_path_is_silent():
    r = run_hook({"tool_input": {}})
    assert r.returncode == 0


def test_garbled_stdin_is_silent():
    r = subprocess.run(
        [sys.executable, str(HOOK)],
        input="not json",
        capture_output=True,
        text=True,
        env={"CLAUDE_PLUGIN_ROOT": str(REPO)},
        check=False,
    )
    assert r.returncode == 0
