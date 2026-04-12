import streamlit as st
import pandas as pd

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
    st.set_page_config(layout="wide", page_title="Yield Equilibrium SME")
    
    # --- FIXED HIGH-CONTRAST STYLING ---
    st.markdown("""
        <style>
        .stApp { background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); }
        [data-testid="stSidebar"] { background-color: #0e1117 !important; }
        /* Force Sidebar text to be readable */
        [data-testid="stSidebar"] p, [data-testid="stSidebar"] span, [data-testid="stSidebar"] label { 
            color: white !important; 
        }
        .stMetric { background: rgba(255, 255, 255, 0.9); border-radius: 15px; padding: 10px; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
        .card { padding: 12px; border-radius: 12px; margin-bottom: 10px; border-left: 10px solid; 
                font-weight: bold; background: white; color: #1e3a8a; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
        h1, h2, h3 { color: #1e3a8a; }
        /* Fix for status visibility */
        .status-box { padding: 4px 8px; border-radius: 4px; font-weight: bold; color: white !important; text-shadow: 1px 1px 2px black; }
        </style>
    """, unsafe_allow_html=True)
    
    with st.sidebar:
        st.markdown("<h2 style='color:#60a5fa;'>Architect</h2>", unsafe_allow_html=True)
        st.markdown("<h3 style='color:white;'>Gayan Nugawela</h3>", unsafe_allow_html=True)
        st.markdown("<p style='color:#cbd5e1;'>MBA | CRME | CHRM | RevOps</p>", unsafe_allow_html=True)
        st.divider()
        h_inv = st.number_input("Total Inventory", 1, 1000, 237)
        st.markdown("### 🍽️ Meals (Net)")
        b = st.number_input("BB", 0.0, 500.0, 2.0)
        l = st.number_input("LN", 0.0, 500.0, 6.0)
        d = st.number_input("DN", 0.0, 500.0, 6.0)
        s = st.number_input("SAI", 0.0, 500.0, 8.0)
        a = st.number_input("AI", 0.0, 500.0, 15.0)
        m = {"RO":0, "BB":b, "HB":b+d, "FB":b+l+d, "SAI":b+l+d+s, "AI":b+l+d+s+a}
        p01 = st.number_input("P01 Fee", 0.0, 100.0, 6.9)
        tx = st.number_input("Tax Divisor", 1.0, 2.0, 1.2327)
        op = st.slider("OTA Comm %", 0, 50, 18) / 100
        cu = st.selectbox("Currency", ["OMR", "AED", "SAR", "EUR", "USD"])

    st.title("🏨 Yield Equilibrium Center")

    def run_logic(rms, adr, nts, mix, cp, fl, ev_r=0, tr_c=0):
        t_rms = sum(rms)
        if t_rms <= 0: return None
        pax = (rms[0]*1 + rms[1]*2 + rms
