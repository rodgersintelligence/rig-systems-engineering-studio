"""Deterministic generator for the corrected 84-coordinate / 588-cell lattice.

Iterates: 7 altitudes x 3 diamonds x 4 modes = 84 primary coordinates,
each expanded to 7 IQRSQPI steps = 588 process-expanded execution cells.

Run:
    python -m lattice.generator                # writes YAML + MD + lattice_index.json
    python -m lattice.generator --validate     # in-memory; doesn't write
"""
from __future__ import annotations

import argparse
import itertools
import json
from datetime import date, timedelta
from pathlib import Path

from .altitude_semantics import ALTITUDE_SEMANTICS
from .build_card import (
    Altitude, BuildCard, BuildMode, Diamond, EngineRefs, IQRSQPI,
    ImplementationStatus, MODE_COST_BANDS, MODE_LONG_NAMES,
)
from .integrations import dv_engines
from .integrations.predictions import MIRO_FISH_CRITERIA
from .question_bank import bank_for_cell
from .score import (
    bms_alignment, confidence_band_for, coordinate_bms, natural_bms,
    threshold_for,
)
from .step_semantics import STEP_SEMANTICS

# Which modes have a working implementation in the private repo today.
# All 4 archetypes shipped 2026-05-16 with 70/70 tests passing.
IMPLEMENTED_MODES = {
    BuildMode.A1_PYTHON_ONLY,
    BuildMode.A2_HYBRID,
    BuildMode.A3_AGENT_BOUNDED,
    BuildMode.A4_LLM_AGENT_FREE,
}
SPEC_AUTHORED_MODES: set[BuildMode] = set()

STACK_BY_MODE = {
    BuildMode.A1_PYTHON_ONLY: [
        "pydantic", "jinja2", "httpx", "sqlalchemy", "MCP clients", "Haiku/MLX (60-word shim)",
    ],
    BuildMode.A2_HYBRID: [
        "LangGraph", "Sonnet (in nodes)", "NeMo Guardrails", "Pydantic + Outlines", "Temporal/Prefect",
    ],
    BuildMode.A3_AGENT_BOUNDED: [
        "Sonnet/Opus agents", "Mem0", "MCP tool ring", "Promptfoo", "AionUI (72h signoff)",
    ],
    BuildMode.A4_LLM_AGENT_FREE: [
        "CrewAI hierarchical", "Opus", "OR-Tools/PuLP", "Brier prediction loop", "AionUI (no timeout)",
    ],
}

GATES_BY_ALTITUDE = {
    Altitude.L7: ["physics_31", "physics_35_bell", "cognitive_01_rupture", "nature_22", "rig_l_composite"],
    Altitude.L6: ["physics_31", "physics_38", "cognitive_05", "nature_24", "rig_l"],
    Altitude.L5: ["physics_32", "cognitive_07", "nature_22", "rig_l"],
    Altitude.L4: ["physics_31", "cognitive_07_voltage", "nature_22", "anti_slop", "rig_l"],
    Altitude.L3: ["physics_33", "cognitive_12", "anti_slop", "rig_l_lite"],
    Altitude.L2: ["physics_34", "anti_slop"],
    Altitude.L1: ["physics_31", "anti_slop", "claim_validator"],
}

APPROVAL_POLICY = {
    BuildMode.A1_PYTHON_ONLY: "conditional",
    BuildMode.A2_HYBRID: "risk-classified conditional",
    BuildMode.A3_AGENT_BOUNDED: "mandatory (72h timeout)",
    BuildMode.A4_LLM_AGENT_FREE: "mandatory (no timeout) + post-mortem",
}

ESCALATION_BY_MODE = {
    BuildMode.A1_PYTHON_ONLY: "UNKNOWN intent -> escalate to A3.1",
    BuildMode.A2_HYBRID: "confidence < 0.8 or gate fail -> escalate to A3.1",
    BuildMode.A3_AGENT_BOUNDED: "budget cap or quality fail -> escalate to A4.1",
    BuildMode.A4_LLM_AGENT_FREE: "block; cannot escalate (top of lattice)",
}


def _implementation_status(mode: BuildMode) -> ImplementationStatus:
    if mode in IMPLEMENTED_MODES:
        return ImplementationStatus.IMPLEMENTED
    if mode in SPEC_AUTHORED_MODES:
        return ImplementationStatus.SPEC_AUTHORED
    return ImplementationStatus.NOT_STARTED


