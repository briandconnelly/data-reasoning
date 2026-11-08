# Installing

The install commands are in the [README](../README.md#install).
This page covers what comes after them.

The default branch, `main`, holds only the runtime tree, rebuilt by CI on every push to `dev`, so an install never downloads the evidence archive.
This repository is its own plugin marketplace.

## Invoke a skill explicitly

A skill loads automatically only when the host routes your request to it, and that routing depends on how you phrase the ask.
For `exploratory-data-analysis`, automatic routing was measured only against a reduced catalog, not the four shipped skills.
In that run, asks phrased "Profile ..." loaded the skill 30/30 times, "Give me a rundown on ..." 23/30, "Give me an overview of ..." 21/30, and "Tell me about ..." 8/30.
The run's per-invocation results are in `skills/exploratory-data-analysis/tests/runs/artifacts/2026-08-15-widening/BvC-fresh/results.jsonl` on the `dev` branch ([pinned copy](https://github.com/briandconnelly/data-reasoning/blob/5fc87dca1358ef41173924ad0ce1ecb9ef35a4f3/skills/exploratory-data-analysis/tests/runs/artifacts/2026-08-15-widening/BvC-fresh/results.jsonl)), which an install does not carry.

To make sure a skill loads, invoke it explicitly:

- Claude Code: run `/data-reasoning:exploratory-data-analysis` followed by your request, or ask for the `exploratory-data-analysis` skill by name.
- Codex: mention the skill as `$exploratory-data-analysis` in your request, as in "Use `$exploratory-data-analysis` to explore this dataset".

For the other three skills, use the same forms with that skill's name.
How often an explicit invocation leads to a completed analysis has not been measured on either host.

## Verify a Codex install

Codex runs a plugin hook only after the user has reviewed and trusted its definition: open `/hooks`, select the data-reasoning hook, and review/trust it.
Repeat that review if Codex reports changed hook definitions after an update.

Use the actual installed plugin root below, not a source checkout; a loaded skill's path is `<plugin-root>/skills/<skill-name>/SKILL.md`.
The install checker needs Python 3.11 or newer and executes the installed hook command against a temporary invalid record, which it removes afterward.

```bash
python3 /absolute/path/to/data-reasoning/instruments/check_install.py
```

A pass checks the discoverable skill layout and direct hook execution only; it cannot establish that Codex trusts or invokes the hook.
For the live test, ask Codex:

> Use `apply_patch` to create a new temporary Markdown file in this workspace containing `# Decision Record: hook probe`, then `## Verdict`, then `- Verdict: optimal`, with blank lines between them.
> Report whether the tool response automatically includes data-reasoning structural findings, then remove the temporary file.
> Do not invoke the hook script manually for this test.

The expected feedback includes the invalid `optimal` verdict and missing sections.
A successful file write with no findings is not a successful hook test; check `/hooks` and retry in a new session.
For writes outside the hook's coverage, see [Record validation](record-validation.md).

## Recover an install containing test skills

The advertised data-reasoning skills should be the four listed in the [README](../README.md).
An extra `data-reasoning:s18-analytics` comes from a development fixture: a full source checkout was installed instead of the runtime release tree.
The release builder excludes fixtures, and the install checker reports nested discoverable skills.
For an older install without that checker, run the current source checkout's `instruments/check_install.py` with the installed plugin root as its argument.

Remove the old install, then reinstall using the Codex commands in the [README](../README.md#install), start a new session, and repeat [verification](#verify-a-codex-install).
For a plugin installed from a configured marketplace, remove that marketplace by its actual name with `codex plugin marketplace remove <marketplace-name>`.
For the default personal marketplace, remove the plugin with `codex plugin remove data-reasoning@<marketplace-name>`.
Do not delete or edit individual cached fixture files: the source package determines what returns on the next install.

## Local development installs

Build a runtime tree first and register that directory as the marketplace:

```bash
python3 scripts/build-release-tree.py /absolute/path/to/data-reasoning-runtime
python3 /absolute/path/to/data-reasoning-runtime/instruments/check_install.py
codex plugin marketplace add /absolute/path/to/data-reasoning-runtime
codex plugin add data-reasoning@data-reasoning
```

Use a fresh output directory or one previously created by this builder.
Resolve an existing marketplace registration as described above before registering a different source with the same name.
