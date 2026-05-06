import streamlit as st

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="Yield Equilibrium Analyzer", layout="wide")

st.markdown("""
<style>
    .noi-card { background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #1e3799; }
    .main-header { color: #1e3799; font-weight: 900; text-transform: uppercase; }
</style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR SIMULATION CONTROLS ---
st.sidebar.markdown("### 📊 Pillar 01: Simulation")
# Simulation bar for 5 to 10,000 rooms as requested
sim_rooms = st.sidebar.slider("Simulate Room Inventory Shift", 5, 10000, 40)
st.sidebar.info(f"Analyzing the impact of shifting {sim_rooms} rooms.")

# --- 3. INPUT DATA ---
st.markdown("<h1 class='main-header'>Yield Equilibrium Displacement Analyzer</h1>", unsafe_allow_html=True)
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

# --- 4. NOI IMPACT CALCULATIONS ---
# Compare Segment A (Target) vs Segment B (Displaced)
baseline_noi = net_b * sim_rooms
projected_noi = net_a * sim_rooms
improvement_val = projected_noi - baseline_noi
improvement_pct = (improvement_val / baseline_noi) * 100 if baseline_noi != 0 else 0

# --- 5. EXECUTIVE DASHBOARD ---
st.divider()
st.markdown("### 📈 Forecasting & NOI Impact")

m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Net Flow (A-B)", f"﷼ {net_a - net_b:,.2f}")
with m2:
    st.metric("Total NOI Gain", f"﷼ {improvement_val:,.2f}")
with m3:
    st.metric("NOI % Improvement", f"{improvement_pct:.2f}%")

# Summary Card
status = "REJECT: DILUTIVE" if net_a < net_b else "ACCEPT: ACCRETIVE"
st.markdown(f"""
<div class='noi-card'>
    <h4>Executive Verdict: {status}</h4>
    By shifting <b>{sim_rooms} rooms</b> to Segment A, the protocol identifies a 
    <b>{improvement_pct:.2f}%</b> improvement in departmental NOI, 
    adding <b>﷼ {improvement_val:,.2f}</b> to the bottom line.
</div>
""", unsafe_allow_html=True)

# --- 6. DATA HANDOFF & NAVIGATION ---
st.session_state["current_audit"] = {
    "label": "Direct vs Group Simulation",
    "yield": net_a,
    "hurdle": net_b,
    "status": status,
    "improvement": improvement_pct,
    "rooms": sim_rooms
}

st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 Run Pillar 02: Strategic AI Audit"):
    st.switch_page("pages/strategic_gem.py")
