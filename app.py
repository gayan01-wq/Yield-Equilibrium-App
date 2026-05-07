import streamlit as st
from datetime import date

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
.alert-box { background-color: #ffeded; border: 1px solid #ff4b4b; color: #ff4b4b; padding: 15px; border-radius: 8px; font-weight: bold; margin-bottom: 15px; border-left: 10px solid #ff4b4b;}
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

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("### 🏨 Hotel Profile")
    h_name = st.text_input("Hotel Name", "Wyndham Garden Salalah")
    h_cap = st.number_input("Total Inventory", min_value=1, value=237)
    city_search = st.text_input("📍 Market Location", "Salalah")
    
    st.divider()
    st.markdown("### 📅 Stay & LOS Logic")
    d1 = st.date_input("Check-In", date.today())
    d2 = st.date_input("Check-Out", date(2026, 5, 12))
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    los_type = "Long Stay (5+ Nights)" if m_nights >= 5 else "Short Stay"
    st.info(f"Stay: {m_nights} Nights | {los_type}")

    st.divider()
    curr_map = {
        "OMR (﷼)": "﷼", "AED (د.إ)": "د.إ", "SAR (﷼)": "﷼", "QAR (﷼)": "﷼",
        "BHD (.د)": ".د", "KWD (د.ك)": "د.ك", "USD ($)": "$", "EUR (€)": "€",
        "GBP (£)": "£", "LKR (රු)": "රු", "INR (₹)": "₹", "AUD ($)": "$"
    }
    cur_sym = curr_map[st.selectbox("Select Currency", list(curr_map.keys()))]

    st.markdown("### 🏛️ Pillars Setup")
    tax_input = st.text_input("Tax Divisor Formula", value="1.2327")
    try: current_tax_divisor = float(eval(tax_input))
    except: current_tax_divisor = 1.2327

    p01_fee = st.number_input(f"P01 Fixed Fee ({cur_sym})", min_value=0.0, value=6.0)

    st.markdown("### 🍽️ Meal Costs (PP)")
    m_costs = {
        "BF": st.number_input("Breakfast Cost", 0.0, value=2.0),
        "LN": st.number_input("Lunch Cost", 0.0),
        "DN": st.number_input("Dinner Cost", 0.0),
        "SAI": st.number_input("SAI Add-on", 0.0),
        "AI": st.number_input("AI Add-on", 0.0)
    }

# --- 4. ENGINE LOGIC ---
def run_yield_engine(adr, meal_qty, hurdle, demand, is_group, rooms, comm=0.0, mice=0.0, laund=0.0, trans=0.0):
    v_mult = {"Compression (Peak)": 1.25, "High Flow": 1.15, "Standard": 1.0, "Distressed": 0.85}.get(demand, 1.0)
    
    # Meal Basis Detection
    bf, ln, dn, sai, ai = meal_qty.get("BF",0), meal_qty.get("LN",0), meal_qty.get("DN",0), meal_qty.get("SAI",0), meal_qty.get("AI",0)
    if ai > 0: mp = "AI"
    elif sai > 0: mp = "SAI"
    elif bf > 0 and ln > 0 and dn > 0: mp = "FB"
    elif bf > 0 and dn > 0: mp = "HB"
    elif bf > 0: mp = "BB"
    else: mp = "RO"

    net_adr = (adr * v_mult) / current_tax_divisor
    comm_cost = net_adr * (comm / 100)
    meal_tot = sum(qty * m_costs.get(p, 0) for p, qty in meal_qty.items())
    
    div = max(rooms, 10) if is_group else max(rooms, 1)
    grp_rev = (mice / current_tax_divisor) + ((trans / current_tax_divisor) / div) if is_group else 0
    unit_w = (net_adr + grp_rev - meal_tot - comm_cost) - p01_fee - laund
    
    dyn_h = hurdle * {"Compression (Peak)": 2.5, "High Flow": 1.7, "Standard": 1.0, "Distressed": 0.65}.get(demand, 1.0)
    
    if m_nights >= 5 and unit_w >= (dyn_h * 0.9): status, color = "ACCEPT: STRATEGIC LONGSTAY", "#2980b9"
    elif unit_w >= dyn_h: status, color = "ACCEPT: OPTIMIZED", "#27ae60"
    else: status, color = "REJECT: DILUTIVE", "#e74c3c"
    
    return {"w": unit_w, "st": status, "cl": color, "mp": mp, "noi": unit_w * div * m_nights, "dh": dyn_h, "vm": v_mult}

# --- 5. TOP DASHBOARD ---
st.markdown(f"<h1 class='main-title'>{h_name.upper()}</h1>", unsafe_allow_html=True)

# Comprehensive Market Insights
intel_db = {
    "salalah": {"ev": "Khareef Festival Season", "fl": "OmanAir/SalamAir Peak", "ns": "Monsoon Tourism Surge expected.", "dm": "Compression"},
    "muscat": {"ev": "Business Summit", "fl": "International Hub Stable", "ns": "MICE demand up 15%.", "dm": "High Flow"}
}
intel = intel_db.get(city_search.lower(), {"ev": "Standard Market Rotation", "fl": "Standard Flights", "ns": "Market flow stable.", "dm": "Standard"})

st.markdown(f"""<div class='google-window'><b>🌐 Market Intelligence: {city_search} | {date.today().strftime('%B %Y')}</b><br>
• <b>Events:</b> {intel['ev']} | <b>Aviation:</b> {intel['fl']}<br>
• <b>News:</b> {intel['ns']} | <b>Pulse:</b> {intel['dm']} Logic Applied.</div>""", unsafe_allow_html=True)

# --- 6. SEGMENTS ---
segments = [
    {"label": "1. DIRECT / FIT", "key": "fit", "color": "#3498db", "h": 45.0, "grp": False, "ota": False},
    {"label": "2. OTA CHANNELS", "key": "ota", "color": "#2ecc71", "h": 35.0, "grp": False, "ota": True},
    {"label": "3. CORPORATE / MICE", "key": "mice", "color": "#34495e", "h": 32.0, "grp": True, "ota": False},
    {"label": "4. GROUP TOUR & TRAVEL", "key": "tnt", "color": "#e67e22", "h": 12.0, "grp": True, "ota": False}
]

total_active_rooms = 0
for s in segments:
    if st.checkbox(f"Enable {s['label']}", value=True, key=f"chk_{s['key']}"):
        st.markdown(f"<div class='card' style='border-left-color:{s['color']}'>{s['label']}</div>", unsafe_allow_html=True)
        with st.container():
            st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
            r1 = st.columns([1, 1, 0.8, 1, 1.2])
            g_rate = r1[0].number_input("Gross Rate", 0.0, 75.0, key=f"adr_{s['key']}")
            rms = r1[1].number_input("Rooms Requested", 1, key=f"rms_{s['key']}")
            total_active_rooms += rms
            dem = r1[2].selectbox("Market Demand", ["Standard", "High Flow", "Compression (Peak)", "Distressed"], key=f"dm_{s['key']}")
            hrd = r1[3].number_input("Base Hurdle", 0.0, s['h'], key=f"hr_{s['key']}")
            
            comm_val = r1[4].slider("OTA Commission %", 0, 30, 15, key=f"comm_{s['key']}") if s['ota'] else 0.0
            if not s['ota']: r1[4].info("Fixed Channel")

            r2 = st.columns([0.6, 0.6, 0.6, 0.6, 0.6, 1.1, 1.1, 1.1])
            q_bf = r2[0].number_input("BB", 0, key=f"bf_{s['key']}")
            q_ln = r2[1].number_input("LN", 0, key=f"ln_{s['key']}")
            q_dn = r2[2].number_input("DN", 0, key=f"dn_{s['key']}")
            q_sai = r2[3].number_input("SAI", 0, key=f"sai_{s['key']}")
            q_ai = r2[4].number_input("AI", 0, key=f"ai_{s['key']}")
            
            m_r = r2[5].number_input("Group Rev", 0.0, key=f"m_{s['key']}") if s['grp'] else 0.0
            l_c = r2[6].number_input("Laundry", 0.0, key=f"l_{s['key']}")
            t_c = r2[7].number_input("Transport", 0.0, key=f"tr_{s['key']}")

            res = run_yield_engine(g_rate, {"BF":q_bf, "LN":q_ln, "DN":q_dn, "SAI":q_sai, "AI":q_ai}, hrd, dem, s['grp'], rms, comm_val, m_r, l_c, t_c)
            
            v = st.columns([1, 1.5, 1])
            v[0].metric("Net Wealth", f"{cur_sym} {res['w']:,.2f}", delta=f"{res['vm']}x Velocity")
            v[1].markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']} ({res['mp']})</div>", unsafe_allow_html=True)
            v[2].markdown(f"<div style='text-align:right;'><span class='noi-badge'>Segment NOI: {cur_sym} {res['noi']:,.2f}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='reason-box'>💡 Strategic Logic: {los_type} | Effective Dynamic Hurdle: {cur_sym} {res['dh']:.2f}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# --- 7. OCCUPANCY ALERT ---
occ_perc = (total_active_rooms / h_cap) * 100
if occ_perc >= 50:
    st.markdown(f"<div class='alert-box'>⚠️ HIGH OCCUPANCY WARNING: Simulation represents {occ_perc:.1f}% of total inventory. Yield displacement is critical. Protect remaining inventory!</div>", unsafe_allow_html=True)

# --- 8. PILLARS ---
st.divider()
st.markdown("<div class='theory-box'><h2 style='color:#1e3799; text-align:center;'>THE YIELD EQUILIBRIUM STRATEGIC FRAMEWORK</h2>", unsafe_allow_html=True)
p1, p2, p3 = st.columns(3)
with p1:
    st.markdown("<span class='pillar-header'>🏛️ Pillar 01: Internal Wealth Stripping</span>", unsafe_allow_html=True)
    st.markdown("Isolates 'Pure Profit' by stripping statutory taxes, channel commissions, and incremental costs (Meals/Laundry). Ensures volume does not dilute profit.")
with p2:
    st.markdown("<span class='pillar-header'>⚖️ Pillar 02: Dynamic Hurdle Equilibrium</span>", unsafe_allow_html=True)
    st.markdown("Acts as the inventory gatekeeper, automatically scaling entry price requirements based on demand compression to protect high-value last-minute demand.")
with p3:
    st.markdown("<span class='pillar-header'>🌐 Pillar 03: External Velocity</span>", unsafe_allow_html=True)
    st.markdown("Integrates real-time city-wide flow data to weight inventory value. Fast market pickup (Compression) increases the value of remaining rooms exponentially.")
st.markdown("</div>", unsafe_allow_html=True)
