# Triple Diamond 21-Step Process — Y-Axis Source of Truth

**Status**: 🟢 v1 authored (2026-05-16).
**Drives**: `lattice/step_semantics.py` — every BuildCard's `diamond_step_semantic` field.

The Y-axis of the 3D lattice is **21 wide** because each of the 3 diamonds runs its own full 7-step IQRSQPI process. The diamonds are not modifiers; they are **three distinct passes** with distinct semantics per step.

| Diamond | Posture | Mechanism Clarity | Sigma Target |
|---|---|---|---|
| **D1 Discovery** | Divergent — open the problem space | Low (intentionally) | ≥ +3σ |
| **D2 Solution** | Convergent — bind to mechanism, ship | High (mandatory) | +0–2σ |
| **D3 Evolution** | Forensic — measure drift, recalibrate | High (must reproduce) | n/a (regression) |

Each entry below has: **Name**, **Purpose** (one sentence), **Inputs** (structured), **Outputs** (structured), **Gates that fire**.

---

## D1 — DISCOVERY

Goal: surface the widest viable possibility space *before* anyone commits to a mechanism. Anything that increases coverage wins; anything that prematurely converges loses.

### D1.I1 — Divergent Intent Capture

- **Purpose**: Treat the incoming signal as a vector of possibilities, not a known intent. Deterministic matchers are deliberately bypassed at D1.
- **Inputs**: `RawSignal { multimodal: any, user_persona: Persona, ambient_context: dict }`
- **Outputs**: `IntentSpace { candidate_intents: list[Intent], abandoned_paths: list[str], stakeholder_map: dict }`
- **Gates**: `cognitive_05` (signal-to-noise lift), `nature_22` (diversity check)

### D1.Q1 — Open-Frame Questioning

- **Purpose**: Generate the widest set of reasonable questions before any narrowing. Each question must score ≥ +3σ on deviation from baseline framings.
- **Inputs**: `IntentSpace`, prior framings from Phronema graph
- **Outputs**: `QuestionSwarm { questions: list[Question], coverage_score: float, deviation_distribution: list[float] }`
- **Gates**: `cognitive_07` (Voltage Reactor), `physics_31` (uncertainty principle)

### D1.R — Wide-Aperture Research

- **Purpose**: Source diversity > depth. Pull from contrarian sources, edge-case datasets, deprecated frameworks. Source allowlist is intentionally permissive here.
- **Inputs**: `QuestionSwarm`, `SourceAllowlist.D1_permissive`
- **Outputs**: `ResearchManifold { sources: list[Source], conflicting_evidence: list[ClaimPair], unresolved_questions: list[str] }`
- **Gates**: `nature_24` (predator-prey diversity), `anti_slop`

### D1.S — Possibility Sketching

- **Purpose**: Generate 5–10 distinct solution shapes without committing to mechanism. Each must be falsifiable, but not yet mechanism-bound.
- **Inputs**: `ResearchManifold`
- **Outputs**: `SolutionField { sketches: list[Sketch], mechanism_hypotheses: list[str], explicit_unknowns: list[str] }`
- **Gates**: `cognitive_01` (Rupture — kill orthodox sketches), `rig_l_lite`

### D1.Q2 — Coverage Check

- **Purpose**: Did we explore the actual problem space, or just the comfortable region? Adversarial perspective sweep + anti-slop probing.
- **Inputs**: `SolutionField`, `IntentSpace.stakeholder_map`
- **Outputs**: `CoverageReport { covered_perspectives: list[str], missed_perspectives: list[str], confidence: float }`
- **Gates**: `anti_slop`, `cognitive_12` (perspective adversarial)

### D1.P — Exploration Receipt

- **Purpose**: Audit-grade record of what was explored AND what was deliberately abandoned. Future agents inherit your dead ends so they don't relitigate them.
- **Inputs**: All prior D1 artifacts
- **Outputs**: `ExplorationProofPacket { explored: list[Path], abandoned: list[(Path, reason)], hash: str, signer: AgentID }`
- **Gates**: `claim_validator`, `anti_slop`

