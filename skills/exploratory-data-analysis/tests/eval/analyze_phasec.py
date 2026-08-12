#!/usr/bin/env python3
"""Frozen, preregistered analysis for Phase C, the crossed speech-act pairs.

This script is the single computational home for the Phase C verdict of
``2026-08-11-veto-fix-prereg.md``. It reads the ``results.jsonl`` emitted by
``run_desc_eval.py`` (one JSON object per invocation attempt), checks validity
and completeness with the same rigor as ``analyze_ab.py``, computes the
preregistered estimand, and prints the support level plus the disclosure
tables.

The estimand, quoted from the preregistration's Phase C section:

    per base i and description D, gap_i(D) = rate(profile) - mean(rate over
    the three generic acts). theta_i = gap_i(B) - gap_i(T); positive theta
    means the treatment narrowed the profile-vs-generic gap. Estimator:
    theta_bar = mean over the 10 bases; uncertainty: exact paired sign-flip
    permutation of theta_i (all 2^10 enumerations, deterministic),
    two-sided 95%.

Support levels, quoted from the same section: **confirmed** if theta_bar > 0
and the permutation interval excludes 0; **directional** if theta_bar > 0
otherwise; **not supported** if theta_bar <= 0.

The reopen rule is also evaluated and printed. The preregistration's rule has a
process precondition this script cannot see -- "if Phase A shipped and Phase C
lands not supported" -- so what is printed is the rule's measurable half:
``theta_bar < 0 and the interval excludes 0``. Reading it as the reopen trigger
requires the Phase A ship verdict from ``analyze_ab.py``, and the printed line
says so.

Base membership, speech-act membership, and scope are read from the fixture's
own ``base_id``, ``speech_act``, and ``scope`` fields, keyed by query index. No
reconstruction is performed and no separate mapping file exists.

Everything below the verdict -- the per-base table, the per-speech-act
marginals, the whole-versus-facet split, the order diagnostics -- is
disclosure, never gating.

Exit codes: 0 the analysis ran; 1 bad usage or unreadable input; 2 a validity,
completeness, duplication, or digest check failed (no result is inspected).

All arithmetic on rates uses ``fractions.Fraction``, so sign comparisons such
as "theta_bar > 0" are exact rather than floating-point approximate. Floats
appear only in printed and JSON output.
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
PROFILE_ACT = "profile"
GENERIC_ACTS = ("overview", "rundown", "tell-me-about")
SPEECH_ACTS = (PROFILE_ACT, *GENERIC_ACTS)
SCOPES = ("whole", "facet")

PERM_ALPHA_NUM = 25  # two-sided 95% -> 0.025 per tail, as 25/1000
PERM_ALPHA_DEN = 1000
EXPECTED_DIGESTS = 2


class CheckFailure(Exception):
    """A validity, completeness, duplication, or digest check failed."""


@dataclass(frozen=True)
class Base:
    """One authored base: its four speech-act queries and its scope."""

    base_id: int
    base_slug: str
    scope: str
    indices: dict[str, int]


@dataclass(frozen=True)
class CellRate:
    """One (query, description) cell: counts and its trigger rate."""

    invocations: int
    triggers: int
    rate: Fraction | None


Outcomes = dict[tuple[int, str], list[bool]]


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


def mean_of(values: list[Fraction]) -> Fraction | None:
    return sum(values, Fraction(0)) / len(values) if values else None


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
    """Read the crossed-pairs fixture; every item needs the crossing fields."""
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list) or not data:
        raise CheckFailure(f"{path}: expected a non-empty JSON list of fixture items")
    problems = []
    for index, item in enumerate(data):
        if not isinstance(item, dict):
            problems.append(f"fixture item {index} is not an object")
            continue
        if not isinstance(item.get("base_id"), int):
            problems.append(f"fixture item {index} has no integer 'base_id' field")
        if not isinstance(item.get("query"), str):
            problems.append(f"fixture item {index} has no string 'query' field")
        act = item.get("speech_act")
        if act not in SPEECH_ACTS:
            problems.append(
                f"fixture item {index} has speech_act {act!r}, not one of {SPEECH_ACTS}"
            )
        scope = item.get("scope")
        if scope not in SCOPES:
            problems.append(f"fixture item {index} has scope {scope!r}, not one of {SCOPES}")
    fail(problems)
    return data


def fixture_bases(fixture: list[dict]) -> list[Base]:
    """Group the fixture into bases; every base must cross all four acts once.

    The crossing is what the estimand is defined on, so a base missing an act,
    carrying an act twice, or mixing scopes is a fixture defect, not a result
    to interpret.
    """
    grouped: dict[int, list[tuple[int, dict]]] = defaultdict(list)
    for index, item in enumerate(fixture):
        grouped[int(item["base_id"])].append((index, item))
    problems = []
    bases = []
    for base_id in sorted(grouped):
        items = grouped[base_id]
        indices: dict[str, int] = {}
        for index, item in items:
            act = str(item["speech_act"])
            if act in indices:
                problems.append(
                    f"base {base_id}: speech act {act!r} appears at query_index "
                    f"{indices[act]} and {index}"
                )
                continue
            indices[act] = index
        missing = [act for act in SPEECH_ACTS if act not in indices]
        if missing:
            problems.append(f"base {base_id}: missing speech act(s) {', '.join(missing)}")
        scopes = sorted({str(item["scope"]) for _, item in items})
        if len(scopes) != 1:
            problems.append(f"base {base_id}: mixed scope values {scopes}")
        slugs = sorted({str(item.get("base_slug", "")) for _, item in items})
        if len(slugs) != 1:
            problems.append(f"base {base_id}: mixed base_slug values {slugs}")
        bases.append(
            Base(
                base_id=base_id,
                base_slug=slugs[0] if len(slugs) == 1 else "",
                scope=scopes[0] if len(scopes) == 1 else "",
                indices=indices,
            )
        )
    fail(problems)
    return bases


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


def cell_rate(outcomes: Outcomes, index: int, arm: str) -> CellRate:
    flags = outcomes.get((index, arm), [])
    return CellRate(
        invocations=len(flags),
        triggers=sum(flags),
        rate=Fraction(sum(flags), len(flags)) if flags else None,
    )


def query_rate(outcomes: Outcomes, index: int, arm: str) -> Fraction | None:
    return cell_rate(outcomes, index, arm).rate


def pooled_rate(outcomes: Outcomes, indices: list[int], arm: str) -> CellRate:
    """Invocation-level rate pooled over a set of queries, for one description."""
    flags = [flag for index in indices for flag in outcomes.get((index, arm), [])]
    return CellRate(
        invocations=len(flags),
        triggers=sum(flags),
        rate=Fraction(sum(flags), len(flags)) if flags else None,
    )


# ---------------------------------------------------------------- estimand


def base_gap(outcomes: Outcomes, base: Base, arm: str) -> dict:
    """gap = rate(profile) - mean(rate over the three generic acts), exactly."""
    rates = {act: query_rate(outcomes, base.indices[act], arm) for act in SPEECH_ACTS}
    profile = rates[PROFILE_ACT]
    generic = [rates[act] for act in GENERIC_ACTS]
    generic_mean = (
        None
        if any(rate is None for rate in generic)
        else mean_of([rate for rate in generic if rate is not None])
    )
    return {
        "rates": rates,
        "profile": profile,
        "generic_mean": generic_mean,
        "gap": delta(profile, generic_mean),
    }


def base_thetas(outcomes: Outcomes, bases: list[Base]) -> tuple[list[dict], list[Fraction]]:
    """Per base: both descriptions' four rates and gaps, plus theta_i."""
    per_base = []
    thetas = []
    for base in bases:
        gaps = {arm: base_gap(outcomes, base, arm) for arm in DESC_ARMS}
        theta = delta(gaps["baseline"]["gap"], gaps["treatment"]["gap"])
        if theta is not None:
            thetas.append(theta)
        per_base.append(
            {
                "base_id": base.base_id,
                "base_slug": base.base_slug,
                "scope": base.scope,
                "query_indices": {act: base.indices[act] for act in SPEECH_ACTS},
                "rates": {
                    arm: {act: as_float(gaps[arm]["rates"][act]) for act in SPEECH_ACTS}
                    for arm in DESC_ARMS
                },
                "profile": {arm: as_float(gaps[arm]["profile"]) for arm in DESC_ARMS},
                "generic_mean": {arm: as_float(gaps[arm]["generic_mean"]) for arm in DESC_ARMS},
                "gap": {arm: as_float(gaps[arm]["gap"]) for arm in DESC_ARMS},
                "theta": as_float(theta),
                "theta_exact": None if theta is None else str(theta),
            }
        )
    return per_base, thetas


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
    """Two-sided 95% interval for theta_bar, by exact paired sign flip.

    The interval inverts the exact sign-flip test: it is the observed mean
    shifted by the null distribution's 2.5% critical points, so it excludes 0
    exactly when the sign-flip test rejects at 5%. This is the same
    construction ``analyze_ab.py`` uses for its paired per-query interval.
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
            f"exact sign-flip DP convolution over {count} per-base theta values "
            f"(exactly equivalent to full 2^{count} = {total} enumeration; "
            f"deterministic, two-sided 95%)"
        ),
        "n": count,
        "mean": float(mean),
        "mean_exact": str(mean),
        "ci_low": float(mean - high * scale),
        "ci_high": float(mean - low * scale),
        "null_critical_low": float(low * scale),
        "null_critical_high": float(high * scale),
        "p_two_sided": float(Fraction(extreme, total)),
        "excludes_zero": bool((mean - high * scale) > 0 or (mean - low * scale) < 0),
    }


# ---------------------------------------------------------------- verdict


def support_level(theta_bar: Fraction | None, excludes_zero: bool) -> str:
    """The preregistration's three support levels, in its own words."""
    if theta_bar is None:
        return "NOT_SUPPORTED"
    if theta_bar > 0:
        return "CONFIRMED" if excludes_zero else "DIRECTIONAL"
    return "NOT_SUPPORTED"


