import streamlit as st
from datetime import date

# --- 1. STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Master")
st.markdown("""<style>
.block-container{padding-top:1rem!important;}
.main-title{font-size:1.8rem!important;font-weight:900;color:#1e3799;text-align:center;margin-top:-10px;}
.card{padding:10px;border-radius:10px;margin-bottom:8px;border-left:10px solid;background:#ffffff;box-shadow: 0 2px 4px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff;padding:12px;border-radius:10px;border:1px solid #d1d9e6; margin-top:5px;}
.google-window{background:#e8f0fe; padding:15px; border-radius:12px; border:2px solid #4285f4; margin-bottom:15px; font-size:0.85rem; line-height:1.6;}
.status-indicator{padding:10px; border-radius:10px; text-align:center; font-weight:900; font-size:1.2rem; color:white; margin-top:10px;}
.audit-box{background:#fff9c4; border:1px solid #fbc02d; padding:10px; border-radius:8px; margin-top:12px; text-align:center; font-weight:bold; color:#5f4300; font-size:0.9rem;}
.theory-box{background:#fdfdfd; padding:25px; border-radius:15px; border:1px solid #dee2e6; margin-top:40px}
.highlight-text{color:#1e3799; font-weight:bold;}
[data-testid="stSidebar"]{background:#f1f4f9; border-right:1px solid #dee2e6}
</style>""", unsafe_allow_html=True)

# --- 2. SESSION STATE & NUCLEAR RESET ---
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

# --- 3. SIDEBAR (STRATEGIC LEVERS) ---
with st.sidebar:
    st.markdown("### 👤 Strategic Architect\nGayan Nugawela")
    if st.button("☢️ Nuclear Data Reset"):
        st.session_state["reset_key"] += 1
        st.rerun()
    st.divider()
    
    rk = str(st.session_state["reset_key"]) 
    
    st.markdown("### 🏨 Pillar 01: Universal Search")
    hotel_name = st.text_input("🏨 Hotel Name", "Wyndham Garden Salalah", key="h"+rk)
    city_name = st.text_input("📍 City/Location", "Salalah, Oman", key="c"+rk)
    
    d1 = st.date_input("Check-In Date", date.today(), key="d1"+rk)
    d2 = st.date_input("Check-Out Date", date.today(), key="d2"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.success(f"**Stay Nights: {m_nights}**")
    
    st.divider()
    st.markdown("### 🌐 Pillar 02: Market Sentinel")
    m_state = st.radio("Market Demand Category", ["Distressed / Crisis", "Stagnant / Recovery", "Peak / Seasonal", "Compression / Sold Out"], index=1, key="ms"+rk)
    m_heat = {"Distressed / Crisis": 0.65, "Stagnant / Recovery": 1.0, "Peak / Seasonal": 1.35, "Compression / Sold Out": 1.65}[m_state]

    st.markdown("### 📊 Pillar 03: Velocity")
    otb_occ = st.slider("OTB Occupancy %", 0, 100, 15, key="otb"+rk)
    avg_hist = st.slider("Historical Avg %", 0, 100, 45, key="hist"+rk)
    v_mult = 1.25 if otb_occ > avg_hist else 0.85 if otb_occ < (avg_hist - 15) else 1.0

    st.divider()
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx"+rk)
    ota_comm = st.slider("OTA Commission %", 0, 40, 18, key="comm"+rk)
    p01_fee = st.number_input("P01 Variable Fee", 0.0, value=6.90, key="p01"+rk)

    st.markdown("### 🍽️ Unit Costs (Pillar 01)")
    c_bb = st.number_input("BB Cost", 0.0, key="cbb"+rk)
    c_hb = st.number_input("HB Cost", 2.5, key="chb"+rk)
    c_fb = st.number_input("FB Cost", 5.0, key="cfb"+rk)
    c_sai = st.number_input("SAI Cost", 7.5, key="csai"+rk)
    c_ai = st.number_input("AI Cost", 10.0, key="cai"+rk)
    meal_costs = {"RO": 0, "BB": c_bb, "HB": c_hb, "FB": c_fb, "SAI": c_sai, "AI": c_ai}

# --- 4. GOOGLE INTELLIGENCE LOGIC ---
intel_db = {
    "Salalah": {"ev": "Khareef Festival (Monsoon)", "fl": "+18% Surge", "basis": "Weather-Driven Demand"},
    "Dubai": {"ev": "Shopping Festival / Global Village", "fl": "+25% Global Influx", "basis": "Peak Business Synergy"},
    "Muscat": {"ev": "Opera House Season", "fl": "+10% Regional Traffic", "basis": "Cultural Tourism Peaks"},
    "London": {"ev": "Wimbledon / Fashion Week", "fl": "Heathrow Slot Capacity 98%", "basis": "Global Hub Supply Constraints"}
}
active_intel = next((v
