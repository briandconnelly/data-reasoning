"""Cell lookup and argument parsing for scripts/run_integration.py; no model is called."""

from __future__ import annotations

import argparse
import importlib.util
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parent / "run_integration.py"
_spec = importlib.util.spec_from_file_location("run_integration", SCRIPT)
ri = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(ri)

PREREG = SCRIPT.parents[1] / "docs/evidence/integration/representative-v1/prereg.md"
NEW = ("R1", "R2", "X1", "X2", "X3")
HOST_ARGS = argparse.Namespace(timeout=5, host="claude")
DEFAULT_TIMEOUT = 1800  # the harness default, unchanged by this suite

# I1-I4 prompts as they stood before the representative suite was added, so an
# edit that moves one fails here.
I_PROMPTS = {
    "I1": "How many orders in `/d/orders.csv` were placed on 2026-06-10 (UTC)?",
    "I2": "Here's two months of our API event logs (`/d/events.csv`). "
    "Nobody has looked at it closely. Take a look, tell me what's going on, "
    "and if anything looks like a real problem, check whether it actually "
    "holds up before you tell me it's real.",
    "I3": "We rolled out the new checkout flow to the West region on 2026-03-15; "
    "East stayed on the old flow. Median checkout completion time in West "
    "dropped afterwards. How much faster did the new flow make checkout? "
    "I need a number for the Q2 review. Data is in `/d`.",
}


def test_every_cell_id_is_known():
    assert set(ri.CELLS) == {"I1", "I2", "I3", "I4", "R1", "R2", "R3", "R4", "X1", "X2", "X3"}


@pytest.mark.parametrize("cell", sorted(ri.CELLS))
def test_every_fixture_exists(cell):
    assert ri.CELLS[cell][0].is_dir()


@pytest.mark.parametrize("cell", sorted(I_PROMPTS))
def test_existing_prompts_are_unchanged(cell):
    assert ri.cell_prompt(cell, Path("/d")) == I_PROMPTS[cell]


def test_i4_still_reads_problem_md():
    assert "`/d`:" in ri.cell_prompt("I4", Path("/d"))


@pytest.mark.parametrize("cell", NEW)
def test_new_prompts_expand_data_and_match_the_prereg_hash(cell):
    prompt = ri.cell_prompt(cell, Path("/d"))
    assert "{DATA}" not in prompt
    assert "/d" in prompt
    assert f"Prompt SHA-256: `{ri.prompt_sha256(cell)}`." in prereg_section(cell)


def prereg_section(cell):
    """The prereg's `### <cell> —` section, up to the next heading."""
    text = PREREG.read_text(encoding="utf-8")
    start = text.index(f"\n### {cell} \u2014")
    end = text.find("\n#", start + 1)
    return text[start:end]


def test_each_hash_sits_only_in_its_own_cell_section():
    for cell in NEW:
        for other in NEW:
            if other != cell:
                assert ri.prompt_sha256(other) not in prereg_section(cell)


@pytest.mark.parametrize("cell", ["R3", "R4"])
def test_placeholders_refuse_to_run(cell):
    with pytest.raises(SystemExit, match="placeholder"):
        ri.cell_prompt(cell, Path("/d"))


def test_parse_args_accepts_a_new_cell_and_dry_run():
    args = ri.parse_args(
        [
            "--cell",
            "X2",
            "--host",
            "codex",
            "--condition",
            "none",
            "--name",
            "n",
            "--out",
            "o",
            "--dry-run",
        ]
    )
    assert (args.cell, args.host, args.condition, args.dry_run) == ("X2", "codex", "none", True)
    assert args.timeout == DEFAULT_TIMEOUT


def test_parse_args_defaults_dry_run_off():
    args = ri.parse_args(
        ["--cell", "I1", "--host", "claude", "--condition", "plugin", "--name", "n", "--out", "o"]
    )
    assert args.dry_run is False


