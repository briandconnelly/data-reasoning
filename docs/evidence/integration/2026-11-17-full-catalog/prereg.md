# Full-catalog routing and end-to-end handoffs — preregistration

Issue #96.
Written 2026-11-17, before any scored arm ran.
Everything below is fixed before the canaries; any change after them is a dated note at the end, never an edit above it.

## Question

With all four shipped skills discoverable as an ordinary install exposes them, does an agent given an ordinary user prompt take the designed route, keep the evidence boundary across each handoff it actually makes, and finish the user's task — and how does that compare with the same host and model given no plugin?
This is the owed integration suite named in `docs/evidence-status.md` § Owed evidence: every arm before it exercised one skill in isolation or read a prepared record.

## Cells

Each cell reuses a fixture already generated and validated by its own prek hook, so no fixture is built for this suite.
Prompts are ordinary user prompts: none names a skill, a route, or a method.
`{DATA}` is replaced with the staged fixture path.

### I1 — direct lookup

Fixture: `skills/hypothesis-driven-analysis/tests/fixtures/s1-conversion/`.
Prompt: "How many orders in `{DATA}/orders.csv` were placed on 2026-06-10 (UTC)?"
Ground truth: 23 (`grep -c ',2026-06-10T'` on the file).
Designed route: no data-reasoning skill, or a skill loaded and immediately routed out as a direct answer with no ceremony.

### I2 — exploration hands a lead to investigation

Fixture: `skills/hypothesis-driven-analysis/tests/fixtures/s5b-seam/` (the E1 seam fixture; ground truth in `../s5b-seam-ground-truth.md` and `skills/exploratory-data-analysis/tests/scenarios.md` § Seam scenario (E1)).
Prompt: "Here's two months of our API event logs (`{DATA}/events.csv`). Nobody has looked at it closely. Take a look, tell me what's going on, and if anything looks like a real problem, check whether it actually holds up before you tell me it's real."
Ground truth: T, `/export` × `4.2.3`, a constant +20pp error-rate lift that reproduces in any late holdout; D, `enterprise` × `/search`, a decaying lift that reproduces nowhere after 06-10; Q, `apac` rows absent 05-14 to 05-16 with no mechanism.
Designed route: `exploratory-data-analysis` then `hypothesis-driven-analysis`.

### I3 — investigation hands an identification gap to causal review

Fixture: `skills/causal-identification-review/tests/fixtures/cs3-rollout/` (ground truth in `../cs3-rollout-ground-truth.md`).
Prompt: "We rolled out the new checkout flow to the West region on 2026-03-15; East stayed on the old flow. Median checkout completion time in West dropped afterwards. How much faster did the new flow make checkout? I need a number for the Q2 review. Data is in `{DATA}`."
Ground truth: both constructible designs end `assumption-contradicted` — the West before/after design by the concurrent West price promotion, and the West-vs-East difference-in-differences design by a planted differential pre-trend; no design identifies the effect.
Designed route: `hypothesis-driven-analysis` then `causal-identification-review` (a direct `causal-identification-review` activation is recorded as such, not as a failure).

### I4 — an unresolved investigation informs a decision

Fixture: `skills/hypothesis-driven-analysis/tests/fixtures/s15-assist-rollout/` (ground truth in `skills/hypothesis-driven-analysis/tests/scenarios.md` § Scenario 15).
Prompt: Scenario 15's prompt verbatim, with its data line replaced by `{DATA}`.
Ground truth: a single calendar cutover with no holdout, so Assist's effect is not identified; the marginal median improvement reverses within every severity stratum; the responder-hours saving reverses under the same standardization.
Designed route: `hypothesis-driven-analysis`, optionally `causal-identification-review`, then `decision-analysis`.

## Conditions

Two hosts × two conditions × four cells × n=3 = 48 scored arms, plus one canary per cell per host in the plugin condition (8), excluded from scoring.

Both plugin conditions install the runtime tree that `scripts/build-release-tree.py` builds from the measured commit — what an install fetches, without tests, fixtures, or run archives.

