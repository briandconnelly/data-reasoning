#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Check a decision record's schema-scope contract, failing closed.

SCOPE: this is a machine encoding of the record's *shape and arithmetic*, not
its content. It verifies: no duplicate sections and no duplicated
route-required slot label within a section; every route-required section
and slot present and non-empty; Route/Verdict/provenance/Claim-class values
drawn from their closed sets; sensitivity-only provenance absent from the
Evidence and update block; a causal Claim class carrying a non-NONE
Identification basis and, when so, non-`none` Identification conditions; the
binary/two-action v1 scope (two ' vs '-separated actions, exactly two
consequence action rows and two state columns on every row -- records
outside it are rejected, not approximated); exactly one provenance mention
on each governed numeric slot (Loss ratio, Decision threshold, Prior odds,
Prior class swept, Loss range swept), and one or more on the voi Signal
model, with a licensed sentinel accepted only bare -- never annotated; a
sourced evidence row
(externally-sourced or estimated-from-data-in-hand) carrying a non-empty
source cell in an exactly-four-cell row; loss numbers parsing as positive
numbers or ranges and carrying belief-grade provenance under a robust
verdict, each field checked independently; a Recommended action naming one
of the two framed actions under `robust`/`dominated` and reading exactly
`returned to owner` under a sensitive verdict; a `dominated` verdict's four
belief slots reading exactly `none needed`, with no trailing annotation; the
voi signal-model/value-basis/verdict coupling and the quantity grammar for
Cost and Upper bound; and
(arithmetic gates) recomputation of the posterior-odds interval and, when a
numeric decision threshold is recorded or supplied by the stated loss ratio,
the ordered verdict rule decided over the swept prior class, the loss range,
and the product of the supported likelihood-ratio ranges jointly -- each
axis's flip, the joint robustness predicate, the crossover interval the
verdict's axis names, and the direction of a robust recommendation against
the Favored if true slot. Decision-boundary comparisons are exact (decimal
values are read as exact fractions, and a range is a point only when its
endpoints are equal); rounding tolerance applies only where a stated number
(posterior odds, a crossover) is compared with a computed one. Required
numeric fields that do not parse, or violate their domain (ordered ranges,
odds, LRs, and thresholds strictly positive), are gate failures -- never
skipped checks.

Explicitly NOT this checker's claim: whether the record preceded reasoning
(a transcript-level fact this file never sees), whether a likelihood ratio is
calibrated or its named source real, whether the state model is exhaustive,
whether the swept prior class or loss range is honest, whether a `dominated`
verdict's statewise-domination claim holds (structural presence only),
whether the voi Value calculation's prose arithmetic and bound derivation are
correct (voi numerics are not recomputed in v1), whether the route was the right one, or whether
any prose entry is semantically adequate. Passing this checker is
consistency, not validity.

The closed-set vocabulary and its semantics are governed by ../SKILL.md
(§ Routing, § Numeric Policy, § The Decide Route, § The VoI Route); this
checker enforces, it does not restate.

Exit codes:
  0  no gate failures
  1  one or more gate failures
  2  UNVERIFIABLE: the record file could not be read
"""

from __future__ import annotations

import re
import sys
from fractions import Fraction
from pathlib import Path

ROUTES = frozenset({"decide", "voi"})
DECIDE_VERDICTS = frozenset(
    {"robust", "prior-sensitive", "loss-sensitive", "evidence-sensitive", "dominated"}
)
VOI_VERDICTS = frozenset(
    {"worth-it", "not-worth-it", "sensitive", "break-even-only", "upper-bound-only"}
)
VOI_BASES = frozenset({"signal-model", "upper-bound"})
PROVENANCE = frozenset(
    {"user-elicited", "externally-sourced", "estimated-from-data-in-hand", "sensitivity-only"}
)
BELIEF_LOSS_PROVENANCE = frozenset({"user-elicited", "externally-sourced"})
# The no-supported-prior form (SKILL.md § Numeric Policy; spellings in the
# template's § Slot notes): Prior odds and Posterior odds carry NO_PRIOR
# together, and an unquantified evidence item carries NO_LR in both its LR
# and provenance cells with the reason in its source cell.
NO_PRIOR = "none supported — see Robustness"
NO_LR = "none supported"
# Authority: hypothesis-driven-analysis's ledger claim classes (its § Plan);
# SKILL.md § The Decide Route points at that authority by reference.
CLAIM_CLASSES = frozenset({"causal", "descriptive", "data-artifact"})

# Every top-level template bullet, by section; Task 5's parity test asserts
# set equality between these labels and the template's bullets.
DECIDE_LABELS: dict[str, tuple[str, ...]] = {
    "Decision frame": (
        "Route:",
        "Actions:",
        "Decision owner:",
        "Reversibility:",
        "Deadline or forcing event:",
        "Consequences:",
        "Favored if true:",
        "Loss ratio:",
        "Decision threshold (posterior odds):",
    ),
    "Decision-state model": (
        "Proposition:",
        "Residual reading:",
        "Claim class:",
        "Identification basis:",
        "Identification conditions:",
        "Ledger mapping:",
    ),
    "Evidence and update": ("Prior odds:", "Evidence:", "Independence:", "Posterior odds:"),
    "Robustness": ("Prior class swept:", "Loss range swept:", "Crossover:"),
    "Verdict": ("Verdict:", "Recommended action:", "Conditions:"),
    "Handoff": ("Open factual disputes:", "Identification gaps:", "VoI question:"),
}
VOI_LABELS: dict[str, tuple[str, ...]] = {
    "VoI": (
        "Route:",
        "Pending decision:",
        "Signal model:",
        "Value basis:",
        "Value calculation:",
        "Upper bound:",
        "Cost:",
        "Verdict:",
    ),
}

EXIT_OK = 0
EXIT_GATE_FAILURE = 1
EXIT_UNVERIFIABLE = 2

# v1 binary/two-action scope constants (see module docstring).
_SCOPE_ACTIONS = 2
_SCOPE_ACTION_ROWS = 2
_SCOPE_TABLE_COLUMNS = 3
_EVIDENCE_ROW_CELLS = 4

_SECTION = re.compile(r"^## (.+?)\s*$", re.MULTILINE)
_PROVENANCE_MENTION = re.compile(r"provenance:\s*`?([a-z-]+)`?")
_RANGE = re.compile(r"^\s*(\d+(?:\.\d+)?)\s*(?:[–-]\s*(\d+(?:\.\d+)?))?\s*$")  # noqa: RUF001
_QUANTITY = re.compile(r"^\s*(\d+(?:\.\d+)?)\s+([A-Za-z][A-Za-z0-9 _/-]*)\s*$")
_SEPARATOR_CELL = re.compile(r"^:?-+:?$")
_REL_TOLERANCE = 0.01


def parse_sections(text: str) -> tuple[dict[str, str], list[str]]:
    """Map each ``## Section`` heading to its body; also return duplicates."""
    sections: dict[str, str] = {}
    duplicates: list[str] = []
    matches = list(_SECTION.finditer(text))
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        name = m.group(1)
        if name in sections:
            # Last body wins in the dict; the duplicate is still recorded and
            # `check()` rejects the record for it, so the overwrite here never
            # lets a duplicated section slip through unnoticed.
            duplicates.append(name)
        sections[name] = text[m.end() : end]
    return sections, duplicates


