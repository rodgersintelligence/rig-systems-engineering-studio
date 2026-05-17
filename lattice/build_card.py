"""Pydantic schema for the corrected RIG Lattice Build Card.

Geometry (corrected 2026-05-16):
    7 altitudes x 3 diamonds x 4 BMS modes = 84 primary coordinates
    84 coordinates x 7 IQRSQPI steps = 588 process-expanded execution cells
    4 modes x 7 steps = 28 reusable implementation archetypes

Schema frozen at v0.2.0.
"""
from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field


class Altitude(str, Enum):
    L1 = "L1"
    L2 = "L2"
    L3 = "L3"
    L4 = "L4"
    L5 = "L5"
    L6 = "L6"
    L7 = "L7"


ALTITUDE_NAMES = {
    Altitude.L1: "Artifacts",
    Altitude.L2: "Tasks",
    Altitude.L3: "Workflows",
    Altitude.L4: "Systems",
    Altitude.L5: "Programs",
    Altitude.L6: "Strategy",
    Altitude.L7: "Vision",
}


class Diamond(str, Enum):
    D1 = "D1"  # Discovery / Physical
    D2 = "D2"  # Solution / Cognitive
    D3 = "D3"  # Evolution / Nature


DIAMOND_NAMES = {
    Diamond.D1: "Discovery",
    Diamond.D2: "Solution",
    Diamond.D3: "Evolution",
}


class IQRSQPI(str, Enum):
    INTENT = "I1"
    QUESTION = "Q1"
    RESEARCH = "R"
    SOLUTION = "S"
    QUALITY = "Q2"
    PROOF = "P"
    INTEGRATE = "I2"


STEP_NAMES = {
    IQRSQPI.INTENT: "Intent",
    IQRSQPI.QUESTION: "Question",
    IQRSQPI.RESEARCH: "Research",
    IQRSQPI.SOLUTION: "Solution",
    IQRSQPI.QUALITY: "Quality",
    IQRSQPI.PROOF: "Proof",
    IQRSQPI.INTEGRATE: "Integrate",
}


class BuildMode(str, Enum):
    """BMS-driven mode. Drives the Z-axis directly."""

    A1_PYTHON_ONLY = "A1"
    A2_HYBRID = "A2"
    A3_AGENT_BOUNDED = "A3"
    A4_LLM_AGENT_FREE = "A4"


MODE_LONG_NAMES = {
    BuildMode.A1_PYTHON_ONLY: "PYTHON_ONLY",
    BuildMode.A2_HYBRID: "HYBRID",
    BuildMode.A3_AGENT_BOUNDED: "AGENT_BOUNDED",
    BuildMode.A4_LLM_AGENT_FREE: "LLM_AGENT_FREE",
}

MODE_BMS_REP = {
    BuildMode.A1_PYTHON_ONLY: 0.90,
    BuildMode.A2_HYBRID: 0.60,
    BuildMode.A3_AGENT_BOUNDED: 0.35,
    BuildMode.A4_LLM_AGENT_FREE: 0.18,
}

MODE_THRESHOLDS = {
    BuildMode.A1_PYTHON_ONLY: ">=0.75",
    BuildMode.A2_HYBRID: "0.45-0.74",
    BuildMode.A3_AGENT_BOUNDED: "0.25-0.44",
    BuildMode.A4_LLM_AGENT_FREE: "<0.25",
}

MODE_COST_BANDS = {
    BuildMode.A1_PYTHON_ONLY: "$0-$0.001",
    BuildMode.A2_HYBRID: "$0.01-$0.30",
    BuildMode.A3_AGENT_BOUNDED: "$0.30-$1.00",
    BuildMode.A4_LLM_AGENT_FREE: "$1-$50 + 4h wall clock",
}


class ImplementationStatus(str, Enum):
    """Where this cell's archetype implementation stands."""

    IMPLEMENTED = "implemented"           # working code shipped to private repo
    SPEC_AUTHORED = "spec_authored"       # deep-spec exists; code not built
    PLANNED = "planned"                   # in roadmap but not specced
    NOT_STARTED = "not_started"


class Question(BaseModel):
    """One question/criterion in a cell's bank (~30 per cell)."""

    id: str
    kind: Literal["question", "criterion"]
    text: str
    pass_condition: str
    severity: Literal["blocker", "warning", "info"] = "warning"


class EngineRefs(BaseModel):
    """DV + prediction engines wired into this cell."""

    dv_research: list[str] = []
    dv_quality_gates: list[str] = []
    predictions: list[str] = []
    diamond_sigma_target: int | None = None


class BuildCard(BaseModel):
    """One execution cell in the 84 x 7 = 588-cell process-expanded lattice.

    cell_id format: L<n>-D<n>-A<n>-<STEP>
    Example: L4-D2-A2-S
    """

    cell_id: str

    # Position
    altitude: Altitude
    diamond: Diamond
    mode: BuildMode
    step: IQRSQPI

    # Coordinate-level identity (84 unique)
    coordinate_id: str  # L<n>-D<n>-A<n>

    # Scoring (LEGACY representative — for backwards compat)
    bms_raw: float = Field(ge=0.0, le=1.0)
    bms_failure_adj: float = 0.0
    bms_volume_adj: float = 0.0
    bms_altitude_adj: float = 0.0
    bms_score: float = Field(ge=0.0, le=1.0)
    bms_threshold: str
    confidence_band: Literal["HIGH", "MEDIUM", "LOW", "OPEN"]

    # REAL 20-criterion-driven BMS (per Build Card Schema §3)
    natural_bms_raw: float = Field(default=0.0, ge=0.0, le=1.0)
    natural_bms_score: float = Field(default=0.0, ge=0.0, le=1.0)
    natural_bms_failure_adj: float = 0.0
    natural_bms_volume_adj: float = 0.0
    natural_bms_altitude_adj: float = 0.0
    natural_mode: str = ""              # A1 | A2 | A3 | A4
    bms_alignment: float = 0.0          # natural_bms_score - mode_floor
    stretch_direction: str = "aligned"  # aligned | heavy | tight
    criteria: dict[str, int] = Field(default_factory=dict)  # C1..C20

    # Altitude semantic (X-axis)
    altitude_name: str = ""             # Artifacts | Tasks | ... | Vision
    altitude_purpose: str = ""

    # Rubric drift (sum of |delta| across criteria, learned from outcomes)
    rubric_drift_magnitude: int = 0
    rubric_drift_per_criterion: dict[str, int] = Field(default_factory=dict)

    # Semantics (Y-axis)
    diamond_step_semantic: str = ""

    # Implementation
    archetype: str  # "A1.7", "A2.3", etc.
    implementation_status: ImplementationStatus = ImplementationStatus.NOT_STARTED
    runtime_entrypoint: str = ""

    # Operational
    primary_stack: list[str] = []
    quality_gates: list[str] = []
    tools: list[str] = []
    models: list[str] = []
    cost_band_usd: str
    approval_policy: str
    proof_policy: str = "required"
    audit_policy: str = "append-only"
    escalation_policy: str = ""

    # Engines wired
    engine_refs: EngineRefs = Field(default_factory=EngineRefs)
    question_bank: list[Question] = Field(default_factory=list)

    # Governance
    next_rescore: str = ""
    recalibration_cron: str = "weekly"
    drift_trigger: str = "brier_score > 0.15 OR rollback_rate > 5%"

    generated_at: datetime = Field(default_factory=datetime.utcnow)
    schema_version: str = "0.2.0"
