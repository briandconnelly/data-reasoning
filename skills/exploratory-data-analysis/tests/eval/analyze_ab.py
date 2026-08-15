#!/usr/bin/env python3
"""Frozen, preregistered analysis for the interleaved two-description A/B.

This script is the single computational home for the Phase A gates of
``2026-08-11-veto-fix-prereg.md``. It reads the ``results.jsonl`` emitted by
``run_desc_eval.py`` (one JSON object per invocation attempt), checks validity
and completeness, computes fixture-arm means per description, evaluates the
three gates top-down, and prints the verdict plus the recorded-not-gating
diagnostics.

Arm membership is read from the fixture's own ``arm`` field, keyed by query
index. No reconstruction is performed and no separate arms file exists.

Gates, hardcoded here, evaluated strictly top-down; the first failure decides
the verdict and nothing below it is evaluated:

1. Instrument -- baseline P0 mean >= 0.8, else VOID.
2. No harm -- treatment P0 >= 0.8 and treatment N1 <= 0.2 and
   (N1 treatment - N1 baseline) <= 0.10 and treatment N2 <= 0.2,
   else NO_SHIP_HARM.
3. Ship -- (P1 treatment - P1 baseline) >= 0, else NO_SHIP_REGRESSION;
   otherwise SHIP.

Everything else it prints -- the paired per-query interval, the mechanism mean,
order diagnostics, tag breakdowns, the F arm -- is disclosure, never a gate.

Exit codes: 0 the analysis ran; 1 bad usage or unreadable input; 2 a validity,
completeness, duplication, or digest check failed (no result is inspected).

All arithmetic on rates uses ``fractions.Fraction``, so gate comparisons such as
"delta >= 0" are exact rather than floating-point approximate. Floats appear
only in printed and JSON output.
"""

from __future__ import annotations

import argparse
import json
import math
import sys
from collections import defaultdict
from dataclasses import dataclass
from fractions import Fraction
from pathlib import Path

DESC_ARMS = ("baseline", "treatment")
FIXTURE_ARM_ORDER = ("P0", "P1", "N1", "N2", "F")
GATED_ARMS = ("P0", "P1", "N1", "N2")

GATE1_BASELINE_P0_MIN = Fraction(8, 10)
GATE2_TREATMENT_P0_MIN = Fraction(8, 10)
GATE2_TREATMENT_N1_MAX = Fraction(2, 10)
GATE2_DELTA_N1_MAX = Fraction(1, 10)
GATE2_TREATMENT_N2_MAX = Fraction(2, 10)

PERM_ALPHA_NUM = 25  # two-sided 95% -> 0.025 per tail, as 25/1000
PERM_ALPHA_DEN = 1000
EXPECTED_DIGESTS = 2


class CheckFailure(Exception):
    """A validity, completeness, duplication, or digest check failed."""


@dataclass(frozen=True)
class GroupMean:
    """One fixture arm x description cell: counts and its two means."""

    queries: int
    invocations: int
    triggers: int
    mean: Fraction | None
    mean_of_query_rates: Fraction | None


Outcomes = dict[tuple[int, str], list[bool]]
Means = dict[str, dict[str, GroupMean]]


def fail(messages: list[str]) -> None:
    """Raise a CheckFailure carrying every message, if there are any."""
    if messages:
        raise CheckFailure("\n".join(messages))


def as_float(value: Fraction | None) -> float | None:
    return None if value is None else float(value)


def delta(left: Fraction | None, right: Fraction | None) -> Fraction | None:
    return None if left is None or right is None else left - right


def fmt(value: Fraction | float | None, places: int = 4) -> str:
    if value is None:
        return "n/a"
    return f"{float(value):.{places}f}"


# ---------------------------------------------------------------- input


def load_rows(path: Path) -> list[dict]:
    """Read results.jsonl; every non-blank line must be a JSON object."""
    rows = []
    with path.open(encoding="utf-8") as handle:
        for number, raw in enumerate(handle, start=1):
            line = raw.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as error:
                raise CheckFailure(f"{path}:{number}: unparseable JSON line: {error}") from error
            if not isinstance(row, dict):
                raise CheckFailure(f"{path}:{number}: line is not a JSON object")
            rows.append(row)
    if not rows:
        raise CheckFailure(f"{path}: no result rows")
    return rows


