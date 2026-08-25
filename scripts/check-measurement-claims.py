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
import hashlib
import importlib.util
import re
import subprocess
import sys
import tomllib
from pathlib import Path

import yaml

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


def _load_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


# Anchor matching reuses check-citations.py's normalization so both gates
# agree on what "appears verbatim" means (dashes, curly quotes, backticks,
# whitespace, case).
_CITATIONS = Path(__file__).resolve().parent / "check-citations.py"
normalize = _load_module("_check_citations", _CITATIONS).normalize

# CommonMark fence: up to three spaces of indent, then three or more of one
# fence character; closed only by the same character at the same or greater
# length.
FENCE_OPEN = re.compile(r"^ {0,3}(`{3,}|~{3,})")
HTML_COMMENT = re.compile(r"<!--.*?(?:-->|\Z)", re.DOTALL)


def visible_lines(text: str) -> list[tuple[int, str]]:
    """The file's visible Markdown, line by line, 1-indexed.

    Fenced code blocks are dropped whole; HTML comments are cut out in place,
    an unclosed one through end of file, each replaced by its own newline
    count so later line numbers stay true. Inline code is kept: filenames and
    annotations legitimately live in backticks.
    """
    text = HTML_COMMENT.sub(lambda m: "\n" * m.group(0).count("\n"), text)
    out: list[tuple[int, str]] = []
    fence: tuple[str, int] | None = None
    for lineno, line in enumerate(text.splitlines(), start=1):
        m = FENCE_OPEN.match(line)
        if fence is None:
            if m:
                fence = (m.group(1)[0], len(m.group(1)))
                continue
            out.append((lineno, line))
        elif m and m.group(1)[0] == fence[0] and len(m.group(1)) >= fence[1]:
            fence = None
    return out


def check_registry(registry: dict[str, Entry], referenced: set[str]) -> list[str]:
    """R2: every entry's artifact exists and visibly carries its anchor; no dead entries."""
    violations: list[str] = []
    rel = REGISTRY_PATH.relative_to(REPO_ROOT)
    for key, entry in registry.items():
        artifact = REPO_ROOT / entry.artifact
        if not artifact.is_file():
            violations.append(f"{rel}: R2: [{key}]: artifact {entry.artifact} does not exist")
            continue
        text = artifact.read_text(encoding="utf-8")
        visible = normalize("\n".join(line for _, line in visible_lines(text)))
        if normalize(entry.anchor) not in visible:
            violations.append(
                f"{rel}: R2: [{key}]: anchor quote does not appear in {entry.artifact}'s "
                f'visible Markdown: "{entry.anchor[:70]}…"'
            )
        if key not in referenced:
            violations.append(
                f"{rel}: R2: [{key}]: no claim references this entry -- remove it or bind the claim"
            )
    return violations


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


class SourceError(Exception):
    """A registry source that cannot be resolved to description text."""


def frontmatter_description(text: str) -> str:
    """The frontmatter description scalar of a SKILL.md text.

    Text-based twin of check-description-freeze.py's read_description (which
    takes a Path and so cannot serve git: sources); the parity test keeps the
    two from drifting.
    """
    if not text.startswith("---\n"):
        raise SourceError("no frontmatter block")
    try:
        end = text.index("\n---", 4)
    except ValueError as exc:
        raise SourceError("frontmatter block is not closed") from exc
    try:
        meta = yaml.safe_load(text[4:end])
    except yaml.YAMLError as exc:
        raise SourceError(f"frontmatter is not valid YAML: {exc}") from exc
    if not isinstance(meta, dict):
        raise SourceError("frontmatter is not a mapping")
    desc = meta.get("description")
    if not isinstance(desc, str) or not desc.strip():
        raise SourceError("no description in frontmatter")
    return desc


def desc_hash(text: str) -> str:
    return hashlib.sha256(text.rstrip().encode("utf-8")).hexdigest()


def golden_hash(skill: str) -> str:
    return desc_hash((GOLDEN_DIR / f"{skill}.txt").read_text(encoding="utf-8"))


