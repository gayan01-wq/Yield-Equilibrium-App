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

# --- 2. AUTHENTICATION & SESSION ISOLATION ---
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

# --- 3. SIDEBAR (INDIVIDUAL MEAL COSTS) ---
rk = str(st.session_state["reset_key"])
with st.sidebar:
    st.markdown("### 🏨 Property Profile")
    h_name = st.text_input("Hotel Name", value="", placeholder="e.g. Wyndham Garden Salalah", key="h_nm_"+rk)
    h_cap = st.number_input("Total Capacity", min_value=1, value=237, step=1, key="cap_"+rk)
    city_search = st.text_input("📍 Market Location", value="", placeholder="e.g. Salalah", key="city_"+rk)
    
    st.divider()
    st.markdown("### 📅 Stay Period")
    d1 = st.date_input("Check-In", date.today(), key="d_in_"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d_out_"+rk)
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

    # UPDATED SIDEBAR: Individual Meal Costs (PP)
    st.markdown("### 🍽️ Meal Plan Cost (PP)")
    c_bf = st.number_input("Breakfast Cost (PP)", min_value=0.0, value=2.00, step=0.5, key="bf_mc_"+rk)
    c_ln = st.number_input("Lunch Cost (PP)", min_value=0.0, value=3.00, step=0.5, key="ln_mc_"+rk)
    c_dn = st.number_input("Dinner Cost (PP)", min_value=0.0, value=5.00, step=0.5, key="dn_mc_"+rk)
    c_sai = st.number_input("SAI Cost (PP)", min_value=0.0, value=12.00, step=0.5, key="sai_mc_"+rk)
    c_ai = st.number_input("AI Cost (PP)", min_value=0.0, value=15.00, step=0.5, key="ai_mc_"+rk)

# --- 4. CALCULATION ENGINE ---
def run_segment_yield(adr, room_counts, base_hurdle, demand_type, is_group, total_rooms, comm_rate=0.0, mice=0.0, laundry=0.0, transport=0.0):
    velocity_map = {"Compression (Peak)": 1.25, "High Flow": 1.10, "Standard": 1.0, "Distressed": 0.85}
    v_mult = velocity_map.get(demand_type, 1.0)
    
    hurdle_multiplier = {"Compression (Peak)": 2.5, "High Flow": 1.5, "Standard": 1.0, "Distressed": 0.7}
    dynamic_hurdle = base_hurdle * hurdle_multiplier.get(demand_type, 1.0)
    
    net_adr = (adr * v_mult) / tx_div
    
    # MEAL LOGIC: Calculate total cost based on the sum of plan components
    cost_bb = room_counts['BB'] * c_bf
    cost_hb = room_counts['HB'] * (c_bf + c_dn)
    cost_fb = room_counts['FB'] * (c_bf + c_ln + c_dn)
    cost_sai = room_counts['SAI'] * c_sai
    cost_ai = room_counts['AI'] * c_ai
    
    total_meal_outflow = cost_bb + cost_hb + cost_fb + cost_sai + cost_ai
    divisor = max(total_rooms, 1)
    meal_per_room = total_meal_outflow / divisor
    
    group_rev_per_room = (mice / tx_div) + ((transport / tx_div) / divisor) if is_group else 0
    comm_outflow = net_adr * (comm_rate/100)
    
    # Unit Wealth (Pillar 01)
    unit_w = (net_adr + group_rev_per_room) - (meal_per_room + comm_outflow + p01_fee + laundry)
    
    # Performance Status
    if unit_w < dynamic_hurdle: stt, clr, rsn = "REJECT: DILUTIVE", "#e74c3c", f"Below {demand_type} Hurdle."
    elif unit_w < (dynamic_hurdle + 5.0): stt, clr, rsn = "REVIEW: MARGINAL", "#f39c12", "Equilibrium threshold."
    else: stt, clr, rsn = "ACCEPT: OPTIMIZED", "#27ae60", "Target Achieved."
    
    # Determine display basis
    mp_basis = "RO"
    for plan in ["AI", "SAI", "FB", "HB", "BB"]:
        if room_counts.get(plan, 0) > 0:
            mp_basis = plan
            break

    total_noi = unit_w * total_rooms * m_nights
    return {"w": unit_w, "st": stt, "cl": clr, "rsn": rsn, "vm": v_mult, "dh": dynamic_hurdle, "noi": total_noi, "mp": mp_basis}

# --- 5. MARKET INTEL DATA ---
intel_db = {
    "salalah": {"ev": "Khareef Festival Season", "fl": "OmanAir/SalamAir Peak", "news": "Monsoon Tourism Surge expected.", "demand": "Compression"},
    "muscat": {"ev": "Business Summit", "fl": "International Hub Stable", "news": "MICE demand up 15%.", "demand": "High Flow"}
}
active_intel = intel_db.get(city_search.lower(), {"ev": "Market Rotation", "fl": "Standard Flights", "news": "Standard flow stable.", "demand": "Standard"})

# --- 6. TOP DASHBOARD ---
display_title = h_name if h_name else "New Property Analysis"
st.markdown(f"<h1 class='main-title'>{display_title.upper()}</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; color:#4b6584; font-weight:700; margin-bottom:20px;'>Yield Equilibrium Strategic Intelligence Engine</div>", unsafe_allow_html=True)

st.markdown(f"""
<div class='google-window'>
    <b>🌐 Market Intelligence: {city_search if city_search else 'Location Pending'} | {date.today().strftime('%B %Y')}</b><br>
    • <b>Aviation Situation:</b> {active_intel['fl']} | <b>Special Events:</b> {active_intel['ev']}<br>
    • <b>Special News Feed:</b> {active_intel['news']} | <b>Market Pulse:</b> {active_intel['demand']} Logic Applied.
</div>
""", unsafe_allow_html=True)

# --- 7. SEGMENT AUDITS ---
segments = [
    {"label": "1. DIRECT / FIT", "key": "fit", "color": "#3498db", "hurdle": 45.0, "group": False},
    {"label": "2. OTA CHANNELS", "key": "ota", "color": "#2ecc71", "hurdle": 35.0, "group": False},
    {"label": "3. CORPORATE / MICE GROUPS", "key": "mice", "color": "#34495e", "hurdle": 32.0, "group": True}
]

wealth_results = {}

for seg in segments:
    if st.checkbox(f"Activate {seg['label']}", value=True, key=f"act_{seg['key']}_{rk}"):
        st.markdown(f"<div class='card' style='border-left-color:{seg['color']}'>{seg['label']}</div>", unsafe_allow_html=True)
        with st.container():
            st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
            
            # Row 1: Core Pricing & Demand
            r1 = st.columns([1, 0.5, 0.5, 0.5, 0.5, 1.2, 1.2])
            g_rate = r1[0].number_input("Gross Rate", value=75.0, step=1.0, key=f"adr_{seg['key']}_{rk}")
            sgl, dbl, tpl, qrpl = r1[1].number_input("SGL", 0, key=f"s_{seg['key']}_{rk}"), r1[2].number_input("DBL", 0, key=f"d_{seg['key']}_{rk}"), r1[3].number_input("TPL", 0, key=f"t_{seg['key']}_{rk}"), r1[4].number_input("QRPL", 0, key=f"q_{seg['key']}_{rk}")
            total_rooms = sgl + dbl + tpl + qrpl
            demand_sel = r1[5].selectbox("Market Demand", ["Compression (Peak)", "High Flow", "Standard", "Distressed"], key=f"dm_{seg['key']}_{rk}")
            h_base = r1[6].number_input("Base Hurdle", value=seg['hurdle'], key=f"hrd_{seg['key']}_{rk}")

            # Row 2: Meal Selections (Rooms on each plan)
            r2 = st.columns([0.6, 0.6, 0.6, 0.6, 0.6, 1.1, 1.1, 1.1])
            bb_r = r2[0].number_input("BB", 0, key=f"bb_r_{seg['key']}_{rk}")
            hb_r = r2[1].number_input("HB", 0, key=f"hb_r_{seg['key']}_{rk}")
            fb_r = r2[2].number_input("FB", 0, key=f"fb_r_{seg['key']}_{rk}")
            sai_r = r2[3].number_input("SAI", 0, key=f"sai_r_{seg['key']}_{rk}")
            ai_r = r2[4].number_input("AI", 0, key=f"ai_r_{seg['key']}_{rk}")
            
            mice_rev = r2[5].number_input("MICE Rev", 0.0, key=f"m_{seg['key']}_{rk}") if seg['group'] else 0.0
            laundry = r2[6].number_input("Laundry", 0.0, key=f"l_{seg['key']}_{rk}")
            transport = r2[7].number_input("Transport", 0.0, key=f"tr_{seg['key']}_{rk}")

            # Calculate using room counts and sidebar individual costs
            meal_dict = {"BB": bb_r, "HB": hb_r, "FB": fb_r, "SAI": sai_r, "AI": ai_r}
            res = run_segment_yield(g_rate, meal_dict, h_base, demand_sel, seg['group'], total_rooms, laundry=laundry, mice=mice_rev, transport=transport)
            
            # Results Display
            v_cols = st.columns([1, 1.5, 1])
            v_cols[0].metric("Net Wealth (Unit)", f"{cur_sym} {res['w']:,.2f}", delta=f"{res['vm']}x Velocity")
            v_cols[1].markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']} ({res['mp']})</div>", unsafe_allow_html=True)
            v_cols[2].markdown(f"<div style='text-align:right;'><span class='noi-badge'>Total NOI: {cur_sym} {res['noi']:,.2f}</span></div>", unsafe_allow_html=True)
            
            st.markdown(f"<div class='reason-box'>💡 <b>Strategic Reasoning:</b> {res['rsn']} | <b>Basis:</b> {res['mp']} | <b>Effective Hurdle:</b> {cur_sym}{res['dh']:,.2f}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