def load_fixture(path: Path) -> list[dict]:
    """Read the eval fixture; every item needs an ``arm`` and a ``query``."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        raise CheckFailure(f"{path}: expected a non-empty JSON list of fixture items")
    problems = []
    for index, item in enumerate(data):
        if not isinstance(item, dict):
            problems.append(f"fixture item {index} is not an object")
            continue
        if not isinstance(item.get("arm"), str):
            problems.append(f"fixture item {index} has no string 'arm' field")
        if not isinstance(item.get("query"), str):
            problems.append(f"fixture item {index} has no string 'query' field")
    fail(problems)
    return data


def fixture_arms(fixture: list[dict]) -> dict[str, list[int]]:
    """Arm name -> sorted 0-based query indices, straight from the fixture."""
    arms: dict[str, list[int]] = defaultdict(list)
    for index, item in enumerate(fixture):
        arms[str(item["arm"])].append(index)
    return {name: sorted(indices) for name, indices in arms.items()}


def load_tags(path: Path | None) -> dict[int, dict[str, str]]:
    if path is None:
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise CheckFailure(f"{path}: expected an object mapping query_index -> tag object")
    return {
        int(key): {str(k): str(v) for k, v in dict(value).items()} for key, value in data.items()
    }


# ---------------------------------------------------------------- checks


def check_schema(rows: list[dict]) -> list[str]:
    """Every row must carry the fields the analysis reads, with legal values."""
    required = ("query_index", "query", "arm_label", "desc_sha256", "run", "status", "triggered")
    problems = []
    for number, row in enumerate(rows, start=1):
        missing = [field for field in required if field not in row]
        if missing:
            problems.append(f"row {number}: missing field(s) {', '.join(missing)}")
            continue
        if row["arm_label"] not in DESC_ARMS:
            problems.append(
                f"row {number}: arm_label {row['arm_label']!r} is not one of {DESC_ARMS}"
            )
        if row["status"] not in ("valid", "void"):
            problems.append(f"row {number}: status {row['status']!r} is not 'valid' or 'void'")
        elif row["status"] == "valid" and not isinstance(row["triggered"], bool):
            problems.append(
                f"row {number}: valid row has non-boolean triggered={row['triggered']!r}"
            )
    return problems


def check_digests(rows: list[dict]) -> tuple[dict[str, str], list[str]]:
    """Each description arm serves exactly one digest; report every foreign one.

    The canonical digest for an arm is the one its rows carry most often (ties
    broken by digest string, so the result is deterministic). Any row whose
    digest differs is foreign and fails the check. Exactly two canonical
    digests must exist and they must differ.
    """
    seen: dict[str, dict[str, int]] = {arm: defaultdict(int) for arm in DESC_ARMS}
    for row in rows:
        arm = row.get("arm_label")
        if isinstance(arm, str) and arm in seen:
            seen[arm][str(row.get("desc_sha256"))] += 1
    canonical = {}
    for arm, counts in seen.items():
        if counts:
            canonical[arm] = min(counts.items(), key=lambda item: (-item[1], item[0]))[0]
    problems = []
    for number, row in enumerate(rows, start=1):
        arm = row.get("arm_label")
        if (
            isinstance(arm, str)
            and arm in canonical
            and str(row.get("desc_sha256")) != canonical[arm]
        ):
            problems.append(
                f"row {number}: foreign desc_sha256 {row.get('desc_sha256')!r} "
                f"for arm {arm!r} (expected {canonical[arm]!r})"
            )
    distinct = sorted(set(canonical.values()))
    if len(canonical) != len(DESC_ARMS):
        problems.append(
            f"expected rows for both description arms {DESC_ARMS}; found {sorted(canonical)}"
        )
    elif len(distinct) != EXPECTED_DIGESTS:
        problems.append(f"expected two distinct description digests; found {distinct}")
    return canonical, problems


def check_fixture_match(rows: list[dict], fixture: list[dict]) -> list[str]:
    """Result rows must point at real fixture rows and carry their exact text."""
    problems = []
    mismatched = set()
    for row in rows:
        index = row.get("query_index")
        if not isinstance(index, int) or not 0 <= index < len(fixture):
            problems.append(f"result row has query_index {index!r} outside the fixture")
            continue
        expected = fixture[index]["query"]
        if row.get("query") != expected and index not in mismatched:
            mismatched.add(index)
            problems.append(
                f"query_index {index}: result query text does not match the fixture "
                f"(fixture {expected!r}, result {row.get('query')!r})"
            )
    return sorted(set(problems))


def check_completeness(rows: list[dict], fixture: list[dict], expected_runs: int) -> list[str]:
    """Every (query, description arm) needs exactly one valid row per run."""
    by_cell: dict[tuple[int, str], dict[int, int]] = defaultdict(lambda: defaultdict(int))
    for row in rows:
        if row.get("status") != "valid":
            continue
        by_cell[(row["query_index"], row["arm_label"])][row["run"]] += 1
    problems = []
    for index in range(len(fixture)):
        for arm in DESC_ARMS:
            runs = by_cell.get((index, arm), {})
            for run, count in sorted(runs.items()):
                if count > 1:
                    problems.append(
                        f"query_index {index} arm {arm} run {run}: "
                        f"{count} valid rows (duplicate final rows)"
                    )
            valid = sum(runs.values())
            if valid < expected_runs:
                problems.append(
                    f"query_index {index} arm {arm}: {valid} valid invocation(s), "
                    f"expected {expected_runs}"
                )
    return problems


def collect_voids(rows: list[dict]) -> list[dict]:
    voids = [
        {
            "query_index": row.get("query_index"),
            "arm_label": row.get("arm_label"),
            "run": row.get("run"),
            "attempt": row.get("attempt"),
            "invalid_reason": row.get("invalid_reason"),
            "transcript_file": row.get("transcript_file"),
        }
        for row in rows
        if row.get("status") == "void"
    ]
    return sorted(
        voids,
        key=lambda v: (
            v["query_index"] or 0,
            str(v["arm_label"]),
            v["run"] or 0,
            v["attempt"] or 0,
        ),
    )


# ---------------------------------------------------------------- rates


def build_outcomes(rows: list[dict]) -> Outcomes:
    """Per (query index, description arm), the valid invocations' outcomes."""
    collected: dict[tuple[int, str], list[tuple[int, bool]]] = defaultdict(list)
    for row in rows:
        if row.get("status") != "valid":
            continue
        collected[(row["query_index"], row["arm_label"])].append(
            (row["run"], bool(row["triggered"]))
        )
    return {key: [flag for _, flag in sorted(pairs)] for key, pairs in collected.items()}