def shallow() -> bool:
    # Same rationale as check-citations.py: a shallow CI clone must fail
    # loudly on git: sources rather than pass quietly.
    return (REPO_ROOT / ".git" / "shallow").exists()


def resolve_source(entry: Entry) -> str:
    form, value = entry.source
    if form == "sha256":
        return value
    if form == "file":
        target = REPO_ROOT / value
        if not target.is_file():
            raise SourceError(f"file source {value} does not exist")
        return desc_hash(target.read_text(encoding="utf-8"))
    rel = f"skills/{entry.skill}/SKILL.md"
    result = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "show", f"{value}:{rel}"],
        capture_output=True,
        text=True,
        check=False,
    )
    if result.returncode != 0:
        detail = " (a shallow clone cannot see it -- fetch full history)" if shallow() else ""
        raise SourceError(f"git source {value}:{rel} cannot be resolved{detail}")
    return desc_hash(frontmatter_description(result.stdout))


def check_state(path: Path, lineno: int, state: str, entry: Entry) -> list[str]:
    """R3: state=current means source hash equals the golden; historical means it differs."""
    try:
        got = resolve_source(entry)
    except SourceError as exc:
        return [f"{path}:{lineno}: R3: [{entry.key}]: {exc}"]
    want = golden_hash(entry.skill)
    if state == "current" and got != want:
        return [
            f"{path}:{lineno}: R3: claim says state=current but [{entry.key}]'s source hashes "
            f"to {got[:12]}… and {entry.skill}'s golden is {want[:12]}… -- the artifact did "
            f"not measure the shipped description"
        ]
    if state == "historical" and got == want:
        return [
            f"{path}:{lineno}: R3: claim says state=historical but [{entry.key}]'s source "
            f"equals {entry.skill}'s golden -- this evidence is for the shipped description"
        ]
    return []


# A run record or run-artifact mention: any tests/runs/… path (file or
# directory), a dated markdown basename (this repo's run records are all
# date-prefixed), or a gate-artifact basename (AvB-gate1.md, BvC-gates.md,
# seam-gate4.md), or a path under a wave directory (seam/t13-rep1.jsonl).
# The dated-basename branch matches ANY date-prefixed filename, including a
# dated prereg or eval note that is not a run artifact, so R4 can fire on
# lines about non-run documents -- a deliberate best-effort trade-off that
# fails loudly at commit time rather than silently missing a real claim.
ARTIFACT_MENTION = re.compile(
    r"(?<!\w)("
    r"tests/runs/[\w./-]*"
    r"|20\d{2}-\d{2}-\d{2}-[\w./-]*"
    r"|[A-Za-z][\w-]*-gate[\w.-]*\.md"
    r"|(?:seam|AvB-[\w-]+|BvC-[\w-]+|screening-[\w-]+)/[\w./-]+"
    r")"
)

MEASURE_WORDS = ("measur", "re-validated", "ran against", "run against", "arms for")


def _segments(path: str) -> list[str]:
    return path.strip("`").rstrip(".").strip("/").split("/")


def _is_suffix(whole: list[str], tail: list[str]) -> bool:
    return len(tail) <= len(whole) and whole[-len(tail) :] == tail


def _mention_covered(mention: str, entry: Entry) -> bool:
    """Whether a mentioned path is the entry's artifact or inside its covers.

    A file mention (ends in an extension) is covered when a covered path ends
    with its segments, or when it sits under a covered directory. A directory
    mention is covered only when the entry lists that directory itself: an
    ancestor like `tests/runs/` is not covered merely because the entry has
    descendants there.
    """
    m = _segments(mention)
    is_file = "." in m[-1]
    for cov in (entry.artifact, *entry.covers):
        c = _segments(cov)
        if _is_suffix(c, m):
            return True
        if is_file and (REPO_ROOT / cov).is_dir():
            if _is_suffix(c, m[:-1]) and (REPO_ROOT / cov / m[-1]).is_file():
                return True
            if any(m[i : i + len(c)] == c for i in range(len(m) - len(c) + 1)):
                return True
    return False


