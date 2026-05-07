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
    cur_sym = st.selectbox("Currency", ["OMR", "AED", "SAR", "USD"])
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f")
    p01_f = st.number_input("P01 Fee", value=6.00)

    st.markdown("### 🍽️ Meal costs (PP)")
    m_costs = {
        "BF": st.number_input("Breakfast", value=2.0),
        "LN": st.number_input("Lunch", value=0.0),
        "DN": st.number_input("Dinner", value=0.0),
        "SAI": st.number_input("SAI", value=0.0),
        "AI": st.number_input("AI", value=0.0)
    }

# --- 4. ENGINE LOGIC ---
def run_yield(adr, meal_qty, hurdle, demand, is_group, rooms, mice=0.0, laund=0.0, trans=0.0):
    v_map = {"Compression (Peak)": 1.25, "High Flow": 1.10, "Standard": 1.0, "Distressed": 0.85}
    v_mult = v_map.get(demand, 1.0)
    
    # Meal Basis Detection
    bf, ln, dn, sai, ai = meal_qty.get("BF", 0), meal_qty.get("LN", 0), meal_qty.get("DN", 0), meal_qty.get("SAI", 0), meal_qty.get("AI", 0)
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
    unit_w = (net_adr + grp_rev - meal_tot) - p01_f - laund
    
    h_map = {"Compression (Peak)": 2.5, "High Flow": 1.5, "Standard": 1.0, "Distressed": 0.7}
    dyn_h = hurdle * h_map.get(demand, 1.0)
    
    stt = "ACCEPT: OPTIMIZED" if unit_w >= dyn_h else "REJECT: DILUTIVE"
    clr = "#27ae60" if unit_w >= dyn_h else "#e74c3c"
    
    return {"w": unit_w, "st": stt, "cl": clr, "mp": mp, "noi": unit_w * div * m_nights, "dh": dyn_h}

# --- 5. MAIN DASHBOARD ---
st.markdown(f"<h1 class='main-title'>{h_name.upper()}</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='google-window'>🌐 <b>Market Intelligence: {city_search}</b> | Duration: {m_nights} Nights</div>", unsafe_allow_html=True)

segs = [
    {"label": "1. DIRECT / FIT", "k": "fit", "c": "#3498db", "h": 45.0, "g": False},
    {"label": "2. OTA CHANNELS", "k": "ota", "c": "#2ecc71", "h": 35.0, "g": False},
    {"label": "3. CORPORATE / MICE", "k": "mice", "c": "#34495e", "h": 32.0, "g": True},
    {"label": "4. GROUP TOUR & TRAVEL", "k": "tnt", "c": "#e67e22", "h": 12.0, "g": True}
]

for s in segs:
    if st.checkbox(f"Activate {s['label']}", value=True, key=f"chk_{s['k']}"):
        st.markdown(f"<div class='card' style='border-left-color:{s['c']}'>{s['label']}</div>", unsafe_allow_html=True)
        with st.container():
            st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
            c1 = st.columns([1, 0.6, 0.6, 0.6, 0.6, 1.2, 1.2])
            g_rate = c1[0].number_input("Gross Rate", 75.0, key=f"adr_{s['k']}")
            sgl, dbl, tpl, qrpl = c1[1].number_input("SGL", 0, key=f"s_{s['k']}"), c1[2].number_input("DBL", 1, key=f"d_{s['k']}"), c1[3].number_input("TPL", 0, key=f"t_{s['k']}"), c1[4].number_input("QRPL", 0, key=f"q_{s['k']}")
            dem = c1[5].selectbox("Demand", ["Standard", "High Flow", "Compression (Peak)", "Distressed"], key=f"dm_{s['k']}")
            hrd = c1[6].number_input("Hurdle", s['h'], key=f"hr_{s['k']}")

            c2 = st.columns([0.6, 0.6, 0.6, 0.6, 0.6, 1.1, 1.1, 1.1])
            bb_v, ln_v, dn_v = c2[0].number_input("BB", 0, key=f"bb_{s['k']}"), c2[1].number_input("LN", 0, key=f"ln_{s['k']}"), c2[2].number_input("DN", 0, key=f"dn_{s['k']}")
            sai_v, ai_v = c2[3].number_input("SAI", 0, key=f"sai_{s['k']}"), c2[4].number_input("AI", 0, key=f"ai_{s['k']}")
            m_r = c2[5].number_input("MICE", 0.0, key=f"m_{s['k']}") if s['g'] else 0.0
            l_c = c2[6].number_input("Laundry", 0.0, key=f"l_{s['k']}") if s['g'] else 0.0
            t_c = c2[7].number_input("Transport", 0.0, key=f"tr_{s['k']}") if s['g'] else 0.0

            res = run_yield(g_rate, {"BF":bb_v, "LN":ln_v, "DN":dn_v, "SAI":sai_v, "AI":ai_v}, hrd, dem, s['g'], (sgl+dbl+tpl+qrpl), m_r, l_c, t_c)
            
            v = st.columns([1, 1.5, 1])
            v[0].metric("Net Wealth", f"{cur_sym} {res['w']:,.2f}")
            v[1].markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']} ({res['mp']})</div>", unsafe_allow_html=True)
            v[2].markdown(f"<div style='text-align:right;'><span class='noi-badge'>Total NOI: {cur_sym} {res['noi']:,.2f}</span></div>", unsafe_allow_html=True)
            st.markdown(f"<div class='reason-box'>Effective Hurdle: {cur_sym} {res['dh']:.2f}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

# --- 6. PILLARS ---
st.divider()
st.markdown("<div class='theory-box'><h3 style='color:#1e3799;'>THE YIELD EQUILIBRIUM STRATEGIC FRAMEWORK</h3>", unsafe_allow_html=True)
p1, p2, p3 = st.columns(3)
p1.markdown("<span class='pillar-header'>🏛️ Pillar 01</span><br><p style='font-size:0.85rem;'>Internal Wealth Stripping</p>", unsafe_allow_html=True)
p2.markdown("<span class='pillar-header'>⚖️ Pillar 02</span><br><p style='font-size:0.85rem;'>Dynamic Hurdle Equilibrium</p>", unsafe_allow_html=True)
p3.markdown("<span class='pillar-header'>🌐 Pillar 03</span><br><p style='font-size:0.85rem;'>External Velocity</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)
