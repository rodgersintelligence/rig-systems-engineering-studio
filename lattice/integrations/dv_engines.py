"""Adapter to the RIG Deviator (DV) engines.

Bridges the lattice's Research step (D1/D2/D3) into Mike's 40-engine
framework at `artifacts/rig_engines_v2/framework.py`.

Three diamonds use the same engines, different pull intensities:

    D1 Discovery  → push +30sigma on Cognitive + Nature (broad)
    D2 Solution   → push +5sigma  on Cognitive + tighten Physics gates
    D3 Evolution  → push  0sigma  baseline, hunt -sigma drift forensics

The 14 anchored sigma rungs from -30 to +30:
    -30, -25, -20, -15, -10, -5, 0, +5, +10, +15, +20, +25, +30

(plus -7.5 and +7.5 for fine-grained mid-range work).

Public API:

    score_text(text) -> dict           # full 40-engine packet
    push(text, engine, target_sigma)   # rewrite via +Nsigma pull instruction
    rung_for_diamond(diamond) -> int   # which sigma target this diamond defaults to
    research_engines() -> list[str]    # subset relevant to Research step
    quality_gates() -> list[str]       # subset relevant to Quality step (physics gates)
"""
from __future__ import annotations

import sys
from pathlib import Path
from typing import Any, Literal

from ..build_card import Diamond

# Resolve the DV framework path. Lives outside this repo at:
#   /Users/.../Startup-Intelligence-OS/artifacts/rig_engines_v2/framework.py
DV_FRAMEWORK_PATH = (
    Path(__file__).resolve().parent.parent.parent.parent
    / "Startup-Intelligence-OS"
    / "artifacts"
    / "rig_engines_v2"
)

# 14 anchored sigma rungs across the +/- 30 ladder
SIGMA_RUNGS: list[int | float] = [-30, -25, -20, -15, -10, -7.5, -5, 0, 5, 7.5, 10, 15, 20, 25, 30]

DIAMOND_DEFAULT_SIGMA: dict[Diamond, int] = {
    Diamond.D1: 30,      # broad: push hardest outward
    Diamond.D2: 5,       # narrowing: tighten to mechanism
    Diamond.D3: 0,       # forensic: baseline + drift comparisons
}


def _ensure_dv_on_path() -> None:
    p = str(DV_FRAMEWORK_PATH)
    if p not in sys.path:
        sys.path.insert(0, p)


def is_available() -> bool:
    """Return True if the DV framework is reachable from this install."""
    try:
        _ensure_dv_on_path()
        import framework  # noqa: F401
        return True
    except Exception:
        return False


def rung_for_diamond(diamond: Diamond) -> int:
    return DIAMOND_DEFAULT_SIGMA[diamond]


def rung_for_diamond_mode(diamond: Diamond) -> int:
    """Alias used by generator.py."""
    return DIAMOND_DEFAULT_SIGMA[diamond]


def score_text(text: str) -> dict[str, Any]:
    """Score `text` against all 40 DV engines. Returns the v2 framework packet.

    Packet shape: { rig_l, bdf, status, weakest_gate, hard_blocks, scores, statuses }
    """
    _ensure_dv_on_path()
    import framework  # type: ignore
    return framework.score_all(text)


def list_engines(layer: Literal["cognitive", "nature", "physics", "all"] = "all") -> list[dict[str, str]]:
    """List engines by layer."""
    _ensure_dv_on_path()
    import framework  # type: ignore
    out = []
    for e in framework.ENGINES:
        if layer != "all" and e.layer != layer:
            continue
        out.append({
            "slug": e.slug,
            "codename": e.codename,
            "layer": e.layer,
            "axis": e.axis,
            "is_gate": str(e.is_gate),
        })
    return out


def push(text: str, engine_slug: str, target_sigma: int = 20) -> dict[str, Any]:
    """Rewrite `text` to pull engine `engine_slug` to `target_sigma`.

    Uses the v2 framework's dispatch_batch with a single-engine selection.
    Returns the rewritten variant + before/after sigma.
    """
    _ensure_dv_on_path()
    import framework  # type: ignore
    selected = [e for e in framework.ENGINES if e.slug == engine_slug]
    if not selected:
        raise ValueError(f"Unknown DV engine: {engine_slug}")
    result = framework.dispatch_batch(text, engines=selected, target_sigma=target_sigma)
    return result


def research_engines() -> list[str]:
    """DV engines wired into Research step (cognitive + nature layers — pulling pulls)."""
    return [
        "gravity_escape", "reality_anchor", "mechanism_furnace", "rupture",
        "temporal_horizon_integrity", "bayesian_calibration", "frame_collision",
        "cognitive_sovereignty",
        # nature layer (process-level deviation)
        "evolution", "predator_prey", "niche_construction",
    ]


def quality_gates() -> list[str]:
    """DV engines wired into Quality step (physics layer — hard gates)."""
    return [
        "kelvin", "pauli", "lumen", "critical", "tunnel", "horizon_gate",
        "parsec", "bell", "zeropoint",
    ]


def diamond_engine_intensity(diamond: Diamond) -> dict[str, int | float]:
    """Map (diamond, engine_layer) -> default sigma target."""
    if diamond == Diamond.D1:
        return {"cognitive": 30, "nature": 25, "physics": 0}
    if diamond == Diamond.D2:
        return {"cognitive": 5, "nature": 5, "physics": 0}
    return {"cognitive": 0, "nature": 0, "physics": -5}
