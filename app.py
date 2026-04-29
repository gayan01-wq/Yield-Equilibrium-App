import streamlit as st
from datetime import date

# --- 1. CORE CONFIG & EXECUTIVE STYLING ---
st.set_page_config(layout="wide", page_title="Displacement Analyzer | Yield Equilibrium")

st.markdown("""<style>
.block-container{padding-top:1rem!important;}
/* Perfect Centering for Header Section */
.header-container{text-align:center; margin-bottom:30px; width:100%;}
.main-title{font-size:2.2rem!important; font-weight:900; color:#1e3799; text-transform:uppercase; letter-spacing:2px; margin-bottom:0px;}
.main-subtitle{font-size:1.1rem!important; font-weight:600; color:#4b6584; letter-spacing:1px; margin-top:-5px;}

.card{padding:12px; border-radius:10px; margin-bottom:10px; border-left:12px solid #1e3799; background:#ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff; padding:15px; border-radius:10px; border:1px solid #d1d9e6; margin-top:5px;}
.status-indicator{padding:12px; border-radius:10px; text-align:center; font-weight:900; font-size:1.1rem; color:white; margin-top:10px;}
.theory-box{background:#f9f9f9; padding:25px; border-radius:15px; border:1px solid #dee2e6; margin-top:30px}
[data-testid="stSidebar"]{background:#f1f4f9; border-right:1px solid #dee2e6}
.contact-section{background:#1e3799; padding:30px; border-radius:15px; margin-top:40px; color:white;}
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if "reset_key" not in st.session_state: st.session_state["reset_key"] = 0

if not st.session_state["auth"]:
    st.markdown("<div class='header-container'><h1 class='main-title'>EQUILIBRIUM ENGINE</h1></div>", unsafe_allow_html=True)
    with st.form("login_gate"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock Engine"):
            if pwd == "Gayan2026": 
                st.session_state["auth"] = True
                st.rerun()
            else: st.error("Access Denied")
    st.stop()

# --- 3. SIDEBAR (STRATEGIC INPUTS) ---
with st.sidebar:
    st.markdown("### 👤 System Developer\nGayan Nugawela")
    if st.button("🧹 Reset System Cache"):
        st.session_state["reset_key"] += 1
        st.rerun()
    st.divider()
    
    rk = str(st.session_state["reset_key"]) 
    cur_sym = st.selectbox("Currency", ["﷼", "රු", "฿", "د.إ", "₹", "$"], key="cur_"+rk)
    city_search = st.text_input("📍 City Search", "Salalah", key="city_"+rk)
    d1 = st.date_input("Check-In", date.today(), key="d_in_"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d_out_"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"📅 Stay Duration: {m_nights} Nights")
    
    st.divider()
    st.markdown("### 📊 Velocity Analytics")
    otb = st.slider("OTB %", 0, 100, 15, key="otb_"+rk)
    hst = st.slider("Hist. Benchmark %", 0, 100, 45, key="hst_"+rk)
    v_mult = 1.35 if otb > hst else 0.85 if otb < (hst - 15) else 1.0

    st.divider()
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx_"+rk)
    ota_comm = st.slider("OTA Commission %", 0, 40, 15, key="ota_"+rk)
    p01_fee = st.number_input(f"P01 Fee ({cur_sym})", value=6.90, key="p01_"+rk)

    st.markdown("### 🍽️ Unit Meal Costs")
    bb_c = st.number_input("BB Cost", 0.0, format="%.3f", key="bb_c_"+rk)
    ai_c = st.number_input("AI Cost", 0.0, format="%.3f", key="ai_c_"+rk)

# --- 4. CALCULATION ENGINE ---
def run_yield(rms, adr, hurdle, demand, comm_rate=0.0):
    if rms <= 0: return None
    d_adj = {"Compression (Peak)": 15.0, "High Flow": 5.0, "Standard": 0.0, "Distressed": -5.0}
    eff_hurdle = hurdle + d_adj.get(demand, 0)
    net_adr = adr / tx_div
    unit_w = (net_adr - bb_c - (net_adr * comm_rate)) - p01_fee
    status = "ACCEPT" if unit_w >= eff_hurdle else "REJECT"
    color = "#27ae60" if unit_w >= eff_hurdle else "#e74c3c"
    return {"w": unit_w, "st": status, "cl": color, "total": unit_w * rms * m_nights}

# --- 5. DASHBOARD HEADER (FIXED ALIGNMENT) ---
st.markdown(f"""
<div class='header-container'>
    <h1 class='main-title'>DISPLACEMENT ANALYZER</h1>
    <div class='main-subtitle'>Yield Equilibrium Strategic Intelligence Engine</div>
</div>
""", unsafe_allow_html=True)

st.info(f"📍 Analysis: {city_search} | 📈 Velocity: {v_mult}x | 📅 Stay: {m_nights} Nights")

# --- 6. SEGMENT GENERATION (RESTORED OPTIONS) ---
def draw_segment(label, key, suggest_adr, floor, is_ota=False):
    st.markdown(f"<div class='card'><b>{label}</b></div>", unsafe_allow_html=True)
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        # Top Row: Basic Pricing
        r1, r2, r3 = st.columns([1, 1, 1.5])
        rms = r1.number_input("Rooms", 0, key="r_"+key)
        rate = r2.number_input(f"Rate ({cur_sym})", value=float(suggest_adr * v_mult), key="a_"+key)
        dem = r3.selectbox("Demand Context", ["Standard", "Compression (Peak)", "Distressed"], key="d_"+key)
        
        # Bottom Row: Meal Options (Restored)
        m1, m2, m3, m4 = st.columns(4)
        ro = m1.checkbox("RO", key="ro_"+key)
        bb = m2.checkbox("BB", key="bb_"+key)
        hb = m3.checkbox("HB", key="hb_"+key)
        fb = m4.checkbox("FB", key="fb_"+key)
        st.markdown("</div>", unsafe_allow_html=True)
    
    res = run_yield(rms, rate, floor, dem, (ota_comm/100 if is_ota else 0.0))
    if res:
        with c2:
            st.metric("Net Wealth", f"{cur_sym}{res['w']:,.2f}")
            st.markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']}</div>", unsafe_allow_html=True)

draw_segment("1. DIRECT / FIT", "fit", 65, 40)
draw_segment("2. OTA CHANNELS", "ota", 60, 35, is_ota=True)
draw_segment("3. CORPORATE GROUPS", "corp", 55, 32)
draw_segment("4. MICE GROUPS", "mice", 50, 30)
draw_segment("5. TOUR & TRAVEL (GROUPS)", "tnt", 45, 25)

# --- 7. METHODOLOGY (RESEARCH PAPER DEFINITIONS) ---
st.divider()
st.markdown("<div class='theory-box'>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center; color:#4b6584; font-weight:700; margin-bottom:15px;'>Research Framework | Live Tax Basis: {tx_div}</div>", unsafe_allow_html=True)
st.markdown("""
<div style='background:white; padding:20px; border-radius:10px; border:1px solid #eee;'>
    <h4 style='color:#1e3799; text-align:center; margin-top:0;'>PILLARS OF YIELD EQUILIBRIUM</h4>
    <p style='font-size:0.88rem; color:#333;'><b>🏛️ PILLAR 01: NET-CORE WEALTH</b> - Stripping statutory taxes and distribution leakages.</p>
    <p style='font-size:0.88rem; color:#333;'><b>⚖️ PILLAR 02: TEMPORAL DISPLACEMENT</b> - Evaluating cumulative wealth over stay duration.</p>
    <p style='font-size:0.88rem; color:#333;'><b>🌐 PILLAR 03: VELOCITY MOMENTUM</b> - Dynamic pricing based on demand acceleration.</p>
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- 8. FOOTER ---
st.markdown("<div class='contact-section'>", unsafe_allow_html=True)
st.subheader("✉️ Contact System Developer")
st.write("Gayan Nugawela | gayan01@gmail.com")
st.markdown("</div>", unsafe_allow_html=True)
