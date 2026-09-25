"""Minimal stdlib client for TypeSafe's System One endpoint (the Jev model).

Everything under jev/ is optional development tooling: it never ships in the
release tree and nothing in the plugin or its hook imports it. Callers must
treat JevUnavailable as "not checked", never as a pass.

The model is pinned rather than aliased: `jev-latest` moves when a release
ships, and a grading question calibrated against one version is not evidence
about the next. Every response records the versioned model that answered.
"""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from collections.abc import Callable
from typing import Any

ENDPOINT = "https://api.typesafe.ai/v1/systemone"
MODEL = "jev-1.13.0"
KEY_VAR = "TYPESAFE_API_KEY"

Transport = Callable[[dict[str, Any]], dict[str, Any]]


class JevUnavailable(RuntimeError):
    """No key, no network, or an API error: the check did not run."""


def _http_transport(body: dict[str, Any]) -> dict[str, Any]:
    key = os.environ.get(KEY_VAR)
    if not key:
        raise JevUnavailable(f"{KEY_VAR} is not set")
    req = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(body).encode(),
        method="POST",
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return json.loads(resp.read())
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
        raise JevUnavailable(f"System One request failed: {exc}") from exc


def available() -> bool:
    return bool(os.environ.get(KEY_VAR))


def evaluate(
    state: Any,
    questions: dict[str, dict[str, Any]],
    *,
    model: str = MODEL,
    transport: Transport | None = None,
) -> dict[str, Any]:
    """Ask every question about one state in a single request.

    Returns the raw response: {"model", "answers": {id: answer}, "usage"}.
    Raises JevUnavailable if the request cannot run or an answer is missing.
    """
    body = {"state": state, "model": model, "questions": questions}
    resp = (transport or _http_transport)(body)
    missing = set(questions) - set(resp.get("answers", {}))
    if missing:
        raise JevUnavailable(f"response omitted answers for {sorted(missing)}")
    return resp


def probability_of_pass(answer: dict[str, Any], pass_option: str | None = None) -> float:
    """Collapse an answer to P(pass): a Noul's p(yes), or a Choice's p(pass_option)."""
    if answer["type"] == "noul":
        return float(answer["noul"])
    if answer["type"] == "choice":
        if pass_option is None:
            raise ValueError("a choice question needs a pass option")
        return float(answer["probabilities"].get(pass_option, 0.0))
    raise ValueError(f"unsupported answer type {answer['type']!r}; score questions are not graded")
