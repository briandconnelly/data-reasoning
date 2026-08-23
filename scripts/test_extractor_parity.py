"""The skills' hidden-text extractors must not drift from each other.

Skills install standalone -- a harness may load any one of them without the
others on disk -- so each carries its own verbatim copy of the extractor
rather than importing a shared module (AGENTS.md: one home per normative
rule, everywhere else a copy or a pointer). Nothing enforced that the copies
stayed identical, and three review rounds found defects fixed in one copy and
left in its siblings. This check is the enforcement.
"""

import re
from pathlib import Path

import pytest

SKILLS = Path(__file__).resolve().parents[1] / "skills"
EXTRACTORS = (
    SKILLS / "exploratory-data-analysis" / "tests" / "test_gate_parity.py",
    SKILLS / "decision-analysis" / "tests" / "test_gate_parity_da.py",
    SKILLS / "causal-identification-review" / "tests" / "test_gate_parity_cir.py",
)
# the shared region: the code-span helpers through the end of visible_text
MIN_REGION_LINES = 50
REGION = re.compile(
    r"^BACKTICK_RUN = re\.compile.*?^def visible_text.*?(?=^def gate_block_from_text)",
    re.S | re.M,
)


def shared_region(path: Path) -> str:
    m = REGION.search(path.read_text())
    if m is None:
        pytest.fail(f"{path.name}: shared extractor region not found")
    return m.group(0)


def test_every_skill_carries_the_same_extractor():
    regions = {p.name: shared_region(p) for p in EXTRACTORS}
    first = next(iter(regions.values()))
    drifted = [name for name, text in regions.items() if text != first]
    assert not drifted, f"extractor copies drifted from each other: {drifted}"


def test_the_region_is_not_trivially_empty():
    """A check that matched nothing would pass for the wrong reason."""
    for path in EXTRACTORS:
        region = shared_region(path)
        assert "code_span_interiors" in region, path.name
        assert "def visible_text" in region, path.name
        assert len(region.splitlines()) > MIN_REGION_LINES, path.name
