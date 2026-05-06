import streamlit as st

# --- 1. SETTINGS & STYLING ---
st.set_page_config(page_title="Yield Equilibrium Analyzer", layout="wide")

st.markdown("""
<style>
    .main-header { color: #1e3799; font-weight: 900; text-transform: uppercase; letter-spacing: 1px; }
    .noi-card { 
        background-color: #f8f9fa; padding: 25px; border-radius: 12px; 
        border-left: 10px solid #1e3799; box-shadow: 0 4px 6px rgba(0,0,0,0.1); color: #2f3640;
    }
</style>
""", unsafe_allow_html=True)

# --- 2. SIDEBAR: STATUTORY DEFLATORS & SIMULATION ---
st.sidebar.markdown("### 🏛️ Statutory Deflators (Oman)")
# Defaulting to Oman market standards (VAT 5%, Muni 4%, Service Charge 8%)
vat = st.sidebar.number_input("VAT (%)", value=5.0) / 100
muni_tax = st.sidebar.number_input("Municipality Tax (%)", value=4.0) / 100
service_charge = st.sidebar.number_input("Service Charge (%)", value=8.0) / 100

st.sidebar.divider()
st.sidebar.markdown("### 📊 Pillar 01: Simulation")
# Room inventory simulation bar (5 - 10,000)
sim_rooms = st.sidebar.slider("Simulate Room Inventory Shift", 5, 10000, 40)

# --- 3. INPUT DATA: SEGMENTS & MEAL PACKAGES ---
st.markdown("<h1 class='main-header'>Yield Equilibrium Displacement Analyzer</h1>", unsafe_allow_html=True)
st.markdown("### Pillar 01: Total Net-Flow & Statutory Deflators")
st.divider()

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown("### Segment A: Direct / FIT")
    adr_a = st.number_input("Gross ADR (A)", value=85.0, key="adr_a")
    meal_a = st.number_input("Meal Package Cost (A)", value=5.0)
    commission_a = st.number_input("Comm/Transaction % (A)", value=0.0) / 100
    
    # Calculation: Backing out taxes to get Net Room Revenue
    total_tax_multiplier = 1 + vat + muni_tax + service_charge
    net_adr_a = adr_a / total_tax_multiplier
    net_a = (net_adr_a * (1 - commission_a)) - meal_a

with col2:
    st.markdown("### Segment B: Group / Wholesale")
    adr_b = st.number_input("Gross ADR (B)", value=65.0, key="adr_b")
    meal_b = st.number_input("Meal Package Cost (B)", value=8.0)
    commission_b = st.number_input("Comm/Transaction % (B)", value=15.0) / 100
    
    # Calculation: Backing out taxes to get Net Room Revenue
    net_adr_b = adr_b / total_tax_multiplier
    net_b = (net_adr_b * (1 - commission_b)) - meal_b

# --- 4. MARGINAL FLOOR & NOI LOGIC ---
# Segment B net-flow acts as the Marginal Floor (Hurdle)
marginal_floor = net_b 
displacement_risk = net_a - marginal_floor

# NOI Improvement based on simulated room count
baseline_noi = net_b * sim_rooms
projected_noi = net_a * sim_rooms
improvement_val = projected_noi - baseline_noi
improvement_pct = (improvement_val / baseline_noi) * 100 if baseline_noi != 0 else 0

# --- 5. EXECUTIVE DASHBOARD ---
st.divider()
st.markdown("### 📈 Forecasting Impact & Marginal Floor Audit")

m1, m2, m3, m4 = st.columns(4)
with m1:
    st.metric("Net Flow (A)", f"﷼ {net_a:,.2f}")
with m2:
    st.metric("Marginal Floor (B)", f"﷼ {net_b:,.2f}")
with m3:
    st.metric("Total NOI Gain", f"﷼ {improvement_val:,.2f}")
with m4:
    st.metric("NOI Improvement", f"{improvement_pct:.2f}%")

# Status Verdict
status = "REJECT: DILUTIVE" if net_a < net_b else "ACCEPT: ACCRETIVE"

# Summary Card
st.markdown(f"""
<div class='noi-card'>
    <h4>Executive Summary: {status}</h4>
    Based on the <b>{sim_rooms} room simulation</b>, Segment A yields a Net Flow of <b>﷼ {net_a:,.2f}</b> 
    against a Marginal Floor of <b>﷼ {net_b:,.2f}</b>. 
    Oman statutory deflators and meal costs have been applied. 
    Total improvement to bottom-line NOI: <b>{improvement_pct:.2f}%</b>.
</div>
""", unsafe_allow_html=True)

# --- 6. DATA HANDOFF ---
st.session_state["current_audit"] = {
    "label": "Direct/FIT vs Group Simulation",
    "yield": net_a,
    "hurdle": net_b,
    "status": status,
    "improvement": improvement_pct,
    "rooms": sim_rooms,
    "market": "Oman"
}

st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 Run Pillar 02: Strategic AI Audit"):
    st.switch_page("pages/strategic_gem.py")
