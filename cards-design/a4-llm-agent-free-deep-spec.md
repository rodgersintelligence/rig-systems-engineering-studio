# A4 LLM_AGENT_FREE Archetype — Deep Spec (7 Files, L6–L7)

**Status**: 🟢 v1 authored (2026-05-16).
**Lives at**: L6 Strategy → L7 Vision (`BMS < 0.25`).
**Cost band**: $30 – $150 per invocation. **Run frequency**: weekly – quarterly.
**Cells unlocked**: ~27 (L7 + rest of L6) → cumulative **147/147 complete**.

Working implementation reference for **Mode 4 / LLM_AGENT_FREE**. Frontier-model multi-agent crews with no auto-execute. This is where the lattice does strategic reasoning — slowly, expensively, with mandatory human signoff and OKR cascade.

---

## Doctrine for A4

1. **Multi-agent crews via CrewAI**, hierarchical process. Each crew has a supervisor and 3–6 specialist agents.
2. **Brier prediction set is MANDATORY** — every strategic decision generates a falsifiable prediction with observable trigger date + threshold.
3. **Strategic signoff is mandatory** (no timeout — open until human decides). AionUI shows charter + mechanism + Brier set + cascade preview.
4. **OKR cascade to L5/L4** — A4 decisions reshape lower-altitude cells. The cascade is computed at A4.7 and dispatched as a list of patch operations against the lattice.
5. **3 strategy archetypes minimum** — the synthesizer must produce 3 distinct strategies (with mechanism + falsifier each) before the judge picks one.
6. **Physics short-circuit** — physics gates run FIRST and HARD-BLOCK without further computation. No point spending $50 on cognitive analysis if physics says NO.
7. **Diamond awareness**: D1 explodes the strategic possibility space (+8σ minimum); D2 binds to mechanism + ships the strategy; D3 measures Brier drift against past predictions and recalibrates.

---

## File Layout

```
archetypes/a4_llm_agent_free/
├── __init__.py
├── _crew.py               # CrewAI crew configurations
├── _agents.py             # specialist agent definitions
├── _brier.py              # prediction set generation + tracking
├── _cascade.py            # OKR cascade engine
├── a4_1_intent.py         # multi-agent debate (extractor + critic + mechanism checker)
├── a4_2_question.py       # divergent question gen, +5σ minimum deviation
├── a4_3_research.py       # deep research crew, 60+ sources
├── a4_4_solution.py       # 3 strategy archetypes with mechanism + falsifier
├── a4_5_quality.py        # physics short-circuit + 10 rubrics + 20 attacks
├── a4_6_proof.py          # charter + mechanism + Brier prediction set
└── a4_7_integrate.py      # strategic signoff + cascade to L5/L4
```

~150 LOC × 12 files ≈ **1,800 lines total** for the LLM_AGENT_FREE tier. Weeks 9–12.

---

## A4.1 — Intent

**Does**: Multi-agent debate to distill strategic prompt into falsifiable strategic objective.
**Tools**: Opus + CrewAI (extractor + critic + mechanism checker).
**Model**: Opus (`claude-opus-4-7`).
**Cost**: $2 – $10.

```python
# a4_1_intent.py
from crewai import Crew, Process
from ._agents import intent_extractor_opus, critic_opus, mechanism_checker_opus

def extract_strategic_intent(prompt: str, diamond: Diamond) -> StrategicIntent:
    # D1: keep all 3 candidate intents (explicit divergence)
    # D2: one intent, mechanism-bound
    # D3: compare against last Brier baseline
    agents = [intent_extractor_opus, critic_opus, mechanism_checker_opus]

    crew = Crew(
        agents=agents,
        process=Process.hierarchical,
        memory=Mem0(namespace=f"a4_intent/{diamond.value}"),
        manager_llm="claude-opus-4-7",
        verbose=True,
    )

    intent = crew.kickoff(
        inputs={"prompt": prompt, "diamond": diamond.value},
        max_iterations=30,
        max_cost_usd=10.0,
    )

    if diamond == Diamond.D3_EVOLUTION:
        baseline = phronema.fetch_strategic_baseline(window_days=365)
        intent.drift_vector = compute_drift(intent, baseline)

    return intent
```

