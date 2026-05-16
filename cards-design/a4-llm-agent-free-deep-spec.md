# A4 LLM_AGENT_FREE Archetype — Deep Spec (7 Files, L6–L7)

**Status**: 🟡 STUB. Mirror the A1 PYTHON_ONLY card shape.
**Cells unlocked**: ~27 (L7 + rest of L6) on top of A1+A2+A3's ~120 = **147/147 complete**.
**Cost band**: $30–$150 / invocation. **Run frequency**: weekly–quarterly.

---

## Doctrine for A4

1. **Multi-agent crews via CrewAI**, hierarchical process.
2. **Brier prediction set** mandatory — every strategic decision generates a falsifiable prediction.
3. **Mandatory strategic signoff** — human approves before cascade.
4. **OKR cascade to L5/L4** — A4 decisions reshape lower altitudes.
5. **Falsification charter + mechanism map + prediction set** all required.

---

## File Layout

```
archetypes/a4_llm_agent_free/
├── __init__.py
├── _crew.py               # CrewAI configuration + agent definitions
├── a4_1_intent.py         # multi-agent debate (extractor + critic + mechanism checker)
├── a4_2_question.py       # divergent question gen, +5σ minimum deviation
├── a4_3_research.py       # deep research crew, 60+ sources
├── a4_4_solution.py       # 3 strategy archetypes with mechanism + falsifier
├── a4_5_quality.py        # physics short-circuit + 10 rubrics + 20 adversarial attacks
├── a4_6_proof.py          # charter + mechanism map + Brier predictions
└── a4_7_integrate.py      # strategic signoff + cascade to lower altitudes
```

[FILL: 7 step write-ups following A1 deep-spec shape]

---

## Tool Inventory (A4-specific additions)

- CrewAI (multi-agent orchestration)
- OR-Tools / PuLP (constraint solving)
- Promptfoo (Brier prediction tracking)

[FILL: full write-up]
