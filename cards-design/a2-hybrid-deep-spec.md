# A2 HYBRID Archetype — Deep Spec (7 Files, L3–L4)

**Status**: 🟢 v1 authored (2026-05-16).
**Lives at**: L3 Workflows + L4 Systems (`0.45 ≤ BMS < 0.75`).
**Cost band**: $0.01 – $0.30 per invocation. **Run frequency**: 10s–100s / day.
**Cells unlocked**: ~50 on top of A1's ~30 = cumulative ~80/147.

Working implementation reference for **Mode 2 / HYBRID** of the RIG Lattice 28-Archetype map. Covers all 7 IQRSQPI steps with LangGraph as the orchestrator and LLMs *inside* nodes (never in the decision path).

---

## Doctrine for A2

1. **LLM lives INSIDE LangGraph nodes**, not in the orchestrator. The DAG is deterministic; the nodes are bounded LLM calls.
2. **Source-per-claim is MANDATORY** — Python wrapper enforces, not the prompt.
3. **Falsification charter is REQUIRED** (lightweight at A2; full mechanism map at A3).
4. **Approval is risk-classified**: auto-execute low-risk; AionUI for medium-risk; mandatory at high-risk.
5. **Full gate stack runs end-to-end**: Physics → Cognitive → Nature → RIG-L composite. Short-circuit on hard fail.
6. **Diamond awareness**: every step accepts a `diamond: Diamond` parameter that shifts behavior (D1 broad / D2 narrow / D3 forensic).

---

## File Layout

```
archetypes/a2_hybrid/
├── __init__.py
├── _state.py              # LangGraph state schema (Pydantic)
├── _graph.py              # DAG construction + node wiring
├── a2_1_intent.py         # multi-class intent classifier
├── a2_2_question.py       # decompose + coverage judge
├── a2_3_research.py       # parallel research + DV engines
├── a2_4_solution.py       # schema-bound synthesis with retry
├── a2_5_quality.py        # NeMo Guardrails gate stack + predictions
├── a2_6_proof.py          # falsification charter + Phronema graph write
└── a2_7_integrate.py      # risk-classified conditional approval
```

~150 LOC × 9 files ≈ **1,350 lines total** for the HYBRID tier. Weeks 3–5 of the 90-day plan.

---

## A2.1 — Intent

**Does**: Multi-class intent classification with confidence threshold + diamond-aware behavior.
**Tools**: LangGraph + Sonnet + Pydantic.
**Model**: Sonnet (claude-sonnet-4-6).
**Cost**: $0.003 – $0.01 per call.

```python
# a2_1_intent.py
from langgraph.graph import StateGraph
from ._state import HybridState, IntentClassification
from ._diamonds import Diamond

@graph.node
def classify_intent(state: HybridState) -> HybridState:
    result = sonnet.classify(
        text=state.input,
        schema=IntentClassification,
        labels=KNOWN_INTENTS,
        diamond=state.diamond,
    )

    if state.diamond == Diamond.D1_DISCOVERY:
        # D1: capture top-3 candidates with confidence scores
        state.intent_candidates = result.top_k(3)
        state.intent = None  # explicitly broad
    elif state.diamond == Diamond.D2_SOLUTION:
        # D2: narrow to single highest-confidence match
        state.intent = result.label if result.confidence > 0.8 else None
    else:  # D3 Evolution
        # D3: compare against prior baseline intent
        state.intent = result.label
        state.drift_flag = result.label != state.baseline_intent
    return state
```

**Doctrine**: D1 surfaces ambiguity (intentional). D2 demands `confidence > 0.8` or escalates to A3.1. D3 flags drift from baseline.

---

## A2.2 — Question

**Does**: Decompose intent into 3–7 sub-questions with mandatory coverage ≥ 0.85.
**Tools**: Sonnet + Outlines + Haiku coverage judge.
**Model**: Sonnet for generation, Haiku for coverage scoring.
**Cost**: $0.01 – $0.03 per call.

```python
# a2_2_question.py
@graph.node
def decompose(state: HybridState) -> HybridState:
    n_questions = {Diamond.D1_DISCOVERY: 7, Diamond.D2_SOLUTION: 5, Diamond.D3_EVOLUTION: 3}[state.diamond]
    questions = sonnet.generate(
        prompt=DECOMP_PROMPT.format(intent=state.intent, n=n_questions, diamond=state.diamond.value),
        schema=List[SubQuestion],
    )
    coverage = haiku_judge_coverage(state.intent, questions)
    threshold = {Diamond.D1_DISCOVERY: 0.75, Diamond.D2_SOLUTION: 0.85, Diamond.D3_EVOLUTION: 0.90}[state.diamond]
    if coverage < threshold:
        if state.retries < 2:
            state.retries += 1
            return decompose(state)  # retry
        return state.halt(f"coverage {coverage:.2f} < {threshold} after 3 attempts")
    state.questions = questions
    state.dependency_graph = _build_dag(questions)
    return state
```

