"""Adapter to the prediction engines (MiroFish / MiroShark / MilkyWay).

Bridges the lattice's Quality step (D1/D2/D3) into Mike's prediction layer:

    MiroFish  — 6-criterion scoring (Hook, Personalization, CTA Clarity,
                Behavioral Hook, Authority Signal, Reply Probability).
                Threshold 8.5/10.
    MiroShark — Full predictive app at miroshark-src/. Calibrated probabilities
                over campaign / asset outcomes.
    MilkyWay  — Build-book at docs/protocols/milkyway-mirofish-build-book.md.
                Long-horizon, ensemble forecasting layer.

All three feed a unified PredictionPacket so the lattice's Quality step can
treat them as interchangeable predictors with Brier-trackable outputs.

Public API:

    is_available() -> bool
    miro_fish_score(text, persona) -> dict       # 6-criterion scores
    miro_shark_predict(seed, horizon) -> dict    # calibrated outcome probabilities
    milkyway_forecast(seed, horizon) -> dict     # long-horizon ensemble
    predictive_swarm(seed, ...) -> dict          # run all three, return packet
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Literal

from ..build_card import Diamond

# Resolve repo root for sibling lookups
REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent / "Startup-Intelligence-OS"

MIROFISH_VALIDATOR = REPO_ROOT / "mirofish_validation_v2.py"
MIROSHARK_SRC = REPO_ROOT / "miroshark-src"
MILKYWAY_BUILDBOOK = REPO_ROOT / "docs" / "protocols" / "milkyway-mirofish-build-book.md"

MIRO_FISH_CRITERIA = [
    "hook_strength",
    "personalization_depth",
    "cta_clarity",
    "behavioral_hook",
    "authority_signal",
    "reply_probability",
]

MIRO_FISH_THRESHOLD = 8.5


def is_available() -> dict[str, bool]:
    return {
        "mirofish": MIROFISH_VALIDATOR.exists(),
        "miroshark": MIROSHARK_SRC.exists(),
        "milkyway": MILKYWAY_BUILDBOOK.exists(),
    }


def miro_fish_score(text: str, persona: dict[str, Any] | None = None) -> dict[str, Any]:
    """Score `text` on MiroFish's 6 criteria.

    Returns: { criterion -> 0..10 float, "overall": float, "passed": bool }
    """
    persona = persona or {}
    scores: dict[str, float] = {c: 0.0 for c in MIRO_FISH_CRITERIA}

    # Heuristic implementation. Replace with call to mirofish_validation_v2.py
    # when env (OPENAI_API_KEY) is wired into the studio runtime.
    wc = max(len(text.split()), 1)
    sl = text.lower()

    scores["hook_strength"] = min(10.0, 10 * (sl.count("?") + sl.count("!")) / max(wc / 50, 1))
    scores["personalization_depth"] = 10.0 if persona else 0.0
    scores["cta_clarity"] = min(10.0, 10 * sum(1 for tok in ["reply", "book", "click", "schedule", "respond"] if tok in sl) / 2)
    scores["behavioral_hook"] = min(10.0, 10 * sum(1 for tok in ["why", "because", "discovered", "noticed"] if tok in sl) / 2)
    scores["authority_signal"] = min(10.0, 10 * sum(1 for tok in ["data", "research", "study", "%", "$"] if tok in sl) / 3)
    scores["reply_probability"] = sum(scores.values()) / 5

    overall = sum(scores.values()) / len(scores)
    return {
        "criteria": scores,
        "overall": round(overall, 2),
        "passed": overall >= MIRO_FISH_THRESHOLD,
        "threshold": MIRO_FISH_THRESHOLD,
        "implementation": "heuristic-v0",
    }


def miro_shark_predict(seed: str, horizon: str = "30d") -> dict[str, Any]:
    """Calibrated outcome probability for `seed` over `horizon`.

    Stub returns a uniform-prior baseline so the Quality step can wire end-to-end
    before MiroShark runtime is bridged. The miroshark-src/ app is the production
    backend; this adapter is the call boundary.
    """
    return {
        "seed_hash": hash(seed) & 0xFFFFFFFF,
        "horizon": horizon,
        "probability": 0.5,
        "confidence": 0.0,
        "brier_baseline": None,
        "implementation": "stub-uniform-prior",
        "next_step": "Bridge to miroshark-src/ runtime via HTTP or subprocess.",
    }


def milkyway_forecast(seed: str, horizon: str = "90d") -> dict[str, Any]:
    """Long-horizon ensemble forecast.

    Stub. See docs/protocols/milkyway-mirofish-build-book.md for the full
    protocol. The Quality step calls this for >30-day predictions where
    MiroShark alone is insufficient.
    """
    return {
        "seed_hash": hash(seed) & 0xFFFFFFFF,
        "horizon": horizon,
        "ensemble_size": 0,
        "median_outcome": None,
        "confidence_interval": None,
        "implementation": "stub",
        "next_step": "Implement per docs/protocols/milkyway-mirofish-build-book.md.",
    }


def predictive_swarm(
    seed: str,
    horizon: str = "30d",
    persona: dict[str, Any] | None = None,
    diamond: Diamond = Diamond.D2,
) -> dict[str, Any]:
    """Run the full predictive challenge layer.

    D1: predictions run on each candidate sketch (broad).
    D2: predictions run on the converged solution + falsifier (narrow).
    D3: predictions compared against past Brier baseline (forensic).
    """
    return {
        "diamond": diamond.value,
        "mirofish": miro_fish_score(seed, persona),
        "miroshark": miro_shark_predict(seed, horizon),
        "milkyway": milkyway_forecast(seed, horizon),
        "synthesis": _synthesize(seed, diamond),
    }


def _synthesize(seed: str, diamond: Diamond) -> dict[str, Any]:
    """Diamond-aware synthesis stub. D1 reports diversity, D2 reports confidence,
    D3 reports drift vs baseline."""
    base = {"diamond": diamond.value}
    if diamond == Diamond.D1:
        base["focus"] = "diversity_across_candidates"
    elif diamond == Diamond.D2:
        base["focus"] = "single_solution_confidence"
    else:
        base["focus"] = "drift_vs_baseline"
    return base
