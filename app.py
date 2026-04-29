import streamlit as st
from datetime import date

# --- 1. CORE CONFIG & EXECUTIVE STYLING ---
st.set_page_config(layout="wide", page_title="Displacement Analyzer | Yield Equilibrium")

st.markdown("""<style>
.block-container{padding-top:1rem!important;}
.main-title{font-size:2.0rem!important;font-weight:900;color:#1e3799;text-align:center;margin-top:-10px;text-transform:uppercase;letter-spacing:2px;}
.main-subtitle{font-size:1.1rem!important;font-weight:600;color:#4b6584;text-align:center;margin-top:-15px;margin-bottom:25px;letter-spacing:1px;}
.card{padding:10px;border-radius:10px;margin-bottom:8px;border-left:10px solid #1e3799;background:#ffffff;box-shadow: 0 2px 4px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff;padding:12px;border-radius:10px;border:1px solid #d1d9e6; margin-top:5px;}
.status-indicator{padding:12px; border-radius:10px; text-align:center; font-weight:900; font-size:1.1rem; color:white; margin-top:10px;}
.reason-box{background:#fff9c4; border:1px solid #fbc02d; padding:10px; border-radius:8px; margin-top:5px; font-size:0.8rem;}
.theory-box{background:#f9f9f9; padding:25px; border-radius:15px; border:1px solid #dee2e6; margin-top:30px}
.theory-card{background:white; padding:15px; border-radius:10px; border:1px solid #eee; margin-bottom:12px;}
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
    city = st.text_input("Analysis City", "Salalah", key="city_"+rk)
    d1 = st.date_input("Check-In", date.today(), key="d1_"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d2_"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    inventory = st.number_input("Property Capacity", 1, 1000, 237, key="inv_"+rk)
    
    st.divider()
    st.markdown("### 📊 Velocity Analytics")
    otb = st.slider("OTB %", 0, 100, 15, key="otb_"+rk)
    hst = st.slider("Hist. Benchmark %", 0, 100, 45, key="hst_"+rk)
    v_mult = 1.35 if otb > hst else 0.85 if otb < (hst - 15) else 1.0
    
    st.divider()
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx_"+rk)
    ota_c = st.slider("OTA Comm %", 0, 40, 15, key="ota_"+rk)
    
    st.markdown("### 🍽️ Unit Costs (0.000 Precision)")
    bb_cost = st.number_input("BB per person", 0.0, format="%.3f", key="bb_"+rk)
    ai_cost = st.number_input("AI per person", 0.0, format="%.3f", key="ai_"+rk)

# --- 4. ENGINE ---
def run_yield_engine(rooms, adr, hurdle, demand, comm=0.0):
    total_rooms = sum(rooms)
    if total_rooms <= 0: return None
    d_adj = {"Compression (Peak)": 15.0, "High Flow": 5.0, "Standard": 0.0, "Distressed": -5.0}
    eff_hurdle = hurdle + d_adj.get(demand, 0)
    net_adr = adr / tx_div
    unit_w = (net_adr - bb_cost - (net_adr * comm)) - 6.90
    status = "ACCEPT" if unit_w >= eff_hurdle else "REJECT"
    color = "#27ae60" if unit_w >= eff_hurdle else "#e74c3c"
    total_w = unit_w * total_rooms * m_nights
    return {"w": unit_w, "st": status, "cl": color, "total": total_w}

# --- 5. DASHBOARD HEADER ---
st.markdown("<h1 class='main-title'>DISPLACEMENT ANALYZER</h1>", unsafe_allow_html=True)
st.markdown("<div class='main-subtitle'>Yield Equilibrium Strategic Intelligence</div>", unsafe_allow_html=True)
st.info(f"📍 Analysis: {city} | 📈 Velocity: {v_mult}x | 📅 Length of Stay: {m_nights} Nights")

# --- 6. SEGMENT GENERATION ---
def draw_segment(label, key, suggest_adr, floor, is_ota=False):
    st.markdown(f"<div class='card'><b>{label}</b></div>", unsafe_allow_html=True)
    c1, c2 = st.columns([2.5, 1])
    with c1:
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        r1, r2, r3 = st.columns(3)
        rms = r1.number_input("Rooms", 0, key="r_"+key)
        rate = r2.number_input("Rate", value=float(suggest_adr * v_mult), key="a_"+key)
        dem = r3.selectbox("Demand Context", ["Standard", "Compression (Peak)", "Distressed"], key="d_"+key)
        st.markdown("</div>", unsafe_allow_html=True)
    
    res = run_yield_engine([rms], rate, floor, dem, (ota_c/100 if is_ota else 0.0))
    if res:
        with c2:
            st.metric("Net Wealth", f"{cur_sym}{res['w']:,.2f}")
            st.markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='reason-box'>Total Stay Wealth: {cur_sym}{res['total']:,.2f}</div>", unsafe_allow_html=True)

draw_segment("1. DIRECT / FIT", "fit", 65, 40)
draw_segment("2. OTA CHANNELS", "ota", 60, 35, is_ota=True)
draw_segment("3. GROUPS / MICE", "grp", 50, 30)

# --- 7. METHODOLOGY (RESEARCH PAPER DEFINITIONS) ---
st.divider()
st.markdown("<div class='theory-box'>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align:center; color:#1e3799;'>Algorithmic Research Framework</h3>", unsafe_allow_html=True)

st.markdown(f"""
<div class='theory-card'>
    <b>🏛️ PILLAR 01: NET-WEALTH DECONSTRUCTION (CLEAN ASSET YIELD)</b><br>
    The model identifies <b>'Clean Asset Yield'</b> by stripping statutory tax liabilities and distribution leakages. This ensures revenue volume does not mask unit-level margin erosion.
</div>
<div class='theory-card'>
    <b>⚖️ PILLAR 02: TEMPORAL LENGTH OF STAY (LOS) YIELDING</b><br>
    The engine evaluates cumulative wealth across the <b>{m_nights}-night stay</b>. This temporal analysis determines if the total wealth generated justifies inventory displacement. Hurdle offsets (Compression +15.0) act as filters during high-velocity windows.
</div>
<div class='theory-card'>
    <b>🌐 PILLAR 03: EXTERNAL VELOCITY MOMENTUM ANALYTICS</b><br>
    Pricing is dynamically adjusted via a <b>Velocity Multiplier ({v_mult}x)</b>. This is a derivative of OTB pace vs historical benchmarks. Acceleration beyond the mean triggers a positive multiplier to capture localized consumer surplus.
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- 8. FOOTER ---
st.markdown("<div class='contact-section'>", unsafe_allow_html=True)
st.subheader("✉️ Contact the System Developer")
st.write("Direct queries to Gayan Nugawela regarding algorithmic logic or research data requests.")
st.write("**Email:** gayan01@gmail.com")
st.markdown("</div>", unsafe_allow_html=True)
