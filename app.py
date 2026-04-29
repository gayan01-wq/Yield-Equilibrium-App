import streamlit as st
from datetime import date

# --- 1. STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Master")
st.markdown("""<style>
.block-container{padding-top:1rem!important;}
.main-title{font-size:1.8rem!important;font-weight:900;color:#1e3799;text-align:center;margin-top:-10px;}
.card{padding:12px;border-radius:10px;margin-bottom:10px;border-left:10px solid;background:#ffffff;box-shadow: 0 2px 4px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff;padding:15px;border-radius:10px;border:1px solid #d1d9e6; margin-top:5px;}
.sentinel-box{background:#1e3799; color:white; padding:15px; border-radius:10px; margin-bottom:15px; border-left:10px solid #ffc107;}
.google-window{background:#e8f0fe; padding:12px; border-radius:10px; border:1px solid #4285f4; margin-bottom:15px; font-size:0.85rem;}
.status-indicator{padding:12px; border-radius:10px; text-align:center; font-weight:900; font-size:1.3rem; color:white; margin-top:10px;}
[data-testid="stSidebar"]{background:#f1f4f9; border-right:1px solid #dee2e6}
.meal-header {font-size: 0.85rem; font-weight: bold; color: #1e3799; margin-top: 10px; border-bottom: 1px solid #d1d9e6;}
</style>""", unsafe_allow_html=True)

# --- 2. SESSION STATE & RESET ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if "reset_key" not in st.session_state: st.session_state["reset_key"] = 0

if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock"):
            if pwd == "Gayan2026": 
                st.session_state["auth"] = True
                st.rerun()
            else: st.error("Denied")
    st.stop()

# --- 3. SIDEBAR (MASTER PILLAR 01 & 03) ---
with st.sidebar:
    st.markdown("### 👤 Strategic Architect\nGayan Nugawela")
    if st.button("☢️ Nuclear Data Reset"):
        st.session_state["reset_key"] += 1
        st.rerun()
    st.divider()
    
    rk = str(st.session_state["reset_key"]) 
    
    st.markdown("### 🏨 Pillar 01: Global Constants")
    location = st.selectbox("📍 Location Select", ["Salalah", "Muscat", "Dubai"], key="loc"+rk)
    
    # STAY DATES
    d1 = st.date_input("Check-In", date.today(), key="d1"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d2"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    
    inventory = st.number_input("Inventory", 1, 1000, 237, key="inv"+rk)
    p01_fee = st.number_input("P01 Variable Fee", 0.00, value=6.90, key="p01"+rk)
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx"+rk)
    
    # MASTER MEAL COSTS (RE-INTEGRATED ALL 6)
    st.markdown("### 🍽️ Pillar 01: Unit Pax Costs")
    c_bb = st.number_input("BB Unit Cost", 0.0, key="cbb"+rk)
    c_hb = st.number_input("HB Unit Cost", 2.5, key="chb"+rk)
    c_fb = st.number_input("FB Unit Cost", 5.0, key="cfb"+rk)
    c_sai = st.number_input("SAI Unit Cost", 7.5, key="csai"+rk)
    c_ai = st.number_input("AI Unit Cost", 10.0, key="cai"+rk)
    
    meal_unit_costs = {"RO": 0, "BB": c_bb, "HB": c_hb, "FB": c_fb, "SAI": c_sai, "AI": c_ai}

    st.markdown("### 📈 Pillar 03: Velocity")
    otb_pace = st.slider("OTB Pace %", 0, 100, 15, key="otb"+rk)
    v_mult = 1.25 if otb_pace > 65 else 1.0

# --- 4. CALCULATION ENGINE ---
def run_yield(rms, nts, adr, meals, hurdle, comm_rate=0.18):
    total_rooms = sum(rms)
    if total_rooms <= 0: return None
    room_nights = total_rooms * nts
    net_adr = adr / tx_div
    
    total_meal_cost = sum(qty * meal_unit_costs.get(plan, 0) for plan, qty in meals.items())
    avg_meal_cost_per_room = total_meal_cost / total_rooms
    
    # Wealth Stripping Formula
    wealth = (net_adr - avg_meal_cost_per_room - (net_adr * comm_rate)) - p01_fee
    
    status, color = ("OPTIMIZED", "#27ae60") if wealth >= hurdle else ("DILUTIVE", "#e74c3c")
    return {"w": wealth, "st": status, "cl": color, "rn": room_nights}

# --- 5. MAIN DASHBOARD ---
st.markdown("<h1 class='main-title'>YIELD EQUILIBRIUM MASTER DASHBOARD</h1>", unsafe_allow_html=True)

st.markdown(f"""<div class='google-window'>
    <b>🌐 Google Intelligence Feed: {location}</b> | 📅 Stay: {d1} to {d2} ({m_nights} Nights) | ⚖️ Tax: {tx_div}
</div>""", unsafe_allow_html=True)

def draw_seg(label, key, suggest_adr, hurdle_rate, color, ota=False):
    rk = str(st.session_state["reset_key"])
    st.markdown(f"<div class='card' style='border-left-color:{color}'>{label}</div>", unsafe_allow_html=True)
    
    col_input, col_result = st.columns([2.6, 1])
    
    with col_input:
        st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
        r1, r2, r3 = st.columns(3)
        sgl = r1.number_input("SGL Rooms", 0, key="s"+key+rk)
        dbl = r2.number_input("DBL Rooms", 0, key="d"+key+rk)
        applied_adr = r3.number_input("Applied ADR", value=float(suggest_adr), key="a"+key+rk)
        
        # MEAL PACKAGES (Restored All 6 in two rows for visibility)
        st.markdown("<div class='meal-header'>Select Meal Plan Quantities (Pax)</div>", unsafe_allow_html=True)
        m_row1 = st.columns(3)
        m_ro = m_row1[0].number_input("RO", 0, key="mro"+key+rk)
        m_bb = m_row1[1].number_input("BB", 0, key="mbb"+key+rk)
        m_hb = m_row1[2].number_input("HB", 0, key="mhb"+key+rk)
        
        m_row2 = st.columns(3)
        m_fb = m_row2[0].number_input("FB", 0, key="mfb"+key+rk)
        m_sai = m_row2[1].number_input("SAI", 0, key="msai"+key+rk)
        m_ai = m_row2[2].number_input("AI", 0, key="mai"+key+rk)
        
        selected_meals = {"RO": m_ro, "BB": m_bb, "HB": m_hb, "FB": m_fb, "SAI": m_sai, "AI": m_ai}
        st.markdown("</div>", unsafe_allow_html=True)
        
    res = run_yield([sgl, dbl], m_nights, applied_adr, selected_meals, hurdle_rate, 0.18 if ota else 0.0)
    
    if res:
        with col_result:
            st.metric("Net Wealth (Unit)", f"OMR {res['w']:,.2f}")
            st.write(f"**Audit Room Nights:** {res['rn']}")
            st.markdown(f"<div class='status-indicator' style='background:{res['cl']}'>{res['st']}</div>", unsafe_allow_html=True)

# DRAW SEGMENTS
draw_seg("1. DIRECT / FIT CHANNELS", "fit", 65, 40, "#3498db")
draw_seg("2. OTA / ONLINE CHANNELS", "ota", 60, 35, "#2ecc71", ota=True)
draw_seg("3. CORPORATE / MICE GROUPS", "grp", 50, 30, "#9b59b6")
