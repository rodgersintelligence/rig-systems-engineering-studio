"""BMS Confidence-3-Element x IQRSQPI semantics (Z-axis source of truth).

Each of the 21 (confidence_element, step) combinations describes WHICH signal
that contributor measures at that IQRSQPI step.

Source of truth: cards-design/bms-confidence-3-element.md. Keep in sync.
"""
from __future__ import annotations

from .build_card import ConfidenceElement, IQRSQPI

CONFIDENCE_SEMANTICS: dict[tuple[ConfidenceElement, IQRSQPI], dict[str, str]] = {
    # --- RAW × IQRSQPI: base scoreability of the 20-criterion rubric -------
    (ConfidenceElement.RAW, IQRSQPI.INTENT): {
        "name": "RAW @ Intent",
        "description": (
            "Can we score the intent at all? Crisp matcher patterns + Phronema priors "
            "raise it. Multimodal ambiguity lowers it."
        ),
    },
    (ConfidenceElement.RAW, IQRSQPI.QUESTION): {
        "name": "RAW @ Question",
        "description": (
            "Can the question be typed against a Phronema query template? Known "
            "shapes raise it; novel multi-hop questions lower it."
        ),
    },
    (ConfidenceElement.RAW, IQRSQPI.RESEARCH): {
        "name": "RAW @ Research",
        "description": (
            "Source determinism. Structured DB/MCP calls raise it; open-web search "
            "and contrarian sourcing lower it."
        ),
    },
    (ConfidenceElement.RAW, IQRSQPI.SOLUTION): {
        "name": "RAW @ Solution",
        "description": (
            "Can the solution render from a template? Stable schemas + Jinja templates "
            "raise it; novel artifacts requiring generation lower it."
        ),
    },
    (ConfidenceElement.RAW, IQRSQPI.QUALITY): {
        "name": "RAW @ Quality",
        "description": (
            "Can the gate stack score this without an LLM judge? Hard gates + strict "
            "schema raise it; qualitative judgment requirements lower it."
        ),
    },
    (ConfidenceElement.RAW, IQRSQPI.PROOF): {
        "name": "RAW @ Proof",
        "description": (
            "Can we hash-and-sign without further reasoning? Content-addressable "
            "artifacts raise it; charter/mechanism authoring lowers it."
        ),
    },
    (ConfidenceElement.RAW, IQRSQPI.INTEGRATE): {
        "name": "RAW @ Integrate",
        "description": (
            "Does the dispatcher have a deterministic path? Known action kinds raise "
            "it; novel action classes lower it."
        ),
    },
    # --- ADJ_FAILURE × IQRSQPI: extra determinism demanded by failure cost --
    (ConfidenceElement.ADJ_FAILURE, IQRSQPI.INTENT): {
        "name": "Failure-cost lift @ Intent",
        "description": (
            "How costly is mis-intent? Customer-facing / regulatory exposure raise "
            "the lift; internal-only / reversible lower it."
        ),
    },
    (ConfidenceElement.ADJ_FAILURE, IQRSQPI.QUESTION): {
        "name": "Failure-cost lift @ Question",
        "description": (
            "How costly is asking the wrong question? One-shot decisions raise the "
            "lift; iterative contexts lower it."
        ),
    },
    (ConfidenceElement.ADJ_FAILURE, IQRSQPI.RESEARCH): {
        "name": "Failure-cost lift @ Research",
        "description": (
            "How bad is researching from wrong sources? Compliance / legal exposure "
            "raise it; internal low-stakes research lowers it."
        ),
    },
    (ConfidenceElement.ADJ_FAILURE, IQRSQPI.SOLUTION): {
        "name": "Failure-cost lift @ Solution",
        "description": (
            "How costly is shipping the wrong solution? External-facing / broadcast "
            "raise it; internal preview / single-user lowers it."
        ),
    },
    (ConfidenceElement.ADJ_FAILURE, IQRSQPI.QUALITY): {
        "name": "Failure-cost lift @ Quality",
        "description": (
            "How bad is a false pass? Public-facing artifacts raise it; sandboxed "
            "tests / reviewer-in-loop lower it."
        ),
    },
    (ConfidenceElement.ADJ_FAILURE, IQRSQPI.PROOF): {
        "name": "Failure-cost lift @ Proof",
        "description": (
            "How bad is signing a wrong receipt? Regulator-visible / financial "
            "reconciliation raise it; internal attestation lowers it."
        ),
    },
    (ConfidenceElement.ADJ_FAILURE, IQRSQPI.INTEGRATE): {
        "name": "Failure-cost lift @ Integrate",
        "description": (
            "How catastrophic is dispatching the wrong action? External email / "
            "payment / broadcast raise it; idempotent internal log lowers it."
        ),
    },
    # --- ADJ_VOLUME × IQRSQPI: throughput pressure toward determinism -------
    (ConfidenceElement.ADJ_VOLUME, IQRSQPI.INTENT): {
        "name": "Volume lift @ Intent",
        "description": (
            "Throughput pressure on intent resolution. Hot-path / real-time raise "
            "it; daily cron / ad-hoc lowers it."
        ),
    },
    (ConfidenceElement.ADJ_VOLUME, IQRSQPI.QUESTION): {
        "name": "Volume lift @ Question",
        "description": (
            "Throughput pressure on question building. Repeat-shape queries raise "
            "it (caching wins); novel-each-time lowers it."
        ),
    },
    (ConfidenceElement.ADJ_VOLUME, IQRSQPI.RESEARCH): {
        "name": "Volume lift @ Research",
        "description": (
            "Throughput pressure on research fan-out. Cacheable / batch-eligible "
            "fetches raise it; per-call billed APIs lower it."
        ),
    },
    (ConfidenceElement.ADJ_VOLUME, IQRSQPI.SOLUTION): {
        "name": "Volume lift @ Solution",
        "description": (
            "Throughput pressure on composition. Template reuse raises it; per-"
            "invocation personalization lowers it."
        ),
    },
    (ConfidenceElement.ADJ_VOLUME, IQRSQPI.QUALITY): {
        "name": "Volume lift @ Quality",
        "description": (
            "Throughput pressure on quality scoring. Hard gates + schema-only raise "
            "it; subjective LLM judge requirements lower it."
        ),
    },
    (ConfidenceElement.ADJ_VOLUME, IQRSQPI.PROOF): {
        "name": "Volume lift @ Proof",
        "description": (
            "Throughput pressure on audit writes. Append-only + batched commits raise "
            "it; synchronous multi-signer protocols lower it."
        ),
    },
    (ConfidenceElement.ADJ_VOLUME, IQRSQPI.INTEGRATE): {
        "name": "Volume lift @ Integrate",
        "description": (
            "Throughput pressure on dispatch. Batch-eligible idempotent APIs raise "
            "it; sync-only APIs requiring per-item approval lower it."
        ),
    },
}

assert len(CONFIDENCE_SEMANTICS) == 21, f"Expected 21 (confidence, step) entries, got {len(CONFIDENCE_SEMANTICS)}"


def get_semantic(confidence_element: ConfidenceElement, step: IQRSQPI) -> str:
    s = CONFIDENCE_SEMANTICS[(confidence_element, step)]
    return f"{s['name']}: {s['description']}"
