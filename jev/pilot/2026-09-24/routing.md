60 standalone prompts; model ['jev-1.13.0']

hypothesis-driven-analysis catalog -> {'hypothesis-driven-analysis': 14, 'none': 8}
exploratory-data-analysis catalog -> {'exploratory-data-analysis': 15, 'hypothesis-driven-analysis': 6, 'none': 2}
causal-identification-review catalog -> {'hypothesis-driven-analysis': 1, 'causal-identification-review': 6, 'none': 1}
decision-analysis catalog -> {'decision-analysis': 6, 'none': 1}

Ambiguous (confidence < 0.75):
- Scenario 15: Confounded rollout — causal status must match design [hypothesis-driven-analysis:1870eae9b8ee]: hypothesis-driven-analysis 0.60, decision-analysis 0.32
- DA-S4 — causal-posterior bypass (adversarial) [decision-analysis:e6c687ed7916]: decision-analysis 0.60, hypothesis-driven-analysis 0.29
- Scenario 11: Mini route [hypothesis-driven-analysis:d58f38105e9a]: none 0.63, hypothesis-driven-analysis 0.37
- T11 — open comparison vs comparative claim (pair) [exploratory-data-analysis:d27d996ccbfb]: exploratory-data-analysis 0.65, none 0.27
- Scenario 22: The cheap routes on the wrong rows [hypothesis-driven-analysis:e1bb928500b4]: none 0.67, hypothesis-driven-analysis 0.32
- T6 — prose-document summary [exploratory-data-analysis:843a6338b578]: none 0.71, exploratory-data-analysis 0.29
- CS6a — Guardrail: non-activation [causal-identification-review:a3e8bcd43c5d]: none 0.73, causal-identification-review 0.26
- DA-S6 — routing: forecast without a decision (trigger) [decision-analysis:f8f6e49b9507]: none 0.73, hypothesis-driven-analysis 0.21
- Scenario 22: The cheap routes on the wrong rows [hypothesis-driven-analysis:51a2c7a21fab]: none 0.79, hypothesis-driven-analysis 0.21
