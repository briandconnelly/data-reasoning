"""Summarize a run_eval.py results file by eval arm.

The harness reports a per-query pass against its own threshold; the gates in
this skill's design are arm means, so they are computed here instead.
"""

import argparse
import collections
import json
from pathlib import Path


def summarize(fixture_path: Path, results_path: Path) -> dict:
    arms = {x["query"]: x["arm"] for x in json.loads(fixture_path.read_text())}
    results = json.loads(results_path.read_text())
    rows = results["results"] if isinstance(results, dict) else results

    # A missing result row would otherwise vanish silently: the run-count check
    # compares runs against the queries actually found, so both sides shrink
    # together and an incomplete run yields a plausible arm mean.
    seen = collections.Counter(row["query"] for row in rows)
    missing = sorted(set(arms) - set(seen))
    extra = sorted(set(seen) - set(arms))
    duplicated = sorted(q for q, n in seen.items() if n > 1)
    if missing or extra or duplicated:
        raise SystemExit(
            "result set does not match the fixture — "
            f"missing={missing} extra={extra} duplicated={duplicated}"
        )

    by_arm = collections.defaultdict(list)
    runs_by_arm = collections.Counter()
    for row in rows:
        arm = arms[row["query"]]
        by_arm[arm].append(row["trigger_rate"])
        runs_by_arm[arm] += row["runs"]

    return {
        arm: {
            "queries": len(rates),
            "mean": round(sum(rates) / len(rates), 4),
            "runs": runs_by_arm[arm],
            "zero_rate_queries": sum(1 for r in rates if r == 0.0),
        }
        for arm, rates in sorted(by_arm.items())
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Summarize trigger-eval results by arm")
    parser.add_argument("--fixture", required=True, type=Path)
    parser.add_argument("--results", required=True, type=Path)
    parser.add_argument("--expected-runs-per-query", type=int, required=True)
    args = parser.parse_args()

    summary = summarize(args.fixture, args.results)
    for arm, stats in summary.items():
        expected = stats["queries"] * args.expected_runs_per_query
        flag = "" if stats["runs"] == expected else f"  RUN COUNT MISMATCH (expected {expected})"
        print(
            f"{arm}: mean={stats['mean']:.3f} queries={stats['queries']} runs={stats['runs']}{flag}"
        )
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
