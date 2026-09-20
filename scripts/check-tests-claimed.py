#!/usr/bin/env python3
"""Fail when a tracked test file is one no prek hook would ever run.

Every suite in this repo runs through a local prek hook whose entry is
`python -m pytest <paths>`. Nothing else collects tests, so a test file that
no such hook reaches is silently unrun, and it stays green forever (issue #31:
skills/exploratory-data-analysis/tests/ lost its only hook and nothing noticed).

A tracked test file passes when some pytest hook both

  collects it  -- the file is one of the entry's path arguments, or sits under
                  a directory argument; and
  is triggered -- the hook's `files` regex (less its `exclude`) matches the
                  test file's own path, so editing the test re-runs it under a
                  plain `prek run`, not only under --all-files.

A deliberate hold-out has one home: a conftest.py `collect_ignore` entry, the
same mechanism that keeps pytest itself away from the file. This checker reads
those lists rather than keeping an exemption list of its own.

The checker fails closed. A pytest entry or a conftest.py it cannot read
exactly is exit 2, never a guess.
"""

from __future__ import annotations

import ast
import re
import shlex
import subprocess
import sys
import tomllib
from dataclasses import dataclass
from pathlib import Path, PurePosixPath

# pytest's default python_files. No pytest configuration file exists in this
# repo; run() fails if one appears, since it could change what is collected.
TEST_NAME = re.compile(r"^(test_.*|.*_test)\.py$")

PYTEST_CONFIG_FILES = (
    "pytest.ini",
    "pytest.toml",
    ".pytest.toml",
    "pyproject.toml",
    "tox.ini",
    "setup.cfg",
)

# Hook keys that narrow which staged files trigger a hook, beyond the `files`
# and `exclude` this checker models. A pytest hook carrying one is unreadable.
UNMODELLED_FILTERS = ("types", "types_or", "exclude_types", "stages")

# conftest.py hooks that decide collection in code, which no static read can follow.
COLLECTION_HOOKS = frozenset(
    {"pytest_ignore_collect", "pytest_collect_file", "pytest_collect_directory"}
)

# Entry options known to take no value. Anything else might swallow the next
# token as its value, and then the path arguments cannot be read reliably.
VALUELESS_OPTIONS = frozenset({"-q", "-v", "-x", "-s"})


class Unreadable(Exception):
    """An input this checker will not guess about."""


@dataclass(frozen=True)
class PytestHook:
    hook_id: str
    paths: tuple[str, ...]
    files: str | None
    exclude: str | None
    always_run: bool

    def collects(self, test_file: str, ignored: list[PurePosixPath]) -> bool:
        """`ignored` is every collect_ignore path at or over the test file.

        pytest applies collect_ignore only to what it finds while recursing: a
        path named on the command line is collected even when a conftest.py
        lists it. So an ignore entry holds the file out of this hook only when
        it lies strictly below the argument that would otherwise reach it.
        """
        path = PurePosixPath(test_file)
        for arg in map(PurePosixPath, self.paths):
            if path != arg and arg not in path.parents:
                continue
            if not any(arg in ig.parents for ig in ignored):
                return True
        return False

    def triggered_by(self, test_file: str) -> bool:
        if self.always_run:
            return True
        if self.files is not None and not re.search(self.files, test_file):
            return False
        return not (self.exclude is not None and re.search(self.exclude, test_file))


def pytest_paths(hook_id: str, entry: str) -> tuple[str, ...] | None:
    """The path arguments of a pytest entry, or None when it is not one."""
    tokens = shlex.split(entry)
    if "pytest" not in tokens:
        return None
    if tokens[:3] != ["python", "-m", "pytest"]:
        raise Unreadable(f"hook {hook_id}: a pytest entry must start `python -m pytest`")
    paths = []
    for token in tokens[3:]:
        if token.startswith("-"):
            if token not in VALUELESS_OPTIONS:
                raise Unreadable(
                    f"hook {hook_id}: pytest option {token!r} is not one this checker knows "
                    f"to take no value; add it to VALUELESS_OPTIONS or teach the parser"
                )
            continue
        if "::" in token:
            raise Unreadable(f"hook {hook_id}: node-id argument {token!r} claims part of a file")
        if PurePosixPath(token).is_absolute() or ".." in PurePosixPath(token).parts:
            raise Unreadable(f"hook {hook_id}: path {token!r} is not a plain repo-relative path")
        paths.append(str(PurePosixPath(token)))
    if not paths:
        raise Unreadable(f"hook {hook_id}: pytest entry names no path, so it collects from cwd")
    return tuple(paths)


def pytest_hooks(config: dict) -> list[PytestHook]:
    # prek applies top-level files/exclude before any hook's own filters.
    for key in ("files", "exclude"):
        if key in config:
            raise Unreadable(
                f"prek.toml: a top-level `{key}` narrows every hook's trigger, and this "
                f"checker models only hook-level `files` and `exclude`"
            )
    hooks = []
    for repo in config.get("repos", []):
        if repo.get("repo") != "local":
            continue
        for hook in repo.get("hooks", []):
            paths = pytest_paths(hook["id"], hook.get("entry", ""))
            if paths is None:
                continue
            if hook.get("args"):
                raise Unreadable(
                    f"hook {hook['id']}: `args` are appended to the entry unread; put "
                    f"pytest's arguments in `entry`, where this checker parses them"
                )
            if hook.get("pass_filenames", True):
                raise Unreadable(
                    f"hook {hook['id']}: pass_filenames is not false, so the staged "
                    f"filenames join the entry's paths and the collection is not fixed"
                )
            unmodelled = [key for key in UNMODELLED_FILTERS if key in hook]
            if unmodelled:
                raise Unreadable(
                    f"hook {hook['id']}: {', '.join(unmodelled)} narrows which files trigger "
                    f"the hook, and this checker models only `files` and `exclude`"
                )
            hooks.append(
                PytestHook(
                    hook["id"],
                    paths,
                    hook.get("files"),
                    hook.get("exclude"),
                    hook.get("always_run", False),
                )
            )
    return hooks