def query_rate(outcomes: Outcomes, index: int, arm: str) -> Fraction | None:
    flags = outcomes.get((index, arm))
    if not flags:
        return None
    return Fraction(sum(flags), len(flags))


def group_mean(outcomes: Outcomes, indices: list[int], arm: str) -> GroupMean:
    """Invocation-level mean (the gate value) plus the mean of per-query rates."""
    flags = [flag for index in indices for flag in outcomes.get((index, arm), [])]
    rates = [rate for index in indices if (rate := query_rate(outcomes, index, arm)) is not None]
    return GroupMean(
        queries=len(rates),
        invocations=len(flags),
        triggers=sum(flags),
        mean=Fraction(sum(flags), len(flags)) if flags else None,
        mean_of_query_rates=sum(rates, Fraction(0)) / len(rates) if rates else None,
    )


def arm_means(outcomes: Outcomes, arms: dict[str, list[int]]) -> Means:
    return {
        name: {arm: group_mean(outcomes, arms[name], arm) for arm in DESC_ARMS}
        for name in sorted(arms)
    }


def mean_value(means: Means, name: str, arm: str) -> Fraction | None:
    entry = means.get(name, {}).get(arm)
    return None if entry is None else entry.mean


# ---------------------------------------------------------------- gates


def _check(label: str, value: Fraction | None, ok: bool, detail: str) -> dict:
    return {"label": label, "value": as_float(value), "detail": detail, "pass": ok}


