import streamlit as st
from datetime import date

# --- 1. SETTINGS & STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Displacement Analyzer")

st.markdown("""<style>
.block-container{padding-top:1rem!important; padding-bottom:0rem!important;}
.main-title { font-size: 2rem!important; font-weight: 900; color: #1e3799; text-align: center; text-transform: uppercase; margin-bottom: -5px; }
.main-subtitle { font-size: 1rem!important; font-weight: 600; color: #4b6584; text-align: center; margin-bottom: 15px; }
.card{padding:8px; border-radius:8px; margin-bottom:5px; border-left:10px solid; background:#ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.05)}
.pricing-row{background:#f8faff; padding:10px; border-radius:10px; border:1px solid #d1d9e6; margin-top:2px;}
.google-window{background:#e8f0fe; padding:15px; border-radius:12px; border:2px solid #4285f4; margin-bottom:15px; font-size:0.88rem; line-height:1.5;}
.status-indicator{padding:10px; border-radius:8px; text-align:center; font-weight:900; font-size:1rem; color:white;}
.reason-box{background:#fff9c4; border:1px solid #fbc02d; padding:8px; border-radius:8px; margin-top:5px; text-align:left; font-weight:500; color:#5f4300; font-size:0.75rem;}
.theory-box { background-color: #f1f4f9; padding: 25px; border-radius: 15px; border: 1px solid #d1d9e6; margin-top: 30px; }
.pillar-header { color: #1e3799; font-weight: 800; font-size: 0.95rem; text-transform: uppercase; margin-bottom: 5px; display: block; }
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

# --- 3. SIDEBAR (STRATEGIC INPUTS) ---
rk = str(st.session_state["reset_key"])
with st.sidebar:
    st.markdown("### 🏨 Property Profile")
    h_name = st.text_input("Hotel", "Wyndham Garden Salalah", key="h_nm_"+rk)
    h_cap = st.number_input("Inventory Capacity", 1, 1000, 237, key="cap_"+rk)
    city_search = st.text_input("📍 Market Location", "Salalah", key="city_"+rk)
    
    st.divider()
    st.markdown("### 📊 Pillar 01: Simulation")
    sim_rooms = st.slider("Inventory Shift", 5, 10000, 40, key="sim_s_"+rk)
    
    st.divider()
    st.markdown("### 📅 Stay Period")
    d1 = st.date_input("Check-In", date.today(), key="d_in_"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d_out_"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.success(f"Stay Duration: {m_nights} Nights")

    st.divider()
    currencies = {
        "OMR (﷼)": "﷼", "AED (د.إ)": "د.إ", "SAR (﷼)": "﷼", "LKR (රු)": "රු", 
        "INR (₹)": "₹", "EUR (€)": "€", "GBP (£)": "£", "USD ($)": "$"
    }
    cur_choice = st.selectbox("Select Currency", list(currencies.keys()), key="c_sel_"+rk)
    cur_sym = currencies[cur_choice]

    st.divider()
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx_v_"+rk)
    ota_comm = st.slider("OTA Comm %", 0, 40, 15, key="ota_v_"+rk)
    p01_fee = st.number_input(f"P01 Fee ({cur_sym})", 0.0, value=6.90, key="p01_v_"+rk)

    st.markdown("### 🍽️ Meal Costs")
    meal_costs = {"RO": 0.0, "BB": st.number_input("BB", 0.0, key="bb_mc_"+rk),
                  "HB": st.number_input("HB", 0.0, key="hb_mc_"+rk), "FB": st.number_input("FB", 0.0, key="fb_mc_"+rk),
                  "SAI": st.number_input("SAI", 0.0, key="sai_mc_"+rk), "AI": st.number_input("AI", 0.0, key="ai_mc_"+rk)}

# --- 4. MARKET INTELLIGENCE DATA ---
intel_db = {
    "salalah": {"ev": "Khareef Festival Season", "fl": "OmanAir/SalamAir Rotations Peak", "news": "Monsoon Tourism Surge expected.", "demand": "Compression"},
    "muscat": {"ev": "Business Summit", "fl": "International Hub Stable", "news": "MICE demand up 15%.", "demand": "High Flow"}
}
active_intel = intel_db.get(city_search.lower(), {"ev": "Market Rotation", "fl": "Standard Flights", "news": "Standard flow stable.", "demand": "Standard"})

# --- 5. ENGINE LOGIC ---
def run_segment_yield(adr, meal_qty, hurdle, demand_type, comm_rate=0.0, mice=0.0, laundry=0.0, transport=0.0):
    velocity_adj = {"Compression (Peak)": 1.25, "High Flow": 1.10, "Standard": 1.0, "Distressed": 0.85}
    v_mult = velocity_adj.get(demand_type, 1.0)
    net_adr = (adr * v_mult) / tx_div
    total_meal_cost = sum(qty * meal_costs.get(p, 0) for p, qty in meal_qty.items())
    unit_w = (net_adr + (mice/tx_div) + ((transport/tx_div)/sim_rooms if sim_rooms>0 else 0) - total_meal_cost - (net_adr * comm_rate)) - p01_fee - laundry
    
    if unit_w < hurdle: stt, clr, rsn = "REJECT: DILUTIVE", "#e74c3c", "Yield below hurdle floor."
    elif unit_w < (hurdle + 5.0): stt, clr, rsn = "REVIEW: MARGINAL", "#f39c12", "Yield at equilibrium window."
    else: stt, clr, rsn = "ACCEPT: OPTIMIZED", "#27ae60", "Wealth protection targets met."
        
    return {"w": unit_w, "st": stt, "cl": clr, "rsn": rsn, "vm": v_mult}

# --- 6. TOP DASHBOARD & MARKET INSIGHTS ---
st.markdown(f"<h1 class='main-title'>{h_name.upper()}</h1>", unsafe_allow_html=True)
st.markdown("<div class='main-subtitle'>Yield Equilibrium Strategic Intelligence Engine</div>", unsafe_allow_html=True)

st.markdown(f"""
<div class='google-window'>
    <b>🌐 Market Intelligence Topic: {city_search} | {date.today().strftime('%B %Y')}</b><br>
    • <b>Aviation Situation:</b> {active_intel['fl']} | <b>Special Events:</b> {active_intel['ev']}<br>
    • <b>Special News Feed:</b> {active_intel['news']} | <b>Market Pulse:</b> {active_intel['demand']} Logic Applied.
</div>
""", unsafe_allow_html=True)

# --- 7. SEGMENT AUDITS ---
segments = [
    {"label": "1. DIRECT / FIT", "key": "fit", "color": "#3498db", "ota": False, "hurdle": 45.0, "group": False},
    {"label": "2. OTA CHANNELS", "key": "ota", "color": "#2ecc71", "ota": True, "hurdle": 35.0, "group": False},
    {"label": "3. CORPORATE / MICE GROUPS", "key": "mice", "color": "#34495e", "ota": False, "hurdle": 32.0, "group": True},
    {"label": "4. GROUP TOUR & TRAVEL", "key": "tnt", "color": "#e67e22", "ota": False, "hurdle": 25.0, "group": True}
]

wealth_results = {}

for seg in segments:
    is_active = st.checkbox(f"Enable {seg['label']}", value=(seg['key'] in ['fit', 'ota']), key=f"act_{seg['key']}_{rk}")
    
    if is_active:
        st.markdown(f"<div class='card' style='border-left-color:{seg['color']}'>{seg['label']}</div>", unsafe_allow_html=True)
        with st.container():
            st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
            r1 = st.columns([1, 0.6, 0.6, 0.6, 0.6, 1.2, 1.2])
            g_rate = r1[0].number_input(f"Gross Rate", value=75.0, key=f"adr_{seg['key']}_{rk}")
            sgl, dbl, tpl, qrpl = r1[1].number_input("SGL", 0, key=f"s_{seg['key']}_{rk}"), r1[2].number_input("DBL", 0, key=f"d_{seg['key']}_{rk}"), r1[3].number_input("TPL", 0, key=f"t_{seg['key']}_{rk}"), r1[4].number_input("QRPL", 0, key=f"q_{seg['key']}_{rk}")
            demand_sel = r1[5].selectbox("Market Demand", ["Compression (Peak)", "High Flow", "Standard", "Distressed"], key=f"dm_{seg['key']}_{rk}")
            h_floor = r1[6].number_input("Hurdle", value=seg['hurdle'], key=f"hrd_{seg['key']}_{rk}")

            r2 = st.columns([0.6,0.6,0.6,0.6,0.6,0.6, 1, 1, 1])
            ro, bb, hb, fb, sai, ai = r2[0].number_input("RO", 0, key=f"ro_{seg['key']}_{rk}"), r2[1].number_input("BB", 0, key=f"bb_{seg['key']}_{rk}"), r2[2].number_input("HB", 0, key=f"hb_{seg['key']}_{rk}"), r2[3].number_input("FB", 0, key=f"fb_{seg['key']}_{rk}"), r2[4].number_input("SAI", 0, key=f"sai_{seg['key']}_{rk}"), r2[5].number_input("AI", 0, key=f"ai_{seg['key']}_{rk}")
            
            m_pp = r2[6].number_input("Events (pp)", 0.0, key=f"m_{seg['key']}_{rk}") if seg['group'] else 0.0
            l_pp = r2[7].number_input("Laundry (pp)", 0.0, key=f"l_{seg['key']}_{rk}") if seg['group'] else 0.0
            t_f = r2[8].number_input("Transport", 0.0, key=f"tr_{seg['key']}_{rk}") if seg['group'] else 0.0

            res = run_segment_yield(g_rate, {"RO":ro,"BB":bb,"HB":hb,"FB":fb,"SAI":sai,"AI":ai}, h_floor, demand_sel, (ota_comm/100 if seg['ota'] else 0.0), m_pp, l_pp, t_f)
            
            v_cols = st.columns([1, 1, 1])
            v_cols[0].metric("Net Wealth", f"{cur_sym} {res['w']:,.2f}", delta=f"{res['vm']}x Velocity")
            v_cols[1].markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='reason-box'>💡 <b>Strategic Reasoning:</b> {res['rsn']}</div>", unsafe_allow_html=True)
            wealth_results[seg['key']] = res['w']
            st.markdown("</div>", unsafe_allow_html=True)

# --- 8. NOI SUMMARY & THEORY BOX ---
st.divider()
enabled_keys = list(wealth_results.keys())
if len(enabled_keys) >= 2:
    net_a, net_b = wealth_results[enabled_keys[0]], wealth_results[enabled_keys[1]]
    imp_val = (net_a - net_b) * sim_rooms * m_nights
    imp_pct = ((net_a - net_b) / net_b * 100) if net_b != 0 else 0

    m1, m2, m3 = st.columns(3)
    with m1: st.metric(f"Wealth Gap", f"{cur_sym} {net_a - net_b:,.2f}")
    with m2: st.metric("Total NOI Gain", f"{cur_sym} {imp_val:,.2f}")
    with m3: st.metric("NOI Improvement", f"{imp_pct:.2f}%")

# THE UPGRADED THEORY BOX (PILLARS)
st.markdown("<div class='theory-box'>", unsafe_allow_html=True)
st.markdown("<h3 style='color:#1e3799; margin-top:0;'>THE YIELD EQUILIBRIUM STRATEGIC FRAMEWORK</h3>", unsafe_allow_html=True)
c_a, c_b, c_c = st.columns(3)
with c_a:
    st.markdown("<span class='pillar-header'>🏛️ Pillar 01: Internal Wealth Stripping</span>", unsafe_allow_html=True)
    st.markdown(f"<p style='font-size:0.88rem; color:#4b6584;'>Strips statutory taxes ({tx_div}), commissions, and marginal meal costs to isolate Net-Core Wealth.</p>", unsafe_allow_html=True)
with c_b:
    st.markdown("<span class='pillar-header'>⚖️ Pillar 02: Hurdle Equilibrium</span>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.88rem; color:#4b6584;'>Establishes dynamic floors to protect inventory from lower-value displacement during high-demand cycles.</p>", unsafe_allow_html=True)
with c_c:
    st.markdown("<span class='pillar-header'>🌐 Pillar 03: External Velocity</span>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.88rem; color:#4b6584;'>Integrates real-time Market Pulse and Aviation situation to apply a Velocity Multiplier to wealth targets.</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
