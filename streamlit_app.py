import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("Interaction Dynamics Lab")
st.write(
    "This instrument visualizes long-form conversational dynamics using "
    "derived, non-semantic metrics from selected example threads."
)

DATA_DIR = "/app/src"

FILES = {
    "Anchor": f"{DATA_DIR}/Anchor_turns.csv",
    "Big Flame": f"{DATA_DIR}/BigFlame_turns.csv",
}

# ---- Load selected thread ----
thread_name = st.selectbox("Select thread", list(FILES.keys()))
csv_path = FILES[thread_name]

df = pd.read_csv(csv_path).sort_values("turn")

# ---- Controls ----
roll_window = st.slider("Rolling window (turns)", 5, 150, 25)
show_band = st.checkbox("Show mean ± variance band", value=True)
k = st.slider("Band width (σ multiplier)", 0.5, 3.0, 1.0, 0.5)

scope = st.radio(
    "Compute stability on:",
    ["GPT turns only", "All turns"],
    horizontal=True
)

st.subheader("Stability Detection")
sigma_thresh = st.slider("Stability threshold (σ)", 10.0, 300.0, 80.0, 5.0)
persist_len = st.slider("Required persistence (turns)", 10, 200, 50)

# ---- Choose series for stability stats ----
if scope == "GPT turns only":
    dstat = df[df["speaker"] == "gpt"].copy()
else:
    dstat = df.copy()

dstat["tokens_est"] = pd.to_numeric(dstat["tokens_est"], errors="coerce").fillna(0)

# Rolling mean & std
dstat["roll_mean"] = dstat["tokens_est"].rolling(roll_window, min_periods=1).mean()
dstat["roll_std"]  = dstat["tokens_est"].rolling(roll_window, min_periods=1).std().fillna(0)

# ---- Time-to-stability detection ----
stability_turn = None
roll_std = dstat["roll_std"].to_numpy()
turns = dstat["turn"].to_numpy()

if len(roll_std) > persist_len:
    for i in range(len(roll_std) - persist_len):
        std_slice = roll_std[i:i + persist_len]
        if (std_slice <= sigma_thresh).all():
            stability_turn = int(turns[i])
            break

# Variance band bounds
dstat["upper"] = dstat["roll_mean"] + (k * dstat["roll_std"])
dstat["lower"] = (dstat["roll_mean"] - (k * dstat["roll_std"])).clip(lower=0)

# ---- Plot ----
fig = px.scatter(
    df,
    x="turn",
    y="tokens_est",
    color="speaker",
    opacity=0.6,
    title="Conversation Rhythm",
)

# Rolling mean line
fig.add_scatter(
    x=dstat["turn"],
    y=dstat["roll_mean"],
    mode="lines",
    name=f"Rolling mean ({scope.lower()}, w={roll_window})",
)

# Variance band
if show_band:
    fig.add_scatter(
        x=dstat["turn"],
        y=dstat["lower"],
        mode="lines",
        line=dict(width=0),
        showlegend=False,
        name="Lower bound",
    )
    fig.add_scatter(
        x=dstat["turn"],
        y=dstat["upper"],
        mode="lines",
        fill="tonexty",
        name=f"± {k}σ band",
        opacity=0.2,
    )

# Stability marker line
if stability_turn is not None:
    fig.add_vline(
        x=stability_turn,
        line_dash="dot",
        line_color="green",
        annotation_text="Stability onset",
        annotation_position="top left",
    )

st.plotly_chart(fig, use_container_width=True)

# ---- Report ----
if stability_turn is not None:
    st.success(f"Stability detected at turn {stability_turn} (σ ≤ {sigma_thresh} for {persist_len} turns)")
else:
    st.warning("No stable regime detected under current parameters.")