@pytest.mark.parametrize(
    "argv",
    [
        ["--cell", "X9", "--host", "claude", "--condition", "plugin", "--name", "n", "--out", "o"],
        ["--cell", "X1", "--host", "gemini", "--condition", "plugin", "--name", "n", "--out", "o"],
        ["--cell", "X1", "--host", "claude", "--condition", "half", "--name", "n", "--out", "o"],
        ["--cell", "X1", "--host", "claude", "--condition", "plugin", "--name", "n"],
    ],
)
def test_parse_args_rejects_bad_values(argv):
    with pytest.raises(SystemExit):
        ri.parse_args(argv)


def test_dry_run_stops_before_any_host_call(monkeypatch, capsys, tmp_path):
    def refuse(cmd, *_a, **_k):
        raise AssertionError(f"dry run spawned {cmd!r}")

    monkeypatch.setattr(subprocess, "run", refuse)
    ri.main(
        [
            "--cell",
            "X3",
            "--host",
            "claude",
            "--condition",
            "plugin",
            "--name",
            "n",
            "--out",
            str(tmp_path / "o"),
            "--dry-run",
        ]
    )
    out = capsys.readouterr().out
    assert f"sha256={ri.prompt_sha256('X3')}" in out
    assert "holdout_scores.csv" in out
    assert not (tmp_path / "o").exists()


def _argv(cell, *extra):
    return [
        "--cell",
        cell,
        "--host",
        "claude",
        "--condition",
        "plugin",
        "--name",
        "X-plugin-1",
        "--out",
        "unused",
        *extra,
    ]


def _forbid(monkeypatch):
    def refuse(*a, **_k):
        raise AssertionError(f"called {a!r}")

    monkeypatch.setattr(subprocess, "run", refuse)
    monkeypatch.setattr(ri.tempfile, "mkdtemp", refuse)
    monkeypatch.setattr(ri.shutil, "copytree", refuse)


@pytest.mark.parametrize("cell", ["R3", "R4"])
@pytest.mark.parametrize("extra", [(), ("--dry-run",)], ids=["run", "dry-run"])
def test_placeholders_are_refused_before_any_staging(monkeypatch, cell, extra):
    _forbid(monkeypatch)
    with pytest.raises(SystemExit, match="placeholder"):
        ri.main(_argv(cell, *extra))


def test_a_representative_run_needs_a_pinned_model(monkeypatch):
    _forbid(monkeypatch)
    with pytest.raises(SystemExit, match="--model"):
        ri.main(_argv("X1"))


@pytest.mark.parametrize("cell", NEW)
def test_representative_prompts_carry_no_workspace_path_or_condition(cell):
    prompt = ri.cell_prompt(cell, ri.data_path(cell, Path("/tmp/int-X1-plugin-1-abc")))
    assert "`data" in prompt
    for leak in ("/tmp", "plugin", "none", "int-"):
        assert leak not in prompt


def test_full_catalog_cells_keep_their_absolute_path():
    assert ri.data_path("I1", Path("/w")) == Path("/w/data")


@pytest.mark.parametrize("cell", NEW)
def test_committed_fixture_matches_the_prereg(cell):
    digest, files = ri.verify_cell(cell, ri.CELLS[cell][0])
    assert digest == ri.prompt_sha256(cell)
    assert files


def test_a_changed_fixture_byte_is_refused(tmp_path):
    staged = tmp_path / "data"
    ri.shutil.copytree(ri.CELLS["X3"][0], staged)
    with (staged / "models.md").open("a", encoding="utf-8") as f:
        f.write(" ")
    with pytest.raises(SystemExit, match="fixture bytes"):
        ri.verify_cell("X3", staged)


def test_a_changed_prompt_is_refused(monkeypatch):
    fixture, template = ri.CELLS["X1"]
    monkeypatch.setitem(ri.CELLS, "X1", (fixture, template + " Thanks!"))
    with pytest.raises(SystemExit, match="prompt hash"):
        ri.verify_cell("X1", fixture)


