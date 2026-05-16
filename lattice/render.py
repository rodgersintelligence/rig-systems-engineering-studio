"""YAML + Markdown renderers for the corrected 588-cell BuildCard."""
from __future__ import annotations

import json

from .build_card import BuildCard


def render_yaml(card: BuildCard) -> str:
    try:
        import yaml  # type: ignore
        return yaml.safe_dump(json.loads(card.model_dump_json()), sort_keys=False)
    except ImportError:
        return card.model_dump_json(indent=2)


def render_markdown(card: BuildCard) -> str:
    status_emoji = {
        "implemented": "✅",
        "spec_authored": "📋",
        "planned": "🟡",
        "not_started": "⚪",
    }.get(card.implementation_status.value, "⚪")

    return f"""---
cell_id: {card.cell_id}
coordinate_id: {card.coordinate_id}
altitude: {card.altitude.value}
diamond: {card.diamond.value}
mode: {card.mode.value}
step: {card.step.value}
archetype: {card.archetype}
bms_score: {card.bms_score}
confidence_band: {card.confidence_band}
implementation_status: {card.implementation_status.value}
schema_version: {card.schema_version}
---

# {card.cell_id}

**Archetype**: `{card.archetype}` · **Mode**: `{card.mode.value}` ({card.confidence_band}, BMS = {card.bms_score})
**Implementation**: {status_emoji} `{card.implementation_status.value}`

## Coordinate
- **Altitude**: `{card.altitude.value}` (X)
- **Diamond**: `{card.diamond.value}` (Y)
- **Mode**: `{card.mode.value}` (Z)
- **IQRSQPI Step**: `{card.step.value}` ({card.diamond_step_semantic})
- **Coordinate**: `{card.coordinate_id}`

## BMS Breakdown
| Component | Value |
| --- | --- |
| RAW | {card.bms_raw} |
| Failure adj | {card.bms_failure_adj} |
| Volume adj | {card.bms_volume_adj} |
| Altitude adj | {card.bms_altitude_adj} |
| **Score** | **{card.bms_score}** |
| Threshold | `{card.bms_threshold}` |

## Stack
{chr(10).join(f"- {s}" for s in card.primary_stack)}

## Quality gates
{chr(10).join(f"- `{g}`" for g in card.quality_gates)}

## Engines wired

- **Diamond sigma target**: `{card.engine_refs.diamond_sigma_target}` (D1=+30, D2=+5, D3=0)
- **DV Research engines**: {", ".join("`" + e + "`" for e in card.engine_refs.dv_research) or "_(only fires at Research step)_"}
- **DV Quality gates**: {", ".join("`" + e + "`" for e in card.engine_refs.dv_quality_gates) or "_(only fires at Quality step)_"}
- **Prediction engines**: {", ".join("`" + p + "`" for p in card.engine_refs.predictions) or "_(only fires at Quality step)_"}

## Operations
- **Cost band**: `{card.cost_band_usd}`
- **Approval policy**: `{card.approval_policy}`
- **Proof policy**: `{card.proof_policy}`
- **Audit policy**: `{card.audit_policy}`
- **Escalation**: `{card.escalation_policy}`
- **Runtime entrypoint**: `{card.runtime_entrypoint}`

## Question bank ({len(card.question_bank)} entries)

{chr(10).join(f"- **`{q.id}`** [{q.severity}] {q.text}" for q in card.question_bank[:10])}

_+{max(0, len(card.question_bank) - 10)} more — full bank in YAML._

## Governance
- Next re-score: `{card.next_rescore}`
- Recalibration cron: `{card.recalibration_cron}`
- Drift trigger: `{card.drift_trigger}`
"""