def check_line_rules(
    path: Path, lineno: int, line: str, registry: dict[str, Entry]
) -> tuple[list[str], set[str]]:
    """R4 and R5 for one visible line; returns (violations, referenced evidence keys)."""
    violations: list[str] = []
    parsed = ANNOTATION.search(line)
    referenced = {parsed.group(3)} if parsed and parsed.group(3) in registry else set()

    stripped = ANNOTATION.sub("", line)
    mentions = [m.group(1) for m in ARTIFACT_MENTION.finditer(stripped)]
    lower = stripped.lower()
    claim_shaped = (
        bool(mentions) and "description" in lower and any(w in lower for w in MEASURE_WORDS)
    )

    if claim_shaped and parsed is None:
        violations.append(
            f"{path}:{lineno}: R4: unbound description-measurement claim -- this line names "
            f"{mentions[0]!r} beside a measurement statement about a description; add a "
            f"trailing [measured: skill=… state=… evidence=…] annotation (see {DECISION})"
        )
    if parsed is not None and mentions:
        entry = registry.get(parsed.group(3))
        if entry is not None:
            for mention in mentions:
                if not _mention_covered(mention, entry):
                    violations.append(
                        f"{path}:{lineno}: R5: {mention!r} is not covered by registry entry "
                        f"[{entry.key}] -- a second assertion cannot ride on this annotation; "
                        f"split the line or extend the entry's covers list"
                    )
    return violations, referenced


def check_file(path: Path, registry: dict[str, Entry]) -> tuple[list[str], set[str]]:
    violations: list[str] = []
    referenced: set[str] = set()
    lines = visible_lines(path.read_text(encoding="utf-8"))
    violations.extend(check_annotations(path, lines, registry))
    for lineno, line in lines:
        line_violations, refs = check_line_rules(path, lineno, line, registry)
        violations.extend(line_violations)
        referenced.update(refs)
        parsed = ANNOTATION.search(line)
        if parsed is None:
            continue
        entry = registry.get(parsed.group(3))
        if entry is not None and entry.skill == parsed.group(1):
            violations.extend(check_state(path, lineno, parsed.group(2), entry))
    return violations, referenced


def scope_files() -> list[Path]:
    found: list[Path] = []
    for root in DEFAULT_SCOPE:
        for pattern in SCOPE_PATTERNS:
            found.extend(sorted((REPO_ROOT / root).glob(pattern)))
    return found


def in_scope(path: Path) -> bool:
    try:
        rel = path.resolve().relative_to(REPO_ROOT)
    except ValueError:
        return False
    if not any(rel.is_relative_to(root) for root in DEFAULT_SCOPE):
        return False
    return any(rel.match(pattern) for pattern in SCOPE_PATTERNS)


def _report_skips(explicit: list[Path]) -> None:
    for p in explicit:
        if not p.is_file():
            print(f"skipped: {p}: not a file", file=sys.stderr)
        elif not in_scope(p):
            print(
                f"skipped: {p}: outside this check's scope -- NOT checked, and this is not a pass",
                file=sys.stderr,
            )


def main(argv: list[str]) -> int:
    try:
        registry = parse_registry(REGISTRY_PATH)
    except (RegistryError, tomllib.TOMLDecodeError) as exc:
        print(f"{REGISTRY_PATH.relative_to(REPO_ROOT)}: R2: {exc}", file=sys.stderr)
        return 1

    explicit = [Path(a).resolve() for a in argv]
    _report_skips(explicit)

    # Line rules are reported for the requested files; registry-wide rules
    # (R2, including dead entries) always evaluate against the FULL scope,
    # because an entry's references live anywhere in it.
    violations: list[str] = []
    referenced: set[str] = set()
    for target in scope_files():
        file_violations, refs = check_file(target, registry)
        referenced.update(refs)
        if not argv or target.resolve() in explicit:
            violations.extend(file_violations)
    violations.extend(check_registry(registry, referenced))

    for violation in violations:
        print(violation, file=sys.stderr)
    if violations:
        print(f"\n{len(violations)} measurement-claim violation(s).", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
