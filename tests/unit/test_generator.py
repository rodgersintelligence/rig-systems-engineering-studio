"""Smoke tests for the lattice generator."""
from __future__ import annotations

from lattice.build_card import Altitude, BuildMode, ConfidenceElement, Diamond, IQRSQPI
from lattice.generator import generate_all, score_cell


def test_cell_count_is_3087() -> None:
    cards = generate_all()
    assert len(cards) == 3087


def test_all_cell_ids_unique() -> None:
    cards = generate_all()
    ids = [c.cell_id for c in cards]
    assert len(set(ids)) == len(ids), "Duplicate cell_id found"


def test_score_cell_deterministic() -> None:
    a = score_cell(
        Altitude.L4_SYSTEMS, Diamond.D2_SOLUTION, IQRSQPI.SOLUTION,
        ConfidenceElement.RAW, IQRSQPI.QUALITY,
    )
    b = score_cell(
        Altitude.L4_SYSTEMS, Diamond.D2_SOLUTION, IQRSQPI.SOLUTION,
        ConfidenceElement.RAW, IQRSQPI.QUALITY,
    )
    assert a.bms == b.bms
    assert a.scores == b.scores
    assert a.mode == b.mode


def test_bms_in_range() -> None:
    for card in generate_all():
        assert 0.0 <= card.bms <= 1.0


def test_mode_thresholds() -> None:
    for card in generate_all():
        if card.bms >= 0.75:
            assert card.mode == BuildMode.PYTHON_ONLY
        elif card.bms >= 0.45:
            assert card.mode == BuildMode.HYBRID
        elif card.bms >= 0.25:
            assert card.mode == BuildMode.AGENT_BOUNDED
        else:
            assert card.mode == BuildMode.LLM_AGENT_FREE


def test_confidence_contribution_matches_element() -> None:
    card = score_cell(
        Altitude.L4_SYSTEMS, Diamond.D2_SOLUTION, IQRSQPI.SOLUTION,
        ConfidenceElement.ADJ_FAILURE, IQRSQPI.PROOF,
    )
    assert card.confidence_contribution == card.adj_failure
