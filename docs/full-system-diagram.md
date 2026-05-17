# RIG Systems Engineering Studio — Full System Diagram

Source-of-truth diagram for the **production** RIG OS. All five runtime stubs
have been replaced with real implementations as of 2026-05-16. Live mesh
end-to-end run confirmed:

- A1 × {D1, D2, D3}: 3/3 success (~10s each)
- A2 × {D1, D2, D3}: 2/3 success (D2 halted on real DV cognitive gate — doctrine working)
- A3 × {D1, D2, D3}: D1 blocked by doctrine, D2 + D3 approved via real AionUI
- A4 × {D1, D2, D3}: D1 blocked, D2 + D3 cascaded to L5 + L4 with 12 Brier predictions each
- **43 audit rows · 36 scheduled reviews · 0 stale approvals**

---

## Layer 1 — Lattice geometry (public)

```mermaid
graph TB
    subgraph "Public — github.com/rodgersintelligence/rig-systems-engineering-studio"
        S1[Altitude<br/>L1..L7<br/>7]
        S2[Diamond<br/>D1 D2 D3<br/>3]
        S3[Mode<br/>A1 A2 A3 A4<br/>4]
        S4[IQRSQPI Step<br/>I1 Q1 R S Q2 P I2<br/>7]
        COORD[84 primary coordinates<br/>= 7 × 3 × 4]
        CELL[588 process-expanded cells<br/>= 84 × 7]
        S1 --> COORD
        S2 --> COORD
        S3 --> COORD
        S4 --> CELL
        COORD --> CELL
        CELL --> GEN[lattice.generator.generate_all<br/>588 BuildCards]
        GEN --> INDEX[viz/lattice_index.json]
        GEN --> CARDS[lattice/cards/L*-D*-A*-*.md ×588]
        INDEX --> R3F[R3F web viewer<br/>rodgersintelligence.github.io]
    end
```

## Layer 2 — Hermes router + archetypes

```mermaid
graph LR
    PAYLOAD[Inbound payload]
    PAYLOAD --> HERMES[rig.hermes.router]
    HERMES --> RESOLVE[resolve coordinate<br/>L×D×A×step]
    RESOLVE --> BMS[compute_bms<br/>raw + adj_failure<br/>+ adj_volume<br/>+ adj_altitude]
    BMS --> MODE{Mode}
    MODE -->|A1 BMS ≥ 0.75| A1[a1_python_only<br/>7 step files]
    MODE -->|A2 0.45–0.74| A2[a2_hybrid<br/>11 step files<br/>LangGraph DAG]
    MODE -->|A3 0.25–0.44| A3[a3_agent_bounded<br/>11 step files<br/>budgeted agents]
    MODE -->|A4 < 0.25| A4[a4_llm_agent_free<br/>12 step files<br/>CrewAI crews]
    A1 --> RUNTIME
    A2 --> RUNTIME
    A3 --> RUNTIME
    A4 --> RUNTIME
    RUNTIME[rig.runtime — 5 services]
```

## Layer 3 — IQRSQPI flow within each archetype

```mermaid
sequenceDiagram
    autonumber
    participant Payload as Inbound
    participant I1 as I1 Intent
    participant Q1 as Q1 Question
    participant R as R Research
    participant S as S Solution
    participant Q2 as Q2 Quality
    participant P as P Proof
    participant I2 as I2 Integrate
    participant Mesh as Mesh (LM Studio)
    participant DV as DV engines (40)
    participant Pred as MiroShark + MilkyWay
    participant AionUI as AionUI approval
    participant Audit as AuditStore (SQLite/Postgres)
    participant Sched as APScheduler reviews

    Payload->>I1: payload + diamond
    I1->>Mesh: chat(tier=a2_synth/a3_agent/a4_strategic)
    Mesh-->>I1: intent JSON
    I1->>Q1: intent
    Q1->>Mesh: decompose into n sub-questions
    Mesh-->>Q1: questions[]
    Q1->>R: questions[]
    R->>DV: score_all(corpus)
    DV-->>R: rig_l + 40-engine packet
    R->>S: ResearchPack
    S->>Mesh: synthesize solution
    Mesh-->>S: Solution body
    S->>Q2: Solution
    Q2->>DV: physics + cognitive + nature + rig_l gates
    DV-->>Q2: gate stack results
    Q2->>Pred: MiroShark + MilkyWay
    Pred-->>Q2: calibrated probabilities + Brier baseline
    Q2->>P: QualityResult
    P->>Sched: schedule_review × 12 (A4)
    P->>I2: ProofPacket
    I2->>AionUI: request_approval(packet)
    AionUI-->>I2: Decision (approved/blocked)
    I2->>Audit: AuditRow append
    I2-->>Payload: ExecutionResult
```

## Layer 4 — Runtime services (private, no stubs)