### D1.I2 — Frame Selection

- **Purpose**: Narrow the SolutionField to 1–3 frames that will be carried forward into D2. Human-in-loop at L5+; deterministic shortlist at L1–L3.
- **Inputs**: `SolutionField`, `CoverageReport`
- **Outputs**: `SelectedFrames { primary: Frame, alternates: list[Frame], rejection_log: list[(Frame, reason)] }`
- **Gates**: `AionUI` (conditional, mandatory at L5+), `rig_l_composite`

---

## D2 — SOLUTION

Goal: convert selected frames into shipped, mechanism-bound, falsifiable artifacts with full audit lineage. *A strategy without mechanism is a wish.*

### D2.I1 — Mechanism-Bound Intent

- **Purpose**: Convert each SelectedFrame into an intent with explicit mechanism. No mechanism, no progress past this step.
- **Inputs**: `SelectedFrames`, `MechanismLibrary`
- **Outputs**: `MechanismBoundIntent { intent: Intent, mechanism: MechanismGraph, falsifier_template: str }`
- **Gates**: `cognitive_10` (Mechanism Clarity — hard gate), `rig_l`

### D2.Q1 — Decomposed Sub-Questions

- **Purpose**: Break the mechanism-bound intent into 3–7 sub-questions with a coverage guarantee ≥ 0.85. Dependency-aware so research can parallelize.
- **Inputs**: `MechanismBoundIntent`
- **Outputs**: `SubQuestionSet { questions: list[SubQ], coverage: float, dependency_graph: DAG }`
- **Gates**: `cognitive_07_voltage`, `anti_slop`

### D2.R — Source-Per-Claim Research

- **Purpose**: Every claim that will appear in the solution must be backed by ≥1 source. Python wrapper enforces — never the prompt.
- **Inputs**: `SubQuestionSet`, `SourceAllowlist.D2_restricted` (peer-reviewed + first-party)
- **Outputs**: `ResearchPack { rows: list[ClaimWithSources], unsourced_claims: [] }`  *(must be empty)*
- **Gates**: `claim_validator` (hard), `source_per_claim`, `anti_slop`

### D2.S — Schema-Bound Synthesis

- **Purpose**: Generate one solution that fully types against the contract. Outlines + Pydantic + retry on schema fail.
- **Inputs**: `ResearchPack`, `MechanismBoundIntent`
- **Outputs**: `Solution { body: str, structured_fields: dict, sources: list[Source] }`
- **Gates**: Pydantic schema, `cognitive_07` (Voltage)

### D2.Q2 — Gate Stack Run

- **Purpose**: Physics → Cognitive → Nature → RIG-L composite. Short-circuit on any hard failure; diagnostic payload returned (not raised).
- **Inputs**: `Solution`
- **Outputs**: `GateResults { passed: bool, results: list[GateResult], short_circuit_at: Optional[str] }`
- **Gates**: `physics_31..40`, `cognitive_01..20`, `nature_21..30`, `rig_l_composite`

### D2.P — Falsification Charter

- **Purpose**: Bind the solution to a written falsifier. *How will we know we were wrong?* Generates Brier-trackable predictions.
- **Inputs**: `Solution`, `GateResults`
- **Outputs**: `FalsificationCharter { hypothesis: str, observable_predictions: list[BrierPrediction], rollback_trigger: str }`
- **Gates**: `cognitive_10` (Mechanism), `claim_validator`

### D2.I2 — Dispatch + Audit

- **Purpose**: Risk-classified approval (conditional at A1/A2, mandatory at A3+) → execute → write audit row tying ProofPacket → Action → Result.
- **Inputs**: `FalsificationCharter`, `Solution`, `Action`
- **Outputs**: `ExecutionResult`, `AuditRow`
- **Gates**: `AionUI` (conditional/mandatory by mode), `audit_appendonly`

