"""RIG Lattice 3D Viewer — Streamlit + Plotly.

Reads viz/lattice_index.json (produced by `python -m lattice.generator`)
and renders the 7 x 21 x 21 = 3,087-cell lattice as a 3D scatter you can
rotate, filter, and hover.

Run:
    streamlit run viz/streamlit_plotly_app.py
"""
from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(
    page_title="RIG Lattice 3D",
    layout="wide",
    initial_sidebar_state="expanded",
)

INDEX_PATH = Path(__file__).parent / "lattice_index.json"

MODE_COLORS = {
    "PYTHON_ONLY": "#22c55e",     # green
    "HYBRID": "#eab308",           # yellow
    "AGENT_BOUNDED": "#f97316",    # orange
    "LLM_AGENT_FREE": "#ef4444",   # red
}

ALTITUDE_ORDER = ["L1", "L2", "L3", "L4", "L5", "L6", "L7"]
STEP_ORDER = ["I1", "Q1", "R", "S", "Q2", "P", "I2"]
DIAMOND_ORDER = ["D1", "D2", "D3"]
CONFIDENCE_ORDER = ["RAW", "ADJ_FAILURE", "ADJ_VOLUME"]


@st.cache_data
def load_index() -> pd.DataFrame:
    if not INDEX_PATH.exists():
        st.error(
            f"`{INDEX_PATH.name}` not found. Run `python -m lattice.generator` first."
        )
        st.stop()
    data = json.loads(INDEX_PATH.read_text())
    df = pd.DataFrame(data)

    # Build numeric Y and Z positions for the 3D scatter
    df["y_diamond_idx"] = df["diamond_y"].map({d: i for i, d in enumerate(DIAMOND_ORDER)})
    df["y_step_idx"] = df["step_y"].map({s: i for i, s in enumerate(STEP_ORDER)})
    df["y_pos"] = df["y_diamond_idx"] * 7 + df["y_step_idx"]  # 0..20

    df["z_conf_idx"] = df["confidence_element_z"].map({c: i for i, c in enumerate(CONFIDENCE_ORDER)})
    df["z_step_idx"] = df["step_z"].map({s: i for i, s in enumerate(STEP_ORDER)})
    df["z_pos"] = df["z_conf_idx"] * 7 + df["z_step_idx"]  # 0..20

    df["y_label"] = df["diamond_y"] + "." + df["step_y"]
    df["z_label"] = df["confidence_element_z"] + "." + df["step_z"]

    return df


def main() -> None:
    st.title("RIG Lattice 3D Viewer")
    st.caption(
        "7 altitudes × (3 diamonds × 7 IQRSQPI) × (3 BMS confidence × 7 IQRSQPI) = **3,087 cells**"
    )

    df = load_index()

    st.sidebar.header("Filters")
    selected_modes = st.sidebar.multiselect(
        "Build modes", list(MODE_COLORS.keys()), default=list(MODE_COLORS.keys()),
    )
    selected_altitudes = st.sidebar.multiselect(
        "Altitudes", ALTITUDE_ORDER, default=ALTITUDE_ORDER,
    )
    selected_diamonds = st.sidebar.multiselect(
        "Diamonds (Y)", DIAMOND_ORDER, default=DIAMOND_ORDER,
    )
    selected_confidence = st.sidebar.multiselect(
        "Confidence elements (Z)", CONFIDENCE_ORDER, default=CONFIDENCE_ORDER,
    )
    bms_range = st.sidebar.slider("BMS range", 0.0, 1.0, (0.0, 1.0), 0.05)

    mask = (
        df["mode"].isin(selected_modes)
        & df["altitude"].isin(selected_altitudes)
        & df["diamond_y"].isin(selected_diamonds)
        & df["confidence_element_z"].isin(selected_confidence)
        & df["bms"].between(*bms_range)
    )
    view = df[mask].copy()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Cells shown", f"{len(view):,}")
    for col, mode in zip([col2, col3, col4], ["PYTHON_ONLY", "HYBRID", "AGENT_BOUNDED"]):
        col.metric(mode, f"{(view['mode'] == mode).sum():,}")

    fig = px.scatter_3d(
        view,
        x="altitude_index",
        y="y_pos",
        z="z_pos",
        color="mode",
        color_discrete_map=MODE_COLORS,
        size="bms",
        size_max=12,
        opacity=0.75,
        hover_data={
            "cell_id": True,
            "altitude": True,
            "y_label": True,
            "z_label": True,
            "bms": ":.3f",
            "contribution": ":.3f",
            "altitude_index": False,
            "y_pos": False,
            "z_pos": False,
        },
        title="3D Lattice — drag to rotate",
    )
    fig.update_layout(
        height=750,
        scene=dict(
            xaxis=dict(
                title="X — Altitude (L1 → L7)",
                tickmode="array",
                tickvals=list(range(7)),
                ticktext=ALTITUDE_ORDER,
            ),
            yaxis=dict(
                title="Y — Triple Diamond × IQRSQPI (21)",
                tickmode="array",
                tickvals=list(range(21)),
                ticktext=[f"{d}.{s}" for d in DIAMOND_ORDER for s in STEP_ORDER],
            ),
            zaxis=dict(
                title="Z — BMS Confidence × IQRSQPI (21)",
                tickmode="array",
                tickvals=list(range(21)),
                ticktext=[f"{c}.{s}" for c in CONFIDENCE_ORDER for s in STEP_ORDER],
            ),
        ),
    )
    st.plotly_chart(fig, use_container_width=True)

    with st.expander("Table view (raw cells)"):
        st.dataframe(
            view[["cell_id", "altitude", "y_label", "z_label", "bms", "mode", "contribution"]],
            use_container_width=True,
            height=400,
        )

    with st.expander("Mode distribution heatmap (altitude × Y)"):
        pivot = view.pivot_table(
            index="altitude", columns="y_label", values="bms", aggfunc="mean",
        )
        pivot = pivot.reindex(ALTITUDE_ORDER)
        st.dataframe(pivot.style.background_gradient(cmap="RdYlGn"), use_container_width=True)


if __name__ == "__main__":
    main()
