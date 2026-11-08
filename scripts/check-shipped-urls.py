#!/usr/bin/env python3
"""Fail when a shipped file links to a repository path its ref cannot serve.

Issue #67: the four SKILL.md intros linked `blob/main/.../tests/scenarios.md`,
but `main` is the runtime tree scripts/build-release-tree.py builds, which
omits every tests/ path, so all four links 404ed and nothing noticed.

What ships is whatever the release builder copies, so this checker builds the
release tree with the builder itself (into a temporary directory) rather than
restating its inclusion rules, then reads every file in that tree for links of
the form https://github.com/briandconnelly/data-reasoning/blob/<ref>/<path>
(or tree/<ref>/<path>) and checks each one:

  ref is `main`          -- <path> must be in the release tree;
  ref is a 40-hex SHA    -- `git cat-file -e <sha>:<path>` must succeed;
  any other ref          -- fails: a branch such as `dev` moves, and a tag or
                            short SHA is not checked here.

Offline: it reads only the working tree and the local git object store, so a
pinned SHA must be present locally (CI checks out with fetch-depth 0).
"""

from __future__ import annotations

import importlib.util
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
BUILDER = REPO / "scripts" / "build-release-tree.py"

URL = re.compile(
    r"https://github\.com/briandconnelly/data-reasoning/(?:blob|tree)/"
    r"(?P<ref>[^/\s]+)/(?P<path>[^\s)\]>\"'`#?,]+)"
)
FULL_SHA = re.compile(r"^[0-9a-f]{40}$")


def load_builder():
    spec = importlib.util.spec_from_file_location("build_release_tree", BUILDER)
    if spec is None or spec.loader is None:
        sys.exit(f"cannot load {BUILDER}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def release_paths(tree: Path) -> set[str]:
    """Every file and directory in a built release tree, as repo-relative paths."""
    return {p.relative_to(tree).as_posix() for p in tree.rglob("*")}


def path_at_commit(sha: str, path: str, repo: Path) -> bool:
    result = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "-e", f"{sha}:{path}"],
        capture_output=True,
        check=False,
    )
    return result.returncode == 0


def check_url(ref: str, path: str, shipped: set[str], repo: Path) -> str | None:
    """Return why the link is broken, or None when it resolves."""
    if ref == "main":
        if path in shipped:
            return None
        return f"`{path}` is not in the release tree that `main` carries"
    if FULL_SHA.match(ref):
        if path_at_commit(ref, path, repo):
            return None
        return f"`{path}` does not exist at {ref}, or that commit is not in the local object store"
    return (
        f"ref `{ref}` is neither `main` nor a full 40-hex commit SHA: "
        "a branch moves, and a tag or short SHA is not checked"
    )


def scan(tree: Path, repo: Path) -> list[str]:
    """Check every repository link in every file of a built release tree."""
    shipped = release_paths(tree)
    failures = []
    for file in sorted(p for p in tree.rglob("*") if p.is_file()):
        try:
            text = file.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        rel = file.relative_to(tree).as_posix()
        for lineno, line in enumerate(text.splitlines(), start=1):
            for m in URL.finditer(line):
                path = m["path"].rstrip(".:;")
                why = check_url(m["ref"], path, shipped, repo)
                if why:
                    failures.append(f"{rel}:{lineno}: {m.group(0).rstrip('.:;')}: {why}")
    return failures


def main() -> int:
    builder = load_builder()
    with tempfile.TemporaryDirectory() as tmp:
        tree = Path(tmp) / "release"
        builder.build(tree)
        failures = scan(tree, REPO)
    for failure in failures:
        print(failure, file=sys.stderr)
    if failures:
        print(f"{len(failures)} shipped link(s) do not resolve", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