def test_a_timeout_is_an_invalid_execution(monkeypatch, tmp_path):
    def slow(cmd, **_k):
        raise subprocess.TimeoutExpired(cmd, 5)

    monkeypatch.setattr(subprocess, "run", slow)
    code, status, _ = ri.run_host(["host"], tmp_path, {}, tmp_path / "arm", HOST_ARGS)
    assert code is None
    assert status == "invalid-execution: timeout after 5s"


def test_an_empty_transcript_is_an_invalid_execution(monkeypatch, tmp_path):
    monkeypatch.setattr(subprocess, "run", lambda *_a, **_k: subprocess.CompletedProcess([], 0))
    code, status, _ = ri.run_host(["host"], tmp_path, {}, tmp_path / "arm", HOST_ARGS)
    assert code == 0
    assert status.startswith("invalid-execution: empty")


def test_workspace_archive_keeps_new_and_changed_files_only(tmp_path):
    root = tmp_path / "ws"
    ri.shutil.copytree(ri.CELLS["X3"][0], root / "data")
    staged = ri.file_digests(root / "data")
    (root / "ledger.md").write_text("# Investigation: x\n", encoding="utf-8")
    (root / "data" / "notes.md").write_text("scratch\n", encoding="utf-8")
    kept = ri.archive_workspace(root, tmp_path / "arm.workspace", staged)
    assert kept == ["data/notes.md", "ledger.md"]
    assert (tmp_path / "arm.workspace" / "ledger.md").is_file()


def test_codex_gets_the_pinned_model(monkeypatch, tmp_path):
    monkeypatch.setattr(ri.Path, "home", lambda: tmp_path)
    (tmp_path / ".codex").mkdir()
    (tmp_path / ".codex" / "auth.json").write_text("{}", encoding="utf-8")
    args = ri.parse_args(
        [
            "--cell",
            "X1",
            "--host",
            "codex",
            "--condition",
            "none",
            "--name",
            "n",
            "--out",
            "o",
            "--model",
            "m-1",
        ]
    )
    cmd, _ = ri.host_command(args, tmp_path / "arm", tmp_path, "p")
    assert cmd[cmd.index("-m") + 1] == "m-1"


CLAUDE_INIT = '{"type": "system", "subtype": "init", "model": "m"}'
CLAUDE_OK = '{"type": "result", "subtype": "success", "is_error": false, "result": "99"}'
CODEX_OK = '{"type": "turn.completed", "usage": {"input_tokens": 1}}'


def _host_writes(monkeypatch, lines, code):
    def fake(cmd, *, stdout, **_k):
        stdout.write("".join(f"{line}\n" for line in lines))
        return subprocess.CompletedProcess(cmd, code)

    monkeypatch.setattr(subprocess, "run", fake)


@pytest.mark.parametrize(
    "case",
    [
        ("claude", [CLAUDE_INIT, CLAUDE_OK], 0, "completed"),
        ("codex", ['{"type": "thread.started"}', CODEX_OK], 0, "completed"),
        ("claude", [CLAUDE_INIT], 1, "invalid-execution: host exit 1"),
        ("claude", [CLAUDE_INIT, CLAUDE_OK, '{"type": "resu'], 0, "invalid-execution: malformed"),
        ("claude", [CLAUDE_INIT, '{"type": "assistant"}'], 0, "invalid-execution: no terminal"),
        ("codex", ['{"type": "turn.started"}'], 0, "invalid-execution: no terminal"),
        (
            "claude",
            [CLAUDE_INIT, '{"type": "result", "subtype": "error_max_turns", "is_error": true}'],
            0,
            "invalid-execution: no terminal",
        ),
    ],
    ids=["claude-ok", "codex-ok", "exit-1", "truncated", "no-result", "codex-no-turn", "error"],
)
def test_completed_needs_exit_0_clean_lines_and_a_success_event(monkeypatch, tmp_path, case):
    host, lines, code, want = case
    _host_writes(monkeypatch, lines, code)
    args = argparse.Namespace(timeout=5, host=host)
    _, status, _ = ri.run_host(["h"], tmp_path, {}, tmp_path / "arm", args)
    assert status.startswith(want)
    assert (tmp_path / "arm.jsonl").read_text(encoding="utf-8").count("\n") == len(lines)


