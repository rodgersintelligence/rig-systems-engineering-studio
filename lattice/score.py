"""Scoring + mode resolution for the corrected 588-cell lattice.

Implements the FULL 20-criterion BMS rubric from Build Card Schema §3:

    RAW = Σ(C_i / 5) / 20                                # [0, 1]
    ADJ_failure   = 0.15 if C1 >= 4 else (0.05 if C1 == 3 else 0)
    ADJ_volume    = 0.10 * (C11 / 5)
    ADJ_altitude  = -0.05 * (altitude_index / 6)         # L1=0, L7=-0.05
    BMS = clamp(RAW + ADJ_failure + ADJ_volume + ADJ_altitude, 0, 1)

Each cell's `natural_bms_score` is computed from the merged criteria vector:
    criteria = ALT_DEFAULTS[altitude] + DIAMOND_MOD[diamond] + STEP_MOD[step]

A cell's `bms_alignment` measures the gap between its natural BMS and the
mode threshold its chosen mode requires:

    A1 (PYTHON_ONLY)     threshold >= 0.75
    A2 (HYBRID)          threshold  0.45-0.74
    A3 (AGENT_BOUNDED)   threshold  0.25-0.44
    A4 (LLM_AGENT_FREE)  threshold  < 0.25

Positive alignment = the cell's natural fit matches or exceeds the chosen
mode's floor. Negative = the operator is stretching the mode beyond what
the rubric suggests (often deliberately, e.g., using A4 at L1 for novelty).
"""
from __future__ import annotations

from .altitude_semantics import ALT_DEFAULTS_C, ALT_INDEX
from .build_card import Altitude, BuildMode, Diamond, IQRSQPI, MODE_BMS_REP, MODE_THRESHOLDS


# ── Diamond modifiers (source: Build Card Schema §3) ─────────────────────────

DIAMOND_MOD: dict[Diamond, dict[str, int]] = {
    Diamond.D1: dict(C8=-2, C10=-2, C15=-2, C17=-2),    # discovery = exploratory
    Diamond.D2: dict(),                                  # solution = baseline
    Diamond.D3: dict(C8=+1, C9=+1, C14=+1, C16=+1),     # evolution = lockdown
}

# ── IQRSQPI step modifiers ───────────────────────────────────────────────────

STEP_MOD: dict[IQRSQPI, dict[str, int]] = {
    IQRSQPI.INTENT:    dict(C10=+1),                              # intent -> mechanism matters
    IQRSQPI.QUESTION:  dict(C6=-1, C17=-1),                       # question = open
    IQRSQPI.RESEARCH:  dict(C7=-2, C8=-2, C17=-2),                # research = exploratory
    IQRSQPI.SOLUTION:  dict(C6=+1, C10=+1),                       # solution = converge
    IQRSQPI.QUALITY:   dict(C9=+2, C18=+1),                       # quality = test heavy
    IQRSQPI.PROOF:     dict(C4=+1, C9=+1),                        # proof = audit heavy
    IQRSQPI.INTEGRATE: dict(C14=+1, C16=+1),                      # integrate = lock down
}

# Mode confidence bands (legacy MODE_BMS_REP for representative comparison)
LEVEL_PRIOR_SCORE = {
    Altitude.L1: 0.90, Altitude.L2: 0.80, Altitude.L3: 0.65, Altitude.L4: 0.50,
    Altitude.L5: 0.35, Altitude.L6: 0.28, Altitude.L7: 0.18,
}

CONFIDENCE_BAND = {
    BuildMode.A1_PYTHON_ONLY: "HIGH",
    BuildMode.A2_HYBRID: "MEDIUM",
    BuildMode.A3_AGENT_BOUNDED: "LOW",
    BuildMode.A4_LLM_AGENT_FREE: "OPEN",
}


# Threshold floors used for bms_alignment.
MODE_FLOOR: dict[BuildMode, float] = {
    BuildMode.A1_PYTHON_ONLY: 0.75,
    BuildMode.A2_HYBRID: 0.45,
    BuildMode.A3_AGENT_BOUNDED: 0.25,
    BuildMode.A4_LLM_AGENT_FREE: 0.0,
}
MODE_CEILING: dict[BuildMode, float] = {
    BuildMode.A1_PYTHON_ONLY: 1.0,
    BuildMode.A2_HYBRID: 0.75,
    BuildMode.A3_AGENT_BOUNDED: 0.45,
    BuildMode.A4_LLM_AGENT_FREE: 0.25,
}


def clamp(v: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, v))


def _clamp_int(v: int, lo: int = 0, hi: int = 5) -> int:
    return max(lo, min(hi, v))


