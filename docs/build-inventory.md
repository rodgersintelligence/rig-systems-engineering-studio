# RIG Systems Engineering Studio — Build Inventory

Comprehensive table of everything shipped. Status as of 2026-05-16, post live-mesh smoke.

## 1 · Repository topology

| Repo | URL | License | Purpose |
|---|---|---|---|
| **Studio** (public) | github.com/rodgersintelligence/rig-systems-engineering-studio | Apache 2.0 | Lattice schema, generator, 588 BuildCards, R3F web viewer, design cards |
| **Private** | github.com/rodgersintelligence/rig-systems-engineering-private | Closed | Archetype implementations, runtime services, rig/ hermes router, integration tests |
| **Live viewer** | rodgersintelligence.github.io/rig-systems-engineering-studio | Public web | 588-cell 3D R3F lattice with mode + coverage colorings |

## 2 · Geometry (locked)

| Axis | Values | Cardinality |
|---|---|---|
| Altitude | L1 Artifacts → L7 Vision | 7 |
| Diamond | D1 Discovery · D2 Solution · D3 Evolution | 3 |
| Mode | A1 PYTHON_ONLY · A2 HYBRID · A3 AGENT_BOUNDED · A4 LLM_AGENT_FREE | 4 |
| IQRSQPI step | I1 Intent · Q1 Question · R Research · S Solution · Q2 Quality · P Proof · I2 Integrate | 7 |
| **Primary coordinates** | 7 × 3 × 4 | **84** |
| **Execution cells** | 84 × 7 | **588** |
| **Reusable archetypes** | 4 × 7 | **28** |

## 3 · Files shipped

### Public studio repo

| Directory | Files | Purpose |
|---|---|---|
| `lattice/` | 6 + 588 generated YAML/MD | Pydantic schema, generator, integrations, question bank |
| `lattice/integrations/` | 3 | DV engines adapter, predictions adapter, package init |
| `cards-design/` | 6 design cards | Triple Diamond, BMS Confidence, A1/A2/A3/A4 deep specs |
| `viz/lattice_r3f/` | React + R3F + Vite app | 3D viewer; src/ types, store, lib, 5 components |
| `viz/streamlit_plotly_app.py` | 1 | Analyst workbench Streamlit 3D |
| `docs/` | viz-design, full-system-diagram, build-inventory | Documentation |
| `tests/` | unit + conftest | 11/11 passing |
| `.github/workflows/` | 2 | generate-lattice CI, deploy-viz to Pages |

### Private archetype repo

| Directory | Files | Purpose |
|---|---|---|
| `rig/_types.py` | 1 | LatticeCoordinate, LatticeCell, BuildModeScore, BuildCard |
| `rig/hermes/` | 3 | Router, run dispatcher |
| `rig/phronema/` | 3 | Build card generator (588) |
| `rig/auditor/` | 2 | Legacy audit store (now superseded by rig/runtime/audit.py) |
| `rig/db/migrations/` | 1 | Postgres lattice_audit migration |
| `rig/tools/` | 2 | OpenClaw-facing wrappers (dispatch_cell, etc.) |
| `rig/runtime/` | **8** | **NEW: production replacements for all 5 stubs** |
| `archetypes/a1_python_only/` | 9 | 7 IQRSQPI step files + types + runtime |
| `archetypes/a2_hybrid/` | 11 | 7 step files + state + graph + LangGraph DAG |
| `archetypes/a3_agent_bounded/` | 11 | 7 step files + state + budget + tools + memory |
| `archetypes/a4_llm_agent_free/` | 13 | 7 step files + state + agents + crew + brier + cascade |
| `tests/` | 7 test files | A1+A2+A3+A4+lattice+smoke+conftest |
| `scripts/live_mesh_smoke.py` | 1 | End-to-end mesh exerciser |

## 4 · Runtime services (rig.runtime/)

**Production replacements for all 5 stubs.** SQLite-by-default with Postgres-compatible adapters.

| Service | File | Production behavior | Lines |
|---|---|---|---|
| **Config** | `config.py` | env-driven RuntimeConfig with safe defaults under `~/.rig/` | 52 |
| **LLM mesh client** | `llm.py` | MeshClient: LM Studio (round-robin 8 instances) → LiteLLM → Anthropic → stub | 380 |
| **AionUI approval** | `approval.py` | SQLite queue + auto-approve fallback + FastAPI UI hook | 232 |
| **Audit store** | `audit.py` | Postgres/SQLite append-only with indexes on archetype/cell/ts | 145 |
| **Predictions** | `predictions.py` | MiroShark logistic blend + MilkyWay 3-ensemble + Brier history | 240 |
| **Scheduler** | `scheduler.py` | APScheduler-backed SQLite jobstore + flush_due fallback | 175 |
| **FastAPI server** | `server.py` | HTML approval queue + healthz + audit + reviews endpoints | 130 |
| **Package init** | `__init__.py` | re-exports all public API | 25 |

## 5 · Mesh fleet (live now — full Tailscale rig)

