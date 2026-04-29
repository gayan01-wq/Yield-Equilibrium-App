import streamlit as st
from datetime import date

# --- 1. STYLING ---
st.set_page_config(layout="wide", page_title="Displacement Analyzer | Yield Equilibrium")
st.markdown("""<style>
.block-container{padding-top:1rem!important;}
.main-title{font-size:2.0rem!important;font-weight:900;color:#1e3799;text-align:center;margin-top:-10px;text-transform:uppercase;letter-spacing:2px;}
.main-subtitle{font-size:1.1rem!important;font-weight:600;color:#4b6584;text-align:center;margin-top:-15px;margin-bottom:25px;letter-spacing:1px;}
.small-framework-header{font-size:0.95rem!important; font-weight:700; color:#4b6584; text-align:center; margin-bottom:15px; letter-spacing:1px;}
.card{padding:10px;border-radius:10px;margin-bottom:8px;border-left:10px solid;background:#ffffff;box-shadow: 0 2px 4px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff;padding:12px;border-radius:10px;border:1px solid #d1d9e6; margin-top:5px;}
.google-window{background:#e8f0fe; padding:18px; border-radius:12px; border:2px solid #4285f4; margin-bottom:15px; font-size:0.85rem; line-height:1.6;}
.news-item{background:#ffffff; border-radius:8px; padding:10px; margin-bottom:8px; border-left:4px solid #ff4b4b; box-shadow: 0 1px 3px rgba(0,0,0,0.05);}
.status-indicator{padding:12px; border-radius:10px; text-align:center; font-weight:900; font-size:1.1rem; color:white; margin-top:10px;}
.reason-box{background:#fff9c4; border:1px solid #fbc02d; padding:10px; border-radius:8px; margin-top:5px; text-align:left; font-weight:500; color:#5f4300; font-size:0.8rem;}
.theory-box{background:#f9f9f9; padding:25px; border-radius:15px; border:1px solid #dee2e6; margin-top:30px}
.theory-card{background:white; padding:12px; border-radius:10px; border:1px solid #eee; margin-bottom:8px;}
[data-testid="stSidebar"]{background:#f1f4f9; border-right:1px solid #dee2e6}
.contact-section{background:#1e3799; padding:30px; border-radius:15px; margin-top:40px; color:white;}
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

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("### 👤 System Developer\nGayan Nugawela")
    if st.button("🧹 Clear Global Cache"):
        st.session_state["reset_key"] += 1
        st.rerun()
    st.divider()
    rk = str(st.session_state["reset_key"]) 
    currencies = {"OMR (﷼)": "﷼", "LKR (රු)": "රු", "THB (฿)": "฿", "AED (د.إ)": "د.إ", "SAR (﷼)": "﷼", "INR (₹)": "₹", "USD ($)": "$"}
    cur_choice = st.selectbox("🌍 Base Currency", list(currencies.keys()), key="c_sel_"+rk)
    cur_sym = currencies[cur_choice]
    hotel_name = st.text_input("🏨 Hotel", "Wyndham Garden Salalah", key="h_nm_"+rk)
    city_search = st.text_input("📍 City Search", "Salalah", key="c_nm_"+rk)
    d1 = st.date_input("Check-In", date.today(), key="d_in_"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d_out_"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"📅 Stay: {m_nights} Nights")
    inventory = st.number_input("Total Capacity", 1, 1000, 237, key="inv_c_"+rk)
    st.divider()
    st.markdown("### 📊 Velocity")
    otb_occ = st.slider("OTB %", 0, 100, 15, key="otb_s_"+rk)
    avg_hist = st.slider("Hist. %", 0, 100, 45, key="hst_s_"+rk)
    v_mult = 1.35 if otb_occ > avg_hist else 0.85 if otb_occ < (avg_hist - 15) else 1.0
    st.divider()
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx_v_"+rk)
    ota_comm = st.slider("OTA Commission %", 0, 40, 15, key="ota_v_"+rk)
    p01_fee = st.number_input(f"P01 Fee ({cur_sym})", 0.0, value=6.90, key="p01_v_"+rk)
    
    # Unit Costs - Precision enabled, default 0
    meal_costs = {
        "RO": 0.0, 
        "BB": st.number_input("BB Cost", 0.0, format="%.3f", step=0.1, key="bb_mc_"+rk),
        "LN": st.number_input("LN Cost", 0.0, format="%.3f", step=0.1, key="ln_mc_"+rk), 
        "DN": st.number_input("DN Cost", 0.0, format="%.3f", step=0.1, key="dn_mc_"+rk),
        "SAI": st.number_input("SAI Cost", 0.0, format="%.3f", step=0.1, key="sai_mc_"+rk), 
        "AI": st.number_input("AI Cost", 0.0, format="%.3f", step=0.1, key="ai_mc_"+rk)
    }

# --- 4. INTEL ---
intel_db = {
    "salalah": {"ev": "Khareef Festival", "fl": "DXB/MCT Rotations", "news": ["Port: Stable", "Tourism: Surge", "Monsoon Rising"], "basis": "Microclimate"},
    "colombo": {"ev": "Tourism Peak", "fl": "UL Hub Growth", "news": ["Arrivals 1.2M+", "LKR Stable", "MICE Demand"], "basis": "Recovery"}
}
active_intel = intel_db.get(city_search.lower(), {"ev": "Active Rotation", "fl": "Baseline", "news": ["Standard market flow."], "basis": "Equilibrium"})

# --- 5. ENGINE ---
def run_yield(rms, nts, adr, meals, hurdle, demand_type, comm_rate=0.0, laundry=0, mice=0, trans=0):
    tr = sum(rms); rn = tr * nts
    if tr <= 0: return None
    demand_adj = {"Compression (Peak)": 15.0, "High Flow": 5.0, "Standard": 0.0, "Distressed": -5.0}
    eff_hurdle = hurdle + demand_adj.get(demand_type, 0)
    net_adr = adr / tx_div
    total_m = sum(qty * meal_costs.get(p, 0) for p, qty in meals.items())
    avg_m = (total_m / tr)
    unit_w = (net_adr - avg_m - (net_adr * comm_rate)) - p01_fee - laundry + (mice / tx_div)
    total_w = (unit_w * rn) + (trans / tx_div)
    if unit_w < eff_hurdle: stt, clr, rsn = "REJECT: DILUTIVE", "#e74c3c", f"Yield < {cur_sym}{eff_hurdle:.2f} hurdle."
    elif unit_w < (eff_hurdle + 3.0): stt, clr, rsn = "REVIEW: MARGINAL", "#f39c12", "Equilibrium window."
    else: stt, clr, rsn = "ACCEPT: OPTIMIZED", "#27ae60", "Wealth targets met."
    if (tr / inventory) >= 0.50: rsn += " | ⚠️ DISPLACEMENT risk."
    return {"w": unit_w, "st": stt, "cl": clr, "rsn": rsn, "rn": rn, "total": total_w}

# --- 6. DASHBOARD ---
st.markdown("<h1 class='main-title'>DISPLACEMENT ANALYZER</h1>", unsafe_allow_html=True)
st.markdown("<div class='main-subtitle'>Yield Equilibrium Strategic Intelligence Engine</div>", unsafe_allow_html=True)
t1, t2 = st.tabs(["🌐 Aviation & Events", "🗞️ Market News Feed"])
with t1: st.markdown(f"<div class='google-window'><b>🌐 Aviation Intelligence: {city_search}</b><br>• <b>Events:</b> {active_intel['ev']} | <b>Basis:</b> {active_intel['basis']}<br>• <b>Velocity:</b> {v_mult}x Applied</div>", unsafe_allow_html=True)
with t2:
    st.markdown(f"<div class='google-window' style='background:#fdf2f2; border-color:#ff4b4b;'><b style='color:#ff4b4b;'>🗞️ Market Alerts: {city_search} | {date.today().strftime('%B %d, %Y')}</b></div>", unsafe_allow_html=True)
    for item in active_intel['news']: st.markdown(f"<div class='news-item'>{item}</div>", unsafe_allow_html=True)

def draw_seg(label, key, suggest_adr, floor_def, color, is_ota=False, group=False):
    st.markdown(f"<div class='card' style='border-left-color:{color}'>{label}</div>", unsafe_allow_html=True)
    c_in, c_res = st.columns([2.6, 1])
    with c_in:
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        r1, r2, r3, r4, r5 = st.columns([0.8,0.8,0.8,1.3,1.3])
        sgl = r1.number_input("SGL", 0, key=f"s_{key}_{rk}"); dbl = r2.number_input("DBL", 0, key=f"d_{key}_{rk}"); tpl = r3.number_input("TPL", 0, key=f"t_{key}_{rk}")
        applied_adr = r4.number_input(f"Rate ({cur_sym})", value=float(suggest_adr * v_mult), key=f"a_{key}_{rk}")
        floor = r5.number_input(f"Base Hurdle", value=float(floor_def), key=f"f_{key}_{rk}")
        m_row = st.columns([1.5, 1, 1, 1, 1, 1, 1])
        demand_sel = m_row[0].selectbox("Demand", ["Compression (Peak)", "High Flow", "Standard", "Distressed"], key=f"dm_{key}_{rk}")
        p_ro = m_row[1].number_input("RO", 0, key=f"ro_{key}_{rk}"); p_bb = m_row[2].number_input("BB", 0, key=f"bb_{key}_{rk}"); p_ln = m_row[3].number_input("LN", 0, key=f"ln_{key}_{rk}"); p_dn = m_row[4].number_input("DN", 0, key=f"dn_{key}_{rk}"); p_sai = m_row[5].number_input("SAI", 0, key=f"sai_{key}_{rk}"); p_ai = m_row[6].number_input("AI", 0, key=f"ai_{key}_{rk}")
        l_c, m_c, t_c = 0.0, 0.0, 0.0
        if group:
            g_row = st.columns(3)
            m_c = g_row[0].number_input(f"MICE", 0.0, key=f"mi_{key}_{rk}"); t_c = g_row[1].number_input(f"Trans", 0.0, key=f"tr_{key}_{rk}"); l_c = g_row[2].number_input(f"Laundry", 0.0, key=f"la_{key}_{rk}")
        st.markdown("</div>", unsafe_allow_html=True)
    res = run_yield([sgl, dbl, tpl], m_nights, applied_adr, {"RO":p_ro,"BB":p_bb,"LN":p_ln,"DN":p_dn,"SAI":p_sai,"AI":p_ai}, floor, demand_sel, (ota_comm/100 if is_ota else 0.0), l_c, m_c, t_c)
    if res:
        with c_res:
            st.metric(f"Net Wealth", f"{cur_sym} {res['w']:,.2f}")
            st.markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='reason-box'>💡 <b>Verdict:</b><br>{res['rsn']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='audit-box'>📊 {res['rn']} RN | Total: {cur_sym} {res['total']:,.2f}</div>", unsafe_allow_html=True)

draw_seg("1. DIRECT / FIT", "fit", 65, 40, "#3498db")
draw_seg("2. OTA CHANNELS", "ota", 60, 35, "#2ecc71", is_ota=True)
draw_seg("3. CORPORATE GROUPS", "corp", 55, 32, "#34495e", group=True)
draw_seg("4. MICE GROUPS", "mice", 50, 30, "#9b59b6", group=True)
draw_seg("5. TOUR & TRAVEL (GROUPS)", "tnt", 45, 25, "#e67e22", group=True)

# --- 7. METHODOLOGY (DETAILED PILLARS) ---
st.divider()
st.markdown("<div class='theory-box'>", unsafe_allow_html=True)
st.markdown(f"<div class='small-framework-header'>The Yield Equilibrium Strategic Framework (Live Tax Basis: {tx_div})</div>", unsafe_allow_html=True)
st.markdown(f"""
<div class='theory-card' style='background:#f1f4f9; border: 1px solid #1e3799; padding:25px;'>
    <h4 style='color:#1e3799; margin-top:0; text-align:center;'>STRATEGIC FRAMEWORK DEEP-DIVE</h4>
    <div style='margin-top:10px;'>
        <p style='font-size:0.88rem; color:#333; margin-bottom:12px;'>
            <b>🏛️ PILLAR 01: INTERNAL WEALTH STRIPPING (THE NET-CORE)</b><br>
            Deconstructs revenue to find the 'True Net'. Every unit of currency is analyzed against <b>statutory tax ({tx_div})</b>, <b>leakage (Comm)</b>, and <b>variable production costs</b>. If it doesn't leave a margin after stripping, it is rejected as dilutive business.
        </p>
        <p style='font-size:0.88rem; color:#333; margin-bottom:12px;'>
            <b>⚖️ PILLAR 02: HURDLE EQUILIBRIUM (THE DISPLACEMENT GUARD)</b><br>
            Hurdles are not static; they are <b>protective barriers</b>. In 'Compression' (High Demand), the analyzer inflates the hurdle by <b>+15.0</b> units. This acts as a filter to ensure that low-value groups or OTAs don't occupy inventory that could be sold to higher-yield last-minute travelers later.
        </p>
        <p style='font-size:0.88rem; color:#333;'>
            <b>🌐 PILLAR 03: EXTERNAL VELOCITY (THE MARKET PULSE)</b><br>
            Yielding at the speed of the market. This pillar calculates <b>Pace Momentum ({v_mult}x)</b>. If OTB pace exceeds historical benchmarks, the system automatically suggests more aggressive pricing. It integrates Aviation intelligence and event rotations to ensure the hotel isn't selling 'under-market' during localized surges.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- 8. FOOTER ---
st.markdown("<div class='contact-section'>", unsafe_allow_html=True)
st.subheader("✉️ Contact the System Developer")
st.write("Direct queries to Gayan Nugawela regarding custom logic.")
col1, col2 = st.columns([1, 1])
with col1:
    contact_form = """
    <form action="https://formspree.io/f/mkoywogq" method="POST" style="display: flex; flex-direction: column; gap: 15px; background: white; padding: 20px; border-radius: 10px;">
        <input type="text" name="name" placeholder="Full Name" style="padding: 10px; border-radius: 5px; border: 1px solid #ddd; color: black;" required>
        <input type="email" name="email" placeholder="Work Email" style="padding: 10px; border-radius: 5px; border: 1px solid #ddd; color: black;" required>
        <textarea name="message" placeholder="Technical query..." style="padding: 10px; border-radius: 5px; border: 1px solid #ddd; height: 100px; color: black;" required></textarea>
        <button type="submit" style="background-color: #1e3799; color: white; padding: 12px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; font-size: 1rem;">🚀 Submit to Developer</button>
    </form>
    """
    st.markdown(contact_form, unsafe_allow_html=True)
with col2:
    st.markdown("### Logic Desk Details\n* **Email:** gayan01@gmail.com\n* **Scope:** Algorithm updates, Displacement logic tweaks.")
st.markdown("</div>", unsafe_allow_html=True)
