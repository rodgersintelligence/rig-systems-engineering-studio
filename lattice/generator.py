"""Deterministic 3,087-cell lattice generator.

Iterates X (altitude) x Y (diamond, step) x Z (confidence_element, step).
Produces 7 x 21 x 21 = 3,087 BuildCards.

Run:
    python -m lattice.generator                # writes YAML + MD + lattice_index.json
    python -m lattice.generator --validate     # validates without writing
"""
from __future__ import annotations

import argparse
import itertools
import json
from datetime import date, timedelta
from pathlib import Path

from .build_card import (
    Altitude, BuildCard, ConfidenceElement, Diamond, IQRSQPI, BuildMode,
)
from .confidence_elements import CONFIDENCE_SEMANTICS
from .score import (
    ALT_INDEX, compute_bms, mode_from_bms, score_criteria,
)
from .step_semantics import STEP_SEMANTICS

STACK_BY_ALTITUDE: dict[Altitude, list[str]] = {
    Altitude.L7_VISION: ["Claude Opus", "CrewAI", "Phronema", "Consensus/arXiv", "Neo4j"],
    Altitude.L6_STRATEGY: ["Claude Sonnet", "OR-Tools", "Phronema", "Neo4j", "Postgres"],
    Altitude.L5_PROGRAMS: ["Claude Sonnet", "LangGraph", "Cookiecutter", "SQLite", "Plotly"],
    Altitude.L4_SYSTEMS: ["Claude Sonnet", "LangGraph", "Pydantic", "DVC", "Promptfoo"],
    Altitude.L3_WORKFLOWS: ["Sonnet/Haiku", "LangGraph", "Temporal", "Pydantic", "Langfuse"],
    Altitude.L2_TASKS: ["Haiku / local Llama", "MLX", "Pydantic", "httpx", "Langfuse"],
    Altitude.L1_ARTIFACTS: ["Haiku / local Llama", "MLX", "Jinja2", "Pydantic", "AionUI"],
}

GATES_BY_ALTITUDE: dict[Altitude, list[str]] = {
    Altitude.L7_VISION: ["physics_31_finetuning", "physics_35_bell", "cognitive_01_rupture",
                         "nature_22_evolution", "rig_l_composite"],
    Altitude.L6_STRATEGY: ["physics_31", "physics_38", "cognitive_05", "nature_24", "rig_l"],
    Altitude.L5_PROGRAMS: ["physics_32", "cognitive_07", "nature_22", "rig_l"],
    Altitude.L4_SYSTEMS: ["physics_31", "cognitive_07_voltage", "nature_22", "anti_slop", "rig_l"],
    Altitude.L3_WORKFLOWS: ["physics_33", "cognitive_12", "anti_slop", "rig_l_lite"],
    Altitude.L2_TASKS: ["physics_34", "anti_slop"],
    Altitude.L1_ARTIFACTS: ["physics_31", "anti_slop", "claim_validator"],
}


def score_cell(
    altitude: Altitude, diamond_y: Diamond, step_y: IQRSQPI,
    confidence_element_z: ConfidenceElement, step_z: IQRSQPI,
) -> BuildCard:
    scores = score_criteria(altitude, diamond_y, step_y)
    raw, adj_f, adj_v, adj_a, bms = compute_bms(scores, altitude)
    bms_r = round(bms, 4)  # classify on the rounded value so stored bms and mode agree

    contribution = {
        ConfidenceElement.RAW: raw,
        ConfidenceElement.ADJ_FAILURE: adj_f,
        ConfidenceElement.ADJ_VOLUME: adj_v,
    }[confidence_element_z]

    cell_id = f"{altitude.value}-{diamond_y.value}.{step_y.value}-{confidence_element_z.value}.{step_z.value}"

    sem_y = STEP_SEMANTICS[(diamond_y, step_y)]
    sem_z = CONFIDENCE_SEMANTICS[(confidence_element_z, step_z)]

    return BuildCard(
        cell_id=cell_id,
        altitude=altitude,
        diamond_y=diamond_y,
        step_y=step_y,
        confidence_element_z=confidence_element_z,
        step_z=step_z,
        scores=scores,
        raw=round(raw, 4),
        adj_failure=round(adj_f, 4),
        adj_volume=round(adj_v, 4),
        adj_altitude=round(adj_a, 4),
        bms=bms_r,
        mode=mode_from_bms(bms_r),
        confidence_contribution=round(contribution, 4),
        diamond_step_semantic=f"{sem_y['name']}: {sem_y['description']}",
        confidence_step_semantic=f"{sem_z['name']}: {sem_z['description']}",
        primary_stack=STACK_BY_ALTITUDE[altitude],
        gates=GATES_BY_ALTITUDE[altitude],
        audit_path=f"phronema://audit/{altitude.value}/{cell_id}/",
        next_rescore=(date.today() + timedelta(days=90)).isoformat(),
    )


def generate_all() -> list[BuildCard]:
    cards: list[BuildCard] = []
    for alt, dia, sy, conf, sz in itertools.product(
        Altitude, Diamond, IQRSQPI, ConfidenceElement, IQRSQPI,
    ):
        cards.append(score_cell(alt, dia, sy, conf, sz))
    return cards


def write_index(cards: list[BuildCard], out_dir: Path) -> Path:
    """Compact JSON for the viz layer."""
    index = []
    for c in cards:
        index.append({
            "cell_id": c.cell_id,
            "altitude": c.altitude.value,
            "altitude_index": ALT_INDEX[c.altitude],
            "diamond_y": c.diamond_y.value,
            "step_y": c.step_y.value,
            "confidence_element_z": c.confidence_element_z.value,
            "step_z": c.step_z.value,
            "bms": c.bms,
            "mode": c.mode.value,
            "contribution": c.confidence_contribution,
        })
    index_path = out_dir / "lattice_index.json"
    index_path.write_text(json.dumps(index, indent=2))
    return index_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the RIG lattice (3,087 cells).")
    parser.add_argument("--out", default="lattice/cards", help="Output dir for YAML/MD cards")
    parser.add_argument("--viz-out", default="viz", help="Output dir for lattice_index.json")
    parser.add_argument("--validate", action="store_true", help="Generate in-memory only; don't write")
    args = parser.parse_args()

    print("[lattice] Generating 7 x 21 x 21 = 3,087 cells …")
    cards = generate_all()
    assert len(cards) == 3087, f"Expected 3,087 cells, got {len(cards)}"
    print(f"[lattice] Generated {len(cards)} cards.")

    if args.validate:
        mode_counts: dict[str, int] = {}
        for c in cards:
            mode_counts[c.mode.value] = mode_counts.get(c.mode.value, 0) + 1
        print(f"[lattice] Mode distribution: {mode_counts}")
        return 0

    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    from .render import render_yaml, render_markdown
    for c in cards:
        (out / f"{c.cell_id}.yaml").write_text(render_yaml(c))
        (out / f"{c.cell_id}.md").write_text(render_markdown(c))

    viz_out = Path(args.viz_out)
    viz_out.mkdir(parents=True, exist_ok=True)
    idx_path = write_index(cards, viz_out)
    print(f"[lattice] Wrote {len(cards)} YAML + MD pairs to {out}/")
    print(f"[lattice] Wrote lattice index to {idx_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
