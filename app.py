import streamlit as st
from datetime import date

# --- 1. CORE CONFIG & EXECUTIVE STYLING ---
st.set_page_config(layout="wide", page_title="Displacement Analyzer | Yield Equilibrium")

st.markdown("""<style>
.block-container{padding-top:1rem!important;}
/* Perfect Header Centering */
.header-wrapper {text-align: center; width: 100%; margin-bottom: 25px;}
.main-title {font-size: 2.2rem!important; font-weight: 900; color: #1e3799; text-transform: uppercase; letter-spacing: 2px; margin: 0;}
.main-subtitle {font-size: 1.1rem!important; font-weight: 600; color: #4b6584; letter-spacing: 1px; margin-top: 5px;}

.card{padding:15px; border-radius:10px; margin-bottom:15px; border-left:12px solid #1e3799; background:#ffffff; box-shadow: 0 2px 5px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff; padding:15px; border-radius:10px; border:1px solid #d1d9e6;}
.metric-box{background:#1e3799; color:white; padding:15px; border-radius:10px; text-align:center;}
.status-tag{padding:10px; border-radius:8px; text-align:center; font-weight:900; color:white; margin-top:10px; text-transform:uppercase;}
[data-testid="stSidebar"]{background:#f1f4f9;}
.footer-text{text-align:center; color:#4b6584; font-size:0.85rem; margin-top:30px;}
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if "reset_key" not in st.session_state: st.session_state["reset_key"] = 0

if not st.session_state["auth"]:
    st.markdown("<div class='header-wrapper'><h1 class='main-title'>EQUILIBRIUM ENGINE</h1></div>", unsafe_allow_html=True)
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
    cur_sym = st.selectbox("Base Currency", ["﷼", "රු", "฿", "د.إ", "₹", "$"], key="cur_"+rk)
    city = st.text_input("Analysis City", "Salalah", key="city_"+rk)
    d1 = st.date_input("Check-In", date.today(), key="d1_"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d2_"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"📅 Stay Duration: {m_nights} Nights")
    
    st.divider()
    st.markdown("### 📊 Velocity Analytics")
    otb = st.slider("OTB %", 0, 100, 15, key="otb_"+rk)
    hst = st.slider("Hist. Benchmark %", 0, 100, 45, key="hst_"+rk)
    v_mult = 1.35 if otb > hst else 0.85 if otb < (hst - 15) else 1.0

    st.divider()
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx_"+rk)
    ota_c = st.slider("OTA Commission %", 0, 40, 15, key="ota_"+rk)
    p01_fee = st.number_input(f"P01 Fee ({cur_sym})", value=6.90, key="p01_"+rk)
    bb_cost = st.number_input("Meal Unit Cost", 0.0, format="%.3f", key="bb_c_"+rk)

# --- 4. CALCULATION ENGINE ---
def run_yield(rms, adr, hurdle, demand, is_ota=False):
    if rms <= 0: return None
    # Pillar 02 Logic
    d_adj = {"Compression (Peak)": 15.0, "High Flow": 5.0, "Standard": 0.0, "Distressed": -5.0}
    eff_hurdle = hurdle + d_adj.get(demand, 0)
    
    # Pillar 01 Logic
    net_adr = adr / tx_div
    comm = (net_adr * (ota_c / 100)) if is_ota else 0.0
    unit_w = (net_adr - bb_cost - comm) - p01_fee
    
    status = "ACCEPT" if unit_w >= eff_hurdle else "REJECT"
    color = "#27ae60" if unit_w >= eff_hurdle else "#e74c3c"
    return {"w": unit_w, "st": status, "cl": color, "total": unit_w * rms * m_nights}

# --- 5. DASHBOARD HEADER ---
st.markdown(f"""
<div class='header-wrapper'>
    <h1 class='main-title'>DISPLACEMENT ANALYZER</h1>
    <div class='main-subtitle'>Yield Equilibrium Strategic Intelligence Engine</div>
</div>
""", unsafe_allow_html=True)

st.info(f"📍 Analysis: {city} | 📈 Velocity: {v_mult}x | 📅 Stay: {m_nights} Nights")

# --- 6. SEGMENTS ---
def draw_seg(label, key, suggest_adr, floor, is_ota=False):
    st.markdown(f"<div class='card'><b>{label}</b></div>", unsafe_allow_html=True)
    c_in, c_met = st.columns([2.8, 1])
    
    with c_in:
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        r1, r2, r3 = st.columns([1, 1, 1.5])
        rms = r1.number_input("Rooms", 0, key="r_"+key)
        rate = r2.number_input(f"Rate ({cur_sym})", value=float(suggest_adr * v_mult), key="a_"+key)
        dem = r3.selectbox("Demand Context", ["Standard", "Compression (Peak)", "Distressed"], key="d_"+key)
        
        m1, m2, m3, m4 = st.columns(4)
        m1.checkbox("RO", key="ro_"+key); m2.checkbox("BB", key="bb_"+key)
        m3.checkbox("HB", key="hb_"+key); m4.checkbox("FB", key="fb_"+key)
        st.markdown("</div>", unsafe_allow_html=True)
    
    res = run_yield(rms, rate, floor, dem, is_ota)
    with c_met:
        if res:
            st.markdown(f"""
            <div class='metric-box'>
                <small>Net Wealth Yield</small><br>
                <span style='font-size:1.4rem; font-weight:bold;'>{cur_sym}{res['w']:,.2f}</span>
            </div>
            <div class='status-tag' style='background:{res['cl']}'>{res['st']}</div>
            <div style='text-align:center; font-size:0.8rem; margin-top:5px; color:#4b6584;'>
                Total Stay Wealth: {cur_sym}{res['total']:,.2f}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Waiting for input...")

draw_seg("1. DIRECT / FIT", "fit", 65, 40)
draw_seg("2. OTA CHANNELS", "ota", 60, 35, is_ota=True)
draw_seg("3. CORPORATE GROUPS", "corp", 55, 32)
draw_seg("4. MICE GROUPS", "mice", 50, 30)
draw_seg("5. TOUR & TRAVEL (GROUPS)", "tnt", 45, 25)

# --- 7. METHODOLOGY ---
st.divider()
st.markdown(f"""
<div style='background:#f1f4f9; padding:25px; border-radius:15px; border:1px solid #1e3799;'>
    <h4 style='color:#1e3799; text-align:center; margin-top:0;'>RESEARCH SUMMARY: YIELD EQUILIBRIUM MODELLING</h4>
    <div style='margin-top:10px;'>
        <p style='font-size:0.88rem; color:#333; margin-bottom:12px;'>
            <b>🏛️ PILLAR 01: NET-WEALTH DECONSTRUCTION (CLEAN ASSET YIELD)</b><br>
            Stripping statutory tax liabilities ({tx_div}) and distribution leakages to establish Clean Asset Yield. 
        </p>
        <p style='font-size:0.88rem; color:#333; margin-bottom:12px;'>
            <b>⚖️ PILLAR 02: HURDLE EQUILIBRIUM & TEMPORAL LOS WEIGHING</b><br>
            Evaluating cumulative wealth