def field(section_text: str, label: str) -> str | None:
    """Return the value of ``- <label> <value>`` in a section, else None."""
    for line in section_text.splitlines():
        stripped = line.strip()
        if stripped.startswith(f"- {label}"):
            return stripped[len(f"- {label}") :].strip()
    return None


def _voi_prose(section_text: str, label: str) -> str | None:
    """Read a VoI prose slot through its continuation paragraphs.

    Stop at any following bullet or heading, including an unrecognized label,
    so a neighboring slot cannot supply missing content or provenance.
    """
    value: list[str] | None = None
    for line in section_text.splitlines():
        stripped = line.strip()
        if value is not None:
            if stripped.startswith(("- ", "#")):
                break
            value.append(line)
        elif stripped.startswith(f"- {label}"):
            value = [stripped[len(f"- {label}") :].strip()]
    return "\n".join(value).strip() if value is not None else None


def parse_range(value: str) -> tuple[float, float] | None:
    """Parse ``3`` or ``0.25-1.0`` (en dash or hyphen) into an ordered (low, high)."""
    m = _RANGE.match(value)
    if not m:
        return None
    low = float(m.group(1))
    high = float(m.group(2)) if m.group(2) else low
    if low > high:
        return None
    return (low, high)


Interval = tuple[Fraction, Fraction]


def parse_exact(value: str) -> Interval | None:
    """`parse_range`, read exactly: each decimal becomes a Fraction, so a
    decision-boundary comparison is never decided by binary rounding."""
    m = _RANGE.match(value)
    if not m:
        return None
    low = Fraction(m.group(1))
    high = Fraction(m.group(2)) if m.group(2) else low
    if low > high:
        return None
    return (low, high)


def _meets(a: Interval, b: Interval) -> bool:
    """Closed intervals share a point; touching endpoints count (a tie is a flip)."""
    return a[0] <= b[1] and b[0] <= a[1]


def _is_point(r: Interval) -> bool:
    return r[0] == r[1]


Losses = dict[str, tuple[Fraction, Fraction]]


def orient(losses: Losses) -> tuple[str, str, Fraction | None]:
    """SKILL.md § Numeric Policy's orientation, executable.

    `losses` maps each of the two actions to its (loss if H, loss if not-H).
    Returns ``("dominated", winner, None)`` when one action's loss is no
    higher than the other's in both states (ties included; r is never
    computed), else ``(favored, other, r)``: favored has the lower loss when
    H is true, and r = [L(other,H) - L(favored,H)] / [L(favored,not-H) -
    L(other,not-H)], both differences positive.
    """
    (a, (a_h, a_n)), (b, (b_h, b_n)) = sorted(losses.items())
    if a_h <= b_h and a_n <= b_n:
        return ("dominated", a, None)
    if b_h <= a_h and b_n <= a_n:
        return ("dominated", b, None)
    favored, other = (a, b) if a_h < b_h else (b, a)
    f_h, f_n = losses[favored]
    o_h, o_n = losses[other]
    return (favored, other, (o_h - f_h) / (f_n - o_n))


def preferred_action(losses: Losses, posterior_odds: Fraction) -> str | None:
    """The action with the lower expected loss at these posterior odds of H,
    or None at an exact tie. The favored action wins above 1/r."""
    kind, winner, r = orient(losses)
    if kind == "dominated":
        return winner
    assert r is not None
    other = next(a for a in losses if a != kind)
    if posterior_odds > 1 / r:
        return kind
    if posterior_odds < 1 / r:
        return other
    return None


def parse_quantity(value: str) -> tuple[float, str] | None:
    """Parse a nonnegative decimal followed by its machine-comparable unit."""
    m = _QUANTITY.match(value)
    if not m:
        return None
    return float(m.group(1)), " ".join(m.group(2).lower().split())


def _bare(value: str) -> str:
    """Strip a trailing '— provenance: ...' annotation from a slot value."""
    return value.split("—", maxsplit=1)[0].strip()


def _close(a: float, b: float) -> bool:
    return abs(a - b) <= _REL_TOLERANCE * max(abs(a), abs(b), 1e-12)


