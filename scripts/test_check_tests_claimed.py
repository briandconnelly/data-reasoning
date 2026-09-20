"""The tests-claimed checker must catch an unrun test and must be able to fail."""

import importlib.util
import re
import sys
import tomllib
from pathlib import Path, PurePosixPath

import pytest

SCRIPTS = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location(
    "check_tests_claimed", SCRIPTS / "check-tests-claimed.py"
)
ctc = importlib.util.module_from_spec(spec)
# Register before exec: a @dataclass under `from __future__ import annotations`
# resolves its module through sys.modules at class-creation time.
sys.modules["check_tests_claimed"] = ctc
spec.loader.exec_module(ctc)

REPO = SCRIPTS.parent
UNREADABLE = 2

HOOK = (
    '{{ id = "suite", language = "python", entry = "{entry}", files = "{files}", '
    "pass_filenames = {pass_filenames} }}"
)


def make_repo(
    tmp_path: Path,
    entry: str = "python -m pytest -q pkg/tests",
    files: str = "^pkg/tests/.*\\\\.py$",
    pass_filenames: str = "false",
) -> Path:
    hook = HOOK.format(entry=entry, files=files, pass_filenames=pass_filenames)
    (tmp_path / "prek.toml").write_text(
        f'[[repos]]\nrepo = "local"\nhooks = [\n  {hook},\n]\n', encoding="utf-8"
    )
    return tmp_path


def test_clean_repo_passes():
    assert ctc.run(REPO) == 0


def test_the_real_repo_has_hooks_and_tests_to_check():
    # Guards the clean pass above against passing because it looked at nothing.
    with (REPO / "prek.toml").open("rb") as fh:
        hooks = ctc.pytest_hooks(tomllib.load(fh))
    assert {"hda-instrument-tests", "instruments-tests"} <= {h.hook_id for h in hooks}
    assert any(h.collects("scripts/test_check_tests_claimed.py", []) for h in hooks)


def test_issue_31_a_test_in_the_unhooked_eda_directory_fails(capsys):
    probe = "skills/exploratory-data-analysis/tests/test_probe.py"
    assert ctc.run(REPO, files=[*ctc.tracked_files(REPO), probe]) == 1
    assert f"UNCLAIMED: {probe}" in capsys.readouterr().err


def test_collected_and_triggered_passes(tmp_path):
    repo = make_repo(tmp_path)
    assert ctc.run(repo, files=["prek.toml", "pkg/tests/test_a.py", "pkg/tests/sub/b_test.py"]) == 0


def test_a_file_argument_claims_only_that_file(tmp_path, capsys):
    repo = make_repo(tmp_path, entry="python -m pytest -q pkg/tests/test_a.py")
    assert ctc.run(repo, files=["pkg/tests/test_a.py", "pkg/tests/test_b.py"]) == 1
    err = capsys.readouterr().err
    assert "UNCLAIMED: pkg/tests/test_b.py" in err
    assert "test_a.py" not in err


def test_a_sibling_directory_sharing_a_prefix_is_not_claimed(tmp_path, capsys):
    repo = make_repo(tmp_path)
    assert ctc.run(repo, files=["pkg/tests/test_a.py", "pkg/tests_extra/test_b.py"]) == 1
    assert "UNCLAIMED: pkg/tests_extra/test_b.py" in capsys.readouterr().err


def test_collected_but_never_triggered_fails(tmp_path, capsys):
    repo = make_repo(tmp_path, files="^pkg/tests/[^/]+\\\\.py$")
    assert ctc.run(repo, files=["pkg/tests/test_a.py", "pkg/tests/sub/test_b.py"]) == 1
    err = capsys.readouterr().err
    assert "UNTRIGGERED: pkg/tests/sub/test_b.py" in err
    assert "suite" in err


def test_collect_ignore_is_the_hold_out(tmp_path):
    repo = make_repo(tmp_path)
    (repo / "pkg" / "tests").mkdir(parents=True)
    (repo / "pkg" / "tests" / "conftest.py").write_text(
        'collect_ignore = ["fixtures/broken", "test_skip.py"]\n', encoding="utf-8"
    )
    held = ["pkg/tests/fixtures/broken/test_bug.py", "pkg/tests/test_skip.py"]
    assert ctc.run(repo, files=["pkg/tests/test_a.py", *held]) == 0
    assert ctc.ignored_over(repo, held[0]) == [PurePosixPath("pkg/tests/fixtures/broken")]
    assert ctc.ignored_over(repo, "pkg/tests/fixtures/test_bug.py") == []


def test_an_explicit_argument_beats_collect_ignore_as_it_does_in_pytest(tmp_path, capsys):
    # pytest collects a path named on its command line even when a conftest.py
    # ignores it, so such a file does run and must therefore be triggered.
    repo = make_repo(
        tmp_path,
        entry="python -m pytest -q pkg/tests pkg/tests/fixtures/broken",
        files="^pkg/tests/[^/]+\\\\.py$",
    )
    (repo / "pkg" / "tests").mkdir(parents=True)
    (repo / "pkg" / "tests" / "conftest.py").write_text(
        'collect_ignore = ["fixtures/broken"]\n', encoding="utf-8"
    )
    broken = "pkg/tests/fixtures/broken/test_bug.py"
    assert ctc.run(repo, files=["pkg/tests/test_a.py", broken]) == 1
    assert f"UNTRIGGERED: {broken}" in capsys.readouterr().err