**Doctrine**: Coverage threshold scales with diamond rigor (D1 lenient, D3 strict). DAG built so research can parallelize.

---

## A2.3 — Research

**Does**: Parallel research with budget caps, source allowlist, AND DV engine push.
**Tools**: LangGraph parallel + Firecrawl/Jina MCP + Phronema + Sonnet + DV adapter.
**Model**: Sonnet.
**Cost**: $0.05 – $0.20 per call.

```python
# a2_3_research.py
from lattice.integrations import dv_engines

@graph.parallel_node
async def research(state: HybridState) -> HybridState:
    sources = ALLOWED_SOURCES_BY_DIAMOND[state.diamond]
    budget = {Diamond.D1_DISCOVERY: 25, Diamond.D2_SOLUTION: 15, Diamond.D3_EVOLUTION: 10}[state.diamond]

    answers = await asyncio.gather(*[
        research_one(q, sources=sources, budget=budget)
        for q in state.questions
    ])
    pack = ResearchPack(answers=answers)

    # DV engine pull on the assembled corpus
    target_sigma = dv_engines.rung_for_diamond(state.diamond)  # D1=+30, D2=+5, D3=0
    pack.dv_packet = dv_engines.score_text(pack.normalized_text())

    # D1 wants HIGH sigma — fail if we couldn't push out
    if state.diamond == Diamond.D1_DISCOVERY and pack.dv_packet["rig_l"] < 5.0:
        return state.halt(f"D1 failed to achieve broad pull: rig_l={pack.dv_packet['rig_l']}")

    state.research = pack
    return state
```

**Doctrine**: D1 fans wide (25 iterations, all source tiers including contrarian). D2 restricts to peer-reviewed + first-party. D3 pulls from baseline-tagged Phronema only. DV engines push aperture deterministically per diamond.

---

## A2.4 — Solution

**Does**: Schema-bound synthesis with retry on validation fail.
**Tools**: LangGraph + Sonnet + Pydantic + Outlines.
**Model**: Sonnet, `temperature=0.3` (D2) / `0.7` (D1) / `0.1` (D3).
**Cost**: $0.02 – $0.08 per call.

```python
# a2_4_solution.py
@graph.node
def synthesize(state: HybridState) -> HybridState:
    temp = {Diamond.D1_DISCOVERY: 0.7, Diamond.D2_SOLUTION: 0.3, Diamond.D3_EVOLUTION: 0.1}[state.diamond]
    n_candidates = {Diamond.D1_DISCOVERY: 5, Diamond.D2_SOLUTION: 1, Diamond.D3_EVOLUTION: 1}[state.diamond]

    candidates = []
    for _ in range(n_candidates):
        candidate = sonnet.generate(
            prompt=SOLUTION_PROMPT.format(research=state.research, diamond=state.diamond.value),
            schema=Solution,
            temperature=temp,
        )
        if not Solution.schema_valid(candidate):
            continue
        candidates.append(candidate)

    if not candidates:
        return state.halt("no candidate survived schema validation")

    state.solution = candidates[0] if len(candidates) == 1 else _tournament(candidates)
    state.candidate_count = len(candidates)
    return state
```

**Doctrine**: D1 generates 5 candidates with tournament selection (broad → narrow within the diamond). D2/D3 generate 1 (narrow). Temperature varies by diamond.

---

## A2.5 — Quality

**Does**: Full Physics → Cognitive → Nature → RIG-L gate stack + MiroFish/MiroShark predictions.
**Tools**: NeMo Guardrails wrapping deterministic gates + lattice predictions adapter.
**Model**: Haiku/Sonnet inside specific engines (e.g., Voltage Reactor).
**Cost**: $0.01 – $0.05 per call.

```python
# a2_5_quality.py
from lattice.integrations import predictions

@graph.node
def gate_stack(state: HybridState) -> HybridState:
    # Gate stack short-circuits on hard fail
    for gate in [physics_gates, cognitive_gates, nature_gates, rig_l]:
        result = gate.evaluate(state.solution, diamond=state.diamond)
        state.gates.append(result)
        if result.short_circuit:
            return state.halt(result.reason)

    # Predictive challenge layer
    horizon = {Diamond.D1_DISCOVERY: "7d", Diamond.D2_SOLUTION: "30d", Diamond.D3_EVOLUTION: "90d"}[state.diamond]
    state.predictions = predictions.predictive_swarm(
        seed=state.solution.body,
        horizon=horizon,
        diamond=state.diamond,
    )

    # D2 hard-fails if MiroFish overall < 8.5
    if state.diamond == Diamond.D2_SOLUTION:
        if state.predictions["mirofish"]["overall"] < 8.5:
            return state.halt(f"MiroFish {state.predictions['mirofish']['overall']:.1f} < 8.5")
    return state
```

**Doctrine**: Gate stack runs in physics → cognitive → nature → rig_l order. Physics gates are HARD BLOCKS (hardware-level constraints). D2 demands MiroFish ≥ 8.5; D3 demands MilkyWay endorsement.

---

## A2.6 — Proof