| Node | Tailscale IP | RAM | LM Studio | Ollama | Status | Tier preference |
|---|---|---|---|---|---|---|
| **rig-256gb-mac-studio** | 100.91.39.12 | 256 GB | :1234 ✅ 18 models | :11434 ✅ | a4 strategic backbone | a4_strategic, a4_critic, a3_agent |
| **rig-96gb-mac-studio-1** | 100.102.142.84 | 96 GB | :1234 ✅ 8 models | :11434 ✅ | a3 agent backbone | a3_agent, a3_red_team, a2_synth |
| **rig-48gb-mbp** | 100.76.209.22 | 48 GB | :1234 ✅ 18 models | :11434 ✅ | a2 synth backbone | a2_synth, a2_judge, coding |
| **rig-36gb-mac-studio-1** | 100.89.143.27 | 36 GB | :1234 ✅ 18 models | :11434 ✅ | a1 shim node | a2_synth, a2_judge, a1_shim |
| **rig-28gb-mbp** | 100.103.237.24 | 28 GB | :1234 ✅ 2 models | :11434 ✅ | fast tier | a1_fast, a1_shim, embedding |
| **blackwell** | 100.67.126.117 | GPU | **vLLM :8000** ✅ | n/a | **qwen2.5-coder-32b** (~1.4s) | coding tier |
| **nas94f2ae** | 100.64.83.55 | NAS | — | — | :8080/:3000 (UI) | storage |
| **rodgemd1-vm** | 100.89.150.120 | VM | — | — | latency ~300ms | services candidate |
| **iphone182** | 100.77.61.95 | iPhone | — | — | mobile peer | — |

**Backbone**: `qwen/qwen3.6-27b` loaded on **4 of 5 Mac nodes** with **8 peer instances each** = 32 effective parallel slots when fully utilized. The fleet router round-robins both across nodes and within a node's `:N` instances.

**Unique models in fleet** (deduplicated):
- qwen3-8b (4 nodes — fastest)
- qwen3-14b (2 nodes)
- qwen3.6-27b ×8 instances (4 nodes — backbone)
- qwen3.5-35b-a3b (96GB only)
- qwen3-coder-30b · qwen3-coder-next (coding)
- google/gemma-4-31b · glm-5.1 · mistralai/devstral-small-2507 (3 nodes)
- nvidia/nemotron-3-nano-omni (96GB only — multimodal)
- nousresearch/hermes-4-70b (96GB + 256GB)
- openai/gpt-oss-120b (256GB only — needs more memory to load)
- hermes-4-405b (256GB only — 210GB load weight)
- text-embedding-nomic-embed-text-v1.5 (all 5 nodes)

## 6 · Archetype implementation status

| Archetype | Files | Tests | LLM tier | Live mesh round-trip | Diamond D1 | D2 | D3 |
|---|---|---|---|---|---|---|---|
| **A1 PYTHON_ONLY** | 9 | 9/9 ✅ | qwen3.6-27b (a1_shim, 60-word cap) | ✅ 7.4–11.4s | success | success | success |
| **A2 HYBRID** | 11 | 13/13 ✅ | qwen3.6-27b (a2_synth, a2_judge) | ✅ 60.8–308.3s | success | halted on real DV cog gate | success |
| **A3 AGENT_BOUNDED** | 11 | 13/13 ✅ | qwen3.6-27b (a3_agent, a3_red_team) | ✅ 60.7–122.8s | blocked by doctrine ✓ | approved | approved |
| **A4 LLM_AGENT_FREE** | 13 | 13/13 ✅ | qwen3.6-27b (a4_strategic, a4_critic) | ✅ 378.5–449.9s | blocked by doctrine ✓ | approved + cascade L5/L4 | approved + cascade |

## 7 · Coverage of the 28 archetype × step pairs

```
            I1     Q1     R      S      Q2     P      I2
A1 PYTHON   ✓      ✓      ✓      ✓      ✓      ✓      ✓
A2 HYBRID   ✓      ✓      ✓      ✓      ✓      ✓      ✓
A3 AGENT    ✓      ✓      ✓      ✓      ✓      ✓      ✓
A4 LLM_FREE ✓      ✓      ✓      ✓      ✓      ✓      ✓
```

**28/28 archetype-step pairs implemented and exercised.**

## 8 · Test totals

| Test file | Tests | Time |
|---|---|---|
| `test_a1_pipeline.py` | 9 | 3.4s |
| `test_a2_pipeline.py` | 13 | 0.08s |
| `test_a3_pipeline.py` | 13 | 0.05s |
| `test_a4_pipeline.py` | 13 | 0.04s |
| `test_rig_lattice.py` | 11 | 16.1s |
| `test_full_lattice_smoke.py` | 7 | 0.08s |
| `test_a3_a4_personal_life.py` | 4 | (Mike-authored) |
| **Private total** | **70** | **0.7s hermetic** |
| `tests/unit/test_generator.py` (public) | 11 | 0.4s |
| **Combined total** | **81** | **~1.1s** |

