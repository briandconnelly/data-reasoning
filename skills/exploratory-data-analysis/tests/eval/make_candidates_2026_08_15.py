"""Derive the 2026-08-15 candidate descriptions from the frozen shipped text.

Each candidate is B (the compression) plus one replacement, so the widening
edit stays single-variable by construction. Asserts lengths and the intact
exclusion tail before writing anything.
"""

from pathlib import Path

EVAL = Path(__file__).parent
SHIPPED = (EVAL / "frozen-2026-08-11-treatment.txt").read_text().rstrip("\n")

COMP_CUT = ", to confirm, never to conclude from"

OLD_OPEN = (
    "Use when handed a dataset, log, or event stream to explore, or a named entity "
    "— an account, customer, or segment — whose story is wanted, "
    "no effect to explain and no claim to check —"
)
NEW_OPEN = (
    "Use for any request about a named entity — an account, customer, or segment "
    "— that asks what is going on with it, in whatever words, "
    "and when handed a dataset, log, or event stream to explore —"
)

EX_OLD = (
    '"what\'s in this data", "profile this", "anything interesting or anomalous", '
    '"tell me about this account"'
)
EX_C2 = EX_OLD + ', "an overview of X", "a rundown on X"'
EX_C3 = (
    '"what\'s in this data", "anything interesting or anomalous" — an overview, '
    "a rundown, or a profile of a named entity all belong here"
)

MAX_DESCRIPTION_LENGTH = 1024  # shipped-description budget the candidates must fit

TAIL_MARKERS = [
    "hypothesis-driven-analysis",
    "bounded descriptive",
    "or summarizing prose",
    "why did this account's spend drop",
    "explore why churn rose",
]


def replace_once(text: str, old: str, new: str) -> str:
    assert text.count(old) == 1, f"expected exactly one occurrence of {old!r}"
    return text.replace(old, new)


def main() -> None:
    b = replace_once(SHIPPED, COMP_CUT, "")
    c1 = replace_once(b, OLD_OPEN, NEW_OPEN)
    c2 = replace_once(b, EX_OLD, EX_C2)
    c3 = replace_once(replace_once(b, OLD_OPEN, NEW_OPEN), EX_OLD, EX_C3)

    expected = {"B-compressed": (b, 983), "C1": (c1, 994), "C2": (c2, 1021), "C3": (c3, 1021)}
    for name, (text, length) in expected.items():
        assert len(text) == length, f"{name}: {len(text)} != {length}"
        assert len(text) <= MAX_DESCRIPTION_LENGTH, name
        for marker in TAIL_MARKERS:
            assert marker in text, f"{name} lost tail marker {marker!r}"
        (EVAL / f"frozen-2026-08-15-{name}.txt").write_text(text + "\n")
        print(f"{name}: {length} chars, tail intact")


if __name__ == "__main__":
    main()
