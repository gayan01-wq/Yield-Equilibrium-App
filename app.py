import streamlit as st
from datetime import date

# --- 1. STYLING (The Global Executive Aesthetic) ---
st.set_page_config(layout="wide", page_title="Displacement Analyzer | Yield Equilibrium")
st.markdown("""<style>
.block-container{padding-top:1rem!important;}
.main-title {
    font-size: 2.2rem!important;
    font-weight: 900;
    color: #1e3799;
    text-align: center!important;
    margin-top: -10px;
    text-transform: uppercase;
    letter-spacing: 2px;
    display: block;
    width: 100%;
}
.main-subtitle {
    font-size: 1.15rem!important;
    font-weight: 600;
    color: #4b6584;
    text-align: center!important;
    margin-top: -10px;
    margin-bottom: 30px;
    letter-spacing: 1px;
    display: block;
    width: 100%;
}
.noi-card { 
    background-color: #f8f9fa; padding: 25px; border-radius: 12px; 
    border-left: 10px solid #1e3799; box-shadow: 0 4px 6px rgba(0,0,0,0.1); color: #2f3640;
}
.card{padding:10px;border-radius:10px;margin-bottom:8px;border-left:10px solid;background:#ffffff;box-shadow: 0 2px 4px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff;padding:12px;border-radius:10px;border:1px solid #d1d9e6; margin-top:5px;}
.status-indicator{padding:12px; border-radius:10px; text-align:center; font-weight:900; font-size:1.1rem; color:white; margin-top:10px;}
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION & CACHE ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if "reset_key" not in st.session_state: st.session_state["reset_key"] = 0

if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login_gate"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock"):
            if pwd == "Gayan2026": 
                st.session_state["auth"] = True
                st.rerun()
            else: st.error("Access Denied")
    st.stop()

# --- 3. SIDEBAR (STRATEGIC GLOBAL INPUTS + SIMULATION) ---
with st.sidebar:
    st.markdown("### 📊 Pillar 01: Simulation")
    # THE ADD-ON: Simulation bar for room inventory shifts (5 to 10,000)
    sim_rooms = st.slider("Simulate Room Inventory Shift", 5, 10000, 40, key="sim_s_"+str(st.session_state["reset_key"]))
    st.info(f"Analyzing impact of shifting **{sim_rooms} rooms**.")
    
    st.divider()
    rk = str(st.session_state["reset_key"]) 
    currencies = {"OMR (﷼)": "﷼", "LKR (රු)": "රු", "THB (฿)": "฿", "AED (د.إ)": "د.إ", "SAR (﷼)": "﷼", "INR (₹)": "₹", "USD ($)": "$"}
    cur_choice = st.selectbox("🌍 Base Currency", list(currencies.keys()), key="c_sel_"+rk)
    cur_sym = currencies[cur_choice]

    st.markdown("### 🏛️ Statutory Deflators")
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx_v_"+rk)
    ota_comm = st.slider("OTA Commission %", 0, 40, 15, key="ota_v_"+rk)
    p01_fee = st.number_input(f"P01 Fee ({cur_sym})", 0.0, value=6.90, key="p01_v_"+rk)

# --- 4. CALCULATION ENGINE ---
def calculate_net_flow(adr, cost_per_room, comm_rate=0.0):
    # Removing statutory taxes from Gross to isolate Net Wealth
    net_adr = adr / tx_div
    # Isolated Net Wealth = (Net ADR - Commission) - Fees/Costs
    return (net_adr * (1 - comm_rate)) - p01_fee - cost_per_room

# --- 5. DASHBOARD ---
st.markdown("<h1 class='main-title'>DISPLACEMENT ANALYZER</h1>", unsafe_allow_html=True)
st.markdown("<div class='main-subtitle'>Yield Equilibrium Strategic Intelligence Engine</div>", unsafe_allow_html=True)

# --- SEGMENT COMPARISON BLOCK ---
col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown(f"<div class='card' style='border-left-color:#3498db'>SEGMENT A: DIRECT / FIT</div>", unsafe_allow_html=True)
    adr_a = st.number_input("Gross ADR (A)", value=85.0, key="adr_a_"+rk)
    cost_a = st.number_input("Cost per Room (A)", value=15.0, key="cost_a_"+rk)
    net_a = calculate_net_flow(adr_a, cost_a)

with col2:
    st.markdown(f"<div class='card' style='border-left-color:#e67e22'>SEGMENT B: GROUP / HURDLE</div>", unsafe_allow_html=True)
    adr_b = st.number_input("Gross ADR (B)", value=65.0, key="adr_b_"+rk)
    cost_b = st.number_input("Cost per Room (B)", value=10.0, key="cost_b_"+rk)
    net_b = calculate_net_flow(adr_b, cost_b)

# --- 6. FORECASTING IMPACT & NOI LOGIC ---
# Marginal Floor logic: Segment B acts as the hurdle
baseline_noi = net_b * sim_rooms
projected_noi = net_a * sim_rooms
improvement_val = projected_noi - baseline_noi
improvement_pct = (improvement_val / baseline_noi) * 100 if baseline_noi != 0 else 0

st.divider()
st.markdown("### 📈 Forecasting Impact & NOI Improvement")

m1, m2, m3 = st.columns(3)
with m1:
    st.metric("Net Flow (A-B)", f"{cur_sym} {net_a - net_b:,.2f}")
with m2:
    st.metric("Total NOI Gain", f"{cur_sym} {improvement_val:,.2f}")
with m3:
    st.metric("NOI % Improvement", f"{improvement_pct:.2f}%")

# Status Verdict
status = "REJECT: DILUTIVE" if net_a < net_b else "ACCEPT: ACCRETIVE"

# Summary Card
st.markdown(f"""
<div class='noi-card'>
    <h4 style='margin-top:0;'>Executive Summary: {status}</h4>
    By shifting <b>{sim_rooms} rooms</b> from Segment B to Segment A, the 
    <b>Yield Equilibrium Protocol</b> identifies a <b>{improvement_pct:.2f}%</b> 
    improvement in departmental NOI, contributing an additional 
    <b>{cur_sym} {improvement_val:,.2f}</b> to the total net-flow.
</div>
""", unsafe_allow_html=True)

# --- 7. DATA HANDOFF & NAVIGATION ---
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