def test_the_real_s3_bug_hold_out_is_read_from_its_conftest():
    s3 = "skills/hypothesis-driven-analysis/tests/fixtures/s3-bug/test_dateutils.py"
    assert s3 in ctc.tracked_files(REPO)
    assert ctc.ignored_over(REPO, s3)


@pytest.mark.parametrize(
    "body",
    [
        "collect_ignore = [name for name in ()]\n",
        'collect_ignore_glob = ["*_wip.py"]\n',
        'collect_ignore = []\ncollect_ignore += ["x"]\n',
        'collect_ignore = []\ncollect_ignore.append("x")\n',
        'collect_ignore = ["test_a.py"]\ncollect_ignore = []\n',
        'if True:\n    collect_ignore = ["x"]\n',
        "def pytest_ignore_collect(collection_path, config):\n    return True\n",
        "def broken(:\n",
    ],
)
def test_a_conftest_it_cannot_read_exactly_is_an_error_not_a_pass(tmp_path, capsys, body):
    repo = make_repo(tmp_path)
    (repo / "pkg" / "tests").mkdir(parents=True)
    (repo / "pkg" / "tests" / "conftest.py").write_text(body, encoding="utf-8")
    assert ctc.run(repo, files=["pkg/tests/test_a.py"]) == UNREADABLE
    assert "conftest.py" in capsys.readouterr().err


@pytest.mark.parametrize(
    ("kwargs", "message"),
    [
        ({"entry": "python -m pytest -k slow pkg/tests"}, "'-k'"),
        ({"entry": "python -m pytest pkg/tests/test_a.py::test_one"}, "node-id"),
        ({"entry": "python -m pytest -q"}, "names no path"),
        ({"pass_filenames": "true"}, "pass_filenames"),
        ({"pass_filenames": 'false, types = ["python"]'}, "types"),
        ({"pass_filenames": 'false, args = ["--ignore=pkg/tests/test_a.py"]'}, "`args`"),
        ({"entry": "pytest -q pkg/tests"}, "python -m pytest"),
        ({"entry": "python -m pytest -q ../pkg/tests"}, "repo-relative"),
        ({"entry": "python scripts/other.py"}, "no pytest hook"),
    ],
)
def test_a_hook_it_cannot_read_exactly_is_an_error_not_a_pass(tmp_path, capsys, kwargs, message):
    repo = make_repo(tmp_path, **kwargs)
    assert ctc.run(repo, files=["pkg/tests/test_a.py"]) == UNREADABLE
    assert message in capsys.readouterr().err


def test_no_test_files_is_an_error_not_a_pass(tmp_path, capsys):
    assert ctc.run(make_repo(tmp_path), files=["prek.toml"]) == UNREADABLE
    assert "verifies nothing" in capsys.readouterr().err


@pytest.mark.parametrize("config", ["pytest.ini", ".pytest.toml", "pkg/tests/pyproject.toml"])
def test_a_pytest_config_file_is_an_error_not_a_pass(tmp_path, capsys, config):
    assert ctc.run(make_repo(tmp_path), files=[config, "pkg/tests/test_a.py"]) == UNREADABLE
    assert config in capsys.readouterr().err


def test_always_run_counts_as_triggered(tmp_path):
    repo = make_repo(tmp_path, files="^never$", pass_filenames="false, always_run = true")
    assert ctc.run(repo, files=["pkg/tests/test_a.py"]) == 0


def test_a_symlinked_test_file_is_an_error_not_a_pass(tmp_path, capsys):
    repo = make_repo(tmp_path)
    (repo / "pkg" / "tests").mkdir(parents=True)
    (repo / "real.py").write_text("", encoding="utf-8")
    (repo / "pkg" / "tests" / "test_a.py").symlink_to(repo / "real.py")
    assert ctc.run(repo, files=["pkg/tests/test_a.py"]) == UNREADABLE
    assert "symlinked" in capsys.readouterr().err


@pytest.mark.parametrize("key", ["files", "exclude"])
def test_a_top_level_prek_filter_is_an_error_not_a_pass(tmp_path, capsys, key):
    repo = make_repo(tmp_path)
    config = repo / "prek.toml"
    config.write_text(
        f"{key} = '^pkg/tests/test_a\\.py$'\n" + config.read_text(encoding="utf-8"),
        encoding="utf-8",
    )
    assert ctc.run(repo, files=["pkg/tests/test_a.py"]) == UNREADABLE
    assert f"top-level `{key}`" in capsys.readouterr().err


def test_the_real_checker_hook_watches_every_input_the_checker_reads():
    with (REPO / "prek.toml").open("rb") as fh:
        local = next(r for r in tomllib.load(fh)["repos"] if r["repo"] == "local")
    hook = next(h for h in local["hooks"] if h["id"] == "check-tests-claimed")
    watched = re.compile(hook["files"])
    inputs = ["prek.toml", "scripts/check-tests-claimed.py", "a/conftest.py", "conftest.py"]
    inputs += ["a/test_x.py", "x_test.py", *ctc.PYTEST_CONFIG_FILES]
    inputs += [f"a/{name}" for name in ctc.PYTEST_CONFIG_FILES]
    assert [path for path in inputs if not watched.search(path)] == []
    assert not watched.search("scripts/build-release-tree.py")
