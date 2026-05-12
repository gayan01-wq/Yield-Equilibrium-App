import streamlit as st
from datetime import date

# --- 1. SETTINGS & STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Displacement Analyzer")

st.markdown("""<style>
.block-container{padding-top:1rem!important; padding-bottom:0rem!important;}
.main-title { font-size: 2.2rem!important; font-weight: 900; color: #1e3799; text-align: center; text-transform: uppercase; margin-bottom: -5px; }
.card{padding:10px; border-radius:10px; margin-bottom:5px; border-left:10px solid; background:#ffffff; box-shadow: 0 2px 4px rgba(0,0,0,0.05)}
.pricing-row{background:#f8faff; padding:15px; border-radius:12px; border:1px solid #d1d9e6; margin-top:2px;}
.google-window{background:#e8f0fe; padding:15px; border-radius:12px; border:2px solid #4285f4; margin-bottom:15px; font-size:0.88rem; line-height:1.5;}
.status-indicator{padding:12px; border-radius:8px; text-align:center; font-weight:900; font-size:1.1rem; color:white; margin-top:10px; display:block;}
.reason-box{background:#fff9c4; border:1px solid #fbc02d; padding:10px; border-radius:8px; margin-top:8px; text-align:left; font-weight:500; color:#5f4300; font-size:0.8rem;}
.noi-badge{background:#1e3799; color:white; padding:8px 12px; border-radius:8px; font-weight:700; font-size:1rem; box-shadow: 0 2px 4px rgba(0,0,0,0.1);}
.theory-box { background-color: #f1f4f9; padding: 25px; border-radius: 15px; border: 1px solid #d1d9e6; margin-top: 35px; }
.pillar-header { color: #1e3799; font-weight: 800; font-size: 1rem; text-transform: uppercase; margin-bottom: 5px; display: block; }
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
    st.stop()

def clear_protocol_data():
    st.session_state["reset_key"] += 1
    for key in list(st.session_state.keys()):
        if key not in ["auth", "reset_key"]:
            del st.session_state[key]

# --- 3. SIDEBAR SETUP ---
rk = str(st.session_state["reset_key"])
with st.sidebar:
    st.markdown("### 🏨 Property Profile")
    h_name = st.text_input("Hotel Name", value="", placeholder="e.g. Wyndham Garden Salalah", key="h_nm_"+rk)
    h_cap = st.number_input("Total Capacity", min_value=1, value=237, step=1, key="cap_"+rk)
    city_search = st.text_input("📍 Market Location", value="", placeholder="e.g. Salalah", key="city_"+rk)
    
    st.divider()
    st.markdown("### 📅 Stay Period")
    d1 = st.date_input("Check-In", date.today(), key="d_in_"+rk)
    d2 = st.date_input("Check-Out", date.today() if (date.today() - date.today()).days > 0 else date.today(), key="d_out_"+rk)
    # LOS (Length of Stay) Calculation
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"Stay Duration: {m_nights} Night(s)")

    st.divider()
    st.markdown("### 🌍 Global Currency Suite")
    currencies = {"OMR (﷼)": "﷼", "AED (د.إ)": "د.إ", "SAR (﷼)": "﷼", "USD ($)": "$"}
    cur_selection = st.selectbox("Select Currency", list(currencies.keys()), key="c_sel_"+rk)
    cur_sym = currencies[cur_selection]

    st.divider()
    st.markdown("### 🏛️ Pillars Setup")
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx_v_"+rk)
    p01_fee = st.number_input(f"P01 Fee ({cur_sym})", value=6.00, step=0.1, key="p01_v_"+rk)

    # Sidebar Meal Plan Costs (PP - Per Person)
    st.markdown("### 🍽️ Meal Plan Cost (PP)")
    meal_costs = {
        "BF": st.number_input("BF Cost (PP)", min_value=0.0, value=2.00, step=0.5, key="bf_mc_"+rk),
        "LN": st.number_input("LN Cost (PP)", min_value=0.0, value=3.00, step=0.5, key="ln_mc_"+rk),
        "DN": st.number_input("DN Cost (PP)", min_value=0.0, value=5.00, step=0.5, key="dn_mc_"+rk),
        "SAI": st.number_input("SAI Cost (PP)", min_value=0.0, value=12.00, step=0.5, key="sai_mc_"+rk),
        "AI": st.number_input("AI Cost (PP)", min_value=0.0, value=15.00, step=0.5, key="ai_mc_"+rk)
    }

    if st.button("🗑️ Reset Protocol Data", use_container_width=True, type="primary"):
        clear_protocol_data()
        st.rerun()

# --- 4. CALCULATION ENGINE ---
def run_segment_yield(adr, meal_pax, base_hurdle, demand_type, is_group, total_rooms, comm_rate=0.0, mice=0.0, laundry=0.0, transport=0.0):
    # 1. Velocity Multiplier Logic
    velocity_map = {"Compression (Peak)": 1.25, "High Flow": 1.10, "Standard": 1.0, "Distressed": 0.85}
    v_mult = velocity_map.get(demand_type, 1.0)
    
    # 2. Dynamic Hurdle Logic
    hurdle_multiplier = {"Compression (Peak)": 2.5, "High Flow": 1.5, "Standard": 1.0, "Distressed": 0.7}
    dynamic_hurdle = base_hurdle * hurdle_multiplier.get(demand_type, 1.0)
    
    # 3. Net ADR (After Tax and Velocity)
    net_adr = (adr * v_mult) / tx_div
    
    # 4. Meal Logic (Pax Basis)
    # The user enters total pax receiving each meal type in the UI.
    # Cost = (Pax * Cost_PP) / Total Rooms (to get cost per room)
    bb, hb, fb, sai, ai = meal_pax.get("BB", 0), meal_pax.get("HB", 0), meal_pax.get("FB", 0), meal_pax.get("SAI", 0), meal_pax.get("AI", 0)
    
    total_meal_outflow = (
        (bb * meal_costs["BF"]) + 
        (hb * (meal_costs["BF"] + meal_costs["DN"])) + 
        (fb * (meal_costs["BF"] + meal_costs["LN"] + meal_costs["DN"])) + 
        (sai * meal_costs["SAI"]) + 
        (ai * meal_costs["AI"])
    )
    
    # Normalize meal cost to "per room" to strip it from ADR
    meal_cost_per_room = total_meal_outflow / max(total_rooms, 1)
    
    # 5. Ancillary / Group Rev (MICE/Transport)
    divisor = max(total_rooms, 1)
    group_rev_per_room = (mice / tx_div) + ((transport / tx_div) / divisor) if is_group else 0
    
    # 6. Unit Wealth (Net NOI per room/night)
    # Formula: [Net ADR + Group Rev] - [Meals + Commission + P01 Fee + Laundry]
    comm_outflow = net_adr * (comm_rate/100)
    unit_w = (net_adr + group_rev_per_room) - (meal_cost_per_room + comm_outflow + p01_fee + laundry)
    
    # 7. Segment Over-performance / Status
    if unit_w < dynamic_hurdle: 
        stt, clr, rsn = "REJECT: DILUTIVE", "#e74c3c", f"Displaced by {demand_type} Hurdle."
    elif unit_w < (dynamic_hurdle + 5.0): 
        stt, clr, rsn = "REVIEW: MARGINAL", "#f39c12", "At equilibrium window."
    else: 
        stt, clr, rsn = "ACCEPT: OPTIMIZED", "#27ae60", "Wealth targets achieved."
        
    # Basis display logic
    if ai > 0: mp_basis = "AI"
    elif sai > 0: mp_basis = "SAI"
    elif fb > 0: mp_basis = "FB"
    elif hb > 0: mp_basis = "HB"
    elif bb > 0: mp_basis = "BB"
    else: mp_basis = "RO"

    # 8. Total NOI (Total Wealth across LOS and Total Rooms)
    total_noi = unit_w * total_rooms * m_nights
    
    return {"w": unit_w, "st": stt, "cl": clr, "rsn": rsn, "vm": v_mult, "dh": dynamic_hurdle, "noi": total_noi, "mp": mp_basis}

# --- 5. UI SEGMENTS ---
display_title = h_name if h_name else "New Property Analysis"
st.markdown(f"<h1 class='main-title'>{display_title.upper()}</h1>", unsafe_allow_html=True)

segments = [
    {"label": "1. DIRECT / FIT", "key": "fit", "color": "#3498db", "ota": False, "hurdle": 45.0, "group": False},
    {"label": "2. OTA CHANNELS", "key": "ota", "color": "#2ecc71", "ota": True, "hurdle": 35.0, "group": False},
    {"label": "3. CORPORATE / MICE GROUPS", "key": "mice", "color": "#34495e", "ota": False, "hurdle": 32.0, "group": True}
]

wealth_results = {}

for seg in segments:
    if st.checkbox(f"Activate {seg['label']}", value=True, key=f"act_{seg['key']}_{rk}"):
        st.markdown(f"<div class='card' style='border-left-color:{seg['color']}'>{seg['label']}</div>", unsafe_allow_html=True)
        with st.container():
            st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
            
            # Row 1: Inputs
            r1 = st.columns([1, 0.5, 0.5, 0.5, 0.5, 1.2, 1.2])
            g_rate = r1[0].number_input("Gross Rate", value=75.0, step=1.0, key=f"adr_{seg['key']}_{rk}")
            sgl = r1[1].number_input("SGL", 0, key=f"s_{seg['key']}_{rk}")
            dbl = r1[2].number_input("DBL", 0, key=f"d_{seg['key']}_{rk}")
            tpl = r1[3].number_input("TPL", 0, key=f"t_{seg['key']}_{rk}")
            qrpl = r1[4].number_input("QRPL", 0, key=f"q_{seg['key']}_{rk}")
            total_rooms = sgl + dbl + tpl + qrpl
            demand_sel = r1[5].selectbox("Market Demand", ["Compression (Peak)", "High Flow", "Standard", "Distressed"], key=f"dm_{seg['key']}_{rk}")
            h_base = r1[6].number_input("Base Hurdle", value=seg['hurdle'], key=f"hrd_{seg['key']}_{rk}")

            # Row 2: Pax Meal Plan Inputs
            r2 = st.columns([0.6, 0.6, 0.6, 0.6, 0.6, 1.1, 1.1, 1.1])
            bb_pax = r2[0].number_input("BB Pax", 0, key=f"bb_p_{seg['key']}_{rk}")
            hb_pax = r2[1].number_input("HB Pax", 0, key=f"hb_p_{seg['key']}_{rk}")
            fb_pax = r2[2].number_input("FB Pax", 0, key=f"fb_p_{seg['key']}_{rk}")
            sai_pax = r2[3].number_input("SAI Pax", 0, key=f"sai_p_{seg['key']}_{rk}")
            ai_pax = r2[4].number_input("AI Pax", 0, key=f"ai_p_{seg['key']}_{rk}")
            
            mice_rev = r2[5].number_input("MICE/Event", 0.0, key=f"m_{seg['key']}_{rk}") if seg['group'] else 0.0
            laundry = r2[6].number_input("Laundry", 0.0, key=f"l_{seg['key']}_{rk}")
            transport = r2[7].number_input("Transport", 0.0, key=f"tr_{seg['key']}_{rk}")

            # Calculations
            res = run_segment_yield(g_rate, {"BB":bb_pax,"HB":hb_pax,"FB":fb_pax,"SAI":sai_pax,"AI":ai_pax}, h_base, demand_sel, seg['group'], total_rooms, laundry=laundry, mice=mice_rev, transport=transport)
            
            # Metrics Display
            v_cols = st.columns([1, 1.5, 1])
            v_cols[0].metric("Net Wealth (Unit)", f"{cur_sym} {res['w']:,.2f}", delta=f"{res['vm']}x Velocity")
            v_cols[1].markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']} ({res['mp']})</div>", unsafe_allow_html=True)
            v_cols[2].markdown(f"<div style='text-align:right;'><span class='noi-badge'>Total NOI: {cur_sym} {res['noi']:,.2f}</span></div>", unsafe_allow_html=True)
            
            st.markdown(f"<div class='reason-box'>💡 <b>Strategic Reasoning:</b> {res['rsn']} | <b>Stay Nights:</b> {m_nights} | <b>Effective Hurdle:</b> {cur_sym}{res['dh']:,.2f}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