# A cell boundary is an unescaped pipe; `\|` inside a cell (a conditional
# probability such as P(gap | real)) is content, not a column. Found by the
# 2026-09-15 remediation wave: three archived records parsed as six-cell
# evidence rows because of it (row 2 of that wave's preregistration).
_CELL_SPLIT = re.compile(r"(?<!\\)\|")


# A stated crossover is a bare number or ordered range, optionally introduced
# by one of these phrases and nothing else: "flips at prior odds 0.025",
# "prior odds 0.02-0.03", "0.025". Signs, reversed ranges, and prose around
# the number are not a crossover statement.
_CROSSOVER_PREFIX = re.compile(
    r"^(?:flips at\s+)?(?:prior odds\s+|loss ratio\s+|likelihood ratio\s+)?", re.I
)
_CROSSOVER_AXIS = re.compile(r"^(?:flips at\s+)?(prior odds|loss ratio|likelihood ratio)\b", re.I)


def _crossover_axis(text: str) -> str | None:
    """The quantity a stated crossover names -- `prior odds`, `loss ratio`,
    or `likelihood ratio` -- or None when it names none of them."""
    m = _CROSSOVER_AXIS.match(text.strip())
    return m.group(1).lower() if m else None


def _rounding_tolerances(text: str) -> tuple[float, float]:
    """Half a unit in the last decimal place of the first and of the last
    number in `text` (the stated low and high endpoints); (0, 0) when it
    carries no number."""
    places = [len(m.group(1)) if m.group(1) else 0 for m in re.finditer(r"\d+(?:\.(\d+))?", text)]
    if not places:
        return (0.0, 0.0)
    return (0.5 * 10 ** (-places[0]), 0.5 * 10 ** (-places[-1]))


def _crossover_value(text: str) -> tuple[float, float] | None:
    body = _CROSSOVER_PREFIX.sub("", text.strip(), count=1)
    if not body or body[0] in "-+":
        return None
    parsed = parse_range(body)
    if parsed is None or parsed[0] <= 0:
        return None
    return parsed


def _table_rows(section_text: str) -> list[list[str]]:
    """All pipe-table rows in a section, as cell lists (outer pipes stripped)."""
    rows = []
    for line in section_text.splitlines():
        stripped = line.strip()
        if stripped.startswith("|") and stripped.endswith("|"):
            rows.append([c.strip().replace("\\|", "|") for c in _CELL_SPLIT.split(stripped[1:-1])])
    return rows


def _data_rows(rows: list[list[str]]) -> list[list[str]]:
    """Table rows minus the first (header) row and any separator rows."""
    body = rows[1:] if rows else []
    return [r for r in body if not all(_SEPARATOR_CELL.match(c) for c in r if c)]


def _require_slots(
    sections: dict[str, str], labels: dict[str, tuple[str, ...]], failures: list[str]
) -> None:
    for section_name, section_labels in labels.items():
        body = sections.get(section_name)
        if body is None:
            failures.append(f"record is missing required section '## {section_name}'")
            continue
        for label in section_labels:
            count = sum(1 for line in body.splitlines() if line.strip().startswith(f"- {label}"))
            if count > 1:
                failures.append(
                    f"slot '- {label}' appears {count} times in '{section_name}'; "
                    "each label must appear exactly once"
                )
            value = (
                _voi_prose(body, label)
                if section_name == "VoI" and label in ("Signal model:", "Value calculation:")
                else field(body, label)
            )
            if value is None:
                failures.append(f"section '{section_name}' is missing required slot '- {label}'")
            elif not value and label not in ("Consequences:", "Evidence:"):
                failures.append(f"slot '- {label}' in '{section_name}' is empty")


def check(text: str) -> list[str]:
    failures: list[str] = []
    sections, duplicates = parse_sections(text)
    for name in duplicates:
        failures.append(f"duplicate section '## {name}'")

    route = None
    for body in sections.values():
        value = field(body, "Route:")
        if value:
            route = _bare(value)
            break
    if route not in ROUTES:
        failures.append(f"Route value {route!r} is not in the closed set {sorted(ROUTES)}")
        return failures

    for value in _PROVENANCE_MENTION.findall(text):
        if value not in PROVENANCE:
            failures.append(
                f"provenance value {value!r} is not in the closed set {sorted(PROVENANCE)}"
            )

    if route == "decide":
        _require_slots(sections, DECIDE_LABELS, failures)
        if not any(f.startswith("record is missing") for f in failures):
            failures.extend(_check_decide(sections))
    else:
        _require_slots(sections, VOI_LABELS, failures)
        if "VoI" in sections:
            failures.extend(_check_voi(sections))
    return failures


def _check_slot_provenance(
    slots: tuple[tuple[str, str], ...], sentinel: str | tuple[str, ...] | None = None
) -> list[str]:
    """Require exactly one provenance mention on each ``(label, value)`` slot.

    ``sentinel`` (e.g. ``"none stated"``, ``"none needed"``, or a tuple of
    such values) is a bare value that is exempt from carrying a provenance
    class. ``None`` means every slot in ``slots`` always requires exactly one
    provenance class.
    """
    sentinels = (sentinel,) if isinstance(sentinel, str) else (sentinel or ())
    failures: list[str] = []
    for label, value in slots:
        # A sentinel may itself contain an em dash, so the whole stripped value
        # is tried first and the bare value second.
        hit = next((x for x in sentinels if value.strip() == x or _bare(value) == x), None)
        if hit is not None:
            if value.strip() != hit:
                failures.append(
                    f"slot '- {label}' sentinel {hit!r} must appear bare, "
                    "with no trailing annotation"
                )
            continue
        provs = _PROVENANCE_MENTION.findall(value)
        if len(provs) != 1:
            failures.append(f"slot '- {label}' must carry exactly one provenance class")
    return failures


