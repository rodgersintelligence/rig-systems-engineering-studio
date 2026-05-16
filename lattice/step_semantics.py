"""Triple Diamond 21-step semantics (Y-axis source of truth).

Each of the 21 (diamond, step) combinations gets a distinct semantic.
This is the content layer Mike authors in cards-design/triple-diamond-21-steps.md.
Stubs here are placeholders to be overwritten when the card is finalized.
"""
from __future__ import annotations

from .build_card import Diamond, IQRSQPI

STEP_SEMANTICS: dict[tuple[Diamond, IQRSQPI], dict[str, str]] = {
    # D1 DISCOVERY — divergent, exploratory, opens the problem space
    (Diamond.D1_DISCOVERY, IQRSQPI.INTENT): {
        "name": "Divergent Intent Capture",
        "description": "STUB. Author in cards-design/triple-diamond-21-steps.md.",
    },
    (Diamond.D1_DISCOVERY, IQRSQPI.QUESTION): {
        "name": "Open-Frame Questioning",
        "description": "STUB.",
    },
    (Diamond.D1_DISCOVERY, IQRSQPI.RESEARCH): {
        "name": "Wide-Aperture Research",
        "description": "STUB.",
    },
    (Diamond.D1_DISCOVERY, IQRSQPI.SOLUTION): {
        "name": "Possibility Sketching",
        "description": "STUB.",
    },
    (Diamond.D1_DISCOVERY, IQRSQPI.QUALITY): {
        "name": "Coverage Check",
        "description": "STUB.",
    },
    (Diamond.D1_DISCOVERY, IQRSQPI.PROOF): {
        "name": "Exploration Receipt",
        "description": "STUB.",
    },
    (Diamond.D1_DISCOVERY, IQRSQPI.INTEGRATE): {
        "name": "Frame Selection",
        "description": "STUB.",
    },
    # D2 SOLUTION — converge, bind to mechanism, ship
    (Diamond.D2_SOLUTION, IQRSQPI.INTENT): {
        "name": "Mechanism-Bound Intent",
        "description": "STUB.",
    },
    (Diamond.D2_SOLUTION, IQRSQPI.QUESTION): {
        "name": "Decomposed Sub-Questions",
        "description": "STUB.",
    },
    (Diamond.D2_SOLUTION, IQRSQPI.RESEARCH): {
        "name": "Source-Per-Claim Research",
        "description": "STUB.",
    },
    (Diamond.D2_SOLUTION, IQRSQPI.SOLUTION): {
        "name": "Schema-Bound Synthesis",
        "description": "STUB.",
    },
    (Diamond.D2_SOLUTION, IQRSQPI.QUALITY): {
        "name": "Gate Stack Run",
        "description": "STUB.",
    },
    (Diamond.D2_SOLUTION, IQRSQPI.PROOF): {
        "name": "Falsification Charter",
        "description": "STUB.",
    },
    (Diamond.D2_SOLUTION, IQRSQPI.INTEGRATE): {
        "name": "Dispatch + Audit",
        "description": "STUB.",
    },
    # D3 EVOLUTION — measure drift, recalibrate, retire/rescore
    (Diamond.D3_EVOLUTION, IQRSQPI.INTENT): {
        "name": "Drift-Triggered Intent",
        "description": "STUB.",
    },
    (Diamond.D3_EVOLUTION, IQRSQPI.QUESTION): {
        "name": "What Broke / Why Now",
        "description": "STUB.",
    },
    (Diamond.D3_EVOLUTION, IQRSQPI.RESEARCH): {
        "name": "Brier Score + Rollback Forensics",
        "description": "STUB.",
    },
    (Diamond.D3_EVOLUTION, IQRSQPI.SOLUTION): {
        "name": "Recalibration Patch",
        "description": "STUB.",
    },
    (Diamond.D3_EVOLUTION, IQRSQPI.QUALITY): {
        "name": "Regression Check",
        "description": "STUB.",
    },
    (Diamond.D3_EVOLUTION, IQRSQPI.PROOF): {
        "name": "Re-Score Receipt",
        "description": "STUB.",
    },
    (Diamond.D3_EVOLUTION, IQRSQPI.INTEGRATE): {
        "name": "Cascade Update",
        "description": "STUB.",
    },
}

assert len(STEP_SEMANTICS) == 21, f"Expected 21 (diamond, step) entries, got {len(STEP_SEMANTICS)}"


def get_semantic(diamond: Diamond, step: IQRSQPI) -> str:
    s = STEP_SEMANTICS[(diamond, step)]
    return f"{s['name']}: {s['description']}"
