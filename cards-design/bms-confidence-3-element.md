# BMS Confidence — 3-Element Card

**Status**: 🟡 STUB.
**Drives**: `lattice/confidence_elements.py` and the BMS formula in `lattice/score.py`.
**Z-axis source of truth.**

The Build Mode Score (BMS) is composed of one base + two adjustments:

```
BMS = clamp(RAW + ADJ_failure + ADJ_volume + ADJ_altitude, 0, 1)
```

ADJ_altitude is implicit in the X-axis (it shifts with altitude position), so the Z-axis surfaces the **three independent confidence contributors**:

1. **RAW** — `Σ(C_i / 5) / 20`. The unadjusted average of all 20 scoring criteria.
2. **ADJ_failure** — failure-cost lift. `+0.15 if C1 ≥ 4 else +0.05 if C1 == 3 else 0`.
3. **ADJ_volume** — throughput lift. `0.10 * (C11 / 5)`.

Each is evaluated per IQRSQPI step, giving 3 × 7 = 21 Z-axis positions.

---

## Section template (fill 21 times)

For each (confidence_element, step):
1. **What it measures at this step**: one sentence.
2. **Why it matters at this step**: what bad outcome happens if confidence is low here?
3. **What raises it**: levers that increase confidence.
4. **What lowers it**: signals/anti-patterns that lower confidence.
5. **Failure mode**: what happens when this element is the *limiting* contributor.

---

## RAW × IQRSQPI (7 entries)

### RAW @ I1 — Intent
- **What**:
- **Why**:
- **Raises**:
- **Lowers**:
- **Failure mode**:

### RAW @ Q1 — Question
- **What**:
- **Why**:
- **Raises**:
- **Lowers**:
- **Failure mode**:

### RAW @ R — Research
### RAW @ S — Solution
### RAW @ Q2 — Quality
### RAW @ P — Proof
### RAW @ I2 — Integrate

---

## ADJ_FAILURE × IQRSQPI (7 entries)

### ADJ_FAILURE @ I1 — Intent
- **What**:
- **Why**:
- **Raises**:
- **Lowers**:
- **Failure mode**:

### ADJ_FAILURE @ Q1 — Question
### ADJ_FAILURE @ R — Research
### ADJ_FAILURE @ S — Solution
### ADJ_FAILURE @ Q2 — Quality
### ADJ_FAILURE @ P — Proof
### ADJ_FAILURE @ I2 — Integrate

---

## ADJ_VOLUME × IQRSQPI (7 entries)

### ADJ_VOLUME @ I1 — Intent
- **What**:
- **Why**:
- **Raises**:
- **Lowers**:
- **Failure mode**:

### ADJ_VOLUME @ Q1 — Question
### ADJ_VOLUME @ R — Research
### ADJ_VOLUME @ S — Solution
### ADJ_VOLUME @ Q2 — Quality
### ADJ_VOLUME @ P — Proof
### ADJ_VOLUME @ I2 — Integrate

---

## After authoring

1. Replace stubs in `lattice/confidence_elements.py` with content from this card.
2. Run `python -m lattice.generator` to regenerate all 3,087 cards.