def gate_checks(means: Means) -> tuple[list[dict], list[dict], list[dict]]:
    """The three gates' individual checks, computed but not yet sequenced."""
    b_p0 = mean_value(means, "P0", "baseline")
    t_p0 = mean_value(means, "P0", "treatment")
    b_n1 = mean_value(means, "N1", "baseline")
    t_n1 = mean_value(means, "N1", "treatment")
    t_n2 = mean_value(means, "N2", "treatment")
    b_p1 = mean_value(means, "P1", "baseline")
    t_p1 = mean_value(means, "P1", "treatment")
    delta_n1 = delta(t_n1, b_n1)
    delta_p1 = delta(t_p1, b_p1)
    gate1 = [
        _check("baseline P0", b_p0, b_p0 is not None and b_p0 >= GATE1_BASELINE_P0_MIN, ">= 0.8")
    ]
    gate2 = [
        _check("treatment P0", t_p0, t_p0 is not None and t_p0 >= GATE2_TREATMENT_P0_MIN, ">= 0.8"),
        _check("treatment N1", t_n1, t_n1 is not None and t_n1 <= GATE2_TREATMENT_N1_MAX, "<= 0.2"),
        _check(
            "delta N1 (treatment - baseline)",
            delta_n1,
            delta_n1 is not None and delta_n1 <= GATE2_DELTA_N1_MAX,
            "<= 0.10",
        ),
        _check("treatment N2", t_n2, t_n2 is not None and t_n2 <= GATE2_TREATMENT_N2_MAX, "<= 0.2"),
    ]
    gate3 = [
        _check(
            "delta P1 (treatment - baseline)",
            delta_p1,
            delta_p1 is not None and delta_p1 >= 0,
            ">= 0",
        )
    ]
    return gate1, gate2, gate3


def evaluate_gates(means: Means) -> dict:
    """Run the gates top-down; the first failure decides and stops evaluation."""
    definitions = [
        ("gate1_instrument", "Instrument", "VOID"),
        ("gate2_no_harm", "No harm", "NO_SHIP_HARM"),
        ("gate3_ship", "Ship", "NO_SHIP_REGRESSION"),
    ]
    all_checks = gate_checks(means)
    gates = []
    verdict = "SHIP"
    for (key, title, failure_verdict), checks in zip(definitions, all_checks, strict=True):
        if verdict != "SHIP":
            gates.append(
                {"key": key, "title": title, "evaluated": False, "checks": [], "pass": None}
            )
            continue
        passed = all(check["pass"] for check in checks)
        gates.append(
            {"key": key, "title": title, "evaluated": True, "checks": checks, "pass": passed}
        )
        if not passed:
            verdict = failure_verdict
    return {"gates": gates, "verdict": verdict}


# ------------------------------------------------- permutation interval


def signflip_distribution(scaled: list[int]) -> dict[int, int]:
    """Exact distribution of sum(s_i * d_i), s_i in {-1,+1}, by DP convolution.

    Equivalent to full 2^n enumeration but keyed by attainable sums, so the
    work is bounded by the lattice width rather than by 2^n.
    """
    counts: dict[int, int] = {0: 1}
    for value in scaled:
        magnitude = abs(value)
        nxt: dict[int, int] = defaultdict(int)
        for total, count in counts.items():
            nxt[total + magnitude] += count
            nxt[total - magnitude] += count
        counts = dict(nxt)
    return counts


def _tail_quantiles(counts: dict[int, int], total: int) -> tuple[int, int]:
    """Lower and upper 2.5% critical points of the null sum distribution."""
    ordered = sorted(counts)
    cumulative = 0
    low = ordered[0]
    for value in ordered:
        cumulative += counts[value]
        if cumulative * PERM_ALPHA_DEN >= total * PERM_ALPHA_NUM:
            low = value
            break
    cumulative = 0
    high = ordered[-1]
    for value in reversed(ordered):
        cumulative += counts[value]
        if cumulative * PERM_ALPHA_DEN >= total * PERM_ALPHA_NUM:
            high = value
            break
    return low, high


def permutation_interval(diffs: list[Fraction]) -> dict:
    """Two-sided 95% interval for the mean paired difference, by sign-flip.

    The interval inverts the exact paired sign-flip test: it is the observed
    mean shifted by the null distribution's 2.5% critical points, so it
    excludes 0 exactly when the sign-flip test rejects at 5%. Disclosure only;
    the prereg makes no gate of it.
    """
    if not diffs:
        return {"method": "none", "n": 0}
    count = len(diffs)
    denominator = math.lcm(*(diff.denominator for diff in diffs))
    scaled = [int(diff * denominator) for diff in diffs]
    counts = signflip_distribution(scaled)
    total = 2**count
    low, high = _tail_quantiles(counts, total)
    observed = sum(scaled)
    mean = Fraction(observed, denominator * count)
    scale = Fraction(1, denominator * count)
    extreme = sum(number for value, number in counts.items() if abs(value) >= abs(observed))
    return {
        "method": (
            f"exact sign-flip DP convolution over {count} paired differences "
            f"(all 2^{count} = {total} assignments enumerated exactly)"
        ),
        "n": count,
        "mean": float(mean),
        "ci_low": float(mean - high * scale),
        "ci_high": float(mean - low * scale),
        "null_critical_low": float(low * scale),
        "null_critical_high": float(high * scale),
        "p_two_sided": float(Fraction(extreme, total)),
        "excludes_zero": bool((mean - high * scale) > 0 or (mean - low * scale) < 0),
    }