**Doctrine**: Three-agent debate (propose → critique → check mechanism) at Opus rates. No single Opus call — the disagreement IS the signal.

---

## A4.2 — Question

**Does**: Divergent question generation with +5σ minimum deviation enforced by Cognitive Engines 01–20.
**Tools**: Opus + CrewAI + DV engine ladder.
**Model**: Opus.
**Cost**: $3 – $15.

```python
# a4_2_question.py
from lattice.integrations import dv_engines

def frame_strategic_questions(intent: StrategicIntent, diamond: Diamond) -> QuestionSet:
    sigma_target = {
        Diamond.D1_DISCOVERY: 8.0,   # genuinely +8σ contrarian
        Diamond.D2_SOLUTION: 5.0,    # +5σ minimum even when narrowing
        Diamond.D3_EVOLUTION: 3.0,   # +3σ to detect drift
    }[diamond]

    crew = Crew(
        agents=[
            question_explorer_opus,
            contrarian_opus,
            framework_curator_opus,
        ],
        tasks=[
            divergent_questioning(intent),
            contrarian_reframing(intent),
            framework_mapping(intent),
        ],
        process=Process.sequential,
    )

    questions = crew.kickoff(inputs={"intent": intent, "target_sigma": sigma_target})

    # Filter through DV ladder at the diamond's target sigma
    deviated = []
    for q in questions:
        scores = dv_engines.score_text(q.text)
        if scores["rig_l"] >= sigma_target:
            deviated.append(q)
        else:
            # Send back through Cognitive Engine 07 (Voltage) for one more pass
            q_revised = dv_engines.push(q.text, engine_slug="voltage_reactor", target_sigma=sigma_target)
            if q_revised["new_sigma"] >= sigma_target:
                deviated.append(q_revised["text"])

    return QuestionSet(questions=deviated, min_sigma=sigma_target)
```

**Doctrine**: +5σ minimum even at D2. If a question can't be pushed to the sigma target after one revision, it's dropped. The lattice does not ship strategy questions that look like everyone else's.

---

## A4.3 — Research

**Does**: Deep research crew, ≥60 sources, mandatory contrarian source mining.
**Tools**: Opus + CrewAI + Firecrawl + Jina + Consensus + arXiv + Phronema + Neo4j.
**Model**: Opus (supervisor) + Sonnet (workers).
**Cost**: $20 – $100.

```python
# a4_3_research.py
def deep_research(questions: QuestionSet, diamond: Diamond) -> ResearchPack:
    min_sources = {Diamond.D1_DISCOVERY: 80, Diamond.D2_SOLUTION: 60, Diamond.D3_EVOLUTION: 40}[diamond]

    crew = Crew(
        agents=[
            ResearchSupervisor_opus,
            ScraperLearner_1_sonnet,
            ScraperLearner_2_sonnet,
            ScraperLearner_3_sonnet,
            ContrarianSourcer_sonnet,   # forced to find non-consensus views
            FrameworkSynthesizer_opus,
        ],
        process=Process.hierarchical,
        memory=Mem0(namespace=f"a4_research/{diamond.value}"),
        max_cost_usd=50.0,
        max_runtime_hours=4,
    )

    pack = crew.kickoff(
        inputs={
            "questions": questions,
            "min_sources": min_sources,
            "min_contrarian": 10,   # forced minimum
            "require_source_per_claim": True,
        }
    )

    # Cross-source the pack with the full DV ladder
    pack.dv_packet = dv_engines.score_text(pack.normalized_text())

    if pack.source_count < min_sources:
        raise InsufficientResearchError(f"only {pack.source_count} sources < {min_sources}")
    if pack.contrarian_source_count < 10:
        raise InsufficientResearchError("fewer than 10 contrarian sources mined")

    return pack
```

**Doctrine**: ≥80 sources at D1, ≥60 at D2, ≥40 at D3. ≥10 explicitly contrarian. 4-hour runtime budget. $50 spend cap.

---

## A4.4 — Solution

**Does**: 3 strategy archetypes minimum, each with explicit mechanism + falsifier.
**Tools**: Opus + CrewAI (synthesizer + mechanism architect + falsification critic).
**Model**: Opus.
**Cost**: $5 – $25.