def _repo(tmp_path):
    repo = tmp_path / "repo"
    for rel in ri.FROZEN_PATHS:
        p = repo / rel
        p = p / "f.txt" if not p.suffix else p
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text("x\n", encoding="utf-8")
    git = [
        "git",
        "-C",
        str(repo),
        "-c",
        "user.name=t",
        "-c",
        "user.email=t@t",
        "-c",
        "commit.gpgsign=false",
    ]
    subprocess.run([*git[:3], "init", "-q"], check=True)
    subprocess.run([*git, "add", "-A"], check=True)
    subprocess.run([*git, "commit", "-qm", "init"], check=True)
    return repo


def test_untracked_arm_output_does_not_trip_the_clean_check(tmp_path):
    repo = _repo(tmp_path)
    arms = repo / "docs/evidence/integration/representative-v1/arms"
    arms.mkdir(parents=True)
    (arms / "X1-claude-plugin-1.jsonl").write_text("{}\n", encoding="utf-8")
    ri.require_clean(repo=repo)


def test_a_modified_fixture_trips_the_clean_check(tmp_path):
    repo = _repo(tmp_path)
    fixture = repo / "docs/evidence/integration/representative-v1/fixtures/f.txt"
    fixture.write_text("changed\n", encoding="utf-8")
    with pytest.raises(SystemExit, match="commit first"):
        ri.require_clean(repo=repo)


def _codex_cmd(command: str, output: str = "") -> dict:
    item = {"type": "command_execution", "command": command, "aggregated_output": output}
    return {"type": "item.completed", "item": item}


def test_codex_route_ignores_skills_named_only_in_command_output():
    # Reading one SKILL.md prints text that names the other skills (#129).
    out = (
        "name: hypothesis-driven-analysis\n"
        "see data-reasoning:decision-analysis and causal-identification-review/SKILL.md"
    )
    events = [_codex_cmd("cat /cache/skills/hypothesis-driven-analysis/SKILL.md", out)]
    assert ri.observed_route(events, "codex") == ["hypothesis-driven-analysis"]


def test_codex_route_counts_each_skill_a_command_names():
    events = [
        _codex_cmd("cat /c/skills/decision-analysis/SKILL.md"),
        _codex_cmd(
            "cat /c/skills/{hypothesis-driven-analysis,causal-identification-review}/SKILL.md"
        ),
    ]
    assert ri.observed_route(events, "codex") == [
        "decision-analysis",
        "hypothesis-driven-analysis",
        "causal-identification-review",
    ]


def test_codex_route_resolves_a_glob_read_from_the_frontmatter_it_printed():
    # `skills/*/SKILL.md` names no skill; the files it printed do, in their `name:` lines.
    out = (
        "---\nname: decision-analysis\ndescription: x\n---\n"
        "body mentions hypothesis-driven-analysis\n"
    )
    events = [_codex_cmd("cat /c/skills/*/SKILL.md", out)]
    assert ri.observed_route(events, "codex") == ["decision-analysis"]


def test_codex_route_is_empty_when_no_skill_file_is_read():
    out = "skills/decision-analysis/SKILL.md\nskills/hypothesis-driven-analysis/SKILL.md"
    assert ri.observed_route([_codex_cmd("rg --files", out)], "codex") == []


@pytest.mark.parametrize(
    "command",
    [
        "cat /c/skills/*-analysis/SKILL.md",
        "cat /c/skills/[dh]*-analysis/SKILL.md",
        "cat /c/plugins/**/SKILL.md",
        "cat /c/skills/decision-analysi?/SKILL.md /c/skills/hypo*/SKILL.md",
    ],
)
def test_codex_route_resolves_a_glob_anywhere_in_the_skill_path(command):
    out = (
        "---\nname: decision-analysis\n---\nmentions causal-identification-review\n"
        "---\nname: hypothesis-driven-analysis\n---\nbody\n"
    )
    assert ri.observed_route([_codex_cmd(command, out)], "codex") == [
        "decision-analysis",
        "hypothesis-driven-analysis",
    ]