# ---------------------------------------------------------------- extras


def paired_differences(outcomes: Outcomes, indices: list[int]) -> tuple[list[dict], list[Fraction]]:
    rows = []
    diffs = []
    for index in sorted(indices):
        baseline = query_rate(outcomes, index, "baseline")
        treatment = query_rate(outcomes, index, "treatment")
        if baseline is None or treatment is None:
            continue
        difference = treatment - baseline
        diffs.append(difference)
        rows.append(
            {
                "query_index": index,
                "baseline": float(baseline),
                "treatment": float(treatment),
                "diff": float(difference),
            }
        )
    return rows, diffs


def sign_summary(diffs: list[Fraction]) -> dict[str, int]:
    return {
        "improved": sum(1 for diff in diffs if diff > 0),
        "unchanged": sum(1 for diff in diffs if diff == 0),
        "worsened": sum(1 for diff in diffs if diff < 0),
    }


def mechanism_summary(outcomes: Outcomes, indices: list[int]) -> dict:
    baseline = group_mean(outcomes, indices, "baseline").mean
    treatment = group_mean(outcomes, indices, "treatment").mean
    return {
        "query_indices": sorted(indices),
        "baseline": as_float(baseline),
        "treatment": as_float(treatment),
        "delta": as_float(delta(treatment, baseline)),
        "per_query": [
            {
                "query_index": index,
                "baseline": as_float(query_rate(outcomes, index, "baseline")),
                "treatment": as_float(query_rate(outcomes, index, "treatment")),
            }
            for index in sorted(indices)
        ],
    }


def order_diagnostics(rows: list[dict]) -> dict[str, dict[str, dict[str, dict]]]:
    """Valid-invocation trigger rate by which_first and by run, per description."""
    buckets: dict[str, dict[str, dict[str, list[bool]]]] = {
        "by_which_first": defaultdict(lambda: defaultdict(list)),
        "by_run": defaultdict(lambda: defaultdict(list)),
    }
    for row in rows:
        if row.get("status") != "valid":
            continue
        arm = str(row.get("arm_label"))
        buckets["by_which_first"][str(row.get("which_first"))][arm].append(bool(row["triggered"]))
        buckets["by_run"][str(row.get("run"))][arm].append(bool(row["triggered"]))
    report: dict[str, dict[str, dict[str, dict]]] = {}
    for facet, groups in buckets.items():
        report[facet] = {}
        for key in sorted(groups):
            entry: dict[str, dict] = {}
            for arm in DESC_ARMS:
                flags = groups[key].get(arm, [])
                entry[arm] = {
                    "n": len(flags),
                    "rate": float(sum(flags) / len(flags)) if flags else None,
                }
            report[facet][key] = entry
    return report


def tag_breakdown(
    outcomes: Outcomes, p1_indices: list[int], tags: dict[int, dict[str, str]]
) -> dict[str, dict[str, dict]]:
    fields = sorted({field for index in p1_indices for field in tags.get(index, {})})
    report: dict[str, dict[str, dict]] = {}
    for field in fields:
        by_value: dict[str, list[int]] = defaultdict(list)
        for index in sorted(p1_indices):
            value = tags.get(index, {}).get(field)
            if value is not None:
                by_value[str(value)].append(index)
        report[field] = {}
        for value in sorted(by_value):
            indices = by_value[value]
            baseline = group_mean(outcomes, indices, "baseline").mean
            treatment = group_mean(outcomes, indices, "treatment").mean
            report[field][value] = {
                "queries": len(indices),
                "query_indices": indices,
                "baseline": as_float(baseline),
                "treatment": as_float(treatment),
                "delta": as_float(delta(treatment, baseline)),
            }
    return report


# ---------------------------------------------------------------- report


