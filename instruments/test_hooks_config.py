"""The shipped hook configuration must match the documented plugin shape:
hooks/hooks.json wraps events in a top-level "hooks" key, and the manifest
declares the file. A malformed config here means the plugin installs with no
live validation and nothing else notices."""

import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]


def test_hooks_json_shape():
    cfg = json.loads((REPO / "hooks" / "hooks.json").read_text(encoding="utf-8"))
    entries = cfg["hooks"]["PostToolUse"]
    assert len(entries) == 1
    entry = entries[0]
    assert entry["matcher"] == "Write|Edit"
    hook = entry["hooks"][0]
    assert hook["type"] == "command"
    # Claude Code exports CLAUDE_PLUGIN_ROOT, Codex exports PLUGIN_ROOT; the
    # command must resolve under either host.
    assert "${CLAUDE_PLUGIN_ROOT:-${PLUGIN_ROOT}}" in hook["command"]
    assert "check_record_hook.sh" in hook["command"]


def test_plugin_manifests_declare_hooks():
    for manifest_dir in (".claude-plugin", ".codex-plugin"):
        manifest = json.loads((REPO / manifest_dir / "plugin.json").read_text(encoding="utf-8"))
        assert manifest["hooks"] == "./hooks/hooks.json", manifest_dir
