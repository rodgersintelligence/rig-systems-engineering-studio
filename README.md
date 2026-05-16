# RIG Systems Engineering Studio

> A 7 × 21 × 21 = **3,087-cell lattice** that maps every RIG OS decision context to a deterministic Build Card and one of 28 implementation archetypes.

[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python 3.12+](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)

## What this is

The lattice is the architectural source of truth for the RIG operating system. Every cell answers: **"At this altitude, in this diamond-step, with this confidence contribution, what tool / approach / archetype do I use?"**

### Three axes

| Axis | Meaning | Size |
|---|---|---|
| **X — Altitude** | `L1 Artifacts → L7 Vision` — granularity of the decision | 7 |
| **Y — Triple Diamond × IQRSQPI** | 3 diamonds (Discovery / Solution / Evolution) × 7 IQRSQPI steps (Intent, Question, Research, Solution, Quality, Proof, Integrate) | 21 |
| **Z — BMS Confidence × IQRSQPI** | 3 confidence contributors (RAW, ADJ_failure, ADJ_volume) × 7 IQRSQPI steps | 21 |

**Total cells**: `7 × 21 × 21 = 3,087`.

### Four build modes (collapsed from 3,087 cells)

| Mode | BMS Range | Lives at | Cost band |
|---|---|---|---|
| `PYTHON_ONLY` | ≥ 0.75 | L1–L2 | $0 – $0.001 |
| `HYBRID` | 0.45–0.74 | L3–L4 | $0.01 – $0.30 |
| `AGENT_BOUNDED` | 0.25–0.44 | L4–L6 | $0.50 – $5.00 |
| `LLM_AGENT_FREE` | < 0.25 | L6–L7 | $30 – $150 |

Each mode × 7 IQRSQPI steps = **28 archetype implementations** that cover all 3,087 cells.

## Quick start

```bash
# Install
pip install -e ".[viz]"

# Generate all 3,087 cards + lattice index
python -m lattice.generator

# Launch the 3D viewer
streamlit run viz/streamlit_plotly_app.py
```

The viewer lets you rotate the 3D lattice, filter by mode/altitude/diamond/confidence, and click any cell to see its full Build Card.

## Repo layout

```
rig-systems-engineering-studio/
├── lattice/                       # Core engine (deterministic, 0 model calls)
│   ├── build_card.py              # Pydantic schema — the contract
│   ├── score.py                   # ALT_DEFAULTS + DIAMOND_MOD + STEP_MOD + BMS math
│   ├── step_semantics.py          # 21 (diamond, step) Y-axis semantics
│   ├── confidence_elements.py     # 21 (confidence, step) Z-axis semantics
│   ├── generator.py               # 3,087-cell deterministic generator
│   ├── render.py                  # YAML + Markdown emitters
│   └── cards/                     # 3,087 generated YAML + MD pairs
├── cards-design/                  # Companion design cards (Mike authors)
│   ├── triple-diamond-21-steps.md
│   ├── bms-confidence-3-element.md
│   ├── a1-python-only-deep-spec.md       # ✅ Complete
│   ├── a2-hybrid-deep-spec.md            # 🟡 Stub
│   ├── a3-agent-bounded-deep-spec.md     # 🟡 Stub
│   └── a4-llm-agent-free-deep-spec.md    # 🟡 Stub
├── viz/
│   ├── streamlit_plotly_app.py    # 3D viewer
│   ├── lattice_index.json         # Single source of truth for all viz
│   └── lattice_r3f/               # (planned) Three.js + R3F GitHub Pages site
├── tests/{unit,integration,evals}/
└── .github/workflows/             # CI + GitHub Pages deploy
```

The **archetype implementations** live in a separate (private) companion repo: `rig-systems-engineering-private`.

## Doctrine

Three hard rules baked into the lattice:

1. **No auto-approval at `AGENT_BOUNDED` or above.** `policy.requiresApproval()` is mandatory.
2. **Source-per-claim required at `HYBRID` and above.** Python wrapper enforces, not the prompt.
3. **Mechanism map required at `AGENT_BOUNDED` and above.** *A strategy without mechanism is a wish.*

## Governance

- **Per-cell re-score**: every 90 days, or on drift trigger.
- **Drift trigger**: `brier_score > 0.15 OR rollback_rate > 5%` → automatic re-score request.
- **Recalibration cron**: weekly.
- **Schema lock**: `build_card.py` is `v0.1.0`. Any breaking change bumps minor version.

## Build phases

| Phase | Window | Output |
|---|---|---|
| **P0** | Day 1 | ✅ Repo scaffold, schema, generator, viz, 5 card stubs |
| **P1** | Days 2–4 | Generator + viz running on placeholder content |
| **P2** | Week 2 | All 5 companion cards authored, regenerate cards with semantics |
| **P3** | Weeks 3–4 | A1 PYTHON_ONLY archetype live (~30 cells active) |
| **P4** | Week 4 | Three.js + R3F viewer deployed to GitHub Pages |
| **P5–P7** | Weeks 5–13 | A2 → A3 → A4 archetypes, full 147 archetype coverage |

## License

Apache 2.0. The lattice, generator, viz, and design cards are open source.
Archetype implementations live in a private companion repo.

## Status

🟢 **P0 scaffold complete.** Generator runs, produces 3,087 placeholder cells.
🟡 **P1 in progress.** Streamlit viewer scaffolded.
⚪ **P2+ pending.** Awaiting card authoring.
