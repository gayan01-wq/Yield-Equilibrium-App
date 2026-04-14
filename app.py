import streamlit as st

# --- 1. CONFIG & PREMIUM STYLING ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

st.markdown("""
    <style>
    .main-title { font-size: 3rem !important; font-weight: 900; color: #1e3799; text-align: center; margin-bottom: 0px; }
    .sub-header { font-size: 1.1rem; text-align: center; color: #4a69bd; font-weight: 600; margin-bottom: 20px; letter-spacing: 1px; }
    .card { padding: 15px; border-radius: 12px; margin-bottom: 15px; border-left: 10px solid; font-weight: bold; background-color: #fcfcfc; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .status-box { padding: 20px; border-radius: 15px; text-align: center; font-size: 1.5rem; font-weight: bold; margin: 10px 0; border: 1px solid rgba(0,0,0,0.1); }
    .exposure-bar { padding: 10px; border-radius: 8px; font-weight: bold; margin-top: 10px; text-align: center; color: white; }
    [data-testid="stSidebar"] { background-color: #f1f4f9; border-right: 2px solid #3498db; }
    </style>
""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth_key" not in st.session_state:
    st.session_state["auth_key"] = False

if not st.session_state["auth_key"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login_form"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock Dashboard"):
            if pwd == "Gayan2026":
                st.session_state["auth_key"] = True
                st.rerun()
            else: st.error("Invalid Key")
    st.stop()

# --- 3. RESET LOGIC ---
def reset_dashboard():
    for key in list(st.session_state.keys()):
        if any(x in key for x in ["fit", "ota", "corp", "cgrp", "tnt"]):
            if "n" in key:
                st.session_state[key] = 1
            elif "adr" not in key and "fl" not in key:
                st.session_state[key] = 0
    st.rerun()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<p style='font-size: 1.4rem; font-weight: 800; color:
