"""Cell lookup and argument parsing for scripts/run_integration.py; no model is called."""

from __future__ import annotations

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
