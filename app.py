import streamlit as st
from datetime import date

# --- 1. INITIALIZE SESSION STATE (CRITICAL FOR ISOLATION) ---
if "auth" not in st.session_state: 
    st.session_state["auth"] = False
if "reset_key" not in st.session_state: 
    st.session_state["reset_key"] = 0

# --- 2. SETTINGS & STYLING (YOUR ORIGINAL FORMAT) ---
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

# --- 3. AUTHENTICATION ---
if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login_gate"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock"):
            if pwd == "Gayan2026": 
                st.session_state["auth"] = True
                st.rerun()
    st.stop()

# --- 4. RESET LOGIC ---
def reset_engine():
    st.session_state["reset_key"] += 1
    # Clear variables but keep auth
    for key in list(st.session_state.keys()):
        if key not in ["auth", "reset_key"]:
            del st.session_state[key]

# --- 5. SIDEBAR (CONTEXTUAL DATA) ---
rk = str(st.session_state["reset_key"])
with st.sidebar:
    st.markdown("### 🏨 Property Profile")
    # value="" ensures it is empty after reset. Wyndham Garden Salalah is now a placeholder.
    h_name = st.text_input("Hotel Name", value="", placeholder="e.g. Wyndham Garden Salalah", key="h_nm_"+rk)
    h_cap = st.number_input("Total Capacity", min_value=1, value=237, step=1, key="cap_"+rk)
    city_search = st.text_input("📍 Market Location", value="", placeholder="e.g. Salalah", key="city_"+rk)
    
    st.divider()
    st.markdown("### 📅 Stay Period")
    d1 = st.date_input("Check-In", date.today(), key="d_in_"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d_out_"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"Stay Duration: {m_nights} Nights")

    st.divider()
    st.markdown("### 🌍 Global Currency Suite")
    currencies = {
        "OMR (﷼)": "﷼", "AED (د.إ)": "د.إ", "SAR (﷼)": "﷼", "QAR (﷼)": "﷼", "BHD (.د)": ".د", "KWD (د.ك)": "د.ك",
        "USD ($)": "$", "EUR (€)": "€", "GBP (£)": "£", "LKR (රු)": "රු", "INR (₹)": "₹", "CHF (CHF)": "CHF"
    }
    cur_sym = currencies[st.selectbox("Select Currency", list(currencies.keys()), key="c_sel_"+rk)]

    st.divider()
    st.markdown("### 🏛️ Pillars Setup")
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx_v_"+rk)
    p01_fee = st.number_input(f"P01 Fee ({cur_sym})", value=6.00, step=0.1, key="p01_v_"+rk)

    st.markdown("### 🍽️ Meal Plan Cost (PP)")
    meal_costs = {
        "BF": st.number_input("Breakfast Cost", min_value=0.0, value=2.00, step=0.5, key="bf_mc_"+rk),
        "LN": st.number_input("Lunch Cost", min_value=0.0, value=0.0, step=0.5, key="ln_mc_"+rk),
        "DN": st.number_input("Dinner Cost", min_value=0.0, value=0.0, step=0.5, key="dn_mc_"+rk),
        "SAI": st.number_input("Soft All-In Cost", min_value=0.0, value=0.0, step=0.5, key="sai_mc_"+rk),
        "AI": st.number_input("All-Inclusive Cost", min_value=0.0, value=0.0, step=0.5, key="ai_mc_"+rk)
    }

    st.divider()
    if st.button("🗑️ RESET ALL DATA", use_container_width=True, type="primary"):
        reset_engine()
        st.rerun()

# --- 6. MARKET INTEL DATA ---
intel_db = {
    "salalah": {"ev": "Khareef Festival Season", "fl": "OmanAir/SalamAir Peak", "news": "Monsoon Tourism Surge expected.", "demand": "Compression"},
    "muscat": {"ev": "Business Summit", "fl": "International Hub Stable", "news": "MICE demand up 15%.", "demand": "High Flow"}
}
active_intel = intel_db.get(city_search.lower(), {"ev": "Market Rotation", "fl": "Standard Flights", "news": "Location data pending.", "demand": "Standard"})

# --- 7. ENGINE LOGIC (YOUR ORIGINAL CALCULATIONS) ---
def run_segment_yield(adr, meal_qty, base_hurdle, demand_type, is_group, total_rooms, comm_rate=0.0, mice=0.0, laundry=0.0, transport=0.0):
    velocity_map = {"Compression (Peak)": 1.25, "High Flow": 1.10, "Standard": 1.0, "Distressed": 0.85}
    v_mult = velocity_map.get(demand_type, 1.0)
    
    bf, ln, dn, sai, ai = meal_qty.get("BF", 0), meal_qty.get("LN", 0), meal_qty.get("DN", 0), meal_qty.get("SAI", 0), meal_qty.get("AI", 0)
    if ai > 0: mp_basis = "AI"
    elif sai > 0: mp_basis = "SAI"
    elif bf > 0 and ln > 0 and dn > 0: mp_basis = "FB"
    elif bf > 0 and dn > 0: mp_basis = "HB"
    elif bf > 0: mp_basis = "BB"
    else: mp_basis = "RO"

    hurdle_multiplier = {"Compression (Peak)": 2.5, "High Flow": 1.5, "Standard": 1.0, "Distressed": 0.7}
    dynamic_hurdle = base_hurdle * hurdle_multiplier.get(demand_type, 1.0)
    
    net_adr = (adr * v_mult) / tx_div
    total_meal_cost = sum(qty * meal_costs.get(p, 0) for p, qty in meal_qty.items())
    
    divisor = max(total_rooms, 10) if is_group else max(total_rooms, 1)
    group_rev = (mice / tx_div) + ((transport / tx_div) / divisor) if is_group else 0
    
    unit_w = (net_adr + group_rev - total_meal_cost - (net_adr * (comm_rate/100))) - p
