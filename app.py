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
    # --- UNIVERSAL PREMIUM STYLING ---
    st.set_page_config(layout="wide", page_title="Yield Equilibrium SME")
    
    st.markdown("""
        <style>
        /* Main Background Gradient */
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #0e1117 !important;
            color: white;
        }
        /* Metric Cards */
        .stMetric {
            background: rgba(255, 255, 255, 0.8);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.3);
            padding: 15px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        }
        /* Segment Cards */
        .card {
            padding: 12px;
            border-radius: 12px;
            margin-bottom: 10px;
            border-left: 10px solid;
            font-weight: bold;
            background: rgba(255, 255, 255, 0.6);
            box-shadow: 2px 2px 5px rgba(0,0,0,0.03);
        }
        h1, h2, h3 {
            color: #1e3a8a;
        }
        </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("<h2 style='color:white;'>👨‍💼 Architect</h2>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:#60a5fa; margin-bottom:0;'>Gayan Nugawela</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color:white; font-size:14px;'>MBA | CRME | CHRM | RevOps</p>", unsafe_allow_html=True)
        st.caption("Revenue Management Expert & SME")
        st.divider()
        
        st.title("⚙️ Global Settings")
        h_nm = st.text_input("Hotel Entity", "Global Portfolio Audit")
        h_cp = st.number_input("Total Inventory", 1, 1000, 158)
        
        st.markdown("### 🍽️ Meals (Net)")
        b, l, d = st.number_input("BB", 0., 500., 2.), st.number_input("LN", 0., 500., 6.), st.number_input("DN", 0., 500., 6.)
        s, a = st.number_input("SAI", 0., 500