```python
# a4_4_solution.py
def synthesize_strategy(research: ResearchPack, diamond: Diamond) -> StrategicSolution:
    crew = Crew(
        agents=[
            strategy_synthesizer_opus,
            mechanism_architect_opus,
            falsification_critic_opus,
        ],
        tasks=[
            generate_archetypes(n=3, diamond=diamond),
            attach_mechanisms,   # MechanismMap with ≥5 nodes, ≥4 edges
            write_falsifiers,    # Brier-trackable predictions per archetype
        ],
        process=Process.sequential,
    )

    archetypes = crew.kickoff(inputs={"research": research, "n_archetypes": 3})

    # Validate each archetype
    for a in archetypes:
        if len(a.mechanism.nodes) < 5 or len(a.mechanism.edges) < 4:
            raise StrategyValidationError(f"archetype {a.name} mechanism too sparse")
        if not a.falsifier or not a.falsifier.observable_at:
            raise StrategyValidationError(f"archetype {a.name} lacks dated falsifier")

    # D1: keep all 3. D2: tournament-select. D3: pick the one closest to baseline + patch.
    if diamond == Diamond.D1_DISCOVERY:
        return StrategicSolution(archetypes=archetypes, selected=None)
    if diamond == Diamond.D2_SOLUTION:
        winner = opus_judge.tournament(archetypes, rubric=STRATEGY_RUBRIC)
        return StrategicSolution(archetypes=archetypes, selected=winner)
    # D3 Evolution
    closest = min(archetypes, key=lambda a: drift_distance(a, baseline))
    patched = apply_recalibration(closest, baseline.drift_vector)
    return StrategicSolution(archetypes=archetypes, selected=patched)
```

**Doctrine**: 3 archetypes minimum. Each must have mechanism (≥5 nodes, ≥4 edges) and dated falsifier. D1 keeps all 3 as alternates; D2 picks one; D3 patches the closest match.

---

## A4.5 — Quality

**Does**: Physics short-circuit + 10 rubrics + 20 adversarial attacks + Brier eval.
**Tools**: NeMo Guardrails + Opus red-team + Sonnet rubric judges + Promptfoo + lattice predictions.
**Model**: Opus (red-team), Sonnet (rubrics).
**Cost**: $5 – $20.

```python
# a4_5_quality.py
from lattice.integrations import predictions

def quality(strategy: StrategicSolution, diamond: Diamond) -> QualityResult:
    # 1. Physics gates FIRST — hard short-circuit before spending on cognitive
    physics = run_physics_gates(strategy.selected, diamond=diamond)
    if not physics.passed:
        return FAIL_SHORTCIRCUIT(physics)

    # 2. 10 rubrics in parallel (Sonnet)
    rubrics = parallel_judge(
        strategy.selected,
        judges=[
            mechanism_clarity_judge,
            falsifier_quality_judge,
            internal_consistency_judge,
            stakeholder_coverage_judge,
            contrarian_resilience_judge,
            time_horizon_judge,
            blast_radius_judge,
            reversibility_judge,
            measurement_judge,
            cascade_impact_judge,
        ],
    )

    # 3. 20 adversarial attacks (Opus)
    red_team = opus_red_team.adversarial_attack(strategy.selected, n_modes=20)

    # 4. Predictive challenge with MilkyWay (long-horizon)
    pred_packet = predictions.predictive_swarm(
        seed=strategy.selected.body,
        horizon="365d",
        diamond=diamond,
    )

    # D2 hard-fails if rubric mean < 8 or any rubric < 5 or red-team breaks > 2
    if diamond == Diamond.D2_SOLUTION:
        if rubrics.mean < 8.0:
            return FAIL("rubric_mean")
        if rubrics.min < 5.0:
            return FAIL("rubric_floor")
        if red_team.breaks > 2:
            return FAIL("red_team")
        if not pred_packet["milkyway"].get("endorses_strategy", False):
            return FAIL("milkyway_endorsement")

    return PASS(physics=physics, rubrics=rubrics, red_team=red_team, predictions=pred_packet)
```

**Doctrine**: Physics first (cheap hard gates). Then 10 rubrics in parallel. Then 20 red-team attacks. Then MilkyWay long-horizon prediction. D2 must hit rubric mean ≥ 8.0, floor ≥ 5.0, red-team breaks ≤ 2, MilkyWay endorses.