def arm_sort_key(name: str) -> tuple[int, str]:
    order = FIXTURE_ARM_ORDER.index(name) if name in FIXTURE_ARM_ORDER else len(FIXTURE_ARM_ORDER)
    return (order, name)


def means_json(means: Means) -> dict:
    return {
        name: {
            arm: {
                "queries": entry.queries,
                "invocations": entry.invocations,
                "triggers": entry.triggers,
                "mean": as_float(entry.mean),
                "mean_of_query_rates": as_float(entry.mean_of_query_rates),
            }
            for arm, entry in sorted(per_arm.items())
        }
        for name, per_arm in sorted(means.items())
    }


def print_means(means: Means) -> None:
    print("== Arm means (valid invocations only) ==")
    header = f"{'arm':<5} {'baseline':>10} {'treatment':>10} {'delta':>10}"
    print(f"{header}  n(queries)  n(invocations)")
    for name in sorted(means, key=arm_sort_key):
        baseline = means[name]["baseline"]
        treatment = means[name]["treatment"]
        note = "  (recorded, never gated)" if name not in GATED_ARMS else ""
        print(
            f"{name:<5} {fmt(baseline.mean):>10} {fmt(treatment.mean):>10} "
            f"{fmt(delta(treatment.mean, baseline.mean)):>10}  {baseline.queries:>10}  "
            f"{baseline.invocations + treatment.invocations:>14}{note}"
        )
    print()


def print_gates(result: dict) -> None:
    print("== Gates (top-down; first failure decides) ==")
    for gate in result["gates"]:
        if not gate["evaluated"]:
            print(f"{gate['key']} ({gate['title']}): NOT EVALUATED (an earlier gate failed)")
            continue
        status = "PASS" if gate["pass"] else "FAIL"
        print(f"{gate['key']} ({gate['title']}): {status}")
        for check in gate["checks"]:
            mark = "PASS" if check["pass"] else "FAIL"
            print(f"    {check['label']:<32} = {fmt(check['value'])}  {check['detail']:<8} {mark}")
    print(f"\nVERDICT: {result['verdict']}\n")


def print_paired(paired: dict) -> None:
    print("== Paired per-query P1 differences (disclosure, not a gate) ==")
    for row in paired["per_query"]:
        print(
            f"  q{row['query_index']:>3}  baseline={row['baseline']:.4f}  "
            f"treatment={row['treatment']:.4f}  diff={row['diff']:+.4f}"
        )
    signs = paired["signs"]
    print(f"  mean difference: {fmt(paired['mean_difference'])}")
    print(
        f"  signs: improved={signs['improved']} unchanged={signs['unchanged']} "
        f"worsened={signs['worsened']}"
    )
    interval = paired["permutation"]
    if interval.get("n"):
        print(f"  method: {interval['method']}")
        print(
            f"  two-sided 95% interval: [{interval['ci_low']:+.4f}, {interval['ci_high']:+.4f}]"
            f"   p={interval['p_two_sided']:.4f}   excludes 0: {interval['excludes_zero']}"
        )
    print()


def print_order(order: dict) -> None:
    print("== Order diagnostics (recorded, not gating) ==")
    for facet, groups in sorted(order.items()):
        print(f"  {facet}:")
        for key, entry in groups.items():
            parts = [f"{arm}={fmt(entry[arm]['rate'])} (n={entry[arm]['n']})" for arm in DESC_ARMS]
            print(f"    {key:<12} " + "  ".join(parts))
    print()


def print_tags(tags: dict) -> None:
    if not tags:
        return
    print("== P1 means by tag value (disclosure) ==")
    for field, values in sorted(tags.items()):
        print(f"  {field}:")
        for value, entry in sorted(values.items()):
            print(
                f"    {value:<14} baseline={fmt(entry['baseline'])} "
                f"treatment={fmt(entry['treatment'])} delta={fmt(entry['delta'])} "
                f"queries={entry['queries']}"
            )
    print()


def print_validity(report: dict) -> None:
    print("== Validity and completeness ==")
    counts = report["validity"]
    print(
        f"  rows={counts['rows']}  valid={counts['valid']}  void={counts['void']}  "
        f"expected_runs={counts['expected_runs']}"
    )
    print("  arm membership: read from the fixture's 'arm' field")
    for name in sorted(report["arm_sizes"], key=arm_sort_key):
        print(f"    {name}: {report['arm_sizes'][name]} queries")
    for arm, digest in sorted(report["digests"].items()):
        print(f"  digest[{arm}] = {digest}")
    if counts["void"]:
        print("  voids (retried, not scored):")
        for void in report["voids"]:
            print(
                f"    q{void['query_index']} {void['arm_label']} run={void['run']} "
                f"attempt={void['attempt']} reason={void['invalid_reason']}"
            )
    print()


