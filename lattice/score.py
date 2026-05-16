"""Scoring + mode resolution for the corrected 84-coordinate lattice.

In the corrected geometry the mode IS the Z-axis, so we don't classify cells
into modes from 20 criteria. We use representative scores per (altitude, mode)
and let runtime overrides modulate the actual score at invocation time.
"""
from __future__ import annotations

from .build_card import (
    Altitude, BuildMode, MODE_BMS_REP, MODE_THRESHOLDS,
)

# Altitude prior — higher altitudes score lower (less determinism available).
LEVEL_PRIOR_SCORE = {
    Altitude.L1: 0.90,
    Altitude.L2: 0.80,
    Altitude.L3: 0.65,
    Altitude.L4: 0.50,
    Altitude.L5: 0.35,
    Altitude.L6: 0.28,
    Altitude.L7: 0.18,
}

CONFIDENCE_BAND = {
    BuildMode.A1_PYTHON_ONLY: "HIGH",
    BuildMode.A2_HYBRID: "MEDIUM",
    BuildMode.A3_AGENT_BOUNDED: "LOW",
    BuildMode.A4_LLM_AGENT_FREE: "OPEN",
}


def clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def coordinate_bms(altitude: Altitude, mode: BuildMode) -> tuple[float, float, float, float, float]:
    """Return (raw, failure_adj, volume_adj, altitude_adj, score) for a coordinate.

    Representative-only; runtime invocations override via payload signals.
    """
    raw = MODE_BMS_REP[mode]
    failure_adj = 0.0
    volume_adj = 0.0
    altitude_adj = (LEVEL_PRIOR_SCORE[altitude] - 0.5) * 0.1  # bumps up to +/- 0.04
    score = clamp(raw + failure_adj + volume_adj + altitude_adj)
    return raw, failure_adj, volume_adj, altitude_adj, score


def threshold_for(mode: BuildMode) -> str:
    return MODE_THRESHOLDS[mode]


def confidence_band_for(mode: BuildMode) -> str:
    return CONFIDENCE_BAND[mode]
