import streamlit as st
from datetime import date

# --- 1. STYLING (Ultra-Stable Layout) ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Master")
st.markdown("""<style>
.block-container{padding-top:1rem!important;}
.main-title{font-size:1.8rem!important;font-weight:900;color:#1e3799;text-align:center;margin-top:-10px;}
.small-framework-header{font-size:0.95rem!important; font-weight:700; color:#4b6584; text-align:center; margin-bottom:15px; letter-spacing:0.5px;}
.card{padding:10px;border-radius:10px;margin-bottom:8px;border-left:10px solid;background:#ffffff;box-shadow: 0 2px 4px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff;padding:12px;border-radius:10px;border:1px solid #d1d9e6; margin-top:5px;}
.google-window{background:#e8f0fe; padding:18px; border-radius:12px; border:2px solid #4285f4; margin-bottom:15px; font-size:0.85rem; line-height:1.6;}
.news-item{background:#ffffff; border-radius:8px; padding:10px; margin-bottom:8px; border-left:4px solid #ff4b4b; box-shadow: 0 1px 3px rgba(0,0,0,0.05);}
.status-indicator{padding:12px; border-radius:10px; text-align:center; font-weight:900; font-size:1.1rem; color:white; margin-top:10px;}
.reason-box{background:#fff9c4; border:1px solid #fbc02d; padding:10px; border-radius:8px; margin-top:5px; text-align:left; font-weight:500; color:#5f4300; font-size:0.8rem;}
.theory-box{background:#f9f9f9; padding:25px; border-radius:15px; border:1px solid #dee2e6; margin-top:30px}
.theory-card{background:white; padding:12px; border-radius:10px; border:1px solid #eee; margin-bottom:8px;}
[data-testid="stSidebar"]{background:#f1f4f9; border-right:1px solid #dee2e6}
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if "reset_key" not in st.session_state: st.session_state["reset_key"] = 0

if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login_gate"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock Engine"):
            if pwd == "Gayan2026": 
                st.session_state["auth"] = True
                st.rerun()
            else: st.error("Access Denied")
    st.stop()

# --- 3. SIDEBAR (STRATEGIC GLOBAL INPUTS) ---
with st.sidebar:
    st.markdown("### 👤 Strategic Architect\nGayan Nugawela")
    if st.button("🧹 Clear Global Cache"):
        st.session_state["reset_key"] += 1
        st.rerun()
    st.divider()
    rk = str(st.session_state["reset_key"]) 
    
    currencies = {"OMR (﷼)": "﷼", "LKR (රු)": "රු", "THB (฿)": "฿", "AED (د.إ)": "د.إ", "SAR (﷼)": "﷼", "INR (₹)": "₹", "USD ($)": "$"}
    cur_choice = st.selectbox("🌍 Operating Currency", list(currencies.keys()), key="cur_sel_"+rk)
    cur_sym = currencies[cur_choice]
    cur_code = cur_choice.split(" ")[0]

    hotel_name = st.text_input("🏨 Hotel", "Wyndham Garden Salalah", key="h_nm_"+rk)
    city_name = st.text_input("📍 City Search", "Salalah", key="c_nm_"+rk)
    
    d1 = st.date_input("Check-In", date.today(), key="d_in_"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d_out_"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"📅 **Stay Duration: {m_nights} Nights**")
    
    inventory = st.number_input("Total Property Capacity", 1, 1000, 237, key="inv_c_"+rk)
    
    st.divider()
    st.markdown("### 📊 Pillar 03: Velocity")
    otb_occ = st.slider("OTB % (Date-Specific)", 0, 100, 15, key="otb_v_"+rk)
    avg_hist = st.slider("Hist. Benchmark %", 0, 100, 45, key="hst_v_"+rk)
    v_mult = 1.35 if otb_occ > avg_hist else 0.85 if otb_occ < (avg_hist - 15) else 1.0

    st.divider()
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx_v_"+rk)
    ota_comm = st.slider("OTA Commission %", 0, 40, 18, key="ota_v_"+rk)
    p01_fee = st.number_input(f"P01 Fee ({cur_sym})", 0.0, value=6.90, key="p01_v_"+rk)

    # UPDATED MEAL COST ARCHITECTURE (PER PERSON BASIS)
    st.markdown("### 🍽️ Unit Costs (Per Person)")
    c_snk = st.number_input(f"Snack Cost ({cur_sym})", 0.0, value=1.5, key="snk_v_"+rk)
    meal_costs = {
        "RO": 0.0,
        "BB": st.number_input("BB Cost (Breakfast)", 2.5, key="bb_mc_"+rk),
        "LN": st.number_input("LN Cost (Lunch)", 4.5, key="ln_mc_"+rk),
        "DN": st.number_input("DN Cost (Dinner)", 5.5, key="dn_mc_"+rk),
        "SAI": st.number_input("SAI Cost (Soft AI)", 8.5, key="sai_mc_"+rk),
        "AI": st.number_input("AI Cost (Premium AI)", 10.5, key="ai_mc_"+rk)
    }

# --- 4. MARKET INTEL ---
intel_db = {
    "salalah": {"ev": "Khareef Festival", "fl": "High Rotations (Dubai/Muscat)", "news": ["Port: Operations stable.", "Tourism: Surge expected.", "Weather: Monsoon rising."], "basis": "Microclimate Compression"},
    "dubai": {"ev": "DIFC Expansion Summit", "fl": "DXB Slot Scarcity 100%", "news": ["BREAKING: UAE exiting OPEC May 1st.", "DIFC Growth: 775 companies.", "Market: Oil volatility."], "basis": "Hub Velocity"},
    "colombo": {"ev": "Tourism Peak", "fl": "UL connectivity rising.", "news": ["Arrivals cross 1.2M mark.", "LKR Stability Improving.", "MICE demand surging."], "basis": "Emerging Market Recovery"}
}
active_intel = intel_db.get(city_name.lower(), {"ev": "Active Seasonal Rotation", "fl": "Baseline Rotation", "news": ["Standard market flow."], "basis": "Equilibrium"})

# --- 5. CALCULATION ENGINE ---
def run_yield(rms, nts, adr, meals, hurdle, comm_rate=0.0, laundry=0, mice=0, trans=0, snack_qty=0):
    tr = sum(rms); rn = tr * nts
    if tr <= 0: return None
    net_adr = adr / tx_div
    total_m_s = sum(qty * meal_costs.get(p, 0) for p, qty in meals.items()) + (snack_qty * c_snk)
    avg_m_s = (total_m_s / tr) if tr > 0 else 0
    unit_w = (net_adr - avg_m_s - (net_adr * comm_rate)) - p01_fee - laundry + (mice / tx_div)
    total_w = (unit_w * rn) + (trans / tx_div)
    disp_risk = (tr / inventory) >= 0.50
    if unit_w < hurdle: stt, clr, rsn = "REJECT: DILUTIVE", "#e74c3c", f"Yield < {cur_sym} hurdle."
    elif unit_w < (hurdle + 3.0): stt, clr, rsn = "REVIEW: MARGINAL", "#f39c12", "Yield at equilibrium window."
    else: stt, clr, rsn = "ACCEPT: OPTIMIZED", "#27ae60", "Wealth targets met."
    if disp_risk: rsn += " | ⚠️ DISPLACEMENT: Segment ≥50% capacity."
    return {"w": unit_w, "st": stt, "cl": clr, "rsn": rsn, "rn": rn, "total": total_w}

# --- 6. DASHBOARD ---
st.markdown("<h1 class='main-title'>YIELD EQUILIBRIUM MASTER DASHBOARD</h1>", unsafe_allow_html=True)
t1, t2 = st.tabs(["🌐 Aviation & Events", "🗞️ Live Market News Feed"])
with t1: st.markdown(f"<div class='google-window'><b>🌐 Aviation Intelligence: {city_name}</b><br>• <b>Events:</b> {active_intel['ev']} | <b>Basis:</b> {active_intel['basis']}<br>• <b>Flights:</b> {active_intel['fl']} | <b>Velocity:</b> {v_mult}x Applied</div>", unsafe_allow_html=True)
with t2:
    st.markdown(f"<div class='google-window' style='background:#fdf2f2; border-color:#ff4b4b;'><b style='color:#ff4b4b;'>🗞️ Market Alerts: {city_name} | {date.today().strftime('%B %d, %Y')}</b></div>", unsafe_allow_html=True)
    for item in active_intel['news']: st.markdown(f"<div class='news-item'>{item}</div>", unsafe_allow_html=True)

def draw_seg(label, key, suggest_adr, floor_def, color, is_ota=False, group=False):
    st.markdown(f"<div class='card' style='border-left-color:{color}'>{label}</div>", unsafe_allow_html=True)
    c_in, c_res = st.columns([2.6, 1])
    with c_in:
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        r1, r2, r3, r4, r5 = st.columns([1,1,1,1.5,1.5])
        # UNIQUE KEY LOCKING SYSTEM + TPL RESTORED
        sgl = r1.number_input("SGL", 0, key=f"sgl_in_{key}_{rk}")
        dbl = r2.number_input("DBL", 0, key=f"dbl_in_{key}_{rk}")
        tpl = r3.number_input("TPL", 0, key=f"tpl_in_{key}_{rk}")
        applied_adr = r4.number_input(f"Rate ({cur_sym})", value=float(suggest_adr * v_mult), key=f"adr_in_{key}_{rk}")
        floor = r5.number_input(f"Floor ({cur_sym})", value=float(floor_def), key=f"flr_in_{key}_{rk}")
        
        m_row = st.columns(7)
        p_ro = m_row[0].number_input("RO", 0, key=f"ro_v_{key}_{rk}")
        p_bb = m_row[1].number_input("BB", 0, key=f"bb_v_{key}_{rk}")
        p_ln = m_row[2].number_input("LN", 0, key=f"ln_v_{key}_{rk}")
        p_dn = m_row[3].number_input("DN", 0, key=f"dn_v_{key}_{rk}")
        p_sai = m_row[4].number_input("SAI", 0, key=f"sai_v_{key}_{rk}")
        p_ai = m_row[5].number_input("AI", 0, key=f"ai_v_{key}_{rk}")
        p_snk = m_row[6].number_input("Snk", 0, key=f"snk_v_{key}_{rk}")
        
        l_c, m_c, t_c = 0.0, 0.0, 0.0
        if group:
            g_row = st.columns(3)
            m_c = g_row[0].number_input(f"MICE Rev", 0.0, key=f"mc_r_{key}_{rk}")
            t_c = g_row[1].number_input(f"Trans Rev", 0.0, key=f"tr_r_{key}_{rk}")
            l_c = g_row[2].number_input(f"Laundry Cost", 0.0, key=f"l_c_{key}_{rk}")
        st.markdown("</div>", unsafe_allow_html=True)
    res = run_yield([sgl, dbl, tpl], m_nights, applied_adr, {"RO":p_ro,"BB":p_bb,"LN":p_ln,"DN":p_dn,"SAI":p_sai,"AI":p_ai}, floor, (ota_comm/100 if is_ota else 0.0), l_c, m_c, t_c, p_snk)
    if res:
        with c_res:
            st.metric(f"Net Wealth", f"{cur_sym} {res['w']:,.2f}")
            st.markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']}</div>", unsafe_allow_html=True