def _check_decide(sections: dict[str, str]) -> list[str]:
    failures: list[str] = []
    frame = sections["Decision frame"]

    actions = _bare(field(frame, "Actions:") or "")
    failures.extend(_check_frame_scope(frame, actions))

    failures.extend(
        _check_slot_provenance(
            tuple(
                (label, field(frame, label) or "")
                for label in ("Loss ratio:", "Decision threshold (posterior odds):")
            ),
            "none stated",
        )
    )
    failures.extend(
        _check_slot_provenance(
            (("Prior odds:", field(sections["Evidence and update"], "Prior odds:") or ""),),
            ("none needed", NO_PRIOR),
        )
    )
    failures.extend(
        _check_slot_provenance(
            (
                (
                    "Prior class swept:",
                    field(sections["Robustness"], "Prior class swept:") or "",
                ),
            ),
            "none needed",
        )
    )
    failures.extend(
        _check_slot_provenance(
            (("Loss range swept:", field(sections["Robustness"], "Loss range swept:") or ""),)
        )
    )

    model = sections["Decision-state model"]
    claim = _bare(field(model, "Claim class:") or "")
    basis = _bare(field(model, "Identification basis:") or "")
    if claim not in CLAIM_CLASSES:
        failures.append(
            f"Claim class value {claim!r} is not in the closed set {sorted(CLAIM_CLASSES)}"
        )
    if claim == "causal" and (not basis or basis.upper() == "NONE"):
        failures.append(
            "Claim class 'causal' requires a non-NONE Identification basis "
            "(HDA's causal-wording bar or a CIR identified-if, by pointer)"
        )
    if claim == "causal" and basis and basis.upper() != "NONE":
        conditions = _bare(field(model, "Identification conditions:") or "")
        if conditions.lower() == "none":
            failures.append(
                "Claim class 'causal' with a non-NONE Identification basis requires "
                "'- Identification conditions:' to restate the identifying assumptions, "
                "not 'none'"
            )

    evidence = sections["Evidence and update"]
    if "sensitivity-only" in evidence:
        failures.append(
            "sensitivity-only provenance may not appear in Evidence and update; "
            "it belongs in Robustness"
        )

    verdict = _bare(field(sections["Verdict"], "Verdict:") or "")
    if verdict not in DECIDE_VERDICTS:
        failures.append(
            f"Verdict value {verdict!r} is not in the closed set {sorted(DECIDE_VERDICTS)}"
        )
    else:
        failures.extend(_check_recommended_action(sections, verdict, actions))
        failures.extend(_check_favored(frame, verdict, actions))
    belief_losses = _belief_grade_losses(sections)
    if verdict in ("robust", "prior-sensitive", "evidence-sensitive") and not belief_losses:
        failures.append(
            f"a {verdict} verdict requires '- Loss ratio:' and '- Loss range swept:' to each "
            "carry exactly one user-elicited or externally-sourced provenance; any other class "
            "caps the verdict at loss-sensitive (SKILL.md § Numeric Policy)"
        )

    failures.extend(_check_decide_arithmetic(sections, verdict, belief_losses))
    return failures


def _belief_grade_losses(sections: dict[str, str]) -> bool:
    """True when both loss slots carry exactly one belief-grade class."""
    for section_name, label in (
        ("Decision frame", "Loss ratio:"),
        ("Robustness", "Loss range swept:"),
    ):
        provs = _PROVENANCE_MENTION.findall(field(sections[section_name], label) or "")
        if len(provs) != 1 or provs[0] not in BELIEF_LOSS_PROVENANCE:
            return False
    return True


def _action_names(actions: str) -> list[str]:
    return [a.strip() for a in re.split(r"\s+vs\s+", actions)]


def _check_favored(frame: str, verdict: str, actions: str) -> list[str]:
    """Favored if true names a framed action, bare -- or, under `dominated`
    only, reads exactly `none needed` (SKILL.md § Numeric Policy)."""
    favored = (field(frame, "Favored if true:") or "").strip()
    names = _action_names(actions)
    if verdict == "dominated":
        if favored != "none needed":
            return [
                "a dominated verdict requires '- Favored if true:' to read exactly "
                f"'none needed', with no annotation; found {favored!r}"
            ]
        return []
    if favored not in names:
        return [
            f"'- Favored if true:' must name one of the framed actions {names!r} exactly "
            f"(or read 'none needed' under a dominated verdict); found {favored!r}"
        ]
    return []


def _check_frame_scope(frame: str, actions: str) -> list[str]:
    """Enforce the v1 binary scope on the Actions slot and Consequences table."""
    failures: list[str] = []
    if len(re.split(r"\s+vs\s+", actions)) != _SCOPE_ACTIONS:
        failures.append("Actions must name exactly two actions separated by ' vs ' (v1 scope)")
    rows = _table_rows(frame)
    data = _data_rows(rows)
    if len(data) != _SCOPE_ACTION_ROWS:
        failures.append(f"Consequences table must have exactly two action rows; found {len(data)}")
    for row in rows:
        if len(row) != _SCOPE_TABLE_COLUMNS:
            failures.append(
                f"Consequences table rows must have exactly two state columns; "
                f"found a row with {len(row) - 1}"
            )
    return failures


def _check_recommended_action(sections: dict[str, str], verdict: str, actions: str) -> list[str]:
    """Require the Recommended action to point at a framed action or the owner."""
    failures: list[str] = []
    recommended = (field(sections["Verdict"], "Recommended action:") or "").strip()
    action_names = [a.strip() for a in re.split(r"\s+vs\s+", actions)]
    if verdict in ("robust", "dominated"):
        if recommended not in action_names:
            failures.append(
                f"a {verdict} verdict requires '- Recommended action:' to name one of "
                f"the framed actions {action_names!r}; found {recommended!r}"
            )
    elif recommended != "returned to owner":
        failures.append(
            f"a {verdict} verdict requires '- Recommended action:' to read exactly "
            f"'returned to owner'; found {recommended!r}"
        )
    return failures


