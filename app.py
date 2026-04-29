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
.google-window{background:#e8f0fe; padding:12px; border-radius:10px; border:2px solid #4285f4; margin-bottom:15px; font-size:0.85rem;}
.status-indicator{padding:10px; border-radius:10px; text-align:center; font-weight:900; font-size:1.2rem; color:white; margin-top:10px;}
[data-testid="stSidebar"]{background:#f1f4f9; border-right:1px solid #dee2e6}
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

# --- 3. SIDEBAR (GLOBAL SELECTION UPGRADE) ---
with st.sidebar:
    st.markdown("### 👤 Strategic Architect\nGayan Nugawela")
    if st.button("☢️ Nuclear Data Reset"):
        st.session_state["reset_key"] += 1
        st.rerun()
    st.divider()
    
    rk = str(st.session_state["reset_key"]) 
    
    st.markdown("### 🏨 Pillar 01: Google Sync Entry")
    # NEW: Global Hotel Search Simulation
    hotel_sync = st.text_input("🏨 Search Hotel (Google Sync)", "Wyndham Garden Salalah", key="h_sync"+rk)
    
    # NEW: Global City Search Simulation
    location_sync = st.text_input("📍 Search City/Location", "Salalah, Oman", key="l_sync"+rk)
    
    st.divider()
    # NEW: Date Alignment (Check-in, Check-out, and Nights below)
    d1 = st.date_input("📅 Check-In", date.today(), key="d1"+rk)
    d2 = st.date_input("📅 Check-Out", date.today(), key="d2"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.success(f"**Total Stay Nights: {m_nights}**")
    
    st.divider()
    st.markdown("### ⚙️ Operational Parameters")
    ota_comm_pct = st.slider("OTA Commission %", 0, 40, 18, key="comm"+rk)
    tx_div = st.number_input("Tax Divisor", value=1.2327, format="%.4f", key="tx"+rk)
    p01_fee = st.number_input("P01 Variable Fee", 0.0, value=6.90, key="p01"+rk)
    
    st.markdown("### 📈 Pillar 03: Pace")
    otb_occ = st.slider("OTB Occupancy %",