```mermaid
graph TB
    subgraph RIG_RUNTIME [rig.runtime package — production]
        LLM[llm.py<br/>MeshClient<br/>LM Studio + LiteLLM + Anthropic<br/>round-robin 8 mesh instances]
        APP[approval.py<br/>AionUIClient<br/>SQLite queue + auto-approve fallback]
        AUD[audit.py<br/>AuditStore<br/>Postgres or SQLite append-only]
        PRED[predictions.py<br/>MiroShark + MilkyWay<br/>logistic + 3-forecaster ensemble<br/>Brier history persistence]
        SCH[scheduler.py<br/>ReviewScheduler<br/>APScheduler-backed SQLite jobstore]
        SRV[server.py<br/>FastAPI on :8765<br/>UI + /approval + /audit + /reviews]
        CFG[config.py<br/>RuntimeConfig<br/>env-driven paths under ~/.rig/]
    end

    EXT_MESH[LM Studio :1234<br/>qwen3.6-27b ×8 + 18 models]
    EXT_DB[(SQLite default<br/>or Postgres)]

    LLM --> EXT_MESH
    APP --> EXT_DB
    AUD --> EXT_DB
    PRED --> EXT_DB
    SCH --> EXT_DB
    SRV --> APP
    SRV --> AUD
    SRV --> SCH
    CFG --> LLM
    CFG --> APP
    CFG --> AUD
    CFG --> PRED
    CFG --> SCH
```

## Layer 5 — Tier → mesh routing

```mermaid
graph LR
    subgraph TIERS [Archetype tier → model]
        T1[a1_fast / a1_shim<br/>60-word cap]
        T2[a2_synth / a2_judge]
        T3[a3_agent / a3_red_team]
        T4[a4_strategic / a4_critic]
        TC[coding]
        TE[embedding]
    end

    BACKBONE[qwen/qwen3.6-27b<br/>×8 round-robin instances<br/>27B-param, 8 mesh peers]
    EMB[text-embedding-nomic-embed-text-v1.5]

    T1 --> BACKBONE
    T2 --> BACKBONE
    T3 --> BACKBONE
    T4 --> BACKBONE
    TC --> BACKBONE
    TE --> EMB

    BACKBONE -.fallback.-> LITELLM[LiteLLM :4000]
    BACKBONE -.fallback.-> ANTHROPIC[Anthropic API]
    BACKBONE -.last resort.-> STUB[Deterministic stub<br/>tests + offline]
```

When the backbone (qwen3.6-27b) round-robin hits a transient load-failure on a
peer node, the client retries on a different mesh instance up to 3 times. The
LM Studio mesh is currently the only fully-loaded tier; higher-tier models
(Hermes-4-405b, gpt-oss-120b, etc.) are registered but not preloaded, so the
client transparently falls back to the backbone for those tiers.

## Layer 6 — Cascade: A4 reshapes lower altitudes

```mermaid
graph TB
    A4P[A4 ProofPacket<br/>charter + mechanism + 12 Brier predictions]
    A4P --> A47[a4_7_integrate]
    A47 --> AION[AionUI strategic signoff<br/>no timeout]
    AION -->|approved| CASCADE[cascade_to_lower_altitudes]
    CASCADE --> L5[L5 Programs<br/>score override patches]
    CASCADE --> L4[L4 Systems<br/>score override patches]
    AION -->|approved| BRIER[schedule_review × 12<br/>30d, 90d, 180d, 365d × 3]
    L5 -.regenerates.-> GEN
    L4 -.regenerates.-> GEN
    GEN[generator.py<br/>588 BuildCards]
    BRIER --> SCHED[APScheduler<br/>fires review_prediction at observable_at]
```

---

## How to verify end-to-end yourself

```bash
# 1. Check the mesh
curl -sS http://localhost:1234/v1/models | jq .data[].id

# 2. Health
python3 -c "from rig.runtime import healthcheck; import json; print(json.dumps(healthcheck(), indent=2))"

# 3. Full live smoke (A1+A2+A3+A4 × D1+D2+D3 = 12 runs through the mesh)
RIG_AIONUI_AUTO_APPROVE=1 python3 scripts/live_mesh_smoke.py

# 4. Inspect persisted artifacts
sqlite3 ~/.rig/audit.sqlite "SELECT archetype, count(*) FROM audit_rows GROUP BY archetype;"
sqlite3 ~/.rig/scheduler.sqlite "SELECT status, count(*) FROM scheduled_reviews GROUP BY status;"
sqlite3 ~/.rig/miroshark.sqlite "SELECT count(*) FROM forecasts;"
sqlite3 ~/.rig/approval.sqlite "SELECT state, count(*) FROM approval_requests GROUP BY state;"

# 5. Launch AionUI server
uvicorn rig.runtime.server:app --host 0.0.0.0 --port 8765
# open http://localhost:8765/
```
