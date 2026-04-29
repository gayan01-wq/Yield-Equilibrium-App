import streamlit as st
from datetime import date

# --- 1. STYLING (The Global Executive Aesthetic) ---
st.set_page_config(layout="wide", page_title="Displacement Analyzer | Yield Equilibrium")
st.markdown("""<style>
.block-container{padding-top:1rem!important;}
.main-title{font-size:2.0rem!important;font-weight:900;color:#1e3799;text-align:center;margin-top:-10px;text-transform:uppercase;letter-spacing:2px; display: block; width: 100%;}
.main-subtitle{font-size:1.1rem!important;font-weight:600;color:#4b6584;text-align:center;margin-top:-15px;margin-bottom:25px;letter-spacing:1px; display: block; width: 100%;}
.small-framework-header{font-size:0.95rem!important; font-weight:700; color:#4b6584; text-align:center; margin-bottom:15px; letter-spacing:1px;}
.card{padding:10px;border-radius:10px;margin-bottom:8px;border-left:10px solid;background:#ffffff;box-shadow: 0 2px 4px rgba(0,0,0,0.1)}
.pricing-row{background:#f8faff;padding:12px;border-radius:10px;border:1px solid #d1d9e6; margin-top:5px;}
.google-window{background:#e8f0fe; padding:18px; border-radius:12px; border:2px solid #4285f4; margin-bottom:15px; font-size:0.85rem; line-height:1.6;}
.news-item{background:#ffffff; border-radius:8px; padding:10px; margin-bottom:8px; border-left:4px solid #ff4b4b; box-shadow: 0 1px 3px rgba(0,0,0,0.05);}
.status-indicator{padding:12px; border-radius:10px; text-align:center; font-weight:900; font-size:1.1rem; color:white; margin-top:10px;}
.reason-box{background:#fff9c4; border:1px solid #fbc02d; padding:10px; border-radius:8px; margin-top:5px; text-align:left; font-weight:500; color:#5f4300; font-size:0.8rem;}
.audit-box{font-size:0.85rem; font-weight:700; color:#1e3799; margin-top:5px; border-top: 1px dotted #d1d9e6; padding-top: 5px;}
.theory-box{background:#f9f9f9; padding:25px; border-radius:15px; border:1px solid #dee2e6; margin-top:30px}
.theory-card{background:white; padding:12px; border-radius:10px; border:1px solid #eee; margin-bottom:8px;}
[data-testid="stSidebar"]{background:#f1f4f9; border-right:1px solid #dee2e6}
.contact-section{background:#1e3799; padding:30px; border-radius:15px; margin-top:40px; color:white;}
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

# --- 3. SIDEBAR (STRATEGIC GLOBAL INPUTS) ---
with st.sidebar:
    st.markdown("### 👤 System Developer\nGayan Nugawela")
    if st.button("🧹 Clear Global Cache"):
        st.session_state["reset_key"] += 1
