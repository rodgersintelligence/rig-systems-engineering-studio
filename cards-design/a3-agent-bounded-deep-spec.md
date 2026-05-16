# A3 AGENT_BOUNDED Archetype — Deep Spec (7 Files, L4–L6)

**Status**: 🟡 STUB. Mirror the A1 PYTHON_ONLY card shape.
**Cells unlocked**: ~40 (most L5, some L6) on top of A1+A2's ~80 = ~120/147.
**Cost band**: $0.50–$5.00 / invocation. **Run frequency**: a few/day.

---

## Doctrine for A3

1. **Mandatory `policy.requiresApproval()`** — no auto-approval at this mode or above.
2. **Source-per-claim REQUIRED** — Python wrapper enforces, not the prompt.
3. **Mechanism map REQUIRED** — "a strategy without mechanism is a wish."
4. **Hard budget caps**: `max_iterations` + `max_cost_usd` per agent run.
5. **Tool-call audit** — every tool invocation written to Postgres.

---

## File Layout

```
archetypes/a3_agent_bounded/
├── __init__.py
├── _budget.py             # iteration + cost wrappers
├── a3_1_intent.py         # open-ended intent extraction
├── a3_2_question.py       # +2σ deviation enforcement
├── a3_3_research.py       # multi-source agent loop
├── a3_4_solution.py       # 5-candidate tournament
├── a3_5_quality.py        # gate stack + red-team
├── a3_6_proof.py          # falsification charter + mechanism map
└── a3_7_integrate.py      # mandatory human approval (72h timeout)
```

[FILL: 7 step write-ups following A1 deep-spec shape]

---

## Tool Inventory (A3-specific additions)

- Anthropic SDK + OpenAI SDK
- Mem0 (long-term agent memory)
- MCP clients: Firecrawl, Jina, Consensus, arXiv, Phronema
- Promptfoo (eval harness with Brier scoring)

[FILL: full write-up]
