"""Smoke tests for the corrected 588-cell lattice generator."""
from __future__ import annotations

from lattice.build_card import (
    Altitude, BuildMode, Diamond, IQRSQPI, ImplementationStatus,
)
from lattice.generator import build_card, generate_all, generate_coordinates


def test_cell_count_is_588() -> None:
    cards = generate_all()
    assert len(cards) == 588


def test_coordinate_count_is_84() -> None:
    coords = generate_coordinates()
    assert len(coords) == 84
    assert len({c["coordinate_id"] for c in coords}) == 84


def test_archetype_count_is_28() -> None:
    cards = generate_all()
    archetypes = {c.archetype for c in cards}
    assert len(archetypes) == 28


def test_all_cell_ids_unique() -> None:
    cards = generate_all()
    ids = [c.cell_id for c in cards]
    assert len(set(ids)) == len(ids), "Duplicate cell_id found"


def test_build_card_deterministic() -> None:
    a = build_card(Altitude.L4, Diamond.D2, BuildMode.A2_HYBRID, IQRSQPI.SOLUTION)
    b = build_card(Altitude.L4, Diamond.D2, BuildMode.A2_HYBRID, IQRSQPI.SOLUTION)
    assert a.bms_score == b.bms_score
    assert a.mode == b.mode
    assert a.archetype == b.archetype


def test_bms_in_range() -> None:
    for card in generate_all():
        assert 0.0 <= card.bms_score <= 1.0


def test_archetype_naming() -> None:
    """Archetype must be M.N where M is mode value and N is 1..7."""
    cards = generate_all()
    for c in cards:
        parts = c.archetype.split(".")
        assert parts[0] == c.mode.value
        assert 1 <= int(parts[1]) <= 7


def test_implementation_status_split() -> None:
    cards = generate_all()
    impl = sum(1 for c in cards if c.implementation_status == ImplementationStatus.IMPLEMENTED)
    spec = sum(1 for c in cards if c.implementation_status == ImplementationStatus.SPEC_AUTHORED)
    # A1+A2 = implemented (2 modes x 3 diamonds x 7 altitudes x 7 steps = 294)
    # A3+A4 = spec_authored (294)
    assert impl == 294
    assert spec == 294


def test_question_bank_populated() -> None:
    cards = generate_all()
    for c in cards:
        assert len(c.question_bank) == 30


def test_research_step_has_dv_engines() -> None:
    card = build_card(Altitude.L4, Diamond.D2, BuildMode.A2_HYBRID, IQRSQPI.RESEARCH)
    assert len(card.engine_refs.dv_research) > 0


def test_quality_step_has_predictions() -> None:
    card = build_card(Altitude.L4, Diamond.D2, BuildMode.A2_HYBRID, IQRSQPI.QUALITY)
    assert len(card.engine_refs.predictions) > 0
    assert any("mirofish" in p for p in card.engine_refs.predictions)
