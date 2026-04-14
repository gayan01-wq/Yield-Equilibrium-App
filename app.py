import streamlit as st

# --- 1. CONFIG & STYLE ---
st.set_page_config(layout="wide", page_title="Yield Equilibrium")

st.markdown("""
<style>
    .main-title { font-size: 2.5rem; font-weight: 900; color: #1e3799; text-align: center; margin-bottom: 20px; }
    .card { padding: 12px; border-radius: 10px; margin-bottom: 15px; border-left: 10px solid; font-weight: bold; background: #fcfcfc; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .status-box { padding: 15px; border-radius: 12px; text-align: center; font-size: 1.3rem; font-weight: bold; margin-bottom: 10px; }
    .exposure-bar { padding: 10px; border-radius: 8px; font-weight: bold; text-align: center; color: white; margin-top: 5px; line-height: 1.2; }
    [data-testid="stSidebar"] { background-color: #f1f4f9; border-right: 1px solid #ddd; }
</style>
""", unsafe_allow_html=True)

# --- 2. AUTH ---
if "auth" not in st.session_state: st.session_state["auth"] = False
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

# --- 3. RESET ---
def reset_db():
    for k in list(st.session_state.keys()):
        if any(x in k for x in ["fit", "ota", "corp", "cgrp", "tnt"]):
            if "n" in k: st.session_state[k] = 1
            elif "a" in k or "f" in k: pass 
            else: st.session_state[k] = 0
    st.rerun()

# --- 4. SIDEBAR ---
with st.sidebar:
    st.markdown("<h3 style='color: #1e3799; margin-bottom: 0;'>Strategic Architect</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("🔒 Logout"):
        st.session_state["auth"] = False
        st.rerun()
    if c2.button("🔄 EMPTY ALL"): reset_db()
    
    st.divider()
    h_name = st.text_input("Hotel Identity", "Wyndham Garden Salalah")
    h_total = st.number_input("Total Inventory", 1, 5000, 237)
    cu = st.selectbox("Currency", ["OMR", "USD", "AED", "SAR", "LKR"])
    st.divider()
    p01 = st.number_input("P01 Fixed Fee", 0.0, 100.0, 6.90)
    tx = st.number_input("Tax Divisor", 1.0, 3.0, 1.2327)
    ota_p = st.slider("OTA Commission %", 0, 50, 18) / 100
    
    st.write("### 🍽️ Meal Allocations")
    m_bb = st.number_input("Breakfast (BB)", value=2.0)
    m_ln = st.number_input("Lunch (LN)", value=4.0)
