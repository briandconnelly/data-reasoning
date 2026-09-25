60 standalone prompts; model ['jev-1.13.0']

hypothesis-driven-analysis catalog -> {'hypothesis-driven-analysis': 14, 'none': 8}
exploratory-data-analysis catalog -> {'exploratory-data-analysis': 15, 'hypothesis-driven-analysis': 6, 'none': 2}
causal-identification-review catalog -> {'hypothesis-driven-analysis': 1, 'causal-identification-review': 6, 'none': 1}
decision-analysis catalog -> {'decision-analysis': 6, 'none': 1}

Ambiguous (confidence < 0.75):
- Scenario 15: Confounded rollout — causal status must match design [hypothesis-driven-analysis]: hypothesis-driven-analysis 0.55, decision-analysis 0.36
- Scenario 11: Mini route [hypothesis-driven-analysis]: none 0.59, hypothesis-driven-analysis 0.41
- DA-S4 — causal-posterior bypass (adversarial) [decision-analysis]: decision-analysis 0.60, hypothesis-driven-analysis 0.30
- T11 — open comparison vs comparative claim (pair) [exploratory-data-analysis]: exploratory-data-analysis 0.65, none 0.26
- Scenario 22: The cheap routes on the wrong rows [hypothesis-driven-analysis]: none 0.67, hypothesis-driven-analysis 0.32
- CS6a — Guardrail: non-activation [causal-identification-review]: none 0.70, causal-identification-review 0.29
- DA-S6 — routing: forecast without a decision (trigger) [decision-analysis]: none 0.70, hypothesis-driven-analysis 0.25
- T6 — prose-document summary [exploratory-data-analysis]: none 0.75, exploratory-data-analysis 0.25
