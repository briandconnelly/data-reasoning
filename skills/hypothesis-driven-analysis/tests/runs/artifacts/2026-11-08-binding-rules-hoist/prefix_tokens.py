#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["tiktoken==0.14.0"]
# ///
"""Measure and cut a SKILL.md prefix by token count, for the binding-rules wave.

Tokenizer: tiktoken `o200k_base`. It is not Claude's tokenizer, which is not
available offline; the bytes/4 proxy is printed beside it so a reader can see
how far apart two cheap estimates are. Neither is what Claude Code uses when it
re-attaches a skill after compaction, and the run record says so.

    uv run prefix_tokens.py offsets <SKILL.md> '<marker>' ...
        print, for each marker, the token and byte offset at which it ends
    uv run prefix_tokens.py cut <SKILL.md> <out> [--tokens 5000]
        write the first N o200k_base tokens of the file to <out>, print sha256s
"""

from __future__ import annotations

import argparse
import hashlib
from pathlib import Path

import tiktoken

ENC = tiktoken.get_encoding("o200k_base")


def offsets(path: Path, markers: list[str]) -> None:
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        end = text.index(marker) + len(marker)
        pre = text[:end]
        nbytes = len(pre.encode("utf-8"))
        print(
            f"{marker!r}: o200k_base={len(ENC.encode(pre))} bytes={nbytes} bytes/4={nbytes // 4}"
        )
    whole = text.encode("utf-8")
    print(f"whole file: o200k_base={len(ENC.encode(text))} bytes={len(whole)}")


def cut(path: Path, out: Path, tokens: int) -> None:
    src = path.read_bytes()
    text = src.decode("utf-8")
    prefix = ENC.decode(ENC.encode(text)[:tokens])
    out.write_text(prefix, encoding="utf-8")
    print(f"source {path}: sha256={hashlib.sha256(src).hexdigest()}")
    print(
        f"prefix {out}: first {tokens} o200k_base tokens, {len(prefix.encode('utf-8'))} bytes, "
        f"sha256={hashlib.sha256(out.read_bytes()).hexdigest()}"
    )
    last = prefix.rstrip().splitlines()[-1] if prefix.strip() else ""
    print(f"prefix ends mid-line: {last[-80:]!r}")


def main() -> None:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    o = sub.add_parser("offsets")
    o.add_argument("path", type=Path)
    o.add_argument("markers", nargs="+")
    c = sub.add_parser("cut")
    c.add_argument("path", type=Path)
    c.add_argument("out", type=Path)
    c.add_argument("--tokens", type=int, default=5000)
    args = ap.parse_args()
    if args.cmd == "offsets":
        offsets(args.path, args.markers)
    else:
        cut(args.path, args.out, args.tokens)


if __name__ == "__main__":
    main()
