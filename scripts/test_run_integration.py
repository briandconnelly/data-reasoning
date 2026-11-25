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


@pytest.mark.parametrize("cell", ["I1", "I2", "I3", "I4"])
def test_every_cell_renders_a_relative_data_path(cell):
    assert ri.data_path(cell, Path("/w/int-I3-claude-plugin-1-abc")) == Path("data")


def run_main_with_stubbed_host(monkeypatch, tmp_path, arm, parent=None):
    """Drive main() with no host: record the cwd and prompt the host would get.
    The workspace is created under `parent` (default: a fresh dir in tmp_path)
    with the prefix main() supplies, so nothing is left in the system temp dir."""
    cell, condition, name = arm
    parent = parent or tmp_path / "tmp"
    parent.mkdir(parents=True, exist_ok=True)
    seen = argparse.Namespace(name=name, cwd=None, prompt=None, prefixes=[])
    real_mkdtemp = ri.tempfile.mkdtemp

    def contained_mkdtemp(*, prefix):
        seen.prefixes.append(prefix)
        return real_mkdtemp(prefix=prefix, dir=parent)

    def fake_command(_args, _base, root, prompt):
        seen.cwd, seen.prompt = root, prompt
        return ["host"], {}

    def fake_run(_cmd, _root, _env, base, _args):
        base.with_suffix(".jsonl").write_text("", encoding="utf-8")
        return 0, "completed", 0

    monkeypatch.setattr(ri.tempfile, "mkdtemp", contained_mkdtemp)
    monkeypatch.setattr(ri, "host_command", fake_command)
    monkeypatch.setattr(ri, "run_host", fake_run)
    monkeypatch.setattr(
        subprocess, "run", lambda *_a, **_k: subprocess.CompletedProcess([], 0, stdout="x")
    )
    argv = ["--cell", cell, "--host", "claude", "--condition", condition]
    ri.main([*argv, "--name", name, "--out", str(tmp_path / "out")])
    return seen


@pytest.mark.parametrize("condition", ["plugin", "none"])
@pytest.mark.parametrize("cell", ["I1", "I2", "I3", "I4"])
def test_staged_arm_shows_no_condition(cell, condition, monkeypatch, tmp_path):
    arm = (cell, condition, f"{cell}-claude-{condition}-1")
    seen = run_main_with_stubbed_host(monkeypatch, tmp_path, arm)
    assert seen.prefixes == ["int-arm-"]
    assert seen.cwd.parent == tmp_path / "tmp"
    for leak in ("plugin", "none", seen.name):
        assert leak not in seen.prompt
        assert leak not in seen.cwd.name


def test_a_labelled_temp_parent_is_the_operators_to_avoid(monkeypatch, tmp_path):
    # The harness controls the generated directory name and the prompt, not the
    # temp parent: a label there still reaches the host's cwd, never the prompt.
    label = "I3-claude-plugin-1"
    seen = run_main_with_stubbed_host(
        monkeypatch, tmp_path, ("I3", "plugin", label), parent=tmp_path / label
    )
    assert seen.cwd.name.startswith("int-arm-")
    assert label in str(seen.cwd)
    for leak in ("plugin", label, str(tmp_path)):
        assert leak not in seen.prompt


@pytest.mark.parametrize("cell", ["I1", "I2", "I3", "I4"])
def test_i_cell_prompt_text_is_unchanged_apart_from_the_data_token(cell):
    old = ri.cell_prompt(cell, Path("/d"))
    new = ri.cell_prompt(cell, Path("data"))
    assert old.replace("/d", "data") == new


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
