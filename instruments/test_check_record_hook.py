"""Hook behavior tests. Failure semantics are owned by
skills/hypothesis-driven-analysis/decisions/006-instruments-are-not-a-live-self-check.md."""

# ruff: noqa: PLR2004 -- 2 is the hook's documented exit code for "not validated"

import importlib.util
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
HOOK = REPO / "hooks" / "check_record_hook.py"
SIGNATURE_RECORD = "# Decision Record: ship?\n\n## Verdict\n\n- Verdict: optimal\n"

_spec = importlib.util.spec_from_file_location("check_record_hook", HOOK)
assert _spec
assert _spec.loader
hook_module = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(hook_module)


def run_hook(
    payload: dict, plugin_root: str | None = None, root_var: str = "CLAUDE_PLUGIN_ROOT"
) -> subprocess.CompletedProcess:
    env = {root_var: plugin_root if plugin_root is not None else str(REPO)}
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
    f.write_text(
        "# VoI Record: is the pull worth it?\n\n## VoI\n\n- Route: voi\n"
        "- Pending decision: ship vs wait\n- Signal model: a 2-week holdout\n"
        "- Value basis: expected loss avoided\n- Value calculation: 0.4 x 3 = 1.2\n"
        "- Upper bound: 1.5\n- Cost: 1.0\n- Verdict: break-even-only\n"
    )
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


def test_validator_exit_1_with_no_findings_is_not_validated(tmp_path):
    fake_root = tmp_path / "root"
    (fake_root / "instruments").mkdir(parents=True)
    (fake_root / "instruments" / "check_record.py").write_text(
        "import sys\n"
        "print('Traceback (most recent call last): boom', file=sys.stderr)\n"
        "sys.exit(1)\n"
    )
    f = tmp_path / "record.md"
    f.write_text("# VoI Record: x\n\n## VoI\n\n- Verdict: worth-it\n")
    r = run_hook({"tool_input": {"file_path": str(f)}}, plugin_root=str(fake_root))
    assert r.returncode == 2
    assert "not validated" in r.stderr
    assert "structural findings" not in r.stderr


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


def test_unreadable_candidate_is_not_a_silent_pass(tmp_path):
    r = run_hook({"tool_input": {"file_path": str(tmp_path / "missing.md")}})
    assert r.returncode == 2
    assert "not validated" in r.stderr


def test_users_own_investigation_note_is_left_alone(tmp_path):
    f = tmp_path / "outage.md"
    f.write_text("# Investigation: prod outage 2026-08-20\n\nTimeline...\n")
    r = run_hook({"tool_input": {"file_path": str(f)}})
    assert r.returncode == 0
    assert not r.stderr


def test_signature_match_without_required_heading_reaches_validator_and_is_silent(tmp_path):
    """Drives the validator-exit-2-with-empty-stderr branch, not the sniff branch."""
    f = tmp_path / "note.md"
    f.write_text("# Investigation: just a note\n\nno headings here\n")
    r = run_hook({"tool_input": {"file_path": str(f)}})
    assert r.returncode == 0
    assert not r.stderr


def test_unknown_validator_exit_code_is_not_a_silent_pass(tmp_path):
    fake_root = tmp_path / "root"
    (fake_root / "instruments").mkdir(parents=True)
    (fake_root / "instruments" / "check_record.py").write_text("import sys\nsys.exit(7)\n")
    f = tmp_path / "record.md"
    f.write_text("# VoI Record: x\n\n## VoI\n\n- Verdict: worth-it\n")
    r = run_hook({"tool_input": {"file_path": str(f)}}, plugin_root=str(fake_root))
    assert r.returncode == 2
    assert "not validated" in r.stderr


def test_invalid_utf8_in_the_title_is_unreadable_not_a_silent_skip(tmp_path):
    """A bad byte in the title must not mutate the signature into a non-match:
    that would exit clean without the validator ever running."""
    f = tmp_path / "record.md"
    f.write_bytes(b"# Investigation\xe9: prod outage\n\n## Problem\n\n- x\n")
    r = run_hook({"tool_input": {"file_path": str(f)}})
    assert r.returncode == 2, r.stderr
    assert "not validated" in r.stderr


