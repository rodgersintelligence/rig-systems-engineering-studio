"""Pydantic schema for the RIG lattice Build Card.

One Build Card per cell. 3,087 cells total. Schema frozen at v1.
"""
from __future__ import annotations

from datetime import date, datetime
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, Field


class Altitude(str, Enum):
    L1_ARTIFACTS = "L1"
    L2_TASKS = "L2"
    L3_WORKFLOWS = "L3"
    L4_SYSTEMS = "L4"
    L5_PROGRAMS = "L5"
    L6_STRATEGY = "L6"
    L7_VISION = "L7"


class Diamond(str, Enum):
    D1_DISCOVERY = "D1"
    D2_SOLUTION = "D2"
    D3_EVOLUTION = "D3"


class IQRSQPI(str, Enum):
    INTENT = "I1"
    QUESTION = "Q1"
    RESEARCH = "R"
    SOLUTION = "S"
    QUALITY = "Q2"
    PROOF = "P"
    INTEGRATE = "I2"


class ConfidenceElement(str, Enum):
    """The 3 mathematical contributors to BMS."""

    RAW = "RAW"
    ADJ_FAILURE = "ADJ_FAILURE"
    ADJ_VOLUME = "ADJ_VOLUME"


class BuildMode(str, Enum):
    PYTHON_ONLY = "PYTHON_ONLY"
    HYBRID = "HYBRID"
    AGENT_BOUNDED = "AGENT_BOUNDED"
    LLM_AGENT_FREE = "LLM_AGENT_FREE"


class ProcessStep(BaseModel):
    order: int
    name: str
    mode: Literal["PY", "LLM", "HUMAN"]
    tool: str
    notes: str = ""


class Example(BaseModel):
    name: str
    inputs: dict[str, Any]
    flow: list[str]
    output: str
    gates_fired: list[str]


class BuildCard(BaseModel):
    """One cell in the 7 x 21 x 21 lattice.

    cell_id format: <altitude>-<diamond>.<step_y>-<conf_element>.<step_z>
    Example: L4-D2.S-ADJ_FAILURE.Q2
    """

    cell_id: str
    altitude: Altitude
    diamond_y: Diamond
    step_y: IQRSQPI
    confidence_element_z: ConfidenceElement
    step_z: IQRSQPI

    scores: dict[str, int] = Field(description="C1..C20, each 0-5")
    raw: float
    adj_failure: float
    adj_volume: float
    adj_altitude: float
    bms: float
    mode: BuildMode

    confidence_contribution: float = Field(
        description="The Z-element's specific contribution to BMS at step_z"
    )

    diamond_step_semantic: str = Field(
        description="Y-axis semantic: what (diamond, step_y) means"
    )
    confidence_step_semantic: str = Field(
        description="Z-axis semantic: what this confidence element evaluates at step_z"
    )

    process_steps: list[ProcessStep] = []
    primary_stack: list[str] = []
    gates: list[str] = []
    approval_surface: str = "AionUI"
    audit_path: str = ""

    examples: list[Example] = []

    next_rescore: str = ""
    recalibration_cron: str = "weekly"
    drift_trigger: str = "brier_score > 0.15 OR rollback_rate > 5%"

    generated_at: datetime = Field(default_factory=datetime.utcnow)
    schema_version: str = "0.1.0"


# 20 scoring criteria
CRITERIA = [
    "C1", "C2", "C3", "C4", "C5",
    "C6", "C7", "C8", "C9", "C10",
    "C11", "C12", "C13", "C14",
    "C15", "C16", "C17", "C18",
    "C19", "C20",
]

CRITERION_NAMES = {
    "C1": "Failure Cost",
    "C2": "Reversibility",
    "C3": "Regulatory/Compliance Exposure",
    "C4": "Auditability Requirement",
    "C5": "Blast Radius",
    "C6": "Output Schema Definability",
    "C7": "Input Structure",
    "C8": "Rule Coverage",
    "C9": "Test Surface",
    "C10": "Mechanism Clarity (RIG doctrine)",
    "C11": "Volume per Day",
    "C12": "Latency Budget",
    "C13": "Cost Sensitivity",
    "C14": "Recurrence Pattern",
    "C15": "Sigma Deviation Target",
    "C16": "Drift Tolerance",
    "C17": "Creative Variation Required",
    "C18": "Judgment Depth",
    "C19": "Human-in-Loop Requirement",
    "C20": "Tooling Maturity",
}
