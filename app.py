import streamlit as st
from datetime import date

# --- STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Master Engine")
st.markdown("""<style>
.block-container{padding-top:1rem!important}
.main-title{font-size:2.5rem!important;font-weight:900;color:#1e3799;text-align:center;margin-top:-10px}
.card{padding:12px;border-radius:10px;margin-bottom:10px;border-left:10px solid;font-weight:bold;background:#fcfcfc}
.pricing-row{background:#f1f4f9;padding:10px;border-radius:8px;margin-top:8px;border:1px solid #1e3799}
.pricing-header{background:#1e3799;color:white;padding:3px 10px;border-radius:5px 5px 0 0;font-size:0.8rem;font-weight:bold;margin-bottom:5px}
.status-box{padding:12px;border-radius:12px;text-align:center;font-size:1.3rem;font-weight:bold;color:white;margin-bottom:8px}
.sentinel-box{background:#1e3799; color:white; padding:20px; border-radius:10px; margin-bottom:20px; border-left:10px solid #ffc107;}
.guide-box{background:#f8f9fa; padding:25px; border-radius:15px; border:1px solid #dee2e6; margin-top:40px;}
[data-testid="stSidebar"]{background:#f1f4f9;border-right:2px solid #3498db}
</style>""", unsafe_allow_html=True)

# --- AUTH ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock"):
            if pwd == "Gayan2026": st.session_state["auth"] = True; st.rerun()
            else: st.error("Denied")
    st.stop()

# --- SIDEBAR ---
with st.sidebar:
    st.markdown("<p style='font-size:1.2rem;font-weight:800;color:#1e3799;margin:0;'>Gayan Nugawela</p><p style='font-size:0.8rem;margin:0;'>Strategic Revenue Architect</p>", unsafe_allow_html=True); st.divider()
    hotel = st.text_input("📍 Targeted Property", "Wyndham Garden Salalah")
    h_tot = st.number_input("Inventory", 1, 5000, 237)
    
    st.write("### 📅 Stay Intelligence")
    today = date.today()
    d1 = st.date_input("Check-In", today)
    d2 = st.date_input("Check-Out", today)
    stay_n = (d2 - d1).days if (d2 - d1).days > 0 else 1
    
    # KHAREEF AUTOMATION LOGIC
    is_khareef = "Salalah" in hotel and (d1.month in [6, 7, 8, 9])
    
    st.write("### 🌐 Market Condition")
    default_state = "Peak Season" if is_khareef else "Global/Local Crisis"
    market_state = st.radio("Sentinel Scrape Status", ["Global/Local Crisis", "Stagnant", "Recovering", "Peak Season"], index=(3 if is_khareef else 0))
    m_logic = {"Global/Local Crisis": 0.65, "Stagnant": 0.85, "Recovering": 1.0, "Peak Season": 1.35}
    m_heat = m_logic[market_state]
    
    st.write("### 📈 Velocity Valve (P03)")
    otb_occ = st.slider("Current OTB %", 0, 100, (70 if is_khareef else 15))
    hist_occ = st.slider("Historical Avg %", 0, 100, 45)
    v_delta = otb_occ - hist_occ
    v_mult = 1.25 if v_delta > 10 else 1.10 if v_delta > 0 else 0.85 if v_delta > -10 else 0.70

    st.divider()
    cu = st.selectbox("Currency", ["OMR","AED","SAR","USD"])
    tx = st.number_input("Tax Divisor", 1.2327, format="%.4f")
    ota_p = st.slider("OTA Commission %", 0, 50, 18) / 100
    m_costs = {"RO": 0.0, "BB": st.number_input("BB", 0.0), "HB":
