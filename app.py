import streamlit as st
from datetime import date
import os

# --- 1. SETTINGS & STYLING ---
st.set_page_config(layout="wide", page_title="Displacement Analyzer | Yield Equilibrium")

st.markdown("""<style>
.main-title { font-size: 2.2rem!important; font-weight: 900; color: #1e3799; text-align: center; text-transform: uppercase; }
.card{padding:10px; border-radius:10px; margin-bottom:8px; border-left:10px solid; background:#ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff; padding:12px; border-radius:10px; border:1px solid #d1d9e6; margin-top:5px;}
.status-indicator{padding:12px; border-radius:10px; text-align:center; font-weight:900; font-size:1.1rem; color:white; margin-top:10px;}
.noi-card { background-color: #f8f9fa; padding: 25px; border-radius: 12px; border-left: 10px solid #1e3799; color: #2f3640; }
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
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

# --- 4. ENGINE LOGIC ---
def run_segment_yield(adr, meal_qty, hurdle, comm_rate=0.0):
    net_adr = adr / tx_div
    total_meal_cost = sum(qty * meal_costs.get(p, 0) for p, qty in meal_qty.items())
    unit_w = (net_adr - total_meal_cost - (net_adr * comm_rate)) - p01_fee
    
    # Classification Logic (Restored Optimized, Marginal, Dilutive)
    if unit_w < hurdle:
        stt, clr = "REJECT: DILUTIVE", "#e74c3c"
    elif unit_w < (hurdle + 5.0):
        stt, clr = "REVIEW: MARGINAL", "#f39c12"
    else:
        stt, clr = "ACCEPT: OPTIMIZED", "#27ae60"
        
    return {"w": unit_w, "st": stt, "cl": clr}

# --- 5. DASHBOARD ---
st.markdown("<h1 class='main-title'>DISPLACEMENT ANALYZER</h1>", unsafe_allow_html=True)
st.divider()

segments = [
    {"label": "1. DIRECT / FIT", "key": "fit", "color": "#3498db", "ota": False, "hurdle": 45.0},
    {"label": "2. OTA CHANNELS", "key": "ota", "color": "#2ecc71", "ota": True, "hurdle": 35.0},
    {"label": "3. CORPORATE / MICE GROUPS", "key": "mice", "color": "#34495e", "ota": False, "hurdle": 32.0},
    {"label": "4. GROUP TOUR & TRAVEL", "key": "tnt", "color": "#e67e22", "ota": False, "hurdle": 25.0}
]

wealth_results = {}

for seg in segments:
    st.markdown(f"<div class='card' style='border-left-color:{seg['color']}'>{seg['label']}</div>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        
        # ROW 1: ROOM COUNTS (SGL, DBL, TPL, QRPL)
        r1_cols = st.columns([1, 1, 1, 1, 1.5, 1.5])
        sgl = r1_cols[0].number_input("SGL", 0, key=f"sgl_{seg['key']}_{rk}")
        dbl = r1_cols[1].number_input("DBL", 0, key=f"dbl_{seg['key']}_{rk}")
        tpl = r1_cols[2].number_input("TPL", 0, key=f"tpl_{seg['key']}_{rk}")
        qrpl = r1_cols[3].number_input("QRPL", 0, key=f"qrp_{seg['key']}_{rk}")
        adr = r1_cols[4].number_input(f"Rate ({cur_sym})", value=75.0, key=f"adr_{seg['key']}_{rk}")
        h_floor = r1_cols[5].number_input("Hurdle Floor", value=seg['hurdle'], key=f"hrd_{seg['key']}_{rk}")
        
        # ROW 2: MEAL PLANS
        r2_cols = st.columns([0.6, 0.6, 0.6, 0.6, 0.6, 0.6, 1.2, 1.2])
        ro = r2_cols[0].number_input("RO", 0, key=f"ro_{seg['key']}_{rk}")
        bb = r2_cols[1].number_input("BB", 0, key=f"bb_{seg['key']}_{rk}")
        hb = r2_cols[2].number_input("HB", 0, key=f"hb_{seg['key']}_{rk}")
        fb = r2_cols[3].number_input("FB", 0, key=f"fb_{seg['key']}_{rk}")
        sai = r2_cols[4].number_input("SAI", 0, key=f"sai_{seg['key']}_{rk}")
        ai = r2_cols[5].number_input("AI", 0, key=f"ai_{seg['key']}_{rk}")
        
        # Calculation Execution
        comm = (ota_comm/100) if seg['ota'] else 0.0
        res = run_segment_yield(adr, {"RO":ro,"BB":bb,"HB":hb,"FB":fb,"SAI":sai,"AI":ai}, h_floor, comm)
        
        r2_cols[6].metric("Net Wealth", f"{cur_sym} {res['w']:,.2f}")
        r2_cols[7].markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']}</div>", unsafe_allow_html=True)
        
        wealth_results[seg['key']] = res['w']
        st.markdown("</div>", unsafe_allow_html=True)

# --- 6. STRATEGIC NOI SIMULATION (PILLAR 02) ---
st.divider()
st.markdown("### 📈 Strategic NOI Simulation (Pillar 02)")
net_a, net_b = wealth_results['fit'], wealth_results['ota']
improvement_val = (net_a - net_b) * sim_rooms * m_nights
improvement_pct = ((net_a - net_b) / net_b * 100) if net_b != 0 else 0

m1, m2, m3 = st.columns(3)
with m1: st.metric("Net Flow Gap (A-B)", f"{cur_sym} {net_a - net_b:,.2f}")
with m2: st.metric("Total NOI Gain", f"{cur_sym} {improvement_val:,.2f}")
with m3: st.metric("NOI % Improvement", f"{improvement_pct:.2f}%")

final_status = "ACCEPT: ACCRETIVE" if net_a > net_b else "REJECT: DILUTIVE"
st.markdown(f"""
<div class='noi-card'>
    <h4>Executive Verdict: {final_status}</h4>
    Shifting <b>{sim_rooms} rooms</b> for <b>{m_nights} nights</b> identifies a <b>{improvement_pct:.2f}%</b> 
    NOI improvement, adding <b>{cur_sym} {improvement_val:,.2f}</b> to the wealth-core.
</div>
""", unsafe_allow_html=True)

# --- 7. DEFENSIVE NAVIGATION ---
st.session_state["current_audit"] = {"yield": net_a, "hurdle": net_b, "status": final_status, "rooms": sim_rooms}
if st.button("🚀 Run Pillar 02: Strategic AI Audit"):
    if os.path.exists("pages/strategic_gem.py"):
        st.switch_page("pages/strategic_gem.py")
    else:
        st.error("Audit Page Missing.")