---

## A4.6 — Proof

**Does**: Falsification charter + full mechanism map + Brier prediction set.
**Tools**: Opus + Pydantic + Neo4j + Phronema audit + Promptfoo prediction tracking.
**Model**: Opus.
**Cost**: $2 – $8.

```python
# a4_6_proof.py
from ._brier import generate_brier_set

def proof(strategy: StrategicSolution, quality: QualityResult, diamond: Diamond) -> ProofPacket:
    charter = opus.generate(CHARTER_PROMPT, strategy=strategy, schema=FalsificationCharter)
    mechanism = opus.generate(MECHANISM_PROMPT, strategy=strategy, schema=MechanismMap)
    predictions_set = generate_brier_set(
        strategy=strategy,
        horizon_days=[30, 90, 180, 365],
        n_predictions_per_horizon=3,
        diamond=diamond,
    )

    # Schedule Brier reviews on each prediction's observable_at date
    for pred in predictions_set.predictions:
        apscheduler.add_job(
            review_prediction,
            run_date=pred.observable_at,
            args=[pred.id],
        )

    return ProofPacket(
        charter=charter,
        mechanism=mechanism,
        predictions=predictions_set,
        evidence=strategy.research.normalized(),
        physics_passed=quality.physics.passed,
        rubric_summary=quality.rubrics.summary(),
        red_team_summary=quality.red_team.summary(),
        graph_node=neo4j.write_strategic_node(strategy, mechanism=mechanism),
        diamond=diamond,
        signer="a4.llm_agent_free.v1",
        cost_usd=quality.total_cost + research.cost + intent.cost,
    )
```

**Doctrine**: 12 Brier predictions minimum (4 horizons × 3 predictions). Each gets a scheduled review on its `observable_at` date — APScheduler picks them up and fires D3 Evolution flow.

---

## A4.7 — Integrate

**Does**: Strategic signoff → cascade OKRs to L5/L4 lower-altitude cells.
**Tools**: AionUI + audit log + APScheduler + cascade engine.
**Model**: None (decision is human).
**Cost**: ~$0.

```python
# a4_7_integrate.py
from ._cascade import cascade_to_lower_altitudes

async def integrate(packet: ProofPacket) -> Decision:
    # D1 Discovery: never dispatched. Generates proof + Brier set; that's it.
    if packet.diamond == Diamond.D1_DISCOVERY:
        audit.record(packet, decision=None, kind="strategic_discovery")
        return BLOCKED("D1 strategic exploration — no dispatch by doctrine")

    decision = await aionui.request_strategic_signoff(
        packet,
        show_charter=True,
        show_mechanism_map=True,
        show_brier_predictions=True,
        show_cascade_preview=True,   # NEW: shows which L5/L4 cells will be patched
        timeout=None,                # NO TIMEOUT — open until human decides
    )
    audit.record(packet, decision)

    if not decision.approved:
        return BLOCKED(decision.reason)

    # Cascade: this is what makes A4 worth its cost band.
    # An approved strategy reshapes lower-altitude cells.
    cascade_result = await cascade_to_lower_altitudes(
        packet,
        target_altitudes=["L5_PROGRAMS", "L4_SYSTEMS"],
        approval_signer=decision.signer,
    )

    # Schedule the 12 Brier reviews
    for pred in packet.predictions.predictions:
        scheduler.schedule_prediction_review(pred)

    return Decision(
        approved=True,
        signer=decision.signer,
        cascade=cascade_result,
        predictions_scheduled=len(packet.predictions.predictions),
    )
```

