#!/usr/bin/env python3
"""Copy the plugin's runtime files into a clean directory.

The release tree is what an install should fetch: the four skills, their
references and decision records, the hook, the validator, the output style,
and the manifests. Evaluation fixtures, archived runs, and test suites stay
on `main`. The output directory is created fresh; an existing directory is
rebuilt only when it carries this builder's marker file."""

import json
import shutil
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
MARKER = ".data-reasoning-release"
ALLOW = [
    ".claude-plugin/plugin.json",
    ".claude-plugin/marketplace.json",
    ".codex-plugin/plugin.json",
    ".agents/plugins/marketplace.json",
    "LICENSE",
    "README.md",
    "hooks/hooks.json",
    "hooks/check_record_hook.py",
    "hooks/check_record_hook.sh",
    "instruments/check_record.py",
    "output-styles/data-answer.md",
]
SKILL_SUBTREES = ("SKILL.md", "references", "decisions")


def prepare_output(out: Path) -> None:
    if out.exists():
        if not (out / MARKER).is_file():
            sys.exit(f"refusing to replace {out}: it exists and was not built by this script")
        shutil.rmtree(out)
    out.mkdir(parents=True)
    (out / MARKER).write_text("built by scripts/build-release-tree.py; safe to delete\n")


def copy_allowlist(out: Path) -> None:
    for rel in ALLOW:
        dst = out / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(REPO / rel, dst)


def copy_skills(out: Path) -> None:
    for skill in sorted((REPO / "skills").iterdir()):
        if not (skill / "SKILL.md").is_file():
            continue
        for name in SKILL_SUBTREES:
            src = skill / name
            if not src.exists():
                continue
            dst = out / "skills" / skill.name / name
            if src.is_dir():
                shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
            else:
                dst.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)


def point_marketplace_at_self(out: Path) -> None:
    path = out / ".claude-plugin" / "marketplace.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    for plugin in data["plugins"]:
        plugin["source"] = "./"
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def build(out: Path) -> None:
    prepare_output(out)
    copy_allowlist(out)
    copy_skills(out)
    point_marketplace_at_self(out)


if __name__ == "__main__":
    if len(sys.argv) != 2:  # noqa: PLR2004
        sys.exit("usage: build-release-tree.py OUTPUT_DIR")
    build(Path(sys.argv[1]).resolve())
