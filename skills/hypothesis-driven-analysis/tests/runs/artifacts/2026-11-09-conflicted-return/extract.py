#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Mechanical extraction for the conflicted-return wave; the scorer reads its output.

    uv run extract.py census <dir>   # manifest count by kind, cost total
    uv run extract.py fields <dir>   # answer fields of every S21 / S20 arm
    uv run extract.py digests <dir>  # skill-tree, fixture and instrument digests per arm

It prints; it does not score. Rationale, token preservation and best-supported
eligibility are rubric reads (see prereg.md). Calibrated before use against the
2026-11-08 binding-rules-hoist archive, whose wave record states 81 arms
(13 canaries, 6 pre-trunc, 62 scored) and $25.97: `census` must reproduce both.
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

FIELDS = (
    "RECONCILED OUTCOME FOR T2",
    "H2 STATUS",
    "BEST SUPPORTED",
    "FAULTS FOUND IN THE RETURN",
    "LIMITATIONS THAT MUST REACH THE CONCLUSION",
)


def arms(d: Path) -> list[tuple[str, dict]]:
    out = []
    for m in sorted(d.glob("*.manifest.json")):
        out.append((m.name[: -len(".manifest.json")], json.loads(m.read_text())))
    return out


def kind(name: str) -> str:
    if name.startswith("canary-"):
        return "canary"
    if "-pretrunc-" in name:
        return "pretrunc"
    return "scored"


def field(text: str, name: str) -> str | None:
    """The text after `NAME:` up to the next ALL-CAPS field label, markdown bold tolerated."""
    pat = rf"^\**{re.escape(name)}\**:\s*(.*?)(?=^\s*\**[A-Z][A-Z0-9 ]+\**:|\Z)"
    m = re.search(pat, text, re.M | re.S)
    return m.group(1).strip() if m else None


def answer(d: Path, name: str, man: dict) -> tuple[str, str]:
    ans = d / f"{name}.scratch" / "answer.md"
    if ans.exists():
        return "answer.md", ans.read_text(encoding="utf-8")
    return "result_text", man.get("result_text") or ""


def census(d: Path) -> None:
    a = arms(d)
    print(f"manifests={len(a)}", dict(Counter(kind(n) for n, _ in a)))
    cost = sum(m["usage"].get("total_cost_usd") or 0.0 for _, m in a)
    print(f"cost=${cost:.2f}")
    print("contaminated:", [n for n, m in a if m.get("contaminated")] or "none")
    print("nonzero exit:", [n for n, m in a if m.get("exit_code") != 0] or "none")


def fields(d: Path) -> None:
    for name, man in arms(d):
        if not re.match(r"(canary-)?s2[01]", name):
            continue
        src, text = answer(d, name, man)
        print(f"== {name} [{src}] skill_ref={man['skill_ref']}")
        for f in FIELDS:
            v = field(text, f)
            if v is not None:
                print(f"   {f}: {' '.join(v.split())[:400]}")


def digests(d: Path) -> None:
    for name, man in arms(d):
        sk = man.get("skill_files_sha256") or {}
        print(
            f"{name:26} ref={man['skill_ref']} "
            f"SKILL.md={sk.get('hypothesis-driven-analysis/SKILL.md', '-')[:12]} "
            f"fixture={sorted(v[:12] for v in man['fixture_files_sha256'].values())} "
            f"instruments={sorted(v[:12] for v in man['instruments_sha256'].values())}"
        )


PATH_KEYS = ("file_path", "path", "notebook_path")
BASH_FLAGS = re.compile(r"\b(warehouse|git|curl|wget|ssh|scp|nc|pip|npm|gh)\b")
ABS_PATH = re.compile(r"(?<![\w.])(/[\w.@%+-]+(?:/[\w.@%+-]+)+)")
SYSTEM_PREFIXES = ("/usr/", "/bin/", "/dev/null", "/opt/homebrew/", "/System/")


def tool_uses(jsonl: Path):
    for line in jsonl.read_text(encoding="utf-8").splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") != "assistant":
            continue
        for block in ev.get("message", {}).get("content", []) or []:
            if isinstance(block, dict) and block.get("type") == "tool_use":
                yield block.get("name"), block.get("input", {}) or {}


def audit_arm(jsonl: Path, man: dict) -> list[str]:
    """Transcript audit beyond run_arm.py's scan, which checks only repository
    paths, other SKILL.md files, and tests/ paths. Flags: a tool outside the
    requested set (MCP tools are present at startup); a path outside the staging
    root; a read of a staged skill file other than SKILL.md (out of scope for
    this wave's prompts); a Bash command naming a collection, VCS, or network
    tool; an absolute path in a Bash command outside the staging root. A run of
    the staged instruments/check_record.py is reported as allowed, not flagged."""
    root = man["staging_root"].rstrip("/")
    skill_dir = f"{root}/skills/{man['skill']}/" if man.get("skill") else None
    allowed = set(man.get("tools_requested") or [])
    hits = []
    for i, (name, inp) in enumerate(tool_uses(jsonl), 1):
        if name not in allowed:
            hits.append(f"#{i} tool outside requested set: {name}")
            continue
        for k in PATH_KEYS:
            v = str(inp.get(k) or "")
            if v.startswith("/") and not (v == root or v.startswith(root + "/")):
                hits.append(f"#{i} {name} path outside staging root: {v}")
            if (
                name == "Read"
                and skill_dir
                and v.startswith(skill_dir)
                and not v.endswith("/SKILL.md")
            ):
                hits.append(f"#{i} read of staged skill file other than SKILL.md: {v}")
        if name == "Bash":
            cmd = str(inp.get("command") or "")
            if "instruments/check_record.py" in cmd:
                hits.append(f"#{i} ALLOWED staged validator run")
            body = re.sub(r"<<'?(\w+)'?.*?\n\1\b", "<<HEREDOC", cmd, flags=re.S)
            for m in BASH_FLAGS.finditer(body):
                hits.append(f"#{i} Bash names {m.group(1)!r}: {body[:160]!r}")
            for m in ABS_PATH.finditer(body):
                p = m.group(1)
                if not (p.startswith(root) or p.startswith(SYSTEM_PREFIXES)):
                    hits.append(f"#{i} Bash absolute path outside staging root: {p}")
    return hits


def audit(d: Path) -> None:
    for name, man in arms(d):
        hits = audit_arm(d / f"{name}.jsonl", man)
        flagged = [h for h in hits if "ALLOWED" not in h]
        print(f"{name:26} scan={len(man.get('contaminated') or [])} audit={len(flagged)}")
        for h in hits:
            print(f"   {h}")


if __name__ == "__main__":
    cmds = {"census": census, "fields": fields, "digests": digests, "audit": audit}
    cmds[sys.argv[1]](Path(sys.argv[2]))
