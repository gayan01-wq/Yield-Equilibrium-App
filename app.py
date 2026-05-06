import streamlit as st
from datetime import date

# --- 1. STYLING ---
st.set_page_config(layout="wide", page_title="Displacement Analyzer | Yield Equilibrium")
st.markdown("""<style>
.block-container{padding-top:1rem!important;}
.main-title { font-size: 2.2rem!important; font-weight: 900; color: #1e3799; text-align: center; text-transform: uppercase; letter-spacing: 2px; }
.card{padding:10px; border-radius:10px; margin-bottom:8px; border-left:10px solid; background:#ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff; padding:12px; border-radius:10px; border:1px solid #d1d9e6; margin-top:5px;}
.noi-card { background-color: #f8f9fa; padding: 25px; border-radius: 12px; border-left: 10px solid #1e3799; color: #2f3640; }
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION & CACHE ---
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

# --- 3. SIDEBAR (STRATEGIC INPUTS) ---
rk = str(st.session_state["reset_key"])
with st.sidebar:
    st.markdown("### 📊 Pillar 01: Simulation")
    sim_rooms = st.slider("Simulate Room Inventory Shift", 5, 10000, 40, key="sim_s_"+rk)
    
    st.divider()
    st.markdown("### 📅 Stay Period")
    d1 = st.date_input("Check-In", date.today(), key="d_in_"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d_out_"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"Stay Duration: {m_nights} Nights")

    st.divider()
    currencies = {"OMR (﷼)": "﷼", "LKR (රු)": "රු", "USD ($)": "$"}
    cur_choice = st.selectbox("🌍 Currency", list(currencies.keys()), key="c_sel_"+rk)
    cur_sym = currencies[cur_choice]

    st.markdown("### 🏛️ Statutory Deflators")
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx_v_"+rk)
    ota_comm = st.slider("OTA Commission %", 0, 40, 15, key="ota_v_"+rk)
    p01_fee = st.number_input(f"P01 Fee ({cur_sym})", 0.0, value=6.90, key="p01_v_"+rk)

    st.markdown("### 🍽️ Unit Costs (Meal Plans)")
    meal_costs = {
        "RO": 0.0, "BB": st.number_input("BB Cost", 0.0, key="bb_mc_"+rk),
        "HB": st.number_input("HB Cost", 0.0, key="hb_mc_"+rk), "FB": st.number_input("FB Cost", 0.0, key="fb_mc_"+rk),
        "SAI": st.number_input("SAI Cost", 0.0, key="sai_mc_"+rk), "AI": st.number_input("AI Cost", 0.0, key="ai_mc_"+rk)
    }

# --- 4. CALCULATION ENGINE ---
def run_segment_yield(adr, meals, comm_rate=0.0):
    net_adr = adr / tx_div
    total_meal_cost = sum(qty * meal_costs.get(p, 0) for p, qty in meals.items())
    unit_w = (net_adr - total_meal_cost - (net_adr * comm_rate)) - p01_fee
    return unit_w

# --- 5. DASHBOARD ---
st.markdown("<h1 class='main-title'>DISPLACEMENT ANALYZER</h1>", unsafe_allow_html=True)
st.divider()

# RENDER SEGMENTS
segments = [
    {"label": "1. DIRECT / FIT", "key": "fit", "color": "#3498db", "ota": False},
    {"label": "2. OTA CHANNELS", "key": "ota", "color": "#2ecc71", "ota": True},
    {"label": "3. CORPORATE / MICE GROUPS", "key": "mice", "color": "#34495e", "ota": False},
    {"label": "4. GROUP TOUR & TRAVEL", "key": "tnt", "color": "#e67e22", "ota": False}
]

# Track Net Wealth for the Simulation
wealth_results = {}

for seg in segments:
    st.markdown(f"<div class='card' style='border-left-color:{seg['color']}'>{seg['label']}</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        cols = st.columns([1.5, 0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 1.2])
        adr = cols[0].number_input(f"Rate ({cur_sym})", value=75.0, key=f"adr_{seg['key']}_{rk}")
        ro = cols[1].number_input("RO", 0, key=f"ro_{seg['key']}_{rk}")
        bb = cols[2].number_input("BB", 0, key=f"bb_{seg['key']}_{rk}")
        hb = cols[3].number_input("HB", 0, key=f"hb_{seg['key']}_{rk}")
        fb = cols[4].number_input("FB", 0, key=f"fb_{seg['key']}_{rk}")
        sai = cols[5].number_input("SAI", 0, key=f"sai_{seg['key']}_{rk}")
        ai = cols[6].number_input("AI", 0, key=f"ai_{seg['key']}_{rk}")
        
        # Calculation
        comm = (ota_comm/100) if seg['ota'] else 0.0
        net_wealth = run_segment_yield(adr, {"RO":ro,"BB":bb,"HB":hb,"FB":fb,"SAI":sai,"AI":ai}, comm)
        total_pax = ro + bb + hb + fb + sai + ai
        
        cols[7].metric("Net Wealth", f"{cur_sym} {net_wealth:,.2f}")
        wealth_results[seg['key']] = net_wealth
        st.markdown("</div>", unsafe_allow_html=True)

# --- 6. FORECASTING & NOI IMPROVEMENT (Pillar 02) ---
st.divider()
st.markdown("### 📈 Strategic NOI Simulation (A vs B)")
# Simulation: Comparing Direct/FIT (A) vs OTA (B) as a default hurdle
net_a = wealth_results['fit']
net_b = wealth_results['ota']

improvement_val = (net_a - net_b) * sim_rooms * m_nights
improvement_pct = ((net_a - net_b) / net_b * 100) if net_b != 0 else 0

m1, m2, m3 = st.columns(3)
with m1: st.metric("Net Flow Gap (A-B)", f"{cur_sym} {net_a - net_b:,.2f}")
with m2: st.metric("Total NOI Gain", f"{cur_sym} {improvement_val:,.2f}")
with m3: st.metric("NOI % Improvement", f"{improvement_pct:.2f}%")

status = "ACCEPT: ACCRETIVE" if net_a > net_b else "REJECT: DILUTIVE"
st.markdown(f"""
<div class='noi-card'>
    <h4>Executive Summary: {status}</h4>
    Shifting <b>{sim_rooms} rooms</b> for <b>{m_nights} nights</b> to Direct/FIT identifies a 
    <b>{improvement_pct:.2f}%</b> NOI improvement, adding <b>{cur_sym} {improvement_val:,.2f}</b> 
    to the wealth-core.
</div>
""", unsafe_allow_html=True)

# Handoff
st.session_state["current_audit"] = {"yield": net_a, "hurdle": net_b, "status": status, "rooms": sim_rooms}
if st.button("🚀 Run Pillar 02: Strategic AI Audit"): st.switch_page("pages/strategic_gem.py")