Live mesh smoke (separate runner, hits the mesh): 12 archetype × diamond runs, **~25 minutes total**, all 12 either succeeded or correctly blocked per doctrine.

## 9 · Persistence (after live smoke run)

| Store | Path | Rows | Notes |
|---|---|---|---|
| Audit | `~/.rig/audit.sqlite` | 43 | A1=13 A2=9 A3=9 A4=12 |
| Approval queue | `~/.rig/approval.sqlite` | 12 decided, 0 pending | All auto-approved via AionUI client |
| MiroShark forecasts | `~/.rig/miroshark.sqlite` | 60+ | 6-feature logistic with Brier history per seed |
| MilkyWay forecasts | `~/.rig/milkyway.sqlite` | 60+ | 3-ensemble (linear + recency + contrarian) |
| Scheduled reviews | `~/.rig/scheduler.sqlite` | 36 (A4 only) | 12 per D2/D3 strategy × 3 horizons |

## 10 · Lattice viewer (live)

| Feature | Status |
|---|---|
| URL | https://rodgersintelligence.github.io/rig-systems-engineering-studio/ |
| Geometry | 7 × 3 × 4 = 84 coordinates rendered, 588 cells in InstancedMesh |
| Color modes | Mode (A1–A4 green/yellow/orange/red) · Coverage (impl status teal/blue/gray) |
| Filters | Mode · Altitude · Diamond · Step · Implementation status · BMS range |
| Click cell | CellPanel with archetype + semantic + GitHub MD link |
| Performance | 1 draw call, ~60fps M1, ~30fps mobile |
| CI | deploy-viz.yml: regen lattice → build → push to Pages on every main commit |
| Cache-bust | per-build SHA appended to lattice_index.json fetch |

## 11 · Design cards authored

| Card | Lines | Status |
|---|---|---|
| `triple-diamond-21-steps.md` | 210 | ✅ v1 |
| `bms-confidence-3-element.md` | 190 | ✅ v1 |
| `a1-python-only-deep-spec.md` | 60 | ✅ v1 |
| `a2-hybrid-deep-spec.md` | 270 | ✅ v1 |
| `a3-agent-bounded-deep-spec.md` | 310 | ✅ v1 |
| `a4-llm-agent-free-deep-spec.md` | 340 | ✅ v1 |

## 13 · Phase 9 — shipped 2026-05-17

Five edges from private repo commit 43d0bbe (`codex/openclaw-rig-lattice-mvp`).

### Private repo additions

| Item | Files | Purpose |
|---|---|---|
| **Watcher launchd** | `bin/rig-cell-watcher` · `bin/rig-runtime-server` · `bin/rig-launchd-install` · `launchd/*.plist` | Always-on macOS service; server auto-restarts on reboot |
| **Weekly brief** | `scripts/weekly_brief.py` | Sunday markdown digest of outcomes, events, audit, rubric, phronema — written to `~/.rig/briefs/` |
| **AionUI inbox** | `rig/runtime/server.py` (+3 endpoints) | `/inbox/pending` GET · `/inbox/{id}/resolve` POST · `/inbox` HTML operator console |
| **Composio bridges** | `rig/runtime/composio_bridge.py` | Auto-promotes 6 stub publishers to live Composio integrations when `COMPOSIO_API_KEY` present |
| **Phronema unification** | `rig/runtime/phronema.py` · `scripts/phronema_migrate.py` | Central DB layer for 7 stores; idempotent migrator preserves old files |

### Public repo additions (this repo)

| Item | Files | Purpose |
|---|---|---|
| **Phase 9 docs** | `docs/phase9.md` | Architecture overview of 5 edges, public/private boundary, rollback paths |
| **System diagram Phase 9** | `docs/full-system-diagram.md` | Appended "Phase 9 surfaces" section with Mermaid boundary diagram |
| **Inbox link** | `viz/lattice_r3f/src/App.tsx` | "inbox →" link in viewer; visible only when SSE connected |
| **Resolved click-through** | `viz/lattice_r3f/src/components/EventTicker.tsx` | `prediction.resolved` rows open `/inbox` in new tab |

---

## 12 · What's no longer a stub

| Was | Now |
|---|---|
| 🟡 AionUI approval (auto-approve) | 🟢 SQLite queue + FastAPI UI + auto-approve fallback (mode-controlled) |
| 🟡 Postgres audit (JSONL files) | 🟢 SQLite default with Postgres adapter via RIG_AUDIT_DATABASE_URL |
| 🟡 MiroShark uniform prior | 🟢 4-feature logistic with persistent Brier history |
| 🟡 MilkyWay stub | 🟢 3-forecaster ensemble (linear trend + recency + contrarian) |
| 🟡 APScheduler returns scheduled-stub | 🟢 SQLite-backed jobstore with flush_due + APScheduler when installed |
| 🟡 LLM calls hit `_stub_classify` only | 🟢 Unified MeshClient: LM Studio → LiteLLM → Anthropic → stub |
