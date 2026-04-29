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
    st.markdown("<div style='text-align:center;'><h1 class='main-title'>EQUILIBRIUM ENGINE</h1></div>", unsafe_allow_html=True)
    with st.form("login_gate"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock Engine"):
            if pwd == "Gayan2026": 
                st.session_state["auth"] = True
                st.rerun()
            else: st.error("Access Denied")
    st.stop()

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("### 👤 System Developer\nGayan Nugawela")
    if st.button("🧹 Reset System Cache"):
        st.session_state["reset_key"] += 1
        st.rerun()
    st.divider()
    
    rk = str(st.session_state["reset_key"]) 
    currencies = {"OMR (﷼)": "﷼", "LKR (රු)": "රු", "THB (฿)": "฿", "AED (د.إ)": "د.إ", "SAR (﷼)": "﷼", "INR (₹)": "₹", "USD ($)": "$"}
    cur_choice = st.selectbox("🌍 Base Currency", list(currencies.keys()), key="cur_"+rk)
    cur_sym = currencies[cur_choice]

    city_search = st.text_input("📍 City Search", "Salalah", key="c_nm_"+rk)
    d1 = st.date_input("Check-In", date.today(), key="d_in_"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d_out_"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"📅 **Stay Duration: {m_nights} Nights**")
    
    inventory = st.number_input("Total Capacity", 1, 1000, 237, key="inv_c_"+rk)
    
    st.divider()
    st.markdown("### 📊 Pillar 03: Velocity")
    otb_occ = st.slider("OTB %", 0, 100, 15, key="otb_s_"+rk)
    avg_hist = st.slider("Hist. Benchmark %", 0, 100, 45, key="hst_s_"+rk)
    v_mult = 1.35 if otb_occ > avg_hist else 0.85 if otb_occ < (avg_hist - 15) else 1.0

    st.divider()
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx_v_"+rk)
    ota_comm = st.slider("OTA Commission %", 0, 40, 15, key="ota_v_"+rk)
    p01_fee = st.number_input(f"P01 Fee ({cur_sym})", 0.0, value=6.90, key="p01_v_"+rk)

    st.markdown("### 🍽️ Unit Costs (Per Person)")
    meal_costs = {
        "RO": 0.0, 
        "BB": st.number_input("BB Cost", 0.0, format="%.3f", key="bb_mc_"+rk),
        "LN": st.number_input("LN Cost", 0.0, format="%.3f", key="ln_mc_"+rk), 
        "DN": st.number_input("DN Cost", 0.0, format="%.3f", key="dn_mc_"+rk),
        "SAI": st.number_input("SAI Cost", 0.0, format="%.3f", key="sai_mc_"+rk), 
        "AI": st.number_input("AI Cost", 0.0, format="%.3f", key="ai_mc_"+rk)
    }

# --- 4. ENGINE ---
def run_yield_engine(rms, adr, hurdle, demand, comm=0.0):
    total_rooms = sum(rms)
    if total_rooms <= 0: return None
    d_adj = {"Compression (Peak)": 15.0, "High Flow": 5.0, "Standard": 0.0, "Distressed": -5.0}
    eff_hurdle = hurdle + d_adj.get(demand, 0)
    net_adr = adr / tx_div
    unit_w = (net_adr - 0.0 - (net_adr * comm)) - p01_fee
    color = "#27ae60" if unit_w >= eff_hurdle else "#e74c3c"
    status = "ACCEPT" if unit_w >= eff_hurdle else "REJECT"
    # RECTIFIED LINE 91: Ensure the dictionary is fully closed
    return {"w": unit_w, "st": status, "cl": color, "total": unit_w * total_rooms * m_nights}

# --- 5. DASHBOARD HEADER ---
st.markdown("""
<div style="text-align: center;">
    <h1 class='main-title'>DISPLACEMENT ANALYZER</h1>
    <div class='main-subtitle'>Yield Equilibrium Strategic Intelligence Engine</div>
</div>
""", unsafe_allow_html=True)

st.info(f"📍 Analysis: {city_search} | 📈 Velocity: {v_mult}x | 📅 Stay: {m_nights} Nights")

# --- 6. SEGMENT GENERATION ---
def draw_segment(label, key, suggest_adr, floor, is_ota=False):
    st.markdown(f"<div class='card'><b>{label}</b></div>", unsafe_allow_html=True)
    c1, c2 = st.columns([2.5, 1])
    with c1:
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        r_col1, r_col2, r_col3 = st.columns(3)
        rms = r_col1.number_input("Rooms", 0, key="r_"+key)
        rate = r_col2.number_input(f"Rate ({cur_sym})", value=float(suggest_adr * v_mult), key="a_"+key)
        dem = r_col3.selectbox("Demand", ["Standard", "Compression (Peak)", "Distressed"], key="d_"+key)
        st.markdown("</div>", unsafe_allow_html=True)
    
    res = run_yield_engine([rms], rate, floor, dem, (ota_comm/100 if is_ota else 0.0))
    if res:
        with c2:
            st.metric("Net Wealth", f"{cur_sym}{res['w']:,.2f}")
            st.markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']}</div>", unsafe_allow_html=True)

draw_segment("1. DIRECT / FIT", "fit", 65, 40)
draw_segment("2. OTA CHANNELS", "ota", 60, 35, is_ota=True)
draw_segment("3. CORPORATE GROUPS", "corp", 55, 32)
draw_segment("4. MICE GROUPS", "mice", 50, 30)
draw_segment("5. TOUR & TRAVEL (GROUPS)", "tnt", 45, 25)

# --- 7. METHODOLOGY ---
st.divider()
st.markdown("<div class='theory-box'>", unsafe_allow_html=True)
st.markdown(f"<div style='text-align:center;'><b style='color:#4b6584;'>Strategic Operating Framework | Live Tax Basis: {tx_div}</b></div>", unsafe_allow_html=True)
st.markdown(f"""
<div class='theory-card' style='background:#f1f4f9; border: 1px solid #1e3799; padding:25px;'>
    <h4 style='color:#1e3799; margin-top:0; text-align:center;'>THEORY OF YIELD EQUILIBRIUM</h4>
    <div style='margin-top:10px;'>
        <p style='font-size:0.88rem; color:#333; margin-bottom:12px;'>
            <b>🏛️ PILLAR 01: NET-WEALTH DECONSTRUCTION (CLEAN ASSET YIELD)</b><br>
            Stripping statutory tax liabilities and distribution leakages to establish a Clean Asset Yield. 
        </p>
        <p style='font-size:0.88rem; color:#333; margin-bottom:12px;'>
            <b>⚖️ PILLAR 02: HURDLE EQUILIBRIUM & TEMPORAL LENGTH OF STAY (LOS)</b><br>
            Evaluating cumulative wealth across stay duration to prevent displacement.
        </p>
        <p style='font-size:0.88rem; color:#333;'>
            <b>🌐 PILLAR 03: EXTERNAL VELOCITY MOMENTUM ANALYTICS</b><br>
            Pricing adjusted via a Velocity Multiplier ({v_mult}x) derivative of OTB pace.
        </p>
    </div>
</div>
""", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# --- 8. FOOTER ---
st.markdown("<div class='contact-section'>", unsafe_allow_html=True)
st.subheader("✉️ Contact the System Developer")
col1, col2 = st.columns([1, 1])
with col1:
    contact_form = """
    <form action="https://formspree.io/f/mkoywogq" method="POST" style="display: flex; flex-direction: column; gap: 15px; background: white; padding: 20px; border-radius: 10px;">
        <input type="text" name="name" placeholder="Full Name" style="padding: 10px; border-radius: 5px; border: 1px solid #ddd; color: black;" required>
        <input type="email" name="email" placeholder="Work Email" style="padding: 10px; border-radius: 5px; border: 1px solid #ddd; color: black;" required>
        <textarea name="message" placeholder="Message..." style="padding: 10px; border-radius: 5px; border: 1px solid #ddd; height: 100px; color: black;" required></textarea>
        <button type="submit" style="background-color: #1e3799; color: white; padding: 12px; border: none; border-radius: 5px; cursor: pointer; font-weight: bold; font-size: 1rem;">🚀 Submit to Developer</button>
    </form>
    """
    st.markdown(contact_form, unsafe_allow_html=True)
with col2:
    st.markdown("### Logic Desk Details\n* **Email:** gayan01@gmail.com\n* **Research Scope:** Displacement Modelling.")
st.markdown("</div>", unsafe_allow_html=True)