def build_card(altitude: Altitude, diamond: Diamond, mode: BuildMode, step: IQRSQPI) -> BuildCard:
    raw, adj_f, adj_v, adj_a, score = coordinate_bms(altitude, mode)

    # Real 20-criterion BMS — varies per (alt, diamond, step), independent of mode.
    nat = natural_bms(altitude, diamond, step)
    align = bms_alignment(nat["bms"], mode)

    archetype = f"{mode.value}.{list(IQRSQPI).index(step) + 1}"
    coord_id = f"{altitude.value}-{diamond.value}-{mode.value}"
    cell_id = f"{coord_id}-{step.value}"

    sem = STEP_SEMANTICS[(diamond, step)]
    alt_sem = ALTITUDE_SEMANTICS[altitude]

    refs = EngineRefs(diamond_sigma_target=dv_engines.rung_for_diamond_mode(diamond))
    if step == IQRSQPI.RESEARCH:
        refs.dv_research = dv_engines.research_engines()
    if step == IQRSQPI.QUALITY:
        refs.dv_quality_gates = dv_engines.quality_gates()
        refs.predictions = (
            [f"mirofish:{c}" for c in MIRO_FISH_CRITERIA] + ["miroshark", "milkyway"]
        )

    return BuildCard(
        cell_id=cell_id,
        altitude=altitude,
        diamond=diamond,
        mode=mode,
        step=step,
        coordinate_id=coord_id,
        bms_raw=round(raw, 4),
        bms_failure_adj=round(adj_f, 4),
        bms_volume_adj=round(adj_v, 4),
        bms_altitude_adj=round(adj_a, 4),
        bms_score=round(score, 4),
        bms_threshold=threshold_for(mode),
        confidence_band=confidence_band_for(mode),  # type: ignore[arg-type]
        natural_bms_raw=nat["raw"],
        natural_bms_score=nat["bms"],
        natural_bms_failure_adj=nat["adj_failure"],
        natural_bms_volume_adj=nat["adj_volume"],
        natural_bms_altitude_adj=nat["adj_altitude"],
        natural_mode=align["natural_mode"],
        bms_alignment=align["alignment"],
        stretch_direction=align["stretch_direction"],
        criteria=nat["criteria"],
        altitude_name=alt_sem["name"],
        altitude_purpose=alt_sem["purpose"],
        diamond_step_semantic=f"{sem['name']}: {sem['description']}",
        archetype=archetype,
        implementation_status=_implementation_status(mode),
        runtime_entrypoint=f"rig.archetypes.{mode.value.lower()}_{MODE_LONG_NAMES[mode].lower()}",
        primary_stack=STACK_BY_MODE[mode],
        quality_gates=GATES_BY_ALTITUDE[altitude],
        tools=STACK_BY_MODE[mode],
        models=[],
        cost_band_usd=MODE_COST_BANDS[mode],
        approval_policy=APPROVAL_POLICY[mode],
        escalation_policy=ESCALATION_BY_MODE[mode],
        engine_refs=refs,
        question_bank=bank_for_cell(diamond, step),
        next_rescore=(date.today() + timedelta(days=90)).isoformat(),
    )


def generate_all() -> list[BuildCard]:
    """7 x 3 x 4 x 7 = 588 cells."""
    cards: list[BuildCard] = []
    for alt, dia, mode, step in itertools.product(Altitude, Diamond, BuildMode, IQRSQPI):
        cards.append(build_card(alt, dia, mode, step))
    return cards


def generate_coordinates() -> list[dict[str, str]]:
    """84 coordinates. Used by viz when collapsing the step dimension."""
    out: list[dict[str, str]] = []
    for alt, dia, mode in itertools.product(Altitude, Diamond, BuildMode):
        out.append({
            "coordinate_id": f"{alt.value}-{dia.value}-{mode.value}",
            "altitude": alt.value,
            "diamond": dia.value,
            "mode": mode.value,
        })
    return out


def write_index(cards: list[BuildCard], out_dir: Path) -> Path:
    """Compact JSON for the viz layer."""
    altitude_idx = {a: i for i, a in enumerate(Altitude)}
    diamond_idx = {d: i for i, d in enumerate(Diamond)}
    mode_idx = {m: i for i, m in enumerate(BuildMode)}
    step_idx = {s: i for i, s in enumerate(IQRSQPI)}

    index = []
    for c in cards:
        index.append({
            "cell_id": c.cell_id,
            "coordinate_id": c.coordinate_id,
            "altitude": c.altitude.value,
            "altitude_index": altitude_idx[c.altitude],
            "altitude_name": c.altitude_name,
            "diamond": c.diamond.value,
            "diamond_index": diamond_idx[c.diamond],
            "mode": c.mode.value,
            "mode_long": MODE_LONG_NAMES[c.mode],
            "mode_index": mode_idx[c.mode],
            "step": c.step.value,
            "step_index": step_idx[c.step],
            "bms_score": c.bms_score,
            "natural_bms_score": c.natural_bms_score,
            "natural_mode": c.natural_mode,
            "bms_alignment": c.bms_alignment,
            "stretch_direction": c.stretch_direction,
            "confidence_band": c.confidence_band,
            "archetype": c.archetype,
            "implementation_status": c.implementation_status.value,
            "diamond_step_semantic": c.diamond_step_semantic,
        })
    index_path = out_dir / "lattice_index.json"
    index_path.write_text(json.dumps(index, indent=2))
    return index_path


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate the corrected 588-cell RIG lattice.")
    parser.add_argument("--out", default="lattice/cards", help="Output dir for YAML/MD cards")
    parser.add_argument("--viz-out", default="viz", help="Output dir for lattice_index.json")
    parser.add_argument("--validate", action="store_true", help="Generate in-memory; don't write")
    args = parser.parse_args()

    print("[lattice] Generating 7 x 3 x 4 x 7 = 588 cells ...")
    cards = generate_all()
    assert len(cards) == 588, f"Expected 588 cells, got {len(cards)}"
    print(f"[lattice] Generated {len(cards)} cards.")

    if args.validate:
        mode_counts: dict[str, int] = {}
        impl_counts: dict[str, int] = {}
        for c in cards:
            mode_counts[c.mode.value] = mode_counts.get(c.mode.value, 0) + 1
            impl_counts[c.implementation_status.value] = impl_counts.get(c.implementation_status.value, 0) + 1
        print(f"[lattice] Mode distribution: {mode_counts}")
        print(f"[lattice] Implementation status: {impl_counts}")
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
