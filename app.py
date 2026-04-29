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

/* Segment Card Styling */
.card{padding:12px; border-radius:10px; margin-bottom:10px; border-left:12px solid #1e3799; background:#ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff; padding:15px; border-radius:10px; border:1px solid #d1d9e6; margin-top:5px;}
.status-indicator{padding:12px; border-radius:10px; text-align:center; font-weight:900; font-size:1.1rem; color:white; margin-top:10px;}
.theory-box{background:#f9f9f9; padding:25px; border-radius:15px; border:1px solid #dee2e6; margin-top:30px}
[data-testid="stSidebar"]{background:#f1f4f9; border-right:1px solid #dee2e6}
.contact-section{background:#1e3799; padding:30px; border-radius:15px; margin-top:40px; color:white;}
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    st.markdown("<div class='header-container'><h1 class='main-title'>EQUILIBRIUM ENGINE</h1></div>", unsafe_allow_html=True)
    with st.form("login"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock"):
            if pwd == "Gayan2026": st.session_state["auth"] = True; st.rerun()
            else: st.error("Access Denied")
    st.stop()

# --- 3. SIDEBAR (STRATEGIC INPUTS) ---
with st.sidebar:
    st.markdown("### 👤 System Developer\nGayan Nugawela")
    if st.button("🧹 Clear Cache"): st.rerun()
    st.divider()
    cur = st.selectbox("Currency", ["﷼", "රු", "฿", "د.إ", "$"])
    city = st.text_input("City Search", "Salalah")
    d1 = st.date_input("Check-In", date.today())
    d2 = st.date_input("Check-Out", date.today())
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"📅 Stay Duration: {m_nights} Nights")
    
    st.divider()
    otb = st.slider("OTB %", 0, 100, 15); hst = st.slider("Hist %", 0, 100, 45)
    v_mult = 1.35 if otb > hst else 0.85 if otb < (hst - 15) else 1.0

    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f")
    ota_comm = st.slider("OTA Commission %", 0, 40, 15)
    p01_fee = st.number_input(f"P01 Fee ({cur})", value=6.90)
    bb_cost = st.number_input("Meal Unit Cost", 0.0, format="%.3f")

# --- 4. CALCULATION ENGINE ---
def run_yield(rms, adr, hurdle, demand, is_ota=False):
    if rms <= 0: return None
    d_adj = {"Compression": 15.0, "High Flow": 5.0, "Standard": 0.0, "Distressed": -5.0}
    eff_hurdle = hurdle + d_adj.get(demand, 0)
    net_adr = adr / tx_div
    comm = (net_adr * (ota_comm / 100)) if is_ota else 0.0
    unit_w = (net_adr - bb_cost - comm) - p01_fee
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

st.success(f"📍 Analysis: {city} | 📈 Velocity: {v_mult}x | 📅 Stay: {m_nights} Nights")

# --- 6. SEGMENT GENERATION (RESTORED FORMAT) ---
def draw_segment(label, key, suggest_adr, floor, is_ota=False):
    st.markdown(f"<div class='card'><b>{label}</b></div>", unsafe_allow_html=True)
    c1, c2 = st.columns([2.6, 1])
    with c1:
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        r1, r2, r3 = st.columns([0.8, 0.8, 1.2])
        rms = r1.number_input("Rooms", 0, key="r_"+key)
        rate = r2.number_input(f"Rate ({cur})", value=float(suggest_adr * v_mult), key="a_"+key)
        dem = r3.selectbox("Demand", ["Standard", "Compression", "Distressed"], key="d_"+key)
        
        m1, m2, m3, m4 = st.columns(4)
        m1.checkbox("RO", key="ro_"+key); m2.checkbox("BB", key="bb_"+key)
        m3.checkbox("HB", key="hb_"+key); m4.checkbox("FB", key="fb_"+key)
        st.markdown("</div>", unsafe_allow_html=True)
    
    res = run_yield(rms, rate, floor, dem, is_ota)
    if res:
        with c2:
            st.metric("Net Wealth Yield", f"{cur}{res['w']:,.2f}")
            st.markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']}</div>", unsafe_allow_html=True)
            st.caption(f"Total Wealth: {cur}{res['total']:,.2f}")

draw_segment("1. DIRECT / FIT", "fit", 65, 40)
draw_segment("2. OTA CHANNELS", "ota", 60, 35, is_ota=True)
draw_segment("3. CORPORATE GROUPS", "corp", 55, 32)
draw_segment("4. MICE GROUPS", "mice", 50, 30)

# --- 7. METHODOLOGY ---
st.divider()
st.markdown(f"""
<div class='theory-box'>
    <div style='text-align:center; color:#4b6584; font-weight:700;'>Research Methodology | Live Tax Basis: {tx_div}</div>
    <div style='margin-top:15px; background:white; padding:15px; border-radius:10px; border:1px solid #eee;'>
        <p style='font-size:0.85rem;'><b>🏛️ PILLAR 01: NET-CORE</b> - Stripping tax and distribution leakages.</p>
        <p style='font-size:
