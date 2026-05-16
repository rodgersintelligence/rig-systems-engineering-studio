# Triple Diamond 21-Step Process — Y-Axis Source of Truth

**Status**: 🟡 STUB — author content for each of the 21 (diamond, step) entries.
**Drives**: `lattice/step_semantics.py` — every BuildCard's `diamond_step_semantic` field.
**Priority**: Highest. Generator content depends on this card.

The Y-axis of the 3D lattice is 21 wide because each of the 3 diamonds runs its own full 7-step IQRSQPI process. Below: one section per (diamond, step) combination. Fill in the 5 bullets per section.

---

## Section template (fill 21 times)

For each (diamond, step):
1. **Name**: 3–5 word label.
2. **Purpose**: one sentence. Why this step exists in *this* diamond.
3. **Inputs**: structured data this step consumes.
4. **Outputs**: structured artifact this step produces.
5. **Gates that fire**: which RIG gates run at this step in this diamond.

---

## D1 — DISCOVERY (divergent, opens the problem space)

### D1.I1 — Intent
- **Name**: Divergent Intent Capture
- **Purpose**:
- **Inputs**:
- **Outputs**:
- **Gates**:

### D1.Q1 — Question
- **Name**: Open-Frame Questioning
- **Purpose**:
- **Inputs**:
- **Outputs**:
- **Gates**:

### D1.R — Research
- **Name**: Wide-Aperture Research
- **Purpose**:
- **Inputs**:
- **Outputs**:
- **Gates**:

### D1.S — Solution
- **Name**: Possibility Sketching
- **Purpose**:
- **Inputs**:
- **Outputs**:
- **Gates**:

### D1.Q2 — Quality
- **Name**: Coverage Check
- **Purpose**:
- **Inputs**:
- **Outputs**:
- **Gates**:

### D1.P — Proof
- **Name**: Exploration Receipt
- **Purpose**:
- **Inputs**:
- **Outputs**:
- **Gates**:

### D1.I2 — Integrate
- **Name**: Frame Selection
- **Purpose**:
- **Inputs**:
- **Outputs**:
- **Gates**:

---

## D2 — SOLUTION (converge, bind to mechanism, ship)

### D2.I1 — Intent
- **Name**: Mechanism-Bound Intent
- **Purpose**:
- **Inputs**:
- **Outputs**:
- **Gates**:

### D2.Q1 — Question
- **Name**: Decomposed Sub-Questions
- **Purpose**:
- **Inputs**:
- **Outputs**:
- **Gates**:

### D2.R — Research
- **Name**: Source-Per-Claim Research
- **Purpose**:
- **Inputs**:
- **Outputs**:
- **Gates**:

### D2.S — Solution
- **Name**: Schema-Bound Synthesis
- **Purpose**:
- **Inputs**:
- **Outputs**:
- **Gates**:

### D2.Q2 — Quality
- **Name**: Gate Stack Run
- **Purpose**:
- **Inputs**:
- **Outputs**:
- **Gates**:

### D2.P — Proof
- **Name**: Falsification Charter
- **Purpose**:
- **Inputs**:
- **Outputs**:
- **Gates**:

### D2.I2 — Integrate
- **Name**: Dispatch + Audit
- **Purpose**:
- **Inputs**:
- **Outputs**:
- **Gates**:

---

## D3 — EVOLUTION (measure drift, recalibrate, retire/rescore)

### D3.I1 — Intent
- **Name**: Drift-Triggered Intent
- **Purpose**:
- **Inputs**:
- **Outputs**:
- **Gates**:

### D3.Q1 — Question
- **Name**: What Broke / Why Now
- **Purpose**:
- **Inputs**:
- **Outputs**:
- **Gates**:

### D3.R — Research
- **Name**: Brier Score + Rollback Forensics
- **Purpose**:
- **Inputs**:
- **Outputs**:
- **Gates**:

### D3.S — Solution
- **Name**: Recalibration Patch
- **Purpose**:
- **Inputs**:
- **Outputs**:
- **Gates**:

### D3.Q2 — Quality
- **Name**: Regression Check
- **Purpose**:
- **Inputs**:
- **Outputs**:
- **Gates**:

### D3.P — Proof
- **Name**: Re-Score Receipt
- **Purpose**:
- **Inputs**:
- **Outputs**:
- **Gates**:

### D3.I2 — Integrate
- **Name**: Cascade Update
- **Purpose**:
- **Inputs**:
- **Outputs**:
- **Gates**:

---

## After authoring

1. Replace stubs in `lattice/step_semantics.py` with content from this card.
2. Run `python -m lattice.generator` to regenerate all 3,087 cards.
3. Open `viz/streamlit_plotly_app.py` to see the lattice with new semantics.
