import streamlit as st
from datetime import date
import pandas as pd

# --- 1. SETTINGS & STYLING ---
st.set_page_config(layout="wide", page_title="Universal Yield Equilibrium Engine")

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
.pillar-header { color: #1e3799; font-weight: 800; font-size: 1.1rem; text-transform: uppercase; margin-bottom: 8px; display: block; border-bottom: 2px solid #1e3799; padding-bottom: 4px;}
.alert-box { background-color: #ffeded; border: 1px solid #ff4b4b; color: #ff4b4b; padding: 10px; border-radius: 8px; font-weight: bold; margin-bottom: 10px;}
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login"):
        if st.text_input("Access Key", type="password") == "Gayan2026":
            if st.form_submit_button("Unlock"):
                st.session_state["auth"] = True
                st.rerun()
    st.stop()

# --- 3. SIDEBAR (UNIVERSAL SETUP) ---
with st.sidebar:
    st.markdown("### 🏨 Hotel Profile")
    h_name = st.text_input("Hotel Name", "Wyndham Garden Salalah")
    h_cap = st.number_input("Total Room Inventory", min_value=1, value=237)
    city_search = st.text_input("📍 Market Location", "Salalah")
    
    st.divider()
    st.markdown("### 📅 Stay & LOS Logic")
    d1 = st.date_input("Check-In", date.today())
    d2 = st.date_input("Check-Out", date(2026, 5, 12))
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    los_type = "Long Stay (LOS High)" if m_nights >= 5 else "Short Stay (LOS Low)"
    st.info(f"Stay: {m_nights} Nights | {los_type}")

    st.divider()
    curr_map = {"OMR (﷼)": "﷼", "AED (د.إ)": "د.إ", "SAR (﷼)": "﷼", "USD ($)": "$", "EUR (€)": "€", "LKR (රු)": "රු"}
    cur_sym = curr_map[st.selectbox("Select Currency", list(curr_map.keys()))]

    # Flexible Tax Divisor Formula
    st.markdown("### 🏛️ Pillars Setup")
    tax_input = st.text_input("Tax Divisor Formula", value="1.2327", help="Enter number or formula like 1.2327 or 1.21*1.05")
    try:
        current_tax_divisor = float(eval(tax_input))
    except:
        current_tax_divisor = 1.0
        st.error("Invalid Tax Formula")

    p01_fee = st.number_input(f"P01 Fixed Fee ({cur_sym})", min_value=0.0, value=6.0)

    st.markdown("### 🍽️ Standard Meal Costs (PP)")
    m_costs = {
        "BF": st.number_input("Breakfast", min_value=0.0, value=2.0),
        "LN": st.number_input("Lunch", min_value=0.0, value=0.0),
        "DN": st.number_input("Dinner", min_value=0.0, value=0.0),
        "SAI": st.number_input("SAI Addon", min_value=0.0, value=0.0),
        "AI": st.number_input("AI Addon", min_value=0.0, value=0.0)
    }

# --- 4. ENGINE LOGIC ---
def run_yield_engine(adr, meal_qty, hurdle, demand, is_group, rooms, comm=0.0, mice=0.0, laund=0.0, trans=0.0):
    # Velocity Multiplier
    v_map = {"Compression (Peak)": 1.25, "High Flow": 1.15, "Standard": 1.0, "Distressed": 0.85}
    v_mult = v_map.get(demand, 1.0)
    
    # Meal Basis Mapping
    bf, ln, dn, sai, ai = meal_qty.get("BF",0), meal_qty.get("LN",0), meal_qty.get("DN",0), meal_qty.get("SAI",0), meal_qty.get("AI",0)
    if ai > 0: mp = "AI"
    elif sai > 0: mp = "SAI"
    elif bf > 0 and ln > 0 and dn > 0: mp = "FB"
    elif bf > 0 and dn > 0: mp = "HB"
    elif bf > 0: mp = "BB"
    else: mp = "RO"

    # Net Calculation
    net_adr = (adr * v_mult) / current_tax_divisor
    comm_cost = net_adr * (comm / 100)
    meal_tot = sum(qty * m_costs.get(p, 0) for p, qty in meal_qty.items())
    
    # Volume Logic
    vol_divisor = max(rooms, 10) if is_group else max(rooms, 1)
    grp_rev = (mice / current_tax_divisor) + ((trans / current_tax_divisor) / vol_divisor) if is_group else 0
    
    unit_wealth = (net_adr + grp_rev - meal_tot - comm_cost) - p01_fee - laund
    
    # Dynamic Hurdle
    h_map = {"Compression (Peak)": 2.5, "High Flow": 1.7, "Standard": 1.0, "Distressed": 0.65}
    dyn_h = hurdle * h_map.get(demand, 1.0)
    
    # LOS Strategic Adjustment
    if m_nights >= 5 and unit_wealth >= (dyn_h * 0.9): status, color = "ACCEPT: STRATEGIC LONGSTAY", "#2980b9"
    elif unit_wealth >= dyn_h: status, color = "ACCEPT: OPTIMIZED", "#27ae60"
    else: status, color = "REJECT: DILUTIVE", "#e74c3c"
    
    return {"w": unit_wealth, "st": status, "cl": color, "mp": mp, "noi": unit_wealth * vol_divisor * m_nights, "dh": dyn_h, "vm": v_mult, "rooms": rooms}

# --- 5. DASHBOARD ---
st.markdown(f"<h1 class='main-title'>{h_name.upper()}</h1>", unsafe_allow_html=True)

segments = [
    {"label": "1. DIRECT / FIT", "key": "fit", "color": "#3498db", "h": 45.0, "grp": False, "ota": False},
    {"label": "2. OTA CHANNELS", "key": "ota", "color": "#2ecc71", "h": 35.0, "grp": False, "ota": True},
    {"label": "3. CORPORATE / MICE", "key": "mice", "color": "#34495e", "h": 32.0, "grp": True, "ota": False},
    {"label": "4. GROUP TOUR & TRAVEL", "key": "tnt", "color": "#e67e22", "h": 12.0, "grp": True, "ota": False}
]

active_rooms = 0
results_store = []

for s in segments:
    if st.checkbox(f"Enable {s['label']}", value=True, key=f"chk_{s['key']}"):
        st.markdown(f"<div class='card' style='border-left-color:{s['color']}'>{s['label']}</div>", unsafe_allow_html=True)
        with st.container():
            st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
            r1 = st.columns([1, 1.2, 0.8, 1, 1])
            g_rate = r1[0].number_input("Gross Rate", min_value=0.0, value=75.0, key=f"adr_{s['key']}")
            
            # Volume/Room Inputs
            c_r = st.columns(4)
            s_r = r1[1].number_input("Rooms (SGL/DBL/TPL)", min_value=1, value=1, key=f"rms_{s['key']}")
            dem = r1[2].selectbox("Demand", ["Standard", "High Flow", "Compression (Peak)", "Distressed"], key=f"dm_{s['key']}")
            hrd = r1[3].number_input("Base Hurdle", min_value=0.0, value=s['h'], key=f"hr_{s['key']}")
            
            # OTA Commission
            comm_val = 0.0
            if s['ota']:
                comm_val = r1[4].slider("OTA Commission %", 0, 30, 15, key=f"ota_comm_{s['key']}")
            else:
                r1[4].info("0% Comm Applied")

            r2 = st.columns([0.6, 0.6, 0.6, 0.6, 0.6, 1.1, 1.1, 1.1])
            v_bb = r2[0].number_input("BB", 0, key=f"bb_{s['k']}")
            v_ln = r2[1].number_input("LN", 0, key=f"ln_{s['k']}")
            v_dn = r2[2].number_input("DN", 0, key=f"dn_{s['k']}")
            v_sai = r2[3].number_input("SAI", 0, key=f"sai_{s['k']}")
            v_ai = r2[4].number_input("AI", 0, key=f"ai_{s['k']}")
            
            m_r = r2[5].number_input("Group Rev", min_value=0.0, key=f"mice_{s['k']}") if s['grp'] else 0.0
            l_c = r2[6].number_input("Laundry", min_value=0.0, key=f"lnd_{s['k']}") if s['grp'] else 0.0
            t_c = r2[7].number_input("Transport", min_value=0.0, key=f"tra_{s['k']}") if s['grp'] else 0.0

            res = run_yield_engine(g_rate, {"BF":v_bb, "LN":v_ln, "DN":v_dn, "SAI":v_sai, "AI":v_ai}, hrd, dem, s['grp'], s_r, comm_val, m_r, l_c, t_c)
            active_rooms += s_r
            
            v = st.columns([1, 1.5, 1])
            v[0].metric("Net Wealth (Unit)", f"{cur_sym} {res['w']:,.2f}", delta=f"{res['vm']}x Velocity")
            v[1].markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']} ({res['mp']})</div>", unsafe_allow_html=True)
            v[2].markdown(f"<div style='text-align:right;'><span class='noi-badge'>Segment NOI: {cur_sym} {res['noi']:,.2f}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='reason-box'>LOS Strategy: {los_type} | Effective Dynamic Hurdle: {cur_sym} {res['dh']:.2f}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# --- 6. OCCUPANCY ALERT SYSTEM ---
occ_perc = (active_rooms / h_cap) * 100
if occ_perc >= 50:
    st.markdown(f"""<div class='alert-box'>⚠️ HIGH OCCUPANCY WARNING: Simulation represents {occ_perc:.1f}% of total inventory. 
    Yield displacement is now critical. Increase hurdles by 20% to protect remaining 50% capacity.</div>""", unsafe_allow_html=True)

# --- 7. DEEP PILLAR DESCRIPTIONS ---
st.divider()
st.markdown("<div class='theory-box'><h2 style='color:#1e3799; text-align:center;'>THE YIELD EQUILIBRIUM STRATEGIC FRAMEWORK</h2>", unsafe_allow_html=True)
p1, p2, p3 = st.columns(3)

with p1:
    st.markdown("<span class='pillar-header'>🏛️ Pillar 01: Internal Wealth Stripping</span>", unsafe_allow_html=True)
    st.markdown(f"""
    **The Objective:** To isolate the "Pure Profit" before it reaches the bottom line. 
    * **Formula Logic:** $Gross - Taxes - Commission - Incremental Costs (Meal/Laundry) - Fixed Overheads$.
    * **Strategic Use:** Ensures that high-volume segments (like Groups) aren't actually costing the hotel money when the "hidden" costs of commissions and food are stripped away.
    """)

with p2:
    st.markdown("<span class='pillar-header'>⚖️ Pillar 02: Dynamic Hurdle Equilibrium</span>", unsafe_allow_html=True)
    st.markdown(f"""
    **The Objective:** To protect inventory for high-value last-minute bookings.
    * **Formula Logic:** $Base Hurdle \\times Market Demand Multiplier$.
    * **Strategic Use:** During "Compression" (high demand), this pillar prevents the hotel from filling up too early with low-rated business. It acts as a gatekeeper that automatically raises the price of entry as the market heats up.
    """)

with p3:
    st.markdown("<span class='pillar-header'>🌐 Pillar 03: External Velocity</span>", unsafe_allow_html=True)
    st.markdown(f"""
    **The Objective:** To align hotel pricing with the speed of market pickup.
    * **Formula Logic:** Adjusting the "Net Wealth" based on the $Velocity Multiplier$.
    * **Strategic Use:** If the city is sold out (Peak), the value of your last remaining rooms is exponentially higher. This pillar forces the engine to weigh "Wealth" more heavily when the market is moving fast.
    """)
st.markdown("</div>", unsafe_allow_html=True)
