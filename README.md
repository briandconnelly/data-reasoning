# data-reasoning

A Claude Code and Codex plugin for reasoning from data: structured exploration that generates honest leads, hypothesis-driven investigation that adjudicates them, causal identification review that turns a dead end into a reviewed, assumption-bounded design, and decision analysis that turns unresolved evidence into a defensible act-wait-or-collect verdict.

## Skills

| Skill | What it covers |
| --- | --- |
| [exploratory-data-analysis](skills/exploratory-data-analysis/) | Structured exploratory data analysis — orient before interpreting, count every look, consolidate ranked leads with their search context, and hand adjudication to hypothesis-driven-analysis. |
| [hypothesis-driven-analysis](skills/hypothesis-driven-analysis/) | Guide empirical investigations with PPDAC and the scientific method — competing hypotheses, preregistered predictions, adequate tests, and a precommitted stop rule. |
| [causal-identification-review](skills/causal-identification-review/) | Review whether a design — proposed, claimed, or still to be found — identifies a causal effect and on what assumptions, with candidate designs, breakable identifying assumptions, probes run against them, and an evidence-bounded disposition that never certifies. |
| [decision-analysis](skills/decision-analysis/) | Decide under uncertainty — a framed choice, provenance-classed odds-form updates, robustness sweeps with crossover statements, value-of-information for collect-more options, and an evidence-bounded verdict that never authorizes execution. |

Exploration generates hypotheses and never confirms them; adjudication is `hypothesis-driven-analysis`'s work; `causal-identification-review` is the constructive continuation when adjudication concludes nothing identifies the effect, or when a claimed design needs its identifying assumptions checked before anyone trusts it.
`decision-analysis` is the constructive continuation when a decision hangs on what an investigation left `UNRESOLVED`: it consumes ledgers and review records as evidence, and its verdicts recommend without authorizing.
All four skills carry the same authorization gate; its text lives once in `scripts/shared-sections/authorization-gate.md` and is rendered into each skill by `scripts/check-shared-sections.py`, which fails when a rendered copy drifts or is hidden.

The pairing is a design claim, not a measured one.
`hypothesis-driven-analysis` has an archived scenario suite behind it (`skills/hypothesis-driven-analysis/tests/`).
`exploratory-data-analysis` has measured description-trigger arms only (`skills/exploratory-data-analysis/tests/runs/2026-08-11-t13-trigger.md`, `2026-08-11-t14-trigger.md`, and the repaired rerun; the lift is recorded in `skills/exploratory-data-analysis/decisions/005-generic-speech-acts-claimed.md`); its behavior scenarios in `tests/scenarios.md` are authored and unrun.
No run has yet exercised a handoff between the two.
Per `skills/hypothesis-driven-analysis/tests/scenarios.md` § "Owed measurements as of 2026-08-08", `hypothesis-driven-analysis`'s description was re-validated on 2026-08-08 against the then two-skill shipped surface plus a `systematic-debugging` stand-in, not the four skills that now ship.
`causal-identification-review`'s description has n=1 trigger cells (CS1, CS2, CS6a) against a three-skill catalog; `decision-analysis`'s has none.
Routing between all four skills rests on zero arms run against the full catalog — the freeze in `skills/exploratory-data-analysis/decisions/006-description-freeze-until-measured.md` holds every description until that changes.
Treat the routing between them, and the handoff itself, as unverified.
`causal-identification-review`'s measurement wave 1 (n=1 per cell) was scored on 2026-08-09 and then partly reopened the same day: CS4 and CS7 moved to "redesign and re-measure" and owe fresh arms before the wave is complete (`skills/causal-identification-review/tests/scenarios.md` § "Global verdict table", addendum).
`decision-analysis`'s original scenarios remain unrun (`skills/decision-analysis/tests/scenarios.md`); focused VoI wording checks are recorded in `skills/decision-analysis/tests/runs/2026-09-04-voi-pricing.md`, with no observed behavioral lift over the old wording for the archived input snapshots.
Treat its routing and its premium as unmeasured.

Three pieces of evidence are owed and not started, named here so the gap is not mistaken for an oversight (external review, 2026-09-15):

- An end-to-end integration suite for the shipped four-skill workflow, on both hosts: a direct answer that loads no skill, exploration handing a lead to adjudication, adjudication handing a dead end to identification review, and an `UNRESOLVED` ledger entering a decision record.
  Every arm run so far exercises one skill in isolation; none shows an agent choosing the right skill, keeping the evidence boundary across a handoff, or finishing the user's task.
- A frozen representative suite kept alongside the adversarial catalogs.
  The catalogs' rule that a baseline already passing means the scenario is too easy finds failures; it cannot estimate practical benefit, because ordinary tasks a baseline already handles still pay the skill's context and ceremony.
  The representative suite keeps such tasks, and scores accuracy, unnecessary ceremony, latency, and total context cost.
