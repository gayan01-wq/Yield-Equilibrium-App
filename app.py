import streamlit as st
from datetime import date

# --- 1. CORE STYLING (Executive Aesthetic) ---
st.set_page_config(layout="wide", page_title="Displacement Analyzer | Yield Equilibrium")
st.markdown("""<style>
.block-container{padding-top:1rem!important;}
.header-container {text-align: center; width: 100%; margin-bottom: 25px;}
.main-title {font-size: 2.2rem!important; font-weight: 900; color: #1e3799; text-transform: uppercase; letter-spacing: 2px; margin: 0;}
.main-subtitle {font-size: 1.1rem!important; font-weight: 600; color: #4b6584; letter-spacing: 1px; margin-top: 5px;}
.card{padding:15px; border-radius:10px; margin-bottom:15px; border-left:12px solid #1e3799; background:#ffffff; box-shadow: 0 2px 5px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff; padding:15px; border-radius:10px; border:1px solid #d1d9e6; margin-top:5px;}
.status-indicator{padding:12px; border-radius:10px; text-align:center; font-weight:900; font-size:1.1rem; color:white; margin-top:10px;}
.theory-box{background:#f1f4f9; padding:25px; border-radius:15px; border:1px solid #1e3799; margin-top:30px}
[data-testid="stSidebar"]{background:#f1f4f9;}
.contact-section{background:#1e3799; padding:30px; border-radius:15px; margin-top:40px; color:white;}
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    st.markdown("<div class='header-container'><h1 class='main-title'>EQUILIBRIUM ENGINE</h1></div>", unsafe_allow_html=True)
    with st.form("login"):
        if st.text_input("Access Key", type="password") == "Gayan2026" and st.form_submit_button("Unlock Engine"):
            st.session_state["auth"] = True; st.rerun()
    st.stop()

# --- 3. SIDEBAR (STRATEGIC INPUTS) ---
with st.sidebar:
    st.markdown("### 👤 System Developer\nGayan Nugawela")
    if st.button("🧹 Reset Cache"): st.rerun()
    st.divider()
    cur = st.selectbox("Base Currency", ["﷼", "රු", "฿", "د.إ", "₹", "$"])
    city = st.text_input("Analysis City", "Salalah")
    d1 = st.date_input("Check-In", date.today())
    d2 = st.date_input("Check-Out", date.today())
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"📅 Stay Duration: {m_nights} Nights")
    
    st.divider()
    otb, hst = st.slider("OTB %", 0, 100, 15), st.slider("Hist. %", 0, 100, 45)
    v_mult = 1.35 if otb > hst else 0.85 if otb < (hst - 15) else 1.0
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f")
    ota_c = st.slider("OTA Commission %", 0, 40, 15)
    p01_fee = st.number_input(f"P01 Fee ({cur})", value=6.90)
    
    st.markdown("### 🍽️ Unit Costs")
    meal_costs = {p: st.number_input(f"{p} Cost", v, step=0.5) for p, v in {"BB":2.5, "LN":4.5, "DN":5.5, "SAI":8.5, "AI":10.5}.items()}

# --- 4. ENGINE ---
def run_yield(rms, adr, meals, hurdle, demand, is_ota=False, mice=0, laundry=0):
    tr = sum(rms)
    if tr <= 0: return None
    eff_hurdle = hurdle + {"Compression (Peak)": 15.0, "High Flow": 5.0, "Standard": 0.0, "Distressed": -5.0}.get(demand, 0)
    net_adr = adr / tx_div
    comm = (net_adr * (ota_c / 100)) if is_ota else 0.0
    avg_m = sum(qty * meal_costs.get(p, 0) for p, qty in meals.items()) / tr
    unit_w = (net_adr - avg_m - comm) - p01_fee - laundry + (mice / tx_div)
    
    status, clr = ("ACCEPT", "#27ae60") if unit_w >= eff_hurdle else ("REJECT", "#e74c3c")
    return {"w": unit_w, "st": status, "cl": clr, "total": unit_w * tr * m_nights}

# --- 5. DASHBOARD HEADER ---
st.markdown(f"""
<div class='header-container'>
    <h1 class='main-title'>DISPLACEMENT ANALYZER</h1>
    <div class='main-subtitle'>Yield Equilibrium Strategic Intelligence Engine</div>
</div>
""", unsafe_allow_html=True)

t1, t2 = st.tabs(["🌐 Aviation Intelligence", "🗞️ Market News Feed"])
with t1: st.info(f"📍 City: {city} | 📈 Velocity: {v_mult}x | ✈️ Flights: Active Rotations")
with t2: st.warning(f"Market Alert: {city} is seeing stable growth in tourism arrivals.")

# --- 6. SEGMENTS ---
def draw_seg(label, key, suggest_adr, floor, color, is_ota=False, is_group=False):
    st.markdown(f"<div class='card' style='border-left-color:{color}'>{label}</div>", unsafe_allow_html=True)
    c1, c2 = st.columns([2.8, 1])
    with c1:
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        r1, r2, r3, r4 = st.columns([1,1,1,1.5])
        sgl, dbl, tpl = r1.number_input("SGL",0,key="s"+key), r2.number_input("DBL",0,key="d"+key), r3.number_input("TPL",0,key="t"+key)
        rate = r4.number_input(f"Rate ({cur})", value=float(suggest_adr * v_mult), key="a"+key)
        
        m_row = st.columns([1.5, 1, 1, 1, 1, 1])
        dem = m_row[0].selectbox("Demand", ["Standard", "Compression (Peak)", "Distressed"], key="dm"+key)
        m_vals = {p: m_row[i+1].number_input(p, 0, key=f"{p}{key}") for i, p in enumerate(["BB", "LN", "DN", "SAI", "AI"])}
        
        mice_v, lnd_v = 0, 0
        if is_group:
            g1, g2 = st.columns(2)
            mice_v = g1.number_input("MICE Revenue", 0.0, key="mi"+key)
            lnd_v = g2.number_input("Laundry Cost", 0.0, key="la"+key)
        st.markdown("</div>", unsafe_allow_html=True)
    
    res = run_yield([sgl, dbl, tpl], rate, m_vals, floor, dem, is_ota, mice_v, lnd_v)
    if res:
        with c2:
            st.metric("Net Wealth Yield", f"{cur}{res['w']:,.2f}")
            st.markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']}</div>", unsafe_allow_html=True)
            st.caption(f"Total Wealth: {cur}{res['total']:,.2f}")

draw_seg("1. DIRECT / FIT", "fit", 65, 40, "#3498db")
draw_seg("2. OTA CHANNELS", "ota", 60, 35, "#2ecc71", is_ota=True)
draw_seg("3. CORPORATE GROUPS", "corp", 55, 32, "#34495e", is_group=True)
draw_seg("4. MICE GROUPS", "mice", 50, 30, "#9b59b6", is_group=True)
draw_seg("5. TOUR & TRAVEL", "tnt", 45, 25, "#e67e22", is_group=True)

# --- 7. METHODOLOGY ---
st.markdown(f"""
<div class='theory-box'>
    <h4 style='color:#1e3799; text-align:center; margin-top:0;'>YIELD EQUILIBRIUM FRAMEWORK</h4>
    <p style='font-size:0.9rem; color:#333;'><b>🏛️ PILLAR 01: NET-CORE WEALTH</b> - Stripping tax ({tx_div}) and commissions.</p>
    <p style='font-size:0.9rem; color:#333;'><b>⚖️ PILLAR 02: TEMPORAL LOS</b> - Evaluating wealth over {m_nights} nights.</p>
    <p style='font-size:0.9rem; color:#333;'><b>🌐 PILLAR 03: VELOCITY MOMENTUM</b> - Pricing based on OTB acceleration.</p>
</div>
""", unsafe_allow_html=True)

# --- 8. FOOTER ---
st.markdown("<div class='contact-section'>", unsafe_allow_html=True)
st.subheader("✉️ Contact the System Developer")
st.write("Gayan Nugawela | gayan01@gmail.com")
st.markdown("</div>", unsafe_allow_html=True)
