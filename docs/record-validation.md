# Record validation

Both hosts get a PostToolUse hook (`hooks/hooks.json`, declared in both plugin manifests) that runs `instruments/check_record.py` on a record file the agent writes through the host's file tools and feeds structural findings back to the agent.
What the validator may and may not check is owned by `skills/hypothesis-driven-analysis/decisions/006-instruments-are-not-a-live-self-check.md`.

## Which writes are covered

The write paths covered are exactly these: Claude Code's `Write` and `Edit` tools, which name the file in `tool_input.file_path`, and Codex's `apply_patch`, whose `Write|Edit` matcher alias hands the hook the patch text in `tool_input.command`.
A record created by a shell command — a heredoc, a redirect, a script — is on neither path and is not validated; nothing in this plugin parses shell commands for file writes.
For Codex hook activation and verification, see [Installing](installing.md#verify-a-codex-install).

## Requirements and fallbacks

The hook needs `python3` on the host's `PATH`.
Without it, a record write is reported as not validated and every other write stays silent; the shell fallback classifies a file by its title line alone, exactly as the Python hook does, and needs `sh`, `sed`, `head`, `grep`, `awk`, and `cat`.
A record whose path contains a double quote cannot be sniffed without Python and is skipped.
Without Python, an `apply_patch` payload is handled by sniffing each `.md` file the patch names on disk and by scanning the patch text itself for a record title, so both a new record and a title-free edit to an existing one are reported as not validated, while a file the patch names that is not on disk is skipped.

## Modes

The hook runs the validator's default mode, in which a record still carrying template placeholders or `pending` slots is in progress and owes no completeness findings.
`check_record.py --final <record>` is the completed-record mode, in which every required slot, every required section, and every cell of a required section's table must be filled, except a Tests row left `NOT_TESTED`, whose evidence may stay `pending`.
No skill yet tells the agent to run `--final` before delivering a record: that pointer is agent-read prose and owes measured arms first, on the terms in decision record 006 cited at the top of this page.

## Running the validator by hand

For a record written through the shell, or an explicit completed-record check, run the validator directly from the installed plugin directory:

```bash
python3 /absolute/path/to/data-reasoning/instruments/check_record.py /absolute/path/to/record.md
python3 /absolute/path/to/data-reasoning/instruments/check_record.py --final /absolute/path/to/record.md
```

These commands provide structural validation, not a review of the analysis or evidence.