# ---------------------------------------------------------------- extras


def sign_summary(thetas: list[Fraction]) -> dict[str, int]:
    return {
        "narrowed": sum(1 for theta in thetas if theta > 0),
        "unchanged": sum(1 for theta in thetas if theta == 0),
        "widened": sum(1 for theta in thetas if theta < 0),
    }


def speech_act_marginals(outcomes: Outcomes, bases: list[Base]) -> dict[str, dict]:
    """Pooled trigger rate per speech act under each description, plus delta."""
    report: dict[str, dict] = {}
    for act in SPEECH_ACTS:
        indices = sorted(base.indices[act] for base in bases)
        cells = {arm: pooled_rate(outcomes, indices, arm) for arm in DESC_ARMS}
        report[act] = {
            "queries": len(indices),
            "query_indices": indices,
            **{
                arm: {
                    "invocations": cells[arm].invocations,
                    "triggers": cells[arm].triggers,
                    "rate": as_float(cells[arm].rate),
                }
                for arm in DESC_ARMS
            },
            "delta": as_float(delta(cells["treatment"].rate, cells["baseline"].rate)),
        }
    return report


def scope_breakdown(outcomes: Outcomes, bases: list[Base]) -> dict[str, dict]:
    """theta_bar and both descriptions' mean gap, split by fixture scope."""
    report: dict[str, dict] = {}
    for scope in SCOPES:
        subset = [base for base in bases if base.scope == scope]
        gaps = {
            arm: [
                gap for base in subset if (gap := base_gap(outcomes, base, arm)["gap"]) is not None
            ]
            for arm in DESC_ARMS
        }
        thetas = []
        for base in subset:
            theta = delta(
                base_gap(outcomes, base, "baseline")["gap"],
                base_gap(outcomes, base, "treatment")["gap"],
            )
            if theta is not None:
                thetas.append(theta)
        theta_bar = mean_of(thetas)
        report[scope] = {
            "bases": len(subset),
            "base_ids": [base.base_id for base in subset],
            "mean_gap": {arm: as_float(mean_of(gaps[arm])) for arm in DESC_ARMS},
            "theta_bar": as_float(theta_bar),
            "signs": sign_summary(thetas),
        }
    return report


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


