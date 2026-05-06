import streamlit as st
from datetime import date
import os

# --- 1. SETTINGS & STYLING ---
st.set_page_config(layout="wide", page_title="Displacement Analyzer | Yield Equilibrium")

st.markdown("""<style>
.main-title { font-size: 2.2rem!important; font-weight: 900; color: #1e3799; text-align: center; text-transform: uppercase; }
.card{padding:10px; border-radius:10px; margin-bottom:8px; border-left:10px solid; background:#ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff; padding:12px; border-radius:10px; border:1px solid #d1d9e6; margin-top:5px;}
.google-window{background:#e8f0fe; padding:18px; border-radius:12px; border:2px solid #4285f4; margin-bottom:15px; font-size:0.85rem; line-height:1.6;}
.status-indicator{padding:12px; border-radius:10px; text-align:center; font-weight:900; font-size:1.1rem; color:white; margin-top:10px;}
.noi-card { background-color: #f8f9fa; padding: 25px; border-radius: 12px; border-left: 10px solid #1e3799; color: #2f3640; }
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION & GLOBAL RESET ---
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
    st.stop()

# --- 3. SIDEBAR (STRATEGIC INPUTS) ---
rk = str(st.session_state["reset_key"])
with st.sidebar:
    st.markdown("### 🏨 Property Profile")
    h_name = st.text_input("Hotel Name", "Wyndham Garden Salalah", key="h_name_"+rk)
    h_cap = st.number_input("Total Inventory", 1, 1000, 237, key="cap_"+rk)
    city_search = st.text_input("📍 Market Location", "Salalah", key="city_"+rk)
    
    st.divider()
    st.markdown("### 📊 Pillar 01: Simulation")
    sim_rooms = st.slider("Simulate Inventory Shift", 5, 10000, 40, key="sim_s_"+rk)
    
    st.divider()
    st.markdown("### 📅 Stay Period")
    d1 = st.date_input("Check-In", date.today(), key="d_in_"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d_out_"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    
    st.divider()
    currencies = {"OMR (﷼)": "﷼", "LKR (රු)": "රු", "USD ($)": "$"}
    cur_choice = st.selectbox("🌍 Currency", list(currencies.keys()), key="c_sel_"+rk)
    cur_sym = currencies[cur_choice]

    st.markdown("### 🏛️ Statutory Deflators")
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx_v_"+rk)
    ota_comm = st.slider("OTA Commission %", 0, 40, 15, key="ota_v_"+rk)
    p01_fee = st.number_input(f"P01 Fee ({cur_sym})", 0.0, value=6.90, key="p01_v_"+rk)

    st.markdown("### 🍽️ Unit Costs (Meal Plans)")
    meal_costs = {"RO": 0.0, "BB": st.number_input("BB Cost", 0.0, key="bb_mc_"+rk),
                  "HB": st.number_input("HB Cost", 0.0, key="hb_mc_"+rk), "FB": st.number_input("FB Cost", 0.0, key="fb_mc_"+rk),
                  "SAI": st.number_input("SAI Cost", 0.0, key="sai_mc_"+rk), "AI": st.number_input("AI Cost", 0.0, key="ai_mc_"+rk)}

# --- 4. ENGINE LOGIC ---
def run_segment_yield(adr, meal_qty, hurdle, demand_type, comm_rate=0.0, mice=0.0, laundry=0.0, transport=0.0):
    velocity_adj = {"Compression (Peak)": 1.25, "High Flow": 1.10, "Standard": 1.0, "Distressed": 0.85}
    v_mult = velocity_adj.get(demand_type, 1.0)
    
    # Pillar 01: Internal Wealth Stripping
    net_adr = (adr * v_mult) / tx_div
    total_meal_cost = sum(qty * meal_costs.get(p, 0) for p, qty in meal_qty.items())
    
    # Adding Group-Specific Revenue Streams
    net_mice = mice / tx_div
    net_transport = (transport / tx_div) / (sim_rooms if sim_rooms > 0 else 1) # Divided per room for unit wealth
    
    unit_w = (net_adr + net_mice + net_transport - total_meal_cost - (net_adr * comm_rate)) - p01_fee - laundry
    
    if unit_w < hurdle: stt, clr = "REJECT: DILUTIVE", "#e74c3c"
    elif unit_w < (hurdle + 5.0): stt, clr = "REVIEW: MARGINAL", "#f39c12"
    else: stt, clr = "ACCEPT: OPTIMIZED", "#27ae60"
        
    return {"w": unit_w, "st": stt, "cl": clr, "vm": v_mult}

# --- 5. DASHBOARD ---
st.markdown(f"<h1 class='main-title'>{h_name.upper()}</h1>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center; color:#4b6584; font-weight:600;'>Yield Equilibrium Displacement Analyzer | {city_search}</div>", unsafe_allow_html=True)

segments = [
    {"label": "1. DIRECT / FIT", "key": "fit", "color": "#3498db", "ota": False, "hurdle": 45.0, "group": False},
    {"label": "2. OTA CHANNELS", "key": "ota", "color": "#2ecc71", "ota": True, "hurdle": 35.0, "group": False},
    {"label": "3. CORPORATE / MICE GROUPS", "key": "mice", "color": "#34495e", "ota": False, "hurdle": 32.0, "group": True},
    {"label": "4. GROUP TOUR & TRAVEL", "key": "tnt", "color": "#e67e22", "ota": False, "hurdle": 25.0, "group": True}
]

wealth_results = {}

for seg in segments:
    st.markdown(f"<div class='card' style='border-left-color:{seg['color']}'>{seg['label']}</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        
        # ROW 1: GROSS RATE & ROOM COUNTS
        r1 = st.columns([1.5, 0.8, 0.8, 0.8, 0.8, 1.5, 1.5])
        g_rate = r1[0].number_input(f"Gross Rate ({cur_sym})", value=75.0, key=f"adr_{seg['key']}_{rk}")
        sgl = r1[1].number_input("SGL", 0, key=f"sgl_{seg['key']}_{rk}")
        dbl = r1[2].number_input("DBL", 0, key=f"dbl_{seg['key']}_{rk}")
        tpl = r1[3].number_input("TPL", 0, key=f"tpl_{seg['key']}_{rk}")
        qrpl = r1[4].number_input("QRPL", 0, key=f"qrp_{seg['key']}_{rk}")
        demand_sel = r1[5].selectbox("Market Demand", ["Compression (Peak)", "High Flow", "Standard", "Distressed"], key=f"dm_{seg['key']}_{rk}")
        h_floor = r1[6].number_input("Hurdle Floor", value=seg['hurdle'], key=f"hrd_{seg['key']}_{rk}")

        # ROW 2: MEALS & GROUP REVENUE (MICE/Laundry/Transport)
        r2 = st.columns([0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 1.5, 1.5, 1.5])
        ro, bb, hb, fb, sai, ai = r2[0].number_input("RO", 0, key=f"ro_{seg['key']}_{rk}"), r2[1].number_input("BB", 0, key=f"bb_{seg['key']}_{rk}"), r2[2].number_input("HB", 0, key=f"hb_{seg['key']}_{rk}"), r2[3].number_input("FB", 0, key=f"fb_{seg['key']}_{rk}"), r2[4].number_input("SAI", 0, key=f"sai_{seg['key']}_{rk}"), r2[5].number_input("AI", 0, key=f"ai_{seg['key']}_{rk}")
        
        # ADD-ON: Group Revenue Fields
        mice_pp = r2[6].number_input("MICE (pp)", 0.0, key=f"mice_{seg['key']}_{rk}") if seg['group'] else 0.0
        laundry_pp = r2[7].number_input("Laundry (pp)", 0.0, key=f"laun_{seg['key']}_{rk}") if seg['group'] else 0.0
        trans_fixed = r2[8].number_input("Transport (Fixed)", 0.0, key=f"trans_{seg['key']}_{rk}") if seg['group'] else 0.0

        # CALCULATION
        res = run_segment_yield(g_rate, {"RO":ro,"BB":bb,"HB":hb,"FB":fb,"SAI":sai,"AI":ai}, h_floor, demand_sel, (ota_comm/100 if seg['ota'] else 0.0), mice_pp, laundry_pp, trans_fixed)
        
        # ROW 3: VERDICT
        v_cols = st.columns([1, 1, 1.5])
        v_cols[0].metric("Unit Wealth", f"{cur_sym} {res['w']:,.2f}", delta=f"{res['vm']}x Velocity")
        v_cols[1].markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']}</div>", unsafe_allow_html=True)
        wealth_results[seg['key']] = res['w']
        st.markdown("</div>", unsafe_allow_html=True)

# --- 6. NOI SIMULATION ---
st.divider()
net_a, net_b = wealth_results['fit'], wealth_results['ota']
improvement_val = (net_a - net_b) * sim_rooms * m_nights
improvement_pct = ((net_a - net_b) / net_b * 100) if net_b != 0 else 0

m1, m2, m3 = st.columns(3)
with m1: st.metric("Wealth Gap (A-B)", f"{cur_sym} {net_a - net_b:,.2f}")
with m2: st.metric("Total NOI Gain", f"{cur_sym} {improvement_val:,.2f}")
with m3: st.metric("NOI % Improvement", f"{improvement_pct:.2f}%")

if st.button("🚀 Run Pillar 02: Strategic AI Audit"):
    st.session_state["current_audit"] = {"yield": net_a, "hurdle": net_b, "status": "OPTIMIZED", "rooms": sim_rooms}
    st.switch_page("pages/strategic_gem.py")