def test_codex_route_ignores_a_glob_that_is_not_a_skill_read():
    out = "---\nname: decision-analysis\n---\n"
    assert ri.observed_route([_codex_cmd("ls data/*.csv; cat notes.md", out)], "codex") == []


# Scratch capture and the named-path check (wave-2 preregistration,
# docs/evidence/integration/2026-11-wave2/prereg.md § G).


@pytest.fixture
def temp_root(monkeypatch, tmp_path):
    root = (tmp_path / "tmp").resolve()
    root.mkdir()
    monkeypatch.setattr(ri, "TEMP_ROOTS", (root,))
    return root


def _write(path: Path, text: str = "x\n") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    return path


def test_scratch_capture_finds_a_mktemp_directory_known_only_from_output(temp_root, tmp_path):
    # I4-codex-plugin-3 (2026-11-17) wrote "$D/ledger.md" after `mktemp -d` printed $D.
    ledger = _write(temp_root / "assist.N7pl00" / "ledger.md", "# Investigation: x\n")
    events = [
        _codex_cmd('D=$(mktemp -d /tmp/assist.XXXXXX); echo "$D"', f"{ledger.parent}\n"),
        _codex_cmd('cat > "$D/ledger.md" <<EOF'),
    ]
    paths = ri.mentioned_paths(events, "codex", "done")
    assert ri.scratch_files(paths, tmp_path / "ws", since=0) == [ledger]


def test_scratch_capture_skips_workspace_harness_dirs_old_files_and_other_roots(
    temp_root, tmp_path
):
    ws = temp_root / "int-arm-abc"
    inside = _write(ws / "memo.md")
    plugin = _write(temp_root / "int-plugin-x" / "data-reasoning" / "SKILL.md")
    home = _write(temp_root / "int-codex-home-y" / "sessions" / "s.jsonl")
    old = _write(temp_root / "old" / "ledger.md")
    ri.os.utime(old, (1, 1))
    outside = _write(tmp_path / "home" / "notes.md")
    named = {str(p) for p in (inside, plugin, home, old, outside, temp_root)}
    assert ri.scratch_files(named, ws, since=100) == []


def test_scratch_capture_finds_a_claude_write_and_maps_its_bytes(temp_root, tmp_path):
    log = _write(temp_root / "explore" / "exploration-log.md", "# Exploration: y\n")
    use = {"type": "tool_use", "input": {"file_path": str(log), "content": "."}}
    events = [{"type": "assistant", "message": {"content": [use]}}]
    files = ri.scratch_files(ri.mentioned_paths(events, "claude", ""), tmp_path / "ws", 0)
    mapping = ri.archive_scratch(files, tmp_path / "arm.scratch")
    entry = mapping[str(log)]
    assert (tmp_path / entry["archived"]).read_text(encoding="utf-8") == "# Exploration: y\n"
    assert entry["sha256"] == ri.hashlib.sha256(log.read_bytes()).hexdigest()


def test_named_paths_are_checked_from_outside_after_the_turn(tmp_path):
    ws = tmp_path / "ws"
    rel = _write(ws / "out" / "decision-record.md")
    absolute = _write(tmp_path / "scratch" / "ledger.md")
    locked = _write(tmp_path / "scratch" / "review.md")
    locked.chmod(0)
    final = (
        f"The ledger is at `{absolute}`, the record at out/decision-record.md, "
        f"the review at {locked}, and the log at /gone/exploration-log.md. "
        "See https://example.com/a/b.md, e.g. the notes."
    )
    try:
        got = {d["named"]: d for d in ri.named_paths(final, ws)}
    finally:
        locked.chmod(0o600)
    assert set(got) == {
        str(absolute),
        "out/decision-record.md",
        str(locked),
        "/gone/exploration-log.md",
    }
    assert got[str(absolute)]["readable"]
    assert got[str(absolute)]["sha256"]
    assert got["out/decision-record.md"]["resolved"] == str(rel)
    assert got["out/decision-record.md"]["readable"]
    assert got[str(locked)]["exists"]
    assert not got[str(locked)]["readable"]
    assert not got["/gone/exploration-log.md"]["exists"]