---

## D3 — EVOLUTION

Goal: detect drift, identify the failure mode, patch the cell, prove the patch holds, and cascade the score change. Forensic posture — reproduce the past exactly, then change it surgically.

### D3.I1 — Drift-Triggered Intent

- **Purpose**: A drift event (Brier > 0.15, rollback > 5%, or scheduled 90-day re-score) generates an intent to investigate what changed in the cell's behavior.
- **Inputs**: `DriftSignal { metric: str, observed: float, threshold: float, cell_id: str, triggered_at: datetime }`
- **Outputs**: `ForensicIntent { affected_cells: list[str], hypotheses: list[DriftHypothesis] }`
- **Gates**: `physics_33` (Phase Transition detection), `nature_22`

### D3.Q1 — What Broke / Why Now

- **Purpose**: Decompose the drift into testable failure-mode questions. Time-windowed comparison to the cell's prior baseline (90d / 180d / 365d).
- **Inputs**: `ForensicIntent`, baseline cell state from Phronema
- **Outputs**: `FailureModeQuestions { questions: list[Q], time_window: tuple, baseline_ref: str }`
- **Gates**: `cognitive_12`, `anti_slop`

### D3.R — Brier Score + Rollback Forensics

- **Purpose**: Pull prediction history, rollback logs, and audit rows. Compute current vs. baseline calibration.
- **Inputs**: `FailureModeQuestions`, `FalsificationCharter` from prior D2.P, audit log
- **Outputs**: `ForensicPack { brier_now: float, brier_baseline: float, rollback_events: list, regression_class: str }`
- **Gates**: `claim_validator`, `source_per_claim`

### D3.S — Recalibration Patch

- **Purpose**: Minimum-diff change to restore the cell to its target performance. Could be a criterion-score override, a prior adjustment, or a mode demotion.
- **Inputs**: `ForensicPack`
- **Outputs**: `RecalibrationPatch { criterion_overrides: dict, mode_change: Optional[BuildMode], rationale: str }`
- **Gates**: `cognitive_05`, `rig_l_lite`

### D3.Q2 — Regression Check

- **Purpose**: Replay the last 30 days of invocations against the patched cell. Confirm Brier improves without breaking adjacent cells in the lattice.
- **Inputs**: `RecalibrationPatch`, replay corpus
- **Outputs**: `RegressionReport { brier_after: float, adjacent_cell_impact: list[Pair], pass: bool }`
- **Gates**: `physics_31`, `anti_slop`, `rig_l`

### D3.P — Re-Score Receipt

- **Purpose**: Append-only record of the score change. Includes prior values, patch reason, trigger source, and proof of regression check.
- **Inputs**: `RecalibrationPatch`, `RegressionReport`
- **Outputs**: `ReScoreProofPacket { cell_id, prior_scores, new_scores, hash, signer, trigger }`
- **Gates**: `claim_validator`, `audit_appendonly`

### D3.I2 — Cascade Update

- **Purpose**: Propagate the score change to dependent cells (same altitude, same step, related diamonds). Regenerate downstream cards and refresh the 3D viz.
- **Inputs**: `ReScoreProofPacket`
- **Outputs**: `CascadeResult { regenerated_cells: list[str], viz_refresh_url: str, downstream_alerts: list }`
- **Gates**: `AionUI` (mandatory at L5+), `rig_l_composite`

---

## The shape, in one sentence

**D1 opens** the possibility space and proves what was explored; **D2 binds** the selected frame to a mechanism and ships it with a falsifier; **D3 measures** drift, patches the cell, and cascades the change — and all three diamonds use the same 7-step IQRSQPI rhythm so every cell in the 3,087-cell lattice has a single deterministic position.

## After authoring

1. Run `python3 -m lattice.generator` to regenerate all 3,087 cards with these semantics.
2. Open `viz/streamlit_plotly_app.py` to see them rendered.
3. Update individual entries here; the generator re-renders everything in one shot.
