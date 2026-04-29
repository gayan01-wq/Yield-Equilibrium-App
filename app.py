import streamlit as st
from datetime import date

# --- 1. CORE STYLING ---
st.set_page_config(layout="wide", page_title="Displacement Analyzer | Yield Equilibrium")
st.markdown("""<style>
.block-container{padding-top:1rem!important;}
.header-container {text-align: center; width: 100%; margin-bottom: 25px;}
.main-title {font-size: 2.2rem!important; font-weight: 900; color: #1e3799; text-transform: uppercase; margin: 0;}
.main-subtitle {font-size: 1.1rem!important; font-weight: 600; color: #4b6584; margin-top: 5px; margin-bottom: 25px;}
.card{padding:15px; border-radius:10px; margin-bottom:15px; border-left:12px solid #1e3799; background:#ffffff; box-shadow: 0 2px 5px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff; padding:15px; border-radius:10px; border:1px solid #d1d9e6;}
.status-indicator{padding:10px; border-radius:8px; text-align:center; font-weight:900; color:white; margin-top:10px; font-size:1.1rem;}
[data-testid="stSidebar"]{background:#f1f4f9;}
.contact-section{background:#1e3799; padding:25px; border-radius:15px; margin-top:30px; color:white;}
</style>""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    st.markdown("<div class='header-container'><h1 class='main-title'>EQUILIBRIUM ENGINE</h1></div>", unsafe_allow_html=True)
    with st.form("login"):
        if st.text_input("Access Key", type="password") == "Gayan2026" and st.form_submit_button("Unlock"):
            st.session_state["auth"] = True; st.rerun()
    st.stop()

# --- 3. SIDEBAR (RESTORED DATES & GLOBAL INPUTS) ---
with st.sidebar:
    st.markdown("### 👤 System Developer\nGayan Nugawela")
    if st.button("🧹 Reset Cache"): st.rerun()
    st.divider()
    
    cur = st.selectbox("Base Currency", ["OMR (﷼)", "LKR (රු)", "THB (฿)", "AED (د.إ)", "SAR (﷼)", "INR (₹)", "USD ($)", "EUR (€)", "GBP (£)"])
    cur_sym = cur.split('(')[1].replace(')', '')
    
    city = st.text_input("Analysis City", "Salalah")
    
    # Restored Check-In / Check-Out in the sidebar
    col_d1, col_d2 = st.columns(2)
    d1 = col_d1.date_input("Check-In", date.today())
    d2 = col_d2.date_input("Check-Out", date.today())
    m_nts = (d2 - d1).days if (d2 - d1).days > 0 else 1
    st.info(f"📅 Total Length of Stay: **{m_nts} Nights**")
    
    st.divider()
    otb, hst = st.slider("OTB %", 0, 100, 15), st.slider("Hist %", 0, 100, 45)
    v_mult = 1.35 if otb > hst else 0.85 if otb < (hst - 15) else 1.0
    tx = st.number_input("Tax Divisor", 1.2327, format="%.4f")
    ota_p = st.slider("OTA Commission %", 0, 40, 15)
    p01 = st.number_input(f"P01 Fee ({cur_sym})", value=6.90)
    
    st.markdown("### 🍽️ Unit Costs")
    mc = {p: st.number_input(f"{p} Cost", v) for p, v in {"BB":2.5, "LN":4.5, "DN":5.5, "SAI":8.5, "AI":10.5}.items()}

# --- 4. ENGINE (FIXED ROOM NIGHT CALCULATION) ---
def run_yield(rms_list, adr, meals, hurdle, demand, is_ota=False, mice=0, lndry=0, trans=0):
    total_rooms = sum(rms_list)
    if total_rooms <= 0: return None
    
    # Demand Adjustment logic
    eff_h = hurdle + {"Compression (Peak)": 15, "High Flow": 5, "Standard": 0, "Distressed": -5}.get(demand, 0)
    
    # Wealth Deconstruction
    net_adr = adr / tx
    comm = (net_adr * (ota_p/100)) if is_
