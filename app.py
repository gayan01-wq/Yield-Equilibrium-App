import streamlit as st
import pandas as pd

# --- ACCESS CONTROL ---
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
    # --- EXECUTIVE STYLING ---
    st.set_page_config(layout="wide", page_title="Yield Equilibrium SME")
    
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
        [data-testid="stSidebar"] { background-color: #0e1117 !important; color: white; }
        .stMetric { background: rgba(255, 255, 255, 0.8); backdrop-filter: blur(10px); border-radius: 15px; padding: 15px; }
        .card { padding: 12px; border-radius: 12px; margin-bottom: 10px; border-left: 10px solid; font-weight: bold; background: rgba(255, 255, 255, 0.6); color: #1e3a8a; }
        h1, h2, h3 { color: #1e3a8a; }
        </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("<h2 style='color:white;'>👨‍💼 Architect</h2>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#60a5fa; margin-bottom:0;'>Gayan Nugawela</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color:white; font-size:14px;'>MBA | CRME | CHRM | RevOps</p>", unsafe_allow_html=True)
        st.divider()
        h_inv = st.number_input("Total Property Inventory", 1, 1000, 158)
        st.markdown("### 🍽️ Meals (Net)")
        b, l, d = st.number_input("BB", 0.0, 500.0, 2.0), st.number_input("LN", 0.0, 500.0, 6.0), st.number_input("DN", 0.0, 500.0, 6.0)
        s, a = st.number_input("SAI", 0.0, 500.0, 8.0), st.number_input("AI", 0.0, 500.0, 15.0)
        m = {"RO":0, "BB":b, "HB":b+d, "FB":b+l+d, "SAI":b+l+d+s, "AI":b+l+d+s+a}
        p01 = st.number_input("P01 Fee", 0.0, 100.0, 6.9)
        tx = st.number_input("Tax Divisor", 1.0, 2.0, 1.23