def _check_decide_arithmetic(  # noqa: PLR0912, PLR0915 -- one gate pass over five slots
    sections: dict[str, str], verdict: str, belief_losses: bool = True
) -> list[str]:
    failures: list[str] = []
    if verdict == "dominated":
        # Statewise domination needs no probabilities (SKILL.md § The Decide
        # Route): Prior odds, Posterior odds, Prior class swept, and
        # Crossover carry no belief-grade numbers to recompute or sweep, so
        # none of the numeric parsing, recomputation, or crossover gates
        # below apply to this record -- but the sentinel itself is required,
        # not optional, on each of those four slots.
        evidence = sections["Evidence and update"]
        robustness = sections["Robustness"]
        for section, label in (
            (evidence, "Prior odds:"),
            (evidence, "Posterior odds:"),
            (robustness, "Prior class swept:"),
            (robustness, "Crossover:"),
        ):
            value = (field(section, label) or "").strip()
            if value != "none needed":
                failures.append(
                    f"a dominated verdict requires '- {label}' to read exactly "
                    f"'none needed', with no annotation; found {value!r}"
                )
        return failures
    evidence = sections["Evidence and update"]
    robustness = sections["Robustness"]
    frame = sections["Decision frame"]

    prior_value = (field(evidence, "Prior odds:") or "").strip()
    posterior_raw = (field(evidence, "Posterior odds:") or "").strip()
    no_prior = prior_value == NO_PRIOR
    prior: tuple[float, float] | None = None
    if not no_prior and prior_value.startswith(NO_PRIOR):
        failures.append(f"Prior odds sentinel {NO_PRIOR!r} must appear bare, with no annotation")
        no_prior = True
    if no_prior:
        if posterior_raw != NO_PRIOR:
            failures.append(
                f"Prior odds reads {NO_PRIOR!r}, so Posterior odds must read the same sentinel, "
                f"bare; found {posterior_raw!r}"
            )
    else:
        prior = parse_range(_bare(prior_value))
        if prior is None or prior[0] <= 0:
            failures.append("Prior odds must parse as a positive number or ordered range")

    lr_product: tuple[float, float] | None = (1.0, 1.0)
    lr_exact: Interval | None = (Fraction(1), Fraction(1))
    lr_ranged = False  # some supported row states its ratio as a range
    supported_rows = 0
    data = _data_rows(_table_rows(evidence))
    if not data:
        failures.append("Evidence table must have at least one data row")
        lr_product = None
    for row in data:
        if len(row) != _EVIDENCE_ROW_CELLS:
            failures.append(f"Evidence row has {len(row)} cells; the template requires exactly 4")
            lr_product = None
            continue
        if row[1].strip() == NO_LR or row[2].strip() == NO_LR:
            if not (row[1].strip() == NO_LR and row[2].strip() == NO_LR):
                failures.append(
                    f"Evidence row {row[0]!r}: {NO_LR!r} must fill both the LR and the "
                    "provenance cell together"
                )
            if not row[3].strip():
                failures.append(
                    f"Evidence row {row[0]!r}: an unquantified item needs its reason in the "
                    "source cell"
                )
            continue
        supported_rows += 1
        lr = parse_range(row[1])
        if lr is None or lr[0] <= 0:
            failures.append(f"Evidence LR {row[1]!r} must parse as a positive ratio or range")
            lr_product = None
        elif lr_product is not None:
            lr_product = (lr_product[0] * lr[0], lr_product[1] * lr[1])
            exact = parse_exact(row[1])
            if exact is not None and lr_exact is not None:
                lr_exact = (lr_exact[0] * exact[0], lr_exact[1] * exact[1])
                lr_ranged = lr_ranged or not _is_point(exact)
        if row[2] not in PROVENANCE:
            failures.append(f"Evidence provenance cell {row[2]!r} is not a provenance class")
        if row[2] in ("externally-sourced", "estimated-from-data-in-hand") and not row[3]:
            failures.append(
                f"Evidence row {row[0]!r} has provenance {row[2]!r} but an empty source, "
                "reference class, conditioning cell"
            )

    if data and supported_rows == 0 and lr_product is not None:
        lr_product = None
        if verdict == "robust":
            failures.append(
                "no supported likelihood ratio remains, so no quantitative update is supported "
                "and hypothetical inputs alone cannot reach robust (SKILL.md § Numeric Policy)"
            )
    if lr_product is None:
        lr_exact = None
    if verdict == "evidence-sensitive" and not lr_ranged:
        failures.append(
            "an evidence-sensitive verdict requires a supported likelihood ratio stated as a "
            "range in the Evidence table; no supported row states one, so no likelihood-ratio "
            "range can flip the action (SKILL.md § Numeric Policy)"
        )

    posterior_value = _bare(posterior_raw)
    posterior = None
    if not no_prior:
        posterior = parse_range(posterior_value)
        if posterior is None:
            failures.append("Posterior odds must parse as a number or ordered range")

    if prior and posterior and lr_product:
        low = prior[0] * lr_product[0]
        high = prior[1] * lr_product[1]
        if not (_close(low, posterior[0]) and _close(high, posterior[1])):
            failures.append(
                f"Posterior odds {posterior_value!r} do not recompute from the recorded "
                f"prior and LR lines (expected {low:g}-{high:g})"
            )

    swept = parse_range(_bare(field(robustness, "Prior class swept:") or ""))
    if swept is None:
        failures.append("Prior class swept must parse as a number or ordered range")

    for section_name, label, sentinel in (
        ("Decision frame", "Loss ratio:", "none stated"),
        ("Robustness", "Loss range swept:", None),
    ):
        value = _bare(field(sections[section_name], label) or "")
        if sentinel is not None and value == sentinel:
            continue
        loss_range = parse_range(value)
        if loss_range is None or loss_range[0] <= 0:
            failures.append(
                f"'- {label}' must parse as a positive number or ordered range; found {value!r}"
            )

    crossover_text = (field(robustness, "Crossover:") or "").strip()
    threshold_value = _bare(field(frame, "Decision threshold (posterior odds):") or "")
    threshold = None if threshold_value == "none stated" else parse_exact(threshold_value)
    if threshold_value != "none stated":
        if threshold is None:
            failures.append("Decision threshold must be 'none stated' or parse as a number")
        elif threshold[0] <= 0:
            failures.append("Decision threshold odds must be strictly positive")
            threshold = None

    loss_swept = parse_exact(_bare(field(robustness, "Loss range swept:") or ""))
    if loss_swept is not None and loss_swept[0] <= 0:
        loss_swept = None
    loss_stated_value = _bare(field(frame, "Loss ratio:") or "")
    loss_stated = None if loss_stated_value == "none stated" else parse_exact(loss_stated_value)
    if threshold is None and loss_stated and loss_stated[0] > 0:
        # No threshold stated: the stated loss ratio supplies it (SKILL.md
        # § Numeric Policy), so a robust claim is never unverifiable merely
        # because the threshold slot reads 'none stated'.
        threshold = (1 / loss_stated[1], 1 / loss_stated[0])

    swept_x = parse_exact(_bare(field(robustness, "Prior class swept:") or ""))
    prior_x = parse_exact(_bare(prior_value)) if prior and not no_prior else None
    if swept_x is not None and swept_x[0] <= 0:
        swept_x = None

    if threshold and lr_exact and swept_x:
        failures.extend(
            _check_ordered_rule(
                sections,
                verdict=verdict,
                belief_losses=belief_losses,
                crossover_text=crossover_text,
                threshold=threshold,
                lr=lr_exact,
                swept=swept_x,
                prior=prior_x,
                loss_swept=loss_swept,
            )
        )
    else:
        if verdict == "robust" and crossover_text != "none within swept class":
            failures.append(
                "a robust verdict requires Crossover 'none within swept class'; "
                f"found {crossover_text!r}"
            )
        if verdict in _SENSITIVE_AXIS:
            expected = _SENSITIVE_AXIS[verdict]
            axis = _crossover_axis(crossover_text)
            if axis is not None and axis != expected:
                failures.append(
                    f"a {verdict} verdict's Crossover names {expected}; found {crossover_text!r}"
                )
            numbers = re.findall(r"\d+(?:\.\d+)?", crossover_text)
            if crossover_text.lower().startswith("none") or not numbers or float(numbers[0]) <= 0:
                failures.append(
                    f"a {verdict} verdict requires a Crossover naming a positive flip "
                    f"point; found {crossover_text!r}"
                )
    return failures