def collect_ignore(conftest: Path) -> list[str]:
    """The literal collect_ignore list a conftest.py assigns, [] when it has none."""
    try:
        tree = ast.parse(conftest.read_text(encoding="utf-8"))
    except SyntaxError as exc:
        raise Unreadable(f"{conftest}: not parseable: {exc}") from exc
    ignored: list[str] = []
    plain_targets = set()
    for node in ast.walk(tree):
        if (
            isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            and node.name in COLLECTION_HOOKS
        ):
            raise Unreadable(f"{conftest}: {node.name} decides collection in code")
    for node in tree.body:
        if not isinstance(node, ast.Assign):
            continue
        for target in node.targets:
            if not isinstance(target, ast.Name) or target.id != "collect_ignore":
                continue
            try:
                value = ast.literal_eval(node.value)
            except ValueError as exc:
                raise Unreadable(f"{conftest}: collect_ignore is not a literal") from exc
            if not isinstance(value, list) or not all(isinstance(v, str) for v in value):
                raise Unreadable(f"{conftest}: collect_ignore is not a list of strings")
            if plain_targets:
                raise Unreadable(f"{conftest}: collect_ignore is assigned more than once")
            ignored.extend(value)
            plain_targets.add(id(target))
    # Any other mention -- collect_ignore_glob, `+=`, `.append(...)`, an
    # annotated or conditional rebinding -- is a list this read did not capture.
    for node in ast.walk(tree):
        if (
            isinstance(node, ast.Name)
            and node.id.startswith("collect_ignore")
            and id(node) not in plain_targets
        ):
            raise Unreadable(
                f"{conftest}: line {node.lineno}: only one plain top-level "
                f"`collect_ignore = [...]` of string literals is understood"
            )
    return ignored


def ignored_over(repo: Path, test_file: str) -> list[PurePosixPath]:
    """Every collect_ignore path, from any conftest.py above, at or over the file."""
    path = PurePosixPath(test_file)
    found = []
    for parent in path.parents:
        conftest = repo / parent / "conftest.py"
        if not conftest.is_file():
            continue
        for entry in collect_ignore(conftest):
            ignored = parent / entry.rstrip("/")
            if path == ignored or ignored in path.parents:
                found.append(ignored)
    return found


def tracked_files(repo: Path) -> list[str]:
    out = subprocess.run(
        ["git", "ls-files", "-z"], cwd=repo, check=True, capture_output=True, text=True
    ).stdout
    return [name for name in out.split("\0") if name]


def run(repo: Path, files: list[str] | None = None) -> int:
    try:
        tracked = tracked_files(repo) if files is None else files
        for name in tracked:
            # At any depth: pytest looks for its rootdir config from the
            # arguments' common ancestor upwards, not only at the repo root.
            if PurePosixPath(name).name in PYTEST_CONFIG_FILES:
                raise Unreadable(
                    f"{name}: a possible pytest configuration file now exists; python_files, "
                    f"testpaths or norecursedirs there would change what is collected, and "
                    f"this checker assumes pytest's defaults"
                )
        with (repo / "prek.toml").open("rb") as fh:
            hooks = pytest_hooks(tomllib.load(fh))
        if not hooks:
            raise Unreadable("prek.toml: no pytest hook found, so this check verifies nothing")
        test_files = [f for f in tracked if TEST_NAME.match(PurePosixPath(f).name)]
        if not test_files:
            raise Unreadable("no tracked test file found, so this check verifies nothing")
        failures = []
        for test_file in test_files:
            if (repo / test_file).is_symlink():
                raise Unreadable(f"{test_file}: a symlinked test file triggers no hook")
            ignored = ignored_over(repo, test_file)
            collectors = [h for h in hooks if h.collects(test_file, ignored)]
            if not collectors and ignored:
                continue  # held out on purpose; the conftest.py is the record of why
            if not collectors:
                failures.append(
                    f"UNCLAIMED: {test_file}\n"
                    f"  No prek hook's pytest entry collects this file, so nothing runs it.\n"
                    f"  Add a pytest hook over its directory to prek.toml, or, if it must not\n"
                    f"  run, hold it out with a commented collect_ignore in a conftest.py."
                )
            elif not any(h.triggered_by(test_file) for h in collectors):
                ids = ", ".join(h.hook_id for h in collectors)
                failures.append(
                    f"UNTRIGGERED: {test_file}\n"
                    f"  Collected by {ids}, but no collecting hook's `files` regex matches\n"
                    f"  this path, so editing the test does not re-run it outside --all-files."
                )
    except (Unreadable, OSError, KeyError, tomllib.TOMLDecodeError, re.error) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2
    except subprocess.CalledProcessError as exc:
        print(f"ERROR: git ls-files failed: {exc.stderr}", file=sys.stderr)
        return 2
    for failure in failures:
        print(failure, file=sys.stderr)
    return 1 if failures else 0


def main() -> int:
    return run(Path(__file__).resolve().parents[1])


if __name__ == "__main__":
    sys.exit(main())