**Does**: Bind solution to falsification charter + write to Phronema graph.
**Tools**: Pydantic + Postgres (append-only) + Neo4j (capability graph).
**Model**: None (charter is templated; mechanism map is text-injected).
**Cost**: ~$0.

```python
# a2_6_proof.py
@graph.node
def proof(state: HybridState) -> HybridState:
    charter = FalsificationCharter.from_solution(
        state.solution,
        diamond=state.diamond,
        predictions=state.predictions,
    )
    state.proof = ProofPacket(
        charter=charter,
        evidence=state.research.normalized(),
        gates=state.gates,
        predictions=state.predictions,
        graph_node=neo4j.write_node(state.solution),
        diamond=state.diamond,
        signer="a2.hybrid.v1",
    )
    return state
```

**Doctrine**: Charter must include `kill_criteria_dated` for A2. Phronema graph write is the durable record; Postgres holds the audit row.

---

## A2.7 — Integrate

**Does**: Risk-classified conditional approval → dispatch → audit.
**Tools**: AionUI + dispatcher + Postgres append-only audit log.
**Model**: None (decision-routing is rules-based).
**Cost**: ~$0.

```python
# a2_7_integrate.py
@graph.node
async def integrate(state: HybridState) -> HybridState:
    risk = risk_classifier(state.solution, diamond=state.diamond)

    # D1 Discovery: never side-effecting, regardless of action
    if state.diamond == Diamond.D1_DISCOVERY:
        result = ExecutionResult(success=True, kind="audit_only")
    elif risk.requires_human or state.solution.external_action:
        decision = await aionui.request_approval(state.proof, timeout="24h")
        if not decision.approved:
            return state.halt(f"rejected: {decision.reason}")
        result = await dispatcher.execute(state.solution)
    else:
        result = await dispatcher.execute(state.solution)

    audit.record(state.proof, result)
    state.result = result
    return state
```

**Doctrine**: D1 forces `audit_only` (no side effects). D2/D3 use AionUI for medium+ risk; auto-execute for low risk. Every execution writes an audit row.

---

## End-to-End Flow

```python
async def run_a2(payload: InboundPayload, diamond: Diamond) -> ExecutionResult:
    state = HybridState(input=payload, diamond=diamond)
    graph = build_a2_graph()  # classify → decompose → research → synthesize → gate_stack → proof → integrate
    final = await graph.ainvoke(state)
    if final.halted:
        return await escalate_to_a3(payload, reason=final.halt_reason)
    return final.result
```

**One sentence**: `classify_intent → decompose → research (parallel + DV pull) → synthesize (n candidates per diamond) → gate_stack (4 layers + predictions) → proof (charter + Phronema) → integrate (risk-classified approval + audit)`.

---

## Test Surface

Per the parent repo structure:

- `tests/unit/a2/test_a2_<n>_<step>.py` — unit tests per node with mocked LLM calls.
- `tests/integration/a2/test_a2_flow.py` — end-to-end with mocked Sonnet + Haiku.
- `tests/evals/a2/a2_<n>.promptfoo.yaml` — Promptfoo specs for nodes that call LLMs (A2.1, A2.2 coverage judge, A2.4 synthesis, A2.5 cognitive judges).

Promptfoo specs use Brier scoring for prediction calibration tracking.

---

## Tool Inventory (A2-specific additions over A1)

11. **LangGraph** — DAG orchestration with state checkpointing.
12. **Temporal** or **Prefect 3** — durable workflows for >5-minute runs.
13. **NeMo Guardrails** — wraps the gate stack with policy enforcement.

Plus the A1 baseline (Pydantic, Outlines, Postgres+pgvector, LanceDB, Neo4j, Tenacity, APScheduler, Langfuse, AionUI).

---

## Build Checklist (Weeks 3–5)

- [ ] `_state.py` finalized with `HybridState` Pydantic schema.
- [ ] `_graph.py` LangGraph DAG with all 7 nodes wired + retry/halt edges.
- [ ] Coverage judge prompts authored for A2.2 (Haiku rubric).
- [ ] Source allowlist YAMLs per diamond at `intent_maps/<studio>/sources_d1.yaml`, etc.
- [ ] DV adapter integration tested at A2.3 (D1=+30, D2=+5, D3=0).
- [ ] Tournament selection logic at A2.4 (D1 only; n=5).
- [ ] Full gate stack live at A2.5 — physics + cognitive + nature + RIG-L composite.
- [ ] MiroFish hard-fail wired at D2 (threshold 8.5).
- [ ] FalsificationCharter Pydantic schema with `kill_criteria_dated` required.
- [ ] Neo4j capability-graph node write at A2.6.
- [ ] Risk classifier rules table populated (low/medium/high).
- [ ] AionUI approval surface live with risk-class routing.
- [ ] Postgres audit table with proof_packet → action → result rows.
- [ ] Promptfoo evals green for A2.1 / A2.2 / A2.4 / A2.5.
- [ ] Hermes routing: A2 ↔ A1 ↔ A3 escalation paths tested.