# The quantity each sensitive verdict's Crossover reports (SKILL.md § Numeric
# Policy's ordered rule).
_SENSITIVE_AXIS = {
    "prior-sensitive": "prior odds",
    "loss-sensitive": "loss ratio",
    "evidence-sensitive": "likelihood ratio",
}


def _fmt(interval: Interval) -> str:
    return f"[{float(interval[0]):g}, {float(interval[1]):g}]"


def _check_ordered_rule(  # noqa: PLR0912, PLR0913, PLR0915 -- one pass over the ordered rule
    sections: dict[str, str],
    *,
    verdict: str,
    belief_losses: bool,
    crossover_text: str,
    threshold: Interval,
    lr: Interval,
    swept: Interval,
    prior: Interval | None,
    loss_swept: Interval | None,
) -> list[str]:
    """SKILL.md § Numeric Policy's ordered verdict rule, decided exactly.

    The threshold interval spans the stated (or loss-supplied) threshold and
    1 / L for every swept loss L. The joint posterior range is the swept prior
    class times the product of the supported likelihood-ratio ranges. Each
    axis flips the action when it is a genuine range (endpoints differ) and,
    with the other inputs held somewhere in their own ranges, moving it
    across its range reaches the threshold -- a tie counts:

    - prior: the joint posterior range meets the threshold interval;
    - loss: at the stated prior (the swept class standing in when no prior
      is supported), posterior odds meet 1 / L for some swept L;
    - likelihood ratio: the joint posterior range meets the threshold interval.

    A record whose joint range meets the threshold although no axis is a
    genuine range (an exact tie at points, or a stated threshold range
    straddling alone) takes prior-sensitive, the first sensitive clause.
    """
    failures: list[str] = []
    thr_lo, thr_hi = threshold
    if loss_swept:
        thr_lo = min(thr_lo, 1 / loss_swept[1])
        thr_hi = max(thr_hi, 1 / loss_swept[0])
    thr = (thr_lo, thr_hi)
    joint = (swept[0] * lr[0], swept[1] * lr[1])
    straddle = _meets(joint, thr)
    # Prior odds at which posterior odds meet the threshold, and the LR
    # product at which the swept prior's posterior meets it.
    pf = (thr_lo / lr[1], thr_hi / lr[0])
    ef = (thr_lo / swept[1], thr_hi / swept[0])
    prior_flip = straddle and not _is_point(swept)
    lr_flip = straddle and not _is_point(lr)
    stated_prior = prior or swept
    lf: Interval | None = None
    loss_flip = False
    if loss_swept:
        lf = (1 / (stated_prior[1] * lr[1]), 1 / (stated_prior[0] * lr[0]))
        loss_flip = not _is_point(loss_swept) and _meets(lf, loss_swept)
    residual = straddle and not (prior_flip or lr_flip or loss_flip)
    prior_clause = prior_flip or residual

    stated = _crossover_value(crossover_text)
    round_lo, round_hi = _rounding_tolerances(crossover_text)
    axis = _crossover_axis(crossover_text)

    def _within(interval: Interval) -> bool:
        """Each stated endpoint lies in the computed interval widened by
        the larger of the relative tolerance and half a unit in that
        endpoint's own last decimal place."""
        if stated is None:
            return False
        lo_c, hi_c = float(interval[0]), float(interval[1])
        for value, rounding in ((stated[0], round_lo), (stated[1], round_hi)):
            lo = min(lo_c * (1 - _REL_TOLERANCE), lo_c - rounding)
            hi = max(hi_c * (1 + _REL_TOLERANCE), hi_c + rounding)
            if not (lo <= value <= hi):
                return False
        return True

    def _axis_matches(expected: str) -> bool:
        return axis is None or axis == expected

    if verdict == "robust":
        if prior_flip:
            failures.append(
                f"robust verdict, but the computed prior-odds crossover {_fmt(pf)} lies "
                "inside the swept prior class (over the stated losses, the swept loss range, "
                "and the supported likelihood-ratio ranges)"
            )
        if loss_flip and lf is not None:
            failures.append(
                f"robust verdict, but the computed loss-ratio crossover {_fmt(lf)} "
                "lies inside the swept loss range"
            )
        if lr_flip and not prior_flip:
            failures.append(
                f"robust verdict, but the supported likelihood-ratio range flips the action: "
                f"joint posterior odds {_fmt(joint)} meet the threshold {_fmt(thr)}; "
                "the ordered rule gives evidence-sensitive (SKILL.md § Numeric Policy)"
            )
        if residual:
            failures.append(
                f"robust verdict, but joint posterior odds {_fmt(joint)} meet the threshold "
                f"{_fmt(thr)} with no range flipping the action on its own (an exact tie, or a "
                "stated threshold range); the ordered rule gives prior-sensitive "
                "(SKILL.md § Numeric Policy)"
            )
        # § Robustness asks for the crossover statement, so a robust record
        # may name the flip point outside the swept class -- every number
        # it states must lie in the computed interval -- or carry the
        # sentinel.
        if crossover_text != "none within swept class":
            if not _axis_matches("prior odds"):
                failures.append(
                    "a robust verdict's stated Crossover names prior odds; "
                    f"found {crossover_text!r}"
                )
            elif not _within(pf):
                failures.append(
                    "a robust verdict requires Crossover 'none within swept class' or the "
                    f"flip point outside the swept class (computed {_fmt(pf)}); "
                    f"found {crossover_text!r}"
                )
        if not (straddle or loss_flip):
            failures.extend(_check_robust_direction(sections, joint, thr))
    elif verdict == "prior-sensitive":
        if not prior_clause:
            failures.append(
                f"prior-sensitive verdict, but the computed prior-odds crossover {_fmt(pf)} "
                "does not intersect the swept prior class"
            )
        elif not _axis_matches("prior odds"):
            failures.append(
                f"a prior-sensitive verdict's Crossover names prior odds; found {crossover_text!r}"
            )
        elif not _within(pf):
            failures.append(
                f"prior-sensitive crossover {crossover_text!r} does not fall in the "
                f"computed prior-odds interval {_fmt(pf)}"
            )
    elif verdict == "loss-sensitive" and belief_losses:
        if prior_clause:
            failures.append(
                "loss-sensitive verdict, but varying the prior flips the action "
                f"(computed {_fmt(pf)} meets the swept class); "
                "the ordered rule gives prior-sensitive (SKILL.md § Numeric Policy)"
            )
        elif not _axis_matches("loss ratio"):
            failures.append(
                f"a loss-sensitive verdict's Crossover names a loss ratio; found {crossover_text!r}"
            )
        elif lf is None or not loss_flip:
            failures.append(
                "loss-sensitive verdict, but the computed loss-ratio crossover "
                + (f"{_fmt(lf)} " if lf else "")
                + "does not intersect the swept loss range"
            )
        elif not _within(lf):
            failures.append(
                f"loss-sensitive crossover {crossover_text!r} does not fall in the "
                f"computed loss-ratio interval {_fmt(lf)}"
            )
    elif verdict == "loss-sensitive":
        if not _axis_matches("loss ratio"):
            failures.append(
                f"a loss-sensitive verdict's Crossover names a loss ratio; found {crossover_text!r}"
            )
        numbers = re.findall(r"\d+(?:\.\d+)?", crossover_text)
        if crossover_text.lower().startswith("none") or not numbers or float(numbers[0]) <= 0:
            failures.append(
                "a loss-sensitive verdict requires a Crossover naming a positive flip "
                f"point; found {crossover_text!r}"
            )
    elif verdict == "evidence-sensitive":
        if prior_clause:
            failures.append(
                "evidence-sensitive verdict, but varying the prior flips the action "
                f"(computed {_fmt(pf)} meets the swept class); "
                "the ordered rule gives prior-sensitive (SKILL.md § Numeric Policy)"
            )
        elif loss_flip:
            failures.append(
                "evidence-sensitive verdict, but varying the losses flips the action "
                f"(computed {_fmt(lf) if lf else ''} meets the swept loss range); "
                "the ordered rule gives loss-sensitive (SKILL.md § Numeric Policy)"
            )
        elif not lr_flip:
            failures.append(
                f"evidence-sensitive verdict, but joint posterior odds {_fmt(joint)} do not "
                f"meet the threshold {_fmt(thr)}: no supported likelihood-ratio range flips "
                "the action"
            )
        elif not _axis_matches("likelihood ratio"):
            failures.append(
                "an evidence-sensitive verdict's Crossover names a likelihood ratio; "
                f"found {crossover_text!r}"
            )
        elif not _within(ef):
            failures.append(
                f"evidence-sensitive crossover {crossover_text!r} does not fall in the "
                f"computed likelihood-ratio interval {_fmt(ef)}"
            )
    return failures


