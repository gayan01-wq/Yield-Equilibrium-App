import streamlit as st
from datetime import date

# --- 1. CORE CONFIG & EXECUTIVE STYLING ---
st.set_page_config(layout="wide", page_title="Displacement Analyzer | Yield Equilibrium")

st.markdown("""<style>
    .block-container{padding-top:1rem!important;}
    .header-wrapper {text-align: center; width: 100%; margin-bottom: 25px;}
    .main-title {font-size: 2.2rem!important; font-weight: 900; color: #1e3799; text-transform: uppercase; letter-spacing: 2px; margin: 0;}
    .main-subtitle {font-size: 1.1rem!important; font-weight: 600; color: #4b6584; letter-spacing: 1px; margin-top: 5px;}
    .card{padding:15px; border-radius:10px; margin-bottom:15px; border-left:12px solid #1e3799; background:#ffffff; box-shadow: 0 2px 5px rgba(0,0,0,0.1)}
    [data-testid="stSidebar"]{background:#f1f4f9;}
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state: st.session_state["auth"] = False
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
    if st.button("🧹 Reset System Cache"): st.rerun()
    st.divider()
    
    cur_sym = st.selectbox("Base Currency", ["﷼", "රු", "฿", "د.إ", "₹", "$"])
    city = st.text_input("Analysis City", "Salalah")
    d1 = st.date_input("Check-In", date.today())
    d2 = st.date_input("Check-Out", date.today())
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    
    st.divider()
    st.markdown("### 📊 Velocity Analytics")
    otb = st.slider("OTB %", 0, 100, 15)
    hst = st.slider("Hist. %", 0, 100, 45)
    v_mult = 1.35 if otb > hst else 0.85 if otb < (hst - 15) else 1.0

    st.divider()
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f")
    ota_c = st.slider("OTA Commission %", 0, 40, 15)
    p01_fee = st.number_input(f"P01 Fee ({cur_sym})", value=6.90)
    meal_cost = st.number_input("Meal Unit Cost", 0.0, format="%.3f")

# --- 4. CALCULATION ENGINE ---
def run_yield(rms, adr, hurdle, demand, is_ota=False):
    if rms <= 0: return None
    d_adj = {"Compression (Peak)": 15.0, "High Flow": 5.0, "Standard": 0.0, "Distressed": -5.0}
    eff_hurdle = hurdle + d_adj.get(demand, 0)
    net_adr = adr / tx_div
    comm = (net_adr * (ota_c / 100)) if is_ota else 0.0
    unit_w = (net_adr - meal_cost - comm) - p01_fee
    
    status = "ACCEPT" if unit_w >= eff_hurdle else "REJECT"
    color = "green" if unit_w >= eff_hurdle else "red"
    return {"w": unit_w, "st": status, "cl": color, "total": unit_w * rms * m_nights}

# --- 5. DASHBOARD HEADER ---
st.markdown(f"""
<div class='header-wrapper'>
    <h1 class='main-title'>DISPLACEMENT ANALYZER</h1>
    <div class='main-subtitle'>Yield Equilibrium Strategic Intelligence Engine</div>
</div>
""", unsafe_allow_html=True)

st.info(f"📍 {city} | 📈 Velocity: {v_mult}x | 📅 Stay: {m_nights} Nights")

# --- 6. SEGMENTS ---
def draw_seg(label, key, suggest_adr, floor, is_ota=False):
    st.markdown(f"<div class='card'><b>{label}</b></div>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1, 1, 1, 1.2])
    
    rms = c1.number_input("Rooms", 0, key="r_"+key)
    rate = c2.number_input(f"Rate", value=float(suggest_adr * v_mult), key="a_"+key)
    dem = c3.selectbox("Demand", ["Standard", "Compression (Peak)", "Distressed"], key="d_"+key)
    
    res = run_yield(rms, rate, floor, dem, is_ota)
    if res:
        c4.metric("Net Wealth Yield", f"{cur_sym}{res['w']:,.2f}")
        c4.markdown(f"**Verdict: :{res['cl']}[{res['st']}]**")
        c4.caption(f"Stay Wealth: {cur_sym}{res['total']:,.2f}")

draw_seg("1. DIRECT / FIT", "fit", 65, 40)
draw_seg("2. OTA CHANNELS", "ota", 60, 35, is_ota=True)
draw_seg("3. CORPORATE GROUPS", "corp", 55, 32)
draw_seg("4. MICE GROUPS", "mice", 50, 30)

# --- 7. METHODOLOGY ---
st.divider()
st.subheader("Algorithmic Research Framework")
col_a, col_b, col_c = st.columns(3)
col_a.info("**PILLAR 01: NET-CORE**\nStripping tax and commissions for Clean Asset Yield.")
col_b.info("**PILLAR 02: TEMPORAL LOS**\nEvaluating cumulative wealth over stay duration to prevent displacement.")
col_c.info("**PILLAR 03: VELOCITY**\nDynamic pricing derivatives based on OTB momentum.")

st.divider()
st.caption("System Developer: Gayan Nugawela | Contact: gayan01@gmail.com")