- **Claude Code, plugin**: `claude -p` in a fresh temporary directory holding only the staged fixture, `--setting-sources project` (no user settings or user plugins), `--plugin-dir` at the release tree, model `sonnet`.
- **Claude Code, no plugin**: the same, without `--plugin-dir`.
- **Codex, plugin**: `codex exec --json` in a fresh temporary directory; `CODEX_HOME` points at a fresh directory holding only `auth.json`, so no user-global skills, `AGENTS.md`, or config load, and the plugin is installed into it with `codex plugin marketplace add <release tree>` and `codex plugin add data-reasoning@data-reasoning`, as `docs/installing.md` § Local development installs prescribes; Codex's default model, recorded from the run.
- **Codex, no plugin**: the same, with nothing installed.

Each arm's prompt, command, host and model versions, transcript, and final message are archived beside this file as `<cell>-<host>-<condition>-<n>.*`.
The harness is `scripts/run_integration.py`.
Built-in skills each host ships are present in both conditions; they are recorded from the init event, not removed.

## Scoring

The scorer reads the final message and the transcript; the observed route is extracted mechanically (Claude: `Skill` tool calls and reads of a staged `SKILL.md`; Codex: reads of `.agents/skills/*/SKILL.md`), then confirmed by hand.

Per arm:

- **R — route.** The ordered list of data-reasoning skills loaded, and whether it matches the cell's designed route.
- **U — uncertainty survives each handoff.** Scored per actual handoff (a skill loaded after another); no handoff → `n/a`.
  - I2: D is not reported as a confirmed problem; T is called confirmed only on rows held out from where it was found, otherwise reported as a lead; Q is reported as a data-coverage question, not a cause.
  - I3: no number is presented as the flow's causal effect; the answer names the promotion or the pre-trend (or both) as the reason.
  - I4: Assist's causal effect is stated as not identified, the responder-hours saving is not booked as attributable, and the decision is conditioned on that rather than on the headline.
  - I1: `n/a`.
- **C — the user's task is complete.** I1: the answer is 23. I2: T is named as the issue that holds up. I3: the user gets a direct answer to "how much" — that no defensible number exists from this data, and what would be needed. I4: a recommendation on expansion is given and is consistent with U.
- **E — evidence boundary, final message.** Applies to every arm, plugin or not, so the conditions are comparable: the I2–I4 criteria of U, read against the final message regardless of route.

Scorers: the dispatching Claude Code session scores every arm; a second, non-Anthropic model scores every arm blind to condition from the final messages with skill names redacted, through amicus.
Disagreements are reported, not reconciled by vote.

## Reachable outcomes

1. Plugin arms take the designed route and keep E where no-plugin arms do not, on a host: the integration evidence the issue asks for, on that host.
2. Plugin arms take the designed route but E matches no-plugin arms: the skills route correctly but add nothing observable on these cells.
3. Plugin arms skip a designed handoff (one skill, or none) while E holds: the boundary comes from the host or a single skill, and the handoff remains unmeasured in practice.
4. Plugin arms break E where no-plugin arms keep it: a regression attributable to the plugin.
5. Plugin arms fail C where no-plugin arms complete it, on any cell including I1: a task regression attributable to the plugin, whatever R and E show.
6. Plugin arms skip a designed handoff and break E: neither the route nor the boundary holds, whatever the no-plugin arms do.
7. Mixed by host: reported per host; no claim pools Claude Code and Codex.

At n=3 per cell per condition no outcome is a rate; each is reported as counts.

## Limits fixed in advance

- One Claude model and one Codex model; neither generalizes to other models.
- The Codex plugin's hook runs only after a user trusts it in `/hooks`; a headless arm cannot, so Codex plugin arms run the skills without the record-checking hook, and Claude Code arms run with it.
- Scoring by the dispatching session is unblinded; the second scorer is blind to condition only as far as the redaction holds.

## Notes after writing

- 2026-11-17, before any arm: a first design review (`openrouter/google/gemini-3.1-pro-preview` through amicus) could not read this file, which was then uncommitted, and reviewed the request's summary instead; it returned NO-GO. Adopted: n=3 per cell (repository precedent), and a real install in place of `.agents/skills/` staging. Declined: building new multi-stage fixtures — the four prompts each require a handoff to be completed as asked, and whether agents make it is the measurement. The design was re-reviewed with this file committed.
- 2026-11-17, before any arm: the re-review (same model, commit `c6727d6`) returned NO-GO on four findings, all adopted: reachable outcomes 5 (task regression) and 6 (route and boundary both fail) added; the harness now collapses only consecutive repeats of a skill, so a return to an earlier skill stays in the route; the Codex model capture is case-insensitive and is confirmed against the canaries before any scored arm. No further design review was run; the canaries are the next check.