# ---------------------------------------------------------------- report


def print_validity(report: dict) -> None:
    print("== Validity and completeness ==")
    counts = report["validity"]
    print(
        f"  rows={counts['rows']}  valid={counts['valid']}  void={counts['void']}  "
        f"expected_runs={counts['expected_runs']}"
    )
    print("  base and scope membership: read from the fixture's own fields")
    print(
        f"    bases={report['base_count']}  "
        f"whole={report['scope_sizes']['whole']}  facet={report['scope_sizes']['facet']}"
    )
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


def print_estimand(report: dict) -> None:
    estimand = report["estimand"]
    interval = estimand["permutation"]
    print("== Preregistered estimand (Phase C) ==")
    print("  gap_i(D) = rate(profile) - mean(rate over overview, rundown, tell-me-about)")
    print("  theta_i  = gap_i(baseline) - gap_i(treatment)   [positive = treatment narrowed]")
    print(f"  bases: {estimand['n_bases']}")
    print(f"  theta_bar = {fmt(estimand['theta_bar'])}   (exact {estimand['theta_bar_exact']})")
    signs = estimand["signs"]
    print(
        f"  signs: narrowed={signs['narrowed']} unchanged={signs['unchanged']} "
        f"widened={signs['widened']}"
    )
    if interval.get("n"):
        print(f"  method: {interval['method']}")
        print(
            f"  two-sided 95% interval: [{interval['ci_low']:+.4f}, {interval['ci_high']:+.4f}]"
            f"   p={interval['p_two_sided']:.4f}   excludes 0: {interval['excludes_zero']}"
        )
    print()


