import streamlit as st
from datetime import date

# --- 1. SETTINGS & STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

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
    st.markdown("### 🏨 Property Profile")
    h_name = st.text_input("Hotel Name", "Wyndham Garden Salalah")
    h_cap = st.number_input("Total Capacity", min_value=1, value=237)
    city_search = st.text_input("📍 Market Location", "Salalah")
    
    st.divider()
    d1 = st.date_input("Check-In", date.today())
    d2 = st.date_input("Check-Out", date(2026, 5, 8))
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"Stay Duration: {m_nights} Nights")

    st.divider()
    curr_map = {
        "OMR (﷼)": "﷼", "AED (د.إ)": "د.إ", "SAR (﷼)": "﷼", "USD ($)": "$", 
        "EUR (€)": "€", "GBP (£)": "£", "LKR (රු)": "රු", "INR (₹)": "₹"
    }
    cur_sym = curr_map[st.selectbox("Select Currency", list(curr_map.keys()))]

    tx_div = st.number_input("Tax Divisor", min_value=1.0, value=1.2327)
    p01_fee = st.number_input(f"P01 Fee ({cur_sym})", min_value=0.0, value=6.0)

    st.markdown("### 🍽️ Meal costs (PP)")
    m_costs = {
        "BF": st.number_input("Breakfast", min_value=0.0, value=2.0),
        "LN": st.number_input("Lunch", min_value=0.0, value=0.0),
        "DN": st.number_input("Dinner", min_value=0.0, value=0.0),
        "SAI": st.number_input("SAI Cost", min_value=0.0, value=0.0),
        "AI": st.number_input("AI Cost", min_value=0.0, value=0.0)
    }

# --- 4. ENGINE LOGIC ---
def run_yield(adr, meal_qty, hurdle, demand, is_group, rooms, mice=0.0, laund=0.0, trans=0.0):
    v_map = {"Compression (Peak)": 1.25, "High Flow": 1.10, "Standard": 1.0, "Distressed": 0.85}
    v_mult = v_map.get(demand, 1.0)
    
    bf, ln, dn, sai, ai = meal_qty.get("BF",0), meal_qty.get("LN",0), meal_qty.get("DN",0), meal_qty.get("SAI",0), meal_qty.get("AI",0)
    if ai > 0: mp = "AI"
    elif sai > 0: mp = "SAI"
    elif bf > 0 and ln > 0 and dn > 0: mp = "FB"
    elif bf > 0 and dn > 0: mp = "HB"
    elif bf > 0: mp = "BB"
    else: mp = "RO"

    net_adr = (adr * v_mult) / tx_div
    meal_tot = sum(qty * m_costs.get(p, 0) for p, qty in meal_qty.items())
    
    div = max(rooms, 10) if is_group else max(rooms, 1)
    grp_rev = (mice / tx_div) + ((trans / tx_div) / div) if is_group else 0
    unit_w = (net_adr + grp_rev - meal_tot) - p01_fee - laund
    
    h_map = {"Compression (Peak)": 2.5, "High Flow": 1.5, "Standard": 1.0, "Distressed": 0.7}
    dyn_h = hurdle * h_map.get(demand, 1.0)
    
    stt = "ACCEPT: OPTIMIZED" if unit_w >= dyn_h else "REJECT: DILUTIVE"
    clr = "#27ae60" if unit_w >= dyn_h else "#e74c3c"
    
    return {"w": unit_w, "st": stt, "cl": clr, "mp": mp, "noi": unit_w * div * m_nights, "dh": dyn_h, "vm": v_mult}

# --- 5. TOP DASHBOARD ---
st.markdown(f"<h1 class='main-title'>{h_name.upper()}</h1>", unsafe_allow_html=True)

intel_db = {
    "salalah": {"ev": "Khareef Season", "fl": "OmanAir Peak", "news": "Surge expected.", "dm": "Compression"},
    "muscat": {"ev": "Business Summit", "fl": "Hub Stable", "news": "MICE demand up.", "dm": "High Flow"}
}
intel = intel_db.get(city_search.lower(), {"ev": "Standard", "fl": "Stable", "news": "Stable flow.", "dm": "Standard"})

st.markdown(f"""
<div class='google-window'>
    <b>🌐 Market Intel: {city_search} | May 2026</b><br>
    • <b>Events:</b> {intel['ev']} | <b>Pulse:</b> {intel['dm']} Logic Applied.
</div>
""", unsafe_allow_html=True)

