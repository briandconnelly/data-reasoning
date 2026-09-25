#!/usr/bin/env python3
"""Ask Jev the two plan-time questions the structural validator cannot answer.

    python jev/semantic_check.py path/to/ledger.md [--json]

Per hypothesis row: does the necessary prediction follow from the candidate
explanation? Per ledger: is the stop condition fixed independently of the
answer? These are HDA decisions/006's named blind spots of structural checks.

Only Plan-time text is sent: the hypothesis row and the Problem section's stop
condition. Tests, outcomes, statuses, and the Conclusion never reach Jev, so a
correct refutation cannot change an answer. What the output may be used for is
owned by jev/README.md; it is advisory and never a gate.

Exit 0 when checked (flags are printed, not failed), 2 when Jev was
unavailable, 1 when the file is not a full-route ledger.
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).parent))
import jev_client

REPO = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location(
    "check_record", REPO / "instruments" / "check_record.py"
)
assert _spec is not None
assert _spec.loader is not None
check_record = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(check_record)

BAND = (0.4, 0.6)
MIN_TABLE_ROWS = 2  # a header and at least one hypothesis

FOLLOWS = {
    "type": "noul",
    "instructions": (
        "`hypothesis.candidate_explanation` is a proposed explanation, and "
        "`hypothesis.necessary_prediction` is the observation declared, before any data was "
        "read, to be one that refutes the explanation if it fails. If the explanation were "
        "true, would the necessary prediction have to hold? Answer about the logical link "
        "only; do not judge whether the explanation is likely."
    ),
    "criteria": {
        "true": (
            "The prediction is a consequence of the explanation's mechanism: a true instance "
            "of the explanation could not fail it."
        ),
        "false": (
            "The prediction is merely compatible with the explanation, could fail even if the "
            "explanation were true, restates the explanation, or is unrelated to it."
        ),
    },
}

STOP = {
    "type": "noul",
    "instructions": (
        "`stop_condition` is the investigation's precommitted criterion for concluding or "
        "stopping, written before any data was read. Is it fixed independently of which "
        "answer the investigation reaches?"
    ),
    "criteria": {
        "true": (
            "It names a budget, a test set, or a decision threshold that applies whatever the "
            "result is, e.g. 'stop after T1-T4 or 30 queries'."
        ),
        "false": (
            "It depends on reaching a particular answer, e.g. 'stop when an explanation is "
            "confirmed' or 'stop once a significant difference is found', or it is empty."
        ),
    },
}


def plan_time_states(text: str) -> tuple[list[dict[str, Any]], str | None]:
    """The hypothesis rows and stop condition, and nothing written after Plan."""
    body = check_record.strip_frontmatter(text)
    rows = check_record._table_rows(check_record._section(body, "## Hypotheses"))
    if len(rows) < MIN_TABLE_ROWS:
        raise ValueError("no Hypotheses table: not a full-route ledger")
    header = [check_record._header_key(h) for h in rows[0]]

    def col(*names: str) -> int:
        for name in names:
            key = check_record._header_key(name)
            if key in header:
                return header.index(key)
        raise ValueError(f"Hypotheses table has no column among {names}")

    i_id, i_claim = col("id"), col("claim")
    i_expl = col("Candidate explanation")
    i_nec = col("Necessary prediction (failure refutes)", "Necessary prediction")
    hyps = [
        {
            "id": r[i_id],
            "claim": r[i_claim],
            "candidate_explanation": r[i_expl],
            "necessary_prediction": r[i_nec],
        }
        for r in rows[1:]
    ]
    stop = check_record._slot_value(check_record._section(body, "## Problem"), "Stop condition")
    return hyps, stop


def verdict(p: float) -> str:
    return "flag" if p < BAND[0] else "ok" if p > BAND[1] else "abstain"


def check(text: str, transport: jev_client.Transport | None = None) -> dict[str, Any]:
    hyps, stop = plan_time_states(text)
    results = []
    for h in hyps:
        resp = jev_client.evaluate({"hypothesis": h}, {"follows": FOLLOWS}, transport=transport)
        p = jev_client.probability_of_pass(resp["answers"]["follows"])
        results.append(
            {
                "id": h["id"],
                "question": "necessary prediction follows",
                "p": round(p, 3),
                "verdict": verdict(p),
            }
        )
    if stop:
        resp = jev_client.evaluate({"stop_condition": stop}, {"stop": STOP}, transport=transport)
        p = jev_client.probability_of_pass(resp["answers"]["stop"])
        results.append(
            {
                "id": "Problem",
                "question": "stop condition fixed in advance",
                "p": round(p, 3),
                "verdict": verdict(p),
            }
        )
    else:
        results.append(
            {
                "id": "Problem",
                "question": "stop condition fixed in advance",
                "p": None,
                "verdict": "not_checked",
            }
        )
    return {"results": results}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("ledger", type=Path)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    try:
        report = check(args.ledger.read_text())
    except ValueError as exc:
        print(f"{args.ledger}: {exc}", file=sys.stderr)
        return 1
    except jev_client.JevUnavailable as exc:
        print(f"not checked: {exc}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(report, indent=1))
    else:
        for r in report["results"]:
            print(f"{r['verdict']:>11}  {r['id']}: {r['question']} (p={r['p']})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
