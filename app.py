import streamlit as st
from datetime import date

# --- STYLING & CONFIG ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium Master Engine")

st.markdown("""<style>
.block-container{padding-top:1rem!important}
.main-title{font-size:2.5rem!important;font-weight:900;color:#1e3799;text-align:center;margin-top:-10px}
.sub-header{font-size:1rem;text-align:center;color:#4a69bd;font-weight:600;margin-bottom:15px}
.pillar-box{background:#fff;padding:12px;border-radius:10px;border-top:4px solid #1e3799;text-align:center;box-shadow:0 4px 10px rgba(0,0,0,0.05);min-height:100px}
.pillar-box h4{color:#1e3799;font-size:0.9rem;margin:0}
.card{padding:12px;border-radius:10px;margin-bottom:10px;border-left:10px solid;font-weight:bold;background:#fcfcfc}
.pricing-row{background:#f1f4f9;padding:10px;border-radius:8px;margin-top:8px;border:1px solid #1e3799}
.pricing-header{background:#1e3799;color:white;padding:3px 10px;border-radius:5px 5px 0 0;font-size:0.8rem;font-weight:bold;margin-bottom:5px}
.status-box{padding:12px;border-radius:12px;text-align:center;font-size:1.3rem;font-weight:bold;color:white;margin-bottom:8px}
.exposure-bar{padding:8px;border-radius:6px;font-weight:bold;text-align:center;color:#1e3799;background:#ffc107;margin-top:6px;font-size:0.85rem}
.sentinel-box{background:#1e3799; color:white; padding:15px; border-radius:10px; margin-bottom:20px; border-left:10px solid #ffc107;}
div.stButton>button:first-child[aria-label="🔄 Empty Data"]{background:#4b6584!important;color:white!important}
[data-testid="stSidebar"]{background:#f1f4f9;border-right:2px solid #3498db}
</style>""", unsafe_allow_html=True)

# --- AUTHENTICATION ---
if "auth" not in st.session_state: st.session_state["auth"] = False
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

# --- SIDEBAR: CONTROL CENTER & PILLAR 03 ---
with st.sidebar:
    st.markdown("<p style='font-size:1.2rem;font-weight:800;color:#1e3799;margin:0;'>Gayan Nugawela</p><p style='font-size:0.8rem;margin:0;'>Strategic Revenue Architect</p><p style='font-size:0.7rem;color:#7f8c8d;'>© 2026 All Rights Reserved</p>", unsafe_allow_html=True)
    st.divider()
    
    if st.button("🔒 Sign Out"):
        st.session_state["auth"] = False
        st.rerun()
        
    st.divider()
    hotel = st.text_input("Property", "Wyndham Garden Salalah")
    h_tot = st.number_input("Inventory", 1, 5000, 237)
    
    st.write("### 📅 Stay Intelligence")
    d1 = st.date_input("Check-In", date.today())
    d2 = st.date_input("Check-Out", date
