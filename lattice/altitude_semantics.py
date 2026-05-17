"""X-axis source of truth — the 7 altitudes of the RIG lattice.

Each altitude is a distinct *granularity of decision*. Higher altitudes are
slower, costlier, and more strategic; lower altitudes are faster, cheaper, and
more deterministic.

Source: companion card `cards-design/altitude-7-levels.md`.
"""
from __future__ import annotations

from .build_card import Altitude


ALTITUDE_SEMANTICS: dict[Altitude, dict[str, str]] = {
    Altitude.L1: {
        "name": "Artifacts",
        "purpose": "Single deliverable produced from a fully-typed payload.",
        "examples": "outbound email, draft tweet, status row, audit receipt, content card",
        "horizon": "seconds",
        "reversibility": "high (artifact-level)",
        "volume": "1000s/day",
        "cost_pressure": "extreme — must be free or near-free",
        "audit_demand": "claim-validator + content hash",
        "owner": "templated by Jinja; signed by agent",
        "doctrine": "No model in the decision path; LLM only as a <=60-word shim.",
    },
    Altitude.L2: {
        "name": "Tasks",
        "purpose": "Multi-step task with a known shape (form → action → record).",
        "examples": "lead enrichment, ticket triage, inbox sweep, daily reconciliation",
        "horizon": "minutes",
        "reversibility": "medium-high",
        "volume": "100s/day",
        "cost_pressure": "high — measure per task",
        "audit_demand": "structured task trace",
        "owner": "Hermes orchestrator dispatches; archetype executes",
        "doctrine": "Schema-bound; templates + tiny model assists.",
    },
    Altitude.L3: {
        "name": "Workflows",
        "purpose": "Decomposable multi-step orchestration with conditional branches.",
        "examples": "research → score → outreach, lead scoring loop, content publish flow",
        "horizon": "minutes to hours",
        "reversibility": "medium",
        "volume": "10s/day",
        "cost_pressure": "moderate",
        "audit_demand": "DAG trace + per-node receipts",
        "owner": "LangGraph DAG with model-in-node",
        "doctrine": "Python orchestrates, LLMs reason inside bounded nodes.",
    },
    Altitude.L4: {
        "name": "Systems",
        "purpose": "Cross-workflow service or capability that other altitudes consume.",
        "examples": "MCP capability, scoring engine, schema registry, RAG service",
        "horizon": "hours to days",
        "reversibility": "medium-low",
        "volume": "few/day",
        "cost_pressure": "low per call, high cumulative",
        "audit_demand": "version + contract + drift telemetry",
        "owner": "Mike approves; agent maintains",
        "doctrine": "Source-per-claim mandatory; mechanism map on every decision.",
    },
    Altitude.L5: {
        "name": "Programs",
        "purpose": "Coordinated set of systems addressing one program objective.",
        "examples": "growth program (Q3), product launch, hiring loop, doctrine refresh",
        "horizon": "weeks",
        "reversibility": "low",
        "volume": "a few in flight",
        "cost_pressure": "negligible vs strategic value",
        "audit_demand": "OKR + Brier predictions per milestone",
        "owner": "Mike + agent crew with mandatory signoff",
        "doctrine": "Red-team + falsification charter required; agent budgeted.",
    },
    Altitude.L6: {
        "name": "Strategy",
        "purpose": "Cross-program strategy that reshapes the operating space.",
        "examples": "pricing strategy, market wedge, RIG product line, partnership doctrine",
        "horizon": "quarters",
        "reversibility": "very low",
        "volume": "rare (quarterly)",
        "cost_pressure": "irrelevant — strategic stakes dominate",
        "audit_demand": "full charter + 12-point Brier set + cascade preview",
        "owner": "Mike signs; agent crew researches + drafts",
        "doctrine": "Multi-agent debate; +5σ minimum deviation; mandatory signoff.",
    },
    Altitude.L7: {
        "name": "Vision",
        "purpose": "Identity-level decisions: what the company IS, who it serves.",
        "examples": "RIG name + scope, doctrine restatement, generational pivot",
        "horizon": "years",
        "reversibility": "approaches zero",
        "volume": "annual or epochal",
        "cost_pressure": "irrelevant",
        "audit_demand": "civilizational artifact — Brier set runs for years",
        "owner": "Mike alone signs; agent crew supports indefinitely",
        "doctrine": "Hierarchical CrewAI; no timeout; cascade to L6/L5/L4 automatic.",
    },
}


def get(altitude: Altitude) -> dict[str, str]:
    return ALTITUDE_SEMANTICS[altitude]


def short(altitude: Altitude) -> str:
    s = ALTITUDE_SEMANTICS[altitude]
    return f"{s['name']} — {s['purpose']}"


# Default 20-criterion priors per altitude. Source: Build Card Schema §3.
# Each criterion lives in [0, 5]; higher = more determinism warranted.
ALT_DEFAULTS_C: dict[Altitude, dict[str, int]] = {
    Altitude.L7: dict(C1=3, C2=3, C3=0, C4=3, C5=4, C6=1, C7=1, C8=0, C9=0, C10=1,
                      C11=0, C12=0, C13=0, C14=0, C15=0, C16=1, C17=0, C18=0, C19=5, C20=2),
    Altitude.L6: dict(C1=3, C2=3, C3=1, C4=3, C5=4, C6=2, C7=2, C8=1, C9=1, C10=2,
                      C11=0, C12=0, C13=1, C14=1, C15=1, C16=2, C17=1, C18=1, C19=4, C20=3),
    Altitude.L5: dict(C1=3, C2=3, C3=1, C4=3, C5=3, C6=3, C7=3, C8=2, C9=2, C10=3,
                      C11=1, C12=1, C13=1, C14=2, C15=2, C16=2, C17=2, C18=2, C19=4, C20=3),
    Altitude.L4: dict(C1=3, C2=2, C3=1, C4=4, C5=3, C6=4, C7=3, C8=2, C9=3, C10=3,
                      C11=1, C12=0, C13=1, C14=3, C15=2, C16=3, C17=2, C18=2, C19=4, C20=4),
    Altitude.L3: dict(C1=3, C2=3, C3=2, C4=4, C5=3, C6=4, C7=4, C8=3, C9=4, C10=4,
                      C11=3, C12=2, C13=3, C14=4, C15=3, C16=4, C17=3, C18=3, C19=3, C20=4),
    Altitude.L2: dict(C1=2, C2=3, C3=1, C4=3, C5=2, C6=5, C7=4, C8=4, C9=4, C10=4,
                      C11=4, C12=3, C13=4, C14=4, C15=4, C16=4, C17=4, C18=4, C19=2, C20=5),
    Altitude.L1: dict(C1=4, C2=5, C3=1, C4=4, C5=2, C6=5, C7=4, C8=4, C9=4, C10=5,
                      C11=3, C12=1, C13=4, C14=4, C15=4, C16=4, C17=4, C18=4, C19=4, C20=5),
}

ALT_INDEX: dict[Altitude, int] = {a: i for i, a in enumerate(
    [Altitude.L1, Altitude.L2, Altitude.L3, Altitude.L4, Altitude.L5, Altitude.L6, Altitude.L7]
)}
