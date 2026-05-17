import streamlit as st
from datetime import date

# --- 1. SETTINGS & STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Strategic Intelligence Engine")

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

def clear_protocol_data():
    st.session_state["reset_key"] += 1
    for key in list(st.session_state.keys()):
        if key not in ["auth", "reset_key"]: del st.session_state[key]

# --- 3. SIDEBAR (COST CENTER) ---
rk = str(st.session_state["reset_key"])
with st.sidebar:
    st.markdown("### 🏨 Property Profile")
    h_name = st.text_input("Hotel Name", value="", placeholder="e.g. Wyndham Garden Salalah", key="h_nm_"+rk)
    city_search = st.text_input("📍 Market Location", value="", placeholder="e.g. Salalah", key="city_"+rk)
    
    st.divider()
    st.markdown("### 📅 Stay Period (LOS)")
    d1 = st.date_input("Check-In", date.today(), key="d_in_"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d_out_"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"Length of Stay: {m_nights} Night(s)")

    st.divider()
    st.markdown("### 🏛️ Pillars Setup")
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx_v_"+rk)
    p01_fee = st.number_input("P01 Fee (Per Room)", value=6.00, step=0.1, key="p01_v_"+rk)

    st.markdown("### 🍽️ Meal Plan Cost (PP)")
    c_bf = st.number_input("BF Cost (PP)", value=2.00, key="bf_mc_"+rk)
    c_ln = st.number_input("LN Cost (PP)", value=3.00, key="ln_mc_"+rk)
    c_dn = st.number_input("DN Cost (PP)", value=5.00, key="dn_mc_"+rk)
    c_sai = st.number_input("SAI Cost (PP)", value=12.00, key="sai_mc_"+rk)
    c_ai = st.number_input("AI Cost (PP)", value=15.00, key="ai_mc_"+rk)

    if st.button("🗑️ Reset Engine", use_container_width=True, type="primary"):
        clear_protocol_data()
        st.rerun()

# --- 4. MARKET INTEL ---
intel_db = {}
intel_db["salalah"] = {
    "ev": "Khareef Season",
    "fl": "OmanAir Peak",
    "news": "Monsoon Surge.",
    "demand": "Compression"
}
intel_db["muscat"] = {
    "ev": "Business Summit",
    "fl": "Hub Stable",
    "news": "MICE demand up.",
    "demand": "High Flow"
}
active_intel = intel_db.get(city_search.lower(), {"ev": "Stable", "fl": "Normal", "news": "Stable.", "demand": "Standard"})

# --- 5. LOGIC ENGINE (STRATEGIC AUDIT) ---
def run_equilibrium_engine(adr, room_counts, base_hurdle, demand, total_rooms, comm_rate=0.0, anc_prpn=0.0, laundry=0.0):
    vm = 1.0 
    
    dh = base_hurdle * {"Compression (Peak)": 2.5, "High Flow": 1.5, "Standard": 1.0, "Distressed": 0.7}.get(demand, 1.0)
    
    net_adr = adr / tx_div
    
    meal_sum = (
        (room_counts['BB'] * c_bf) +
        (room_counts['HB'] * (c_bf + c_dn)) +
        (room_counts['FB'] * (c_bf + c_ln + c_dn)) +
        (room_counts['SAI'] * c_sai) +
        (room_counts['AI'] * c_ai)
    )
    meal_unit = meal_sum / max(total_rooms, 1)
    
    anc_net = anc_prpn / tx_div
    
    comm_val = net_adr * (comm_rate / 100)
    
    unit_w = (net_adr + anc_net) - (meal_unit + comm_val + p01_fee + laundry)
    
    if unit_w < dh: 
        stt = "REJECT: DILUTIVE"
        clr = "#e74c3c"
        rsn = "Wealth below market equilibrium."
    elif unit_w < (dh + 5.0): 
        stt = "REVIEW: MARGINAL"
        clr = "#f39c12"
        rsn = "At hurdle equilibrium threshold."
    else: 
        stt = "ACCEPT: OPTIMIZED"
        clr = "#27ae60"
        rsn = "Wealth targets successfully achieved."
    
    mp_basis = "RO"
    for p in ["AI", "SAI", "FB", "HB", "BB"]:
        if room_counts.get(p, 0) > 0: mp_basis = p; break

    total_noi = unit_w * total_rooms * m_nights
    
    return {"w": unit_w, "st": stt, "cl": clr, "dh": dh, "noi": total_noi, "mp": mp_basis, "rsn": rsn}

# --- 6. DASHBOARD MAIN ---
st.markdown(f"<h1 class='main-title'>{h_name.upper() if h_name else 'YIELD ENGINE'}</h1>", unsafe_allow_html=True)
st.markdown("<div style='text-align:center; color:#4b6584; font-weight:700; margin-bottom:20px;'>Yield Equilibrium Strategic Intelligence Engine</div>", unsafe_allow_html=
