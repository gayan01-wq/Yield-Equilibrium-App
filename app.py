import streamlit as st
from datetime import date

# --- 1. CORE CONFIG & EXECUTIVE STYLING ---
st.set_page_config(layout="wide", page_title="Displacement Analyzer | Yield Equilibrium")

st.markdown("""<style>
.block-container{padding-top:1rem!important;}
.header-wrapper {text-align: center; width: 100%; margin-bottom: 25px;}
.main-title {font-size: 2.2rem!important; font-weight: 900; color: #1e3799; text-transform: uppercase; letter-spacing: 2px; margin: 0;}
.main-subtitle {font-size: 1.1rem!important; font-weight: 600; color: #4b6584; letter-spacing: 1px; margin-top: 5px;}
.card{padding:10px; border-radius:10px; margin-bottom:8px; border-left:10px solid #1e3799; background:#ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff; padding:12px; border-radius:10px; border:1px solid #d1d9e6; margin-top:5px;}
.status-indicator{padding:12px; border-radius:10px; text-align:center; font-weight:900; font-size:1.1rem; color:white; margin-top:10px;}
[data-testid="stSidebar"]{background:#f1f4f9;}
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    st.markdown("<div class='header-wrapper'><h1 class='main-title'>EQUILIBRIUM ENGINE</h1></div>", unsafe_allow_html=True)
    with st.form("login"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock"):
            if pwd == "Gayan2026": 
                st.session_state["auth"] = True
                st.rerun()
            else: st.error("Access Denied")
    st.stop()

# --- 3. SIDEBAR (STRATEGIC INPUTS) ---
with st.sidebar:
    st.markdown("### 👤 System Developer\nGayan Nugawela")
    if st.button("🧹 Reset Cache"): st.rerun()
    st.divider()
    cur = st.selectbox("Currency", ["﷼", "රු", "฿", "د.إ", "₹", "$"])
    city = st.text_input("City Search", "Salalah")
    d1 = st.date_input("Check-In", date.today())
    d2 = st.date_input("Check-Out", date.today())
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"📅 Stay: {m_nights} Nights")
    
    st.divider()
    otb = st.slider("OTB %", 0, 100, 15)
    hst = st.slider("Hist. %", 0, 100, 45)
    v_mult = 1.35 if otb > hst else 0.85 if otb < (hst - 15) else 1.0
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f")
    ota_c = st.slider("OTA Comm %", 0, 40, 15)
    p01 = st.number_input(f"P01 Fee ({cur})", value=6.90)
    meal_c = st.number_input("Meal Cost", 0.0, format="%.3f")

# --- 4. ENGINE ---
def run_yield(rms, adr, hurdle, demand, is_ota=False):
    if rms <= 0: return None
    d_adj = {"Compression (Peak)": 15.0, "High Flow": 5.0, "Standard": 0.0, "Distressed": -5.0}
    eff_hurdle = hurdle + d_adj.get(demand, 0)
    net_adr = adr / tx_div
    comm = (net_adr * (ota_c / 100)) if is_ota else 0.0
    unit_w = (net_adr - meal_c - comm) - p01
    status = "ACCEPT" if unit_w >= eff_hurdle else "REJECT"
    color = "#27ae60" if unit_w >= eff_hurdle else "#e74c3c"
    return {"w": unit_w, "st": status, "cl": color, "total": unit_w * rms * m_nights}

# --- 5. HEADER (CENTERED) ---
st.markdown(f"""
<div class='header-wrapper'>
    <h1 class='main-title'>DISPLACEMENT ANALYZER</h1>
    <div class='main-subtitle'>Yield Equilibrium Strategic Intelligence Engine</div>
</div>
""", unsafe_allow_html=True)

# --- 6. SEGMENTS ---
def draw_seg(label, key, suggest_adr, floor, is_ota=False):
    st.markdown(f"<div class='card'><b>{label}</b></div>", unsafe_allow_html=True)
    c_in, c_res = st.columns([2.6, 1])
    with c_in:
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        r1, r2, r3 = st.columns([1, 1, 1.5])
        rms = r1.number_input("Rooms", 0, key="r_"+key)
        rate = r2.number_input(f"Rate ({cur})", value=float(suggest_adr * v_mult), key="a_"+key)
        dem = r3.selectbox("Demand", ["Standard", "Compression (Peak)", "Distressed"], key="d_"+key)
        m1, m2, m3, m4 = st.columns(4)
        m1.checkbox("RO", key="ro_"+key); m2.checkbox("BB", key="bb_"+key)
        m3.checkbox("HB", key="hb_"+key); m4.checkbox("FB", key="fb_"+key)
        st.markdown("</div>", unsafe_allow_html=True)
    
    res = run_yield(rms, rate, floor, dem, is_ota)
    if res:
        with c_res:
            st.metric("Net Wealth", f"{cur}{res['w']:,.2f}")
            st.markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']}</div>", unsafe_allow_html=True)

draw_seg("1. DIRECT / FIT", "fit", 65, 40)
draw_seg("2. OTA CHANNELS", "ota", 60, 35, is_ota=True)
draw_seg("3. CORPORATE GROUPS", "corp", 55, 32)
draw_seg("4. MICE GROUPS", "mice", 50, 30)
draw_seg("5. TOUR & TRAVEL (GROUPS)", "tnt", 45, 25)

st.divider()
st.markdown(f"<div style='text-align:center; color:#4b6584; font-size:0.8rem;'>System Developer: Gayan Nugawela | gayan01@gmail.com</div>", unsafe_allow_html=True)