def print_report(report: dict) -> None:
    print_validity(report)
    print_means(report["means"])
    print_gates(report["gate_result"])
    print_paired(report["paired_p1"])
    if report["mechanism"] is not None:
        mechanism = report["mechanism"]
        print("== Mechanism mean (recorded, not gating) ==")
        print(f"  queries: {mechanism['query_indices']}")
        print(
            f"  baseline={fmt(mechanism['baseline'])}  treatment={fmt(mechanism['treatment'])}  "
            f"delta={fmt(mechanism['delta'])}\n"
        )
    print_order(report["order"])
    print_tags(report["tags"])


# ---------------------------------------------------------------- driver


def build_report(args: argparse.Namespace) -> dict:
    rows = load_rows(args.results)
    fixture = load_fixture(args.fixture)
    arms = fixture_arms(fixture)
    tags = load_tags(args.tags)

    fail(check_schema(rows))
    digests, digest_problems = check_digests(rows)
    fail(digest_problems)
    fail(check_fixture_match(rows, fixture))
    fail(check_completeness(rows, fixture, args.expected_runs))

    outcomes = build_outcomes(rows)
    means = arm_means(outcomes, arms)
    gate_result = evaluate_gates(means)
    per_query, diffs = paired_differences(outcomes, arms.get("P1", []))
    mechanism = (
        None
        if args.mechanism_queries is None
        else mechanism_summary(outcomes, args.mechanism_queries)
    )
    mean_difference = float(sum(diffs, Fraction(0)) / len(diffs)) if diffs else None
    return {
        "results_file": str(args.results),
        "fixture_file": str(args.fixture),
        "expected_runs": args.expected_runs,
        "arm_sizes": {name: len(indices) for name, indices in sorted(arms.items())},
        "digests": digests,
        "validity": {
            "rows": len(rows),
            "valid": sum(1 for row in rows if row["status"] == "valid"),
            "void": sum(1 for row in rows if row["status"] == "void"),
            "expected_runs": args.expected_runs,
        },
        "voids": collect_voids(rows),
        "means": means,
        "gate_result": gate_result,
        "verdict": gate_result["verdict"],
        "paired_p1": {
            "per_query": per_query,
            "mean_difference": mean_difference,
            "signs": sign_summary(diffs),
            "permutation": permutation_interval(diffs),
        },
        "mechanism": mechanism,
        "order": order_diagnostics(rows),
        "tags": tag_breakdown(outcomes, arms.get("P1", []), tags),
    }


def json_ready(report: dict) -> dict:
    payload = dict(report)
    payload["means"] = means_json(report["means"])
    return payload


def parse_index_list(raw: str | None) -> list[int] | None:
    if raw is None:
        return None
    data = json.loads(raw)
    if not isinstance(data, list) or not all(isinstance(item, int) for item in data):
        raise CheckFailure("--mechanism-queries must be a JSON list of integers")
    return sorted(set(data))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preregistered A/B analysis and gates for the description veto fix."
    )
    parser.add_argument("--results", required=True, type=Path, help="results.jsonl to analyze")
    parser.add_argument(
        "--fixture", required=True, type=Path, help="Eval fixture JSON (carries the arm field)"
    )
    parser.add_argument(
        "--mechanism-queries",
        default=None,
        help="JSON list of 0-based query indices for the recorded mechanism mean",
    )
    parser.add_argument(
        "--tags", default=None, type=Path, help="JSON object: query_index -> tag fields"
    )
    parser.add_argument("--expected-runs", type=int, default=3, help="Valid runs per (query, arm)")
    parser.add_argument("--json", action="store_true", help="Emit the full report as JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        args.mechanism_queries = parse_index_list(args.mechanism_queries)
        report = build_report(args)
    except CheckFailure as error:
        print(f"CHECK FAILED — no result is inspected.\n{error}", file=sys.stderr)
        return 2
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(json_ready(report), indent=2, sort_keys=True))
    else:
        print_report(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