def print_verdict(report: dict) -> None:
    estimand = report["estimand"]
    print("== Support level (preregistered) ==")
    print("  CONFIRMED     theta_bar > 0 and the interval excludes 0")
    print("  DIRECTIONAL   theta_bar > 0 otherwise")
    print("  NOT_SUPPORTED theta_bar <= 0")
    print(f"\nVERDICT: {report['verdict']}")
    print(f"REOPEN CONDITION (theta_bar < 0 AND interval excludes 0): {report['reopen_condition']}")
    print(f"  {report['reopen_note']}")
    print(f"  theta_bar={fmt(estimand['theta_bar'])}  excludes_zero={report['excludes_zero']}\n")


def print_per_base(report: dict) -> None:
    print("== Per-base rates, gaps, and theta (disclosure, not gating) ==")
    header = (
        f"  {'base':<4} {'slug':<26} {'scope':<6} {'desc':<10} "
        f"{'profile':>8} {'overvw':>8} {'rundown':>8} {'tell':>8} {'gap':>8}"
    )
    print(header)
    for base in report["per_base"]:
        for arm in DESC_ARMS:
            rates = base["rates"][arm]
            print(
                f"  {base['base_id']:<4} {base['base_slug']:<26} {base['scope']:<6} {arm:<10} "
                f"{fmt(rates['profile'], 3):>8} {fmt(rates['overview'], 3):>8} "
                f"{fmt(rates['rundown'], 3):>8} {fmt(rates['tell-me-about'], 3):>8} "
                f"{fmt(base['gap'][arm], 3):>8}"
            )
        print(f"  {'':<4} {'':<26} {'':<6} {'theta_i':<10} {fmt(base['theta']):>44}")
    print()


def print_marginals(report: dict) -> None:
    print("== Speech-act marginal rates (disclosure, not gating) ==")
    print(f"  {'speech act':<16} {'baseline':>10} {'treatment':>10} {'delta':>10}  n(invocations)")
    for act in SPEECH_ACTS:
        entry = report["speech_acts"][act]
        total = entry["baseline"]["invocations"] + entry["treatment"]["invocations"]
        print(
            f"  {act:<16} {fmt(entry['baseline']['rate']):>10} "
            f"{fmt(entry['treatment']['rate']):>10} {fmt(entry['delta']):>10}  {total:>14}"
        )
    print()


