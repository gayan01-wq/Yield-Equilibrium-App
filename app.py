import streamlit as st

# --- 1. CONFIG & PREMIUM STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

st.markdown("""
<style>
    .main-title { font-size: 3rem !important; font-weight: 900; color: #1e3799; text-align: center; margin-bottom: 0px; }
    .sub-header { font-size: 1.1rem; text-align: center; color: #4a69bd; font-weight: 600; margin-bottom: 20px; letter-spacing: 1px; }
    .definition-box { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); padding: 20px; border-radius: 15px; border-left: 8px solid #1e3799; margin-bottom: 25px; box-shadow: 0px 4px 15px rgba(0,0,0,0.05); }
    .pillar-box { background-color: #ffffff; padding: 15px; border-radius: 10px; border-top: 4px solid #1e3799; text-align: center; box-shadow: 0px 4px 10px rgba(0,0,0,0.05); min-height: 120px; }
    .pillar-box h4 { margin-top: 0; color: #1e3799; font-size: 1rem; }
    .pillar-box p { font-size: 0.85rem; color: #555; line-height: 1.2; }
    .card { padding: 15px; border-radius: 12px; margin-bottom: 15px; border-left: 10px solid; font-weight: bold; background-color: #fcfcfc; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .status-box { padding: 15px; border-radius: 15px; text-align: center; font-size: 1.4rem; font-weight: bold; color: white; margin-bottom: 10px; }
    .insight-box { padding: 12px; border-radius: 10px; font-size: 0.9rem; border: 1px solid #ddd; background: #ffffff; line-height: 1.4; }
    .exposure-bar { padding: 10px; border-radius: 8px; font-weight: bold; text-align: center; color: white; margin-top: 8px; font-size: 0.9rem; }
    .crisis-alert { background-color: #fff3cd; color: #856404; padding: 15px; border-radius: 10px; border: 1px solid #ffeeba; font-weight: bold; text-align: center; margin-bottom: 20px; }
    [data-testid="stSidebar"] { background-color: #f1f4f9; border-right: 2px solid #3498db; }
</style>
""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state: st.session_state["auth"] = False
if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock Dashboard"):
            if pwd == "Gayan2026":
                st.session_state["auth"] = True
                st.rerun()
            else: st.error("Access Denied")
    st.stop()

# --- 3. SIDEBAR ---
with st.sidebar:
    st.markdown("<h2 style='color:#1e3799; margin-bottom:0;'>Control Center</h2>", unsafe_allow_html=True)
    
    # SIGN OUT & RESET
    col_auth = st.columns(2)
    if col_auth[0].button("🔒 Sign Out"):
        st.session_state["auth"] = False
        st.rerun()
    if col_auth[1].button("🔄 Empty Data", type="primary"):
        for k in list(st.session_state.keys()):
            if any(seg in k for seg in ["fit", "ota", "corp", "cgrp", "tnt"]):
                if k.endswith("n"): st.session_state[k] = 1
                elif k.endswith("a
