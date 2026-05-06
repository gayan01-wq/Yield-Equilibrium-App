import streamlit as st

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="Yield Equilibrium Analyzer", layout="wide")

st.markdown("""
<style>
    .main-header { 
        color: #1e3799; 
        font-weight: 900; 
        text-transform: uppercase; 
        letter-spacing: 1px;
    }
    .noi-card { 
        background-color: #f0f2f6; 
        padding: 25px; 
        border-radius: 12px; 
        border-left: 10px solid #1e3799; 
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        color: #2f3640;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR SIMULATION CONTROLS ---
st.sidebar.markdown("### 📊 Pillar 01: Simulation")
# The simulation bar for 5 to 10,000 rooms as requested
sim_rooms = st.sidebar.slider("Simulate Room Inventory Shift", 5, 10000, 40)
st.sidebar.info(f"Analyzing the impact of shifting {sim_rooms} rooms between segments.")

# --- 3. INPUT DATA ---
st.markdown("<h1 class='main-header'>Yield Equilibrium Displacement Analyzer</h1>", unsafe_allow_html=True)
st.markdown("### Pillar 01: Total Net-Flow Logic")
st.divider()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Segment A: Direct / FIT")
    adr_a = st.number_input("ADR (A)", value=85.0)
    cost_a = st.number_input("Cost per Room (A)", value=15.0)
    net_a = adr_a - cost_a

with col2:
    st.subheader("Segment B: Group / Wholesale")
    adr_b = st.number_input("ADR (B)", value=65.0)
    cost_b = st.number_input("Cost per Room (B)", value=10.0)
    net_b = adr_b - cost_b

# --- 4. FORECASTING & NOI CALCULATIONS ---
# Calculate the total value of the shift based on the Simulation Bar
baseline_noi = net_b * sim_rooms
projected_noi = net_a * sim_rooms
improvement_val = projected_noi - baseline_noi

# Calculate % Improvement (NOI Growth)
improvement_pct = (improvement_val / baseline_noi) * 100 if baseline_noi != 0 else 0

# --- 5. EXECUTIVE DASHBOARD ---
st.divider()
st.markdown("### 📈 Forecasting Impact & Equilibrium Audit")

m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Net Flow (A-B)", f"﷼ {net_a - net_b:,.2f}")
with m2:
    st.metric("Total NOI Gain", f"﷼ {improvement_val:,.2f}")
with m3:
    st.metric("NOI % Improvement", f"{improvement_pct:.2f}%")

# Status Verdict
status = "REJECT: DILUTIVE" if net_a < net_b else "ACCEPT: ACCRETIVE"

# Summary Card
st.markdown(f"""
<div class='noi-card'>
    <h4>Executive Summary: {status}</h4>
    By shifting <b>{sim_rooms} rooms</b> from Segment B to Segment A, the 
    <b>Yield Equilibrium Protocol</b> identifies a <b>{improvement_pct:.2f}%</b> 
    improvement in departmental NOI, contributing an additional 
    <b>﷼ {improvement_val:,.2f}</b> to the total net-flow.
</div>
""", unsafe_allow_html=True)

# --- 6. DATA HANDOFF & NAVIGATION ---
# Ensuring variables are passed to Pillar 02 (Strategic Gem)
st.session_state["current_audit"] = {
    "label": "Direct/FIT vs Group Simulation",
    "yield": net_a,
    "hurdle": net_b,
    "status": status,
    "improvement": improvement_pct,
    "rooms": sim_rooms
}

st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 Run Pillar 02: Strategic AI Audit"):
    st.switch_page("pages/strategic_gem.py")