def criteria_for(altitude: Altitude, diamond: Diamond, step: IQRSQPI) -> dict[str, int]:
    """Merge altitude priors with diamond + step modifiers; clamp each to [0,5]."""
    out: dict[str, int] = dict(ALT_DEFAULTS_C[altitude])
    for k, v in DIAMOND_MOD[diamond].items():
        out[k] = _clamp_int(out.get(k, 0) + v)
    for k, v in STEP_MOD[step].items():
        out[k] = _clamp_int(out.get(k, 0) + v)
    return out


def natural_bms(altitude: Altitude, diamond: Diamond, step: IQRSQPI) -> dict[str, float]:
    """Compute the FULL 20-criterion BMS for a (altitude, diamond, step).

    Returns {raw, adj_failure, adj_volume, adj_altitude, bms, criteria}.
    Mode is NOT part of natural BMS — the rubric says which mode best fits.
    """
    crit = criteria_for(altitude, diamond, step)
    raw = sum(crit.values()) / (20 * 5)
    adj_failure = 0.15 if crit["C1"] >= 4 else (0.05 if crit["C1"] == 3 else 0.0)
    adj_volume = 0.10 * (crit["C11"] / 5)
    adj_altitude = -0.05 * (ALT_INDEX[altitude] / 6)
    bms = clamp(raw + adj_failure + adj_volume + adj_altitude)
    return {
        "raw": round(raw, 4),
        "adj_failure": round(adj_failure, 4),
        "adj_volume": round(adj_volume, 4),
        "adj_altitude": round(adj_altitude, 4),
        "bms": round(bms, 4),
        "criteria": crit,
    }


def natural_mode(bms_score: float) -> BuildMode:
    """Which mode does the natural BMS suggest?"""
    if bms_score >= 0.75:
        return BuildMode.A1_PYTHON_ONLY
    if bms_score >= 0.45:
        return BuildMode.A2_HYBRID
    if bms_score >= 0.25:
        return BuildMode.A3_AGENT_BOUNDED
    return BuildMode.A4_LLM_AGENT_FREE


def bms_alignment(bms_score: float, chosen_mode: BuildMode) -> dict[str, float | str]:
    """Measure fit between a cell's natural BMS and its chosen execution mode.

    alignment > 0  -> natural BMS exceeds the mode's floor; well-aligned
    alignment = 0  -> on the mode's floor
    alignment < 0  -> stretched (operating in a more-expensive mode than rubric needs)
                      OR conservative (operating in a less-capable mode than rubric needs)

    `stretch_direction` is "heavy" when chosen mode is below natural mode (e.g.
    L1 cell at A4 — paying $30+ for what could be deterministic) and "tight"
    when chosen mode is above natural mode (e.g. L7 cell at A1 — using a
    template for a strategic decision).
    """
    nat = natural_mode(bms_score)
    floor = MODE_FLOOR[chosen_mode]
    ceiling = MODE_CEILING[chosen_mode]
    in_range = floor <= bms_score < ceiling

    rank = {
        BuildMode.A1_PYTHON_ONLY: 0,
        BuildMode.A2_HYBRID: 1,
        BuildMode.A3_AGENT_BOUNDED: 2,
        BuildMode.A4_LLM_AGENT_FREE: 3,
    }
    delta = rank[chosen_mode] - rank[nat]
    if delta == 0:
        stretch = "aligned"
    elif delta > 0:
        stretch = "heavy"     # chose a heavier mode than the rubric needs
    else:
        stretch = "tight"     # chose a lighter mode than the rubric suggests

    return {
        "natural_mode": nat.value,
        "chosen_mode": chosen_mode.value,
        "natural_bms": round(bms_score, 4),
        "mode_floor": floor,
        "mode_ceiling": ceiling,
        "in_range": in_range,
        "alignment": round(bms_score - floor, 4),
        "stretch_direction": stretch,
        "rank_delta": delta,
    }


# ── Coordinate BMS (LEGACY representative score, kept for backwards compat) ──


def coordinate_bms(altitude: Altitude, mode: BuildMode) -> tuple[float, float, float, float, float]:
    """Representative (raw, fail_adj, vol_adj, alt_adj, score) per (altitude, mode).

    DEPRECATED: use natural_bms(altitude, diamond, step) for real per-cell BMS.
    Kept so existing callers don't break.
    """
    raw = MODE_BMS_REP[mode]
    failure_adj = 0.0
    volume_adj = 0.0
    altitude_adj = (LEVEL_PRIOR_SCORE[altitude] - 0.5) * 0.1
    score = clamp(raw + failure_adj + volume_adj + altitude_adj)
    return raw, failure_adj, volume_adj, altitude_adj, score


def threshold_for(mode: BuildMode) -> str:
    return MODE_THRESHOLDS[mode]


def confidence_band_for(mode: BuildMode) -> str:
    return CONFIDENCE_BAND[mode]