**Doctrine**: No timeout on signoff (it's a strategic decision — let humans take their time). Cascade engine patches L5/L4 cells based on the strategy. 12 Brier reviews are scheduled. The lattice itself updates as a result of the approval.

---

## End-to-End Flow

```python
async def run_a4(prompt: str, diamond: Diamond) -> Decision:
    intent = extract_strategic_intent(prompt, diamond=diamond)
    questions = frame_strategic_questions(intent, diamond=diamond)
    research = await deep_research(questions, diamond=diamond)
    strategy = synthesize_strategy(research, diamond=diamond)
    quality_result = quality(strategy, diamond=diamond)
    if not quality_result.passed:
        # A4 cannot escalate up — at the top of the lattice
        return BLOCKED(f"quality.{quality_result.failed_layer}")
    packet = proof(strategy, quality_result, diamond=diamond)
    return await integrate(packet)
```

**One sentence**: `extract_strategic_intent (3-agent Opus debate) → frame_strategic_questions (+5σ min via DV ladder) → deep_research (hierarchical crew, 60+ sources, ≥10 contrarian) → synthesize_strategy (3 archetypes with mechanism + falsifier) → quality (physics short-circuit → 10 rubrics → 20 attacks → MilkyWay) → proof (charter + mechanism + 12 Brier predictions, scheduled reviews) → integrate (no-timeout signoff + L5/L4 cascade)`.

---

## Test Surface

- `tests/unit/a4/test_a4_<n>.py` — Mock CrewAI crews, test budget caps, source-per-claim, mechanism sparsity validation.
- `tests/integration/a4/test_a4_flow.py` — End-to-end with stubbed Opus/Sonnet; verify cascade patch list is generated and `aionui.request_strategic_signoff` is called with `timeout=None`.
- `tests/evals/a4/a4_<n>.promptfoo.yaml` — Brier-scored evals on intent debate, framing sigma, strategy quality.
- `tests/cascade/test_cascade.py` — Verify cascade engine correctly identifies dependent L5/L4 cells and produces a valid patch list.
- `tests/brier/test_review_schedule.py` — Verify APScheduler picks up prediction reviews on the right dates.

---

## Tool Inventory (A4-specific additions over A1+A2+A3)

18. **CrewAI** — multi-agent orchestration with hierarchical + sequential processes.
19. **OR-Tools / PuLP** — constraint solving when synthesis has trade-off math (capacity allocation, budget under constraints).

---

## Build Checklist (Weeks 9–12)

- [ ] `_crew.py` CrewAI crew factories per A4 step.
- [ ] `_agents.py` specialist agent definitions (intent_extractor_opus, critic_opus, mechanism_checker_opus, etc.).
- [ ] `_brier.py` prediction set generator with `observable_at` dates per prediction.
- [ ] `_cascade.py` cascade engine: given an A4 ProofPacket, compute the L5/L4 cell patches.
- [ ] Strategic intent extraction with 3-agent debate (cost cap $10).
- [ ] DV sigma enforcement at A4.2 (D1=+8, D2=+5, D3=+3).
- [ ] Deep research crew with 6 specialists, 4-hour runtime, $50 budget.
- [ ] 3-archetype synthesis with mechanism (≥5 nodes, ≥4 edges) and dated falsifiers.
- [ ] Quality: physics short-circuit → 10 rubrics → 20 attacks → MilkyWay long-horizon.
- [ ] D2 hard-fail thresholds wired (rubric mean ≥ 8, floor ≥ 5, red-team breaks ≤ 2).
- [ ] 12 Brier predictions per strategy (4 horizons × 3).
- [ ] APScheduler jobs scheduled for each prediction's review date.
- [ ] AionUI strategic signoff surface with cascade preview (no timeout).
- [ ] Cascade engine wired to patch L5/L4 cells in the lattice.
- [ ] Postgres + Neo4j audit rows tying strategy → cascade patches.
- [ ] Promptfoo evals green at full Opus cost band (single canonical run).
- [ ] D1 strategic-discovery dispatch-block doctrine enforced at A4.7.
- [ ] Quarterly Brier dashboard live; drift triggers automatic D3 Evolution flow.

---

## What this archetype unlocks

When A4 ships, the lattice is **complete** — 147/147 cells reachable. The full RIG OS doctrine is implementable:

- L7 Vision decisions cascade through L6 Strategy → L5 Programs → L4 Systems → L3 Workflows → L2 Tasks → L1 Artifacts deterministically.
- Every cell has a Build Card with a generator-known archetype, gates, and audit path.
- Every strategic claim has a Brier-scored prediction with a scheduled review.
- Drift triggers D3 Evolution at every altitude automatically.

This is the doctrine: **exploratory while building, deterministic while running, never both at once** — applied to a 3,087-cell architectural lattice that knows what it is, what it isn't, and what it's about to become.
