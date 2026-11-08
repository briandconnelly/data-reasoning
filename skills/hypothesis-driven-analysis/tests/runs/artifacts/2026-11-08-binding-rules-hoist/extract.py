#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Mechanical extraction for the binding-rules wave; the scorer reads its output.

    uv run extract.py s21     # status / best-supported lines and S21.Q per arm
    uv run extract.py report <arm>...   # final message + ledger Conclusion section
    uv run extract.py cost    # cost and duration per arm, and totals

S21.Q: every fragment of GOVERNING SKILL TEXT of 20+ characters, after removing
backticks and asterisks, splitting on ellipses and quotation boundaries, and
collapsing whitespace, must be a substring of the SKILL.md that arm was staged
with (pre or post commit, or the truncated prefix named in its manifest).
"""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).parent
REPO = HERE.parents[5]
GROUP_MARKERS = {
    "G1": ["Derive hypothesis status", "The status set is closed", "is not decided at conclusion time"],
    "G2": ["Precedence when tests disagree", "an adequate test failing the necessary"],
    "G4": ["is not a status;", "The per-hypothesis summary table repeats"],
    "G5": ["Apply the precommitted stop rule"],
}


def norm(s: str) -> str:
    """Drop markup, quotation marks, list markers, and whitespace runs."""
    s = re.sub(r"(?m)^\s*- ", " ", s)
    for ch in '`*"“”\\':
        s = s.replace(ch, "")
    return re.sub(r"\s+", " ", s).strip()


def fragments(gov: str) -> list[str]:
    """Sentence-sized pieces of a quotation, connectors and wrappers stripped."""
    out = []
    for piece in re.split(r"(?<=[.;:])\s+|\.\.\.|…|\s/\s", norm(gov)):
        piece = re.sub(r"^(?:and|/|\(?Also:|From SKILL\.md[^:]*:)\s*", "", piece.strip())
        piece = piece.strip(" ()")
        if len(piece) >= 20:
            out.append(piece)
    return out


def skill_text(manifest: dict) -> str:
    over = manifest.get("skill_md_override")
    if over:
        return (REPO / over["path"]).read_text(encoding="utf-8")
    ref = manifest["skill_ref"]
    return subprocess.run(
        ["git", "-C", str(REPO), "show", f"{ref}:skills/hypothesis-driven-analysis/SKILL.md"],
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def field(text: str, name: str) -> str:
    m = re.search(rf"^{name}:\s*(.*?)(?=^\s*[A-Z][A-Z ]+:|\Z)", text, re.M | re.S)
    return m.group(1).strip() if m else ""


def s21() -> None:
    for man in sorted(HERE.glob("*s21d*.manifest.json")):
        m = json.loads(man.read_text())
        ans = man.with_suffix("").with_suffix(".scratch") / "answer.md"
        text = ans.read_text(encoding="utf-8") if ans.exists() else (m.get("result_text") or "")
        status = field(text, "H2 STATUS").splitlines()[0][:70] if field(text, "H2 STATUS") else "?"
        best = field(text, "BEST SUPPORTED")[:110].replace("\n", " ")
        gov = field(text, "GOVERNING SKILL TEXT")
        hay = norm(skill_text(m))
        frags = fragments(gov)
        missing = [f for f in frags if f not in hay]
        groups = sorted(
            g for g, keys in GROUP_MARKERS.items() for k in keys if any(k in f for f in frags)
        )
        q = "ok" if frags and not missing else f"MISS{len(missing)}/{len(frags)}"
        print(f"{m['name']:24} status={status!r}")
        if best:
            print(f"{'':24} best={best!r}")
        print(f"{'':24} S21.Q={q} groups={','.join(sorted(set(groups))) or '-'}")
        for f in missing:
            print(f"{'':24}   missing: {f[:100]!r}")


def report(arms: list[str]) -> None:
    for name in arms:
        m = json.loads((HERE / f"{name}.manifest.json").read_text())
        print(f"==================== {name}\n--- final message")
        print(m.get("result_text") or "")
        for led in sorted((HERE / f"{name}.scratch").glob("*.md")):
            text = led.read_text(encoding="utf-8")
            i = text.find("## Conclusion")
            print(f"--- {led.name} Conclusion section")
            print(text[i:] if i >= 0 else "(no ## Conclusion)")


def cost() -> None:
    tot = 0.0
    for man in sorted(HERE.glob("*.manifest.json")):
        m = json.loads(man.read_text())
        c = m["usage"].get("total_cost_usd") or 0.0
        tot += c
        print(f"{m['name']:26} ${c:.3f} {m['duration_s']}s contaminated={len(m['contaminated'])}")
    print(f"TOTAL ${tot:.2f} over {len(list(HERE.glob('*.manifest.json')))} arms")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "s21":
        s21()
    elif cmd == "report":
        report(sys.argv[2:])
    else:
        cost()