def _check_robust_direction(
    sections: dict[str, str], joint: Interval, threshold: Interval
) -> list[str]:
    """A robust record recommends the Favored if true action when posterior
    odds lie above the threshold, and the other action when they lie below
    (SKILL.md § Numeric Policy)."""
    actions = _action_names(_bare(field(sections["Decision frame"], "Actions:") or ""))
    favored = (field(sections["Decision frame"], "Favored if true:") or "").strip()
    recommended = (field(sections["Verdict"], "Recommended action:") or "").strip()
    if favored not in actions or recommended not in actions or len(actions) != _SCOPE_ACTIONS:
        return []  # each is its own finding already
    other = next(a for a in actions if a != favored)
    expected, side = (favored, "above") if joint[0] > threshold[1] else (other, "below")
    if recommended != expected:
        return [
            f"robust verdict recommends {recommended!r}, but posterior odds {_fmt(joint)} lie "
            f"{side} the threshold {_fmt(threshold)}, where the preferred action is "
            f"{expected!r} (Favored if true: {favored!r}; SKILL.md § Numeric Policy)"
        ]
    return []


def _check_voi_signal_model(signal: str, basis: str, failures: list[str]) -> None:
    """Apply the signal model's sentinel, provenance, and basis coupling."""
    if _bare(signal) == "unavailable":
        if signal.strip() != "unavailable":
            failures.append(
                "Signal model sentinel 'unavailable' must appear bare, with no annotation"
            )
    elif not _PROVENANCE_MENTION.findall(signal):
        failures.append("slot '- Signal model:' must carry one or more provenance classes")
    if ("sensitivity-only" in signal or _bare(signal) == "unavailable") and basis != "upper-bound":
        failures.append("an unavailable or sensitivity-only Signal model requires upper-bound")


