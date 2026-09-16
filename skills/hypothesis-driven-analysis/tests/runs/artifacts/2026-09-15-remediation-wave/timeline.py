#!/usr/bin/env python3
"""Print an archived arm's assistant text blocks and tool calls in order.

    python3 timeline.py <name>.jsonl [--full]

Text blocks are truncated to 400 characters unless --full is given; tool
calls show the tool name and the path-bearing fields. Used by the scorer for
ordering assertions (what was said before which read).
"""

import json
import sys
from pathlib import Path

PATH_FIELDS = ("file_path", "path", "command", "pattern", "notebook_path")


def main() -> None:
    path = Path(sys.argv[1])
    full = "--full" in sys.argv
    n = 0
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            ev = json.loads(line)
        except json.JSONDecodeError:
            continue
        if ev.get("type") != "assistant":
            continue
        for block in ev.get("message", {}).get("content", []) or []:
            if block.get("type") == "text":
                text = block.get("text", "")
                print(f"[text] {text if full else text[:400]}")
            elif block.get("type") == "tool_use":
                n += 1
                inp = block.get("input", {}) or {}
                fields = {k: str(inp[k])[:200] for k in PATH_FIELDS if inp.get(k)}
                print(f"[tool {n}] {block.get('name')} {fields}")


if __name__ == "__main__":
    main()
