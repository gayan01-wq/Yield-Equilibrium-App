import streamlit as st
from datetime import date

# --- 1. STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Master")
st.markdown("""<style>
.block-container{padding-top:1rem!important;}
.main-title{font-size:1.8rem!important;font-weight:900;color:#1e3799;text-align:center;margin-top:-10px;}
.card{padding:10px;border-radius:10px;margin-bottom:8px;border-left:10px solid;background:#ffffff;box-shadow: 0 2px 4px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff;padding:12px;border-radius:10px;border:1px solid #d1d9e6; margin-top:5px;}
.sentinel-box{background:#1e3799; color:white; padding:15px; border-radius:10px; margin-bottom:15px; border-left:10px solid #ffc107;}
.google-window{background:#e8f0fe; padding:12px; border-radius:10px; border:1px solid #4285f4; margin-bottom:15px; font-size:0.85rem;}
.status-indicator{padding:10px; border-radius:10px; text-align:center; font-weight:900; font-size:1.2rem; color:white; margin-top:10px;}
[data-testid="stSidebar"]{background:#f1f4f9; border-right:1px solid #dee2e6}
.meal-header {font-size: 0.8rem; font-weight: bold; color: #1e3799; border-bottom: 1px solid #ddd; margin-bottom: 5px;}
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

# --- 3. SIDEBAR (PILLAR 01 & 03) ---
with st.sidebar:
    st.markdown("### 👤 Strategic Architect\nGayan Nugawela")
    if st.button("☢️ Nuclear Data Reset"):
        st.session_state["reset_key"] += 1
        st.rerun()
    st.divider()
    
    rk = str(st.session_state["reset_key"]) 
    
    st.markdown("### 🏨 Pillar 01: Global Constants")
    location = st.selectbox("📍 Location Select", ["Salalah", "Muscat", "Dubai"], key="loc"+rk)
    d1 = st.date_input("Check-In", date.today(), key="d1"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d2"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    
    inventory = st.number_input("Total Inventory", 1, 1000, 237, key="inv"+rk)
    p01_fee = st.number_input("P01 Variable Fee", 0.0, value=6.90, key="p01"+rk)
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx"+rk)
    
    st.markdown("### 🍽️ Unit Pax Costs")
    c_bb = st.number_input("BB Cost", 0.0, key="cbb"+rk)
    c_hb = st.number_input("HB Cost", 2.5, key="chb"+rk)
    c_fb = st.number_input("FB Cost", 5.0, key="cfb"+rk)
    c_sai = st.number_input("SAI Cost", 7.5, key="csai"+rk)
    c_ai = st.number_input("AI Cost", 10.0, key="cai"+rk)
    meal_unit_costs = {"RO": 0, "BB": c_bb, "HB": c_hb, "FB": c_fb, "SAI": c_sai, "AI": c_ai}

    st.markdown("### 📈 Pillar 03: Velocity & Pace")
    otb_pace = st.slider("OTB Pace %", 0, 100, 15, key="otb"+rk)
    avg_occ = st.slider("Avg Historical Occupancy %", 0, 100, 45, key="occ"+rk)
    v_mult = 1.25 if otb_pace > avg_occ else 1.0

# --- 4. CALCULATION ENGINE ---
def run_yield(rms, nts, adr, meals, hurdle, comm_rate=0.18, laundry=0):
    total_rooms = sum(rms)
    if total_rooms <= 0: return None
    room_nights = total_rooms * nts
    net_adr = adr / tx_div
    total_meal_cost = sum(qty * meal_unit_costs.get(plan, 0) for plan, qty in meals.items())
    avg_meal_cost = total_meal_cost / total_rooms
    
    # Wealth Stripping including Laundry
    wealth = (net_adr - avg_meal_cost - (net_adr * comm_rate)) - p01_fee - laundry
    status, color = ("OPTIMIZED", "#27ae60") if wealth >= hurdle else ("DILUTIVE", "#e74c3c")
    return {"w": wealth, "st": status, "cl": color, "rn": room_nights}

# --- 5. MAIN DASHBOARD ---
st.markdown("<h1 class='main-title'>YIELD EQUILIBRIUM MASTER DASHBOARD</h1>", unsafe_allow_html=True)

st.markdown(f"""<div class='google-window'>
    <b>🌐 Google Intelligence Feed: {location