def test_invalid_byte_past_a_non_record_title_is_still_silent(tmp_path):
    """The title proves the file is not a record, so a bad byte later in the
    read-ahead buffer must not produce validator feedback."""
    f = tmp_path / "notes.md"
    f.write_bytes(b"# Ordinary notes\n\n" + b"a" * 5000 + b"\xff\n")
    r = run_hook({"tool_input": {"file_path": str(f)}})
    assert r.returncode == 0, r.stderr
    assert not r.stderr


def test_record_under_frontmatter_reaches_the_validator(tmp_path):
    f = tmp_path / "record.md"
    f.write_text(
        "---\ntags: [x]\n---\n# Decision Record: ship?\n\n## Verdict\n\n- Verdict: optimal\n"
    )
    r = run_hook({"tool_input": {"file_path": str(f)}})
    assert r.returncode == 2
    assert "verdict" in r.stderr.lower()


def test_record_under_oversized_frontmatter_is_not_a_silent_pass(tmp_path):
    """The closing delimiter falls past the scan budget, so the sniff cannot
    tell a record from an ordinary file. Indeterminate is not a clean pass."""
    f = tmp_path / "record.md"
    padding = "".join(f"k{i}: {'v' * 60}\n" for i in range(1200))
    f.write_text(
        "---\n" + padding + "---\n# Decision Record: ship?\n\n## Verdict\n\n- Verdict: optimal\n"
    )
    assert f.stat().st_size > hook_module.FRONTMATTER_SCAN_BYTES  # the case really is oversized
    r = run_hook({"tool_input": {"file_path": str(f)}})
    assert r.returncode == 2, r.stderr
    assert "not validated" in r.stderr


def test_unterminated_frontmatter_seen_whole_stays_a_non_record(tmp_path):
    """The other side of the boundary: a document opening with a horizontal
    rule is smaller than the budget and has been read entirely, so there is
    nothing left to discover. It is not a record, and failing it closed would
    fire "not validated" on ordinary Markdown."""
    f = tmp_path / "notes.md"
    f.write_text("---\n\nNotes that open with a horizontal rule.\n" + "filler\n" * 200)
    assert f.stat().st_size < hook_module.FRONTMATTER_SCAN_BYTES  # the case really is short
    r = run_hook({"tool_input": {"file_path": str(f)}})
    assert r.returncode == 0, r.stderr
    assert not r.stderr


def test_record_under_long_frontmatter_reaches_the_validator(tmp_path):
    f = tmp_path / "record.md"
    padding = "".join(f"k{i}: {'v' * 60}\n" for i in range(120))  # > 4,096 bytes
    f.write_text(
        "---\n" + padding + "---\n# Decision Record: ship?\n\n## Verdict\n\n- Verdict: optimal\n"
    )
    r = run_hook({"tool_input": {"file_path": str(f)}})
    assert r.returncode == 2
    assert "verdict" in r.stderr.lower()


def hook_command() -> str:
    cfg = json.loads((REPO / "hooks" / "hooks.json").read_text(encoding="utf-8"))
    return cfg["hooks"]["PostToolUse"][0]["hooks"][0]["command"]


