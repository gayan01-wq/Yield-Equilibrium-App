import streamlit as st

# --- 1. CONFIG & STYLE ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

st.markdown("""
<style>
    .main-title { font-size: 2.2rem; font-weight: 900; color: #1e3799; text-align: center; }
    .card { padding: 10px; border-radius: 10px; margin-bottom: 10px; border-left: 10px solid; font-weight: bold; background: #fcfcfc; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .status-box { padding: 15px; border-radius: 12px; text-align: center; font-size: 1.2rem; font-weight: bold; }
    .exposure-bar { padding: 8px; border-radius: 5px; font-weight: bold; text-align: center; color: white; margin-top: 5px; }
    [data-testid="stSidebar"] { background-color: #f1f4f9; }
</style>
""", unsafe_allow_html=True)

# --- 2. AUTHENTICATION ---
if "auth" not in st.session_state: 
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock"):
            if pwd == "Gayan2026":
                st.session_state["auth"] = True
                st.rerun()
            else: st.error("Access Denied")
    st.stop()

# --- 3. RESET LOGIC ---
def reset_db():
    for k in list(st.session_state.keys()):
        if any(x in k for x in ["fit", "ota", "corp", "cgrp", "tnt"]):
            if "n" in k: st.session_state[k] = 1
            elif "a" in k or "f" in k: pass 
            else: st.session_state[k] = 0
    st.rerun()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.write("### Strategic Architect")
    c1, c2 = st.columns(2)
    if c1.button("🔒 Logout"):
        st.session_state["auth"] = False
        st.rerun()
    if c2.button("🔄 EMPTY ALL"): 
        reset_db()
    
    st.divider()
    h_name = st.text_input("Hotel", "Wyndham Garden Salalah")
    h_total
