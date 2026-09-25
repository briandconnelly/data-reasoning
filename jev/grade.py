#!/usr/bin/env python3
"""Second-scorer pass over archived arms: ask Jev each rubric item, report where it disagrees.

    python jev/grade.py jev/pilot/2026-09-24/wave.json [--out report.json]

A wave file names the frozen questions, the abstain band, the arms (as
`run_arm.py` archived them), and, optionally, the existing scorer's labels
with that scorer named. An arm entry with `"kind": "control"` carries labels
constructed by the wave's author (a question asked of an arm whose correct
answer differs); controls are counted apart from the reference labels.
How this report may and may not be used is owned by jev/README.md; this
module only produces it.

Exit 0 when every point was asked, 2 when Jev was unavailable (nothing was
checked), 1 on a malformed wave file.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))
import jev_client

REPO = Path(__file__).resolve().parents[1]
TEXT_SUFFIXES = {".md", ".txt", ".csv", ".json", ".py", ".sql"}
# Jev's state budget is 32k tokens including the longest question; ~4 chars a token.
MAX_STATE_CHARS = 100_000
HALF = 0.5
EXIT_UNAVAILABLE = 2


def arm_state(arm_dir: Path, arm: str) -> dict[str, Any]:
    """What a scorer reads: the prompt, the final answer, and every file the arm wrote."""
    final = ""
    for line in (arm_dir / f"{arm}.jsonl").read_text().splitlines():
        if not line.strip():
            continue
        event = json.loads(line)
        if event.get("type") == "result":
            final = event.get("result") or ""
    files = {}
    scratch = arm_dir / f"{arm}.scratch"
    if scratch.is_dir():
        for f in sorted(scratch.rglob("*")):
            if f.is_file() and f.suffix in TEXT_SUFFIXES:
                files[str(f.relative_to(scratch))] = f.read_text(errors="replace")
    prompt_file = arm_dir / f"{arm}.prompt.txt"
    prompt = prompt_file.read_text() if prompt_file.is_file() else ""
    return {"user_prompt": prompt, "final_answer": final, "files_written": files}


def label(p: float, band: tuple[float, float]) -> str:
    lo, hi = band
    if p < lo:
        return "fail"
    if p > hi:
        return "pass"
    return "abstain"


def status(jev_label: str, reference: bool | None) -> str:
    if jev_label == "abstain":
        return "abstain"
    if reference is None:
        return "unreferenced"
    return "agree" if (jev_label == "pass") == reference else "disagree"


def load_wave(path: Path) -> dict[str, Any]:
    wave = json.loads(path.read_text())
    lo, hi = wave["abstain_band"]
    if not 0 <= lo <= HALF <= hi <= 1:
        raise ValueError("abstain_band must straddle 0.5 within [0, 1]")
    items = wave["items"]
    for arm in wave["arms"]:
        if not arm["items"]:
            raise ValueError(f"arm {arm['arm']} asks no items")
        unknown = set(arm["items"]) - set(items)
        if unknown:
            raise ValueError(f"arm {arm['arm']} names unknown items {sorted(unknown)}")
        if any(v is not None for v in arm["items"].values()) and not wave.get("reference_scorer"):
            raise ValueError("reference labels need `reference_scorer`: who scored them")
    return wave


def questions_digest(items: dict[str, Any]) -> str:
    return hashlib.sha256(json.dumps(items, sort_keys=True).encode()).hexdigest()[:16]


def grade(wave: dict[str, Any], transport: jev_client.Transport | None = None) -> dict[str, Any]:
    band = tuple(wave["abstain_band"])
    items = wave["items"]
    points, models, tokens = [], set(), 0
    for arm in wave["arms"]:
        kind = arm.get("kind", "reference")
        state = arm_state(REPO / arm["dir"], arm["arm"])
        qs = {item: items[item]["question"] for item in arm["items"]}
        # The budget covers the state plus the longest question, so both are counted.
        size = len(json.dumps(state)) + max(len(json.dumps(q)) for q in qs.values())
        if size > MAX_STATE_CHARS:
            for item, ref in arm["items"].items():
                points.append(
                    {
                        "arm": arm["arm"],
                        "item": item,
                        "kind": kind,
                        "reference": ref,
                        "status": "not_checked",
                        "reason": f"state and longest question {size} chars",
                    }
                )
            continue
        resp = jev_client.evaluate(state, qs, transport=transport)
        models.add(resp.get("model"))
        tokens += resp.get("usage", {}).get("input_tokens", 0)
        for item, ref in arm["items"].items():
            p = jev_client.probability_of_pass(
                resp["answers"][item], items[item].get("pass_option")
            )
            jl = label(p, band)
            points.append(
                {
                    "arm": arm["arm"],
                    "item": item,
                    "kind": kind,
                    "reference": ref,
                    "p_pass": round(p, 3),
                    "jev": jl,
                    "status": status(jl, ref),
                }
            )
    counts: dict[str, dict[str, int]] = {}
    for pt in points:
        per_kind = counts.setdefault(pt["kind"], {})
        per_kind[pt["status"]] = per_kind.get(pt["status"], 0) + 1
    return {
        "wave": wave.get("title"),
        "models": sorted(m for m in models if m),
        "questions_sha256_16": questions_digest(items),
        "abstain_band": list(band),
        "reference_scorer": wave.get("reference_scorer"),
        "input_tokens": tokens,
        "counts": counts,
        "points": points,
    }


def render(report: dict[str, Any]) -> str:
    c = report["counts"]
    lines = [
        f"# Jev second-scorer report: {report['wave']}",
        "",
        f"Model {', '.join(report['models']) or 'n/a'}; questions {report['questions_sha256_16']}; "
        f"abstain band {report['abstain_band']}; {report['input_tokens']} input tokens.",
        f"Reference scorer: {report['reference_scorer'] or 'none'}.",
        "",
        *(
            f"Counts ({kind}): " + ", ".join(f"{k} {v}" for k, v in sorted(by.items()))
            for kind, by in sorted(c.items())
        ),
        "",
        "## For a person to read",
        "",
        "Disagreements and abstentions are where the rubric text, the reference, "
        "or Jev may be wrong.",
        "Read the arm before deciding which.",
        "",
        "| arm | item | kind | reference | Jev p(pass) | status |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for pt in report["points"]:
        if pt["status"] in {"disagree", "abstain", "not_checked"}:
            ref = {True: "PASS", False: "FAIL", None: "—"}[pt["reference"]]
            lines.append(
                f"| {pt['arm']} | {pt['item']} | {pt['kind']} | {ref} "
                f"| {pt.get('p_pass', '—')} | {pt['status']} |"
            )
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("wave", type=Path)
    ap.add_argument("--out", type=Path, help="write the full JSON report here")
    args = ap.parse_args(argv)
    try:
        wave = load_wave(args.wave)
    except (ValueError, KeyError, json.JSONDecodeError) as exc:
        print(f"malformed wave file: {exc}", file=sys.stderr)
        return 1
    try:
        report = grade(wave)
    except jev_client.JevUnavailable as exc:
        print(f"not checked: {exc}", file=sys.stderr)
        return EXIT_UNAVAILABLE
    if args.out:
        args.out.write_text(json.dumps(report, indent=1) + "\n")
    sys.stdout.write(render(report))
    return 0


if __name__ == "__main__":
    sys.exit(main())
