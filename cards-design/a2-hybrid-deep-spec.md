# A2 HYBRID Archetype — Deep Spec (7 Files, L3–L4)

**Status**: 🟡 STUB. Mirror the A1 PYTHON_ONLY card shape.
**Cells unlocked**: ~50 (most L3, L4) on top of A1's ~30 = ~80/147.
**Cost band**: $0.01–$0.30 / invocation. **Run frequency**: 10s–100s/day.

---

## Doctrine for A2

1. **LLM lives INSIDE LangGraph nodes**, not in the orchestrator.
2. **Source-per-claim is mandatory at A2**, enforced by Python wrapper.
3. **Falsification charter required** (lightweight version, full version at A3).
4. **Approval is risk-classified conditional** (auto for low-risk, AionUI for medium+).
5. **Gate stack runs end-to-end**: Physics → Cognitive → Nature → RIG-L.

---

## File Layout

```
archetypes/a2_hybrid/
├── __init__.py
├── _state.py              # LangGraph state schema
├── a2_1_intent.py         # multi-class intent + Sonnet
├── a2_2_question.py       # decompose + Haiku coverage judge
├── a2_3_research.py       # parallel research with budget caps
├── a2_4_solution.py       # schema-bound synthesis with retry
├── a2_5_quality.py        # Physics→Cog→Nature→RIG-L gate stack
├── a2_6_proof.py          # Falsification charter + Phronema write
└── a2_7_integrate.py      # risk-classified conditional approval
```

---

## A2.1 — Intent

**Does**: Multi-class intent classification with confidence threshold.
**Tools**: LangGraph + Sonnet + Pydantic. **Model**: Sonnet. **Cost**: $0.003–$0.01.

```python
@graph.node
def classify_intent(state: State) -> State:
    result = sonnet.classify(text=state.input, schema=IntentClassification, labels=KNOWN_INTENTS)
    state.intent = result.label if result.confidence > 0.8 else None
    return state
```

[FILL: when to escalate, retry policy, schema details]

---

## A2.2 — Question

**Does**: Decompose intent into 3–7 sub-questions with coverage check.
**Tools**: Sonnet + Outlines + Haiku coverage judge. **Cost**: $0.01–$0.03.

```python
@graph.node
def decompose(state: State) -> State:
    questions = sonnet.generate(prompt=DECOMP_PROMPT, schema=List[SubQuestion])
    coverage = haiku_judge_coverage(state.intent, questions)
    if coverage < 0.85: return state.retry()
    state.questions = questions
    return state
```

[FILL: coverage rubric, retry budget, failure mode]

---

## A2.3 — Research

[FILL: full A1-style write-up for each step]

---

## A2.4 — Solution
[FILL]

## A2.5 — Quality
[FILL]

## A2.6 — Proof
[FILL]

## A2.7 — Integrate
[FILL]

---

## End-to-End Flow
[FILL: one-sentence shape + LangGraph DAG diagram]

## Test Surface
[FILL]

## Build Checklist (Weeks 3–5)
[FILL]
