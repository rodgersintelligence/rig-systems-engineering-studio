"""RIG Systems Engineering Studio — Lattice core.

Generates and renders the corrected 7 x 3 x 4 x 7 = 588-cell deterministic
lattice that maps every RIG OS decision context to a Build Card and archetype.

Axes:
    X: Altitude          (L1..L7)                                 = 7
    Y: Diamond           (D1..D3)                                 = 3
    Z: Mode              (A1..A4)                                 = 4
    Step (internal):     IQRSQPI (I1, Q1, R, S, Q2, P, I2)         = 7

84 coordinates x 7 steps = 588 process-expanded execution cells.
4 modes x 7 steps = 28 reusable implementation archetypes.
"""
from .build_card import (
    Altitude, BuildCard, BuildMode, Diamond, EngineRefs, IQRSQPI,
    ImplementationStatus, Question,
)
from .generator import build_card, generate_all, generate_coordinates
from .render import render_yaml, render_markdown

__all__ = [
    "Altitude", "BuildCard", "BuildMode", "Diamond", "EngineRefs", "IQRSQPI",
    "ImplementationStatus", "Question",
    "build_card", "generate_all", "generate_coordinates",
    "render_yaml", "render_markdown",
]
__version__ = "0.2.0"