# --- 6. SEGMENTS ---
segments = [
    {"label": "1. DIRECT / FIT", "key": "fit", "color": "#3498db", "h": 45.0, "grp": False},
    {"label": "2. OTA CHANNELS", "key": "ota", "color": "#2ecc71", "h": 35.0, "grp": False},
    {"label": "3. CORPORATE / MICE", "key": "mice", "color": "#34495e", "h": 32.0, "grp": True},
    {"label": "4. GROUP TOUR & TRAVEL", "key": "tnt", "color": "#e67e22", "h": 12.0, "grp": True}
]

for s in segments:
    if st.checkbox(f"Activate {s['label']}", value=True, key=f"chk_{s['key']}"):
        st.markdown(f"<div class='card' style='border-left-color:{s['color']}'>{s['label']}</div>", unsafe_allow_html=True)
        with st.container():
            st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
            r1 = st.columns([1, 0.6, 0.6, 0.6, 0.6, 1.2, 1.2])
            g_rate = r1[0].number_input("Gross Rate", min_value=0.0, value=75.0, key=f"adr_{s['key']}")
            sgl, dbl, tpl, qrpl = r1[1].number_input("SGL", 0, key=f"s_{s['key']}"), r1[2].number_input("DBL", 1, key=f"d_{s['key']}"), r1[3].number_input("TPL", 0, key=f"t_{s['key']}"), r1[4].number_input("QRPL", 0, key=f"q_{s['key']}")
            dem = r1[5].selectbox("Demand", ["Standard", "High Flow", "Compression (Peak)", "Distressed"], key=f"dm_{s['key']}")
            hrd = r1[6].number_input("Hurdle", min_value=0.0, value=s['h'], key=f"hr_{s['key']}")

            r2 = st.columns([0.6, 0.6, 0.6, 0.6, 0.6, 1.1, 1.1, 1.1])
            v_bb = r2[0].number_input("BB", 0, key=f"bb_{s['key']}")
            v_ln = r2[1].number_input("LN", 0, key=f"ln_{s['key']}")
            v_dn = r2[2].number_input("DN", 0, key=f"dn_{s['key']}")
            v_sai = r2[3].number_input("SAI", 0, key=f"sai_{s['key']}")
            v_ai = r2[4].number_input("AI", 0, key=f"ai_{s['key']}")
            
            m_r = r2[5].number_input("MICE Rev", min_value=0.0, key=f"mice_{s['key']}") if s['grp'] else 0.0
            l_c = r2[6].number_input("Laundry", min_value=0.0, key=f"lnd_{s['key']}") if s['grp'] else 0.0
            t_c = r2[7].number_input("Transport", min_value=0.0, key=f"tra_{s['key']}") if s['grp'] else 0.0

            res = run_yield(g_rate, {"BF":v_bb, "LN":v_ln, "DN":v_dn, "SAI":v_sai, "AI":v_ai}, hrd, dem, s['grp'], (sgl+dbl+tpl+qrpl), m_r, l_c, t_c)
            
            v = st.columns([1, 1.5, 1])
            v[0].metric("Net Wealth", f"{cur_sym} {res['w']:,.2f}", delta=f"{res['vm']}x Velocity")
            v[1].markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']} ({res['mp']})</div>", unsafe_allow_html=True)
            v[2].markdown(f"<div style='text-align:right;'><span class='noi-badge'>Total NOI: {cur_sym} {res['noi']:,.2f}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='reason-box'>💡 Hurdle: {cur_sym} {res['dh']:.2f} | Basis: {res['mp']}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# --- 7. PILLARS ---
st.divider()
st.markdown("<div class='theory-box'><h3 style='color:#1e3799; margin-top:0;'>THE YIELD EQUILIBRIUM STRATEGIC FRAMEWORK</h3>", unsafe_allow_html=True)
p1, p2, p3 = st.columns(3)
p1.markdown("<span class='pillar-header'>🏛️ Pillar 01: Wealth Stripping</span>", unsafe_allow_html=True)
p2.markdown("<span class='pillar-header'>⚖️ Pillar 02: Dynamic Hurdle</span>", unsafe_allow_html=True)
p3.markdown("<span class='pillar-header'>🌐 Pillar 03: Market Velocity</span>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
