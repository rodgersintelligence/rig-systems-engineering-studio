"""RIG Systems Engineering Studio — Lattice core.

Generates and renders the 7 x 21 x 21 = 3,087-cell deterministic lattice
that maps every RIG OS decision context to a Build Card and archetype.

Axes:
    X: Altitude          (L1..L7)                                = 7
    Y: Diamond x IQRSQPI (D1..D3 x I1,Q1,R,S,Q2,P,I2)            = 21
    Z: Confidence x IQRSQPI (RAW, ADJ_failure, ADJ_volume x 7)   = 21
"""
from .build_card import BuildCard, Altitude, Diamond, IQRSQPI, BuildMode, ConfidenceElement
from .generator import generate_all, score_cell
from .render import render_yaml, render_markdown

__all__ = [
    "BuildCard",
    "Altitude",
    "Diamond",
    "IQRSQPI",
    "BuildMode",
    "ConfidenceElement",
    "generate_all",
    "score_cell",
    "render_yaml",
    "render_markdown",
]
__version__ = "0.1.0"
