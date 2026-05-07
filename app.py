import streamlit as st
from datetime import date

# --- 1. SETTINGS & STYLING ---
st.set_page_config(layout="wide", page_title="Universal Yield Engine")

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

# --- 3. SIDEBAR (UNIVERSAL CONFIG) ---
with st.sidebar:
    st.markdown("### 🏨 Property Setup")
    h_name = st.text_input("Hotel/Resort Name", "Wyndham Garden Salalah")
    h_cap = st.number_input("Total Room Inventory", min_value=1, value=237)
    
    st.divider()
    st.markdown("### 📅 Stay Duration")
    d1 = st.date_input("Check-In", date.today())
    d2 = st.date_input("Check-Out", date(2026, 5, 12))
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"Analysis Period: {m_nights} Nights")

    st.divider()
    curr_map = {"OMR (﷼)": "﷼", "AED (د.إ)": "د.إ", "SAR (﷼)": "﷼", "USD ($)": "$", "EUR (€)": "€", "LKR (රු)": "රු"}
    cur_sym = curr_map[st.selectbox("Select Currency", list(curr_map.keys()))]

    # FLEXIBLE TAX DIVISOR FORMULA
    st.markdown("### 🏛️ Pillar 01: Tax Formula")
    tax_input = st.text_input("Tax Divisor (Formula/Value)", value="1.2327", help="e.g. 1.2327 or (1+0.15)*(1+0.05)")
    try:
        # Evaluates string as math. Default to 1.2327 if empty or error.
        current_tax_divisor = float(eval(tax_input)) if tax_input else 1.2327
    except:
        current_tax_divisor = 1.2327
        st.warning("Invalid math. Using default 1.2327")
    
    st.caption(f"Calculated Divisor: **{current_tax_divisor:.4f}**")

    p01_fee = st.number_input(f"P01 Fixed Fee ({cur_sym})", min_value=0.0, value=6.0)

# --- 4. ENGINE LOGIC ---
def run_yield_calculation(adr, meal_qty, hurdle, demand, is_group, rooms, comm_rate=0.0):
    # Velocity Mapping
    v_mult = {"Compression": 1.25, "High Flow": 1.15, "Standard": 1.0, "Distressed": 0.85}.get(demand, 1.0)
    
    # Net ADR Calculation
    net_adr = (adr * v_mult) / current_tax_divisor
    commission_cost = net_adr * (comm_rate / 100)
    
    # Pillar 01: Pure Wealth
    unit_wealth = (net_adr - commission_cost) - p01_fee
    
    # Dynamic Hurdle (Pillar 02)
    dynamic_hurdle = hurdle * {"Compression": 2.5, "High Flow": 1.7, "Standard": 1.0, "Distressed": 0.7}.get(demand, 1.0)
    
    status = "ACCEPT: OPTIMIZED" if unit_wealth >= dynamic_hurdle else "REJECT: DILUTIVE"
    clr = "#27ae60" if unit_wealth >= dynamic_hurdle else "#e74c3c"
    
    return {"w": unit_wealth, "st": status, "cl": clr, "dh": dynamic_hurdle, "vm": v_mult}

# --- 5. MAIN UI ---
st.markdown(f"<h1 class='main-title'>{h_name.upper()}</h1>", unsafe_allow_html=True)
st.markdown(f"<div class='google-window'>🌐 <b>Tax Divisor Formula Active:</b> {tax_input} | <b>Effective Divisor:</b> {current_tax_divisor:.4f}</div>", unsafe_allow_html=True)

# Example Segment
st.markdown("<div class='card' style='border-left-color:#3498db'>1. DIRECT / FIT SEGMENT</div>", unsafe_allow_html=True)
with st.container():
    st.markdown("<div class='pricing-row'>", unsafe_allow_html=True)
    c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
    g_rate = c1.number_input("Gross Rate", value=75.0)
    dem = c2.selectbox("Market Demand", ["Standard", "High Flow", "Compression", "Distressed"])
    hrd = c3.number_input("Base Hurdle", value=45.0)
    comm = c4.slider("Commission %", 0, 25, 0)

    res = run_yield_calculation(g_rate, {}, hrd, dem, False, 1, comm)
    
    v = st.columns([1, 1.5, 1])
    v[0].metric("Net Wealth (Unit)", f"{cur_sym}
