import streamlit as st
from datetime import date

# --- 1. STYLING (The Global Executive Aesthetic) ---
st.set_page_config(layout="wide", page_title="Displacement Analyzer | Yield Equilibrium")
st.markdown("""<style>
.block-container{padding-top:1rem!important;}
.main-title { font-size: 2.2rem!important; font-weight: 900; color: #1e3799; text-align: center!important; margin-top: -10px; text-transform: uppercase; letter-spacing: 2px; display: block; width: 100%; }
.main-subtitle { font-size: 1.15rem!important; font-weight: 600; color: #4b6584; text-align: center!important; margin-top: -10px; margin-bottom: 30px; letter-spacing: 1px; display: block; width: 100%; }
.card{padding:10px;border-radius:10px;margin-bottom:8px;border-left:10px solid;background:#ffffff;box-shadow: 0 2px 4px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff;padding:12px;border-radius:10px;border:1px solid #d1d9e6; margin-top:5px;}
.status-indicator{padding:12px; border-radius:10px; text-align:center; font-weight:900; font-size:1.1rem; color:white; margin-top:10px;}
.noi-card { background-color: #f8f9fa; padding: 25px; border-radius: 12px; border-left: 10px solid #1e3799; box-shadow: 0 4px 6px rgba(0,0,0,0.1); color: #2f3640; }
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
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

# --- 3. SIDEBAR (STRATEGIC GLOBAL INPUTS) ---
with st.sidebar:
    st.markdown("### 📊 Pillar 01: Simulation")
    # THE ADD-ON: Simulation bar (5 to 10,000)
    sim_rooms = st.slider("Simulate Room Inventory Shift", 5, 10000, 40, key="sim_s_"+str(st.session_state["reset_key"]))
    
    st.divider()
    rk = str(st.session_state["reset_key"]) 
    currencies = {"OMR (﷼)": "﷼", "LKR (රු)": "රු", "THB (฿)": "฿", "AED (د.إ)": "د.إ", "SAR (﷼)": "﷼", "INR (₹)": "₹", "USD ($)": "$"}
    cur_choice = st.selectbox("🌍 Base Currency", list(currencies.keys()), key="c_sel_"+rk)
    cur_sym = currencies[cur_choice]

    st.markdown("### 🏛️ Statutory Deflators")
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx_v_"+rk)
    ota_comm = st.slider("OTA Commission %", 0, 40, 15, key="ota_v_"+rk)
    p01_fee = st.number_input(f"P01 Fee ({cur_sym})", 0.0, value=6.90, key="p01_v_"+rk)

    st.markdown("### 🍽️ Unit Costs (Per Person Basis)")
    meal_costs = {
        "RO": 0.0, 
        "BB": st.number_input("BB Cost", 0.0, key="bb_mc_"+rk),
        "LN": st.number_input("LN Cost", 0.0, key="ln_mc_"+rk), 
        "DN": st.number_input("DN Cost", 0.0, key="dn_mc_"+rk),
        "SAI": st.number_input("SAI Cost", 0.0, key="sai_mc_"+rk), 
        "AI": st.number_input("AI Cost", 0.0, key="ai_mc_"+rk)
    }

# --- 4. ENGINE LOGIC ---
def run_yield_v2(adr, meals, comm_rate=0.0):
    net_adr = adr / tx_div
    total_meal_cost = sum(qty * meal_costs.get(p, 0) for p, qty in meals.items())
    # Formula: (Net ADR - Meals - Commission) - System Fee
    unit_w = (net_adr - total_meal_cost - (net_adr * comm_rate)) - p01_fee
    return unit_w

# --- 5. DASHBOARD ---
st.markdown("<h1 class='main-title'>DISPLACEMENT ANALYZER</h1>", unsafe_allow_html=True)
st.markdown("<div class='main-subtitle'>Yield Equilibrium Strategic Intelligence Engine</div>", unsafe_allow_html=True)

# SEGMENT A
st.markdown(f"<div class='card' style='border-left-color:#3498db'>1. DIRECT / FIT</div>", unsafe_allow_html=True)
with st.container():
    st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
    c1, c2, c3, c4, c5, c6, c7, c8 = st.columns([1.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 1])
    applied_adr_a = c1.number_input(f"Rate ({cur_sym})", value=85.0, key="adr_a_"+rk)
    p_ro_a = c2.number_input("RO", 0, key="ro_a_"+rk); p_bb_a = c3.number_input("BB", 0, key="bb_a_"+rk)
    p_ln_a = c4.number_input("LN", 0, key="ln_a_"+rk); p_dn_a = c5.number_input("DN", 0, key="dn_a_"+rk)
    p_sai_a = c6.number_input("SAI", 0, key="sai_a_"+rk); p_ai_a = c7.number_input("AI", 0, key="ai_a_"+rk)
    net_a = run_yield_v2(applied_adr_a, {"RO":p_ro_a,"BB":p_bb_a,"LN":p_ln_a,"DN":p_dn_a,"SAI":p_sai_a,"AI":p_ai_a})
    c8.metric("Net Wealth (A)", f"{cur_sym} {net_a:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)

# SEGMENT B
st.markdown(f"<div class='card' style='border-left-color:#e67e22'>2. GROUP / HURDLE</div>", unsafe_allow_html=True)
with st.container():
    st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
    b1, b2, b3, b4, b5, b6, b7, b8 = st.columns([1.2, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 1])
    applied_adr_b = b1.number_input(f"Rate ({cur_sym})", value=65.0, key="adr_b_"+rk)
    p_ro_b = b2.number_input("RO", 0, key="ro_b_"+rk); p_bb_b = b3.number_input("BB", 0, key="bb_b_"+rk)
    p_ln_b = b4.number_input("LN", 0, key="ln_b_"+rk); p_dn_b = b5.number_input("DN", 0, key="dn_b_"+rk)
    p_sai_b = b6.number_input("SAI", 0, key="sai_b_"+rk); p_ai_b = b7.number_input("AI", 0, key="ai_b_"+rk)
    net_b = run_yield_v2(applied_adr_b, {"RO":p_ro_b,"BB":p_bb_b,"LN":p_ln_b,"DN":p_dn_b,"SAI":p_sai_b,"AI":p_ai_b})
    b8.metric("Net Wealth (B)", f"{cur_sym} {net_b:,.2f}")
    st.markdown("</div>", unsafe_allow_html=True)

# --- 6. FORECASTING & NOI IMPROVEMENT ---
baseline_noi = net_b * sim_rooms
projected_noi = net_a * sim_rooms
improvement_val = projected_noi - baseline_noi
improvement_pct = (improvement_val / baseline_noi) * 100 if baseline_noi != 0 else 0

st.divider()
st.markdown("### 📈 Forecasting Impact & NOI Improvement")
m1, m2, m3 = st.columns(3)
with m1: st.metric("Net Flow (A-B)", f"{cur_sym} {net_a - net_b:,.2f}")
with m2: st.metric("Total NOI Gain", f"{cur_sym} {improvement_val:,.2f}")
with m3: st.metric("NOI % Improvement", f"{improvement_pct:.2f}%")

status = "REJECT: DILUTIVE" if net_a < net_b else "ACCEPT: ACCRETIVE"
st.markdown(f"""
<div class='noi-card'>
    <h4 style='margin-top:0;'>Executive Summary: {status}</h4>
    By shifting <b>{sim_rooms} rooms</b> from Segment B to Segment A, the <b>Yield Equilibrium Protocol</b> 
    identifies a <b>{improvement_pct:.2f}%</b> improvement in departmental NOI, 
    contributing an additional <b>{cur_sym} {improvement_val:,.2f}</b> to the bottom line.
</div>
""", unsafe_allow_html=True)

# --- 7. DATA HANDOFF ---
st.session_state["current_audit"] = {
    "label": "Direct/FIT vs Group Simulation",
    "yield": net_a, "hurdle": net_b, "status": status,
    "improvement": improvement_pct, "rooms": sim_rooms, "market": "Oman"
}

st.markdown("<br>", unsafe_allow_html=True)
if st.button("🚀 Run Pillar 02: Strategic AI Audit"):
    st.switch_page("pages/strategic_gem.py")
