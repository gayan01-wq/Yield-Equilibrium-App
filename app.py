import streamlit as st
from datetime import date

# --- 1. CORE CONFIG & STYLING ---
st.set_page_config(layout="wide", page_title="Displacement Analyzer")

# Simple styling to ensure visibility
st.markdown("""<style>
.main-title{font-size:2.5rem; font-weight:900; color:#1e3799; text-align:center;}
.card{padding:15px; border-radius:10px; border-left:10px solid #1e3799; background:#f8f9fa; margin-bottom:10px;}
[data-testid="stSidebar"]{background:#f1f4f9;}
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
            else: st.error("Access Denied")
    st.stop()

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("### 👤 System Developer\nGayan Nugawela")
    if st.button("🧹 Reset System"):
        st.session_state["reset_key"] += 1
        st.rerun()
    st.divider()
    
    rk = str(st.session_state["reset_key"])
    cur_sym = st.selectbox("Currency", ["﷼", "රු", "฿", "$"], key="c_"+rk)
    city = st.text_input("City", "Salalah", key="ct_"+rk)
    d1 = st.date_input("Check-In", date.today(), key="d1_"+rk)
    d2 = st.date_input("Check-Out", date.today(), key="d2_"+rk)
    m_nights = (d2 - d1).days if (d2 - d1).days > 0 else 1
    inventory = st.number_input("Capacity", 1, 1000, 237, key="inv_"+rk)
    
    st.divider()
    otb = st.slider("OTB %", 0, 100, 15, key="otb_"+rk)
    hst = st.slider("Hist %", 0, 100, 45, key="hst_"+rk)
    v_mult = 1.35 if otb > hst else 0.85 if otb < (hst - 15) else 1.0
    
    tx_div = st.number_input("Tax Divisor", 1.0, 2.0, 1.2327, format="%.4f", key="tx_"+rk)
    ota_c = st.slider("OTA Comm %", 0, 40, 15, key="ota_"+rk)
    
    st.markdown("### 🍽️ Unit Costs")
    bb_c = st.number_input("BB Cost", 0.0, format="%.3f", key="bb_"+rk)
    ai_c = st.number_input("AI Cost", 0.0, format="%.3f", key="ai_"+rk)

# --- 4. ENGINE ---
def calculate(rms, adr, hurdle, demand, comm=0.0):
    tr = sum(rms)
    if tr <= 0: return None
    
    d_adj = {"Compression (Peak)": 15.0, "High Flow": 5.0, "Standard": 0.0, "Distressed": -5.0}
    eff_hurdle = hurdle + d_adj.get(demand, 0)
    
    net_adr = adr / tx_div
    # Simplified cost check for visibility
    unit_w = (net_adr - bb_c - (net_adr * comm)) - 6.90 
    
    color = "#27ae60" if unit_w >= eff_hurdle else "#e74c3c"
    status = "ACCEPT" if unit_w >= eff_hurdle else "REJECT"
    
    return {"w": unit_w, "st": status, "cl": color, "total": unit_w * tr * m_nights}

# --- 5. DASHBOARD ---
st.markdown("<h1 class='main-title'>DISPLACEMENT ANALYZER</h1>", unsafe_allow_html=True)
st.info(f"Analysis for {city} | Velocity: {v_mult}x | Duration: {m_nights} Nights")

def draw_section(label, key, base_adr, base_hurdle, is_ota=False):
    st.markdown(f"<div class='card'><b>{label}</b></div>", unsafe_allow_