def run_command_without_python(payload: dict, tmp_path: Path) -> subprocess.CompletedProcess:
    """Run the configured shell command with a PATH that has sh, sed, head, grep,
    cat but no python3."""
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    for tool in ("sh", "sed", "head", "grep", "cat"):
        real = shutil.which(tool)
        assert real, tool
        (bin_dir / tool).symlink_to(real)
    env = {"CLAUDE_PLUGIN_ROOT": str(REPO), "PATH": str(bin_dir)}
    return subprocess.run(
        [str(bin_dir / "sh"), "-c", hook_command()],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def test_without_python_a_record_write_is_not_validated(tmp_path):
    f = tmp_path / "record.md"
    f.write_text(SIGNATURE_RECORD)
    r = run_command_without_python({"tool_input": {"file_path": str(f)}}, tmp_path)
    assert r.returncode == 2
    assert "not validated" in r.stderr
    assert "python3" in r.stderr


def test_without_python_a_non_record_write_is_silent(tmp_path):
    f = tmp_path / "notes.md"
    f.write_text("# Meeting notes\n")
    r = run_command_without_python({"tool_input": {"file_path": str(f)}}, tmp_path)
    assert r.returncode == 0
    assert not r.stderr


def test_without_python_a_source_write_is_silent(tmp_path):
    f = tmp_path / "main.py"
    f.write_text("print('hi')\n")
    r = run_command_without_python({"tool_input": {"file_path": str(f)}}, tmp_path)
    assert r.returncode == 0
    assert not r.stderr


def test_with_python_the_wrapper_reaches_the_python_hook(tmp_path):
    f = tmp_path / "record.md"
    f.write_text(SIGNATURE_RECORD)
    r = subprocess.run(
        ["sh", "-c", hook_command()],
        input=json.dumps({"tool_input": {"file_path": str(f)}}),
        capture_output=True,
        text=True,
        env={**os.environ, "CLAUDE_PLUGIN_ROOT": str(REPO)},
        check=False,
    )
    assert r.returncode == 2
    assert "structural findings" in r.stderr


def test_shell_sniff_signatures_match_python_signatures():
    """The shell wrapper's record-signature list must not drift from
    SIGNATURES in hooks/check_record_hook.py."""
    sh_text = (REPO / "hooks" / "check_record_hook.sh").read_text(encoding="utf-8")
    match = re.search(r"grep -q -E '\^# \(([^)]+)\): '", sh_text)
    assert match, "could not find the signature grep in check_record_hook.sh"
    sh_signatures = {f"# {name}: " for name in match.group(1).split("|")}

    assert sh_signatures == set(hook_module.SIGNATURES)


# 2026-09-15 Codex review: the hook read only `tool_input.file_path`, so on
# Codex -- whose apply_patch payload carries the patch in `tool_input.command`
# -- a record with findings exited 0 in silence.

BAD_RECORD = "# Decision Record: ship or wait?\n\n## Verdict\n\n- Verdict: optimal\n"


def codex_patch(*paths: str) -> str:
    body = "".join(f"*** Add File: {p}\n+# Decision Record: x\n" for p in paths)
    return f"*** Begin Patch\n{body}*** End Patch\n"


def test_codex_apply_patch_payload_reports_findings(tmp_path):
    f = tmp_path / "record.md"
    f.write_text(BAD_RECORD)
    payload = {
        "tool_name": "apply_patch",
        "cwd": str(tmp_path),
        "tool_input": {"command": codex_patch("record.md")},
    }
    r = run_hook(payload)
    assert r.returncode == 2
    assert "verdict" in r.stderr.lower()
    assert str(f) in r.stderr


def test_codex_update_file_path_is_resolved_against_cwd(tmp_path):
    (tmp_path / "sub").mkdir()
    f = tmp_path / "sub" / "record.md"
    f.write_text(BAD_RECORD)
    patch = "*** Begin Patch\n*** Update File: sub/record.md\n@@\n-x\n+y\n*** End Patch\n"
    r = run_hook(
        {"tool_name": "apply_patch", "cwd": str(tmp_path), "tool_input": {"command": patch}}
    )
    assert r.returncode == 2
    assert str(f) in r.stderr


def test_codex_patch_over_a_non_record_is_silent(tmp_path):
    (tmp_path / "notes.md").write_text("# Notes\n")
    r = run_hook(
        {
            "tool_name": "apply_patch",
            "cwd": str(tmp_path),
            "tool_input": {"command": codex_patch("notes.md")},
        }
    )
    assert r.returncode == 0
    assert not r.stderr


def test_codex_patch_writing_two_records_reports_both(tmp_path):
    for name in ("a.md", "b.md"):
        (tmp_path / name).write_text(BAD_RECORD)
    r = run_hook(
        {
            "tool_name": "apply_patch",
            "cwd": str(tmp_path),
            "tool_input": {"command": codex_patch("a.md", "b.md")},
        }
    )
    assert r.returncode == 2
    assert str(tmp_path / "a.md") in r.stderr
    assert str(tmp_path / "b.md") in r.stderr


def test_plugin_root_env_var_is_honored(tmp_path):
    f = tmp_path / "record.md"
    f.write_text(BAD_RECORD)
    r = run_hook({"tool_input": {"file_path": str(f)}}, root_var="PLUGIN_ROOT")
    assert r.returncode == 2
    assert "verdict" in r.stderr.lower()


def test_shell_command_payload_is_not_covered(tmp_path):
    """A record created by a shell command is outside both payload shapes;
    the README says so. This test pins that it is silence, not a crash."""
    f = tmp_path / "record.md"
    f.write_text(BAD_RECORD)
    r = run_hook({"tool_name": "Bash", "tool_input": {"command": f"cat > {f}"}})
    assert r.returncode == 0
    assert not r.stderr


def test_candidate_paths_shapes(tmp_path):
    assert hook_module.candidate_paths({"tool_input": {"file_path": "/x/y.md"}}) == ["/x/y.md"]
    patch = (
        "*** Begin Patch\n*** Update File: a.md\n*** Move to: b.md\n"
        "*** Delete File: c.md\n*** End Patch"
    )
    got = hook_module.candidate_paths({"cwd": str(tmp_path), "tool_input": {"command": patch}})
    assert got == [str(tmp_path / "b.md")]  # the move vacates a.md; c.md is deleted
    assert hook_module.candidate_paths({"tool_input": {"command": "echo hi"}}) == []
    assert hook_module.candidate_paths({"tool_input": "garbage"}) == []


# Codex review pass 1: a rename validated the vacated source path and warned
# that it could not be read; a title-free Update File patch on an existing
# record slipped through the no-Python fallback in silence.


def test_a_rename_validates_only_the_destination(tmp_path):
    dest = tmp_path / "renamed.md"
    dest.write_text(BAD_RECORD)
    patch = (
        "*** Begin Patch\n*** Update File: old.md\n*** Move to: renamed.md\n"
        "@@\n-x\n+y\n*** End Patch\n"
    )
    r = run_hook(
        {"tool_name": "apply_patch", "cwd": str(tmp_path), "tool_input": {"command": patch}}
    )
    assert r.returncode == 2
    assert str(dest) in r.stderr
    assert "could not be read" not in r.stderr


def test_a_rename_of_a_non_record_is_silent(tmp_path):
    (tmp_path / "README.md").write_text("# readme\n")
    patch = "*** Begin Patch\n*** Update File: gone.md\n*** Move to: README.md\n*** End Patch\n"
    r = run_hook(
        {"tool_name": "apply_patch", "cwd": str(tmp_path), "tool_input": {"command": patch}}
    )
    assert r.returncode == 0
    assert not r.stderr


def codex_payload(tmp_path: Path, patch: str) -> dict:
    return {"tool_name": "apply_patch", "cwd": str(tmp_path), "tool_input": {"command": patch}}


def test_without_python_a_patch_adding_a_record_is_not_validated(tmp_path):
    r = run_command_without_python(codex_payload(tmp_path, codex_patch("record.md")), tmp_path)
    assert r.returncode == 2
    assert "not validated" in r.stderr


def test_without_python_a_title_free_edit_to_a_record_is_not_validated(tmp_path):
    (tmp_path / "record.md").write_text(SIGNATURE_RECORD)
    patch = "*** Begin Patch\n*** Update File: record.md\n@@\n-x\n+y\n*** End Patch\n"
    r = run_command_without_python(codex_payload(tmp_path, patch), tmp_path)
    assert r.returncode == 2
    assert "not validated" in r.stderr
    assert str(tmp_path / "record.md") in r.stderr


def test_without_python_a_patch_to_a_non_record_is_silent(tmp_path):
    (tmp_path / "notes.md").write_text("# Notes\n")
    patch = "*** Begin Patch\n*** Update File: notes.md\n@@\n-x\n+y\n*** End Patch\n"
    r = run_command_without_python(codex_payload(tmp_path, patch), tmp_path)
    assert r.returncode == 0
    assert not r.stderr


def test_without_python_a_patch_to_source_files_is_silent(tmp_path):
    patch = "*** Begin Patch\n*** Update File: main.py\n@@\n-x\n+y\n*** End Patch\n"
    r = run_command_without_python(codex_payload(tmp_path, patch), tmp_path)
    assert r.returncode == 0
    assert not r.stderr


def test_without_python_a_spaced_filename_is_one_candidate(tmp_path):
    (tmp_path / "decision record.md").write_text(SIGNATURE_RECORD)
    patch = "*** Begin Patch\n*** Update File: decision record.md\n@@\n-x\n+y\n*** End Patch\n"
    r = run_command_without_python(codex_payload(tmp_path, patch), tmp_path)
    assert r.returncode == 2
    assert str(tmp_path / "decision record.md") in r.stderr


def test_a_spaced_filename_reaches_the_python_hook(tmp_path):
    f = tmp_path / "decision record.md"
    f.write_text(BAD_RECORD)
    patch = "*** Begin Patch\n*** Update File: decision record.md\n@@\n-x\n+y\n*** End Patch\n"
    r = run_hook(codex_payload(tmp_path, patch))
    assert r.returncode == 2
    assert str(f) in r.stderr
