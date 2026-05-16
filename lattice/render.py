"""YAML + Markdown renderers for BuildCards."""
from __future__ import annotations

import json

from .build_card import BuildCard


def render_yaml(card: BuildCard) -> str:
    """Compact YAML via JSON round-trip (no yaml dep required)."""
    try:
        import yaml  # type: ignore
        return yaml.safe_dump(json.loads(card.model_dump_json()), sort_keys=False)
    except ImportError:
        return card.model_dump_json(indent=2)


def render_markdown(card: BuildCard) -> str:
    return f"""---
cell_id: {card.cell_id}
altitude: {card.altitude.value}
diamond_y: {card.diamond_y.value}
step_y: {card.step_y.value}
confidence_element_z: {card.confidence_element_z.value}
step_z: {card.step_z.value}
bms: {card.bms}
mode: {card.mode.value}
schema_version: {card.schema_version}
---

# {card.cell_id}

**Mode**: `{card.mode.value}` (BMS = {card.bms})

## Position
- **X / Altitude**: `{card.altitude.value}`
- **Y / Diamond.Step**: `{card.diamond_y.value}.{card.step_y.value}` — {card.diamond_step_semantic}
- **Z / Confidence.Step**: `{card.confidence_element_z.value}.{card.step_z.value}` — {card.confidence_step_semantic}

## BMS Breakdown
| Component | Value |
| --- | --- |
| RAW | {card.raw} |
| ADJ_failure | {card.adj_failure} |
| ADJ_volume | {card.adj_volume} |
| ADJ_altitude | {card.adj_altitude} |
| **BMS (final)** | **{card.bms}** |

This cell's Z-axis confidence contribution: `{card.confidence_element_z.value} = {card.confidence_contribution}`.

## Stack
{chr(10).join(f"- {s}" for s in card.primary_stack)}

## Gates
{chr(10).join(f"- `{g}`" for g in card.gates)}

## Audit
`{card.audit_path}`

## Engines wired

- **Diamond sigma target**: `{card.engine_refs.diamond_sigma_target}` (D1=+30, D2=+5, D3=0)
- **DV Research engines**: {", ".join("`" + e + "`" for e in card.engine_refs.dv_research) or "_(only fires at Research step)_"}
- **DV Quality gates (physics)**: {", ".join("`" + e + "`" for e in card.engine_refs.dv_quality_gates) or "_(only fires at Quality step)_"}
- **Prediction engines**: {", ".join("`" + p + "`" for p in card.engine_refs.predictions) or "_(only fires at Quality step)_"}

## Question bank ({len(card.question_bank)} entries)

{chr(10).join(f"- **`{q.id}`** [{q.severity}] {q.text} _pass:_ `{q.pass_condition}`" for q in card.question_bank[:10])}

_+{max(0, len(card.question_bank) - 10)} more — full bank in YAML._

## Governance
- Next re-score: `{card.next_rescore}`
- Recalibration cron: `{card.recalibration_cron}`
- Drift trigger: `{card.drift_trigger}`
"""