def print_scope(report: dict) -> None:
    print("== Scope breakdown (disclosure, not gating) ==")
    for scope in SCOPES:
        entry = report["scope"][scope]
        signs = entry["signs"]
        print(
            f"  {scope:<6} bases={entry['bases']}  "
            f"mean gap baseline={fmt(entry['mean_gap']['baseline'])} "
            f"treatment={fmt(entry['mean_gap']['treatment'])}  "
            f"theta_bar={fmt(entry['theta_bar'])}  "
            f"(narrowed={signs['narrowed']} unchanged={signs['unchanged']} "
            f"widened={signs['widened']})"
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


def print_report(report: dict) -> None:
    print_validity(report)
    print_estimand(report)
    print_verdict(report)
    print_per_base(report)
    print_marginals(report)
    print_scope(report)
    print_order(report["order"])


# ---------------------------------------------------------------- driver


REOPEN_NOTE = (
    "measurable half of the prereg's reopen rule; it reopens the ship decision "
    "only if Phase A shipped, which analyze_ab.py decides, not this script"
)


def build_report(args: argparse.Namespace) -> dict:
    rows = load_rows(args.results)
    fixture = load_fixture(args.fixture)
    bases = fixture_bases(fixture)

    fail(check_schema(rows))
    digests, digest_problems = check_digests(rows)
    fail(digest_problems)
    fail(check_fixture_match(rows, fixture))
    fail(check_completeness(rows, fixture, args.expected_runs))

    outcomes = build_outcomes(rows)
    per_base, thetas = base_thetas(outcomes, bases)
    theta_bar = mean_of(thetas)
    interval = permutation_interval(thetas)
    excludes_zero = bool(interval.get("excludes_zero", False))
    verdict = support_level(theta_bar, excludes_zero)
    reopen = bool(theta_bar is not None and theta_bar < 0 and excludes_zero)

    return {
        "results_file": str(args.results),
        "fixture_file": str(args.fixture),
        "expected_runs": args.expected_runs,
        "base_count": len(bases),
        "scope_sizes": {scope: sum(1 for base in bases if base.scope == scope) for scope in SCOPES},
        "digests": digests,
        "validity": {
            "rows": len(rows),
            "valid": sum(1 for row in rows if row["status"] == "valid"),
            "void": sum(1 for row in rows if row["status"] == "void"),
            "expected_runs": args.expected_runs,
        },
        "voids": collect_voids(rows),
        "estimand": {
            "n_bases": len(thetas),
            "theta_bar": as_float(theta_bar),
            "theta_bar_exact": None if theta_bar is None else str(theta_bar),
            "signs": sign_summary(thetas),
            "permutation": interval,
        },
        "verdict": verdict,
        "excludes_zero": excludes_zero,
        "reopen_condition": reopen,
        "reopen_note": REOPEN_NOTE,
        "per_base": per_base,
        "speech_acts": speech_act_marginals(outcomes, bases),
        "scope": scope_breakdown(outcomes, bases),
        "order": order_diagnostics(rows),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Preregistered Phase C analysis for the description veto fix."
    )
    parser.add_argument("--results", required=True, type=Path, help="results.jsonl to analyze")
    parser.add_argument(
        "--fixture",
        required=True,
        type=Path,
        help="Crossed-pairs fixture JSON (carries base_id, speech_act, scope)",
    )
    parser.add_argument("--expected-runs", type=int, default=3, help="Valid runs per (query, arm)")
    parser.add_argument("--json", action="store_true", help="Emit the full report as JSON")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        report = build_report(args)
    except CheckFailure as error:
        print(f"CHECK FAILED — no result is inspected.\n{error}", file=sys.stderr)
        return 2
    except (OSError, json.JSONDecodeError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print_report(report)
    return 0


if __name__ == "__main__":
    sys.exit(main())
