#!/usr/bin/env python3
"""Bind description-measurement claims to registry evidence.

skills/exploratory-data-analysis/decisions/007-measurement-claim-binding.md
is the authority on the convention: what an annotation is, what a registry
entry is, and what each of rules R1-R5 requires. This module is the
instrument only. It reads the annotations in agent-read skill prose, reads
scripts/measured-descriptions.toml, and reports every line where the two
disagree with each other, with the frozen artifacts, or with the description
goldens in scripts/frontmatter-descriptions/.

Mechanics worth knowing when reading the code:
- "visible Markdown" means fenced code blocks and HTML comments are removed
  before any line is inspected, with line numbers preserved.
- anchor matching uses check-citations.py's normalize(), so both gates agree
  on what "appears verbatim" means.
- description hashes are sha256 over the rstripped text; that is what the run
  manifests recorded, and what the goldens hash to after their trailing
  newline is stripped.
- registry-wide checks (R2) always evaluate against the full scope, even
  when files are passed on the command line, because an entry's references
  live anywhere in it.

Exit non-zero on any violation. With no arguments, checks the default scope.
"""

from __future__ import annotations

import dataclasses
import re
import tomllib
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = REPO_ROOT / "scripts" / "measured-descriptions.toml"
GOLDEN_DIR = REPO_ROOT / "scripts" / "frontmatter-descriptions"
DECISION = "skills/exploratory-data-analysis/decisions/007-measurement-claim-binding.md"

SKILLS = (
    "hypothesis-driven-analysis",
    "exploratory-data-analysis",
    "causal-identification-review",
    "decision-analysis",
)

# Same scope classes as check-citations.py: agent-read skill prose plus the
# live test catalogs. Frozen runs are evidence, not claim sources.
DEFAULT_SCOPE = tuple(f"skills/{s}" for s in SKILLS)
SCOPE_PATTERNS = ("SKILL.md", "references/*.md", "tests/scenarios.md", "decisions/*.md")

# The only accepted form: backticked, at the end of the line.
ANNOTATION = re.compile(
    r"`\[measured:\s*skill=([a-z][a-z0-9-]*)\s+state=(current|historical)"
    r"\s+evidence=([A-Za-z0-9._-]+)\s*\]`\s*$"
)
# Anything that starts an annotation anywhere on the line. An opener the
# strict form does not match is a typo or a misplaced annotation, and must
# fail rather than pass as prose.
ANNOTATION_OPENER = re.compile(r"\[measured:")

SOURCE_FORMS = ("sha256", "file", "git")
HEX = re.compile(r"[0-9a-f]+")


class RegistryError(ValueError):
    """A registry entry that does not have the shape decision 007 requires."""


@dataclasses.dataclass(frozen=True)
class Entry:
    key: str
    skill: str
    artifact: str
    source: tuple[str, str]  # (form, value); form in SOURCE_FORMS
    anchor: str
    covers: tuple[str, ...]


def _repo_relative(key: str, field: str, value: object) -> str:
    if not isinstance(value, str) or not value:
        raise RegistryError(f"[{key}]: {field} must be a non-empty string")
    parts = value.split("/")
    if value.startswith("/") or ".." in parts or "." in parts or "\\" in value:
        raise RegistryError(f"[{key}]: {field} must be a repo-relative POSIX path, got {value!r}")
    return value.rstrip("/")


def _parse_source(key: str, raw: object) -> tuple[str, str]:
    if not isinstance(raw, str):
        raise RegistryError(f"[{key}]: source must be a string")
    form, _, value = raw.partition(":")
    if form not in SOURCE_FORMS or not value:
        raise RegistryError(
            f"[{key}]: source must be sha256:<hex>, file:<path>, or git:<sha>, got {raw!r}"
        )
    if form == "sha256" and not (len(value) == 64 and HEX.fullmatch(value)):  # noqa: PLR2004
        raise RegistryError(f"[{key}]: sha256 source must be 64 lowercase hex chars")
    if form == "git" and not (7 <= len(value) <= 40 and HEX.fullmatch(value)):  # noqa: PLR2004
        raise RegistryError(f"[{key}]: git source must be a 7-40 char hex commit id")
    if form == "file":
        value = _repo_relative(key, "file source", value)
    return form, value


def parse_registry(path: Path) -> dict[str, Entry]:
    raw = tomllib.loads(path.read_text(encoding="utf-8"))
    entries: dict[str, Entry] = {}
    for key, table in raw.items():
        if not isinstance(table, dict):
            raise RegistryError(f"[{key}]: entry must be a table")
        skill = table.get("skill")
        if skill not in SKILLS:
            raise RegistryError(f"[{key}]: unknown skill {skill!r}")
        anchor = table.get("anchor")
        if not isinstance(anchor, str) or not anchor.strip():
            raise RegistryError(f"[{key}]: anchor is required")
        covers_raw = table.get("covers", [])
        if not isinstance(covers_raw, list):
            raise RegistryError(f"[{key}]: covers must be a list of paths")
        entries[key] = Entry(
            key=key,
            skill=skill,
            artifact=_repo_relative(key, "artifact", table.get("artifact")),
            source=_parse_source(key, table.get("source")),
            anchor=anchor,
            covers=tuple(_repo_relative(key, "covers", c) for c in covers_raw),
        )
    return entries


def check_annotations(
    path: Path, lines: list[tuple[int, str]], registry: dict[str, Entry]
) -> list[str]:
    """R1 over visible lines: every annotation is well-formed, placed, and resolves."""
    violations: list[str] = []
    for lineno, line in lines:
        parsed = ANNOTATION.search(line)
        openers = len(ANNOTATION_OPENER.findall(line))
        if openers > (1 if parsed else 0):
            violations.append(
                f"{path}:{lineno}: R1: malformed or misplaced annotation -- the only accepted "
                f"form is a backticked [measured: skill=… state=… evidence=…] at the end of "
                f"the line (see {DECISION})"
            )
        if parsed is None:
            continue
        skill, _state, evidence = parsed.group(1), parsed.group(2), parsed.group(3)
        entry = registry.get(evidence)
        if entry is None:
            violations.append(
                f"{path}:{lineno}: R1: evidence key {evidence!r} is not in "
                f"scripts/measured-descriptions.toml"
            )
        elif entry.skill != skill:
            violations.append(
                f"{path}:{lineno}: R1: annotation says skill={skill} but registry entry "
                f"[{evidence}] is for {entry.skill}"
            )
    return violations