def _check_voi_upper_bound(
    basis: str, bound: str, cost: str, verdict: str, failures: list[str]
) -> None:
    """Validate the bound's basis-specific sentinel and a no-buy comparison."""
    if basis == "signal-model":
        if bound != "not applicable":
            failures.append("signal-model Value basis requires Upper bound 'not applicable'")
        return
    if bound == "unavailable":
        if verdict == "not-worth-it":
            failures.append("an upper-bound not-worth-it verdict requires a finite Upper bound")
        return
    bound_quantity = parse_quantity(bound)
    if bound_quantity is None:
        failures.append(
            "Upper bound must be 'unavailable' or a nonnegative decimal followed by its unit"
        )
        return
    if verdict != "not-worth-it":
        return
    cost_quantity = parse_quantity(cost)
    if cost_quantity is None:
        failures.append("an upper-bound not-worth-it verdict requires a stated full Cost")
        return
    if cost_quantity[1] != bound_quantity[1]:
        failures.append(
            "an upper-bound not-worth-it verdict requires Cost in the Upper bound's unit"
        )
    elif cost_quantity[0] + _REL_TOLERANCE * max(bound_quantity[0], 1) < bound_quantity[0]:
        failures.append("an upper-bound not-worth-it verdict requires Cost at least Upper bound")


def _check_voi(sections: dict[str, str]) -> list[str]:
    failures: list[str] = []
    voi = sections["VoI"]
    verdict = _bare(field(voi, "Verdict:") or "")
    if verdict not in VOI_VERDICTS:
        failures.append(
            f"Verdict value {verdict!r} is not in the closed set {sorted(VOI_VERDICTS)}"
        )
    signal = _voi_prose(voi, "Signal model:") or ""
    basis = _bare(field(voi, "Value basis:") or "")
    if basis not in VOI_BASES:
        failures.append(f"Value basis {basis!r} is not in the closed set {sorted(VOI_BASES)}")
    _check_voi_signal_model(signal, basis, failures)
    if basis == "upper-bound" and verdict not in {"upper-bound-only", "not-worth-it"}:
        failures.append("upper-bound Value basis requires upper-bound-only or not-worth-it")
    if basis == "signal-model" and verdict == "upper-bound-only":
        failures.append("signal-model Value basis cannot carry an upper-bound-only verdict")
    bound = (field(voi, "Upper bound:") or "").strip()
    cost = (field(voi, "Cost:") or "").strip()
    _check_voi_upper_bound(basis, bound, cost, verdict, failures)
    if cost == "none stated":
        if basis == "signal-model" and verdict != "break-even-only":
            failures.append(
                "an unstated full cost with signal-model basis makes the break-even "
                "price the deliverable; "
                "the verdict must be break-even-only"
            )
        if basis == "upper-bound" and verdict == "not-worth-it":
            failures.append("an upper-bound not-worth-it verdict requires a stated full Cost")
    elif parse_quantity(cost) is None:
        failures.append(
            "Cost must state a nonnegative decimal followed by its unit, "
            f"or read exactly 'none stated'; found {cost!r}"
        )
    elif basis == "signal-model" and verdict == "break-even-only":
        failures.append("a stated full Cost with signal-model basis requires a net-value verdict")
    return failures


def main(argv: list[str]) -> int:
    if len(argv) != 1:
        print("usage: check_decision.py <record.md>", file=sys.stderr)
        return EXIT_UNVERIFIABLE
    try:
        text = Path(argv[0]).read_text(encoding="utf-8")
    except OSError as exc:
        print(f"UNVERIFIABLE: {exc}", file=sys.stderr)
        return EXIT_UNVERIFIABLE
    failures = check(text)
    for failure in failures:
        print(f"GATE FAILURE: {failure}")
    return EXIT_GATE_FAILURE if failures else EXIT_OK


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
