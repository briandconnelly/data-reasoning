"""Run one representative cell with an explicit-load sentence before its frozen prompt.

Everything else is scripts/run_integration.py unchanged: the frozen prompt and fixtures
are verified against the prereg's hashes first, and only the prompt handed to the host
gains the sentence. See prereg.md beside this file.
Usage: forced.py <the same arguments as run_integration.py>
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[5] / "scripts"))
import run_integration as ri

PREFIX = (
    "First load the data-reasoning:hypothesis-driven-analysis skill and follow its instructions. "
)
_original = ri.host_command


def _forced(args, base, root, prompt):
    forced = PREFIX + prompt
    base.with_suffix(".prompt.txt").write_text(forced + "\n", encoding="utf-8")
    return _original(args, base, root, forced)


ri.host_command = _forced

if __name__ == "__main__":
    ri.main()
