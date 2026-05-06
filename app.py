import streamlit as st
from datetime import date

# --- 1. SETTINGS & STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Displacement Analyzer")

st.markdown("""<style>
.block-container{padding-top:1rem!important; padding-bottom:0rem!important;}
.main-title { font-size: 2.2rem!important; font-weight: 900; color: #1e3799; text-align: center; text-transform: uppercase; margin-bottom: -5px; }
.card{padding:8px; border-radius:8px; margin-bottom:5px; border-left:10px solid; background:#ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.05)}
.pricing-row{background:#f8faff; padding:15px; border-radius:12px; border:1px solid #d1d9e6; margin-top:2px;}
.status-indicator{padding:12px; border-radius:8px; text-align:center; font-weight:900; font-size:1.1rem; color:white;}
.reason-box{background:#fff9c4; border:1px solid #fbc02d; padding:10px; border-radius:8px; margin-top:8px; text-align:left; font-weight:500; color:#5f4300; font-size:0.8rem;}
.theory-box { background-color: #f1f4f9; padding: 25px; border-radius: 15px; border: 1px solid #d1d9e6; margin-top: 35px; }
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
    st.stop()

# --- 3. SIDEBAR (CONTEXTUAL DATA) ---
rk = str(st.session_state["reset_key"])
with st.sidebar:
    st.markdown("### 🏨 Property Profile")
    h_name = st.text_input("Hotel Name", "Wyndham Garden Salalah", key="h_nm_"+rk)
    h_cap = st.number_input("Total Capacity", 1, 1000, 237, key="cap_"+rk)
    city_search = st.text_input("📍 Market Location", "Salalah", key="city_"+rk)
    
    st.divider()
    st.markdown("### 📅 Stay Period")
    d1 = st.date_input("Check-In", date.today(), key="d_in_"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d_out_"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"Stay Duration: {m_nights} Nights")

    st.divider()
    currencies = {"OMR (﷼)": "﷼", "AED (د.إ)": "د.إ", "SAR (﷼)": "﷼", "LKR (රු)": "රු", "INR (₹)": "₹", "USD ($)": "$"}
    cur_sym = currencies[st.selectbox("Select Currency", list(currencies.keys()), key="c_sel_"+rk)]

    st.divider()
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx_v_"+rk)
    ota_comm = st.slider("OTA Comm %", 0, 40, 15, key="ota_v_"+rk)
    p01_fee = st.number_input(f"P01 Fee ({cur_sym})", 0.0, value=6.90, key="p01_v_"+rk)

    meal_costs = {"RO": 0.0, "BB": st.number_input("BB", 0.0, key="bb_mc_"+rk),
                  "HB": st.number_input("HB", 0.0, key="hb_mc_"+rk), "FB": st.number_input("FB", 0.0, key="fb_mc_"+rk),
                  "SAI": st.number_input("SAI", 0.0, key="sai_mc_"+rk), "AI": st.number_input("AI", 0.0, key="ai_mc_"+rk)}

# --- 4. CALIBRATED ENGINE LOGIC (DYNAMIC HURDLE) ---
def run_segment_yield(adr, meal_qty, base_hurdle, demand_type, is_group, total_rooms, comm_rate=0.0, mice=0.0, laundry=0.0, transport=0.0):
    # PILLAR 03: Velocity Multipliers
    velocity_map = {"Compression (Peak)": 1.25, "High Flow": 1.10, "Standard": 1.0, "Distressed": 0.85}
    v_mult = velocity_map.get(demand_type, 1.0)
    
    # NEW PILLAR 02: Dynamic Hurdle Logic
    # Hurdle floor scales based on market demand to reflect opportunity cost
    hurdle_multiplier = {"Compression (Peak)": 2.5, "High Flow": 1.5, "Standard": 1.0, "Distressed": 0.7}
    dynamic_hurdle = base_hurdle * hurdle_multiplier.get(demand_type, 1.0)
    
    net_adr = (adr * v_mult) / tx_div
    total_meal_cost = sum(qty * meal_costs.get(p, 0) for p, qty in meal_qty.items())
    group_rev = (mice / tx_div) + ((transport / tx_div) / total_rooms if total_rooms > 0 else 0) if is_group else 0
    
    unit_w = (net_adr + group_rev - total_meal_cost - (net_adr * comm_rate)) - p01_fee - laundry
    
    if unit_w < dynamic_hurdle:
        stt, clr, rsn = "REJECT: DILUTIVE", "#e74c3c", f"Yield {cur_sym}{unit_w:,.2f} displaced by dynamic peak hurdle ({cur_sym}{dynamic_hurdle:,.2f})."
    elif unit_w < (dynamic_hurdle + 5.0):
        stt, clr, rsn = "REVIEW: MARGINAL", "#f39c12", "Yield at equilibrium window."
    else:
        stt, clr, rsn = "ACCEPT: OPTIMIZED", "#27ae60", "Wealth protection targets achieved."
        
    return {"w": unit_w, "st": stt, "cl": clr, "rsn": rsn, "vm": v_mult, "dh": dynamic_hurdle}

# --- 5. TOP DASHBOARD ---
st.markdown(f"<h1 class='main-title'>{h_name.upper()}</h1>", unsafe_allow_html=True)

segments = [
    {"label": "1. DIRECT / FIT", "key": "fit", "color": "#3498db", "ota": False, "hurdle": 45.0, "group": False},
    {"label": "2. OTA CHANNELS", "key": "ota", "color": "#2ecc71", "ota": True, "hurdle": 35.0, "group": False},
    {"label": "3. CORPORATE / MICE GROUPS", "key": "mice", "color": "#34495e", "ota": False, "hurdle": 32.0, "group": True},
    {"label": "4. GROUP TOUR & TRAVEL", "key": "tnt", "color": "#e67e22", "ota": False, "hurdle": 12.0, "group": True}
]

wealth_results = {}

for seg in segments:
    is_active = st.checkbox(f"Activate {seg['label']}", value=(seg['key'] in ['fit', 'tnt']), key=f"act_{seg['key']}_{rk}")
    
    if is_active:
        st.markdown(f"<div class='card' style='border-left-color:{seg['color']}'>{seg['label']}</div>", unsafe_allow_html=True)
        with st.container():
            st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
            r1 = st.columns([1, 0.6, 0.6, 0.6, 0.6, 1.2, 1.2])
            g_rate = r1[0].number_input(f"Gross Rate", value=29.0 if seg['key']=='tnt' else 75.0, key=f"adr_{seg['key']}_{rk}")
            sgl, dbl, tpl, qrpl = r1[1].number_input("SGL", 0, key=f"s_{seg['key']}_{rk}"), r1[2].number_input("DBL", 25 if seg['key']=='tnt' else 0, key=f"d_{seg['key']}_{rk}"), r1[3].number_input("TPL", 0, key=f"t_{seg['key']}_{rk}"), r1[4].number_input("QRPL", 0, key=f"q_{seg['key']}_{rk}")
            
            rooms_total = sgl + dbl + tpl + qrpl
            demand_sel = r1[5].selectbox("Market Demand", ["Compression (Peak)", "High Flow", "Standard", "Distressed"], key=f"dm_{seg['key']}_{rk}")
            h_base = r1[6].number_input("Base Hurdle", value=seg['hurdle'], key=f"hrd_{seg['key']}_{rk}")

            r2 = st.columns([0.6,0.6,0.6,0.6,0.6,0.6, 1.1, 1.1, 1.1])
            ro, bb, hb, fb, sai, ai = r2[0].number_input("RO", 0, key=f"ro_{seg['key']}_{rk}"), r2[1].number_input("BB", 1 if seg['key']=='tnt' else 0, key=f"bb_{seg['key']}_{rk}"), r2[2].number_input("HB", 0, key=f"hb_{seg['key']}_{rk}"), r2[3].number_input("FB", 0, key=f"fb_{seg['key']}_{rk}"), r2[4].number_input("SAI", 0, key=f"sai_{seg['key']}_{rk}"), r2[5].number_input("AI", 0, key=f"ai_{seg['key']}_{rk}")
            
            mice_pp = r2[6].number_input("Events (pp)", 0.0, key=f"m_{seg['key']}_{rk}") if seg['group'] else 0.0
            laundry_pp = r2[7].number_input("Laundry (pp)", 0.0, key=f"l_{seg['key']}_{rk}") if seg['group'] else 0.0
            trans_f = r2[8].number_input("Transport", 0.0, key=f"tr_{seg['key']}_{rk}") if seg['group'] else 0.0

            res = run_segment_yield(g_rate, {"RO":ro,"BB":bb,"HB":hb,"FB":fb,"SAI":sai,"AI":ai}, h_base, demand_sel, seg['group'], rooms_total, (ota_comm/100 if seg['ota'] else 0.0), mice_pp, laundry_pp, trans_f)
            
            v_cols = st.columns([1, 1, 1])
            v_cols[0].metric("Net Wealth", f"{cur_sym} {res['w']:,.2f}", delta=f"{res['vm']}x Velocity")
            v_cols[1].markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='reason-box'>💡 <b>Strategic Reasoning:</b> {res['rsn']} | <b>Effective Hurdle:</b> {cur_sym}{res['dh']:,.2f}</div>", unsafe_allow_html=True)
            
            wealth_results[seg['key']] = {"w": res['w'], "rooms": rooms_total}
            st.markdown("</div>", unsafe_allow_html=True)

# --- 6. NOI SUMMARY & PILLARS ---
st.divider()
e_keys = list(wealth_results.keys())
if len(e_keys) >= 2:
    sa, sb = wealth_results[e_keys[0]], wealth_results[e_keys[1]]
    tg = (sa['w'] - sb['w']) * sb['rooms'] * m_nights
    
    m1, m2, m3 = st.columns(3)
    with m1: st.metric("Wealth Gap", f"{cur_sym} {sa['w'] - sb['w']:,.2f}")
    with m2: st.metric(f"Total NOI Gain ({sb['rooms']} Rooms)", f"{cur_sym} {tg:,.2f}")
    with m3: st.metric("NOI Improvement", f"{((sa['w'] - sb['w'])/sb['w']*100 if sb['w']!=0 else 0):.2f}%")

st.markdown("<div class='theory-box'><b>🏛️ PILLAR 01: NET-CORE</b> | <b>⚖️ PILLAR 02: DYNAMIC HURDLE</b> | <b>🌐 PILLAR 03: VELOCITY</b></div>", unsafe_allow_html=True)
