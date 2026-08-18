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
All four skills carry the same authorization gate verbatim, and `skills/exploratory-data-analysis/decisions/001-shared-gate-authority.md` names `hypothesis-driven-analysis/SKILL.md` as its single authority — three parity tests (EDA↔HDA, CIR↔HDA, DA↔HDA) keep the copies from drifting.

The pairing is a design claim, not a measured one.
`hypothesis-driven-analysis` has an archived scenario suite behind it (`skills/hypothesis-driven-analysis/tests/`); `exploratory-data-analysis` has none — its scenarios are authored and no arm has run (`skills/exploratory-data-analysis/tests/scenarios.md`).
No run has yet exercised a handoff between the two.
Per `skills/hypothesis-driven-analysis/tests/scenarios.md` § "Owed measurements as of 2026-08-08", the descriptions that decide which skill activates also rest on zero valid arms.
Treat the routing between them, and the handoff itself, as unverified.
`causal-identification-review` differs: measurement wave 1 (n=1 per cell) has been scored, with the verdict row recorded in `skills/causal-identification-review/tests/scenarios.md` § "Global verdict table".
`decision-analysis` has authored scenarios and no run arms (`skills/decision-analysis/tests/scenarios.md`); treat its routing and its premium as unmeasured.

The measured premiums above count the procedure, not the prose: loading a skill has a fixed context cost the scenario arms do not meter.
As of 2026-08-18 (`wc -w skills/*/SKILL.md skills/*/references/*.md`): `hypothesis-driven-analysis` is 6,263 words plus a 3,180-word ledger template and a 700-word subagent brief; `decision-analysis` is 2,765 plus a 690-word template; `causal-identification-review` is 2,416 plus 492; `exploratory-data-analysis` is 2,415 plus 843.
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

## Installation

### Claude Code

This repository is its own plugin marketplace (`.claude-plugin/marketplace.json`).
Add it, then install the plugin from it:

```
/plugin marketplace add briandconnelly/data-reasoning
/plugin install data-reasoning@data-reasoning
```

### Codex

Add this repository as a marketplace, then install the plugin from it:

```bash
codex plugin marketplace add briandconnelly/data-reasoning
codex plugin add data-reasoning@data-reasoning
```

Start a new Codex session after installation so the bundled skills are available.

## Development

All gates run through [prek](https://github.com/j178/prek):

```bash
prek run --all-files
```

## License

MIT
