import streamlit as st
import pandas as pd

# --- PASSWORD PROTECTION ---
def check_password():
    if "auth" not in st.session_state:
        st.session_state["auth"] = False
    if not st.session_state["auth"]:
        st.title("🏨 Yield Equilibrium Center")
        pwd = st.text_input("Access Key", type="password")
        if st.button("Unlock") or (pwd == "Gayan2026"): 
            st.session_state["auth"] = True
            st.rerun()
        return False
    return True

if check_password():
    st.set_page_config(layout="wide", page_title="Yield Equilibrium")
    
    st.markdown("""
        <style>
        .stMetric {background:#fff; border:1px solid #eee; padding:10px; border-radius:10px}
        .card {padding:8px; border-radius:8px; margin-bottom:5px; border-left:8px solid; font-weight:bold}
        </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.title("👨‍💼 Architect")
        st.subheader("Gayan Nugawela")
        st.write("MBA | CRME | CHRM | RevOps")
        st.caption("Revenue Management Expert & SME")
        st.divider()
        
        st.title("⚙️ Global Settings")
        h_nm = st.text_input("Hotel", "Wyndham Garden Salalah")
        h_cp = st.number_input("Total Inventory", 1, 1000, 158)
        
        st.header("🍽️ Meals (Net)")
        b = st.number_input("BB", 0., 500., 2.)
        l = st.number_input("LN", 0., 500., 6.)
        d = st.number_input("DN", 0., 500., 6.)
        s = st.number_input("SAI", 0., 500., 8.)
        a = st.number_input("AI", 0., 500., 15.)
        m = {"RO":0, "BB":b, "HB":b+d, "FB":b+l+d, "SAI":b+l+d+s, "AI":b+l+d+s+a}
        
        p01 = st.number_input("P01 Fee", 0., 100., 6.9)
        tx = st.number_input("Tax Div", 1., 2., 1.2327, format="%.4f")
        op = st.slider("OTA Comm %", 0, 50, 18) / 100
        cu = st.selectbox("Currency
