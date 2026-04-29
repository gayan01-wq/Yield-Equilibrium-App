import streamlit as st
from datetime import date

# --- 1. CORE CONFIG & STYLING ---
st.set_page_config(layout="wide", page_title="Displacement Analyzer")

# High-visibility styling that won't break the script
st.markdown("""<style>
    .main-title {text-align: center; color: #1e3799; font-weight: 900; text-transform: uppercase;}
    .sub-title {text-align: center; color: #4b6584; font-weight: 600; margin-bottom: 20px;}
    [data-testid="stSidebar"] {background-color: #f1f4f9;}
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock"):
            if pwd == "Gayan2026":
                st.session_state["auth"] = True
                st.rerun()
            else: st.error("Denied")
    st.stop()

# --- 3. SIDEBAR INPUTS ---
with st.sidebar:
    st.subheader("👤 Developer: Gayan Nugawela")
    if st.button("🧹 Clear Cache"): st.rerun()
    st.divider()
    
    cur = st.selectbox("Currency", ["﷼", "රු", "฿", "د.إ", "$"])
    city = st.text_input("City Search", "Salalah")
    d1 = st.date_input("Check-In", date.today())
    d2 = st.date_input("Check-Out", date.today())
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    
    st.divider()
    otb = st.slider("OTB %", 0, 100, 15)
    hst = st.slider("Hist %", 0, 100, 45)
    v_mult = 1.35 if otb > hst else 0.85 if otb < (hst - 15) else 1.0
    
    tx = st.number_input("Tax Divisor", value=1.2327, format="%.4f")
    ota_p = st.slider("OTA Comm %", 0, 40, 15)
    p01 = st.number_input(f"P01 Fee ({cur})", value=6.90)
    meal_c = st.number_input("Meal Unit Cost", 0.0, format="%.3f")

# --- 4. CALCULATION ENGINE ---
def get_yield(rms, adr, hurdle, demand, is_ota=False):
    if rms <= 0: return None
    # Demand Adjustments
    d_map = {"Compression (Peak)": 15.0, "High Flow": 5.0, "Standard": 0.0, "Distressed": -5.0}
    eff_hurdle = hurdle + d_map.get(demand, 0)
    
    net_adr = adr / tx
    comm = (net_adr * (ota_p / 100)) if is_ota else 0.0
    unit_w = (net_adr - meal_c - comm) - p01
    
    status = "ACCEPT" if unit_w >= eff_hurdle else "REJECT"
    color = "green" if unit_w >= eff_hurdle else "red"
    return {"w": unit_w, "st": status, "cl": color, "total": unit_w * rms * m_nights}

# --- 5. MAIN INTERFACE ---
st.markdown("<h1 class='main-title'>DISPLACEMENT ANALYZER</h1>", unsafe_allow_html=True)
st.markdown("<div class='sub-title'>Yield Equilibrium Strategic Intelligence</div>", unsafe_allow_html=True)

st.success(f"📍 {city} | 📈 Velocity: {v_mult}x | 📅 Stay: {m_nights} Nights")

def draw_section(label, key, suggest_adr, floor, is_ota=False):
    with st.expander(f"📊 {label}", expanded=True):
        col1, col2, col3, col4 = st.columns([1, 1, 1, 1.2])
        rms = col1.number_input("Rooms", 0, key="r"+key)
        rate = col2.number_input(f"Rate", value=float(suggest_adr * v_mult), key="a"+key)
        dem = col3.selectbox("Demand", ["Standard", "Compression (Peak)", "Distressed"], key="d"+key)
        
        res = get_yield(rms, rate, floor, dem, is_ota)
        if res:
            col4.metric("Net Wealth", f"{cur}{res['w']:,.2f}")
            col4.markdown(f"**Verdict: :{res['cl']}[{res['st']}]**")
            col4.caption(f"Total Stay: {cur}{res['total']:,.2f}")

draw_section("DIRECT / FIT", "fit", 65, 40)
draw_section("OTA CHANNELS", "ota", 60, 35, is_ota=True)
draw_section("CORPORATE GROUPS", "corp", 55, 32)
draw_section("MICE GROUPS", "mice", 50, 30)

# --- 6. METHODOLOGY ---
st.divider()
st.subheader("Algorithmic Research Framework")
col_a, col_b, col_c = st.columns(3)
col_a.info("**PILLAR 01: NET-CORE**\nStripping tax and distribution leakages for Clean Asset Yield.")
col_b.info("**PILLAR 02: TEMPORAL LOS**\nEvaluating cumulative wealth over stay duration to prevent displacement.")
col_c.info("**PILLAR 03: VELOCITY**\nDynamic pricing derivatives based on OTB momentum.")

st.divider()
st.caption("System Developer: Gayan Nugawela | Contact: gayan01@gmail.com")
