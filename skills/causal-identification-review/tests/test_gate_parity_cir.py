"""causal-identification-review's authorization gate must match HDA's verbatim.

Mirrors `skills/exploratory-data-analysis/tests/test_gate_parity.py`. Skills
install standalone -- a harness may load any one of them without the others
on disk -- so each skill carries its own verbatim copy of the shared
authorization-gate text rather than pointing at another skill's file
(AGENTS.md: one home per normative rule, everywhere else a copy or a
pointer). `hypothesis-driven-analysis/SKILL.md` § "Authorization gate
(always binds)" is that one home; this check keeps this skill's copy from
drifting from it.
"""

import re
from pathlib import Path

import pytest

SKILLS_DIR = Path(__file__).resolve().parents[2]
HDA_SKILL = SKILLS_DIR / "hypothesis-driven-analysis" / "SKILL.md"
CIR_SKILL = SKILLS_DIR / "causal-identification-review" / "SKILL.md"
HEADING = "### Authorization gate (always binds)"
MIN_GATE_LENGTH = 1000


def gate_block(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    start = text.index(HEADING)
    rest = text[start + len(HEADING) :]
    nxt = re.search(r"\n#{2,3} ", rest)
    end = start + len(HEADING) + (nxt.start() if nxt else len(rest))
    return text[start:end].strip()


@pytest.mark.parametrize("path", [HDA_SKILL, CIR_SKILL], ids=["hda", "cir"])
def test_gate_block_extracts_real_content(path: Path):
    """The instrument can surface a known positive, so an empty match cannot pass.

    Run against both sides, not just the authority: a comparison of two blocks
    the extractor silently truncated the same way would pass while checking
    nothing.
    """
    block = gate_block(path)
    assert "None of the following is authorization" in block
    assert len(block) > MIN_GATE_LENGTH


def test_authorization_gate_matches_hda_verbatim():
    assert gate_block(CIR_SKILL) == gate_block(HDA_SKILL)
