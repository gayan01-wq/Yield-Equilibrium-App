import streamlit as st
from datetime import date

# --- 1. STYLING (Professional Market Intelligence Theme) ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Master")
st.markdown("""<style>
.block-container{padding-top:1rem!important;}
.main-title{font-size:1.8rem!important;font-weight:900;color:#1e3799;text-align:center;margin-top:-10px;}
.card{padding:10px;border-radius:10px;margin-bottom:8px;border-left:10px solid;background:#ffffff;box-shadow: 0 2px 4px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff;padding:12px;border-radius:10px;border:1px solid #d1d9e6; margin-top:5px;}
.google-window{background:#e8f0fe; padding:18px; border-radius:12px; border:2px solid #4285f4; margin-bottom:15px; font-size:0.85rem; line-height:1.6;}
.news-item{background:#ffffff; border-radius:8px; padding:12px; margin-bottom:8px; border-left:4px solid #ff4b4b; box-shadow: 0 1px 3px rgba(0,0,0,0.05);}
.status-indicator{padding:12px; border-radius:10px; text-align:center; font-weight:900; font-size:1.1rem; color:white; margin-top:10px;}
.reason-box{background:#fff9c4; border:1px solid #fbc02d; padding:10px; border-radius:8px; margin-top:5px; text-align:left; font-weight:500; color:#5f4300; font-size:0.8rem;}
.theory-box{background:#f9f9f9; padding:30px; border-radius:15px; border:1px solid #dee2e6; margin-top:40px}
[data-testid="stSidebar"]{background:#f1f4f9; border-right:1px solid #dee2e6}
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION & SESSION ---
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

# --- 3. SIDEBAR (GLOBAL INPUTS) ---
with st.sidebar:
    st.markdown("### 👤 Strategic Architect\nGayan Nugawela")
    if st.button("🧹 Clear Global Cache"):
        st.session_state["reset_key"] += 1
        st.rerun()
    st.divider()
    
    rk = str(st.session_state["reset_key"]) 
    
    currencies = {
        "OMR (﷼)": "﷼", "LKR (රු)": "රු", "THB (฿)": "฿", "AED (د.إ)": "د.إ", 
        "SAR (﷼)": "﷼", "INR (₹)": "₹", "CNY (¥)": "¥", "SGD ($)": "$", 
        "MYR (RM)": "RM", "USD ($)": "$", "GBP (£)": "£", "EUR (€)": "€"
    }
    cur_choice = st.selectbox("🌍 Base Operating Currency", list(currencies.keys()), key="cur"+rk)
    cur_sym = currencies[cur_choice]
    cur_code = cur_choice.split(" ")[0]

    hotel_name = st.text_input("🏨 Hotel Name", "Wyndham Garden Salalah", key="h"+rk)
    city_name = st.text_input("📍 City Search", "Salalah, Oman", key="c"+rk)
    
    d1 = st.date_input("Check-In", date.today(), key="d1"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d2"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    
    inventory = st.number_input("Total Capacity (Rooms)", 1, 1000, 237, key="inv"+rk)
    st.info(f"**Max Capacity: {inventory * m_nights} RN**")
    
    st.divider()
    st.markdown("### 📊 Pillar 03: Velocity (ADW Pace)")
    otb_occ = st.slider("OTB % (Date-Specific)", 0, 100, 15, key="otb"+rk)
    avg_hist = st.slider("Hist. Benchmark % (LY ADW)", 0, 100, 45, key="hist"+rk)
    v_mult = 1.35 if otb_occ > avg_hist else 0.85 if otb_occ < (avg_hist - 15) else 1.0

    st.divider()
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx"+rk)
    ota_comm = st.slider("OTA Commission %", 0, 40, 18, key="comm"+rk)
    p01_fee = st.number_input(f"P01 Fee ({cur_sym})", 0.0, value=6.90, key="p01"+rk)

    st.markdown("### 🍽️ Unit Costs (Pillar 01)")
    c_snk = st.number_input(f"Snack Cost ({cur_sym})", 0.0, value=1.5, key="csnk"+rk)
    meal_costs = {
        "RO": 0, "BB": st.number_input(f"BB Cost", 0.0, key="cbb"+rk),
        "HB": st.number_input(f"HB Cost", 2.5, key="chb"+rk), "FB": st.number_input(f"FB Cost", 5.0, key="cfb"+rk),
        "SAI": st.number_input(f"SAI Cost", 7.5, key="csai"+rk), "AI": st.number_input(f"AI Cost", 10.0, key="cai"+rk)
    }

# --- 4. DEEP MARKET INTELLIGENCE (PILLAR 02) ---
# REAL-TIME MOCK DATA BASED ON APRIL 29, 2026 EVENTS
intel_db = {
    "Salalah": {
        "ev": "Khareef Season Prep / Port Logistics Spike",
        "fl": "Direct Rotations via Oman Air & SalamAir. +18% Cargo/Pax Surge.",
        "news": [
            "Port of Salalah Alert: Operations restricted after drone incident; limited damage reported.",
            "Tourism Outlook: Khareef arrivals expected to surge 15% due to new regional road networks.",
            "Weather: Monsoon conditions expected within 10 days; early bookings rising."
        ],
        "basis": "Macro-Security & Seasonal Compression"
    },
    "Dubai": {
        "ev": "DIFC Q1 Growth Expansion",
        "fl": "DXB Operations at 100% Slot Scarcity. EK A380 fleet fully deployed.",
        "news": [
            "BREAKING: UAE announces exit from OPEC effective May 1st to pump more crude.",
            "DIFC Growth: 775 new companies established in Q1
