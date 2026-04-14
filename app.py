import streamlit as st

# --- 1. CONFIG ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

st.markdown("<style>.main-title { font-size: 2.5rem; font-weight: 900; color: #1e3799; text-align: center; } .card { padding: 10px; border-radius: 10px; margin-bottom: 10px; border-left: 10px solid; font-weight: bold; background: #fcfcfc; } .status-box { padding: 15px; border-radius: 12px; text-align: center; font-size: 1.2rem; font-weight: bold; } .exposure-bar { padding: 8px; border-radius: 5px; font-weight: bold; text-align: center; color: white; margin-top: 5px; }</style>", unsafe_allow_html=True)

# --- 2. AUTH ---
if "auth_key" not in st.session_state: 
    st.session_state["auth_key"] = False

if not st.session_state["auth_key"]:
    st.markdown("<h1 class='main-title'>EQUILIBRIUM ENGINE</h1>", unsafe_allow_html=True)
    with st.form("login"):
        pwd = st.text_input("Access Key", type="password")
        if st.form_submit_button("Unlock"):
            if pwd == "Gayan2026":
                st.session_state["auth_key"] = True
                st.rerun()
            else: st.error("Wrong Key")
    st.stop()

# --- 3. HARD RESET FUNCTION ---
def reset_dashboard():
    for k in list(st.session_state.keys()):
        # Targeted reset for all segment inputs
        if any(x in k for x in ["fit", "ota", "corp", "cgrp", "tnt"]):
            if "n" in k:
                st.session_state[k] = 1 # Reset nights to 1
            elif "a" in k or "f" in k:
                pass # Keep ADR and Floor as they are defaults
            else:
                st.session_state[k] = 0 # Empty all occupancy and meal inputs
    st.rerun()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.write("### Strategic Architect")
    c_out, c_res = st.columns(2)
    if c_out.button("🔒 Logout"):
        st.
