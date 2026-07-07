# sinecossum.py
import numpy as np
import streamlit as st
import plotly.graph_objects as go
st.set_page_config(page_title="EE261 SineCosSum", layout="wide")
# CSS for the Streamlit layout
st.markdown("""
<style>
html, body, [data-testid="stAppViewContainer"] {
   height: 100vh;
   overflow: hidden;
}
[data-testid="stHeader"] {
   display: none;
}
.main .block-container {
   height: 100vh;
   max-width: 100%;
   padding: 1rem 1.5rem 0 1.5rem;
   overflow: hidden;
}
div[data-testid="column"]:first-of-type {
   height: calc(100vh - 110px);
   overflow-y: auto;
   overflow-x: hidden;
   padding-right: 1rem;
   border-right: 1px solid rgba(128,128,128,0.25);
}
div[data-testid="column"]:nth-of-type(2) {
   height: calc(100vh - 110px);
   overflow: hidden;
   padding-left: 1rem;
}
div[data-testid="stButton"] button {
   width: 100%;
   border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)
st.title("EE 261 SineCosSum")

# If the Streamlit session state does not already have harmonic list, initialize it with a single harmonic
if "harmonics" not in st.session_state:
   st.session_state.harmonics = [
       {"enabled": True, "kind": "sin", "amp": 5, "n": 1, "freq": 1, "phase": 0},
       
   ]
# Similar to above, except for A0
if "A0" not in st.session_state:
   st.session_state.A0 = 0

def add_harmonic():
   next_n = len(st.session_state.harmonics) + 1
   st.session_state.harmonics.append(
       {"enabled": True, "kind": "sin", "amp": 1, "n": next_n, "freq": 1, "phase": 0}
   )

def remove_harmonic():
   if st.session_state.harmonics:
       st.session_state.harmonics.pop()

# Builds the equation for display purposes based on the harmonics configured
def build_equation(harmonics, A0):
   parts = [f"{A0}"]
   for h in harmonics:
       if not h["enabled"]:
           continue
       sign = "+" if h["amp"] >= 0 else "-"
       amp = abs(h["amp"])
       parts.append(
           f"{sign} {amp}{h['kind']}(2π·{h['n']}·{h['freq']}·t + {h['phase']})"
       )
   return "f(t) = " + " ".join(parts)

# Calculates the waveform values
def compute_wave(t, harmonics, A0):
   y = np.full_like(t, A0, dtype=float)
   for h in harmonics:
       if not h["enabled"]:
           continue
       angle = 2 * np.pi * h["n"] * h["freq"] * t + h["phase"]
       if h["kind"] == "sin":
           y += h["amp"] * np.sin(angle)
       else:
           y += h["amp"] * np.cos(angle)
   return y

# Creates the two Streamlit columns for the wave, the left pane for harmonic definition and the right pane for graphing
left, right = st.columns([1, 2.6], gap="large")

# Contains the code for all of the components in the left pane
with left:
   st.subheader("Harmonic Table")
   st.session_state.A0 = st.number_input(
       "DC offset/zeroeth Fourier coefficient A₀",
       value=int(st.session_state.A0),
       step=1,
       format="%d",
   )
   c_add, c_remove, c_update = st.columns([1, 1, 2])
   if c_add.button("🟢 +"):
       add_harmonic()
   if c_remove.button("🔴 −"):
       remove_harmonic()
   update_clicked = c_update.button("Update Wave")
   st.caption("Columns: enabled | type | amplitude | harmonic n | frequency multiplier | phase ")
   for i, h in enumerate(st.session_state.harmonics):
       cols = st.columns([0.65, 0.9, 1, 1, 1, 1])
       enabled = cols[0].checkbox("", value=h["enabled"], key=f"enabled_{i}")
       kind = cols[1].selectbox(
           "",
           ["sin", "cos"],
           index=0 if h["kind"] == "sin" else 1,
           key=f"kind_{i}",
       )
       amp = cols[2].number_input(
           "",
           value=int(h["amp"]),
           step=1,
           format="%d",
           key=f"amp_{i}",
       )
       n = cols[3].number_input(
           "",
           value=int(h["n"]),
           min_value=1,
           step=1,
           format="%d",
           key=f"n_{i}",
       )
       freq = cols[4].number_input(
           "",
           value=int(h["freq"]),
           min_value=1,
           step=1,
           format="%d",
           key=f"freq_{i}",
       )
       phase = cols[5].number_input(
           "",
           value=int(h["phase"]),
           step=1,
           format="%d",
           key=f"phase_{i}",
       )
       if update_clicked:
           st.session_state.harmonics[i] = {
               "enabled": enabled,
               "kind": kind,
               "amp": amp,
               "n": n,
               "freq": freq,
               "phase": phase,
           }
   st.subheader("Current Equation")
   st.code(build_equation(st.session_state.harmonics, st.session_state.A0))
t = np.linspace(-1, 1, 3000)
y = compute_wave(t, st.session_state.harmonics, st.session_state.A0)

# Contains the graphing components for the right pane
with right:
   title_col, mode_col = st.columns([3, 1])
   with title_col:
       st.subheader("Live Plot")
   with mode_col:
       use_3d = st.checkbox("3D", value=False)
   if not use_3d:
       fig = go.Figure()
       fig.add_trace(
           go.Scatter(
               x=t,
               y=y,
               mode="lines",
               name="f(t)",
           )
       )
       fig.add_vline(x=0, line_width=2, line_dash="solid")
       fig.add_hline(y=0, line_width=4, line_dash="solid")
       fig.update_layout(
           title="Fourier Harmonic Sum",
           xaxis_title="t",
           yaxis_title="f(t)",
           height=700,
           margin=dict(l=40, r=30, t=60, b=40),
       )
       st.plotly_chart(fig, use_container_width=True)
   else:
       fig = go.Figure()
       fig.add_trace(
           go.Scatter3d(
               x=t,
               y=np.sin(2 * np.pi * t),
               z=y,
               mode="lines",
               name="3D Fourier curve",
           )
       )
       fig.update_layout(
           title="3D Fourier Harmonic Sum",
           scene=dict(
               xaxis_title="t",
               yaxis_title="oscillation axis",
               zaxis_title="f(t)",
           ),
           height=700,
           margin=dict(l=0, r=0, t=60, b=0),
       )
       st.plotly_chart(fig, use_container_width=True)
   st.caption("Edit harmonic rows on the left, then click Update Wave.")