- Measured simplification experiments: the checkers below preserve wording and provenance, but nothing yet establishes whether each accumulated rule still earns its context cost.

The skill wording this remediation changed was measured on 2026-09-15 on the cells that reach it, with a baseline arm, a pre-edit arm, and a post-edit arm per cell (`skills/hypothesis-driven-analysis/tests/runs/artifacts/2026-09-15-remediation-wave-prereg.md` § Results).
One sentence reached behavior (the estimation route's data-validity inheritance); the rest either did not change behavior against the pre-edit skill at n=1 or failed on form both arms share; the run records say which, and the owner's decision on each is recorded there.

The measured premiums above count the procedure, not the prose: loading a skill has a fixed context cost the scenario arms do not meter.
As of 2026-09-15 (`wc -w skills/*/SKILL.md skills/*/references/*.md`): `hypothesis-driven-analysis` is 6,419 words plus a 3,180-word ledger template and a 700-word subagent brief; `decision-analysis` is 3,569 plus a 715-word template; `causal-identification-review` is 2,440 plus 492; `exploratory-data-analysis` is 2,510 plus 843.
Co-loading two skills — the designed handoff case — pays the verbatim authorization gate (~350 words) and a near-duplicate costly-collection section once per skill loaded.
Reducing that duplication means extracting the shared contract, which edits `hypothesis-driven-analysis` and is deferred on the terms in `skills/exploratory-data-analysis/decisions/001-shared-gate-authority.md` § Consequences.

## Output style

The plugin ships one optional output style, `Data Answer` (`output-styles/data-answer.md`): an analyst persona that answers data questions answer-first, with a short standing bar on reporting numbers you have not checked.
The file is the contract; this section does not restate it.

It supplies presentation and answer hygiene, not analysis method.
The skills decide what an answer must disclose and what a report must contain; the style yields to a skill's report format, its ordering, and its placement rules wherever one applies.

It adds no record-keeping to HDA's ceremony-free `direct` route, but it does shape a direct answer — a source-and-freshness footer, an offer of the query.
Whether the split between the two holds under a real run is untested; treat it as a design claim, like the routing and handoffs above.

Select it through `/config` → Output style.
It sets `force-for-plugin: false`, so installing the plugin never changes the active style on its own, and `keep-coding-instructions: true`, so the default coding guidance stays in place for the code an analysis has to write.

Output styles are a Claude Code feature.
Codex has no equivalent, so a Codex install gets the four skills and no style.

## Live record validation

Both hosts get a PostToolUse hook (`hooks/hooks.json`, declared in both plugin manifests) that runs `instruments/check_record.py` on a record file the agent writes through the host's file tools and feeds structural findings back to the agent.
What the validator may and may not check is owned by `skills/hypothesis-driven-analysis/decisions/006-instruments-are-not-a-live-self-check.md`.
The write paths covered are exactly these: Claude Code's `Write` and `Edit` tools, which name the file in `tool_input.file_path`, and Codex's `apply_patch`, whose `Write|Edit` matcher alias hands the hook the patch text in `tool_input.command`.
A record created by a shell command — a heredoc, a redirect, a script — is on neither path and is not validated; nothing in this plugin parses shell commands for file writes.
Codex runs a plugin hook only after the user has reviewed and trusted its definition (`/hooks` in Codex), so a Codex install has no live validation until that trust is granted.
The hook needs `python3` on the host's `PATH`.
Without it, a record write is reported as not validated and every other write stays silent; a record whose path contains a double quote cannot be sniffed without Python and is skipped.
Without it, an `apply_patch` payload is handled by sniffing each `.md` file the patch names on disk and by scanning the patch text itself for a record title, so both a new record and a title-free edit to an existing one are reported as not validated, while a file the patch names that is not on disk is skipped.
The hook runs the validator's default mode, in which a record still carrying template placeholders or `pending` slots is in progress and owes no completeness findings; `check_record.py --final <record>` is the completed-record mode, in which every required slot must be filled.
No skill yet tells the agent to run `--final` before delivering a record: that pointer is agent-read prose and owes measured arms first, on the terms in the decision record above.

## Installation

### Claude Code

This repository is its own plugin marketplace (`.claude-plugin/marketplace.json`).
Add it from the `release` branch, then install the plugin from it:

```
/plugin marketplace add briandconnelly/data-reasoning#release
/plugin install data-reasoning@data-reasoning
```

`#release` is a runtime-only branch rebuilt by CI on every push to `main`.
Adding the marketplace without it clones the full evidence archive.

### Codex

Add the marketplace pinned to the `release` branch, then install the plugin from it:

```bash
codex plugin marketplace add briandconnelly/data-reasoning --ref release
codex plugin add data-reasoning@data-reasoning
```

Adding the marketplace without `--ref release` clones the full evidence archive.
Start a new Codex session after installation so the bundled skills are available.

## Development

All gates run through [prek](https://github.com/j178/prek):

```bash
prek run --all-files
```

## License

MIT