def test_clear_scratch_removes_files_and_empty_dirs_but_never_the_root(temp_root):
    keep = _write(temp_root / "shared" / "other.md")
    gone = _write(temp_root / "shared" / "deep" / "ledger.md")
    solo = _write(temp_root / "solo" / "review.md")
    ri.clear_scratch([gone, solo])
    assert not gone.exists()
    assert not (temp_root / "shared" / "deep").exists()
    assert not (temp_root / "solo").exists()
    assert keep.exists()
    assert temp_root.is_dir()


def test_capture_flags_scratch_under_a_preexisting_entry_and_checks_before_clearing(
    temp_root, tmp_path
):
    earlier = temp_root / "earlier"
    earlier.mkdir()
    before = ri.temp_entries()
    fresh = _write(temp_root / "new-dir" / "ledger.md")
    reused = _write(earlier / "ledger.md")
    events = [_codex_cmd(f"cat {fresh} {reused}")]
    files = ri.scratch_files(ri.mentioned_paths(events, "codex", ""), tmp_path / "ws", 0)
    named = ri.named_paths(f"See {fresh}.", tmp_path / "ws")
    got = ri.capture(files, named, before, tmp_path / "arm", clear=True)
    assert got["scratch_files"][str(fresh)]["top_entry_preexisted"] is False
    assert got["scratch_files"][str(reused)]["top_entry_preexisted"] is True
    assert got["named_paths"][0]["readable"]  # checked before clearing
    assert not fresh.exists()
    assert not reused.exists()
    assert got["scratch_cleared"]


def test_an_i_cell_arm_archives_its_workspace_scratch_and_named_paths(
    monkeypatch, temp_root, tmp_path
):
    scratch = temp_root / "assist-review" / "ledger.md"

    def fake_run(cmd, *_a, **kw):
        if cmd[0] == "git":
            return subprocess.CompletedProcess(cmd, 0, stdout="abc\n", stderr="")
        if cmd[1:] == ["--version"]:
            return subprocess.CompletedProcess(cmd, 0, stdout="2.1.0\n", stderr="")
        _write(scratch, "# Investigation: x\n")
        _write(Path(kw["cwd"]) / "memo.md", "# memo\n")
        use = {"type": "tool_use", "input": {"file_path": str(scratch), "content": "."}}
        events = [
            {"type": "system", "subtype": "init", "model": "m"},
            {"type": "assistant", "message": {"content": [use]}},
            {"type": "result", "subtype": "success", "result": f"Ledger: {scratch}; memo.md"},
        ]
        kw["stdout"].write("\n".join(ri.json.dumps(e) for e in events) + "\n")
        return subprocess.CompletedProcess(cmd, 0)

    workspace = temp_root / "int-arm-ws"
    workspace.mkdir()
    monkeypatch.setattr(subprocess, "run", fake_run)
    monkeypatch.setattr(ri.tempfile, "mkdtemp", lambda **_k: str(workspace))
    out = tmp_path / "o"
    argv = ["--cell", "I4", "--host", "claude", "--condition", "none", "--name", "I4-a"]
    ri.main([*argv, "--out", str(out), "--clear-scratch"])
    manifest = ri.json.loads((out / "I4-a.manifest.json").read_text(encoding="utf-8"))
    assert manifest["status"] == "completed"
    assert manifest["workspace_files"] == ["memo.md"]
    assert list(manifest["scratch_files"]) == [str(scratch)]
    archived = out / manifest["scratch_files"][str(scratch)]["archived"]
    assert archived.read_text(encoding="utf-8") == "# Investigation: x\n"
    assert {d["named"]: d["readable"] for d in manifest["named_paths"]} == {
        str(scratch): True,
        "memo.md": True,
    }
    assert not scratch.exists()
    assert manifest["data_modified"] is False
