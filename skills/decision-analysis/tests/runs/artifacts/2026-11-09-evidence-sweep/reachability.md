# Reachability: which cells the 2026-11-09 edit reaches

Settled before any arm runs, under `../../../../hypothesis-driven-analysis/tests/PROTOCOL.md` § What owes a rerun: a cell owes arms when its decision point traverses an edited sentence.
The judgement reads each fixture and prompt against the edited prose; "reaches" means the cell's record must take a value the sentence governs, not merely that the agent may read it.
The preregistration for the new cells is `prereg.md` beside this file.

## Edited sentences and template changes

| ID | Edit | Where |
| --- | --- | --- |
| E1 | "Orientation has its home here." and the three sentences after it: the Favored if true slot, r as a ratio of incremental losses, the favored action preferred above the threshold, 1/r when no threshold is stated (replaces "hold wins where posterior odds exceed one over the loss ratio") | `SKILL.md` § Numeric Policy |
| E2 | `dominated` bullet: "no higher … under both states, ties included", and Favored if true takes `none needed` | § Numeric Policy |
| E3 | `evidence-sensitive` bullet | § Numeric Policy |
| E4 | `robust` bullet: "every combination of the stated prior class, the loss range, and the supported likelihood-ratio ranges" | § Numeric Policy |
| E5 | "The prior and loss clauses test their own quantity with each supported likelihood ratio held anywhere within its stated range." | § Numeric Policy |
| E6 | Exact comparisons; a tie is never `robust` (replaces "A tie counts as a flip") | § Numeric Policy |
| E7 | "A range whose endpoints are equal is a point, and a point never flips the action on its own." (replaces "a range that is a single point cannot flip") | § Numeric Policy |
| E8 | The residual: combined inputs reach the threshold with no range flipping alone → `prior-sensitive` | § Numeric Policy |
| E9 | Removed: "v1 sweeps the prior class and the loss range only: a likelihood ratio stated as a range is carried through the posterior range and named in Conditions, never swept on its own." | § Numeric Policy |
| E10 | Decision frame paragraph names "the action the proposition favors" | § The Decide Route |
| E11 | Robustness paragraph adds "or what likelihood-ratio product" | § The Decide Route |
| E12 | Verdict set adds `evidence-sensitive`; the recommendation mapping adds it to `returned to owner` | § The Decide Route |
| T1 | New skeleton slot `- Favored if true:` | template |
| T2 | Crossover skeleton names the likelihood-ratio product | template |
| T3 | Slot notes: `none needed` covers Favored if true; `flips at likelihood ratio` is a Crossover phrase | template § Slot notes |
| K | New checker findings, which reach an agent through the PostToolUse hook and through § Record Delivery's `--final` run | `instruments/check_record.py` |

## Cell by cell

| Cell | Route and decision points | Edits reached | Owes a rerun? |
| --- | --- | --- | --- |
| DA-S1 | decide; no stated threshold, a rounded loss of 10, the point ratio 4.5, no supported prior | E1 (the slot, and the threshold from 1/r), E10, E12 (the closed set it chooses from), T1, T2, T3, K; E7 by its point loss range (the archived post swept `10–10`), a restatement with the same consequence | **yes** — measured and shipping; paid as a control in this wave (pre 1, post 1) |
| DA-S1x | as DA-S1, exact loss | as DA-S1 | **yes** — explicit unpaid debt |
| DA-S2 | decide; unsourceable ratios | E1, E10, E12, T1–T3, K; E3–E5 and E9 if a record keeps a supported ratio range | no arm has ever run (`unrun`); its first run owes nothing extra, and the fixture is still to be generated |
| DA-S3 | decide; no losses, so the loss cap governs | E1, E10, T1 (the slot is required even with no numeric loss), K; E2 on its `dominated` branch; the cap decides before E3–E8 | **yes** — explicit unpaid debt (its row already says the shipped wording post-dates its arms) |
| DA-S4 | decide or decline; a causal proposition | E1, E10, E12, T1–T3 only if a record is written | no arm has ever run; nothing extra owed |
| DA-S5 | voi | none: no edited sentence lies on the VoI route, and the VoI template block is unchanged | no |
| DA-S6 | routing | none | no |
| DA-S7 | voi | none | no |
| DA-S8 | decide; elicited prior range, loss range 2–20, point ratio 4.5; double flip | E1, E5 (vacuous at a point ratio), E10, E12, T1–T3, K; the prior clause decides before E3, E4, E8 | **yes** — paid as a control in this wave (pre 1, post 1); a pre/post difference here is a regression on a control |
| DA-S9 | new | E3, E4, E5, E6, E7, E9, E11, E12, T2, T3 | preregistered (`prereg.md`) |
| DA-S10 | new | E1, E10, T1, and E4 or E8 depending on the swept class | preregistered (`prereg.md`) |
| VoI route generally | voi | none | no |

## Debt this wave leaves unpaid

- DA-S1x and DA-S3 reach E1, E10, T1, and K and are not rerun; their rows must say the shipped wording post-dates their arms.
- DA-S1 and DA-S8 get one pre and one post arm each, enough to catch a gross regression and no more.
- E6 and E8 (the exact tie and the residual) are reached by no fixture in the catalog; they are checker-enforced and unmeasured.
- The checker findings (K) are agent-read through the hook; no arm isolates their wording.
- Codex is unmeasured for every edit.
