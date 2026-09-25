#!/usr/bin/env python3
"""Route every catalog prompt through Jev against the frozen skill descriptions.

    python jev/route.py [--out routing.json] [--labels labels.json]

This measures whether a prompt's text separates the routes as the frozen
descriptions draw them. It is Jev's routing, not the agent's: what it may be
used for is owned by jev/README.md. The output that matters is the list of
prompts Jev cannot place, which are candidates for real agent arms.

`--labels` maps a prompt id to its intended route (a skill name or `none`);
labelled prompts are then scored for agreement. An id is the catalog's skill
name and the first 12 hex digits of the prompt text's sha256, because one
scenario heading can carry several prompts (a pair, or S22's three routes).
With no labels the probe reports distributions and ambiguity only.

Exit 0 on success, 2 when Jev was unavailable.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from collections import Counter
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))
import jev_client

REPO = Path(__file__).resolve().parents[1]
SKILLS = (
    "hypothesis-driven-analysis",
    "exploratory-data-analysis",
    "causal-identification-review",
    "decision-analysis",
)
NONE_OPTION = "none"
NONE_TEXT = (
    "None of these skills fits: a direct lookup, a simple computation, or a request "
    "outside data analysis; answer directly."
)
AMBIGUOUS_BELOW = 0.75
PROMPT_LINE = re.compile(r"^\*\*Prompt[^*]*\*\*(?:\s*\(verbatim\))?:?\s*")
# "as Scenario 1, but …", "DA-S1's prompt, but …": not standalone requests.
DERIVED = re.compile(r"^(as |[\w-]+'s prompt)", re.IGNORECASE)


def frozen_descriptions() -> dict[str, str]:
    """The goldens check-description-freeze.py pins, so the probe reads exactly what is frozen."""
    gold = REPO / "scripts" / "frontmatter-descriptions"
    return {s: (gold / f"{s}.txt").read_text().strip() for s in SKILLS}


def catalog_prompts(text: str) -> list[tuple[str, str]]:
    """(scenario heading, prompt) for every standalone `**Prompt…**` in a catalog.

    A prompt is the text after the marker on its own line, plus any blockquote
    lines that follow it (after blank lines). Derived prompts are skipped.
    """
    lines = text.splitlines()
    out, heading = [], ""
    for i, line in enumerate(lines):
        if line.startswith("#"):
            heading = line.lstrip("#").strip()
        if not line.startswith("**Prompt"):
            continue
        parts = [PROMPT_LINE.sub("", line).strip()]
        j = i + 1
        while j < len(lines) and not lines[j].strip():
            j += 1
        while j < len(lines) and lines[j].startswith(">"):
            parts.append(lines[j].lstrip(">").strip())
            j += 1
        prompt = " ".join(p for p in parts if p).strip().strip('"')
        if prompt and not DERIVED.match(prompt):
            out.append((heading, prompt))
    return out


def prompt_id(skill: str, prompt: str) -> str:
    return f"{skill}:{hashlib.sha256(prompt.encode()).hexdigest()[:12]}"


def route_question(descriptions: dict[str, str]) -> dict[str, Any]:
    criteria = dict(descriptions)
    criteria[NONE_OPTION] = NONE_TEXT
    return {
        "type": "choice",
        "instructions": (
            "A data-analysis agent received the user request in `request`. "
            "Which skill should it load to handle it? Judge from the request text alone."
        ),
        "criteria": criteria,
    }


def probe(transport: jev_client.Transport | None = None) -> list[dict[str, Any]]:
    question = route_question(frozen_descriptions())
    rows = []
    for skill in SKILLS:
        catalog = (REPO / "skills" / skill / "tests" / "scenarios.md").read_text()
        for heading, prompt in catalog_prompts(catalog):
            resp = jev_client.evaluate(
                {"request": prompt}, {"route": question}, transport=transport
            )
            ans = resp["answers"]["route"]
            rows.append(
                {
                    "id": prompt_id(skill, prompt),
                    "catalog": skill,
                    "scenario": heading,
                    "prompt": prompt,
                    "choice": ans["choice"],
                    "confidence": ans["confidence"],
                    "probabilities": ans["probabilities"],
                    "model": resp.get("model"),
                }
            )
    return rows


def summarize(rows: list[dict[str, Any]], labels: dict[str, str] | None = None) -> str:
    out = [f"{len(rows)} standalone prompts; model {sorted({r['model'] for r in rows})}", ""]
    for skill in SKILLS:
        dist = Counter(r["choice"] for r in rows if r["catalog"] == skill)
        out.append(f"{skill} catalog -> {dict(dist)}")
    out += ["", f"Ambiguous (confidence < {AMBIGUOUS_BELOW}):"]
    for r in sorted(rows, key=lambda r: r["confidence"]):
        if r["confidence"] < AMBIGUOUS_BELOW:
            top = sorted(r["probabilities"].items(), key=lambda kv: -kv[1])[:2]
            pair = ", ".join(f"{k} {v:.2f}" for k, v in top)
            out.append(f"- {r['scenario']} [{r['id']}]: {pair}")
    if labels:
        by_id = {r["id"]: r for r in rows}
        unknown = sorted(set(labels) - set(by_id))
        if unknown:
            raise ValueError(f"labels name no current prompt: {unknown}")
        agree = sum(by_id[k]["choice"] == route for k, route in labels.items())
        out += ["", f"Labelled: {agree}/{len(labels)} agree"]
    return "\n".join(out) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", type=Path)
    ap.add_argument("--labels", type=Path)
    args = ap.parse_args(argv)
    labels = json.loads(args.labels.read_text()) if args.labels else None
    try:
        rows = probe()
    except jev_client.JevUnavailable as exc:
        print(f"not checked: {exc}", file=sys.stderr)
        return 2
    if args.out:
        args.out.write_text(json.dumps(rows, indent=1) + "\n")
    sys.stdout.write(summarize(rows, labels))
    return 0


if __name__ == "__main__":
    sys.exit(main())
