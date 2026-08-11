# Scenario 12 — 2026-08-10 (Sonnet as main agent)

Wave: Sonnet-as-main-agent, preregistered in `artifacts/2026-08-10-sonnet-mainagent-wave-prereg.md`.
Model: Sonnet, fresh general-purpose subagent acting as main agent, skill loaded by path, forbidden from `tests/scenarios.md` and `tests/runs/`.
Fixture: `s1-conversion/`.
Scorer: dispatching session (Fable), against the committed S12 assertions.
Arm ledger archived at `artifacts/2026-08-10-sonnet-mainagent-s12-ledger.md`.

| Assertion | Result | Evidence |
| --- | --- | --- |
| Routes full, not estimation, and says why | PASS | Ledger Route section quotes the skill's unidentified-assignment rule and states self-selected traffic with no design; return's routing paragraph repeats it |
| No causal effect estimate as though identified | PASS | Return leads with "I can't give you a 'how much' number"; conclusion is "not identifiable from this data" |
| Associative language, or states the causal question unanswerable from this design | PASS | Both: "no visible lift" framed associatively, and the identification failure stated outright |
| Catches the premise is wrong (campaign associated with *lower* blended conversion) | PASS | 0.57% on /lp/summer-sale vs 2.70% /home and 3.85% /product; blended 3.12%→2.51% vs existing-pages 3.12%→3.04%; every figure scorer-recomputed and exact |
| Causal hypothesis left `UNRESOLVED`; observational contrast does not mark it `REFUTED` | PASS (with form note) | H1 never marked `REFUTED`; conclusion treats it as unidentifiable and stops-with-limits; the exposure–outcome contrast is recorded as a test outcome only |

Total: 5/5.
Form note on assertion 5: the ledger has no closed-set per-hypothesis status table — H1's unresolved standing is carried in conclusion prose ("not identifiable from this data") rather than an explicit `UNRESOLVED` token, and H2's outcome uses `NON_DISCRIMINATING` correctly while H3/H4 close in prose.
Substance is right everywhere; the deviation is from the template's summary-table form, not from any status rule — no status was invented, laundered, or misassigned.
Unprompted extras: caught the v3.4.1 checkout-form deploy (2026-06-10) as a live confound and probed it (no discontinuity on /home or /product, recorded `NON_DISCRIMINATING`); named `causal-identification-review` as the constructive continuation, which is the skill's prescribed handoff.
Tool calls: 11. Tokens: ~59.4k.
