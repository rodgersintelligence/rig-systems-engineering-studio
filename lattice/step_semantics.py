"""Triple Diamond 21-step semantics (Y-axis source of truth).

Each of the 21 (diamond, step) combinations is a distinct semantic.
Source of truth: cards-design/triple-diamond-21-steps.md.
Keep this file synchronized with the markdown card.
"""
from __future__ import annotations

from .build_card import Diamond, IQRSQPI

STEP_SEMANTICS: dict[tuple[Diamond, IQRSQPI], dict[str, str]] = {
    # --- D1 DISCOVERY --- divergent; open the problem space ----------------
    (Diamond.D1, IQRSQPI.INTENT): {
        "name": "Divergent Intent Capture",
        "description": (
            "Treat the incoming signal as a vector of possibilities, not a known intent. "
            "Deterministic matchers are deliberately bypassed at D1."
        ),
    },
    (Diamond.D1, IQRSQPI.QUESTION): {
        "name": "Open-Frame Questioning",
        "description": (
            "Generate the widest set of reasonable questions before any narrowing. "
            "Each question must score >= +3 sigma on deviation from baseline framings."
        ),
    },
    (Diamond.D1, IQRSQPI.RESEARCH): {
        "name": "Wide-Aperture Research",
        "description": (
            "Source diversity > depth. Pull from contrarian sources, edge-case datasets, "
            "and deprecated frameworks. Source allowlist is intentionally permissive."
        ),
    },
    (Diamond.D1, IQRSQPI.SOLUTION): {
        "name": "Possibility Sketching",
        "description": (
            "Generate 5-10 distinct solution shapes without committing to mechanism. "
            "Each must be falsifiable but not yet mechanism-bound."
        ),
    },
    (Diamond.D1, IQRSQPI.QUALITY): {
        "name": "Coverage Check",
        "description": (
            "Did we explore the actual problem space, or just the comfortable region? "
            "Adversarial perspective sweep + anti-slop probing."
        ),
    },
    (Diamond.D1, IQRSQPI.PROOF): {
        "name": "Exploration Receipt",
        "description": (
            "Audit-grade record of what was explored AND what was deliberately abandoned. "
            "Future agents inherit your dead ends so they don't relitigate them."
        ),
    },
    (Diamond.D1, IQRSQPI.INTEGRATE): {
        "name": "Frame Selection",
        "description": (
            "Narrow the SolutionField to 1-3 frames that carry forward into D2. "
            "Human-in-loop at L5+; deterministic shortlist at L1-L3."
        ),
    },
    # --- D2 SOLUTION --- converge; bind to mechanism; ship -----------------
    (Diamond.D2, IQRSQPI.INTENT): {
        "name": "Mechanism-Bound Intent",
        "description": (
            "Convert each SelectedFrame into an intent with explicit mechanism. "
            "No mechanism, no progress past this step."
        ),
    },
    (Diamond.D2, IQRSQPI.QUESTION): {
        "name": "Decomposed Sub-Questions",
        "description": (
            "Break the mechanism-bound intent into 3-7 sub-questions with a coverage "
            "guarantee >= 0.85. Dependency-aware so research can parallelize."
        ),
    },
    (Diamond.D2, IQRSQPI.RESEARCH): {
        "name": "Source-Per-Claim Research",
        "description": (
            "Every claim that will appear in the solution must be backed by >=1 source. "
            "Python wrapper enforces, never the prompt."
        ),
    },
    (Diamond.D2, IQRSQPI.SOLUTION): {
        "name": "Schema-Bound Synthesis",
        "description": (
            "Generate one solution that fully types against the contract. "
            "Outlines + Pydantic + retry on schema fail."
        ),
    },
    (Diamond.D2, IQRSQPI.QUALITY): {
        "name": "Gate Stack Run",
        "description": (
            "Physics -> Cognitive -> Nature -> RIG-L composite. Short-circuit on any "
            "hard failure; diagnostic payload returned, not raised."
        ),
    },
    (Diamond.D2, IQRSQPI.PROOF): {
        "name": "Falsification Charter",
        "description": (
            "Bind the solution to a written falsifier. How will we know we were wrong? "
            "Generates Brier-trackable predictions."
        ),
    },
    (Diamond.D2, IQRSQPI.INTEGRATE): {
        "name": "Dispatch + Audit",
        "description": (
            "Risk-classified approval (conditional at A1/A2, mandatory at A3+) -> "
            "execute -> write audit row tying ProofPacket -> Action -> Result."
        ),
    },
    # --- D3 EVOLUTION --- measure drift; recalibrate; cascade --------------
    (Diamond.D3, IQRSQPI.INTENT): {
        "name": "Drift-Triggered Intent",
        "description": (
            "A drift event (Brier > 0.15, rollback > 5%, or 90-day re-score) generates "
            "an intent to investigate what changed in the cell's behavior."
        ),
    },
    (Diamond.D3, IQRSQPI.QUESTION): {
        "name": "What Broke / Why Now",
        "description": (
            "Decompose the drift into testable failure-mode questions. Time-windowed "
            "comparison to the cell's prior baseline (90d / 180d / 365d)."
        ),
    },
    (Diamond.D3, IQRSQPI.RESEARCH): {
        "name": "Brier Score + Rollback Forensics",
        "description": (
            "Pull prediction history, rollback logs, and audit rows. Compute current "
            "vs. baseline calibration."
        ),
    },
    (Diamond.D3, IQRSQPI.SOLUTION): {
        "name": "Recalibration Patch",
        "description": (
            "Minimum-diff change to restore the cell to its target performance. "
            "Could be a criterion override, a prior adjustment, or a mode demotion."
        ),
    },
    (Diamond.D3, IQRSQPI.QUALITY): {
        "name": "Regression Check",
        "description": (
            "Replay the last 30 days of invocations against the patched cell. "
            "Confirm Brier improves without breaking adjacent cells in the lattice."
        ),
    },
    (Diamond.D3, IQRSQPI.PROOF): {
        "name": "Re-Score Receipt",
        "description": (
            "Append-only record of the score change. Includes prior values, patch "
            "reason, trigger source, and proof of regression check."
        ),
    },
    (Diamond.D3, IQRSQPI.INTEGRATE): {
        "name": "Cascade Update",
        "description": (
            "Propagate the score change to dependent cells (same altitude, same step, "
            "related diamonds). Regenerate downstream cards and refresh the 3D viz."
        ),
    },
}

assert len(STEP_SEMANTICS) == 21, f"Expected 21 (diamond, step) entries, got {len(STEP_SEMANTICS)}"


def get_semantic(diamond: Diamond, step: IQRSQPI) -> str:
    s = STEP_SEMANTICS[(diamond, step)]
    return f"{s['name']}: {s['description']}"
