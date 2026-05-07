import streamlit as st
from datetime import date

# --- 1. SETTINGS & STYLING (Original High-Fidelity) ---
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
    with st.form("login_gate"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock"):
            if pwd == "Gayan2026": 
                st.session_state["auth"] = True
                st.rerun()
    st.stop()

# --- 3. SIDEBAR (STAY & COSTS) ---
with st.sidebar:
    st.markdown("### 🏨 Property Profile")
    h_name = st.text_input("Hotel Name", "Wyndham Garden Salalah")
    h_cap = st.number_input("Total Capacity", min_value=1, value=237)
    city_search = st.text_input("📍 Market Location", "Salalah")
    
    st.divider()
    st.markdown("### 📅 Stay Period")
    d1 = st.date_input("Check-In", date.today())
    d2 = st.date_input("Check-Out", date(2026, 5, 8))
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"Stay Duration: {m_nights} Nights")

    st.divider()
    currencies = {"OMR (﷼)": "﷼", "AED (د.إ)": "د.إ", "SAR (﷼)": "﷼", "USD ($)": "$"}
    cur_sym = currencies[st.selectbox("Select Currency", list(currencies.keys()))]

    st.markdown("### 🏛️ Pillars Setup")
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f")
    p01_fee = st.number_input(f"P01 Fee ({cur_sym})", value=6.00)

    st.markdown("### 🍽️ Meal Plan Cost (PP)")
    meal_costs = {
        "BF": st.number_input("Breakfast (BF)", value=2.00),
        "LN": st.number_input("Lunch (LN)", value=0.0),
        "DN": st.number_input("Dinner (DN)", value=0.0),
        "SAI": st.number_input("Soft All-In (SAI)", value=0.0),
        "AI": st.number_input("All-Inclusive (AI)", value=0.0)
    }

# --- 4. ENGINE LOGIC ---
def run_segment_yield(adr, meal_qty, base_hurdle, demand_type, is_group, total_rooms, mice=0.0, laundry=0.0, transport=0.0):
    v_mult = {"Compression (Peak)": 1.25, "High Flow": 1.10, "Standard": 1.0, "Distressed": 0.85}.get(demand_type, 1.0)
    
    # Identify Basis Label
    bf, ln, dn, sai, ai = meal_qty.get("BF", 0), meal_qty.get("LN", 0), meal_qty.get("DN", 0), meal_qty.get("SAI", 0), meal_qty.get("AI", 0)
    if ai > 0: mp_basis = "AI"
    elif sai > 0: mp_basis = "SAI"
    elif bf > 0 and ln > 0 and dn > 0: mp_basis = "FB"
    elif bf > 0 and dn > 0: mp_basis = "HB"
    elif bf > 0: mp_basis = "BB"
    else: mp_basis = "RO"

    dynamic_hurdle = base_hurdle * {"Compression (Peak)": 2.5, "High Flow": 1.5, "Standard": 1.0, "Distressed": 0.7}.get(demand_type, 1.0)
    net_adr = (adr * v_mult) / tx_div
    total_meal_cost = sum(qty * meal_costs.get(p, 0) for p, qty in meal_qty.items())
    
    divisor = max(total_rooms, 10) if is_group else max(total_rooms, 1)
    group_rev = (mice / tx_div) + ((transport / tx_div) / divisor) if is_group else 0
    unit_w = (net_adr + group_rev - total_meal_cost) - p01_fee - laundry
    
    if unit_w < dynamic_hurdle: stt, clr, rsn = "REJECT: DILUTIVE", "#e74c3c", f"Below Hurdle ({mp_basis})"
    elif unit_w < (dynamic_hurdle + 5.0): stt, clr, rsn = "REVIEW: MARGINAL", "#f39c12", f"Equilibrium window ({mp_basis})"
    else: stt, clr, rsn = "ACCEPT: OPTIMIZED", "#27ae60", f"Optimal Wealth ({mp_basis})"
        
    return {"w": unit_w, "st": stt, "cl": clr, "rsn": rsn, "vm": v_mult, "dh": dynamic_hurdle, "noi": unit_w * divisor * m_nights}

# --- 5. TOP DASHBOARD ---
st.markdown(f"<h1 class='main-title'>{h_name.upper()}</h1>", unsafe_allow_html=True)
st.markdown(f"""<div class='google-window'><b>🌐 Market Intelligence: {city_search} | May 2026</b><br>
• <b>Stay Duration:</b> {m_nights} Nights | <b>Currency:</b> {cur_sym} | <b>Market Pulse:</b> Standard Flow Applied.</div>""", unsafe_allow_html=True)

# --- 6. SEGMENT AUDITS ---
segments = [
    {"label": "1. DIRECT / FIT", "key": "fit", "color": "#3498db", "hurdle": 45.0, "group": False},
    {"label": "2. OTA CHANNELS", "key": "ota", "color": "#2ecc71", "hurdle": 35.0, "group": False},
    {"label": "3. CORPORATE / MICE", "key": "mice", "color": "#34495e", "hurdle": 32.0, "group": True},
    {"label": "4. GROUP TOUR & TRAVEL", "key": "tnt", "color": "#e67e22", "hurdle": 12.0, "group": True}
]

for seg in segments:
    if st.checkbox(f"Activate {seg['label']}", value=True, key=f"act_{seg['key']}"):
        st.markdown(f"<div class='card' style='border-left-color:{seg['color']}'>{seg['label']}</div>", unsafe_allow_html=True)
        with st.container():
            st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
            r1 = st.columns([1, 0.6, 0.6, 0.6, 0.6, 1.2, 1.2])
            g_rate = r1[0].number_input(f"Gross Rate", value=75.0, key=f"adr_{seg['key']}")
            sgl, dbl, tpl, qrpl = r1[1].number_input("SGL", 0, key=f"s_{seg['key']}"), r1[2].number_input("DBL", 1, key=f"d_{seg['key']}"), r1[3].number_input("TPL", 0, key=f"t_{seg['key']}"), r1[4].number_input("QRPL", 0, key=f"q_{seg['key']}")
            demand_sel = r1[5].selectbox("Demand", ["Standard", "High Flow", "Compression (Peak)", "Distressed"], key=f"dm_{seg['key']}")
            h_base = r1[6].number_input("Base Hurdle", value=seg['hurdle'], key=f"hr_{seg['key
