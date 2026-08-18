#!/usr/bin/env python3
"""Pin the four skills' frontmatter descriptions against unmeasured drift.

skills/exploratory-data-analysis/decisions/006-description-freeze-until-measured.md
is the authority on when a description may change; this hook only makes a
silent change impossible. Refresh a golden (--update <skill>) only under that
record's unfreezing conditions.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

SKILLS = [
    "hypothesis-driven-analysis",
    "exploratory-data-analysis",
    "causal-identification-review",
    "decision-analysis",
]

DECISION = "skills/exploratory-data-analysis/decisions/006-description-freeze-until-measured.md"


def read_description(skill_md: Path) -> str:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"{skill_md}: no frontmatter block")
    end = text.index("\n---", 4)
    try:
        meta = yaml.safe_load(text[4:end])
    except yaml.YAMLError as exc:
        raise ValueError(f"{skill_md}: frontmatter is not valid YAML: {exc}") from exc
    if not isinstance(meta, dict):
        raise ValueError(f"{skill_md}: frontmatter is not a mapping")
    desc = meta.get("description")
    if not isinstance(desc, str) or not desc.strip():
        raise ValueError(f"{skill_md}: no description in frontmatter")
    return desc


def run(repo: Path, update: frozenset[str]) -> int:
    if update and not update <= set(SKILLS) and update != {"all"}:
        print(f"ERROR: unknown --update target(s): {sorted(update - set(SKILLS))}", file=sys.stderr)
        return 2
    golden_dir = repo / "scripts" / "frontmatter-descriptions"
    golden_dir.mkdir(parents=True, exist_ok=True)
    failures = 0
    for skill in SKILLS:
        try:
            desc = read_description(repo / "skills" / skill / "SKILL.md")
        except (OSError, ValueError) as exc:
            print(f"ERROR: {exc}", file=sys.stderr)
            return 2
        golden = golden_dir / f"{skill}.txt"
        if skill in update or "all" in update:
            golden.write_text(desc + "\n", encoding="utf-8")
            continue
        if not golden.exists():
            print(f"ERROR: missing golden {golden}; run --update {skill} once", file=sys.stderr)
            return 2
        if golden.read_text(encoding="utf-8") != desc + "\n":
            failures += 1
            print(
                f"FROZEN: {skill}'s description differs from its golden.\n"
                f"  Descriptions are frozen against unmeasured change; {DECISION}\n"
                f"  states the unfreezing conditions, after which --update {skill}\n"
                f"  refreshes the pin.",
                file=sys.stderr,
            )
    return 1 if failures else 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--update",
        nargs="+",
        default=[],
        metavar="SKILL",
        help="refresh the named skill golden(s), or 'all'",
    )
    args = parser.parse_args()
    repo_root = Path(__file__).resolve().parents[1]
    return run(repo_root, update=frozenset(args.update))


if __name__ == "__main__":
    sys.exit(main())
