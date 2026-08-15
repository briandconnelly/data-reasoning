"""Build and verify the 2026-08-15 confirmatory and cost-arm fixtures.

Queries are constructed frame + content_phrase + period, so content
parallelism within a base holds by construction; the verifier re-checks it
plus snapshot temporality and cross-fixture duplicates, and can be pointed
at any fixture file with --verify-only.
"""

import argparse
import json
import re
import sys
from pathlib import Path

EVAL = Path(__file__).parent

FRAMES = {
    "profile": "Profile {c}.",
    "overview": "Give me an overview of {c}.",
    "rundown": "Give me a rundown on {c}.",
    "tell-me-about": "Tell me about {c}.",
}

# (base_id, slug, scope, entity, facet, content_phrase)
BASES = [
    (1, "route-12-crosstown", "whole", "Route 12 crosstown bus", None,
     "the Route 12 crosstown bus"),
    (2, "eastgate-garage", "whole", "Eastgate park-and-ride garage", None,
     "the Eastgate park-and-ride garage"),
    (3, "route-7-farebox", "facet", "Route 7 express", "farebox revenue",
     "farebox revenue for the Route 7 express"),
    (4, "harbor-ferry-otp", "facet", "Harbor Point ferry", "on-time performance",
     "on-time performance for the Harbor Point ferry"),
    (5, "route-22-ridership", "facet", "Route 22 loop", "ridership by stop",
     "ridership by stop for the Route 22 loop"),
    (6, "fleetwood-backlog", "facet", "Fleetwood bus depot", "maintenance backlog",
     "the maintenance backlog at the Fleetwood bus depot"),
    (7, "student-fare-program", "whole", "student fare program", None,
     "the student fare program"),
    (8, "paratransit-complaints", "facet", "paratransit service", "complaint volume",
     "complaint volume for the paratransit service"),
    (9, "downtown-transit-mall", "whole", "downtown transit mall", None,
     "the downtown transit mall"),
    (10, "central-transfers", "facet", "Central Station", "transfer volumes",
     "transfer volumes at Central Station"),
]

TEMPORAL = re.compile(
    r"evolv|grown|grew|chang|trend|over the (last|past)|since|increas|decreas"
    r"|drop|rise|rose|fell|improv|declin"
)


def build_crossed() -> list[dict]:
    rows = []
    for base_id, slug, scope, entity, facet, content in BASES:
        for act, frame in FRAMES.items():
            rows.append({
                "base_id": base_id,
                "base_slug": slug,
                "speech_act": act,
                "query": frame.format(c=content),
                "scope": scope,
                "entity": entity,
                "facet": facet,
                "content_phrase": content,
            })
    return rows


def build_cost() -> list[dict]:
    src = json.loads((EVAL / "entity-profiling-eval.json").read_text())
    rows = [q for q in src if q.get("arm") in ("N1", "N2")]
    assert len(rows) == 16, len(rows)
    return rows


def verify_crossed(rows: list[dict]) -> list[str]:
    errors = []
    if len(rows) != 40:
        errors.append(f"expected 40 rows, got {len(rows)}")
    for r in rows:
        want = FRAMES[r["speech_act"]].format(c=r["content_phrase"])
        if r["query"] != want:
            errors.append(f"base {r['base_id']}/{r['speech_act']}: not frame-parallel")
        if TEMPORAL.search(r["query"]):
            errors.append(f"base {r['base_id']}/{r['speech_act']}: temporal wording")
    whole = {r["base_id"] for r in rows if r["scope"] == "whole"}
    if whole != {1, 2, 7, 9}:
        errors.append(f"whole-entity bases {sorted(whole)} != [1, 2, 7, 9]")
    others = set()
    for name in ("entity-profiling-eval.json", "holdout.json", "crossed-pairs-2026-08-11.json"):
        others |= {q["query"] for q in json.loads((EVAL / name).read_text())}
    dupes = {r["query"] for r in rows} & others
    if dupes:
        errors.append(f"duplicates an existing fixture query: {sorted(dupes)}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--verify-only", type=Path, default=None,
                        help="verify an existing crossed-pairs fixture file and exit")
    args = parser.parse_args()

    if args.verify_only:
        errors = verify_crossed(json.loads(args.verify_only.read_text()))
    else:
        crossed = build_crossed()
        errors = verify_crossed(crossed)
        if not errors:
            (EVAL / "crossed-pairs-2026-08-15.json").write_text(
                json.dumps(crossed, indent=2, ensure_ascii=False) + "\n")
            (EVAL / "cost-arms-2026-08-15.json").write_text(
                json.dumps(build_cost(), indent=2, ensure_ascii=False) + "\n")
    for e in errors:
        print(f"FAIL: {e}")
    if not errors:
        print("verified: 40 frame-parallel snapshot queries, no cross-fixture duplicates")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
