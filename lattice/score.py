"""Scoring priors and modifiers for the RIG lattice.

Source of truth for ALT_DEFAULTS, DIAMOND_MOD, STEP_MOD, BMS computation.
Edit here, then run `python -m lattice.generator` to regenerate all 3,087 cells.
"""
from __future__ import annotations

from .build_card import Altitude, Diamond, IQRSQPI, BuildMode

ALT_INDEX = {a: i for i, a in enumerate(Altitude)}  # L1=0, L7=6

ALT_DEFAULTS: dict[Altitude, dict[str, int]] = {
    Altitude.L7_VISION: dict(C1=3, C2=3, C3=0, C4=3, C5=4, C6=1, C7=1, C8=0, C9=0, C10=1,
                             C11=0, C12=0, C13=0, C14=0, C15=0, C16=1, C17=0, C18=0, C19=5, C20=2),
    Altitude.L6_STRATEGY: dict(C1=3, C2=3, C3=1, C4=3, C5=4, C6=2, C7=2, C8=1, C9=1, C10=2,
                               C11=0, C12=0, C13=1, C14=1, C15=1, C16=2, C17=1, C18=1, C19=4, C20=3),
    Altitude.L5_PROGRAMS: dict(C1=3, C2=3, C3=1, C4=3, C5=3, C6=3, C7=3, C8=2, C9=2, C10=3,
                               C11=1, C12=1, C13=1, C14=2, C15=2, C16=2, C17=2, C18=2, C19=4, C20=3),
    Altitude.L4_SYSTEMS: dict(C1=3, C2=2, C3=1, C4=4, C5=3, C6=4, C7=3, C8=2, C9=3, C10=3,
                              C11=1, C12=0, C13=1, C14=3, C15=2, C16=3, C17=2, C18=2, C19=4, C20=4),
    Altitude.L3_WORKFLOWS: dict(C1=3, C2=3, C3=2, C4=4, C5=3, C6=4, C7=4, C8=3, C9=4, C10=4,
                                C11=3, C12=2, C13=3, C14=4, C15=3, C16=4, C17=3, C18=3, C19=3, C20=4),
    Altitude.L2_TASKS: dict(C1=2, C2=3, C3=1, C4=3, C5=2, C6=5, C7=4, C8=4, C9=4, C10=4,
                            C11=4, C12=3, C13=4, C14=4, C15=4, C16=4, C17=4, C18=4, C19=2, C20=5),
    Altitude.L1_ARTIFACTS: dict(C1=4, C2=5, C3=1, C4=4, C5=2, C6=5, C7=4, C8=4, C9=4, C10=5,
                                C11=3, C12=1, C13=4, C14=4, C15=4, C16=4, C17=4, C18=4, C19=4, C20=5),
}

DIAMOND_MOD: dict[Diamond, dict[str, int]] = {
    Diamond.D1_DISCOVERY: dict(C8=-2, C10=-2, C15=-2, C17=-2),
    Diamond.D2_SOLUTION: dict(),
    Diamond.D3_EVOLUTION: dict(C8=+1, C9=+1, C14=+1, C16=+1),
}

STEP_MOD: dict[IQRSQPI, dict[str, int]] = {
    IQRSQPI.INTENT: dict(C10=+1),
    IQRSQPI.QUESTION: dict(C6=-1, C17=-1),
    IQRSQPI.RESEARCH: dict(C7=-2, C8=-2, C17=-2),
    IQRSQPI.SOLUTION: dict(C6=+1, C10=+1),
    IQRSQPI.QUALITY: dict(C9=+2, C18=+1),
    IQRSQPI.PROOF: dict(C4=+1, C9=+1),
    IQRSQPI.INTEGRATE: dict(C14=+1, C16=+1),
}


def clamp(v: int, lo: int = 0, hi: int = 5) -> int:
    return max(lo, min(hi, v))


def score_criteria(altitude: Altitude, diamond: Diamond, step: IQRSQPI) -> dict[str, int]:
    s = dict(ALT_DEFAULTS[altitude])
    for k, v in DIAMOND_MOD[diamond].items():
        s[k] = clamp(s[k] + v)
    for k, v in STEP_MOD[step].items():
        s[k] = clamp(s[k] + v)
    return s


def compute_bms(scores: dict[str, int], altitude: Altitude) -> tuple[float, float, float, float, float]:
    raw = sum(scores.values()) / (20 * 5)
    adj_failure = 0.15 if scores["C1"] >= 4 else (0.05 if scores["C1"] == 3 else 0.0)
    adj_volume = 0.10 * (scores["C11"] / 5)
    adj_altitude = -0.05 * ALT_INDEX[altitude] / 6
    bms = max(0.0, min(1.0, raw + adj_failure + adj_volume + adj_altitude))
    return raw, adj_failure, adj_volume, adj_altitude, bms


def mode_from_bms(bms: float) -> BuildMode:
    if bms >= 0.75:
        return BuildMode.PYTHON_ONLY
    if bms >= 0.45:
        return BuildMode.HYBRID
    if bms >= 0.25:
        return BuildMode.AGENT_BOUNDED
    return BuildMode.LLM_AGENT_FREE
