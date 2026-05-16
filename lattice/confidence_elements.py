"""BMS Confidence-3-Element x IQRSQPI semantics (Z-axis source of truth).

Each of the 21 (confidence_element, step) combinations describes how that
confidence contributor is evaluated at that IQRSQPI step.

Stubs here are placeholders to be overwritten when
cards-design/bms-confidence-3-element.md is finalized.
"""
from __future__ import annotations

from .build_card import ConfidenceElement, IQRSQPI

CONFIDENCE_SEMANTICS: dict[tuple[ConfidenceElement, IQRSQPI], dict[str, str]] = {
    # RAW: the unadjusted average of all 20 criteria (0..1)
    (ConfidenceElement.RAW, IQRSQPI.INTENT): {
        "name": "RAW @ Intent",
        "description": "STUB. Mean of C1..C20 evaluated against intent-capture context.",
    },
    (ConfidenceElement.RAW, IQRSQPI.QUESTION): {"name": "RAW @ Question", "description": "STUB."},
    (ConfidenceElement.RAW, IQRSQPI.RESEARCH): {"name": "RAW @ Research", "description": "STUB."},
    (ConfidenceElement.RAW, IQRSQPI.SOLUTION): {"name": "RAW @ Solution", "description": "STUB."},
    (ConfidenceElement.RAW, IQRSQPI.QUALITY): {"name": "RAW @ Quality", "description": "STUB."},
    (ConfidenceElement.RAW, IQRSQPI.PROOF): {"name": "RAW @ Proof", "description": "STUB."},
    (ConfidenceElement.RAW, IQRSQPI.INTEGRATE): {"name": "RAW @ Integrate", "description": "STUB."},
    # ADJ_FAILURE: +0.15 if C1>=4, +0.05 if C1==3, else 0
    (ConfidenceElement.ADJ_FAILURE, IQRSQPI.INTENT): {
        "name": "Failure-cost lift @ Intent",
        "description": "STUB. How much extra determinism is demanded if mis-intent is high-cost.",
    },
    (ConfidenceElement.ADJ_FAILURE, IQRSQPI.QUESTION): {"name": "Failure-cost lift @ Question", "description": "STUB."},
    (ConfidenceElement.ADJ_FAILURE, IQRSQPI.RESEARCH): {"name": "Failure-cost lift @ Research", "description": "STUB."},
    (ConfidenceElement.ADJ_FAILURE, IQRSQPI.SOLUTION): {"name": "Failure-cost lift @ Solution", "description": "STUB."},
    (ConfidenceElement.ADJ_FAILURE, IQRSQPI.QUALITY): {"name": "Failure-cost lift @ Quality", "description": "STUB."},
    (ConfidenceElement.ADJ_FAILURE, IQRSQPI.PROOF): {"name": "Failure-cost lift @ Proof", "description": "STUB."},
    (ConfidenceElement.ADJ_FAILURE, IQRSQPI.INTEGRATE): {"name": "Failure-cost lift @ Integrate", "description": "STUB."},
    # ADJ_VOLUME: 0.10 * (C11/5)
    (ConfidenceElement.ADJ_VOLUME, IQRSQPI.INTENT): {
        "name": "Volume lift @ Intent",
        "description": "STUB. Throughput pressure that pushes step toward more-deterministic execution.",
    },
    (ConfidenceElement.ADJ_VOLUME, IQRSQPI.QUESTION): {"name": "Volume lift @ Question", "description": "STUB."},
    (ConfidenceElement.ADJ_VOLUME, IQRSQPI.RESEARCH): {"name": "Volume lift @ Research", "description": "STUB."},
    (ConfidenceElement.ADJ_VOLUME, IQRSQPI.SOLUTION): {"name": "Volume lift @ Solution", "description": "STUB."},
    (ConfidenceElement.ADJ_VOLUME, IQRSQPI.QUALITY): {"name": "Volume lift @ Quality", "description": "STUB."},
    (ConfidenceElement.ADJ_VOLUME, IQRSQPI.PROOF): {"name": "Volume lift @ Proof", "description": "STUB."},
    (ConfidenceElement.ADJ_VOLUME, IQRSQPI.INTEGRATE): {"name": "Volume lift @ Integrate", "description": "STUB."},
}

assert len(CONFIDENCE_SEMANTICS) == 21, f"Expected 21 (confidence, step) entries, got {len(CONFIDENCE_SEMANTICS)}"


def get_semantic(confidence_element: ConfidenceElement, step: IQRSQPI) -> str:
    s = CONFIDENCE_SEMANTICS[(confidence_element, step)]
    return f"{s['name']}: {s['description']}"
