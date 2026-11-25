"""Run one representative cell with an explicit-load sentence before its frozen prompt.

Everything else is scripts/run_integration.py unchanged; see prereg.md beside this file.
Usage: forced.py <the same arguments as run_integration.py>
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "scripts"))
import run_integration as ri  # noqa: E402

PREFIX = (
    "First load the data-reasoning:hypothesis-driven-analysis skill and follow its instructions. "
)
_original = ri.cell_prompt


def _forced(cell, data):
    return PREFIX + _original(cell, data)


ri.cell_prompt = _forced

if __name__ == "__main__":
    ri.main()
